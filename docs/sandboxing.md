> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configure the sandboxed Bash tool

> Restrict the files and network hosts Claude Code's shell commands can reach with the built-in sandbox. Turn it on, set the boundary, and fix what it breaks.

The Bash sandbox is a boundary that the operating system enforces around the shell commands Claude runs on your machine. You set which files and network domains those commands can reach, and the limits apply to Bash, PowerShell, and Monitor commands and the processes they start. Because the operating system applies the limits while a command runs, Claude Code can [run sandboxed commands without asking you](#sandbox-modes) to approve each one.

The sandbox covers shell commands only. Claude's file tools, MCP servers, and hooks [run outside it](#what-runs-outside-the-sandbox).

The sandbox runs on macOS, Linux, and WSL2. On native Windows, Claude Code runs commands unsandboxed. To use the sandbox on a Windows machine, run Claude Code inside a WSL2 distribution.

<Note>
  This page covers the sandbox around shell commands on your own machine. Other pages cover related questions:

  * For how a cloud session is isolated, see [Security and isolation](/docs/en/claude-code-on-the-web#security-and-isolation)
  * To compare other isolation approaches such as dev containers, custom containers, and virtual machines, see [Sandbox environments](/docs/en/sandbox-environments)
  * To reduce permission prompts for tools other than Bash, see [permission modes](/docs/en/permission-modes)
</Note>

## What the sandbox restricts

While the sandbox is on, the shell commands Claude runs start inside its boundary, and so do the processes they start. The sandbox is off by default. To turn it on, run `/sandbox` in a session, as [Get started](#get-started) shows, or set [`sandbox.enabled`](/docs/en/settings-reference#sandbox-enabled) to `true` in a [settings file](/docs/en/settings) such as `~/.claude/settings.json`.

The table shows what a sandboxed command can reach by default and the settings that change each default.

| Access | Default | Change it with |
| :- | :- | :- |
| Writes | The working directory, a per-user temp directory, and [directories you've added](/docs/en/permissions#additional-directories-grant-file-access-not-configuration). [Protected paths](#protected-paths) stay write-denied | [`filesystem.allowWrite`](/docs/en/settings-reference#sandbox-filesystem-allowwrite), [`filesystem.denyWrite`](/docs/en/settings-reference#sandbox-filesystem-denywrite) |
| Reads | Most of the machine, including credential files such as `~/.ssh` and `~/.aws/credentials` | [`filesystem.denyRead`](/docs/en/settings-reference#sandbox-filesystem-denyread), [`credentials`](#protect-credentials) |
| Network | No direct route out. Connections go through a proxy on your machine that checks each host against your allowed domains, which start empty. Your permission mode decides [what happens to other hosts](#hosts-outside-your-allowed-domains) | [`network.allowedDomains`](/docs/en/settings-reference#sandbox-network-alloweddomains), [`network.deniedDomains`](/docs/en/settings-reference#sandbox-network-denieddomains) |
| Environment variables | Inherited from Claude Code, including any secrets in its environment | [`credentials`](#protect-credentials), [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](/docs/en/env-vars) |

Claude Code builds the sandbox on the open source [`@anthropic-ai/sandbox-runtime`](https://github.com/anthropics/sandbox-runtime) package.

### What runs outside the sandbox

The sandbox wraps shell commands. These tools and processes run outside it:

* **Built-in file and web tools**: tools such as Read, Edit, Write, WebFetch, and WebSearch follow [permission rules](/docs/en/permissions) instead. A `denyRead` entry doesn't stop the Read tool, and `allowedDomains` doesn't limit WebFetch
* **Other processes Claude Code starts**: command [hooks](/docs/en/hooks), local [MCP servers](/docs/en/mcp), [plugin monitors](/docs/en/plugins/components#monitors), [LSP servers](/docs/en/tools-reference#lsp-tool-behavior), and helper commands such as your [status line](/docs/en/statusline) command and `apiKeyHelper` run with your full access

Some shell commands also run outside the sandbox, depending on your settings:

* **Commands you type yourself**: a command you enter at the [`!` shell-mode prompt](/docs/en/interactive-mode#shell-mode-with-prefix) runs unsandboxed in most sessions. [Strict sandbox mode](#turn-off-the-retry-with-strict-sandbox-mode) lists the sessions where a command you type runs sandboxed
* **Excluded commands**: commands that match [`excludedCommands`](#run-commands-outside-the-sandbox-with-excludedcommands) run unsandboxed
* **Unsandboxed retries**: Claude can [ask to run a command unsandboxed](#the-unsandboxed-retry-escape-hatch), usually after it fails in the sandbox

To put the tools, processes, and commands in this section behind one boundary, run the Claude Code process itself in a [container, virtual machine, or the sandbox runtime](/docs/en/sandbox-environments).

## Get started

The sandbox is built into Claude Code. What you install depends on your platform:

* **macOS**: sandboxing uses the built-in Seatbelt framework, so you can go straight to the steps
* **Linux and WSL2**: the sandbox relies on `bubblewrap` and `socat`, covered in [Set up Linux and WSL2](#set-up-linux-and-wsl2). Even if you haven't installed them yet, you can start with `/sandbox`, because its panel shows whether anything is missing

<Steps>
  <Step title="Run /sandbox">
    Start a Claude Code session and run the `/sandbox` command:

    ```text theme={null}
    /sandbox
    ```

    This opens the sandbox panel with three tabs, plus a Dependencies tab on Linux when the optional seccomp filter is missing:

    * **Mode**: choose how sandboxed commands are approved, covered in the next step
    * **Overrides**: choose whether commands that fail under the sandbox can fall back to running unsandboxed. This is the [`allowUnsandboxedCommands`](/docs/en/settings-reference#sandbox-allowunsandboxedcommands) setting
    * **Config**: view the resolved sandbox settings

    If the panel shows only a Dependencies tab, a required package is missing. Install it as described in [Set up Linux and WSL2](#set-up-linux-and-wsl2), restart Claude Code, and run `/sandbox` again.
  </Step>

  <Step title="Choose a mode">
    On the Mode tab, select auto-allow or regular permissions. Auto-allow runs sandboxed commands without prompting, and regular permissions keeps the regular permission prompts even when commands are sandboxed. See [Sandbox modes](#sandbox-modes) for which commands still prompt in auto-allow mode.
  </Step>

  <Step title="Run a Bash command">
    Ask Claude to run a command, such as a build or a test suite. By default, commands inside the sandbox can write to the working directory, a [per-user temp directory](/docs/en/env-vars), and any [directories you've added](/docs/en/permissions#additional-directories-grant-file-access-not-configuration) with `--add-dir`, `/add-dir`, or `permissions.additionalDirectories`.

    The first time a command needs a new network domain, Claude Code prompts for approval; in [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode), Claude instead names the hosts a command needs [on the command itself](#per-command-allowed-domains-in-auto-mode) for the classifier to review with it.

    To widen or narrow what the sandbox allows, see [Configure sandboxing](#configure-sandboxing).

    If sandboxed commands fail with `Operation not permitted` inside a container, see [Bubblewrap fails to start inside a container](#bubblewrap-fails-to-start-inside-a-container).
  </Step>
</Steps>

When you select a mode in the panel, Claude Code saves it to your project's local settings at `.claude/settings.local.json`, which apply to the current project. Claude Code adds that file to your global gitignore when it saves a setting there. To enable the sandbox across all of your projects, set [`sandbox.enabled`](/docs/en/settings-reference#sandbox-enabled) to `true` in your user settings at `~/.claude/settings.json`. To enforce sandboxing for every developer in an organization, use [managed settings](#enforce-sandboxing-with-managed-settings).

To change the sandbox for one session without writing to a settings file, start Claude Code with [`--settings`](/docs/en/settings#change-a-setting-for-one-session). For example, this command starts a sandboxed session in which Claude can't retry a blocked command outside the sandbox:

```bash theme={null}
claude --settings '{"sandbox": {"enabled": true, "allowUnsandboxedCommands": false}}'
```

<Warning>
  By default, if the sandbox can't start because a dependency is missing or the platform is unsupported, Claude Code runs commands without sandboxing. To make Claude Code exit at startup instead, set [`sandbox.failIfUnavailable`](/docs/en/settings-reference#sandbox-failifunavailable) to `true`. Managed deployments that require sandboxing as a security gate can use this setting.
</Warning>

### Confirm commands run inside the sandbox

To check that the sandbox is working, ask Claude to run each line in the table. What you type at the [`!` prompt](#what-runs-outside-the-sandbox) usually runs outside the sandbox, so typing a line yourself doesn't test it.

| Command | Result inside the sandbox |
| :- | :- |
| `touch ~/sandbox-probe` | Fails with `Operation not permitted` on macOS, or `Read-only file system` on Linux and WSL2 |
| `curl --noproxy '*' https://example.com` | Fails with `Could not resolve host`, because the command has no route around the sandbox proxy |

If Claude asks to retry a failed command outside the sandbox, decline the retry. If `touch` succeeds and your home directory isn't one of the directories the sandbox lets commands write to, delete `~/sandbox-probe`. Then run `/sandbox` to check that the sandbox is on and its dependencies are installed.

### Set up Linux and WSL2

On Linux and WSL2, the sandbox relies on these packages:

* [`bubblewrap`](https://github.com/containers/bubblewrap): the unprivileged sandboxing tool that enforces filesystem isolation
* [`socat`](http://www.dest-unreach.org/socat/): the relay used to route network traffic through the sandbox proxy

Install them with your distribution's package manager:

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

When a dependency is missing, the Dependencies tab in `/sandbox` lists which of `ripgrep`, `bubblewrap`, `socat`, and the seccomp filter your platform lacks. If you don't see the tab after installing and restarting Claude Code, all dependencies are present.

Ripgrep is bundled with the native Claude Code binary. The seccomp filter is optional and adds Unix domain socket blocking. Install it with `npm install -g @anthropic-ai/sandbox-runtime` if it is missing.

When a required dependency is missing, the Dependencies tab is the only tab shown until you install it. When only the optional seccomp filter is missing, the Dependencies tab appears alongside the other tabs. The dependency check runs at startup, so restart Claude Code after installing packages for `/sandbox` to detect them.

<AccordionGroup>
  <Accordion title="Ubuntu 24.04 and later: allow bubblewrap to create user namespaces">
    On Ubuntu 24.04 and later, the default AppArmor policy prevents bubblewrap from creating the user namespaces it needs for isolation.

    To check whether your environment enforces this restriction, including inside WSL2, run `sysctl kernel.apparmor_restrict_unprivileged_userns`. If the command returns `0`, skip this step. If it prints a `No such file or directory` error, the key doesn't exist and you can skip this step. If it returns `1`, add an AppArmor profile that grants `bwrap` this capability:

    ```bash theme={null}
    sudo tee /etc/apparmor.d/bwrap > /dev/null <<'EOF'
    abi <abi/4.0>,
    include <tunables/global>

    profile bwrap /usr/bin/bwrap flags=(unconfined) {
      userns,
      include if exists <local/bwrap>
    }
    EOF
    ```

    The profile applies only to `bwrap` itself, not to the commands it runs inside the sandbox. Reload AppArmor to apply it:

    ```bash theme={null}
    sudo systemctl reload apparmor
    ```
  </Accordion>

  <Accordion title="WSL2 notes">
    Check your WSL version with `wsl -l -v` from PowerShell. If you see `Sandboxing requires WSL2`, your distribution is running WSL1. Upgrade it to WSL2 or run Claude Code without sandboxing.

    On WSL2, WSL hands a launch of a Windows binary such as `cmd.exe`, `powershell.exe`, or anything under `/mnt/c/` to the Windows host over a Unix socket, so whether a sandboxed command can launch one follows the sandbox's [Unix-socket settings](/docs/en/settings-reference#sandbox-network-allowunixsockets): the optional seccomp filter has to be installed to block the socket in the first place. To allow these launches, set `allowAllUnixSockets`, which opens every Unix socket to sandboxed commands.
  </Accordion>
</AccordionGroup>

### Sandbox modes

Claude Code offers two sandbox modes. In both, the sandbox enforces the same filesystem and network restrictions; the difference is only in whether sandboxed commands are auto-approved or require explicit permission.

#### Auto-allow mode

Claude Code approves a command automatically, with no prompt, when the command runs inside the sandbox. A command goes through the regular [permission flow](/docs/en/permissions) when it runs outside the sandbox because it matches [`excludedCommands`](#run-commands-outside-the-sandbox-with-excludedcommands) or because Claude [retries it unsandboxed](#the-unsandboxed-retry-escape-hatch).

A sandboxed command that connects to a host you haven't allowed stays in the sandbox. [Hosts outside your allowed domains](#hosts-outside-your-allowed-domains) covers who decides whether the connection goes through.

Even in auto-allow mode, the following still apply:

* Explicit [deny rules](/docs/en/permissions) are always respected
* `rm` or `rmdir` commands that target a [critical path](/docs/en/permission-modes#critical-paths) still go through the regular permission flow
* Content-scoped [ask rules](/docs/en/permissions) like `Bash(git push *)` still force a prompt even for sandboxed commands
* A bare `Bash` ask rule, or the equivalent `Bash(*)` form, is skipped for commands that run sandboxed; it still applies to commands that fall back to the regular permission flow. In [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode), the rule isn't skipped: it prompts for sandboxed commands too, including read-only ones

<Info>
  Auto-allow mode works independently of your permission mode setting, with three exceptions: [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode), an auto mode command that carries [per-command allowed domains](#per-command-allowed-domains-in-auto-mode), and [server-side classifier review](/docs/en/permission-modes#how-the-classifier-evaluates-actions) of sandboxed commands in auto mode. Even if you're not in "accept edits" mode, sandboxed Bash commands run automatically when auto-allow is enabled. This means Bash commands that modify files within the sandbox boundaries execute without prompting, even in Manual mode, where the file edit tools would prompt.

  In plan mode, auto-allow doesn't widen approvals; see [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) for how Claude Code gates commands while you plan.
</Info>

#### Regular permissions mode

All Bash commands go through the regular permission flow, even when sandboxed. This provides more control but requires more approvals.

#### The unsandboxed retry escape hatch

The unsandboxed retry is an escape hatch for commands that fail inside the sandbox, such as tools that are incompatible with it. When the sandbox blocks a network connection, Claude Code names the denied host in the command's result, so Claude sees what was blocked. Claude analyzes the failure and may retry the command with the `dangerouslyDisableSandbox` parameter.

The retried command runs unsandboxed. In an interactive terminal session, who approves it depends on your permission mode:

* **`bypassPermissions` mode**: the retry runs without a prompt
* **Manual mode and `acceptEdits` mode**: you get a prompt titled "Bash command (unsandboxed)"
* **[Auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode)**: a separate classifier model evaluates the underlying command
* **`dontAsk` mode**: Claude Code denies the retry
* **Plan mode**: see [how Claude Code gates commands while you plan](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode)

These rules and settings change who approves the retry:

* **A matching allow rule**: if an allow rule such as `Bash(curl *)` matches the command, it also approves the retry, so the command runs outside the sandbox with no prompt
* **An ask rule for the parameter**: add an [ask rule](/docs/en/permissions#match-by-input-parameter) for `Bash(dangerouslyDisableSandbox:true)` to be prompted on Bash retries. You get the prompt in auto mode and `bypassPermissions` mode too, and the rule takes precedence over a matching allow rule
* **[`permissions.blockReadsOutsideWorkingDirectories`](/docs/en/settings-reference#permissions-blockreadsoutsideworkingdirectories)**: [Actions no mode auto-approves](/docs/en/permission-modes#actions-no-mode-auto-approves) covers the retries that prompt while it's on

#### Turn off the retry with strict sandbox mode

You can disable the unsandboxed retry by setting `"allowUnsandboxedCommands": false` in your [sandbox settings](/docs/en/settings-reference#sandbox-settings). With the retry disabled, Claude Code ignores the `dangerouslyDisableSandbox` parameter. While the sandbox is running, commands Claude runs are then sandboxed unless they match an `excludedCommands` entry. To keep Claude Code from running commands unsandboxed when the sandbox can't start, also set [`failIfUnavailable`](/docs/en/settings-reference#sandbox-failifunavailable). The `/sandbox` **Overrides** tab shows this setting as **Strict sandbox mode**.

A `false` in your user settings, `--settings`, or managed settings holds even when a project's settings set `true`. A `false` in your user settings doesn't make the sandbox admin-required, so a project's other sandbox settings still apply. Before v2.1.285, a project's `true` overrode a `false` in your user settings.

If you or your administrator disable the retry in managed settings or with the `--settings` flag, the sandbox becomes admin-required. Claude Code then ignores the settings in a repository's files that loosen the sandbox, `excludedCommands` entries included. [Repository settings under an admin-required sandbox](#repository-settings-under-an-admin-required-sandbox) lists them.

Strict sandbox mode applies to the commands Claude runs. Commands you type yourself at the [`!` shell-mode prompt](/docs/en/interactive-mode#shell-mode-with-prefix) run outside the sandbox unless the session is one of these:

* **A [background session](/docs/en/agent-view)**: strict sandbox mode covers shell-mode commands too
* **A Linux session with [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](/docs/en/env-vars#variables) set**: every command runs sandboxed, shell-mode commands included

Before v2.1.260, strict sandbox mode sandboxed shell-mode commands in every session.

#### Temporary directories

A per-user temp directory is writable inside the sandbox by default, alongside the working directory. Unless you [disable filesystem isolation](#disable-filesystem-isolation), Claude Code sets `$TMPDIR` to this directory for sandboxed commands, so tools that write temporary files work without extra configuration.

Unsandboxed commands inherit your shell's `$TMPDIR` when it is set, so while filesystem isolation is on, sandboxed and unsandboxed commands resolve `$TMPDIR` to different directories. If your shell leaves `$TMPDIR` unset or empty, an unsandboxed command that references `$TMPDIR` receives your [`CLAUDE_CODE_TMPDIR`](/docs/en/env-vars) override, or the operating system's temp directory when you haven't set one or the override is a long path, so the variable doesn't expand to an empty string. To pass temporary files between the two, write them under the working directory instead.

## Configure sandboxing

Customize sandbox behavior through your `settings.json` file. See [Settings](/docs/en/settings-reference#sandbox-settings) for the complete configuration reference.

By default, sandboxed commands can write to the current working directory, the per-user temp directory, and any [directories you've added](/docs/en/permissions#additional-directories-grant-file-access-not-configuration) with `--add-dir`, `/add-dir`, or `permissions.additionalDirectories`. If subprocess commands like `kubectl`, `terraform`, or `npm` need to write outside those directories, use `sandbox.filesystem.allowWrite` to grant access to specific paths:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowWrite": ["~/.kube", "/tmp/build"]
    }
  }
}
```

These paths are enforced at the OS level, so all commands running inside the sandbox, including their child processes, respect them. This is the recommended approach when a tool needs write access to a specific location, rather than excluding the tool from the sandbox entirely with `excludedCommands`.

When you define the same filesystem array in multiple [settings scopes](/docs/en/settings#settings-precedence), Claude Code merges them, combining the paths rather than replacing one scope's array with another's. Claude Code leaves an entry out of the merge when a lock under [Keep developers from widening the policy](#keep-developers-from-widening-the-policy) covers it.

If you exclude a source with [`--setting-sources`](/docs/en/cli-reference) on the CLI or [`settingSources`](/docs/en/agent-sdk/claude-code-features#control-filesystem-settings-with-settingsources) in the Agent SDK, Claude Code ignores its `sandbox.filesystem` entries, its `Edit` permission rules, and its `Read` deny rules when building the sandbox configuration. Requires Claude Code v2.1.246 or later.

When you edit these filesystem lists during a session, Claude Code [applies the change to the running session](/docs/en/settings#when-edits-take-effect), so the next sandboxed command runs under the new paths.

Sandbox filesystem paths use standard conventions: `/tmp/build` is absolute and `~/.kube` is relative to your home directory. This differs from [Read and Edit permission rules](/docs/en/permissions#read-and-edit), which use `//path` for absolute and `/path` for project-relative. For relative paths, trailing slashes, and wildcards, see [Sandbox path prefixes](/docs/en/settings-reference#sandbox-path-prefixes).

You can also deny write or read access using `sandbox.filesystem.denyWrite` and `sandbox.filesystem.denyRead`, and re-allow specific paths within a denied region using `sandbox.filesystem.allowRead`. When read rules overlap, the rule with the narrower path applies:

| Example rules | Result |
| :- | :- |
| `"denyRead": ["~/"]` with `"allowRead": ["~/projects"]` | `~/projects` is readable and the rest of the home directory stays blocked. The narrower allow re-opens that part of the denied region |
| `"allowRead": ["~/"]` with `"denyRead": ["~/.env"]` | `~/.env` stays blocked and the rest of the home directory is readable. The deny holds inside a wider allow, so a broad allow can't silently re-expose a secret |
| `"allowRead": ["~/"]` with `"denyRead": ["~/**/.env"]` | Every `.env` under the home directory stays blocked and the rest is readable. A [wildcard deny](/docs/en/settings-reference#sandbox-path-prefixes) holds inside a wider allow the same way an exact path does |

The example below blocks reading from the entire home directory while still allowing reads from the current project. Place it in your project's `.claude/settings.json`, because the relative path `.` resolves to the project root when the configuration lives in project settings:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    }
  }
}
```

If you placed the same configuration in `~/.claude/settings.json`, `.` would resolve to `~/.claude` instead, and project files would remain blocked by the `denyRead` rule.

To deny sandboxed commands read access to home directories and mounted volumes while keeping the working directories readable, set [`permissions.blockReadsOutsideWorkingDirectories`](/docs/en/settings-reference#permissions-blockreadsoutsideworkingdirectories) instead of writing path rules.

### Run commands outside the sandbox with `excludedCommands`

List a command pattern in [`sandbox.excludedCommands`](/docs/en/settings-reference#sandbox-excludedcommands) to run matching commands outside the sandbox, which means no filesystem restrictions and no network proxy. Use it for a tool that can't work inside the sandbox and that you trust with your full access. A tool that needs one more directory or one more host may work with `allowWrite` or `allowedDomains`, which keep the command sandboxed.

This example takes `docker compose` commands out of the sandbox. Save it in `~/.claude/settings.json` to apply it to all of your projects:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "excludedCommands": ["docker compose *"]
  }
}
```

Claude Code checks your entries against each Bash and Monitor call. A call is the whole command line Claude sends, which can chain several commands. The following rules decide whether a call leaves the sandbox:

* **End the pattern with ` *`**: entries use the same syntax as a `Bash(...)` [permission rule](/docs/en/permissions#permission-rule-syntax), where a pattern with no wildcard is an exact match. `docker` matches only `docker` with no arguments. `docker *` matches `docker` with or without arguments
* **Every command in the call has to match**: `npm ci && docker compose build` stays sandboxed unless another entry covers `npm ci`
* **Claude Code matches the text of the call**: a script or `make` target that calls `docker` internally doesn't match, and neither does `/usr/local/bin/docker`
* **Some calls stay sandboxed**: a redirect to a file, a `cd`, or a command substitution such as `$(...)` keeps the whole call sandboxed. The [reference entry](/docs/en/settings-reference#sandbox-excludedcommands) lists more calls that stay sandboxed
* **Where you save the entry can matter**: while the sandbox is [admin-required](#repository-settings-under-an-admin-required-sandbox), Claude Code ignores entries in `.claude/settings.json` and `.claude/settings.local.json`

An excluded command goes through the regular permission flow:

* [Read-only commands](/docs/en/permissions#read-only-commands) and commands your allow rules cover run without a prompt
* In auto mode, the classifier reviews other excluded commands
* In `bypassPermissions` mode, an excluded command runs without a prompt unless an ask rule matches it

To confirm an entry matches, switch to Manual mode and ask Claude to run a matching command that changes something, such as `docker compose up -d`. The permission prompt is titled "Bash command (unsandboxed)".

<Warning>
  An excluded command runs with your full access. A broad entry such as `docker *` covers everything that tool can do. If you write a pattern that covers an interpreter, a script inside your working directory, or a tool that acts on a file there, as `docker compose` does with its compose file, Claude can write that file and then run it outside the sandbox. A narrower pattern leaves less that Claude can run outside the sandbox.
</Warning>

### Disable filesystem isolation

Set `sandbox.filesystem.disabled` to `true` to skip filesystem isolation while keeping network isolation. The example below turns off filesystem isolation while keeping an allowlist of network domains:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "disabled": true
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  }
}
```

The sandbox has two independent layers: [filesystem isolation](#filesystem-isolation) controls which paths sandboxed commands can read and write, and [network isolation](#network-isolation) controls which domains they can reach. With the filesystem layer off, sandboxed commands get unrestricted read and write access to the host filesystem, while their network egress stays confined to your allowed domains. Turn the layer off when you sandbox to control where commands connect rather than what they write.

`sandbox.filesystem.disabled` defaults to `false`. Requires Claude Code v2.1.216 or later.

<Warning>
  With filesystem isolation off and commands auto-allowed, a sandboxed command can write files that later commands run or read, such as shell startup files, executables on `$PATH`, or `~/.claude/settings.json`, and use them to widen its own access on the next run. Set `filesystem.disabled` to `true` only for workloads you trust not to escalate their own access. Locking network domains with [`allowManagedDomainsOnly`](#keep-developers-from-widening-the-policy) narrows the risk but doesn't remove it, since that lock applies only to commands running inside the sandbox.
</Warning>

#### Which settings can disable it

Because turning filesystem isolation off widens what sandboxed commands can do, Claude Code honors `filesystem.disabled` from these settings sources only:

* User settings, managed settings, and the `--settings` CLI flag can set it. Project settings in `.claude/settings.json` and `.claude/settings.local.json` can't, so a checked-out project can't switch filesystem isolation off.
* When managed settings configure `sandbox.filesystem` at all, or list any `sandbox.credentials.files` entry with `"mode": "deny"`, only managed settings can set the key. This keeps administrator-deployed filesystem restrictions in force; to relax such a deployment, set `"disabled": true` in managed settings.
* When [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](/docs/en/env-vars) is set, Claude Code ignores `filesystem.disabled` from every source, including managed settings, and keeps filesystem isolation on.

A [valid](/docs/en/settings-reference#invalid-credential-entries-in-managed-settings) `mask` entry doesn't lock the key, even when Claude Code [falls back to `deny`](#mask-credential-files) for it at startup. List a path that can't be masked, such as a credential directory, as an explicit `deny` entry in managed settings, which locks the key.

#### What changes when filesystem isolation is off

Setting `filesystem.disabled` lifts the protections the filesystem layer itself enforces. Protections that other layers enforce keep applying:

| Protection | With filesystem isolation off |
| - | - |
| `filesystem.denyRead` and [`credentials.files`](#protect-credentials) `deny` read blocks | Not enforced. The filesystem layer applies both |
| `credentials.envVars` `deny` and `mask` entries | Enforced. Environment variable scrubbing is independent of the filesystem layer |
| [`credentials.files` `mask` entries](#mask-credential-files) applied as masks | Enforced: masking is independent of the filesystem layer. An entry that [fell back to `deny`](#mask-credential-files) is not enforced, like any `deny` entry |

Two other things change:

* Sandboxed commands inherit your shell's `$TMPDIR` instead of the per-user temp directory, because every temp directory is writable and Claude Code no longer redirects commands to the per-user one.

  On Linux the variable is often unset in the parent shell. The Bash tool guidance tells Claude to create scratch directories with `mktemp -d` instead of relying on `$TMPDIR`.
* [`autoAllowBashIfSandboxed`](/docs/en/settings-reference#sandbox-autoallowbashifsandboxed) still defaults to `true`, so sandboxed commands keep running without prompts. Set it to `false` to prompt for sandboxed commands.

### Protect credentials

The `sandbox.credentials` setting declares credential files and environment variables to protect from sandboxed commands. Each entry names a file path or an environment variable and a `mode`. The dedicated `credentials` block keeps credential rules grouped together and separate from general filesystem rules.

For entries with `"mode": "deny"`, file paths are denied for reads inside the sandbox, the same restriction that `filesystem.denyRead` applies, and environment variables are unset before each sandboxed command runs. The file protection is part of the filesystem layer, so it doesn't apply if you [disable filesystem isolation](#disable-filesystem-isolation); the environment variable protection still does.

The example below blocks reads of the AWS credentials file and the SSH directory and removes `GITHUB_TOKEN` and `NPM_TOKEN` from the environment of sandboxed commands:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "credentials": {
      "files": [
        { "path": "~/.aws/credentials", "mode": "deny" },
        { "path": "~/.ssh", "mode": "deny" }
      ],
      "envVars": [
        { "name": "GITHUB_TOKEN", "mode": "deny" },
        { "name": "NPM_TOKEN", "mode": "deny" }
      ]
    }
  }
}
```

Environment variable entries and file entries also accept `"mode": "mask"`, described under [Mask credentials](#mask-credentials).

File paths follow the same [prefix rules](/docs/en/settings-reference#sandbox-path-prefixes) as `sandbox.filesystem.*` settings.

Claude Code merges the `deny` entries from every [settings scope](/docs/en/settings#settings-precedence) the session loads. A `deny` entry only ever narrows access, so any scope can add one, but no scope can remove one that another scope added.

When you [exclude a settings source](#configure-sandboxing):

* **Project or local settings**: Claude Code applies none of their `credentials` entries. Requires Claude Code v2.1.246 or later.
* **User settings**: Claude Code still applies the `deny` entries in `~/.claude/settings.json` and keeps its [file `mask` entries](#mask-credential-files) as restrictions that no longer authorize the proxy to substitute the real value, but drops its [environment variable `mask` entries](#mask-environment-variables).

There is no built-in credential deny list, so only the files and variables you list are restricted.

`sandbox.credentials` affects sandboxed Bash commands only. To strip credentials from all subprocesses regardless of sandboxing, set [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](/docs/en/env-vars).

### Mask credentials

When you mask a credential, Claude Code shows sandboxed commands a per-session placeholder called the sentinel, and the [sandbox proxy](#network-isolation) substitutes the real value on outbound requests to hosts you allow. A `deny` entry under [Protect credentials](#protect-credentials) blocks the credential instead. For files on macOS, Claude Code [blocks the file instead](#mask-credential-files) of masking it. The [`sandbox.credentials`](/docs/en/settings-reference#sandbox-credentials) reference lists every field.

Masking requires the following:

* **TLS termination**: the proxy substitutes the real value inside request contents, so it has to see them. Set [`network.tlsTerminate`](/docs/en/settings-reference#sandbox-network-tlsterminate) so the proxy terminates TLS itself. Without it, masking fails without exposing anything: the command still sees only the sentinel, but the sentinel reaches the server unchanged and authentication fails. To check for this misconfiguration, run `claude doctor` in your terminal and look for the `TLS termination is unavailable` warning.
* **An allowed destination**: each `mask` entry can list `injectHosts`, the hosts the real value is allowed to reach. The proxy injects only on connections the [domain allowlist](#network-isolation) admits, so each `injectHosts` host must also be reachable through `network.allowedDomains`. For a `mask` entry with no `injectHosts`, the proxy substitutes the real value on requests to every host in `network.allowedDomains`.
* **A trusted settings scope**: masking authorizes the proxy to send your real credential somewhere, so Claude Code honors `mask` entries, `network.tlsTerminate`, [`credentials.allowPlaintextInject`](/docs/en/settings-reference#sandbox-credentials-allowplaintextinject), `awsPairs`, and `sigv4` only from user settings, managed settings, and the `--settings` flag. It ignores them in a repository's `.claude/settings.json` or `.claude/settings.local.json`. When your administrator delivers `mask` entries, `network.tlsTerminate`, or `credentials.allowPlaintextInject` through server-managed settings, they count as [settings that need approval](/docs/en/server-managed-settings#security-approval-dialogs).

#### Mask environment variables

To mask an environment variable, set `"mode": "mask"` on its `credentials.envVars` entry. The command and anything it logs never hold the real credential, but its requests still authenticate. When the same variable is listed with `deny` in any scope, `deny` takes precedence.

This example masks two tokens. `GH_TOKEN` is substituted only on requests to `api.github.com`, while `NPM_TOKEN` has no `injectHosts` and is substituted on requests to every host in `network.allowedDomains`:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "network": {
      "tlsTerminate": {},
      "allowedDomains": ["*.github.com", "registry.npmjs.org"]
    },
    "credentials": {
      "envVars": [
        { "name": "GH_TOKEN", "mode": "mask", "injectHosts": ["api.github.com"] },
        { "name": "NPM_TOKEN", "mode": "mask" }
      ]
    }
  }
}
```

Masking replaces the whole value by default. For a value with structure, such as a `DATABASE_URL` connection string or a JWT, use the [`extract`, `decode`, `maskClaims`, and `onExtractNoMatch` fields](/docs/en/settings-reference#sandbox-credentials-envvars) so tools that parse the value keep working.

<span id="ipv6-destinations-in-injecthosts" />For an IPv6 destination, spell the address differently in the two lists:

* **`network.allowedDomains`**: the bracketed form, such as `"[::1]"`
* **`injectHosts`**: the bare address in its canonical compressed form, such as `"::1"`

The proxy matches each `injectHosts` entry against the connection's bare destination address, ignoring ports, so a bracketed, zone-ID, or differently compressed spelling never matches. `claude doctor` flags entries that can never match with the warning `Sandbox credential injectHosts entries can never match their destination`. This check requires Claude Code v2.1.229 or later.

#### Re-sign AWS requests

AWS requests carry SigV4 signatures over the request contents, so mask `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` together. The proxy detects a SigV4 request by the access key's [sentinel](#mask-credentials) and re-signs the request with the real values, which requires Claude Code v2.1.221 or later. If you mask only the secret, requests are signed with a placeholder the proxy can't detect, so they fail at AWS.

Claude Code links the conventional `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` variables into one credential automatically when you mask their whole values. If your AWS credential is in variables with other names, group them with [`credentials.awsPairs`](/docs/en/settings-reference#sandbox-credentials-awspairs), which requires Claude Code v2.1.224 or later.

Streaming uploads, presigned URLs, and SigV4A requests carry signatures the proxy can't recompute. When one of these requests is signed with a masked pair's placeholder, the proxy fails it rather than forward a broken signature. Requests signed with unmasked credentials aren't affected. Use [`credentials.sigv4`](/docs/en/settings-reference#sandbox-credentials-sigv4), which requires Claude Code v2.1.224 or later, to forward one of these request forms instead. AWS still rejects the request, so the calling tool receives AWS's own rejection response instead of a proxy error.

#### Mask credential files

To mask a credential file, set `"mode": "mask"` on its `credentials.files` entry. Masking files requires Claude Code v2.1.221 or later. What a sandboxed command sees depends on the platform:

* **Linux and WSL2**: sandboxed commands read a [sentinel](#mask-credentials) copy of the file, and the proxy substitutes the real value on outbound requests.
* **macOS**: sandboxed commands can't read the file at all. Claude Code builds no sentinel copy, so tools that authenticate with the file don't work inside the sandbox, the same effect as `deny`. The read block holds even when you [disable filesystem isolation](#disable-filesystem-isolation).

This example masks a GitHub token stored in `~/.config/gh/hosts.yml`. The `extract` pattern marks which part of the file is the secret, so on Linux and WSL2 `gh` still parses the rest of its config:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "network": {
      "tlsTerminate": {},
      "allowedDomains": ["*.github.com"]
    },
    "credentials": {
      "files": [
        {
          "path": "~/.config/gh/hosts.yml",
          "mode": "mask",
          "extract": "oauth_token:\\s*(\\S+)",
          "injectHosts": ["api.github.com"]
        }
      ]
    }
  }
}
```

To confirm the mask is active, ask Claude to run `cat ~/.config/gh/hosts.yml` in a sandboxed command. On Linux and WSL2 the output shows a sentinel in place of the token, and on macOS the read fails.

Without `extract` or `decode`, Claude Code replaces the entire file with one sentinel, which suits a file holding a single bare secret. Use the [`extract`, `decode`, `maskClaims`, `onExtractNoMatch`, and `maskDuplicates` fields](/docs/en/settings-reference#sandbox-credentials-files) to control partial masking and what happens when the pattern matches nothing.

<Warning>
  When matching finds nothing to mask, the default `onExtractNoMatch` value, `warn`, skips the entry, so sandboxed commands can read the real file unmasked. On macOS, Claude Code applies `mask` entries as `deny` before the pattern runs whenever filesystem isolation is on, so the no-match outcomes take effect there only when [filesystem isolation is off](#disable-filesystem-isolation). The default suits credentials that may be legitimately absent. If the secret might be present but the pattern might miss it, use [`deny`](/docs/en/settings-reference#mask-fields-for-files).
</Warning>

`mask` applies to a single file, so list each credential file individually. Claude Code falls back to `deny` for a `mask` entry it can't mask safely: a directory path, a glob pattern, a file larger than 8 MiB, or a file that isn't UTF-8 text.

## How sandboxing works

### Filesystem isolation

The sandboxed Bash tool restricts file system access to specific directories:

* **Default write behavior**: read and write access to the current working directory and its subdirectories, any directories you've added with `--add-dir`, `/add-dir`, or [`permissions.additionalDirectories`](/docs/en/settings-reference#permissions-additionaldirectories), plus the per-user temp directory that `$TMPDIR` points to
* **Default read behavior**: read access to the entire computer, except certain denied directories. This default still allows reading credential files, so [protect credentials](#protect-credentials) you don't want commands to read.
* **Read block**: with [`permissions.blockReadsOutsideWorkingDirectories`](/docs/en/settings-reference#permissions-blockreadsoutsideworkingdirectories) on, sandboxed commands also lose read access to your home directory and the other directories that hold user files, apart from the paths that [Sandboxed commands under the block](/docs/en/settings-reference#sandboxed-commands-under-the-block) lists. That section also says when this part of the block doesn't apply.
* **Git worktrees**: when the working directory is a [linked git worktree](/docs/en/worktrees), the sandbox also allows writes to the main repository's shared `.git` directory so commands such as `git commit` can update refs and the index. Writes to `hooks/` and `config` inside that directory remain denied.

To skip filesystem isolation entirely while keeping network isolation, set [`sandbox.filesystem.disabled`](#disable-filesystem-isolation).

### Protected paths

Inside the directories that sandboxed commands can write to, the sandbox still denies writes to the files Claude Code loads configuration and code from. A command that could edit those files could grant itself permissions, or add a hook or MCP server that Claude Code runs outside the sandbox. The permission system has its own [protected paths](/docs/en/permission-modes#protected-paths), which control what Claude Code approves before a tool runs; the sandbox's list applies to a command that is already running. It covers four groups of paths:

* **In your working directory and the directories above it**: the `.claude` settings files, the `.claude/skills`, `.claude/agents`, `.claude/commands`, and `.claude/hooks` directories, `.mcp.json`, and the files Claude Code runs on its own, such as `.claude/workflows` and `.claude/scheduled_tasks.json`
* **In your working directory only**: shell startup files such as `.bashrc` and `.zshrc`, `.gitconfig`, the `.vscode` and `.idea` directories, and `hooks` and `config` inside `.git`
* **Files that would turn your working directory into a bare git repository**: `HEAD`, `objects`, and `refs` at the top level, plus existing `config` and `hooks` entries there when a `HEAD` sits beside them. A file named `config` is denied even with no `HEAD`. On Linux and WSL2, the sandbox deletes a top-level `HEAD` file or `objects` or `refs` directory that appears while a sandboxed command is running
* **In `~/.claude`, or the directory `CLAUDE_CONFIG_DIR` points to**: most of its contents, plus `~/.claude.json` and the `.credentials.json` credential store

If a symlink appears at a protected settings file's path during the session, the sandbox also denies writes to the file it points to, starting with the next command.

There is no way to exempt one of these paths: an `allowWrite` entry or an `Edit` allow rule that covers the path doesn't lift the protection. The only way to turn the protection off is [`filesystem.disabled`](#disable-filesystem-isolation), which turns off filesystem isolation for every path. To see most of these paths resolved for your machine, run `/sandbox` and open the **Config** tab, which lists them under **Denied within allowed**, mixed in with your own `denyWrite` entries.

If `git merge` or `git checkout` fails with `unable to unlink old` on one of these paths, see [A git command fails with `unable to unlink old`](#a-git-command-fails-with-unable-to-unlink-old).

### Network isolation

A sandboxed command has no direct route to the network:

* **Linux and WSL2**: the command runs in a separate network namespace that has no connection to your network
* **macOS**: the Seatbelt sandbox framework by default blocks connections other than the one to the sandbox proxy

Claude Code runs the sandbox proxy on your machine, outside the sandbox, and directs commands to it with `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, and related environment variables. The proxy checks the hostname of each connection against your allowed and denied domains.

What a tool can reach depends on whether it uses the proxy:

* **Tools that read the proxy variables**: `curl`, `npm`, `git` over HTTPS, and similar tools connect once their host is allowed. An `allowedDomains` entry with no port allows every port on that host
* **Tools that ignore the proxy variables**: plain `ssh`, most database drivers, and similar tools can't connect, even to an allowed host. See [A database client or other non-HTTP tool fails to reach an allowed host](#a-database-client-or-other-non-http-tool-fails-to-reach-an-allowed-host)
* **Anything that isn't TCP**: UDP, HTTP/3 over QUIC, and ICMP tools such as `ping` can't leave the sandbox

The following settings and behaviors control which hosts the proxy allows:

* **Domain restrictions**: your allowed domains start empty. [Hosts outside your allowed domains](#hosts-outside-your-allowed-domains) covers what happens the first time a command needs a new domain.
* **Approval choices**: if you choose Yes when prompted, Claude Code allows the host for the rest of the current session. If you choose "Yes, and don't ask again", Claude Code saves a `WebFetch(domain:...)` allow rule to your [local settings](/docs/en/permissions#permission-system), so the host stays allowed in future sessions. While the sandbox is [admin-required](#repository-settings-under-an-admin-required-sandbox), Claude Code saves the rule to your user settings, where it applies in every project.
* **Pre-allowed domains**: pre-allow domains with [`allowedDomains`](/docs/en/settings-reference#sandbox-network-alloweddomains) to avoid the prompt entirely. Claude Code also pre-allows domains from `WebFetch(domain:...)` allow rules, as described in [Permission rules](#permission-rules).
* **Strict allowlist**: if you set [`strictAllowlist`](/docs/en/settings-reference#sandbox-network-strictallowlist) to `true` in user, managed, or CLI `--settings` settings, Claude Code denies sandboxed commands access to any host outside the allowlist instead of prompting. The allowlist is `allowedDomains` plus domains from `WebFetch(domain:...)` allow rules, or only the managed settings entries when `allowManagedDomainsOnly` is set. [Locks that apply without an admin-required sandbox](#locks-that-apply-without-an-admin-required-sandbox) covers a repository's entries. Claude Code enforces this for sandboxed commands only; in-process tools such as `WebFetch` still follow their [permission rules](#permission-rules). Setting it in a repository's `.claude/settings.json` or `.claude/settings.local.json` has no effect. Requires Claude Code v2.1.219 or later.
* **Managed lockdown**: if [`allowManagedDomainsOnly`](/docs/en/settings-reference#sandbox-network-allowmanageddomainsonly) is set in managed settings, non-allowed domains are blocked automatically instead of prompting, and only `allowedDomains` and `WebFetch(domain:...)` allow rules from managed settings are honored.
* **Corporate proxy**: when your network requires outbound traffic to go through a corporate proxy, set `HTTPS_PROXY`, `HTTP_PROXY`, and `NO_PROXY` as [proxy configuration](/docs/en/network-config#proxy-configuration) describes, in the `env` block of your settings so that [background agents](/docs/en/network-config#set-network-variables-in-settings-not-the-shell) get them too, or in the environment you launch Claude Code from. Claude Code enforces the domain allowlist and then tunnels allowed connections through that upstream proxy. `http://` and `https://` proxy URLs work, with basic authentication in the URL if you need it.

In a `WebFetch(domain:...)` rule, the sandbox honors two wildcard forms: a leading `*.`, such as `*.example.com`, and a bare `*`. The bare `*` form requires Claude Code v2.1.186 or later. A wildcard in any other position, such as `WebFetch(domain:example.*)`, still matches fetches but has no effect on sandboxed commands.

<Note>
  The built-in proxy enforces the allowlist based on the requested hostname and, by default, does not terminate or inspect TLS traffic. The experimental [`network.tlsTerminate`](/docs/en/settings-reference#sandbox-network-tlsterminate) setting makes the built-in proxy terminate TLS itself, which [`mask` credential entries](#mask-credentials) require. See [Security limitations](#security-limitations) for the implications of the default, and [Custom proxy configuration](#custom-proxy-configuration) if your threat model requires TLS inspection.
</Note>

#### Hosts outside your allowed domains

When a sandboxed command connects to a host that isn't in your allowed domains, the command stays in the sandbox and waits for a decision. In an interactive terminal session, the decision depends on your permission mode:

| Permission mode | What happens to the connection |
| :- | :- |
| `bypassPermissions` mode, and plan mode with [bypass permissions available](/docs/en/permission-modes#skip-all-checks-with-bypasspermissions-mode) | Allowed without a prompt |
| Manual mode, `acceptEdits` mode, and plan mode otherwise | You get a prompt |
| Auto mode | Refused unless the command [listed the host](#per-command-allowed-domains-in-auto-mode) and the classifier approved the list |
| `dontAsk` mode | Refused |

With [`strictAllowlist`](/docs/en/settings-reference#sandbox-network-strictallowlist) or [`allowManagedDomainsOnly`](/docs/en/settings-reference#sandbox-network-allowmanageddomainsonly) on, the built-in sandbox proxy refuses the connection in every permission mode. In `bypassPermissions` mode, hosts outside your allowed domains are allowed unless one of them is on. [The unsandboxed retry escape hatch](#the-unsandboxed-retry-escape-hatch) covers when a command can leave the sandbox in that mode. A connection to a host in [`deniedDomains`](/docs/en/settings-reference#sandbox-network-denieddomains) is refused in every permission mode too.

#### Hostnames that resolve to local addresses

After a hostname passes the allowlist, the sandbox proxy resolves it and refuses the connection when the name resolves only to local addresses. Local addresses include loopback addresses such as `127.0.0.1`, link-local addresses such as the `169.254.169.254` cloud metadata endpoint, and addresses assigned to your own machine. The names `localhost` and `*.localhost` are allowed to resolve to loopback.

An allowed intranet hostname that resolves to a private range such as `10.0.0.0/8` connects. To let a name resolve to a refused address, add that IP address to `allowedDomains`, such as `"127.0.0.1:8080"`.

The check applies to hostnames. Your allowed domains and permission mode decide a connection to an IP address. The proxy also skips the check for connections it sends through an upstream corporate proxy, because that proxy resolves the name.

#### Per-command allowed domains in auto mode

In [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode) with sandboxing on, Claude names the hosts a command needs on the command itself instead of triggering a network approval for each connection. Each Bash, PowerShell, or [Monitor](/docs/en/tools-reference#monitor-tool) command that runs in the sandbox can carry a list of hosts beyond the sandbox's allowlist: a domain such as `registry.npmjs.org`, a wildcard such as `*.pythonhosted.org`, or an IP address, each with an optional `:port`. The classifier reviews the hosts together with the command. Requires Claude Code v2.1.271 or later.

An approved list opens those hosts for that one command alone, for as long as it runs. Nothing is added to your session's allowed hosts or your settings; the next command names its own hosts.

A command that carries hosts goes to the classifier instead of being approved by a permission rule or the sandbox's [auto-allow mode](#sandbox-modes). If an [ask rule](/docs/en/permissions#manage-permissions) forces a prompt for the command, the permission dialog in your terminal lists the hosts beside it, and approving there covers both.

A per-command list widens only what the sandbox denies by default. [`deniedDomains`](/docs/en/settings-reference#sandbox-network-denieddomains) entries still block. When [`strictAllowlist`](/docs/en/settings-reference#sandbox-network-strictallowlist) or [`allowManagedDomainsOnly`](/docs/en/settings-reference#sandbox-network-allowmanageddomainsonly) locks the allowlist, Claude Code refuses per-command lists.

While per-command lists apply, Claude Code refuses a connection to a host that no approved command listed, without a prompt or a classifier check. The refusal names the host in the command's result, and Claude re-runs the command with the host added.

#### IPv6 addresses in domain lists

To match an IPv6 address in `allowedDomains`, `deniedDomains`, or a `WebFetch(domain:...)` rule, write the address in brackets: `"[::1]"` matches that address on every port, and `"[::1]:443"` matches it on port 443 only. The bracketed form requires Claude Code v2.1.229 or later.

An unbracketed entry such as `::1:443` is ambiguous between an address and an address with a port:

* **Deny lists**: Claude Code denies every reading the entry parses as, so whichever reading you meant is blocked. For an entry with no parseable reading, Claude Code blocks nothing
* **Allow lists**: Claude Code never allows more than you wrote. It rewrites an ambiguous entry to its host-and-port reading when that reading parses cleanly, and may drop the entry entirely rather than widen the allowlist

To find ambiguous entries, run `claude doctor` in your terminal and look for the `Sandbox network domain entries have unreliable spellings` warning. Rewrite each ambiguous entry in the bracketed form.

### OS-level enforcement

The sandboxed Bash tool uses operating system security primitives:

* **macOS**: uses Seatbelt for sandbox enforcement
* **Linux**: uses [bubblewrap](https://github.com/containers/bubblewrap) for isolation
* **WSL2**: uses bubblewrap, same as Linux

You can also run the [`@anthropic-ai/sandbox-runtime`](https://github.com/anthropics/sandbox-runtime) package on its own to wrap the Claude Code process. See [Sandbox runtime](/docs/en/sandbox-environments#sandbox-runtime).

## How sandboxing relates to permissions and permission modes

Sandboxing, [permission rules](/docs/en/permissions), and [permission modes](/docs/en/permission-modes) are complementary layers. The sections below cover how the sandbox interacts with each.

### Permission rules

Permission rules and sandboxing control different things:

* **Permission rules** control which tools Claude Code can use and are evaluated before any tool runs. They apply to every tool: Bash, Read, Edit, WebFetch, MCP, and others, except that a deny or ask rule can't block [`EndConversation`](/docs/en/tools-reference#endconversation-tool-behavior) while any other tool remains.
* **Sandboxing** provides OS-level enforcement that restricts what shell commands can access at the filesystem and network level. It applies only to Bash, PowerShell, and [Monitor](/docs/en/tools-reference#monitor-tool) commands and their child processes.

The two layers also differ in how they are enforced. Claude Code evaluates permission decisions before a command runs, based on the command string and, in auto mode, a separate classifier's judgment about whether the command is safe. The operating system enforces the sandbox boundary on the running process, so it holds regardless of what the model chose to run and even if an allowed command does more than its name suggests.

Filesystem and network restrictions are configured through both sandbox settings and permission rules:

| Setting or rule | What it does |
| :- | :- |
| `sandbox.filesystem.allowWrite` | Grants subprocess write access to paths outside the working directory |
| `sandbox.filesystem.denyWrite` and `sandbox.filesystem.denyRead` | Block subprocess access to specific paths |
| `sandbox.filesystem.allowRead` | Re-allows reading specific paths within a `denyRead` region |
| [`sandbox.filesystem.disabled`](#disable-filesystem-isolation) | Turns the filesystem layer off entirely while keeping network isolation |
| `Edit` allow rules | Grant write access to specific paths, the same way `sandbox.filesystem.allowWrite` does |
| `Read` and `Edit` deny rules | Block access to specific files or directories |
| `WebFetch(domain:...)` allow and deny rules | Control domain access |
| Sandbox `allowedDomains` | Controls which domains Bash commands can reach |
| Sandbox `deniedDomains` | Blocks specific domains even when a broader `allowedDomains` wildcard would otherwise permit them |

Paths and domains from both sandbox settings and permission rules are merged into the final sandbox configuration.

The [claude-code repository's examples directory](https://github.com/anthropics/claude-code/tree/main/examples/settings) includes starter settings configurations for common deployment scenarios, including sandbox-specific examples. Use these as starting points and adjust them to fit your needs.

### Permission modes

`/sandbox` is not a [permission mode](/docs/en/permission-modes). Permission modes decide whether a tool call runs and whether you are prompted first, while the sandbox restricts what a Bash command can access once it runs. They differ in what they control and what replaces the per-action prompt:

| | What it controls | What replaces the prompt |
| :- | :- | :- |
| `/sandbox` | What a Bash command can access once it runs | The sandbox boundary itself, in [auto-allow mode](#sandbox-modes) |
| [Auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode) | Whether each tool call runs | A classifier that reviews actions |
| `--dangerously-skip-permissions` | Whether each tool call runs | Nothing. [Protected path](/docs/en/permission-modes#protected-paths) checks are also skipped; the [actions no mode auto-approves](/docs/en/permission-modes#actions-no-mode-auto-approves) still apply |

The sandbox's [auto-allow mode](#sandbox-modes) is separate from [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode): auto-allow approves Bash commands because the sandbox boundary contains them, while auto mode uses a classifier to review actions. The two work independently and can be combined, with the exceptions listed under [Sandbox modes](#sandbox-modes). To choose an isolation boundary for unattended runs, see [Sandbox environments](/docs/en/sandbox-environments#how-isolation-relates-to-permission-modes). For a table of common permission mode and sandbox pairings with the flags that start each one, see [Common setups](/docs/en/permission-modes#common-setups).

## Configure the sandbox for your organization

Administrators can require sandboxing for every user, keep developers from widening the policy, and route sandbox traffic through a corporate proxy.

### Enforce sandboxing with managed settings

To require the sandbox for every developer, deliver the `sandbox` keys through [managed settings](/docs/en/managed-settings#delivery-mechanisms), either as a file managed by your MDM or through [server-managed settings](/docs/en/server-managed-settings) on claude.ai.

The following managed settings configuration enables the sandbox, refuses to start Claude Code when the platform is unsupported or a dependency is missing, and prevents the model from retrying commands outside the sandbox:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false
  }
}
```

The two keys beyond `enabled` control what happens when the sandbox cannot run a command:

* **`failIfUnavailable`**: a missing dependency such as bubblewrap on Linux blocks Claude Code from starting rather than falling back to unsandboxed execution
* **`allowUnsandboxedCommands: false`**: Claude Code ignores the `dangerouslyDisableSandbox` escape hatch, so when a command fails under the sandbox, Claude can't retry it unsandboxed

Consider these additions alongside them:

* Add `excludedCommands` for any organization-approved tools that must run without isolation, because this configuration [stops a repository's settings from taking commands out of the sandbox](#repository-settings-under-an-admin-required-sandbox)
* Add [`sandbox.credentials`](#protect-credentials) entries for credential directories such as `~/.aws` and `~/.ssh` and for secret environment variables, since the default read policy still allows them

This configuration sandboxes the commands Claude runs. A developer can still type a command at the [`!` shell-mode prompt](/docs/en/interactive-mode#shell-mode-with-prefix) and run it outside the sandbox, with the same access they already have in any terminal outside Claude Code. See [strict sandbox mode](#turn-off-the-retry-with-strict-sandbox-mode) for the sessions where typed commands run sandboxed.

The sandbox doesn't run on native Windows, so with `failIfUnavailable` set, Claude Code exits at startup on those machines. If your fleet includes Windows hosts, you can:

* **Deliver the configuration by operating system**: deploy it through your MDM or as a [managed settings file](/docs/en/managed-settings#delivery-mechanisms) on macOS and Linux machines only. [Server-managed settings](/docs/en/server-managed-settings#current-limitations) apply to all users in the organization
* **Move Windows users into a supported environment**: have them run Claude Code inside WSL2 or a container

### Keep developers from widening the policy

When managed settings set a Boolean key such as `enabled` or `failIfUnavailable`, Claude Code uses the managed value and ignores anything a developer sets locally. For array keys such as `allowRead`, Claude Code merges entries from the scopes the session loads, so a developer can append entries that widen the policy unless a lock covers that key.

Unless managed settings set them, a developer's user settings or `--settings` can turn on the following keys. A repository's `.claude/settings.json` can too, unless the sandbox is [admin-required](#repository-settings-under-an-admin-required-sandbox). Each one weakens the sandbox, so set it to `false` in managed settings if you don't want it used:

* [`enableWeakerNestedSandbox`](/docs/en/settings-reference#sandbox-enableweakernestedsandbox)
* [`enableWeakerNetworkIsolation`](/docs/en/settings-reference#sandbox-enableweakernetworkisolation)
* [`network.allowAllUnixSockets`](/docs/en/settings-reference#sandbox-network-allowallunixsockets)
* [`network.allowLocalBinding`](/docs/en/settings-reference#sandbox-network-allowlocalbinding)
* [`allowAppleEvents`](/docs/en/settings-reference#sandbox-allowappleevents), which a repository can't turn on

Set `allowManagedReadPathsOnly` to `true` in managed settings so that only `allowRead` entries from managed settings are honored. This prevents developers from widening read access beyond the organization-approved paths.

To lock network domains to the managed values the same way, set [`allowManagedDomainsOnly`](/docs/en/settings-reference#sandbox-network-allowmanageddomainsonly). With the lock on, only managed settings can set a [proxy port](#custom-proxy-configuration).

When managed settings configure `sandbox.filesystem` or list any `sandbox.credentials.files` entry with `"mode": "deny"`, only managed settings can set [`filesystem.disabled`](#disable-filesystem-isolation), so developers can't switch off administrator-deployed filesystem restrictions. A [valid](/docs/en/settings-reference#invalid-credential-entries-in-managed-settings) `mask` entry doesn't lock the key. See [Which settings can disable it](#which-settings-can-disable-it).

#### Repository settings under an admin-required sandbox

The sandbox is admin-required while one of these settings is in effect:

* [`allowUnsandboxedCommands`](/docs/en/settings-reference#sandbox-allowunsandboxedcommands) set to `false` in managed settings, or with the `--settings` flag unless managed settings set it to `true`
* [`allowManagedDomainsOnly`](/docs/en/settings-reference#sandbox-network-allowmanageddomainsonly) set to `true` in managed settings

These settings don't turn the sandbox on, so set `enabled` as well.

While the sandbox is admin-required, Claude Code takes the settings that loosen it only from managed settings, the `--settings` flag, and each developer's `~/.claude/settings.json`. It ignores these settings in a repository's `.claude/settings.json` and `.claude/settings.local.json`:

| Repository setting | What Claude Code ignores |
| :- | :- |
| `excludedCommands`, `ignoreViolations`, `network.allowedDomains`, `network.allowUnixSockets`, `network.allowMachLookup`, `network.httpProxyPort`, `network.socksProxyPort` | Every entry |
| `filesystem.allowWrite`, `Edit(...)` allow rules, `permissions.additionalDirectories` | The write access each entry gives sandboxed commands. Claude's file tools still follow the `Edit(...)` rules and additional directories |
| `WebFetch(domain:...)` allow rules | The host each rule adds to the sandbox allowlist. The WebFetch tool still follows the rule |
| `enableWeakerNestedSandbox`, `enableWeakerNetworkIsolation`, `network.allowAllUnixSockets`, `network.allowLocalBinding` | `true`. A `false` still applies |
| `enabled`, `failIfUnavailable` | `false`, when the developer's `~/.claude/settings.json` sets `true` |
| `filesystem.allowRead` | An entry at or under a path that managed settings, `--settings`, or user settings deny reading, or a glob that could match one |

These settings still apply while the sandbox is admin-required:

* **In a repository's files**: deny entries and the `autoAllowBashIfSandboxed` value. Set the key in managed settings to keep a repository from changing it
* **In a developer's own settings**: the settings in the table still apply from `~/.claude/settings.json` or `--settings`, unless a managed-only lock such as `allowManagedDomainsOnly` covers them. Most of them, such as `excludedCommands` and `filesystem.allowWrite`, have no managed-only lock

The configuration under [Enforce sandboxing with managed settings](#enforce-sandboxing-with-managed-settings) makes the sandbox admin-required. Add the `excludedCommands`, `allowWrite`, and socket entries that your approved tools need to managed settings, because a repository can't supply them.

Requires Claude Code v2.1.285 or later. From v2.1.282 to v2.1.284, the same settings made Claude Code ignore a repository's `excludedCommands` entries.

#### Locks that apply without an admin-required sandbox

Some settings make Claude Code ignore the repository keys that directly override one restriction, even when the sandbox isn't admin-required. Each one has this effect only when you set it in a file its row names, and the repository's other sandbox settings still apply. Requires Claude Code v2.1.285 or later.

| Setting | Where you set it | What Claude Code ignores in a repository's settings |
| :- | :- | :- |
| `network.deniedDomains` or a `WebFetch(domain:...)` deny rule | Managed settings, `--settings` | `httpProxyPort` and `socksProxyPort` |
| `network.strictAllowlist` | Managed settings, `--settings`, user settings | The proxy ports, `allowedDomains`, and `WebFetch(domain:...)` allow rules |
| `filesystem.denyRead`, a `Read(...)` deny rule, or a `credentials.files` entry | Managed settings, `--settings` | An `allowRead`, `allowWrite`, `Edit(...)` allow, or `additionalDirectories` entry at or under a path that managed settings, `--settings`, or user settings deny reading, or a glob that could match one |

These locks change what sandboxed commands can reach. The WebFetch tool and Claude's file tools still follow a repository's rules and additional directories.

### Custom proxy configuration

To inspect, filter, or log sandbox traffic with your own tooling, replace the built-in sandbox proxy with a proxy you run on the same machine.

To route sandbox traffic through a corporate proxy elsewhere on your network, set `HTTPS_PROXY` instead, as the **Corporate proxy** entry under [Network isolation](#network-isolation) describes. That way, Claude Code's allowlist still applies.

To direct sandboxed commands to your proxy, set the localhost ports it listens on in [sandbox settings](/docs/en/settings-reference#sandbox-settings):

```json theme={null}
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

If you set a port and also set `HTTPS_PROXY` or `HTTP_PROXY`, Claude Code doesn't forward what sandboxed commands send to your proxy on to the proxy those variables name. To reach a corporate proxy, configure your own proxy to forward to it.

Which files can set a port depends on your other sandbox settings. The first case that matches applies:

* **`allowManagedDomainsOnly` is on**: managed settings only
* **The sandbox is [admin-required](#repository-settings-under-an-admin-required-sandbox), or a [narrower network lock](#locks-that-apply-without-an-admin-required-sandbox) applies**: managed settings, `--settings`, and user settings
* **Otherwise**: any settings file

Claude Code ignores a port set anywhere else. Before v2.1.285, any settings file could set a port.

<Warning>
  Once either port applies, your proxy is responsible for filtering everything sent to it. Claude Code's own network controls, such as `allowedDomains`, `deniedDomains`, `strictAllowlist`, approval prompts, and the [local-address check](#hostnames-that-resolve-to-local-addresses), stop applying to that traffic. A sandboxed command can connect to either proxy, so if you set only one port, Claude Code's domain lists on the other proxy don't limit what the command reaches through yours.
</Warning>

## Troubleshooting

Some commands fail inside the sandbox even though they work outside it. Find the heading that matches your symptom or error message.

If your organization's sandbox is [admin-required](#repository-settings-under-an-admin-required-sandbox), Claude Code ignores the settings these fixes name in a project's settings files, so save them in `~/.claude/settings.json`, where they apply in every project. If a fix still has no effect, your organization's managed settings may set that key.

A fix that adds an `excludedCommands` pattern removes the sandbox from the commands the pattern matches. See [what an excluded command can do](#run-commands-outside-the-sandbox-with-excludedcommands).

### Commands fail with a host-not-allowed error

Many CLI tools need to reach specific hosts. Approve the host when prompted, or add it to [`allowedDomains`](/docs/en/settings-reference#sandbox-network-alloweddomains). If your organization locks the allowlist with `allowManagedDomainsOnly`, there's no prompt, so ask your administrator to add the host.

### `jest` hangs or fails

`watchman` is incompatible with the sandbox. Run `jest --no-watchman` instead.

### Go-based CLIs fail TLS verification on macOS

Tools such as `gh`, `gcloud`, and `terraform` may fail TLS verification under [Seatbelt](#os-level-enforcement). To run these tools outside the sandbox, add a pattern for each tool, such as `gh *`, to [`excludedCommands`](#run-commands-outside-the-sandbox-with-excludedcommands). The tool then runs with your full access and its stored credentials. If you are using `httpProxyPort` with a MITM proxy and custom CA, set [`enableWeakerNetworkIsolation`](/docs/en/settings-reference#sandbox-enableweakernetworkisolation) to `true` instead.

### `open`, `osascript`, or browser-based auth flows fail with error `-600` on macOS

The sandbox blocks Apple Events by default. Set [`allowAppleEvents`](/docs/en/settings-reference#sandbox-allowappleevents) to `true` in your user, managed, or CLI settings to allow them. Claude Code ignores this key in project settings.

Enabling `allowAppleEvents` removes code-execution isolation, since sandboxed commands can then launch other applications unsandboxed with no user prompt, and can send AppleScript commands to running applications, subject to the macOS automation-consent prompt (TCC). Alternatively, add a pattern such as `open *` to [`excludedCommands`](#run-commands-outside-the-sandbox-with-excludedcommands). Each `open` call then goes through the permission flow, and `open` can launch any file or app, including one Claude wrote.

### `docker` commands fail

`docker` is incompatible with the sandbox. Take the `docker` commands you need out of the sandbox with an `excludedCommands` pattern such as `docker compose *`. [Run commands outside the sandbox with `excludedCommands`](#run-commands-outside-the-sandbox-with-excludedcommands) explains what an excluded `docker` command can reach. A narrower pattern takes fewer commands out of the sandbox.

### `pbcopy`, `xclip`, or `wl-copy` doesn't update the clipboard

The `pbcopy`, `xclip`, and `wl-copy` clipboard utilities can fail to reach the system clipboard from inside the sandbox, in which case the text piped to them doesn't arrive.

To put Claude's output on your clipboard, ask Claude to print it in its response, then run [`/copy`](/docs/en/commands). `/copy` writes to the clipboard from the Claude Code process rather than from a sandboxed command.

When Claude pipes text to one of these tools, adding the tool to [`excludedCommands`](/docs/en/settings-reference#sandbox-excludedcommands) doesn't take that call out of the sandbox on its own.

### A git command fails with `unable to unlink old`

`git merge`, `git checkout`, and similar commands fail with `unable to unlink old` when they need to replace a file the sandbox denies writes to. On Linux and WSL2 the error ends with `Read-only file system`. The file can be in one of these places:

* Under a [protected path](#protected-paths) such as `.claude/skills`
* Under one of your `denyWrite` entries
* Outside the directories the sandbox lets commands write to at all

After the failure, Claude may [offer to rerun the command outside the sandbox](#the-unsandboxed-retry-escape-hatch). Approve that retry, or run the git command yourself in another terminal. If you've set `allowUnsandboxedCommands` to `false`, Claude can't offer the retry, so run the command yourself.

### Bubblewrap fails to start inside a container

In an unprivileged container, [bubblewrap](#os-level-enforcement) can't mount a fresh `/proc` filesystem, so sandboxed commands fail with a `bwrap` error such as `Can't mount proc on /newroot/proc: Operation not permitted`. Set [`enableWeakerNestedSandbox`](/docs/en/settings-reference#sandbox-enableweakernestedsandbox) to `true` so the sandbox bind-mounts the container's existing `/proc` instead. Only use this setting when the outer container already provides the isolation boundary you need, since the setting exposes process information to sandboxed commands that a fresh `/proc` mount would hide.

### 0-byte read-only files appear at `.claude` settings paths, and "Yes, and don't ask again" doesn't save

On Linux and WSL2, the sandbox holds a write denial on a file that doesn't exist yet by creating a 0-byte read-only placeholder there while a sandboxed command runs. The sandbox removes the placeholder afterward. If a session is killed before that cleanup runs, for example by SIGKILL, the placeholders stay behind. Later sessions bind the placeholders read-only again on every start, so a settings write such as saving a permission choice fails at a path where a placeholder remains.

Run `claude doctor` in your terminal to list the leftover placeholder files. The [`Stale sandbox mask files left by a killed session`](/docs/en/errors#stale-sandbox-mask-files-left-by-a-killed-session) warning names some of them and counts the rest. Delete each file with `rm` while no other Claude Code session is running in that project. Before v2.1.257, Claude Code left the same placeholders behind without flagging them.

### `git` over SSH fails with the sandbox on

On macOS, `git fetch`, `git pull`, and `git push` against an SSH remote fail inside the sandbox even when the host is allowed. On Linux and WSL2, they work once the host is allowed. Claude Code tunnels git's SSH connection through the [sandbox proxy](#network-isolation), and the macOS tunnel can't authenticate to that proxy.

On Linux and WSL2, check these if the connection still fails:

* **The host is allowed on port 22**: an `allowedDomains` entry with no port, such as `"git.example.com"`, covers it
* **Your corporate proxy permits port 22**: if your network requires an upstream proxy, the tunnel goes through it too
* **The key is readable as a file**: the sandbox can block the `ssh-agent` socket, and a `denyRead` or `credentials` entry for `~/.ssh` hides your key files

On macOS, switch the remote to HTTPS, which needs HTTPS credentials such as a personal access token:

```bash theme={null}
git remote set-url origin https://git.example.com/example-org/example-repo.git
```

If you have to keep the SSH remote, take git's network commands out of the sandbox with [`excludedCommands`](#run-commands-outside-the-sandbox-with-excludedcommands):

```json theme={null}
{
  "sandbox": {
    "excludedCommands": ["git fetch *", "git pull *", "git push *"]
  }
}
```

These entries match `git push origin main`. A call that adds a `cd`, uses `git -C`, or contains a command substitution stays sandboxed. The excluded git commands can reach any host, not only the ones in `allowedDomains`.

Plain `ssh`, `scp`, and `rsync` over SSH fail for the reason [the database client entry](#a-database-client-or-other-non-http-tool-fails-to-reach-an-allowed-host) gives.

### A database client or other non-HTTP tool fails to reach an allowed host

A tool that ignores the proxy environment variables can't connect from inside the sandbox, even to a host in `allowedDomains`. A sandboxed command has [no direct route to the network](#network-isolation), so a tool that opens its own connection fails. Most database drivers, plain `ssh`, and tools that use UDP behave this way.

The failure looks like a network or name resolution error:

* **macOS**: `Operation not permitted`, or a name resolution error such as `Could not resolve host`
* **Linux and WSL2**: `Network is unreachable`, or a name resolution error such as `Temporary failure in name resolution`

A tool that uses the proxy fails differently when its host isn't allowed. You get a network prompt, or the tool receives a `403` response from the proxy.

To let the tool connect, run the command that needs it outside the sandbox with [`excludedCommands`](#run-commands-outside-the-sandbox-with-excludedcommands). This example excludes one script and adds an [ask rule](/docs/en/permissions) so that you approve each run:

```json theme={null}
{
  "sandbox": {
    "excludedCommands": ["python scripts/load_orders.py *"]
  },
  "permissions": {
    "ask": ["Bash(python scripts/load_orders.py *)"]
  }
}
```

The script runs with your full access, and Claude can edit a script that's inside your working directory, so review it when the prompt appears.

### A command fails to reach a server on localhost

By default, a sandboxed command can't connect directly to a server that's running on your machine outside the sandbox, such as a dev server or a database in a container. What you can change depends on your platform:

* **macOS**: set [`network.allowLocalBinding`](/docs/en/settings-reference#sandbox-network-allowlocalbinding) to `true`. Sandboxed commands can then listen on network ports and connect to any port on localhost, which includes every other service listening there. A localhost service that doesn't require authentication, such as a debugger, can then act for the command outside the sandbox, and a command that listens on a non-loopback address accepts connections from other machines
* **Linux and WSL2**: a sandboxed command's `localhost` is private to that command. The command can listen on a port and reach servers it started itself. A direct connection to `localhost` or `127.0.0.1` doesn't reach servers on the host, and `allowLocalBinding` has no effect. Run the command that needs the host's server outside the sandbox with [`excludedCommands`](#run-commands-outside-the-sandbox-with-excludedcommands), where it has no filesystem or network limits. For connections that go through the sandbox proxy, see [Hostnames that resolve to local addresses](#hostnames-that-resolve-to-local-addresses)

This example turns the setting on for macOS:

```json theme={null}
{
  "sandbox": {
    "network": {
      "allowLocalBinding": true
    }
  }
}
```

An `allowedDomains` entry for `localhost` applies to connections that go through the proxy, so it doesn't change a direct connection. Claude Code sets `NO_PROXY` for sandboxed commands so that they connect to `localhost` directly instead of through the proxy. The entry also exposes every port on your machine's localhost to a command that does use the proxy. For a development hostname that points at `127.0.0.1`, see [An allowed hostname is refused with `resolved to a loopback address`](#an-allowed-hostname-is-refused-with-resolved-to-a-loopback-address).

### An allowed hostname is refused with `resolved to a loopback address`

The sandbox proxy refuses an allowed hostname that [resolves to a local address](#hostnames-that-resolve-to-local-addresses), which affects development names such as `myapp.test` that point at `127.0.0.1`. The command sees a `403` response whose body names the kind of address, such as `Connection to myapp.test blocked: resolved to a loopback address`.

Add the IP address the name resolves to alongside the hostname in `allowedDomains`, each with the port your server listens on:

```json theme={null}
{
  "sandbox": {
    "network": {
      "allowedDomains": ["myapp.test:3000", "127.0.0.1:3000"]
    }
  }
}
```

An IP address entry with no port lets sandboxed commands reach every service listening on that address.

Before v2.1.284, the proxy connected to whatever address an allowed hostname resolved to.

### `/sandbox` fails with `Sandbox settings are overridden by a higher-priority configuration`

`/sandbox` prints `Error: Sandbox settings are overridden by a higher-priority configuration and cannot be changed locally.` instead of opening its panel when a higher [settings level](/docs/en/settings#settings-precedence) sets `sandbox.enabled`, `sandbox.autoAllowBashIfSandboxed`, or `sandbox.allowUnsandboxedCommands`. The panel saves your choices to `.claude/settings.local.json`, and a value saved there can't override those levels.

Managed settings and `--settings` rank above local settings. To see which of them this session loaded, run `/status` and read the `Setting sources` line:

* **`Command line arguments`**: if you started Claude Code with [`--settings`](/docs/en/settings#change-a-setting-for-one-session), check whether the file or JSON you passed sets one of those keys. If it does, change the value there, or start Claude Code again without those keys.
* **`Enterprise managed settings`**: your organization's managed settings are loaded. If they set one of those keys, you can't change that key from `/sandbox` or from any settings file you control, so ask your administrator.

## Limitations

Sandboxing reduces risk but is not a complete isolation boundary. Review the limitations below before relying on it as a hard security control.

### Security limitations

* **Network filtering**: the sandbox restricts which domains processes can connect to. By default the built-in proxy does not terminate or inspect TLS on outbound traffic, so the contents of encrypted connections are not examined. The experimental [`network.tlsTerminate`](/docs/en/settings-reference#sandbox-network-tlsterminate) setting terminates TLS at the proxy for [`mask` credential substitution](#mask-credentials) but does not add content filtering. You are responsible for ensuring that only trusted domains are allowed in your policy.

<Warning>
  Allowing broad domains such as `github.com` can create paths for data exfiltration. Because the proxy makes its allow decision from the client-supplied hostname without inspecting TLS, code running inside the sandbox can potentially use [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting) or similar techniques to reach hosts outside the allowlist. If your threat model requires stronger guarantees, configure a [custom proxy](#custom-proxy-configuration) that terminates TLS and inspects traffic, and install its CA certificate inside the sandbox. Stronger TLS-aware network isolation is an active area of development.
</Warning>

* **Privilege escalation via Unix sockets**: the `allowUnixSockets` configuration can inadvertently grant access to system services that could lead to sandbox bypasses. For example, allowing access to `/var/run/docker.sock` effectively grants access to the host system through the Docker socket. Consider carefully any Unix sockets that you allow through the sandbox.
* **Filesystem permission escalation**: overly broad filesystem write permissions can enable privilege escalation attacks. Allowing writes to directories containing executables in `$PATH`, system configuration directories, or user shell configuration files such as `.bashrc` or `.zshrc` can lead to code execution in different security contexts when other users or system processes access these files.
* **Linux sandbox strength**: the Linux implementation provides strong filesystem and network isolation but includes an `enableWeakerNestedSandbox` mode that enables it to work inside Docker environments without privileged namespaces. This option considerably weakens security and should only be used when additional isolation is otherwise enforced.
* **Apple Events on macOS**: the macOS sandbox blocks Apple Events by default. The `allowAppleEvents` setting lifts this restriction so tools such as `open` and `osascript` work, but it removes code-execution isolation: sandboxed commands can launch other applications unsandboxed with no user prompt, and can send AppleScript commands to running applications, subject to the per-app macOS automation-consent prompt (TCC). It is only honored from user, managed, or CLI settings. Project settings cannot enable it.

### Scope

The sandbox isolates shell commands and their child processes. [What runs outside the sandbox](#what-runs-outside-the-sandbox) lists the tools and helper processes it doesn't cover. Computer use and subagents relate to the sandbox as follows:

* **Computer use**: when Claude opens apps and controls your screen, it runs on your actual desktop rather than in an isolated environment. Per-app permission prompts gate each application. See [computer use in the CLI](/docs/en/computer-use) or [computer use in Desktop](/docs/en/desktop#let-claude-use-your-computer).
* **Subagents**: [subagents](/docs/en/sub-agents) run in the same process as the parent session and use the same sandbox configuration. Bash commands inside a subagent are sandboxed when sandboxing is enabled in the parent session.
* **Mods**: a [mod](/docs/en/plugins/mods/overview) is a plugin that runs its own code inside Claude Code, and a process that a mod starts runs outside the sandbox. See [What a mod can reach](/docs/en/plugins/mods/overview#what-a-mod-can-reach).

<Warning>
  Effective sandboxing requires both filesystem and network isolation. Without network isolation, a compromised agent could exfiltrate sensitive files like SSH keys. Without filesystem isolation, whether from a permissive policy or from [disabling the filesystem layer](#disable-filesystem-isolation), a compromised agent could backdoor system resources to gain network access. When you widen the defaults, check that an `allowWrite` path, a broad `allowedDomains` entry, or an `excludedCommands` exception does not undo a restriction on the other side.
</Warning>

## See also

* [Sandbox environments](/docs/en/sandbox-environments): compare the built-in sandbox with dev containers, containers, and VMs
* [Security](/docs/en/security): comprehensive security features and best practices
* [Permissions](/docs/en/permissions): permission configuration and access control
* [All settings](/docs/en/settings-reference): every settings key
* [CLI reference](/docs/en/cli-reference): command-line options
