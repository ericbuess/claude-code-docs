> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Speed up responses with fast mode

> Get faster Opus responses in Claude Code by toggling fast mode.

<Note>
  Fast mode is in [research preview](#research-preview). The feature, pricing, and availability may change based on feedback.
</Note>

Fast mode is a high-speed configuration for Claude Opus, making the model 2.5x faster at a higher cost per token. Toggle it on with `/fast` when you need speed for interactive work like rapid iteration or live debugging, and toggle it off when cost matters more than latency.

Fast mode is not a different model. It uses Claude Opus with a different API configuration that prioritizes speed over cost efficiency. You get identical quality and capabilities, just faster responses. Fast mode is supported on Opus 4.6 and Opus 4.7. It is not available on Sonnet, Haiku, or other models.

<Note>
  Fast mode requires Claude Code v2.1.36 or later. Check your version with `claude --version`.
</Note>

What to know:

* Use `/fast` to toggle on fast mode in Claude Code CLI. Also available via `/fast` in Claude Code VS Code Extension.
* By default, `/fast` runs on Opus 4.6. To run fast mode on Opus 4.7 instead, set the [`CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE`](#use-fast-mode-on-opus-4-7) environment variable.
* Fast mode pricing is $30/$150 MTok on both Opus 4.6 and Opus 4.7.
* Available to all Claude Code users on subscription plans (Pro/Max/Team/Enterprise) and Claude Console.
* For Claude Code users on subscription plans (Pro/Max/Team/Enterprise), fast mode is available via extra usage only and not included in the subscription rate limits.

This page covers how to [toggle fast mode](#toggle-fast-mode), [use fast mode on Opus 4.7](#use-fast-mode-on-opus-4-7), the [cost tradeoff](#understand-the-cost-tradeoff), [when to use it](#decide-when-to-use-fast-mode), [requirements](#requirements), [per-session opt-in](#require-per-session-opt-in), and [rate limit behavior](#handle-rate-limits).

## Toggle fast mode

Toggle fast mode in either of these ways:

* Type `/fast` and press Tab to toggle on or off
* Set `"fastMode": true` in your [user settings file](/en/settings)

By default, fast mode persists across sessions. Administrators can configure fast mode to reset each session. See [require per-session opt-in](#require-per-session-opt-in) for details.

For the best cost efficiency, enable fast mode at the start of a session rather than switching mid-conversation. See [understand the cost tradeoff](#understand-the-cost-tradeoff) for details.

When you enable fast mode:

* If you're on a different model, Claude Code automatically switches to the fast mode model: Opus 4.6 by default, or Opus 4.7 when [`CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE`](#use-fast-mode-on-opus-4-7) is set.
* You'll see a confirmation message: "Fast mode ON"
* A small `↯` icon appears next to the prompt while fast mode is active
* Run `/fast` again at any time to check whether fast mode is on or off

When you disable fast mode with `/fast` again, you remain on the same Opus version that fast mode was running on. The model does not revert to your previous model. To switch to a different model, use `/model`.

## Use fast mode on Opus 4.7

<Note>
  Fast mode on Opus 4.7 requires Claude Code v2.1.139 or later.
</Note>

Fast mode for Claude Opus 4.7 is in research preview. It runs at the same 2.5x speed and the same price as fast mode for Opus 4.6, with no other behavior changes.

<Note>
  On May 14, 2026, Opus 4.7 becomes the default fast mode model. Until then, opt in by setting `CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE=1`.
</Note>

To opt in, set `CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE=1` before launching Claude Code. With the variable set, `/fast` runs on Opus 4.7. Without it, `/fast` continues to run on Opus 4.6.

You can set the variable as a shell export:

```bash theme={null}
export CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE=1
```

Or in any Claude Code [settings file](/en/settings#settings-files), including user, project, and managed settings, to scope the opt-in:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE": "1"
  }
}
```

Fast mode for Opus 4.6 remains available alongside Opus 4.7. The two share the same fast mode rate limit pool: usage on either model draws from the same limits.

To pin fast mode to Opus 4.6 explicitly, set `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1`. This variable takes precedence, so fast mode runs on Opus 4.6 regardless of whether `CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE` is set.

## Understand the cost tradeoff

Fast mode has higher per-token pricing than standard Opus:

| Mode                  | Input (MTok) | Output (MTok) |
| --------------------- | ------------ | ------------- |
| Fast mode on Opus 4.6 | \$30         | \$150         |
| Fast mode on Opus 4.7 | \$30         | \$150         |

Fast mode pricing is flat across the full 1M token context window.

When you switch into fast mode mid-conversation, you pay the full fast mode uncached input token price for the entire conversation context. This costs more than if you had enabled fast mode from the start.

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

| Setting                | Effect                                                                           |
| ---------------------- | -------------------------------------------------------------------------------- |
| **Fast mode**          | Same model quality, lower latency, higher cost                                   |
| **Lower effort level** | Less thinking time, faster responses, potentially lower quality on complex tasks |

You can combine both: use fast mode with a lower [effort level](/en/model-config#adjust-effort-level) for maximum speed on straightforward tasks.

## Requirements

Fast mode requires all of the following:

* **Not available on third-party cloud providers**: fast mode is not available on Amazon Bedrock, Google Vertex AI, or Microsoft Azure Foundry. Fast mode is available through the Anthropic Console API and for Claude subscription plans using extra usage.
* **Extra usage enabled**: your account must have extra usage enabled, which allows billing beyond your plan's included usage. For individual accounts, enable this in your [Console billing settings](https://platform.claude.com/settings/organization/billing). For Team and Enterprise, an admin must enable extra usage for the organization.

<Note>
  Fast mode usage is billed directly to extra usage, even if you have remaining usage on your plan. This means fast mode tokens do not count against your plan's included usage and are charged at the fast mode rate from the first token.
</Note>

* **Admin enablement for Team and Enterprise**: fast mode is disabled by default for Team and Enterprise organizations. An admin must explicitly [enable fast mode](#enable-fast-mode-for-your-organization) before users can access it.

<Note>
  If your admin has not enabled fast mode for your organization, the `/fast` command will show "Fast mode has been disabled by your organization."
</Note>

### Enable fast mode for your organization

Admins can enable fast mode in:

* **Console** (API customers): [Claude Code preferences](https://platform.claude.com/claude-code/preferences)
* **Claude AI** (Team and Enterprise): [Admin Settings > Claude Code](https://claude.ai/admin-settings/claude-code)

Another option to disable fast mode entirely is to set `CLAUDE_CODE_DISABLE_FAST_MODE=1`. See [Environment variables](/en/env-vars).

### Require per-session opt-in

By default, fast mode persists across sessions: if a user enables fast mode, it stays on in future sessions. Administrators on [Team](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_teams#team-&-enterprise) or [Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_enterprise) plans can prevent this by setting `fastModePerSessionOptIn` to `true` in [managed settings](/en/settings#settings-files) or [server-managed settings](/en/server-managed-settings). This causes each session to start with fast mode off, requiring users to explicitly enable it with `/fast`.

```json theme={null}
{
  "fastModePerSessionOptIn": true
}
```

This is useful for controlling costs in organizations where users run multiple concurrent sessions. Users can still enable fast mode with `/fast` when they need speed, but it resets at the start of each new session. The user's fast mode preference is still saved, so removing this setting restores the default persistent behavior.

## Handle rate limits

Fast mode has separate rate limits from standard Opus. Fast mode for Opus 4.6 and Opus 4.7 share the same rate limit pool: usage on either model draws from the same limits. When you hit the fast mode rate limit or run out of extra usage:

1. Fast mode automatically falls back to standard speed on the same Opus version
2. The `↯` icon turns gray to indicate cooldown
3. You continue working at standard speed and pricing
4. When the cooldown expires, fast mode automatically re-enables

To disable fast mode manually instead of waiting for cooldown, run `/fast` again.

## Research preview

Fast mode is a research preview feature. This means:

* The feature may change based on feedback
* Availability and pricing are subject to change
* The underlying API configuration may evolve

Report issues or feedback through your usual Anthropic support channels.

## See also

* [Model configuration](/en/model-config): switch models and adjust effort levels
* [Manage costs effectively](/en/costs): track token usage and reduce costs
* [Status line configuration](/en/statusline): display model and context information
