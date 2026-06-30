> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Escalate hard decisions with the advisor tool

> Pair your main model with a stronger advisor model that Claude consults at key moments during a task.

{/* plan-availability: feature=advisor providers=anthropic */}

<Note>
  The advisor tool is experimental and requires Claude Code v2.1.98 or later with the Anthropic API. It is not available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry. Behavior, pricing, and availability may change.
</Note>

The advisor tool lets Claude consult a second, typically stronger model at key moments during a task, such as before committing to an approach, when stuck on a recurring error, or before declaring a task complete. The advisor receives the full conversation, including every tool call and result, and returns guidance that Claude applies before continuing.

The advisor runs server-side on Anthropic's infrastructure as a [server tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool), available to both subscription and API-billed accounts. You choose which model acts as the advisor, and Claude decides when to call it.

This page covers how to enable the advisor, which model pairings are accepted, what Claude shows during a consultation, and how advisor usage is billed.

## When to use the advisor

The advisor fits long, multi-step tasks where most turns are routine but plan quality determines the outcome. Examples include large refactors, debugging sessions where an error keeps recurring, and tasks you want independently checked before Claude declares them done.

It adds less value on short tasks where there is little to plan, or on work where every turn needs the strongest model. For those, [switch the main model](/en/model-config#setting-your-model) instead, or see [how the advisor compares with opusplan and subagents](#compare-with-related-features) for other ways to get a second opinion.

## Enable the advisor

You can set the advisor model in three ways:

* **`/advisor` command**: set or change the advisor mid-session and save it as your default
* **`advisorModel` setting**: configure a persistent default in your [settings file](/en/settings)
* **`--advisor` flag**: set the advisor for a single session at launch

If any of these sets an advisor model, the advisor is enabled for sessions whose main model [supports it](#choose-an-advisor-model). To stop using it, see [Turn the advisor off](#turn-the-advisor-off).

<Note>
  To use Fable 5 as the advisor, you need Claude Code v2.1.170 or later and [Fable 5 access](/en/model-config#work-with-fable-5) for your organization.
</Note>

### Use the `/advisor` command

Run `/advisor` without arguments to open a picker listing the available advisor models, or pass the model directly:

```
/advisor opus
```

Your selection is saved to `advisorModel` in your user settings and persists across sessions. If your organization's [`availableModels`](/en/model-config#restrict-model-selection) allowlist excludes the saved advisor model, the advisor is not invoked until you pick an allowed model with `/advisor`. If your current main model does not support the advisor, the selection is still saved and activates when you switch to a [compatible main model](#choose-an-advisor-model) with [`/model`](/en/model-config#setting-your-model).

### Set `advisorModel` in settings

To configure the advisor as a default without opening a session, set it in your settings file:

```json theme={null}
{
  "advisorModel": "opus"
}
```

### Use the `--advisor` flag

To set the advisor for a single session without changing your saved setting, launch with the flag:

```bash theme={null}
claude --advisor opus
```

The flag takes precedence over the `advisorModel` setting for that session. It exits with an error if the session's main model does not support the advisor, or if the requested advisor model is excluded by your organization's [`availableModels`](/en/model-config#restrict-model-selection) allowlist.

## Choose an advisor model

The advisor must be at least as capable as the main model. The accepted advisors for each main model are:

| Main model                                      | Accepted advisors                                | Notes                                                 |
| ----------------------------------------------- | ------------------------------------------------ | ----------------------------------------------------- |
| Haiku 4.5                                       | Fable, Opus, Sonnet                              | Haiku can call the advisor but cannot act as one      |
| Sonnet 4.6                                      | Fable, Opus, Sonnet                              |                                                       |
| Sonnet 5                                        | Fable, Opus, Sonnet 5                            | A Sonnet 4.6 advisor is rejected                      |
| Opus 4.6 or later                               | Fable, Opus at or above the main model's version | An Opus 4.7 main with an Opus 4.6 advisor is rejected |
| Fable 5 ({/* min-version: 2.1.170 */}v2.1.170+) | Fable                                            | An Opus or Sonnet advisor is rejected                 |

Fable 5 requires Claude Code v2.1.170 or later and Fable 5 access, whether it acts as the main model or the advisor.

Set the advisor as `opus`, `sonnet`, or `fable`. These aliases resolve to the latest version of each model. You can also pass a full model ID such as `claude-opus-4-8`.

Subagents inherit the configured advisor and apply the same pairing check against their own model.

Claude Code validates the pairing before sending a request:

* If the advisor is less capable than the main model, the advisor is not attached to the main model's requests. The `/advisor` command output and a notification show this. Subagents whose own model satisfies the pairing may still use the advisor.
* If the main model or the advisor is a model Claude Code does not recognize, the advisor is not attached.

### Common model pairings

Any accepted pairing works. These combinations balance cost against capability in different ways:

| Pairing                      | When to use                                                                                                                                                              |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Sonnet main + Opus advisor   | Sonnet handles routine work and escalates planning, ambiguous failures, and completion checks to Opus                                                                    |
| Sonnet main + Fable advisor  | Fable 5 guidance at decision points without running Fable 5 throughout. Requires v2.1.170 or later and Fable 5 access                                                    |
| Haiku main + Opus advisor    | Lowest-cost main model with strong planning. Expect higher cost than Haiku alone but lower than switching the main model to Sonnet or Opus                               |
| Opus main + Opus advisor     | A second Opus reviews the first. Useful for high-stakes tasks where an independent check matters more than cost                                                          |
| Fable main + Fable advisor   | Highest-capability pairing when Fable 5 is available (v2.1.170+). Fable is a higher tier than Opus and Sonnet, so it is the only accepted advisor for a Fable main model |
| Sonnet main + Sonnet advisor | A lower-cost second opinion for catching routine oversights                                                                                                              |

## When Claude consults the advisor

Claude decides when to call the advisor. It tends to consult before committing to an approach, when an error keeps recurring, and before declaring a task done, but the timing is model-driven rather than rule-based.

You can ask for a consultation in your prompt the same way you would request any tool, for example `consult the advisor before you continue`. There is no setting to cap or force advisor calls; if you want Claude to consult more or less often during a task, say so in your instructions.

## What you see during a session

When Claude calls the advisor, the transcript shows an `Advising` line with the advisor model name while the call is in progress. When the result returns, the line confirms that the advisor has reviewed the conversation. Press `Ctrl+O` to expand it and read the advisor's full guidance.

Claude generally follows the advisor's guidance, but adapts when its own evidence contradicts a specific claim: if a recommended step fails when tried, or the file contents contradict the advice, Claude surfaces the conflict rather than following the guidance unconditionally.

The advisor always receives the full conversation, and Claude controls the timing. For more control or a different configuration, see [how the advisor compares with subagents and opusplan](#compare-with-related-features).

## Cost

Each advisor call sends the conversation to the advisor model, so it consumes tokens at the advisor model's rates in addition to your main model's usage. With API billing, advisor tokens are charged at the advisor model's input and output rates. On subscription plans, advisor usage counts toward your plan's usage limits.

Claude calls the advisor at decision points rather than on every turn, so pairing a faster main model with a stronger advisor typically costs less than running the stronger model throughout. Advisor usage counts toward the session totals shown by [`/usage`](/en/costs#track-your-costs).

For how advisor tokens are reported in API responses, see [Usage and billing](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool#usage-and-billing) in the Claude API documentation.

## Impact on prompt caching

Enabling or disabling the advisor mid-session does not invalidate your main model's [prompt cache](/en/prompt-caching). Unlike [changing model or effort level](/en/prompt-caching#actions-that-invalidate-the-cache), toggling `/advisor` keeps the cached prefix intact, and the advisor's returned guidance is cached as part of the transcript on later turns.

The advisor model's own read of the conversation is not cached. Each advisor call processes the full transcript anew, with no reuse between calls.

## Requirements

The advisor tool requires all of the following:

* **Claude Code v2.1.98 or later**: run `claude update` to upgrade.
* **Anthropic API only**: the advisor is a server-executed tool. It is not available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry. Through an [LLM gateway](/en/llm-gateway) configured with `ANTHROPIC_BASE_URL`, availability depends on whether the gateway forwards the request intact to the Anthropic API.
* **Supported main model**: Opus 4.6 or later, Sonnet 4.6 or later, or Haiku 4.5. {/* min-version: 2.1.170 */}Fable 5 also qualifies on Claude Code v2.1.170 or later.

## Turn the advisor off

To stop using the advisor and clear your saved `advisorModel`, run `/advisor off` or choose **No advisor** in the `/advisor` picker:

```
/advisor off
```

To disable the advisor tool entirely, including the `/advisor` command and the `--advisor` flag, set `CLAUDE_CODE_DISABLE_ADVISOR_TOOL=1`. See [Environment variables](/en/env-vars).

## Compare with related features

The advisor is one of several ways to combine model strengths. Pick based on when you want a second model involved.

| Approach                                                    | When the stronger model runs                                                                                                           | How it starts                                |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| Advisor tool                                                | At decision points mid-task                                                                                                            | Claude calls it when it needs guidance       |
| [`opusplan`](/en/model-config#opusplan-model-setting)       | During plan mode when [allowed by `availableModels`](/en/model-config#restrict-model-selection), then switches to Sonnet for execution | You enter plan mode                          |
| [Subagents](/en/sub-agents#choose-a-model) with `model` set | For the entire delegated subtask                                                                                                       | Claude delegates, or you invoke the subagent |
| [`/model`](/en/model-config#setting-your-model)             | For all subsequent turns                                                                                                               | You switch models                            |

## See also

* [Model configuration](/en/model-config): switch models, set effort levels, and use `opusplan`
* [Manage costs effectively](/en/costs): track token usage across models
* [Advisor tool in the Claude API](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool): understand the underlying server tool, or use it directly from the Messages API
* [The advisor strategy](https://claude.com/blog/the-advisor-strategy): why pairing a fast main model with a stronger advisor works
