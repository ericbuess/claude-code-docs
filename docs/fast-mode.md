> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Speed up responses with fast mode

> Get faster Opus responses in Claude Code by toggling fast mode.

> [!NOTE]
>
> Fast mode is in [research preview](#research-preview). The feature, pricing, and availability may change based on feedback.

Fast mode is a high-speed configuration for Claude Opus, making the model up to 2.5x faster at a higher cost per token. Toggle it on with `/fast` when you need speed for interactive work like rapid iteration or live debugging, and toggle it off when cost matters more than latency.

Fast mode is not a different model. It uses Claude Opus with a different API configuration that prioritizes speed over cost efficiency. You get identical quality and capabilities with faster responses. Fast mode is supported on Opus 5.5, Opus 5, and Opus 4.8. It is not available on Sonnet, Haiku, or other models.

Opus 4.7 doesn't support fast mode, so switching to it turns fast mode off. Fast mode for Opus 4.7 was deprecated on June 25, 2026, and removed on July 24, 2026.

What to know:

* Use `/fast` to toggle on fast mode in the Claude Code CLI. The [VS Code extension](https://code.claude.com/docs/en/vs-code.md) offers a **Toggle fast mode** command when the selected model supports fast mode. Claude Code saves that toggle to your [`fastMode` setting](#toggle-fast-mode).
* Fast mode pricing per MTok input/output is \$8/\$40 on Opus 5.5 and \$10/\$50 on Opus 5 and Opus 4.8.
* Available to Claude Code users on subscription plans (Pro/Max/Team/Enterprise) and on Claude Console. Team and Enterprise organizations need an Owner to enable it first, and Console organizations need access provisioned first, both described under [Requirements](#requirements).
* For Claude Code users on subscription plans (Pro/Max/Team/Enterprise), fast mode is available via usage credits only and not included in the subscription rate limits.

## Toggle fast mode

In the CLI, toggle fast mode in either of these ways:

* Run `/fast`, press Space to toggle on or off, then press Enter to confirm
* Set `"fastMode": true` in your [user settings file](https://code.claude.com/docs/en/settings.md)

By default, fast mode you turn on in an interactive session persists across sessions. You can configure fast mode to reset each session. See [require per-session opt-in](#require-per-session-opt-in) for details.

Outside a [cloud session](#use-fast-mode-in-cloud-sessions), in [non-interactive mode](https://code.claude.com/docs/en/headless.md) with the `-p` flag, `/fast` works only in a session launched with fast mode in its [`--settings`](https://code.claude.com/docs/en/cli-reference#cli-flags) value, for example `claude -p --settings '{"fastMode": true}'`; the toggle then applies to that session only and isn't saved as your default. The `-p` form requires Claude Code v2.1.205 or later. Elsewhere in non-interactive mode, the command reports that fast mode isn't available.

You can run `/fast` while Claude is working, and Claude Code toggles fast mode without waiting for the turn to end. Claude Code finishes the running turn at its original speed, so the speed change takes effect from your next turn. If your current model doesn't support fast mode, turning it on also switches your model, and Claude Code uses the new model from its next request in that turn.

For the best cost efficiency, enable fast mode at the start of a session rather than switching mid-conversation. See [understand the cost tradeoff](#understand-the-cost-tradeoff) for details.

When you enable fast mode:

* If your current model doesn't support fast mode, Claude Code switches to Opus
* You'll see a confirmation message: "Fast mode ON"
* A small `↯` icon appears next to the prompt while fast mode is active
* Run `/fast` again at any time to check whether fast mode is on or off

Opus 5.5 is the fast mode default in Claude Code v2.1.280 and later. Before v2.1.280, fast mode defaulted to Opus 5 from v2.1.219.

When you disable fast mode with `/fast` again, you remain on Opus. To switch to a different model, use `/model`.

### Switch models while fast mode is on

Fast mode follows your model switches in both directions:

* **Switch away**: when you switch to a model that doesn't support fast mode, Claude Code turns fast mode off. This includes Opus 4.7; before v2.1.221, fast mode stayed on after a switch to Opus 4.7 and the API rejected the requests.
* **Switch back**: switching back to a supported Opus model turns fast mode on again when your saved fast mode preference is on, the same preference a new session starts from by default. A model switch never turns fast mode on for a session whose saved preference is off, and with [per-session opt-in](#require-per-session-opt-in) configured, switching back doesn't turn it on either; run `/fast` to re-enable it.

Whenever a model switch turns fast mode on or off, Claude Code shows a `Fast mode ON` or `Fast mode OFF` confirmation, and the `↯` icon appears while fast mode is on. This holds whether you switch with `/model`, with [`/config model=<model>`](https://code.claude.com/docs/en/settings), or from a device connected through [Remote Control](https://code.claude.com/docs/en/remote-control.md).

Claude Code resends the session's fast mode status to devices connected through Remote Control after a model switch, a reconnection, or a failed [availability check](#use-fast-mode-behind-proxies-and-llm-gateways).

### Use fast mode in cloud sessions

Fast mode works in [cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web.md) when it's available on your account, whether the session runs on Anthropic-managed infrastructure or a [self-hosted runner](https://code.claude.com/docs/en/self-hosted-environments). Requires Claude Code v2.1.271 or later in the session's environment.

Type `/fast on` in the session to turn fast mode on. It stays on for that session only and isn't saved as your default. The [requirements](#requirements) apply in cloud sessions too.

In the browser at [claude.ai/code](https://claude.ai/code), you can also turn fast mode on and off from the model menu on the message box. The menu shows the switch when your plan includes fast mode and the selected model supports it.

## Understand the cost tradeoff

Fast mode has higher per-token pricing than standard Opus:

| Model | Input (MTok) | Output (MTok) |
| - | - | - |
| Opus 5.5 | \$8 | \$40 |
| Opus 5 | \$10 | \$50 |
| Opus 4.8 | \$10 | \$50 |

Fast mode pricing is flat across the full 1M token context window. For the standard Opus rate to compare against, see the [Claude pricing reference](https://platform.claude.com/docs/en/about-claude/pricing).

The first time you enable fast mode in a conversation, you pay the full fast mode uncached input token price for the entire conversation context. The deeper into a conversation you are, the more this costs, so the charge is smallest when you enable fast mode at the start. Fast mode and standard speed keep [separate caches](https://code.claude.com/docs/en/prompt-caching.md#turning-on-fast-mode), so each later switch reads part or all of the conversation uncached again.

### See where fast mode spend appears

You see fast mode spend in a different place depending on how you signed in, so first run [`/status`](https://code.claude.com/docs/en/commands) to check. If it shows a `Login method` row such as `Claude Max account`, you signed in with a Claude subscription. If it shows an `API key` row instead, your requests bill to a Claude Console organization.

* **Pro and Max**: you pay for fast mode from your usage credits. Go to [**Settings > Usage**](https://claude.ai/settings/usage) on claude.ai, where the **Usage credits** section shows how much you've spent in usage credits this month. That figure includes fast mode but doesn't break it out separately.
* **Team and Enterprise**: your organization pays for your fast mode usage from its usage credits. To see your own usage-credits spend, run [`/usage`](https://code.claude.com/docs/en/costs#check-your-usage-credits-spend). For where your organization sees that spend, see [Claude for Teams and Enterprise](https://code.claude.com/docs/en/costs.md#claude-for-teams-and-enterprise).
* **Claude Console**: your organization pays for fast mode with the rest of its API usage. On the Console [Usage](https://platform.claude.com/usage) and [Cost](https://platform.claude.com/cost) pages, select **Speed (Research Preview)** in the **Group by** menu to separate fast mode from standard-speed usage. You see that option only when the selected date range includes fast mode usage.

## Decide when to use fast mode

Fast mode is best for interactive work where response latency matters more than cost:

* Rapid iteration on code changes
* Live debugging sessions
* Time-sensitive work with tight deadlines

Standard mode is better for:

* Long autonomous tasks where speed matters less
* Batch processing or CI/CD pipelines
* Cost-sensitive workloads

### Fast mode vs effort level

Fast mode and effort level both affect response speed, but differently:

| Setting | Effect |
| - | - |
| **Fast mode** | Same model quality, lower latency, higher cost |
| **Lower effort level** | Less thinking time, faster responses, potentially lower quality on complex tasks |

You can combine both: use fast mode with a lower [effort level](https://code.claude.com/docs/en/model-config.md#adjust-effort-level) for maximum speed on straightforward tasks.

## Requirements

Fast mode requires all of the following:

* **Anthropic API or subscription only**: fast mode is available through the Anthropic Console API and for Claude subscription plans using usage credits. It is not available on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or Claude Platform on AWS. Console organizations must also have [fast mode access provisioned](#enable-fast-mode-for-your-organization).
* **Usage credits turned on for subscription plans**: on a Pro, Max, Team, or Enterprise plan, your account must have [usage credits](https://code.claude.com/docs/en/costs.md#add-usage-credits-to-your-subscription) turned on, which allows billing beyond your plan's included usage. Until they're on, `/fast` reports "Fast mode requires usage credits". How you turn them on depends on your plan:
  * On Pro and Max, turn them on in the **Usage credits** section of [**Settings > Usage**](https://claude.ai/settings/usage) on claude.ai, or run `/usage-credits` to open that page.
  * On Team and Enterprise, a member with billing access turns them on for the organization at [**Organization settings > Usage**](https://claude.ai/admin-settings/usage), and a member without it runs `/usage-credits` to send the organization's admins a request.

> [!NOTE]
>
> Fast mode usage draws directly from usage credits, even if you have remaining usage on your plan.

* **Paid Console organization**: Claude Console accounts don't use usage credits, and your organization pays for fast mode per token with the rest of its API usage. On the Console's free Evaluation plan, `/fast` shows "Fast mode unavailable during evaluation. Please purchase credits." To clear it, purchase credits in your [Console billing settings](https://platform.claude.com/settings/billing).
* **Owner enablement for Team and Enterprise**: fast mode is disabled by default for Team and Enterprise organizations. An Owner must explicitly [enable fast mode](#enable-fast-mode-for-your-organization) before users can access it.

> [!NOTE]
>
> Four organization settings can block turning fast mode on with `/fast`:
>
> * **Fast mode not enabled**: if fast mode hasn't been enabled for your organization, turning fast mode on with `/fast` shows "Fast mode has been disabled by your organization."
> * **Fast mode turned off by managed settings**: if your organization deploys [managed settings](https://code.claude.com/docs/en/managed-settings.md) that set [`fastMode: false`](https://code.claude.com/docs/en/settings-reference#fastmode), turning fast mode on with `/fast` shows the same "Fast mode has been disabled by your organization" message.
> * **Per-session opt-in required**: managed settings that set [`fastModePerSessionOptIn: true`](#require-per-session-opt-in) refuse `/fast on` with the same message everywhere except an interactive terminal session.
> * **Fast-mode model not allowed**: if your organization's [`availableModels`](https://code.claude.com/docs/en/model-config#restrict-model-selection) allowlist excludes the fast-mode Opus model, turning it on is refused with "is not in your organization's allowed models". In a session already running on an allowed Opus model that supports fast mode, `/fast` instead enables fast mode on your current model without switching models.

### Enable fast mode for your organization

Where you enable fast mode depends on which product your organization uses:

* **Console** (API customers): an admin enables it in [Claude Code preferences](https://platform.claude.com/claude-code/preferences). Fast mode is in [research preview](#research-preview), so your organization must also have fast mode access provisioned before fast mode requests succeed. To get access, contact your account manager or join the waitlist, as described in [fast mode on the Claude API](https://platform.claude.com/docs/en/build-with-claude/fast-mode).

  Without provisioned access, the API rejects each fast mode request with a 429, and Claude Code treats each rejection as a [fast mode rate limit](#handle-rate-limits). Unlike a rate limit's cooldown, the rejections continue until access is provisioned.
* **Claude AI** (Team and Enterprise): an Owner enables it at [**Organization settings > Claude Code**](https://claude.ai/admin-settings/claude-code)

Another option to disable fast mode entirely is to set `CLAUDE_CODE_DISABLE_FAST_MODE=1`. See [Environment variables](https://code.claude.com/docs/en/env-vars.md).

### Use fast mode behind proxies and LLM gateways

Before offering fast mode, Claude Code checks your organization's fast mode availability with a request directly to `api.anthropic.com`. The check doesn't follow [`ANTHROPIC_BASE_URL`](https://code.claude.com/docs/en/llm-gateway-connect#set-the-base-url-and-credential), so on a network that routes Claude traffic through an [LLM gateway](https://code.claude.com/docs/en/llm-gateway) and blocks direct egress to `api.anthropic.com`, the check fails even though inference requests work. The check does use a configured [HTTP proxy](https://code.claude.com/docs/en/network-config.md#proxy-configuration), so a network block fails the check only where `api.anthropic.com` is unreachable even through the proxy.

If your organization has fast mode enabled and `/fast` says otherwise, find the message it shows among these cases.

#### Fast mode unavailable due to network connectivity issues

The availability check failed, for example because your network blocks `api.anthropic.com`, and requests run at standard speed. A check that succeeded in the past keeps working from its cached result, so a blocked check mostly affects new installations.

To restore fast mode, allowlist direct egress to `api.anthropic.com`, or set `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS=1`, which treats a failed check as available and still honors a "disabled by your organization" response.

#### Fast mode is currently unavailable

Behind a gateway, check for these configurations, in which Claude Code doesn't send the availability check and has no earlier successful check cached:

* You point `ANTHROPIC_BASE_URL` at your gateway and set [`ANTHROPIC_API_KEY`](https://code.claude.com/docs/en/llm-gateway-connect#set-the-base-url-and-credential) to a gateway-issued key that isn't in the format of an Anthropic API key.
* You set [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](https://code.claude.com/docs/en/env-vars), so Claude Code skips the check.

To restore fast mode in either configuration, set `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS=1`.

#### Fast mode has been disabled by your organization

Behind a gateway, you can see this message even when your organization has fast mode enabled, in either of these configurations:

* You authenticate with [`ANTHROPIC_AUTH_TOKEN`](https://code.claude.com/docs/en/llm-gateway-connect#set-the-base-url-and-credential) alone, with no claude.ai login, no API key, and no cached successful check. Claude Code then treats fast mode as disabled by your organization without sending the request.
* A proxy intercepts the check and answers with its own page, for example a TLS-inspecting proxy returning an HTTP 200 block page. Claude Code reads that page as a response saying your organization has fast mode disabled.

In both cases, set `CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1`, which skips the check entirely, rather than `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS`, which doesn't apply to either.

> [!NOTE]
>
> The skip variables change only the client-side check. When your organization has fast mode disabled, the API rejects fast mode requests whether or not they're set. Claude Code then retries the request at standard speed, turns fast mode off, and `/fast` reports that your organization has disabled fast mode.

### Require per-session opt-in

By default, fast mode a user turns on in an interactive session persists across sessions. To change this, set `fastModePerSessionOptIn` to `true` in any [settings file](https://code.claude.com/docs/en/settings.md#where-settings-live), which causes each session to start with fast mode off and requires users to explicitly enable it with `/fast`. Owners on [Team](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_teams#team-&-enterprise) or [Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_enterprise) plans can deploy it organization-wide through [server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md).

```json theme={null}
{
  "fastModePerSessionOptIn": true
}
```

This is useful for controlling costs in organizations where users run multiple concurrent sessions. The user's fast mode preference is still saved, so removing this setting restores the default persistent behavior.

When managed settings set the key, `/fast on` works only in an interactive terminal session. Everywhere else, including [non-interactive mode](https://code.claude.com/docs/en/headless.md), the [VS Code extension](https://code.claude.com/docs/en/vs-code.md), and [cloud sessions](#use-fast-mode-in-cloud-sessions), it's refused with a message that your organization has disabled fast mode.

## Handle rate limits

Fast mode has separate rate limits from standard Opus. All supported Opus models share one fast mode rate limit pool: usage on any of them draws from the same limits. When you hit the fast mode rate limit:

1. Fast mode automatically falls back to standard speed
2. The `↯` icon turns gray to indicate cooldown
3. You continue working at standard speed and pricing
4. When the cooldown expires, fast mode automatically re-enables

To disable fast mode manually instead of waiting for cooldown, run `/fast` again.

If you run out of usage credits mid-session, Claude Code retries each rejected fast mode request at standard speed and pricing, so you keep working, and there is no cooldown. How you see the rejection depends on the session type:

* In an interactive session, Claude Code shows a "Fast mode disabled · usage credits exhausted" notification and turns fast mode off for the rest of the session. Your saved fast mode preference doesn't change; run `/fast` to turn fast mode back on.
* In [non-interactive mode](https://code.claude.com/docs/en/headless.md) with `--output-format stream-json`, and through the Agent SDK, Claude Code emits the same text on the message stream as a `system` message with subtype `notification`, once per turn while you're out of usage credits. Fast mode stays on. Requires Claude Code v2.1.221 or later.

## Research preview

Fast mode is a research preview feature. This means:

* The feature may change based on feedback
* Availability and pricing are subject to change
* The underlying API configuration may evolve

Report issues or feedback through your usual Anthropic support channels.

## See also

* [Model configuration](https://code.claude.com/docs/en/model-config.md): switch models and adjust effort levels
* [Manage costs effectively](https://code.claude.com/docs/en/costs.md): track token usage and reduce costs
* [Status line configuration](https://code.claude.com/docs/en/statusline.md): display model and context information
