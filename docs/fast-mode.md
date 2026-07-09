> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Speed up responses with fast mode

> Get faster Opus responses in Claude Code by toggling fast mode.

<Note>
  Fast mode is in [research preview](#research-preview). The feature, pricing, and availability may change based on feedback.
</Note>

Fast mode is a high-speed configuration for Claude Opus, making the model up to 2.5x faster at a higher cost per token. Toggle it on with `/fast` when you need speed for interactive work like rapid iteration or live debugging, and toggle it off when cost matters more than latency.

Fast mode is not a different model. It uses Claude Opus with a different API configuration that prioritizes speed over cost efficiency. You get identical quality and capabilities with faster responses. Fast mode is supported on Opus 4.8 and Opus 4.7. It is not available on Sonnet, Haiku, or other models.

<Warning>
  Fast mode for Opus 4.7 is deprecated as of June 25, 2026, and will be removed on July 24, 2026. After removal, fast mode requests on Opus 4.7 return an error and do not fall back to standard Opus 4.7. Migrate to Opus 4.8 to keep the speedup.
</Warning>

<Note>
  Fast mode requires Claude Code v2.1.36 or later. Check your version with `claude --version`.
</Note>

What to know:

* Use `/fast` to toggle on fast mode in the Claude Code CLI. Fast mode is not supported in the VS Code extension.
* Fast mode pricing per MTok input/output is \$10/\$50 on Opus 4.8 and \$30/\$150 on Opus 4.7.
* Available to all Claude Code users on subscription plans (Pro/Max/Team/Enterprise) and Claude Console.
* For Claude Code users on subscription plans (Pro/Max/Team/Enterprise), fast mode is available via usage credits only and not included in the subscription rate limits.

## Toggle fast mode

Toggle fast mode in either of these ways:

* Type `/fast` and press Tab to toggle on or off
* Set `"fastMode": true` in your [user settings file](/en/settings)

By default, fast mode you turn on in an interactive session persists across sessions. {/* min-version: 2.1.205 */}In [non-interactive mode](/en/headless), with the `-p` flag, `/fast` works only in a session launched with fast mode in its [`--settings`](/en/cli-reference#cli-flags) value, for example `claude -p --settings '{"fastMode": true}'`; the toggle then applies to that session only and isn't saved as your default, and in any other non-interactive session the command reports that fast mode isn't available. Administrators can configure fast mode to reset each session. See [require per-session opt-in](#require-per-session-opt-in) for details.

For the best cost efficiency, enable fast mode at the start of a session rather than switching mid-conversation. See [understand the cost tradeoff](#understand-the-cost-tradeoff) for details.

When you enable fast mode:

* If you're on a different model, Claude Code automatically switches to Opus
* You'll see a confirmation message: "Fast mode ON"
* A small `↯` icon appears next to the prompt while fast mode is active
* Run `/fast` again at any time to check whether fast mode is on or off

When you disable fast mode with `/fast` again, you remain on Opus. The model does not revert to your previous model. To switch to a different model, use `/model`.

Opus 4.8 is the fast mode default in Claude Code v2.1.154 and later. On v2.1.142 through v2.1.153, fast mode defaults to Opus 4.7.

## Understand the cost tradeoff

Fast mode has higher per-token pricing than standard Opus, with the multiplier varying by model:

| Model    | Input (MTok) | Output (MTok) |
| -------- | ------------ | ------------- |
| Opus 4.8 | \$10         | \$50          |
| Opus 4.7 | \$30         | \$150         |

Fast mode pricing is flat across the full 1M token context window. For the standard Opus rate to compare against, see the [Claude pricing reference](https://platform.claude.com/docs/en/about-claude/pricing).

The first time you enable fast mode in a conversation, you pay the full fast mode uncached input token price for the entire conversation context. The deeper into a conversation you are, the more this costs, so enabling fast mode from the start is cheaper. The cost applies once per conversation, so toggling fast mode off and on again later does not repeat it. For the mechanism, see [how fast mode interacts with the prompt cache](/en/prompt-caching#turning-on-fast-mode).

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

* **Anthropic API or subscription only**: fast mode is available through the Anthropic Console API and for Claude subscription plans using usage credits. It is not available on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or Claude Platform on AWS.
* **Usage credits turned on**: your account must have usage credits turned on, which allows billing beyond your plan's included usage. For individual accounts, turn this on in your [Console billing settings](https://platform.claude.com/settings/organization/billing). For Team and Enterprise, an admin must turn on usage credits for the organization.

<Note>
  Fast mode usage draws directly from usage credits, even if you have remaining usage on your plan. This means fast mode tokens do not count against your plan's included usage and are charged at the fast mode rate from the first token.
</Note>

* **Owner enablement for Team and Enterprise**: fast mode is disabled by default for Team and Enterprise organizations. An Owner must explicitly [enable fast mode](#enable-fast-mode-for-your-organization) before users can access it.

<Note>
  If fast mode has not been enabled for your organization, the `/fast` command will show "Fast mode has been disabled by your organization." If your organization's [`availableModels`](/en/model-config#restrict-model-selection) allowlist excludes the fast-mode Opus model, `/fast` is refused with "is not in your organization's allowed models". The exception is a session already running on an allowed Opus model that supports fast mode: `/fast` enables fast mode on your current model instead of switching models.
</Note>

### Enable fast mode for your organization

Where you enable fast mode depends on which product your organization uses:

* **Console** (API customers): an admin enables it in [Claude Code preferences](https://platform.claude.com/claude-code/preferences)
* **Claude AI** (Team and Enterprise): an Owner enables it at [Admin Settings > Claude Code](https://claude.ai/admin-settings/claude-code)

Another option to disable fast mode entirely is to set `CLAUDE_CODE_DISABLE_FAST_MODE=1`. See [Environment variables](/en/env-vars).

### Require per-session opt-in

By default, fast mode a user turns on in an interactive session persists across sessions: it stays on in future sessions. Administrators on [Team](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_teams#team-&-enterprise) or [Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_enterprise) plans can prevent this by setting `fastModePerSessionOptIn` to `true` in [managed settings](/en/settings#settings-files) or [server-managed settings](/en/server-managed-settings). This causes each session to start with fast mode off, requiring users to explicitly enable it with `/fast`.

```json theme={null}
{
  "fastModePerSessionOptIn": true
}
```

This is useful for controlling costs in organizations where users run multiple concurrent sessions. Users can still enable fast mode with `/fast` when they need speed, but it resets at the start of each new session. The user's fast mode preference is still saved, so removing this setting restores the default persistent behavior.

## Handle rate limits

Fast mode has separate rate limits from standard Opus. Fast mode on Opus 4.8 and Opus 4.7 shares the same rate limit pool: usage on either of them draws from the same limits. When you hit the fast mode rate limit or run out of usage credits:

1. Fast mode automatically falls back to standard speed
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
