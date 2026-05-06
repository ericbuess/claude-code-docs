> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Error reference

> Look up Claude Code runtime error messages with what each one means and how to fix it.

This page lists runtime errors Claude Code displays and how to recover from each one, plus what to check when responses seem off without an error. For installation errors such as `command not found` or TLS failures during setup, see [Troubleshoot installation and login](/en/troubleshoot-install).

These errors and recovery commands apply across the CLI, the [Desktop app](/en/desktop), and [Claude Code on the web](/en/claude-code-on-the-web), since all three wrap the same Claude Code CLI. For surface-specific issues, see the troubleshooting section on that surface's page.

<Note>
  Claude Code calls the Claude API for model responses, so most runtime errors map to an underlying API error code. This page covers what each error means inside Claude Code and how to recover. For the raw HTTP status code definitions, see the [Claude Platform error reference](https://platform.claude.com/docs/en/api/errors).
</Note>

## Find your error

Match the message you see in your terminal to a section below.

| Message                                                                              | Section                                                                                                                       |
| :----------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| `API Error: 500 ... Internal server error`                                           | [Server errors](#api-error-500-internal-server-error)                                                                         |
| `API Error: Repeated 529 Overloaded errors`                                          | [Server errors](#api-error-repeated-529-overloaded-errors)                                                                    |
| `Request timed out`                                                                  | [Server errors](#request-timed-out), or [Network](#unable-to-connect-to-api) if the message mentions your internet connection |
| `<model> is temporarily unavailable, so auto mode cannot determine the safety of...` | [Server errors](#auto-mode-cannot-determine-the-safety-of-an-action)                                                          |
| `You've hit your session limit` / `You've hit your weekly limit`                     | [Usage limits](#youve-hit-your-session-limit)                                                                                 |
| `Server is temporarily limiting requests`                                            | [Usage limits](#server-is-temporarily-limiting-requests)                                                                      |
| `Request rejected (429)`                                                             | [Usage limits](#request-rejected-429)                                                                                         |
| `Credit balance is too low`                                                          | [Usage limits](#credit-balance-is-too-low)                                                                                    |
| `Not logged in · Please run /login`                                                  | [Authentication](#not-logged-in)                                                                                              |
| `Invalid API key`                                                                    | [Authentication](#invalid-api-key)                                                                                            |
| `This organization has been disabled`                                                | [Authentication](#this-organization-has-been-disabled)                                                                        |
| `OAuth token revoked` / `OAuth token has expired`                                    | [Authentication](#oauth-token-revoked-or-expired)                                                                             |
| `does not meet scope requirement user:profile`                                       | [Authentication](#oauth-scope-requirement)                                                                                    |
| `Unable to connect to API`                                                           | [Network](#unable-to-connect-to-api)                                                                                          |
| `SSL certificate verification failed`                                                | [Network](#ssl-certificate-errors)                                                                                            |
| `Prompt is too long`                                                                 | [Request errors](#prompt-is-too-long)                                                                                         |
| `Error during compaction: Conversation too long`                                     | [Request errors](#error-during-compaction-conversation-too-long)                                                              |
| `Request too large`                                                                  | [Request errors](#request-too-large)                                                                                          |
| `Image was too large`                                                                | [Request errors](#image-was-too-large)                                                                                        |
| `PDF too large` / `PDF is password protected`                                        | [Request errors](#pdf-errors)                                                                                                 |
| `Extra inputs are not permitted`                                                     | [Request errors](#extra-inputs-are-not-permitted)                                                                             |
| `There's an issue with the selected model`                                           | [Request errors](#theres-an-issue-with-the-selected-model)                                                                    |
| `Claude Opus is not available with the Claude Pro plan`                              | [Request errors](#claude-opus-is-not-available-with-the-claude-pro-plan)                                                      |
| `thinking.type.enabled is not supported for this model`                              | [Request errors](#thinking-type-enabled-is-not-supported-for-this-model)                                                      |
| `max_tokens must be greater than thinking.budget_tokens`                             | [Request errors](#thinking-budget-exceeds-output-limit)                                                                       |
| `API Error: 400 due to tool use concurrency issues`                                  | [Request errors](#tool-use-or-thinking-block-mismatch)                                                                        |
| Responses seem lower quality than usual                                              | [Response quality](#responses-seem-lower-quality-than-usual)                                                                  |

## Automatic retries

Claude Code retries transient failures before showing you an error. Server errors, overloaded responses, request timeouts, temporary 429 throttles, and dropped connections are all retried up to 10 times with exponential backoff. While retrying, the spinner shows a `Retrying in Ns · attempt x/y` countdown.

When you see one of the errors on this page, those retries have already been exhausted. You can tune the behavior with two environment variables:

| Variable                                  | Default | Effect                                                                                                               |
| :---------------------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------- |
| [`CLAUDE_CODE_MAX_RETRIES`](/en/env-vars) | 10      | Number of retry attempts. Lower it to surface failures faster in scripts; raise it to wait through longer incidents. |
| [`API_TIMEOUT_MS`](/en/env-vars)          | 600000  | Per-request timeout in milliseconds. Raise it for slow networks or proxies.                                          |

## Server errors

These errors come from Anthropic infrastructure rather than your account or request.

### API Error: 500 Internal server error

Claude Code shows the raw API response body for any 5xx status. The example below shows a 500 response:

```text theme={null}
API Error: 500 {"type":"error","error":{"type":"api_error","message":"Internal server error"}} · check status.claude.com
```

This indicates an unexpected failure inside the API. It is not caused by your prompt, settings, or account.

**What to do:**

* Check [status.claude.com](https://status.claude.com) for active incidents
* Wait a minute, then send your message again. Your original message is still in the conversation, so for a long prompt you can type `try again` instead of pasting the whole thing.
* If the error persists with no posted incident, run `/feedback` so Anthropic can investigate with your request details. See [Report an error](#report-an-error) if `/feedback` is unavailable on your provider.

### API Error: Repeated 529 Overloaded errors

The API is temporarily at capacity across all users. Claude Code has already retried several times before showing this message:

```text theme={null}
API Error: Repeated 529 Overloaded errors · check status.claude.com
```

A 529 is not your usage limit and does not count against your quota.

**What to do:**

* Check [status.claude.com](https://status.claude.com) for capacity notices
* Try again in a few minutes
* Run `/model` and switch to a different model to keep working, since capacity is tracked per model. Claude Code prompts you to do this when one model is under particularly high load, for example `Opus is experiencing high load, please use /model to switch to Sonnet`.

### Request timed out

The API did not respond before the connection deadline.

```text theme={null}
Request timed out
```

This can happen during periods of high load or when a very large response is being generated. The default request timeout is 10 minutes.

**What to do:**

* Retry the request
* For long-running tasks, break the work into smaller prompts
* If a slow network or proxy is the cause, raise `API_TIMEOUT_MS` as described in [Automatic retries](#automatic-retries)
* If timeouts are frequent and your network is otherwise healthy, see [Network and connection errors](#network-and-connection-errors) below

### Auto mode cannot determine the safety of an action

The model that [auto mode](/en/permission-modes#eliminate-prompts-with-auto-mode) uses to classify actions is overloaded, so auto mode blocked the action instead of approving it unchecked.

```text theme={null}
<model> is temporarily unavailable, so auto mode cannot determine the safety of <tool> right now. Wait briefly and then try this action again.
```

Reads, searches, and edits inside your working directory skip the classifier, so they keep working during the outage.

**What to do:**

* Retry after a few seconds; Claude sees the same message and usually retries on its own
* If retries keep failing, continue with read-only tasks and come back to the blocked action later
* This is transient and unrelated to [auto mode eligibility](/en/permission-modes#eliminate-prompts-with-auto-mode); you do not need to change settings

## Usage limits

These errors mean a quota tied to your account or plan has been reached. They are distinct from [server errors](#server-errors), which affect everyone.

### You've hit your session limit

Subscription plans include a rolling usage allowance. When it runs out you see one of these messages:

```text theme={null}
You've hit your session limit · resets 3:45pm
You've hit your weekly limit · resets Mon 12:00am
You've hit your Opus limit · resets 3:45pm
```

Claude Code blocks further requests until the reset time shown in the message.

**What to do:**

* Wait for the reset time shown in the error
* Run `/usage` to see your plan limits and when they reset
* Run `/extra-usage` to buy additional usage on Pro and Max, or to request it from your admin on Team and Enterprise. See [Extra usage for paid plans](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) for how this is billed.
* To upgrade your plan for higher base limits, see [claude.com/pricing](https://claude.com/pricing)

To watch your remaining allowance before you hit the limit, add the `rate_limits` fields to a [custom status line](/en/statusline#rate-limit-usage), or in the Desktop app click the [usage ring](/en/desktop#check-usage) next to the model picker.

### Server is temporarily limiting requests

The API applied a short-lived throttle that is unrelated to your plan quota.

```text theme={null}
API Error: Server is temporarily limiting requests (not your usage limit)
```

This is [retried automatically](#automatic-retries) before being shown.

**What to do:**

* Wait briefly and try again
* Check [status.claude.com](https://status.claude.com) if it persists

### Request rejected (429)

You have hit the rate limit configured for your API key, Amazon Bedrock project, or Google Vertex AI project.

```text theme={null}
API Error: Request rejected (429) · this may be a temporary capacity issue
```

**What to do:**

* Run `/status` and confirm the active credential is the one you expect. A stray `ANTHROPIC_API_KEY` in your environment can route requests through a low-tier key instead of your subscription.
* Check your provider console for the active limits and request a higher tier if needed
* For Anthropic API keys, see the [rate limits reference](https://platform.claude.com/docs/en/api/rate-limits) for how tiers work and how to set per-workspace caps
* Reduce concurrency: lower [`CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`](/en/env-vars), avoid running many parallel subagents, or switch to a smaller model with `/model` for high-volume scripted runs

### Credit balance is too low

Your Console organization has run out of prepaid credits.

```text theme={null}
Credit balance is too low
```

**What to do:**

* Add credits at [platform.claude.com/settings/billing](https://platform.claude.com/settings/billing), and consider enabling auto-reload there so the balance refills before it hits zero
* Switch to subscription authentication with `/login` if you have a Pro, Max, Team, or Enterprise plan
* Set per-workspace spend caps in the Console to prevent a single project from draining the org balance. See [Manage costs effectively](/en/costs).

## Authentication errors

These errors mean Claude Code cannot prove who you are to the API. Run `/status` at any time to see which credential is currently active.

### Not logged in

No valid credential is available for this session.

```text theme={null}
Not logged in · Please run /login
```

**What to do:**

* Run `/login` to authenticate with your Claude subscription or Console account
* If you expected an environment variable to authenticate you, confirm `ANTHROPIC_API_KEY` is set and exported in the shell where you launched `claude`
* For CI or automation where interactive login is not possible, configure an [`apiKeyHelper`](/en/settings#available-settings) script that fetches a key at startup
* See [Authentication precedence](/en/authentication#authentication-precedence) to understand which credential wins when several are present

If you are prompted to log in repeatedly, see [Not logged in or token expired](/en/troubleshoot-install#not-logged-in-or-token-expired) for system clock and macOS Keychain fixes.

### Invalid API key

The `ANTHROPIC_API_KEY` environment variable or `apiKeyHelper` script returned a key the API rejected.

```text theme={null}
Invalid API key · Fix external API key
```

**What to do:**

* Check for typos and confirm the key has not been revoked in the [Console](https://platform.claude.com/settings/keys)
* Run `env | grep ANTHROPIC` in the same shell. Tools like direnv, dotenv shell plugins, and IDE terminals can load a stale key from a `.env` file in your project without you setting it explicitly.
* Unset `ANTHROPIC_API_KEY` and run `/login` to use subscription auth instead
* If the key comes from an [`apiKeyHelper`](/en/settings#available-settings) script, run the script directly to confirm it prints a valid key on stdout
* Run `/status` to confirm which credential source Claude Code is actually using

### This organization has been disabled

A stale `ANTHROPIC_API_KEY` from a disabled Console organization is overriding your subscription login.

```text theme={null}
Your ANTHROPIC_API_KEY belongs to a disabled organization · Unset the environment variable to use your other credentials
API Error: 400 ... This organization has been disabled.
```

Environment variables take precedence over `/login`, so a key exported in your shell profile or loaded from a `.env` file is used even when you have a working Pro or Max subscription. In non-interactive mode (`-p`), the key is always used when present.

**What to do:**

* Unset `ANTHROPIC_API_KEY` in the current shell and remove it from your shell profile, then relaunch `claude`
* Run `/status` afterward to confirm the active credential is your subscription
* If no environment variable is set and the error persists, the disabled organization is the one tied to your `/login`. Contact support or sign in with a different account.

### OAuth token revoked or expired

Your saved login is no longer valid. A revoked token means you signed out everywhere or an admin removed access; an expired token means the automatic refresh failed mid-session.

```text theme={null}
OAuth token revoked · Please run /login
OAuth token has expired · Please run /login
API Error: 401 ... authentication_error
```

**What to do:**

* Run `/login` to sign in again
* If the error returns within the same session after re-authenticating, run `/logout` first to fully clear the stored token, then `/login`
* For repeated prompts to log in across launches, see the system clock and macOS Keychain checks in [Troubleshooting](/en/troubleshoot-install#not-logged-in-or-token-expired)
* For other failures including `403 Forbidden` and OAuth browser issues, see [Login and authentication](/en/troubleshoot-install#login-and-authentication)

### OAuth scope requirement

The stored token predates a permission scope that a newer feature needs. You see this most often from `/usage` and the status line usage indicator:

```text theme={null}
OAuth token does not meet scope requirement: user:profile
```

**What to do:**

* Run `/login` to mint a new token with the current scopes. You do not need to log out first.

## Network and connection errors

These errors mean Claude Code could not reach the API at all. They almost always originate in your local network, proxy, or firewall rather than Anthropic infrastructure.

### Unable to connect to API

The TCP connection to the API failed or never completed.

```text theme={null}
Unable to connect to API. Check your internet connection
Unable to connect to API (ECONNREFUSED)
Unable to connect to API (ECONNRESET)
Unable to connect to API (ETIMEDOUT)
fetch failed
Request timed out. Check your internet connection and proxy settings
```

Common causes include no internet access, a VPN that blocks `api.anthropic.com`, or a required corporate proxy that is not configured.

**What to do:**

* Confirm you can reach the API host from the same shell by running `curl -I https://api.anthropic.com`. On Windows PowerShell use `curl.exe -I https://api.anthropic.com` so the built-in `Invoke-WebRequest` alias is not used.
* If you are behind a corporate proxy, set `HTTPS_PROXY` before launching Claude Code and see [Network configuration](/en/network-config)
* If you route through an LLM gateway or relay, set [`ANTHROPIC_BASE_URL`](/en/env-vars) to its address. See [LLM gateway configuration](/en/llm-gateway) for setup.
* Ensure your firewall allows the hosts listed in [Network access requirements](/en/network-config#network-access-requirements)
* Intermittent failures are [retried automatically](#automatic-retries); persistent failures point to a local network issue

If `curl` succeeds but Claude Code still fails, the cause is usually something between the runtime and the network rather than the network itself:

* On Linux and WSL, check `/etc/resolv.conf` for an unreachable nameserver. WSL in particular can inherit a broken resolver from the host.
* On macOS, a VPN client that was disconnected or uninstalled can leave a tunnel interface or routing rule behind. Check `ifconfig` for stale `utun` interfaces and remove the VPN's network extension in System Settings.
* Docker Desktop and similar container runtimes can intercept outbound traffic. Quit them and retry to rule this out.

### SSL certificate errors

A proxy or security appliance on your network is intercepting TLS traffic with its own certificate, and Claude Code does not trust it.

```text theme={null}
Unable to connect to API: SSL certificate verification failed. Check your proxy or corporate SSL certificates
Unable to connect to API: Self-signed certificate detected
```

**What to do:**

* Export your organization's CA bundle and point Claude Code at it with `NODE_EXTRA_CA_CERTS=/path/to/ca-bundle.pem`
* See [Network configuration](/en/network-config#custom-ca-certificates) for full setup instructions
* Do not set `NODE_TLS_REJECT_UNAUTHORIZED=0`, which disables certificate validation entirely

## Request errors

These errors mean the API received your request but rejected its content.

### Prompt is too long

The conversation plus attached files exceeds the model's context window.

```text theme={null}
Prompt is too long
```

**What to do:**

* Run `/compact` to summarize earlier turns and free space, or `/clear` to start fresh
* Run `/context` to see a breakdown of what is consuming the window: system prompt, tools, memory files, and messages
* Disable MCP servers you are not using with `/mcp disable <name>` to remove their tool definitions from context
* Trim large `CLAUDE.md` memory files, or move instructions into [path-scoped rules](/en/memory#path-specific-rules) that load only when relevant
* Subagents inherit every MCP tool definition from the parent session, which can fill their context window before the first turn. Disable MCP servers you are not using before spawning subagents.
* Auto-compact is on by default and normally prevents this error. If you have set [`DISABLE_AUTO_COMPACT`](/en/env-vars), re-enable it or run `/compact` manually before the window fills.

See [Explore the context window](/en/context-window) for an interactive view of how context fills up.

### Error during compaction: Conversation too long

`/compact` itself failed because there is not enough free context to hold the summary it produces.

```text theme={null}
Error during compaction: Conversation too long. Press esc twice to go up a few messages and try again.
```

This can happen when the window is already full at the moment auto-compact triggers, or when you run `/compact` after seeing `Prompt is too long`.

**What to do:**

* Press Esc twice to open the message list and step back several turns. This drops the most recent messages from context. Then run `/compact` again.
* If stepping back does not free enough space, run `/clear` to start a fresh session. Your previous conversation is preserved and can be reopened with `/resume`.

### Request too large

The raw request body exceeded the API's byte limit before tokenization, usually because of a large pasted file or attachment.

```text theme={null}
Request too large (max 30 MB). Double press esc to go back and remove or shrink the attached content.
```

This is a size limit on the HTTP request, separate from the [context window limit](#prompt-is-too-long).

**What to do:**

* Press Esc twice and step back past the turn that added the oversized content
* Reference large files by path instead of pasting their contents, so Claude can read them in chunks
* For images, see [Image was too large](#image-was-too-large) below

### Image was too large

A pasted or attached image exceeds the API's size or dimension limits.

```text theme={null}
Image was too large. Double press esc to go back and try again with a smaller image.
API Error: 400 ... image dimensions exceed max allowed size
```

The image stays in conversation history after the error, so every subsequent message fails with the same error until you remove it.

**What to do:**

* Press Esc twice and step back past the turn where the image was added
* Resize the image before pasting. The API accepts images up to 8000 pixels on the longest edge for a single image, or 2000 pixels when many images are in context.
* Take a tighter screenshot of the relevant region instead of the full screen

### PDF errors

The PDF you attached could not be processed.

```text theme={null}
PDF too large (max 100 pages, 32 MB). Try splitting it or extracting text first.
PDF is password protected. Try removing protection or extracting text first.
The PDF file was not valid. Try converting to a different format first.
```

**What to do:**

* For oversized PDFs, ask Claude to read a page range with the Read tool instead of attaching the whole file, or extract text with a tool like `pdftotext` and reference the output file by path
* For protected or invalid PDFs, remove the password or re-export the file from its source application, then try again

### Extra inputs are not permitted

A proxy or LLM gateway between Claude Code and the API stripped the `anthropic-beta` request header, so the API rejected fields that depend on it.

```text theme={null}
API Error: 400 ... Extra inputs are not permitted ... context_management
API Error: 400 ... Extra inputs are not permitted ... tools.0.custom.input_examples
API Error: 400 ... Unexpected value(s) for the `anthropic-beta` header
```

Claude Code sends beta-only fields such as `context_management`, `effort`, and tool `input_examples` alongside an `anthropic-beta` header that enables them. When a gateway forwards the body but drops the header, the API sees fields it does not recognize.

**What to do:**

* Configure your gateway to forward the `anthropic-beta` header. See [LLM gateway configuration](/en/llm-gateway).
* As a fallback, set [`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`](/en/env-vars) before launching. This disables features that require the beta header so requests succeed through a gateway that cannot forward it.

### There's an issue with the selected model

The configured model name was not recognized or your account lacks access to it.

```text theme={null}
There's an issue with the selected model (claude-...). It may not exist or you may not have access to it. Run /model to select a different one.
```

**What to do:**

* Run `/model` to pick from models available to your account
* Use an alias such as `sonnet` or `opus` instead of a full versioned ID. Aliases track the latest release so they do not go stale. See [Model configuration](/en/model-config).
* If the wrong model keeps coming back, a stale ID is set somewhere. Check in [priority order](/en/model-config#setting-your-model): the `--model` flag, the `ANTHROPIC_MODEL` environment variable, then the `model` field in `.claude/settings.local.json`, your project's `.claude/settings.json`, and `~/.claude/settings.json`. Remove the stale value and Claude Code falls back to your account default.
* For Vertex AI deployments, see [Vertex AI troubleshooting](/en/google-vertex-ai#troubleshooting).

### Claude Opus is not available with the Claude Pro plan

Your active subscription plan does not include the model you selected.

```text theme={null}
Claude Opus is not available with the Claude Pro plan · Select a different model in /model
```

**What to do:**

* Run `/model` and select a model your plan includes
* If you upgraded your plan recently and still see this, run `/logout` then `/login`. The stored token reflects your plan at the time you signed in, so upgrading on the web does not take effect in an existing session until you re-authenticate.
* See [claude.com/pricing](https://claude.com/pricing) for which models each plan includes

### thinking.type.enabled is not supported for this model

Your Claude Code version is older than the minimum for Opus 4.7. The CLI sent a thinking configuration the model no longer accepts.

```text theme={null}
API Error: 400 ... "thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

**What to do:**

* Run `claude update` to upgrade to v2.1.111 or later, then restart Claude Code
* If you cannot upgrade, run `/model` and select Opus 4.6 or Sonnet instead
* If you hit this in the Agent SDK, see [SDK troubleshooting](/en/agent-sdk/quickstart#troubleshooting)

### Thinking budget exceeds output limit

The configured extended thinking budget exceeds the maximum response length, so there is no room left for the actual answer.

```text theme={null}
API Error: 400 ... max_tokens must be greater than thinking.budget_tokens
```

Claude Code adjusts these values automatically on the Anthropic API. You typically see this error on Amazon Bedrock or Google Vertex AI when [`MAX_THINKING_TOKENS`](/en/env-vars) is set higher than the provider's output limit, or when plan mode raises the thinking budget.

**What to do:**

* Lower `MAX_THINKING_TOKENS`, or raise [`CLAUDE_CODE_MAX_OUTPUT_TOKENS`](/en/env-vars) above the thinking budget
* See [Extended thinking](/en/model-config#extended-thinking) for how the budget interacts with output length

### Tool use or thinking block mismatch

The conversation history reached the API in an inconsistent state, usually after a tool call was interrupted or a turn was edited mid-stream.

```text theme={null}
API Error: 400 due to tool use concurrency issues. Run /rewind to recover the conversation.
API Error: 400 ... unexpected `tool_use_id` found in `tool_result` blocks
API Error: 400 ... thinking blocks ... cannot be modified
```

All three variants mean the same thing: the sequence of `tool_use`, `tool_result`, and `thinking` blocks in history no longer matches what the API expects.

**What to do:**

* Run `/rewind`, or press Esc twice, to step back to a checkpoint before the corrupted turn and continue from there. See [Checkpointing](/en/checkpointing) for how checkpoints are created and restored.

## Responses seem lower quality than usual

If Claude's answers seem less capable than you expect but no error is shown, the cause is usually conversation state rather than the model itself. Claude Code does not silently change model versions. It can switch to a fallback model in specific cases such as an Opus quota being reached or a Bedrock or Vertex AI region lacking your model; the Model selection check below catches both, and [Model configuration](/en/model-config) explains when fallback applies.

Check these first:

* **Model selection**: run `/model` to confirm you are on the model you expect. A previous `/model` choice or an `ANTHROPIC_MODEL` environment variable may have you on a smaller model than you intended.
* **Effort level**: run `/effort` to check the current reasoning level and raise it for hard debugging or design work. Defaults vary by model, so check before assuming you are below the maximum. See [Adjust effort level](/en/model-config#adjust-effort-level) for per-model defaults and the `ultrathink` shortcut.
* **Context pressure**: run `/context` to see how full the window is. If it is near capacity, run `/compact` at a natural breakpoint or `/clear` to start fresh. See [Explore the context window](/en/context-window) for how auto-compact affects earlier turns.
* **Stale instructions**: large or outdated `CLAUDE.md` files and MCP tool definitions consume context and can steer responses. `/doctor` flags oversized memory files and subagent definitions; `/context` shows MCP tool token usage.

When a response goes wrong, rewinding usually works better than replying with corrections. Press Esc twice or run `/rewind` to step back to before the bad turn, then rephrase the prompt with more specifics. Correcting in-thread keeps the wrong attempt in context, which can anchor later answers to it. See [Checkpointing](/en/checkpointing).

If quality still seems off after checking the above, run `/feedback` and describe what you expected versus what you got. Feedback submitted this way includes the conversation transcript, which is the fastest way for Anthropic to diagnose a real regression. See [Report an error](#report-an-error) if `/feedback` is unavailable on your provider.

## Report an error

This page covers errors from the Claude API. For errors from other Claude Code components, see the relevant guide:

* MCP server failed to connect or authenticate: [MCP](/en/mcp)
* Hook script failed or blocked a tool: [Debug hooks](/en/hooks#debug-hooks)
* Permission denied or filesystem errors during install: [Troubleshoot installation and login](/en/troubleshoot-install)

If an error is not listed here or the suggested fix does not help:

* Run `/feedback` inside Claude Code to send the transcript and a description to Anthropic. The command also offers to open a prefilled GitHub issue. Feedback is unavailable on Bedrock, Vertex AI, and Foundry deployments.
* Run `/doctor` to check for local configuration problems
* Check [status.claude.com](https://status.claude.com) for active incidents
* Search [existing issues](https://github.com/anthropics/claude-code/issues) on GitHub
