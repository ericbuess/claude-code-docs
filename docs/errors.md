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

| Message                                                                                       | Section                                                                                                                       |
| :-------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| `API Error: 500 Internal server error`                                                        | [Server errors](#api-error-500-internal-server-error)                                                                         |
| `API Error: Repeated 529 Overloaded errors`                                                   | [Server errors](#api-error-repeated-529-overloaded-errors)                                                                    |
| `Request timed out`                                                                           | [Server errors](#request-timed-out), or [Network](#unable-to-connect-to-api) if the message mentions your internet connection |
| `Server error mid-response. The response above may be incomplete.`                            | [Server errors](#the-response-above-may-be-incomplete)                                                                        |
| `Connection closed mid-response` / `Response stalled mid-stream`                              | [Server errors](#the-response-above-may-be-incomplete)                                                                        |
| `<model> is temporarily unavailable, so auto mode cannot determine the safety of...`          | [Server errors](#auto-mode-cannot-determine-the-safety-of-an-action)                                                          |
| `Auto mode could not evaluate this action and is blocking it for safety`                      | [Server errors](#auto-mode-cannot-determine-the-safety-of-an-action)                                                          |
| `Auto mode classifier transcript exceeded context window`                                     | [Server errors](#auto-mode-cannot-determine-the-safety-of-an-action)                                                          |
| `Agent terminated early due to an API error`                                                  | [Server errors](#agent-terminated-early-due-to-an-api-error)                                                                  |
| `You've hit your session limit` / `You've hit your weekly limit`                              | [Usage limits](#you%E2%80%99ve-hit-your-session-limit)                                                                        |
| `Usage credits required for 1M context`                                                       | [Usage limits](#usage-credits-required-for-1m-context)                                                                        |
| `Server is temporarily limiting requests`                                                     | [Usage limits](#server-is-temporarily-limiting-requests)                                                                      |
| `Request rejected (429)`                                                                      | [Usage limits](#request-rejected-429)                                                                                         |
| `Credit balance is too low`                                                                   | [Usage limits](#credit-balance-is-too-low)                                                                                    |
| `Not logged in · Please run /login`                                                           | [Authentication](#not-logged-in)                                                                                              |
| `Could not resolve authentication method`                                                     | [Authentication](#could-not-resolve-authentication-method)                                                                    |
| `Invalid API key`                                                                             | [Authentication](#invalid-api-key)                                                                                            |
| `This organization has been disabled`                                                         | [Authentication](#this-organization-has-been-disabled)                                                                        |
| `Your organization has disabled API key authentication`                                       | [Authentication](#your-organization-has-disabled-api-key-authentication)                                                      |
| `Your organization has disabled Claude subscription access`                                   | [Authentication](#your-organization-has-disabled-claude-subscription-access)                                                  |
| `Routines are disabled by your organization's policy`                                         | [Authentication](#routines-are-disabled-by-your-organization%E2%80%99s-policy)                                                |
| `Remote Control is only available when using Claude via api.anthropic.com`                    | [Authentication](#remote-control-requires-the-anthropic-api)                                                                  |
| `OAuth token revoked` / `OAuth token has expired`                                             | [Authentication](#oauth-token-revoked-or-expired)                                                                             |
| `does not meet scope requirement user:profile`                                                | [Authentication](#oauth-scope-requirement)                                                                                    |
| `AWS credentials expired or invalid`                                                          | [Authentication](#aws-credentials-expired-or-invalid)                                                                         |
| `AWS authentication failed`                                                                   | [Authentication](#aws-authentication-failed)                                                                                  |
| `Unable to connect to API`                                                                    | [Network](#unable-to-connect-to-api)                                                                                          |
| `Waiting for API response · will retry in`                                                    | [Automatic retries](#automatic-retries), or [Network](#unable-to-connect-to-api) if it persists                               |
| `SSL certificate verification failed`                                                         | [Network](#ssl-certificate-errors)                                                                                            |
| `SSL certificate error (...)` during login or startup                                         | [Network](#ssl-certificate-errors)                                                                                            |
| `403` with `x-deny-reason: host_not_allowed` in a cloud or routine session                    | [Network](#host-not-allowed-in-a-cloud-session)                                                                               |
| `Couldn't reconnect to your Remote Control session`                                           | [Network](#couldn%E2%80%99t-reconnect-to-your-remote-control-session)                                                         |
| `Prompt is too long`                                                                          | [Request errors](#prompt-is-too-long)                                                                                         |
| `Error during compaction: Conversation too long`                                              | [Request errors](#error-during-compaction-conversation-too-long)                                                              |
| `Request too large`                                                                           | [Request errors](#request-too-large)                                                                                          |
| `Image was too large`                                                                         | [Request errors](#image-was-too-large)                                                                                        |
| `Unable to resize image`                                                                      | [Request errors](#unable-to-resize-image)                                                                                     |
| `PDF too large` / `PDF is password protected`                                                 | [Request errors](#pdf-errors)                                                                                                 |
| `Extra inputs are not permitted`                                                              | [Request errors](#extra-inputs-are-not-permitted)                                                                             |
| `There's an issue with the selected model`                                                    | [Request errors](#there%E2%80%99s-an-issue-with-the-selected-model)                                                           |
| `Model ... is not a recognized model id`                                                      | [Request errors](#model-is-not-a-recognized-model-id)                                                                         |
| `Claude Opus is not available with the Claude Pro plan`                                       | [Request errors](#claude-opus-is-not-available-with-the-claude-pro-plan)                                                      |
| `Model ... is restricted by your organization's settings`                                     | [Request errors](#model-is-restricted-by-your-organization%E2%80%99s-settings)                                                |
| `thinking.type.enabled is not supported for this model`                                       | [Request errors](#thinking-type-enabled-is-not-supported-for-this-model)                                                      |
| `max_tokens must be greater than thinking.budget_tokens`                                      | [Request errors](#thinking-budget-exceeds-output-limit)                                                                       |
| `API Error: 400 due to tool use concurrency issues`                                           | [Request errors](#tool-use-or-thinking-block-mismatch)                                                                        |
| `Claude Code is unable to respond to this request, which appears to violate our Usage Policy` | [Request errors](#usage-policy-refusal)                                                                                       |
| `<model> has safety measures that flagged this message for a cybersecurity topic`             | [Request errors](#safety-measures-flagged-a-cybersecurity-topic)                                                              |
| `Installation was killed before it could finish (exit code 137)`                              | [Installation errors](#installation-was-killed-before-it-could-finish)                                                        |
| `The connection dropped while downloading the update`                                         | [Installation errors](#the-connection-dropped-while-downloading-the-update)                                                   |
| `--bg and --print conflict`                                                                   | [Command-line errors](#command-line-errors)                                                                                   |
| `Ignoring N permissions.allow entries from ... this workspace has not been trusted`           | [Configuration warnings](#workspace-has-not-been-trusted)                                                                     |
| Responses seem lower quality than usual                                                       | [Response quality](#responses-seem-lower-quality-than-usual)                                                                  |

## Automatic retries

Claude Code retries transient failures before showing you an error. Server errors, overloaded responses, request timeouts, temporary 429 throttles, and dropped connections are all retried up to 10 times with exponential backoff. {/* min-version: 2.1.198 */}As of v2.1.198, this covers connections that drop in the middle of a response before any visible output has streamed: Claude Code re-issues the request with the same backoff and the turn continues instead of stopping with a connection error. {/* min-version: 2.1.199 */}As of v2.1.199, temporary 429 throttles that don't carry your plan's quota headers are also retried when you're signed in with a claude.ai subscription; earlier versions retried them only for API key and Enterprise sign-ins.

Two failure classes aren't retried, because a retry can't succeed:

* {/* min-version: 2.1.199 */}As of v2.1.199, a TLS certificate validation failure, such as a TLS-inspecting proxy, a missing `NODE_EXTRA_CA_CERTS` bundle, or an expired certificate, fails on the first attempt so the fix appears immediately instead of after the full retry budget. See [SSL certificate errors](#ssl-certificate-errors). Transient TLS conditions such as a handshake timeout still retry.
* {/* min-version: 2.1.199 */}As of v2.1.199, a server error that arrives after Claude has already streamed visible output keeps the partial response and appends an [incomplete-response notice](#the-response-above-may-be-incomplete) instead of retrying, since re-running the request could execute the same tools twice. Earlier versions discarded the partial output and reported the turn as an error.

While retrying, the spinner shows a `Retrying in Ns · attempt x/y` countdown after an error label. The label names the specific reason from the first attempt for failures you can act on right away: the network is down, a TLS handshake failed, or you hit a rate limit. For other errors it reads `API error` at first. {/* min-version: 2.1.198 */}As of v2.1.198 it switches to the specific reason from the third attempt, or on the final attempt when `CLAUDE_CODE_MAX_RETRIES` allows fewer than three; earlier versions switch only on the final attempt.

{/* min-version: 2.1.198 */}As of v2.1.198, the usual spinner tip is suppressed during retries. Once the error reason is revealed, if the failure is a 529 overload the line below the countdown also names where to check service status: `status.claude.com` on the Anthropic API, or the provider or gateway host named in the message on other configurations.

{/* min-version: 2.1.185 */}If no data arrives on the response stream for 20 seconds while a request is still pending, the spinner shows `Waiting for API response · will retry in … · check your network` before any retry has started. The request has not failed yet: the countdown runs to the point where Claude Code aborts the stalled connection and retries, so the banner clears on its own once data resumes or the retry succeeds. As of v2.1.185 the threshold is 20 seconds; earlier versions show the banner after 10 seconds with different wording. If it reappears on every attempt, treat it as a [network issue](#unable-to-connect-to-api).

When you see one of the errors on this page, those retries have already been exhausted, unless it belongs to a class that isn't retried, such as a certificate-validation failure. You can tune the behavior with these environment variables:

| Variable                                     | Default | Effect                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :------------------------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`CLAUDE_CODE_MAX_RETRIES`](/en/env-vars)    | 10      | Number of retry attempts. {/* min-version: 2.1.186 */}Capped at 15 as of v2.1.186; {/* min-version: 2.1.199 */}as of v2.1.199 `CLAUDE_CODE_RETRY_WATCHDOG` raises the default and removes the cap. Lower it to surface failures faster in scripts.                                                                                                                                                                                                                               |
| [`CLAUDE_CODE_RETRY_WATCHDOG`](/en/env-vars) | unset   | Set to `1` in unattended sessions such as CI jobs to retry `429` and `529` capacity errors indefinitely instead of failing after `CLAUDE_CODE_MAX_RETRIES` attempts. {/* min-version: 2.1.199 */}As of v2.1.199 it also raises the default retry count for other transient errors, such as server errors, timeouts, and dropped connections, to 300, roughly three hours of backoff, and removes the cap of 15 on `CLAUDE_CODE_MAX_RETRIES` if you set that variable explicitly. |
| [`API_TIMEOUT_MS`](/en/env-vars)             | 600000  | Per-request timeout in milliseconds. Raise it for slow networks or proxies.                                                                                                                                                                                                                                                                                                                                                                                                      |

## Server errors

These errors come from the inference provider rather than your account or request. On the Anthropic API that means Anthropic infrastructure. On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or a custom gateway it means that provider's infrastructure.

### API Error: 500 Internal server error

Claude Code shows the status code and the API's error message for any 5xx response. The example below shows a 500 response on the Anthropic API:

```text theme={null}
API Error: 500 Internal server error. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.
```

The trailing sentence names where to check service health and varies by provider. Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry configurations name that provider's service status. A custom `ANTHROPIC_BASE_URL` names the gateway host.

This indicates an unexpected failure inside the API. It is not caused by your prompt, settings, or account.

**What to do:**

* Check [status.claude.com](https://status.claude.com), or the provider status page named in the message, for active incidents
* Wait a minute, then send your message again. Your original message is still in the conversation, so for a long prompt you can type `try again` instead of pasting the whole thing.
* If the error persists with no posted incident, run `/feedback` so Anthropic can investigate with your request details. See [Report an error](#report-an-error) if `/feedback` is unavailable in your environment.

### API Error: Repeated 529 Overloaded errors

The API is temporarily at capacity across all users. Claude Code has already retried several times before showing this message:

```text theme={null}
API Error: Repeated 529 Overloaded errors. The API is at capacity — this is usually temporary. Try again in a moment. If it persists, check https://status.claude.com.
```

The trailing sentence varies by provider in the same way as the 500 error above.

A 529 is not your usage limit and doesn't count against your quota.

**What to do:**

* Check [status.claude.com](https://status.claude.com), or the provider status page named in the message, for capacity notices
* Try again in a few minutes
* Run `/model` and switch to a different model to keep working, since capacity is tracked per model. Claude Code prompts you to do this when one model is under particularly high load, for example `Opus is experiencing high load, please use /model to switch to Sonnet`.

### Request timed out

The API didn't respond before the connection deadline.

```text theme={null}
Request timed out
```

This can happen during periods of high load or when the model is generating a very large response. The default request timeout is 10 minutes.

**What to do:**

* Retry the request
* For long-running tasks, break the work into smaller prompts
* If a slow network or proxy is the cause, raise `API_TIMEOUT_MS` as described in [Automatic retries](#automatic-retries)
* If timeouts are frequent and your network is otherwise healthy, see [Network and connection errors](#network-and-connection-errors) below

### The response above may be incomplete

A streaming response failed after Claude had already produced visible output. Re-sending the request could run the same tool calls twice, so Claude Code keeps what already streamed and appends this notice instead of discarding the turn. Which variant you see names the cause:

```text theme={null}
API Error: Server error mid-response. The response above may be incomplete.
API Error: Connection closed mid-response. The response above may be incomplete.
API Error: Response stalled mid-stream. The response above may be incomplete.
```

* {/* min-version: 2.1.199 */}`Server error mid-response`: a mid-stream overloaded or 5xx server error. This variant requires Claude Code v2.1.199 or later; before then that case discarded the partial output and reported the whole turn as an error.
* `Connection closed mid-response`: the connection dropped.
* `Response stalled mid-stream`: the stream stopped sending data.

**What to do:**

* Read the response that streamed. Nothing has been lost, but the final sentences or tool calls may be missing.
* Reply with `continue` to have Claude pick up where it stopped
* If the same error appears before any visible output, Claude Code retries the request instead of finalizing it. See [Automatic retries](#automatic-retries).

### Auto mode cannot determine the safety of an action

The model that [auto mode](/en/permission-modes#eliminate-prompts-with-auto-mode) uses to classify actions couldn't produce a decision, so auto mode didn't approve the action automatically. The message you see depends on why the classifier failed.

Reads, searches, and edits inside your working directory skip the classifier, so they keep working in all of these cases.

When the classifier model is overloaded:

```text theme={null}
<model> is temporarily unavailable, so auto mode cannot determine the safety of <tool> right now. Wait briefly and then try this action again.
```

**What to do:**

* Retry after a few seconds; Claude sees the same message and usually retries on its own
* If retries keep failing, continue with read-only tasks and come back to the blocked action later
* This is transient and unrelated to [auto mode eligibility](/en/permission-modes#eliminate-prompts-with-auto-mode); you don't need to change settings

When the classifier returned an unparseable response:

```text theme={null}
Auto mode could not evaluate this action and is blocking it for safety — run with --debug for details
```

**What to do:**

* Retry the action; this usually succeeds on the next attempt
* Run `claude --debug` and repeat the action to see the underlying classifier response in the debug log

When a separate API safety check blocked the classifier request because of earlier conversation content:

```text theme={null}
Auto mode could not evaluate this action and is blocking it for safety — a safety check separate from auto mode blocked this request because of earlier conversation content — it isn't about the action itself — run with --debug for details
```

**What to do:**

* This is not a decision about your action. Content already in your conversation triggered a safety filter on the API when auto mode sent the conversation to the classifier
* Retrying will not help; the same conversation content will trigger the filter again
* Switch to a different [permission mode](/en/permission-modes) so you can approve the action when prompted, or start a fresh conversation without the triggering content

When the conversation has grown larger than the classifier's context window:

```text theme={null}
Auto mode classifier transcript exceeded context window — falling back to manual approval (try /compact to reduce conversation size)
```

In an interactive session, auto mode falls back to a normal permission prompt for that action so you can approve or deny it manually. In [non-interactive mode](/en/headless) the run aborts because the transcript only grows and retrying can't succeed.

**What to do:**

* Approve or deny the action in the prompt that appears
* Run `/compact` to reduce the conversation size so subsequent actions fit within the classifier window again

### Agent terminated early due to an API error

{/* min-version: 2.1.199 */}A [subagent](/en/sub-agents)'s API request failed terminally, for example because a usage limit was reached or retries for a server error ran out, so the subagent stopped before finishing its task. This message requires Claude Code v2.1.199 or later; before then the API error text was returned to Claude as if it were the subagent's result.

```text theme={null}
Agent terminated early due to an API error: <error detail>
```

**What to do:**

* Match the error detail after the colon to its own section on this page, such as [Usage limits](#usage-limits) or [Server errors](#server-errors), and follow that section's steps
* Once the underlying error clears, ask Claude to retry the task or [resume the subagent](/en/sub-agents#resume-subagents)

When a rate limit, overload, or server error interrupts a foreground subagent that already produced text output, Claude receives that partial output marked as incomplete instead of this error. {/* min-version: 2.1.200 */}A subagent whose only output was tool calls gets this error too; in v2.1.199 that shape returned an empty partial result instead. See [API errors in subagents](/en/sub-agents#api-errors-in-subagents).

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
* Run `/usage-credits` to buy additional usage on Pro and Max, or to request it from your admin on Team and Enterprise. See [usage credits for paid plans](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) for how this is billed.
* To upgrade your plan for higher base limits, see [claude.com/pricing](https://claude.com/pricing)

To watch your remaining allowance before you hit the limit, add the `rate_limits` fields to a [custom status line](/en/statusline#rate-limit-usage), or in the Desktop app click the [usage ring](/en/desktop#check-usage) next to the model picker.

### Usage credits required for 1M context

The selected model uses the 1M-token extended context window, and your plan only includes it through usage credits.

```text theme={null}
API Error: Usage credits required for 1M context · run /usage-credits to turn them on, or /model to switch to standard context
```

This is an entitlement check, not a quota exhaustion. It fires even when your session and weekly allowances have capacity remaining. See [Extended context](/en/model-config#extended-context) for which plans include 1M context directly and which require usage credits.

{/* min-version: 2.1.172 */}When this error appears mid-conversation because the context grew past 200K tokens, Claude Code automatically compacts the conversation back under the standard context limit and keeps the session at that limit afterward, so no action is needed. On versions before v2.1.172, the error repeated on every subsequent request including `/compact`; run `/clear` on those versions to recover. The steps below apply when you explicitly selected a `[1m]` model.

**What to do:**

* Run `/model` and select the variant without the `[1m]` suffix to fall back to the standard context window
* Run `/usage-credits` to turn on metered billing for the 1M variant on Pro and Max, or to request it from your admin on Team and Enterprise
* If the error persists after `/model`, a 1M model ID may be set elsewhere. See [There's an issue with the selected model](#there%E2%80%99s-an-issue-with-the-selected-model) for the configuration locations to check in priority order.
* To remove 1M variants from the model picker entirely, set [`CLAUDE_CODE_DISABLE_1M_CONTEXT=1`](/en/env-vars)

### Server is temporarily limiting requests

The API applied a short-lived throttle that is unrelated to your plan quota.

```text theme={null}
API Error: Server is temporarily limiting requests (not your usage limit)
```

Claude Code tells these apart from your plan limit by the absence of the unified quota headers a real limit response carries. {/* min-version: 2.1.199 */}As of v2.1.199 this is [retried automatically](#automatic-retries) with backoff before being shown, whichever way you authenticate. On earlier versions, a session signed in with a claude.ai subscription failed the turn on the first occurrence; only API key and Enterprise sign-ins retried it.

**What to do:**

* Wait briefly and try again
* Check [status.claude.com](https://status.claude.com) if it persists

### Request rejected (429)

You have hit the rate limit configured for your API key, Amazon Bedrock project, or Google Cloud project.

```text theme={null}
API Error: Request rejected (429) · this may be a temporary capacity issue. If it persists, check https://status.claude.com.
```

The trailing sentence names where to check service health and varies by provider. Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry configurations name that provider's service status instead of the Anthropic status page. A custom `ANTHROPIC_BASE_URL` names the gateway host.

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
* See [Authentication precedence](/en/authentication#authentication-precedence) to understand which credential Claude Code uses when several are present

If you are prompted to log in repeatedly, see [Not logged in or token expired](/en/troubleshoot-install#not-logged-in-or-token-expired) for system clock and macOS Keychain fixes.

### Could not resolve authentication method

The session reached the API client without any credential. This appears in [background sessions](/en/agent-view), cloud sessions, and Agent SDK contexts where the interactive login check doesn't run before the first request.

```text theme={null}
Could not resolve authentication method. Expected one of apiKey, authToken, credentials, config, or profile to be set. Or for one of the "X-Api-Key" or "Authorization" headers to be explicitly omitted
```

{/* min-version: 2.1.174 */}Before v2.1.174, a background or cloud session assigned to an idle pre-initialized worker could fail this way even when valid credentials were configured. Upgrade to recover. On current versions the error means no credential was available to the worker process.

**What to do:**

* Upgrade to v2.1.174 or later if this appears in a background or cloud session and your credentials are already configured
* Confirm `ANTHROPIC_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`, or your cloud provider credentials are set in the environment that launches the worker, not only in your interactive shell
* For the Agent SDK, see [authentication setup](/en/agent-sdk/overview#get-started)
* Run `/status` in an interactive session in the same environment to confirm which credential source resolves

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

### Your organization has disabled API key authentication

This message requires Claude Code v2.1.169 or later. Your Console organization's admin has turned off API key authentication, so the API rejects the key Claude Code is sending. The recovery hint after the `·` varies by where the key came from:

```text theme={null}
Your organization has disabled API key authentication · Run /login to sign in with your claude.ai account
Your organization has disabled API key authentication · Unset ANTHROPIC_API_KEY to use your claude.ai account instead
Your organization has disabled API key authentication · Unset ANTHROPIC_API_KEY and run /login to sign in with your claude.ai account
Your organization has disabled API key authentication · Unset the apiKeyHelper setting and run /login to sign in with your claude.ai account
```

Environment variables and `apiKeyHelper` take precedence over `/login`, so running `/login` alone doesn't help while either is still supplying a key. See [Authentication precedence](/en/authentication#authentication-precedence).

**What to do:**

* If the message names `ANTHROPIC_API_KEY`, unset it in the current shell and remove it from your shell profile or `.env` file, then relaunch `claude`
* If the message names `apiKeyHelper`, remove the [`apiKeyHelper`](/en/settings#available-settings) setting from your `settings.json`
* Run `/login` to sign in with your claude.ai account
* Run `/status` afterward to confirm the active credential is your subscription rather than an API key
* If you need API key authentication for automation, ask your organization admin to re-enable it in the Console

### Your organization has disabled Claude subscription access

Your Claude organization doesn't allow signing in to Claude Code with a subscription login. Running `/login` again with the same account returns the same error.

```text theme={null}
Your organization has disabled Claude subscription access for Claude Code · Use an Anthropic API key instead, or ask your admin to enable access
```

This is a server-side organization setting, so it can't be overridden from local settings, environment variables, or CLI flags.

The Agent SDK and `-p` non-interactive mode surface this as the `oauth_org_not_allowed` error code.

**What to do:**

* Ask your admin to enable Claude Code access for your organization
* Authenticate with a Console API key instead of your subscription. See [Claude Console authentication](/en/authentication#claude-console-authentication) for setup.
* If you are the admin and do not see an option to enable access, contact [Anthropic support](https://support.claude.com)

### Routines are disabled by your organization's policy

An Owner in your Team or Enterprise organization has turned off routines at the organization level. The error appears when you try to create or run a routine, including from `/schedule` and the [Routines](/en/routines) UI on claude.ai/code.

```text theme={null}
Routines are disabled by your organization's policy.
```

This is a server-side setting, so it can't be overridden from local settings, environment variables, or CLI flags.

**What to do:**

* Ask an Owner in your organization to enable the **Routines** toggle at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)
* For one-off scheduled work that does not require organization-level routines, see [scheduled tasks](/en/scheduled-tasks)

### Remote Control requires the Anthropic API

The session isn't talking to the Anthropic API directly, so there is no claude.ai backend for [Remote Control](/en/remote-control) to pair with.

```text theme={null}
Remote Control is only available when using Claude via api.anthropic.com.
```

This appears on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry. {/* min-version: 2.1.196 */}As of v2.1.196 it also appears when [`ANTHROPIC_BASE_URL`](/en/env-vars) points at a host other than `api.anthropic.com`, such as an [LLM gateway](/en/llm-gateway) or proxy, even when you sign in with claude.ai.

**What to do:**

* Unset `ANTHROPIC_BASE_URL` and restart the session, or start Remote Control from a session that talks to the Anthropic API directly
* For this and the other Remote Control startup messages, see [Troubleshoot Remote Control](/en/remote-control#troubleshooting)

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

* Run `/login` to get a new token with the current scopes. You don't need to log out first.

### AWS credentials expired or invalid

{/* min-version: 2.1.198 */}This message requires Claude Code v2.1.198 or later and only appears when [`awsAuthRefresh`](/en/amazon-bedrock#advanced-credential-configuration) is set in your settings file. Your AWS session token expired or was rejected, and the automatic refresh Claude Code already ran didn't produce a credential the API accepts. It appears on a 401 from [Claude Platform on AWS](/en/claude-platform-on-aws) or the [Mantle endpoint](/en/amazon-bedrock#use-the-mantle-endpoint), which is how those providers report an expired security token.

The action hint in the middle names the `awsAuthRefresh` command from your settings, so it varies. The stable part is the leading `AWS credentials expired or invalid`:

```text theme={null}
AWS credentials expired or invalid · run /login and select "Claude Platform on AWS · refresh credentials", or run `aws sso login --profile myprofile` in another terminal · API Error: 401 ...
```

Without `awsAuthRefresh` configured, the same 401 shows the generic `Please run /login` message instead, which can't refresh AWS credentials.

**What to do:**

* Run the `awsAuthRefresh` command named in the message, such as `aws sso login --profile myprofile`, in another terminal and complete the browser sign-in, then retry
* In an interactive session, run `/login`, choose **3rd-party platform**, then select **Claude Platform on AWS · refresh credentials** under **Using 3rd-party platforms** to run the same command without restarting Claude Code. See [Configure AWS credentials](/en/claude-platform-on-aws#1-configure-aws-credentials)
* If the error repeats after the refresh command succeeds, confirm the identity is valid outside Claude Code with `aws sts get-caller-identity` in the same shell and profile

### AWS authentication failed

{/* min-version: 2.1.198 */}This message requires Claude Code v2.1.198 or later and only appears when [`awsAuthRefresh`](/en/amazon-bedrock#advanced-credential-configuration) is set in your settings file. Your AWS provider returned a 403, or [Amazon Bedrock](/en/amazon-bedrock) returned a 401.

Claude Code can't tell which cause you hit. Amazon Bedrock reports an expired security token as a 403, but a 403 is also how it reports an authorization denial, such as an `AccessDeniedException` from a missing IAM permission or a model that isn't enabled for your account.

A 401 from Amazon Bedrock also lands here rather than under [AWS credentials expired or invalid](#aws-credentials-expired-or-invalid), because Amazon Bedrock doesn't report an expired token as a 401. A 401 from that endpoint typically comes from something else in the request path, such as a corporate proxy.

A credential refresh fixes an expired token and can't fix the other causes, so the message offers both:

```text theme={null}
AWS authentication failed · run /login and select "Claude Platform on AWS · refresh credentials", or run `aws sso login --profile myprofile` in another terminal · if credentials are current, check AWS permissions and model access · API Error: 403 ...
```

The action hint in the middle names the `awsAuthRefresh` command from your settings, so it varies. The stable part is the leading `AWS authentication failed`.

**What to do:**

* Run the `awsAuthRefresh` command named in the message, or `aws sso login`, in case an expired credential is the cause
* If your credentials are current, confirm the IAM permissions in [IAM configuration](/en/amazon-bedrock#iam-configuration) are attached to the identity you're using and that the selected model is enabled for your account and region
* Run `aws sts get-caller-identity` to confirm which identity your requests use; a stale `AWS_PROFILE` or default profile is a common cause of a permission mismatch

## Network and connection errors

These errors mean a network request from Claude Code failed to reach its destination. They usually originate in your local network, proxy, or firewall, or in the cloud environment's network policy.

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
* If you route through an LLM gateway or relay, set [`ANTHROPIC_BASE_URL`](/en/env-vars) to its address. See [Connect Claude Code to an LLM gateway](/en/llm-gateway-connect) for setup.
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

{/* min-version: 2.1.199 */}As of v2.1.199, a certificate validation failure isn't retried, so this error appears on the first attempt instead of after the full [retry budget](#automatic-retries). Earlier versions spent a few minutes retrying before showing it. Transient TLS conditions, such as a handshake timeout, still retry.

During `/login` and the startup connectivity check, the same failure is reported with the OpenSSL code and the fix inline:

```text theme={null}
SSL certificate error (UNABLE_TO_GET_ISSUER_CERT_LOCALLY). If you are behind a corporate proxy or TLS-intercepting firewall, set NODE_EXTRA_CA_CERTS to your CA bundle path, or ask IT to allowlist *.anthropic.com. Run /doctor for details.
```

**What to do:**

* Export your organization's CA bundle and point Claude Code at it with `NODE_EXTRA_CA_CERTS=/path/to/ca-bundle.pem`
* See [Network configuration](/en/network-config#custom-ca-certificates) for full setup instructions
* Don't set `NODE_TLS_REJECT_UNAUTHORIZED=0`, which disables certificate validation entirely

### Host not allowed in a cloud session

An outbound HTTP request from a cloud session or routine was blocked by the environment's network policy.

```text theme={null}
HTTP 403
x-deny-reason: host_not_allowed
```

You may also see a TLS certificate that doesn't match the destination's real certificate. The cloud environment routes outbound traffic through a proxy that enforces the network policy, so a mismatched certificate means the proxy terminated the connection, not the destination.

This is not a client-side network problem. Cloud sessions and [routines](/en/routines) run inside a sandboxed environment whose outbound traffic is filtered to the environment's allowlist. The **Default** environment uses **Trusted** access, which permits the [default allowlist](/en/claude-code-on-the-web#default-allowed-domains) of package registries, cloud provider APIs, container registries, and common development domains but blocks everything else.

**What to do:**

* Open the routine for editing, or start a cloud session. Select the cloud icon showing your environment's name, such as **Default**, to open the selector. Hover over your environment and click the settings icon.
* In the **Update cloud environment** dialog, change **Network access** from **Trusted** to **Custom**, then add the blocked domain to **Allowed domains**. Enter one domain per line. Check **Also include default list of common package managers** to keep the [default allowlist](/en/claude-code-on-the-web#default-allowed-domains) alongside your custom domains. Select **Full** instead if you want unrestricted access.
* Click **Save changes**. The next run uses the updated allowlist.

See [Network access](/en/claude-code-on-the-web#network-access) for access levels and the default allowlist. Local CLI sessions are not affected by this policy.

### Couldn't reconnect to your Remote Control session

```text theme={null}
Couldn't reconnect to your Remote Control session. Retry, or start a fresh session without --resume.
```

Resuming with `claude --resume` or `claude --continue` reconnects to the [Remote Control](/en/remote-control) session recorded in that conversation. This message means the reconnection failed for a reason that may be temporary, such as a network interruption or a server error, so Claude Code can't confirm whether the remote session still exists. Your local session keeps running without Remote Control.

**What to do:**

* Run `/remote-control` to retry the connection
* Start Claude Code without `--resume` to create a new Remote Control session
* For other Remote Control startup messages, see [Troubleshoot Remote Control](/en/remote-control#troubleshooting)

You won't see this message when the server confirms the previous session no longer exists; Claude Code creates a new one in that case. {/* min-version: 2.1.200 */}Before v2.1.200, any reconnection failure created a new Remote Control session, which left extra sessions in the session list at claude.ai/code.

## Request errors

These errors relate to the content of your request. Most come back from the API after it rejected the request; a few are produced locally by Claude Code before any request is sent.

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
* If stepping back doesn't free enough space, run `/clear` to start a fresh session. Your previous conversation is preserved and can be reopened with `/resume`.

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

{/* min-version: 2.1.142 */}Claude Code replaces the unprocessable image with a text placeholder and retries, so subsequent messages succeed. On versions before 2.1.142, a pasted image could remain in the conversation and repeat the same error on every subsequent message. To recover on those versions, press Esc twice and step back past the turn where the image was added.

**What to do:**

* Resize the image before pasting. The API accepts images up to 8000 pixels on the longest edge for a single image, or 2000 pixels when many images are in context.
* Take a tighter screenshot of the relevant region instead of the full screen

### Unable to resize image

Claude Code couldn't downscale an attached image before sending it to the API.

```text theme={null}
Unable to resize image — image processing is unavailable and dimensions could not be read from the file header. Please convert the image to PNG, JPEG, GIF, or WebP.
Unable to resize image — dimensions exceed the 2000x2000px limit and image processing failed. Please resize the image to reduce its pixel dimensions.
Unable to resize image (… raw, … base64). The image exceeds the … API limit and compression failed. Please resize the image manually or use a smaller image.
Unable to resize image — could not verify image dimensions are within the 2000x2000px API limit.
```

Claude Code normally resizes large images automatically. These errors mean the native image processor failed to load or returned an error, so the image couldn't be resized to fit within API limits.

**What to do:**

* If the message asks you to convert the image, convert it to PNG, JPEG, GIF, or WebP and attach it again. Claude Code can verify dimensions for these formats without the image processor.
* If the message reports a dimension or size limit, resize or recompress the image below that limit before attaching.

### PDF errors

The PDF you attached couldn't be processed.

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

Claude Code sends beta-only fields such as `context_management`, `effort`, and tool `input_examples` alongside an `anthropic-beta` header that enables them. When a gateway forwards the body but drops the header, the API sees fields it doesn't recognize.

**What to do:**

* Configure your gateway to forward the `anthropic-beta` header. See [feature pass-through](/en/llm-gateway-protocol#feature-pass-through) for what gateways must forward.
* As a fallback, set [`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`](/en/env-vars) before launching. This disables features that require the beta header so requests succeed through a gateway that cannot forward it.

### There's an issue with the selected model

The configured model name was not recognized or your account lacks access to it. As of v2.1.160 the trailing hint, shown here in its interactive form, varies by surface.

```text theme={null}
There's an issue with the selected model (claude-...). It may not exist or you may not have access to it. Run /model to pick a different model.
```

**What to do:**

* **Interactive CLI**: run `/model` to pick from models available to your account.
* **Non-interactive mode (`-p`)**: pass `--model` with a valid alias or ID, or set [`ANTHROPIC_MODEL`](/en/env-vars). The error text shows `Run --model` on this surface.
* **Agent SDK**: the error text omits the hint because the model is set programmatically. Set [`model` on `Options`](/en/agent-sdk/typescript#options) in TypeScript or [`ClaudeAgentOptions(model=...)`](/en/agent-sdk/python#claudeagentoptions) in Python, and handle the structured `model_not_found` error to surface your own retry or model picker.
* Use an alias such as `sonnet` or `opus` instead of a full versioned ID. Aliases resolve to a maintained default so they don't go stale. See [Model configuration](/en/model-config).
* If the wrong model keeps coming back in the CLI, a stale ID is set somewhere. Check in [priority order](/en/model-config#setting-your-model): the `--model` flag, the `ANTHROPIC_MODEL` environment variable, then the `model` field in `.claude/settings.local.json`, your project's `.claude/settings.json`, and `~/.claude/settings.json`. Remove the stale value and Claude Code falls back to your account default.
* For Google Cloud's Agent Platform deployments, see [Google Cloud's Agent Platform troubleshooting](/en/google-vertex-ai#troubleshooting).

### Model is not a recognized model id

The model string you passed to a model switch isn't a model alias, a model ID this Claude Code version knows, or an ID that starts with `claude-`. The usual causes are a typo in the ID, a display name such as `Sonnet 5` where the ID `claude-sonnet-5` is expected, or an alias that only newer Claude Code versions recognize. Claude Code rejects the switch immediately. Before v2.1.200, Claude Code saved the string and failed on the next request with [There's an issue with the selected model](#there%E2%80%99s-an-issue-with-the-selected-model).

```text theme={null}
Model "claud-sonnet-5" is not a recognized model id. Did you mean 'claude-sonnet-5'?
```

The trailing hint names the closest matching alias or model ID. When nothing is close enough, it reads `Run /model to see available models.` instead.

Claude Code produces this error locally at the moment the switch is requested, before any API request is made. It applies when a model is set through the [Agent SDK](/en/agent-sdk/typescript) `setModel()` method or by an app such as the [Desktop app](/en/desktop) that runs the Claude Code CLI for you.

**What to do:**

* Run `/model` with no argument to open the picker and choose from the models available to your account, then pass the alias or ID shown there
* If you used an alias that a newer Claude Code version supports, run `claude update`. A full ID that starts with `claude-` passes this check even when the model is newer than your Claude Code version, so upgrading isn't needed for those.
* A model saved before v2.1.200 isn't repaired by this check. If a stale value keeps coming back, remove it from the locations listed under [There's an issue with the selected model](#there%E2%80%99s-an-issue-with-the-selected-model).
* The check runs only on the Anthropic API. On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, [Claude Platform on AWS](/en/claude-platform-on-aws), and behind an [LLM gateway](/en/llm-gateway) or a custom `ANTHROPIC_BASE_URL`, your provider or gateway defines the model names, so Claude Code accepts any string and passes it through.

### Claude Opus is not available with the Claude Pro plan

Your active subscription plan does not include the model you selected.

```text theme={null}
Claude Opus is not available with the Claude Pro plan · Select a different model in /model
```

**What to do:**

* Run `/model` and select a model your plan includes
* If you upgraded your plan recently and still see this, run `/logout` then `/login`. The stored token reflects your plan at the time you signed in, so upgrading on the web does not take effect in an existing session until you re-authenticate.
* See [claude.com/pricing](https://claude.com/pricing) for which models each plan includes

### Model is restricted by your organization's settings

Your organization admin has disabled this model in the claude.ai admin console, or it is excluded by an [`availableModels`](/en/model-config#restrict-model-selection) allowlist in managed settings. When the restricted model was set with `--model`, `ANTHROPIC_MODEL`, or the `model` setting, Claude Code substitutes an allowed model and continues. Typing `/model <name>` for a restricted model is rejected with `Run /model to choose a different model.` and the session keeps its current model.

```text theme={null}
Model "claude-opus-4-8" is restricted by your organization's settings. Using claude-sonnet-4-6 instead.
```

**What to do:**

* Run `/model` to pick from the models your organization allows. Restricted models are hidden from the picker.
* If the restricted model was set in `--model`, `ANTHROPIC_MODEL`, or the `model` field of a settings file, remove or update that value so the notice doesn't recur on each launch
* If you need access to the restricted model, ask your organization admin to enable it. See [Organization model restrictions](/en/model-config#organization-model-restrictions).

### thinking.type.enabled is not supported for this model

Your Claude Code version is older than the minimum for Sonnet 5, Opus 4.8, or Opus 4.7. The CLI sent a thinking configuration the model no longer accepts.

```text theme={null}
API Error: 400 ... "thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

**What to do:**

* Run `claude update` and restart Claude Code. Opus 4.7 needs v2.1.111 or later. Opus 4.8 needs v2.1.154 or later. Sonnet 5 needs v2.1.197 or later
* If you can't upgrade, run `/model` and select Opus 4.6 or Sonnet 4.6 instead
* {/* min-version: agent-sdk@0.3.197 */}If you hit this in the [Agent SDK](/en/agent-sdk/overview), upgrade the SDK package instead. Opus 4.8 needs TypeScript SDK v0.3.154 or later and Python SDK v0.2.88 or later. Sonnet 5 needs TypeScript SDK v0.3.197 or later

### Thinking budget exceeds output limit

The configured extended thinking budget exceeds the maximum response length, so there is no room left for the actual answer.

```text theme={null}
API Error: 400 ... max_tokens must be greater than thinking.budget_tokens
```

Claude Code adjusts these values automatically on the Anthropic API. You typically see this error on Amazon Bedrock or Google Cloud's Agent Platform when [`MAX_THINKING_TOKENS`](/en/env-vars) is set higher than the provider's output limit, or when plan mode raises the thinking budget.

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

* {/* max-version: 2.1.155 */}If you are using Opus 4.7 or Opus 4.8, run `claude update` first. Versions before v2.1.156 can trigger this error during normal tool use, and `/rewind` doesn't clear it.
* Run `/rewind`, or press Esc twice, to step back to a checkpoint before the corrupted turn and continue from there. See [Checkpointing](/en/checkpointing) for how checkpoints are created and restored.

### Usage Policy refusal

The API declined to respond because content in the conversation triggered a [Usage Policy](https://www.anthropic.com/legal/aup) check. The message includes a Request ID you can quote to support if you believe the refusal is incorrect.

```text theme={null}
API Error: Claude Code is unable to respond to this request, which appears to violate our Usage Policy (https://www.anthropic.com/legal/aup). Please double press esc to edit your last message or start a new session for Claude Code to assist with a different task.
```

The check evaluates the full conversation, not only your latest prompt, so sending a new message in the same session usually re-triggers the same refusal. The same applies after exiting and reopening the session with `--continue` or `--resume`, since the transcript on disk still contains the triggering content. On [Amazon Bedrock](/en/amazon-bedrock), [Google Cloud's Agent Platform](/en/google-vertex-ai), and [Microsoft Foundry](/en/microsoft-foundry), this message also covers requests the model's safety measures flagged as a cybersecurity topic. See [Safety measures flagged a cybersecurity topic](#safety-measures-flagged-a-cybersecurity-topic).

**What to do:**

* Press Esc twice or run `/rewind` to step back to a checkpoint before the turn that triggered the refusal, then rephrase or take a different approach. See [Checkpointing](/en/checkpointing).
* If you can't identify which turn caused it, run `/clear` to start a fresh conversation in the same project. Your previous conversation is preserved on disk and remains available in `/resume`.
* In [non-interactive mode](/en/headless) (`-p`), where rewind is unavailable, retry with a rephrased prompt in a new session without `--continue`. Policy checks vary by model, so switching to a different model with `--model` may also resolve the refusal in some cases.

### Safety measures flagged a cybersecurity topic

The model's safety measures flagged content in the conversation as a cybersecurity topic. The message names the model that flagged the request:

```text theme={null}
API Error: Opus 4.8 has safety measures that flagged this message for a cybersecurity topic. To learn about the Cyber Verification Program and apply for access, visit our help center: https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude.

If you were not engaging in a cybersecurity topic, please send feedback via /feedback.
```

The message links to the [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude), which grants access for legitimate cybersecurity work. The safeguard itself is server-side and predates v2.1.203; this release changed only the wording of the message and the page it links to.

What you see depends on your provider and mode:

* On [Amazon Bedrock](/en/amazon-bedrock), [Google Cloud's Agent Platform](/en/google-vertex-ai), and [Microsoft Foundry](/en/microsoft-foundry), a cybersecurity flag produces the [Usage Policy refusal](#usage-policy-refusal) message instead.
* [Non-interactive mode](/en/headless) omits the `/feedback` sentence.

{/* max-version: 2.1.202 */}Before v2.1.203, the message read `<model>'s safeguards flagged this message for a cybersecurity topic. If your work requires this access, you can apply for an exemption:` followed by an exemption form link.

**What to do:**

* If your work requires this content, apply for access through the [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude)
* If your request wasn't about a cybersecurity topic, run `/feedback` to report the false positive
* To keep working in the same session, press Esc twice or run `/rewind` to step back to a checkpoint before the turn that triggered the flag, then take a different approach. See [Checkpointing](/en/checkpointing).

## Installation errors

These errors appear while installing or updating Claude Code, from the [install script](/en/setup#install-claude-code), `claude install`, or `claude update`. For `command not found`, PATH, permission, and TLS problems during setup, see [Troubleshoot installation and login](/en/troubleshoot-install).

### Installation was killed before it could finish

The install script reports when the `claude install` step is terminated by a signal. On Linux, exit code 137 means the process received SIGKILL, and on a low-memory host that's usually the kernel out-of-memory (OOM) killer. The script prints this explanation and exits with code 137:

```text theme={null}
Installation was killed before it could finish (exit code 137). This usually means the system ran out of memory.
Claude Code needs roughly 512MB of free memory to install. Free up memory, then run this script again.
```

For any other fatal signal, and for exit code 137 on macOS, the script prints `Installation was killed before it could finish (exit code <N>)` with the actual exit code and omits the out-of-memory explanation. The message comes from the install script macOS and Linux use, which also covers installs inside WSL; the native Windows install scripts never print it. Before v2.1.200, the script exited with only the shell's bare `Killed` line.

**What to do:**

* Stop other processes to free memory, then rerun the installer
* Add swap space or move to a larger instance. See [Install killed on low-memory Linux servers](/en/troubleshoot-install#install-killed-on-low-memory-linux-servers) for the swap-file commands.

### The connection dropped while downloading the update

The connection to the download server closed while `claude install`, `claude update`, or the [automatic updater](/en/setup#auto-updates) was fetching the Claude Code binary, and the retries didn't recover. Claude Code retries the download when the connection drops, the transfer stalls, or the downloaded file fails its checksum, up to three attempts in total. A completed HTTP error, such as a 404, isn't retried because the server already answered. {/* min-version: 2.1.202 */}Before v2.1.202, a single dropped connection failed the download immediately with the bare error `aborted` instead of retrying.

```text theme={null}
The connection dropped while downloading the update (attempt 3/3: aborted). Check your network — proxies sometimes cut off large downloads.
```

The text in parentheses names which attempt failed and the underlying network error. `claude update` precedes the message with `Error: Failed to install native update` on stderr.

The usual cause is a proxy or gateway that closes a long transfer before it finishes. The Claude Code binary is a large download, so a proxy connection limit that never affects normal API traffic can still interrupt it.

**What to do:**

* Run `claude update` again. On an otherwise healthy network, the download usually succeeds on the next run.
* If your network requires a proxy, set `HTTPS_PROXY` before running the installer or `claude update`. See [Check network connectivity](/en/troubleshoot-install#check-network-connectivity).
* If a corporate proxy keeps closing the transfer, ask your network team to allow the full download from `downloads.claude.ai`. See [Network access requirements](/en/network-config#network-access-requirements).
* Run `claude doctor` from your shell for installation diagnostics

## Command-line errors

These errors come from Claude Code's own validation of the `claude` command line. Claude Code prints them immediately, before it creates a session or sends any API request.

### Conflict between --bg and --print

This message requires Claude Code v2.1.198 or later. You combined `--bg` with `-p` or `--print` in the same `claude` invocation. `--bg` starts a [background session](/en/agent-view#from-your-shell) that you later attach to with `claude agents`, while `--print` runs [non-interactively](/en/headless) and never starts the interactive session that `claude agents` attaches to. Before v2.1.198 this combination silently created a background job that could never be attached to.

```text theme={null}
--bg and --print conflict: --print never starts the interactive session that `claude agents` attaches to, so the job would be unattachable. The prompt is the positional — drop --print: `claude --bg '<task>'`.
```

**What to do:**

* Drop `-p` or `--print`. `--bg` takes the prompt as its positional argument, so `claude --bg "<task>"` is the complete command. See [Dispatch new agents from your shell](/en/agent-view#from-your-shell).
* To run the prompt non-interactively and print the result instead of creating a background session, drop `--bg` and run `claude -p "<task>"`

## Configuration warnings

Claude Code writes these messages to stderr at startup rather than showing an error in the conversation. They report configuration it read but didn't apply.

### Workspace has not been trusted

Claude Code found `permissions.allow` rules or `permissions.additionalDirectories` entries in the project's `.claude/settings.json` or `.claude/settings.local.json` and didn't apply them, because [allow rules from project settings require workspace trust](/en/permissions#project-allow-rules-and-workspace-trust). The count, the setting name, and the file named in the message vary with your configuration. `deny` and `ask` rules aren't affected.

```text theme={null}
Ignoring 2 permissions.allow entries from .claude/settings.local.json: this workspace has not been trusted. Run Claude Code interactively here once and accept the trust dialog, or set projects["/Users/you/project"].hasTrustDialogAccepted: true in /Users/you/.claude.json.
```

**What to do:**

* Run `claude` in the directory and accept the trust dialog. {/* min-version: 2.1.200 */}The dialog appears even when a parent directory is already trusted, lists the rules being held back, and lets you decline and keep working without them. Before v2.1.200, no dialog appeared in that situation, so this step couldn't be completed there.
* In [non-interactive mode](/en/headless) with `-p` no dialog is shown. Set the `hasTrustDialogAccepted` entry in `~/.claude.json` using the exact `projects` key the message prints.
* {/* min-version: 2.1.200 */}If the message names `.claude/settings.local.json` and you started Claude Code outside a git repository or in your home directory, update to v2.1.200 or later. Versions 2.1.196 through 2.1.199 treated your own `.claude/settings.local.json` as repository-supplied in those workspaces. See [Project allow rules and workspace trust](/en/permissions#project-allow-rules-and-workspace-trust).

## Responses seem lower quality than usual

If Claude's answers seem less capable than you expect but no error is shown, the cause is usually conversation state rather than the model itself. Claude Code doesn't silently change model versions. It can switch to a fallback model in three specific cases:

* A configured [`--fallback-model`](/en/cli-reference#cli-flags) takes over after an availability error, for that turn only, with a notice in the transcript
* An Amazon Bedrock or Google Cloud's Agent Platform startup check finds your default model unavailable
* [Automatic model fallback](/en/model-config#automatic-model-fallback) on Fable 5 moves the session to the default Opus model and shows a notice in the transcript

The Model selection check below catches the second and third cases; the first appears as a transcript notice rather than a `/model` change. [Model configuration](/en/model-config) explains when each fallback applies.

Check these first:

* **Model selection**: run `/model` to confirm you are on the model you expect. A previous `/model` choice or an `ANTHROPIC_MODEL` environment variable may have you on a smaller model than you intended.
* **Effort level**: run `/effort` to check the current reasoning level and raise it for hard debugging or design work. Defaults vary by model, so check before assuming you are below the maximum. See [Adjust effort level](/en/model-config#adjust-effort-level) for per-model defaults and the `ultrathink` shortcut.
* **Context pressure**: run `/context` to see how full the window is. If it is near capacity, run `/compact` at a natural breakpoint or `/clear` to start fresh. See [Explore the context window](/en/context-window) for how auto-compact affects earlier turns.
* **Stale instructions**: large or outdated `CLAUDE.md` files and MCP tool definitions consume context and can steer responses. `/doctor` flags oversized memory files and subagent definitions; `/context` shows MCP tool token usage.

When a response goes wrong, rewinding usually works better than replying with corrections. Press Esc twice or run `/rewind` to step back to before the bad turn, then rephrase the prompt with more specifics. Correcting in-thread keeps the wrong attempt in context, which can anchor later answers to it. See [Checkpointing](/en/checkpointing).

If quality still seems off after checking the above, run `/feedback` and describe what you expected versus what you got. Feedback submitted this way includes the conversation transcript, which is the fastest way for Anthropic to diagnose a real regression. See [Report an error](#report-an-error) if `/feedback` is unavailable in your environment.

{/* min-version: 2.1.201 */}If Sonnet 5 refuses a request and cites a suspected prompt injection on Claude Code v2.1.200 or earlier, run `claude update` to pick up the v2.1.201 fix.

## Report an error

For errors from components this page doesn't cover, see the relevant guide:

* MCP server failed to connect or authenticate: [MCP](/en/mcp)
* Hook script failed or blocked a tool: [Debug hooks](/en/hooks#debug-hooks)
* Permission denied or filesystem errors during install: [Troubleshoot installation and login](/en/troubleshoot-install)

If an error is not listed here or the suggested fix does not help:

* Run `/feedback` inside Claude Code to send the transcript and a description to Anthropic. The command also offers to open a prefilled GitHub issue. On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and other third-party providers, `/feedback` saves a local archive you can send to your Anthropic account representative instead.
* Run `/doctor` to check for local configuration problems
* Check [status.claude.com](https://status.claude.com) for active incidents
* Search [existing issues](https://github.com/anthropics/claude-code/issues) on GitHub
