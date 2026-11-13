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

* **Resuming**: you can resume a Code Mode session only in the terminal, with Code Mode on
* **Auto mode**: auto mode's classifier [reviews the code, not each tool call](#permission-checks)
* **Long-running code**: unless [code can run in the background](#long-running-code), you wait for it to finish, and it stops after ten minutes
* **Hooks**: you can see [tool calls refused](#tool-call-refused-by-a-hook) when a `PreToolUse` hook can't run or times out, and [code output blocked](#code-output-withheld-by-a-hook) by a `UserPromptSubmit` hook
* **Unavailable features**: you can't use [Remote Control](https://code.claude.com/docs/en/remote-control.md), [Claude in Chrome](https://code.claude.com/docs/en/chrome.md), or [computer use](https://code.claude.com/docs/en/computer-use.md)
* **Moving the session**: you can't move the session to the Desktop app or turn it into a [background session](https://code.claude.com/docs/en/agent-view.md), and `/fork` can't start a background copy

## Requirements

* **Version**: Claude Code v2.1.323 or later, on either [release channel](https://code.claude.com/docs/en/setup.md#configure-release-channel). An older version starts without Code Mode, with or without the reason `it isn't open to your account yet`
* **Account**: a Claude subscription or Console account. You can't use Code Mode through a gateway, Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, or Microsoft Foundry
* **Organization**: your organization doesn't use the [HIPAA configuration](https://code.claude.com/docs/en/hipaa-setup.md) or [zero data retention](https://code.claude.com/docs/en/zero-data-retention.md)
* **Model**: Claude Opus 5.5, Sonnet 5.5, Haiku 5.5, or Fable 5.2
* **Surface**: an interactive `claude` session in a terminal. Code Mode doesn't work with `-p`, the Agent SDK, the VS Code panel, the Desktop app, or cloud sessions
* **Installation**: the [native build](https://code.claude.com/docs/en/setup.md) of Claude Code
* **Windows**: [Git for Windows](https://git-scm.com/downloads/win) is installed

You also can't start Code Mode with some settings on, such as an API key helper, agent teams, OpenTelemetry export, or `DISABLE_TELEMETRY`. For the fix for each, see [Code Mode doesn't start](#code-mode-doesnt-start).

## Try Code Mode

Turn on Code Mode, give Claude a task, and look at the code that Claude wrote.

**1. Check your version**

Run `claude --version`. If the version is older than v2.1.323, run `claude update`. If you're on the `stable` channel and the update doesn't reach v2.1.323, wait for `stable` to catch up or [switch to `latest`](https://code.claude.com/docs/en/setup#configure-release-channel).

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

### Turn off Code Mode

Remove `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` from your shell and from `~/.claude/settings.json`, then start a new session. You can also keep the variable and change its value to `0` in either place. With a `0` in one place, Code Mode stays off even if you set `1` in the other.

### Block Code Mode for your organization

Add `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` with the value `0` to your [managed settings](https://code.claude.com/docs/en/managed-settings.md) so that nobody in your organization can use Code Mode:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_CODE_MODE": "0"
  }
}
```

Users who are in a Code Mode session stay in it until they exit or restart Claude Code. After that, your users start without Code Mode and can't resume their Code Mode sessions while the `0` is in place. You can't turn on Code Mode for your users from managed settings.

## Permissions and long-running code

Your permission mode decides how Claude's code is checked and whether you can talk to Claude while the code runs.

### Permission checks

Each tool call that Claude's code makes goes through your `deny` and `ask` [permission rules](https://code.claude.com/docs/en/permissions.md) and your [`PreToolUse` hooks](https://code.claude.com/docs/en/hooks#pretooluse). You don't need to change a rule or matcher for a tool such as `Bash`. Beyond rules and hooks, a classifier reviews the code in auto mode, and you answer prompts in the modes that ask:

* **[Auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode)**: the classifier reviews each piece of code before it runs, not each tool call. It doesn't see values computed at run time, such as a path taken from search output, so keep rules or hooks for calls you must control. You can still be [prompted when new code starts while earlier code runs](#permission-prompt-with-a-countdown)
* **Other [permission modes](https://code.claude.com/docs/en/permission-modes.md)**: the code starts without a review, and you're prompted for each tool call that would prompt you in that mode

To check the code itself, write a `PreToolUse` hook that matches `REPL`, the tool that runs Claude's code, and read the JavaScript from `tool_input.code`.

> [!WARNING]
>
> Bash rules match command text, so Claude can run a denied command [in a form the rule doesn't match](https://code.claude.com/docs/en/permissions.md#bash-rule-limits), with or without Code Mode. For limits that don't depend on command text, see [sandboxing](https://code.claude.com/docs/en/sandboxing.md).

### Long-running code

While code runs a long build or test, Claude either waits for it or lets it continue in the background:

* **Waiting**: Claude answers after the code finishes, and the code stops after ten minutes, including time you spend at permission prompts
* **Background**: you can keep talking to Claude, and the code can run for up to two hours

For background code, start your session in auto or `bypassPermissions` mode. If Claude still waits, check your current mode and how you started the session:

* **You switched to another mode**: press `Shift+Tab` until you're back in the mode you started in
* **You started in another mode, or picked the session from the `claude --resume` list**: if [auto mode is available](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode) to you, exit, then run `claude --continue --permission-mode auto` with Code Mode on
* **You passed tool names to `--tools`**: start again in auto mode without that flag

## Troubleshooting

### Code Mode doesn't start

`Code Mode (experimental) isn't available` near the top of the session means that Claude Code started without Code Mode. The reason follows on the same line, and `/status` shows it too. Find the reason in this table, make the change, and start a new session. For a reason that isn't listed, check the [requirements](#requirements).

| Reason includes | What to do |
| :- | :- |
| `it isn't open to your account yet` | If your version is older than v2.1.323, [update](#try-code-mode). Otherwise, check your network connection and start again. If the reason stays, try again another day |
| `it only works with the Anthropic API` | Remove the settings that route requests through a cloud provider, a gateway, or a custom `ANTHROPIC_BASE_URL` |
| `it doesn't work with an API key helper` | Remove `apiKeyHelper`, `ANTHROPIC_AUTH_TOKEN`, and any `Authorization` or `X-Api-Key` header in `ANTHROPIC_CUSTOM_HEADERS`. Then sign in or set `ANTHROPIC_API_KEY` |
| `it only works with Opus 5.5, Sonnet 5.5 and later models` | Start with a [supported model](#requirements), for example with `--model opus`. Haiku 5.5 and Fable 5.2 also work |
| `it doesn't work in background jobs` | Start in the foreground, without `--remote-control` |
| `it needs settings that Claude Code downloads from Anthropic` | Unset the variable that [turns off feature-flag fetching](https://code.claude.com/docs/en/env-vars.md#features-that-need-feature-flag-fetching), such as `DISABLE_TELEMETRY` |
| `OpenTelemetry is on` | Unset `CLAUDE_CODE_ENABLE_TELEMETRY` and `ENABLE_BETA_TRACING_DETAILED` if you can work without [OpenTelemetry export](https://code.claude.com/docs/en/monitoring-usage.md) |
| `it doesn't yet work with an installed mod` | Turn off the [mod](https://code.claude.com/docs/en/plugins/mods/overview.md) that checks tool calls |
| `it can't be used together with agent teams yet` | Unset `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` |
| `this launch's tool options` | Start without `--restricted`, add `REPL` to `--tools`, and remove `REPL` from `--disallowedTools` and your `deny` rules |
| `couldn't save your answer` | Make `~/.claude.json` writable |
| `your organization's settings don't allow it` | Ask your administrator about the [managed setting](#block-code-mode-for-your-organization) |

If you see no line about Code Mode, run `claude --version`. If your version is older than v2.1.323, update. Then check that `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` is `1` in your shell or user settings, and remove any `0` from those and from any `--settings` file.

### Permission prompt with a countdown

When Claude starts more code in auto mode while earlier code is still running, the earlier code loses its classifier review. Claude Code then asks you about the earlier code's remaining calls that would need a review. With no IDE connected, the prompt shows a countdown:

```text theme={null}
Claude Code will automatically block this request in 1:59, to avoid holding up an unattended session
```

Answer before the countdown ends. Otherwise that call is refused, and later calls that would show a countdown are refused without a prompt. To see the prompts again, send Claude a message.

### Tool call refused by a hook

If Claude reports a refused tool call, ask it for the error text. These errors mean that a `PreToolUse` hook didn't give a decision, which refuses the call even when [`onFailure`](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails) is unset:

* **`the hook failed`**: on a call from Claude's code, your hook couldn't start, was killed, exited with 126, 127, or a code above 128, or returned an HTTP error or invalid output. Fix the hook
* **`the hook did not finish`**: your hook timed out on a call from Claude's code, or on any other tool call once Claude has run code in the session. Raise the hook's [`timeout`](https://code.claude.com/docs/en/hooks#common-fields)

To let calls go ahead when a `command` or `http` hook fails or times out, set `"onFailure": "continue"` on it. If a `command` hook exits with an ordinary code such as 1, the call goes ahead unless you set `"onFailure": "block"`.

### Code output withheld by a hook

If Claude reports a hook's block reason where you expected output from Claude's code, check your [`UserPromptSubmit`](https://code.claude.com/docs/en/hooks#userpromptsubmit) hooks. When [code can run in the background](#long-running-code), `command`, `http`, and `mcp_tool` hooks on that event also run on code output. To let the output through, change the hook so that it doesn't block when `source` in its input is `poll_event`.

## Related resources

* [Permission modes](https://code.claude.com/docs/en/permission-modes.md): compare auto mode with the modes that prompt you
* [Hooks reference](https://code.claude.com/docs/en/hooks.md): write `PreToolUse` and `UserPromptSubmit` hooks
* [Managed settings](https://code.claude.com/docs/en/managed-settings.md): apply one configuration across an organization
