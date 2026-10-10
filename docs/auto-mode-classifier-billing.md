> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Auto mode classifier request charges

> Resolve the Claude Code notice saying this session isn't eligible for auto mode's no-charge classifier requests: what it means, why it appears, and what to do.

In [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode), a classifier checks actions such as shell commands and network requests before they run. Wherever [server-side checks are on](/docs/en/permission-modes#server-side-classifier-review), the server performs those checks as part of the session's own model requests, at no charge. This notice means the server's checks aren't reaching your session, so Claude Code is making its own classifier requests instead, and on your account those requests count toward your token usage:

```text theme={null}
We're changing auto mode to no longer charge for classifier requests in Claude Code. However, this session isn't eligible.
```

At the prompt, Claude Code holds the first action it would check that way until you answer. Nothing is broken: auto mode keeps working, and its classifier requests are billed as they were before. The most common cause is an LLM gateway or proxy between Claude Code and the API, and when Claude Code can identify one, the notice names it. Press **Enter** to continue, or see [Make the session eligible](#make-the-session-eligible) to keep it from appearing in new sessions.

## Respond to the notice

The notice holds the action until you answer it:

* **Enter** continues: the held action and the rest of the session use Claude Code's own classifier requests, billed as token usage as before, and the notice doesn't appear again in that session. When the notice named a gateway, acknowledging it keeps it from reappearing on this machine for 24 hours. When it didn't, the notice returns the next time a session falls back.
* **Esc** or **Ctrl+C** cancels: the held action doesn't run and the current turn stops, with the session still in auto mode. Nothing is remembered, so the notice appears again before the next checked action.

To stop using auto mode instead, switch permission modes with `Shift+Tab` after you answer.

Where the notice can't wait for an answer, Claude Code reports the same text and the session continues in auto mode, unless a gateway acknowledgment on this machine in the last 24 hours has dismissed it. In [non-interactive mode](/docs/en/headless) with `-p` it prints the text to stderr, and in `stream-json` output it emits a `system` warning message, which Agent SDK applications can read from the message stream.

## Make the session eligible

If a gateway is the cause, ask your company's admin or your gateway provider to pass requests and replies through unchanged. That means forwarding request headers and body fields as they are, including ones the gateway doesn't recognize such as the `safeguards` request field, and returning responses and streaming events without dropping keys such as the `safeguard_results` field or rewriting tool-use IDs, as the [gateway compatibility guide](/docs/en/llm-gateway-protocol#feature-pass-through) describes. A gateway that passes traffic through this way keeps working with this feature and with future ones. New sessions then use the server's checks again.

If you already know that your gateway can't provide the server's checks, tell Claude Code not to ask for them there by setting `CLAUDE_CODE_AUTO_MODE_SERVER` to `0` before you start the session, in your shell or in the [`env` settings key](/docs/en/settings-reference#env):

```bash theme={null}
export CLAUDE_CODE_AUTO_MODE_SERVER=0
```

Classifier requests are then always Claude Code's own, billed the same way, and the notice doesn't appear. On a direct connection to the Anthropic API, the variable requires Claude Code v2.1.281 or later. Setting `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` while `CLAUDE_CODE_AUTO_MODE_SERVER` is unset turns the server's checks off as well, except as [Disable pre-release capabilities](/docs/en/llm-gateway-protocol#disable-pre-release-capabilities) describes.

`CLAUDE_CODE_AUTO_MODE_SERVER` is a temporary setting and may be removed in a later release.

## Why the notice appears

[Server-side classifier review](/docs/en/permission-modes#server-side-classifier-review) lists which sessions ask the server for the classifier checks. Pro, Max, and Team plans never show the notice. When it appears, the usual causes are:

* **An LLM gateway or proxy is in the path**: one that strips or rewrites request headers, drops request fields it doesn't recognize, or edits responses. The server then never receives the request for checks, or Claude Code never receives the results. When your configuration or the responses identify the gateway, the notice names it.
* **Server-side checks haven't reached your platform, region, or credential yet**: whether a platform or region performs them depends on that platform's rollout. If you see the notice with no gateway or proxy in the path and it keeps appearing, this is the likely cause. To confirm, contact support or your company's admin, or report it with `/feedback`.

To check a session that's in auto mode, run `/status` at the Claude Code prompt: its **Auto mode server** row reads `Enabled` while the server's checks decide the session's actions and `Disabled` once the session has fallen back.

When a gateway cuts responses short or rewrites the results into a form Claude Code can't read, you get denials with no verdict in place of this notice; see [Server-side classifier review](/docs/en/permission-modes#server-side-classifier-review).

## Related resources

* [Auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode): what auto mode is and what it blocks by default
* [Server-side classifier review](/docs/en/permission-modes#server-side-classifier-review): which sessions ask the server to check actions, and the Claude Code version each one requires
* [Gateway compatibility guide](/docs/en/llm-gateway-protocol#feature-pass-through): what breaks when a gateway strips headers or body fields
* [The server returned no safety verdict](/docs/en/errors#the-server-returned-no-safety-verdict): the denial you see when the server gives no verdict for an action
* [Manage costs effectively](/docs/en/costs): track token usage and reduce Claude Code costs
