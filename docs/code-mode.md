> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Run tool calls from code with Code Mode

> Try Code Mode, an experimental feature in which Claude writes JavaScript that makes several tool calls in one step.

Code Mode changes how Claude uses its [tools](https://code.claude.com/docs/en/tools-reference.md). Without Code Mode, Claude asks for tool calls such as Bash, Read, or Edit directly and reads each result before it decides what to do next. With Code Mode, Claude writes a piece of JavaScript that makes the tool calls, and Claude Code runs that code in your session.

> [!NOTE]
>
> Code Mode is experimental and off by default. It may change or be removed in any release. To share feedback, run `/feedback`.

## How Code Mode works

In a Code Mode session, you still describe your task in a prompt, and Claude writes JavaScript to carry it out. One piece of code can run commands in parallel, use one result in the next call, and return the part of the output that Claude needs to read.

For example, if you ask Claude to raise a retry limit, Claude might write this code to find the file, edit it, and run the tests. The last line returns the file's path and the test output to Claude:

```javascript theme={null}
const files = await $`rg -l "function retryPolicy" src`.text();
const target = files.trim().split("\n")[0];
await edit(target, "maxAttempts: 3", "maxAttempts: 5");
({ edited: target, tests: $`npm test -- retryPolicy`.nothrow() });
```

In the conversation, you see the tool calls, such as the edit's diff, and not the code. To read the code, press `Ctrl+O` to open the [transcript viewer](https://code.claude.com/docs/en/interactive-mode.md#transcript-viewer). Each piece of code appears there as a collapsed **Code** row, with a hint for how to expand it.

### When to use Code Mode

Try Code Mode on tasks that take many related tool calls, such as:

* A change that repeats across many files
* A search whose results need filtering before Claude reads them
* Several independent commands that can run at the same time

### Code Mode limitations

Before you turn on Code Mode, check that you can accept these limits:

* **Resuming**: you can resume a Code Mode session only with Code Mode on. After a Code Mode session has run with a Claude subscription or a Console account, you can't resume it on a cloud provider such as Amazon Bedrock
* **Auto mode**: auto mode's classifier [reviews the code, not each tool call](#permission-checks)
* **Long-running code**: unless [code can run in the background](#long-running-code), you wait for it to finish, and it stops after ten minutes
* **Hooks**: by default, expect a [refused tool call](#tool-call-refused-by-a-hook) when a `PreToolUse` hook doesn't finish, and a [call that can still run](#tool-call-ran-after-a-hook-failed) when the hook fails another way
* **Unavailable features**: you can't use [Remote Control](https://code.claude.com/docs/en/remote-control.md), [Claude in Chrome](https://code.claude.com/docs/en/chrome.md), or [computer use](https://code.claude.com/docs/en/computer-use.md)
* **Moving the session**: you can't move the session to the Desktop app or turn it into a [background session](https://code.claude.com/docs/en/agent-view.md), and `/fork` can't start a background copy

## Requirements

* **Version**: Claude Code v2.1.323 or later, on either [release channel](https://code.claude.com/docs/en/setup.md#configure-release-channel). An older version starts without Code Mode, with or without the reason `it isn't open to your account yet`
* **Account or provider**: a Claude subscription, a Console account, or a [cloud provider](https://code.claude.com/docs/en/feature-availability.md#availability-by-model-provider) such as Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry. With a cloud provider, you need v2.1.331 or later. You can't use Code Mode through a [gateway](https://code.claude.com/docs/en/gateways.md) or with Claude for Government. If you reach a cloud provider with an [Enterprise Admin Console sign-in](https://code.claude.com/docs/en/authentication.md#log-in-to-claude-code), you need Agent Platform, or Amazon Bedrock without the [Mantle endpoint](https://code.claude.com/docs/en/amazon-bedrock.md#use-the-mantle-endpoint)
* **Organization**: your organization doesn't use the [HIPAA configuration](https://code.claude.com/docs/en/hipaa-setup.md) or [zero data retention](https://code.claude.com/docs/en/zero-data-retention.md)
* **Model**: Claude Opus 5.5, Sonnet 5.5, Haiku 5.5, or Fable 5.2. If you select the model by a deployment name or an application inference profile, ask whoever manages that name whether it points to one of these models
* **Surface**: an interactive `claude` session in a terminal. Code Mode doesn't work with the VS Code panel, the Desktop app, or cloud sessions
* **Agent teams**: to use Code Mode with [agent teams](https://code.claude.com/docs/en/agent-teams.md) on, you need v2.1.326 or later. Teammates run in Code Mode in the default [in-process display mode](https://code.claude.com/docs/en/agent-teams.md#choose-a-display-mode), and start without it in split panes
* **Mods**: to use Code Mode with a [mod](https://code.claude.com/docs/en/plugins/mods/overview.md) that hooks tool calls, you need v2.1.327 or later. If you're on the `stable` channel and an update doesn't reach that version, [switch to `latest`](https://code.claude.com/docs/en/setup#configure-release-channel)
* **Telemetry settings**: to use Code Mode with [feature-flag fetching off](https://code.claude.com/docs/en/env-vars.md#features-that-need-feature-flag-fetching) or [OpenTelemetry](https://code.claude.com/docs/en/monitoring-usage.md) events and metrics on, you need v2.1.329 or later. Keep [tracing](https://code.claude.com/docs/en/monitoring-usage.md#traces-beta) off on any version
* **Installation**: the [native build](https://code.claude.com/docs/en/setup.md) of Claude Code
* **Windows**: [Git for Windows](https://git-scm.com/downloads/win) is installed

You also can't start Code Mode with some settings on, such as an API key helper on a direct connection to Anthropic. For the fix for each, see [Code Mode doesn't start](#code-mode-doesnt-start).

## Try Code Mode

Turn on Code Mode, give Claude a task, and look at the code that Claude wrote.

**1. Check your version**

Run `claude --version`. If the version is older than the one you [need for your setup](#requirements), run `claude update`. If you're on the `stable` channel and the update doesn't reach that version, wait for `stable` to catch up or [switch to `latest`](https://code.claude.com/docs/en/setup#configure-release-channel).

**2. Start Claude Code with Code Mode on**

Set the [`CLAUDE_CODE_EXPERIMENTAL_CODE_MODE`](https://code.claude.com/docs/en/env-vars#variables) environment variable to `1`. To try Code Mode, set it in your shell. To turn on Code Mode for every new session, set it in your user settings.

> [tab] macOS, Linux, WSL
>
> ```bash theme={null}
> CLAUDE_CODE_EXPERIMENTAL_CODE_MODE=1 claude
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> $env:CLAUDE_CODE_EXPERIMENTAL_CODE_MODE = "1"
> claude
> ```

> [tab] settings.json
>
> Save this `env` block in `~/.claude/settings.json` and start `claude`:
>
> ```json theme={null}
> {
>   "env": {
>     "CLAUDE_CODE_EXPERIMENTAL_CODE_MODE": "1"
>   }
> }
> ```
>
> Claude Code [ignores this variable in a project's settings files](https://code.claude.com/docs/en/settings-reference.md#variables-claude-code-ignores-in-env), so a repository you clone can't turn on Code Mode for you.

**3. Confirm that you want Code Mode**

Claude Code asks you to confirm before your first Code Mode session. Select **Yes, turn on Code Mode**. Claude Code restarts and shows this line near the top of the session:

```text theme={null}
Code Mode (experimental) is on · this session can be resumed only with Code Mode on
```

If you see a different line or none, see [Code Mode doesn't start](#code-mode-doesnt-start).

**4. Give Claude a task with many tool calls**

In a project you know, send a prompt such as this one:

```text theme={null}
Read every Markdown file in this project and list the links that point to local files that don't exist.
```

**5. Read the code Claude wrote**

Press `Ctrl+O` and expand a **Code** row to see the JavaScript behind the tool calls. Press `Ctrl+O` again to return to the conversation.

> [!WARNING]
>
> To resume a Code Mode session later, keep `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` set to `1` when you run `claude --continue` or `claude --resume`. With Code Mode off, Claude Code refuses to resume the session. Sessions that you started without Code Mode resume without Code Mode, even with the variable set.

### Use Code Mode in subagents

If your [subagent](https://code.claude.com/docs/en/sub-agents.md) has a `tools` list, add [`REPL`](https://code.claude.com/docs/en/tools-reference) to the list so that the subagent uses Code Mode:

```yaml theme={null}
tools: Read, Bash, REPL
```

### Turn off Code Mode

Remove `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` from your shell, `~/.claude/settings.json`, and any `--settings` file, then start a new session. You can also keep the variable and change its value to `0` in any of them. With a `0` in one place, Code Mode stays off even if you set `1` in another.

### Block Code Mode for your organization

Add `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` with the value `0` to your [managed settings](https://code.claude.com/docs/en/managed-settings.md) so that nobody in your organization can use Code Mode:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_CODE_MODE": "0"
  }
}
```

If your users can connect through a cloud provider, deploy this setting through [MDM or a managed settings file](https://code.claude.com/docs/en/managed-settings.md#delivery-mechanisms). A user who sets a provider variable such as `CLAUDE_CODE_USE_BEDROCK` in their shell or user settings can start Code Mode without receiving [server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md#platform-availability).

Users who are in a Code Mode session stay in it until they exit or restart Claude Code. After that, your users start without Code Mode and can't resume their Code Mode sessions while the `0` is in place. You can't turn on Code Mode for your users from managed settings.

### Monitor Code Mode with OpenTelemetry

If you collect [OpenTelemetry events](https://code.claude.com/docs/en/monitoring-usage.md#events), your backend receives `tool_decision` and `tool_result` events for the tool calls in the code that Claude writes, under each tool's usual name, such as `Bash`. Update your queries and settings for these calls:

* **Find calls from code**: filter on `tool_use_id` values that start with `repl_` or `toolu_cc_`. The `REPL` tool, which runs the code, has events of its own without either prefix
* **Read classifier verdicts**: in auto mode, a call that the classifier's [review of the code](#permission-checks) covers has no `classifier_verdict`. Look for the verdict on the `REPL` tool's `tool_decision` events that have that call's `request_id`. If you find more than one, the events don't show which piece of code made the call
* **Keep secrets out of your backend**: code can read a value, such as a token in a file, and pass it to another call. Leave `OTEL_LOG_TOOL_DETAILS` unset if your backend shouldn't receive those values

## Permissions and long-running code

Your permission mode decides how the code that Claude writes is checked and whether you can talk to Claude while the code runs.

### Permission checks

In auto and `bypassPermissions` modes, code can run from start to finish without a permission prompt. Some calls still prompt you, such as the [actions no mode auto-approves](https://code.claude.com/docs/en/permission-modes.md#actions-no-mode-auto-approves).

To control tool calls in the code, write `deny` and `ask` [permission rules](https://code.claude.com/docs/en/permissions.md) and [`PreToolUse` hooks](https://code.claude.com/docs/en/hooks#pretooluse) under the tool's usual name, such as `Bash` or an [MCP tool's name](https://code.claude.com/docs/en/permissions.md#mcp). Beyond rules and hooks, a classifier reviews the code in auto mode, and you answer prompts in the modes that ask:

* **[Auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode)**: the classifier reviews each piece of code before it runs, not each tool call. It doesn't see values computed at run time, such as a path taken from search output, so keep rules or hooks for calls you must control. You can still be [prompted for some calls](#permission-prompt-with-a-countdown), such as calls in code that you approved yourself after repeated classifier blocks
* **Other [permission modes](https://code.claude.com/docs/en/permission-modes.md)**: you're prompted for each tool call that would prompt you in that mode

If you have a `PreToolUse` hook that allows or blocks shell commands, make it check each part of a command, as [Bash rules do](https://code.claude.com/docs/en/permissions.md#compound-commands). In Code Mode, a `git push` in a folder named `app` can reach your hook as `cd 'app' && git push`.

To check the code itself, write a `PreToolUse` hook that matches `REPL`, the tool that runs the code, and read the JavaScript from `tool_input.code`. To check what the code returns, see [Check code output with a hook](#check-code-output-with-a-hook).

> [!WARNING]
>
> Bash rules match command text, so Claude can run a denied command [in a form the rule doesn't match](https://code.claude.com/docs/en/permissions.md#bash-rule-limits), with or without Code Mode. For limits that don't depend on command text, see [sandboxing](https://code.claude.com/docs/en/sandboxing.md).

#### Require approval for a command

To see a prompt for a specific command in auto or `bypassPermissions` mode, add an `ask` rule for it. You're prompted for the [forms of the command that the rule matches](https://code.claude.com/docs/en/permissions.md#bash-rule-limits). To be prompted for commands that start with `git push`, save this rule in `~/.claude/settings.json`:

```json theme={null}
{
  "permissions": {
    "ask": ["Bash(git push *)"]
  }
}
```

To test the rule, start a new session in auto mode in a repository with no remote, and ask Claude to run `git push origin main`. You see a prompt for that command.

#### Approve each piece of code first

To read and approve code before it starts, add an `ask` rule for `REPL`, the tool that runs the code. Save this rule in `~/.claude/settings.json`:

```json theme={null}
{
  "permissions": {
    "ask": ["REPL"]
  }
}
```

To test the rule, start a new session and give Claude a task. You see a prompt that doesn't include the code. To read the code before you answer, press `Ctrl+O`, expand the **Code** row, and press `Ctrl+O` again to return. From the main conversation, you don't see a [subagent](https://code.claude.com/docs/en/sub-agents.md)'s code in that view.

If you approve in auto mode, the code starts even when the classifier would have blocked it, and its project edits and read-only commands run without a prompt. If Claude reports that the code can't start a subagent, remove the rule.

#### Answer a permission prompt while code runs

To stop the code at a prompt for one of its tool calls, answer **No** without a comment. These results apply to prompts that aren't labeled as coming from a subagent:

* **No, or `Esc`**: the code stops, and changes from calls that already finished stay in place
* **No, with a [comment](https://code.claude.com/docs/en/permissions.md#add-a-comment-when-you-answer-a-permission-prompt)**: the call is refused, and the code can continue with its other calls

### Limit shell commands with the sandbox

Your [sandbox](https://code.claude.com/docs/en/sandboxing.md) settings apply to the shell commands that code runs. The JavaScript itself and its file, web, and MCP tool calls run [outside the sandbox](https://code.claude.com/docs/en/sandboxing.md#what-runs-outside-the-sandbox). To isolate the JavaScript and those calls too, run Claude Code in a [container or virtual machine](https://code.claude.com/docs/en/sandbox-environments.md).

To keep commands in the sandbox when code requests to run them unsandboxed, turn on [strict sandbox mode](https://code.claude.com/docs/en/sandboxing.md#turn-off-the-retry-with-strict-sandbox-mode). In auto mode, the classifier reviews the code that makes the request, and the command has no separate review.

### Long-running code

While code runs a long build or test, Claude either waits for it or lets it continue in the background:

* **Waiting**: Claude answers after the code finishes, and the code stops after ten minutes. In Manual and `acceptEdits` [modes](https://code.claude.com/docs/en/permission-modes.md#available-modes), time you spend at a tool's permission prompt doesn't count toward the ten minutes. Before v2.1.328, that time counted.
* **Background**: you can keep talking to Claude, and the code can run for up to two hours

For background code, start your session in auto or `bypassPermissions` mode. If Claude still waits, check your current mode and how you started the session:

* **You're on a version before v2.1.328 and picked the session from the `claude --resume` list**: exit, [update Claude Code](https://code.claude.com/docs/en/setup.md#update-claude-code), then run the same `claude --resume` command with Code Mode on. To stay on your version, replace `--resume` with `--continue`. If Claude still waits after the update, start a new session in auto mode
* **You passed tool names to `--tools`**: start a new session in auto mode, with Code Mode on and without that flag
* **The session first started in auto or `bypassPermissions` mode**: press `Shift+Tab` until you're back in that mode. If that doesn't help, exit, then run `claude --continue --permission-mode auto` with Code Mode on
* **The session first started in another mode**: if [auto mode is available](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode) to you, exit, then run `claude --permission-mode auto` with Code Mode on to start a new session. On v2.1.331 or later, expect Claude to keep waiting if you resume the old session instead

### Stop code in progress

To stop code while Claude is responding or waiting for the code, press `Esc`. To stop background code after Claude finishes responding, run [`/tasks`](https://code.claude.com/docs/en/commands) in the session, select the running task, and press `x`.

After you stop the code, check `/tasks` for [subagents](https://code.claude.com/docs/en/sub-agents.md), [shell commands](https://code.claude.com/docs/en/interactive-mode.md#background-bash-commands), and [MCP calls](https://code.claude.com/docs/en/mcp.md#automatic-backgrounding-of-long-tool-calls) that the code started and that are still running. To stop one, select it and press `x`.

### Check code output with a hook

To check or redact what the code returns, write a [`PostToolUse` hook](https://code.claude.com/docs/en/hooks#posttooluse) that matches `REPL`, the tool that runs the code. The same hook runs when [background code](#long-running-code) finishes and when code throws an error.

#### Read code output in the hook

In your `PostToolUse` hook, read the output from `tool_response`, which has fields such as these:

```json theme={null}
{
  "code": "(await $`cat notes.txt`.text())",
  "result": "deploy token: abc123",
  "stdout": "",
  "stderr": "",
  "toolsUsed": ["Bash"]
}
```

#### Redact code output

To hide part of the output, return a changed copy of `tool_response` as [`updatedToolOutput`](https://code.claude.com/docs/en/hooks#posttooluse-decision-control), and build the copy this way:

* **Change the text**: redact `result`, `stdout`, `stderr`, and `error`. Handle a `result` that's missing or `null`, and expect `error` only when the code failed or was stopped
* **Keep the shape**: return `code`, `stdout`, and `stderr` as strings, and return `error` as a string or leave it out. If you break this shape, Claude gets the original output
* **Remove images, PDFs, and page errors**: if the copy has `images`, `documents`, or `imagePagesFailed` to hide, set that field to `[]`. The `imagePagesFailed` field lists the file path and error for each PDF page that couldn't be shown
* **Remove the path to long output**: on v2.1.331 or later, omit `uncutOutputNote` from the copy. The field gives Claude a path to the uncut text

To hide the deploy token in the `notes.txt` result, print this JSON:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "updatedToolOutput": {
      "code": "(await $`cat notes.txt`.text())",
      "result": "deploy token: REDACTED",
      "stdout": "",
      "stderr": "",
      "toolsUsed": ["Bash"]
    }
  }
}
```

To test the hook, create a file that contains a value your hook redacts. Then start a Code Mode session, and ask Claude to read and quote the file. Type the path without `@`, and check that Claude's reply shows your replacement text.

> [!WARNING]
>
> Don't rely on this hook to hide a value in a refused tool call's input, such as a Bash command. The `refusedCalls` field can repeat that input, and Claude reads it unchanged.

#### Redact when your hook blocks or hits an error

Return a changed copy of `tool_response` as `updatedToolOutput` even when your hook blocks or hits an error:

* **Your hook blocks**: print the [redacted copy](#redact-code-output) in the same JSON as [`"decision": "block"`](https://code.claude.com/docs/en/hooks#posttooluse-decision-control). Without the copy, Claude still reads the original output
* **Your hook hits an error**: catch the error, and print a copy with placeholder text in the fields that you redact. If the hook crashes, times out, or prints invalid JSON, Claude gets the original output

#### Move a check from a `UserPromptSubmit` hook

If you check code output in a [`UserPromptSubmit` hook](https://code.claude.com/docs/en/hooks#userpromptsubmit), move that check to your `PostToolUse` hook. On v2.1.328 or later, `UserPromptSubmit` hooks don't receive code output, even when an administrator sets them in [managed settings](https://code.claude.com/docs/en/managed-settings.md).

## Troubleshooting

### Code Mode doesn't start

`Code Mode (experimental) isn't available` near the top of the session means that Claude Code started without Code Mode. The reason follows on the same line, and `/status` shows it too. Find the reason in this table, make the change, and start a new session. For a reason that isn't listed, check the [requirements](#requirements).

| Reason includes | What to do |
| :- | :- |
| `it isn't open to your account in this version` or `it isn't open to your account yet` | If your version is older than v2.1.323, [update](#try-code-mode). Otherwise, check your network connection and start again. If the reason stays, try again another day |
| `Anthropic has turned it off for now` | [Update Claude Code](https://code.claude.com/docs/en/setup.md#update-claude-code), or start again later |
| `it only works directly with the Anthropic API` or `it only works with the Anthropic API` | If you use a cloud provider without a gateway, [update Claude Code](https://code.claude.com/docs/en/setup.md#update-claude-code) to v2.1.331 or later. If you use a gateway, follow the next row |
| `it isn't offered yet through a gateway or proxy` | If your administrator set up the [gateway](https://code.claude.com/docs/en/gateways.md), you need it, or you use Claude for Government, [turn off Code Mode](#turn-off-code-mode) to stop seeing the line. Otherwise, remove [the gateway's settings](https://code.claude.com/docs/en/llm-gateway-connect.md) and key, and connect directly. You can keep `HTTPS_PROXY`. If you signed in to a Claude apps gateway, also remove [its entries from your user settings](https://code.claude.com/docs/en/claude-apps-gateway#set-the-gateway-url-in-user-settings) and run `/logout`, which removes saved MCP server logins and plugin secrets too |
| `it isn't offered yet through a gateway or proxy`, with an [Enterprise Admin Console sign-in](https://code.claude.com/docs/en/authentication.md#log-in-to-claude-code) | Run `/status`. If `API provider` shows a provider that the [requirements](#requirements) rule out, such as `Microsoft Foundry` or `Amazon Bedrock (Mantle)`, [turn off Code Mode](#turn-off-code-mode) to stop seeing the line. Otherwise, follow the previous row |
| `it doesn't work with an API key helper` | Remove `apiKeyHelper`, `ANTHROPIC_AUTH_TOKEN`, and any `Authorization` or `X-Api-Key` header in `ANTHROPIC_CUSTOM_HEADERS`. Then sign in or set `ANTHROPIC_API_KEY` |
| `it only works with Opus 5.5, Sonnet 5.5 and later models` | Pass the full name of a [supported model](#requirements) that your account can use, for example `--model claude-opus-5-5`, or on Microsoft Foundry the name of your deployment of one. Avoid aliases such as `sonnet`, which [select older models on some providers](https://code.claude.com/docs/en/model-config.md#model-aliases) |
| `it doesn't work in background jobs` | Start in the foreground, without `--remote-control`. If the reason shows in a teammate's split pane, use the [in-process display mode](https://code.claude.com/docs/en/agent-teams.md#choose-a-display-mode) to run teammates in Code Mode |
| `it needs settings that Claude Code downloads from Anthropic` | [Update Claude Code](https://code.claude.com/docs/en/setup.md#update-claude-code) to meet the [telemetry settings requirement](#requirements). To stay on your version, unset the variable that [turns off feature-flag fetching](https://code.claude.com/docs/en/env-vars.md#features-that-need-feature-flag-fetching), such as `DISABLE_TELEMETRY` |
| `OpenTelemetry tracing is on` | Unset `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA`, `ENABLE_ENHANCED_TELEMETRY_BETA`, and `ENABLE_BETA_TRACING_DETAILED` if you can work without [traces](https://code.claude.com/docs/en/monitoring-usage.md#traces-beta) |
| `OpenTelemetry is on` | To keep events and metrics on, [update Claude Code](https://code.claude.com/docs/en/setup.md#update-claude-code) and meet the [telemetry settings requirement](#requirements). To stay on your version, unset `CLAUDE_CODE_ENABLE_TELEMETRY` and `ENABLE_BETA_TRACING_DETAILED` if you can work without [OpenTelemetry export](https://code.claude.com/docs/en/monitoring-usage.md) |
| `it doesn't yet work with the plugin` | [Update Claude Code](https://code.claude.com/docs/en/setup.md#update-claude-code) to meet the [mods requirement](#requirements). To stay on your version, run `/plugin` and disable each plugin that the reason names. If your organization turned one on, ask your administrator to turn it off |
| `it doesn't yet work with an installed mod` | [Update Claude Code](https://code.claude.com/docs/en/setup.md#update-claude-code) to meet the [mods requirement](#requirements). To stay on your version, run `/plugin` and disable each mod you installed |
| `it can't be used together with agent teams yet` | To keep agent teams on, [update Claude Code](https://code.claude.com/docs/en/setup.md#update-claude-code) to v2.1.326 or later. To stay on your version, unset `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` |
| `this launch's tool options` | Start without `--restricted`, add `REPL` to `--tools`, and remove `REPL` from `--disallowedTools` and your `deny` rules |
| `couldn't read your organization's settings or policy` | Start again. If your Enterprise Admin Console sign-in ended, run `claude auth login` and select your organization. If the reason stays and your network blocks `api.anthropic.com`, ask your administrator to allow that host. If you use a cloud provider and not that sign-in, you can instead unset `ANTHROPIC_API_KEY` and run `claude auth logout`, which also removes saved MCP server logins and plugin secrets |
| `couldn't save your answer` | Make `~/.claude.json` writable |
| `your organization's settings don't allow it` | Ask your administrator about the [managed setting](#block-code-mode-for-your-organization) |

If you see no line about Code Mode, run `claude --version`. If your version is older than v2.1.323, update. Then check that `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` is `1` in your shell or user settings, and remove any `0` from those and from any `--settings` file.

### Permission prompt with a countdown

In auto mode, if you approve code yourself after [repeated classifier blocks](https://code.claude.com/docs/en/permission-modes.md#when-auto-mode-falls-back), you can be asked about tool calls in that code and in earlier code that's still running. Expect the same in auto mode after an [`ask` rule](#approve-each-piece-of-code-first) or a `PreToolUse` hook on `REPL` has you approve the code.

With no IDE connected, the prompt can show a countdown:

```text theme={null}
Claude Code will automatically block this request in 1:59, to avoid holding up an unattended session
```

Answer before the countdown ends. Otherwise that call is refused, and later calls that would show a countdown are refused without a prompt. To see the prompts again, send Claude a message.

Before v2.1.327, you could also be asked about the remaining calls in running code after Claude started new code, even if the classifier allowed the new code. To see fewer of these prompts, [update Claude Code](https://code.claude.com/docs/en/setup.md#update-claude-code) to v2.1.327 or later.

### Tool call refused by a hook

If Claude reports a refused call, ask it for the error text. These errors mean your [`PreToolUse` hook](https://code.claude.com/docs/en/hooks#pretooluse) gave no decision:

* **`the hook did not finish`**: your hook timed out, or your agent hook ended without a decision. Raise the hook's [`timeout`](https://code.claude.com/docs/en/hooks#common-fields), or set [`"onFailure": "continue"`](#tool-call-ran-after-a-hook-failed) on a `command` or `http` hook. If an agent hook still gives this error, move the check to a `command` hook. After Claude runs code, you can see this error on calls outside code too
* **`the hook failed`**: your hook failed on a call from code, for example because it couldn't start. Find the failure in the [debug log](https://code.claude.com/docs/en/hooks.md#debug-hooks) and fix it. Expect this error before v2.1.329. On later versions, you can see it after you turn off [feature-flag fetching](https://code.claude.com/docs/en/env-vars.md#features-that-need-feature-flag-fetching) during a session

### Tool call ran after a hook failed

To stop a call from code when its `PreToolUse` hook fails, use a `command` or `http` hook and set [`"onFailure": "block"`](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails). If several settings files have that hook, give it the same `onFailure` value in each.

On v2.1.329 or later, expect these results for `command` and `http` hooks:

| `onFailure` | Hook times out | Hook fails another way, such as a missing script |
| :- | :- | :- |
| Not set | Refused | Goes on to permission checks, [with rare exceptions](#tool-call-refused-by-a-hook) |
| `"block"` | Refused | Refused |
| `"continue"` | Goes on to permission checks | Goes on to permission checks |

### Code output withheld by a hook

If you expected output from code and see `UserPromptSubmit operation blocked by hook` in Claude's reply, your [`UserPromptSubmit`](https://code.claude.com/docs/en/hooks#userpromptsubmit) hook received the output as a prompt and blocked it. If Claude reports only the hook's reason, ask it to quote the message it received.

On v2.1.328 or later, `UserPromptSubmit` hooks don't receive code output. To let the output through on an earlier version, update Claude Code or change the hook:

* **Update**: if you rely on the hook to check code output, first [move the check to a `PostToolUse` hook](#check-code-output-with-a-hook). Then [update Claude Code](https://code.claude.com/docs/en/setup.md#update-claude-code) to v2.1.328 or later
* **Stay on your version**: change the hook so that it doesn't block when `source` in its input is `poll_event`

## Related resources

* [Permission modes](https://code.claude.com/docs/en/permission-modes.md): compare auto mode with the modes that prompt you
* [Hooks reference](https://code.claude.com/docs/en/hooks.md): write `PreToolUse` and `PostToolUse` hooks
* [Managed settings](https://code.claude.com/docs/en/managed-settings.md): apply one configuration across an organization
