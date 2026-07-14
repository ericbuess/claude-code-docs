> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Model configuration

> Learn about the Claude Code model configuration, including model aliases like `opusplan`

## Available models

For the `model` setting in Claude Code, you can configure either:

* A **model alias**
* A **model name**
  * Anthropic API: a full **[model name](https://platform.claude.com/docs/en/about-claude/models/overview)**
  * Amazon Bedrock: an inference profile ARN
  * Microsoft Foundry: a deployment name
  * Google Cloud's Agent Platform: a version name

<Note>
  `ANTHROPIC_BASE_URL` changes where requests are sent, not which model answers them. To route Claude through an LLM gateway, see [LLM gateways](/en/llm-gateway).
</Note>

### Model aliases

Model aliases provide a convenient way to select model settings without
remembering exact version numbers:

| Model alias      | Behavior                                                                                                                                                                                                                                                                                                                                 |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**    | Special value that clears any model override and reverts to the recommended model for your account type, or to the [organization default model](#organization-default-model) when an admin has set one. Not itself a model alias                                                                                                         |
| **`best`**       | Uses Fable 5 where your organization has access to it, otherwise the latest Opus model                                                                                                                                                                                                                                                   |
| **`fable`**      | Uses Claude Fable 5 for your hardest and longest-running tasks                                                                                                                                                                                                                                                                           |
| **`sonnet`**     | Uses the latest Sonnet model for daily coding tasks                                                                                                                                                                                                                                                                                      |
| **`opus`**       | Uses the latest Opus model for complex reasoning tasks                                                                                                                                                                                                                                                                                   |
| **`haiku`**      | Uses the fast and efficient Haiku model for simple tasks                                                                                                                                                                                                                                                                                 |
| **`sonnet[1m]`** | Uses Sonnet with a [1 million token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#context-window-sizes-by-model) for long sessions. No effect when `sonnet` already resolves to Sonnet 5 with its native 1M window; behind an [LLM gateway](/en/llm-gateway), selects the 1M window for Sonnet 5 |
| **`opus[1m]`**   | Uses Opus with a [1 million token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#context-window-sizes-by-model) for long sessions                                                                                                                                                                 |
| **`opusplan`**   | Special mode that uses `opus` during plan mode, then switches to `sonnet` for execution                                                                                                                                                                                                                                                  |

The version that the `opus` and `sonnet` aliases resolve to depends on the provider:

| Provider                                             | `opus`   | `sonnet`   |
| :--------------------------------------------------- | :------- | :--------- |
| Anthropic API                                        | Opus 4.8 | Sonnet 5   |
| [Claude Platform on AWS](/en/claude-platform-on-aws) | Opus 4.8 | Sonnet 4.6 |
| Amazon Bedrock, Google Cloud's Agent Platform        | Opus 4.8 | Sonnet 4.5 |
| Microsoft Foundry                                    | Opus 4.6 | Sonnet 4.5 |

Where an alias resolves to an older model, newer models are available by selecting the full model name explicitly or setting `ANTHROPIC_DEFAULT_OPUS_MODEL` or `ANTHROPIC_DEFAULT_SONNET_MODEL`.

{/* min-version: 2.1.207 */}Before v2.1.207, `opus` resolved to Opus 4.7 on Claude Platform on AWS and to Opus 4.6 on Amazon Bedrock and Google Cloud's Agent Platform.

Aliases point to the recommended version for your provider and update over time. To pin to a specific version, use the full model name, for example `claude-opus-4-8`, or set the corresponding environment variable like `ANTHROPIC_DEFAULT_OPUS_MODEL`.

<Note>
  Sonnet 5 requires Claude Code v2.1.197 or later. Opus 4.8 requires v2.1.154 or later. Run `claude update` to upgrade.
</Note>

### Work with Fable 5

[Claude Fable 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) is the most capable model in Claude Code, suited to tasks larger than a single sitting. It sustains long autonomous sessions, investigates before acting, and verifies its work more often than smaller models.

Fable 5 is not the default model. Select it with `/model fable`. Requests that its safety classifiers flag, most often in cybersecurity and biology domains, trigger [automatic model fallback](#automatic-model-fallback).

To get the most from Fable 5:

* **Describe the outcome, not the steps**: hand it the result you want and let it plan the path. To keep it working until that outcome holds, [set a goal](/en/goal).
* **Hand it ambiguous problems**: root-cause investigations, outage debugging, and architecture decisions are where the extra investigation and verification pay off.
* **Skip the verification reminders**: it verifies its own work with less prompting, so reminders to test or check are usually unnecessary.
* **Size up larger tasks**: give it work you would normally break into pieces. It holds long sessions without losing the thread.

<Note>
  Fable 5 requires Claude Code v2.1.170 or later. Older versions do not show Fable 5 in the model picker and cannot select it. Run `claude update` to upgrade. Fable 5 is not available under [zero data retention](/en/zero-data-retention), where the `/model` picker either omits it or shows it disabled.
</Note>

### Setting your model

You can configure your model in several ways, listed in order of priority:

1. **During session**: use `/model <alias|name>` to switch immediately, or run `/model` with no argument to open the picker. The picker asks for confirmation when the conversation has prior output, since the next response re-reads the full history without cached context
2. **At startup**: launch with `claude --model <alias|name>`
3. **Environment variable**: set `ANTHROPIC_MODEL=<alias|name>`
4. **Settings**: configure permanently in your settings file using the `model` field

As of v2.1.153, `/model` saves your choice as the default for new sessions by writing the `model` field in your user settings. In the picker:

* `Enter`: switch model and save as your default
* `s`: switch model for this session only

Typing `/model <name>` directly behaves like `Enter`. {/* min-version: 2.1.205 */}A model set with `/model` in [non-interactive mode](/en/headless), with the `-p` flag, applies to the current session only and isn't saved as your default. Project and managed settings still take precedence and reapply on the next launch. {/* min-version: 2.1.196 */}An [organization default model](#organization-default-model) that your admin has configured to override user selection also reapplies on the next launch.

In v2.1.144 through v2.1.152, `/model` applied to the current session only and `d` in the picker saved a default.

The `--model` flag and `ANTHROPIC_MODEL` environment variable apply only to the session you launch with them. To run different models in different terminals at the same time, launch each one with its own `--model` flag rather than switching with `/model`.

Prices in the `/model` picker appear when Claude Code talks to the Anthropic API, directly or through an [LLM gateway](/en/llm-gateway) that proxies it, and the price on a row is the price of the model that row selects. On [third-party providers](/en/third-party-integrations) such as Amazon Bedrock and on the [Claude apps gateway](/en/claude-apps-gateway), your provider or gateway determines what you pay, so picker rows show no price. The price is a display label only; it doesn't affect which model a row selects or what your provider bills. Before v2.1.206, [Claude Platform on AWS](/en/claude-platform-on-aws) and gateway sessions showed Anthropic list prices, and a row could show the price of a different model than the one it selected.

Resumed sessions started with `claude --resume`, `--continue`, or the `/resume` picker keep the model they were using when the transcript was saved, regardless of the current `model` setting. If the restored model has been retired or is excluded by [`availableModels`](#restrict-model-selection), the session falls through to the normal precedence order. This prevents another session's `/model` choice from changing the model on resume.

A model you pick for the new launch with `--model` or `ANTHROPIC_MODEL` still takes precedence over the restored model. {/* min-version: 2.1.195 */}As of v2.1.195, so does an [`ANTHROPIC_DEFAULT_OPUS_MODEL`](#environment-variables) family variable.

When the active model at startup comes from project or managed settings rather than your own selection, the startup header shows which settings file set it. Run `/model` to override; the project or managed setting reapplies on the next launch.

When a model switch is requested through the [Agent SDK](/en/agent-sdk/overview) `setModel()` method or by an app such as the [Desktop app](/en/desktop) that runs the Claude Code CLI for you, Claude Code checks that the string is one it recognizes before saving it. This check requires Claude Code v2.1.200 or later. On the Anthropic API, Claude Code recognizes:

* a model alias
* an entry from the `/model` picker
* any name that starts with `claude-`
* a value you configured yourself as a [custom model option](#add-a-custom-model-option) or in [`modelOverrides`](#override-model-ids-per-version)

Claude Code rejects an unrecognized string with `Model "<name>" is not a recognized model id.` and the session keeps its current model, instead of saving the string and failing on the next request. See [the error reference](/en/errors#model-is-not-a-recognized-model-id) for recovery steps.

The check runs only on the Anthropic API. On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, [Claude Platform on AWS](/en/claude-platform-on-aws), and behind an [LLM gateway](/en/llm-gateway) or a custom `ANTHROPIC_BASE_URL`, your provider or gateway defines the model names, so Claude Code passes any string through without checking it. The check also doesn't cover the `--model` flag, the `ANTHROPIC_MODEL` environment variable, or the `model` setting; a mistyped value there produces [There's an issue with the selected model](/en/errors#theres-an-issue-with-the-selected-model) on the first request instead.

When the requested model has a scheduled retirement date or is automatically remapped to a newer version, Claude Code shows a warning that names the requested model. Interactive sessions show it as a startup notice. From v2.1.182, the same warning is written to stderr in [non-interactive mode](/en/headless) when using the default text output format. The check also covers a `model` set in [subagent frontmatter](/en/sub-agents). The stderr warning is suppressed for `--output-format json` and `stream-json`; read the actual model from the `modelUsage` field of the [result message](/en/headless#get-structured-output) instead.

Example usage:

```bash theme={null}
# Start with Opus
claude --model opus

# Switch to Sonnet during session
/model sonnet
```

Example settings file:

```json theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## Restrict model selection

Enterprise administrators can use `availableModels` in [managed or policy settings](/en/settings#settings-files) to restrict which models users can select. Entries match a model family such as `sonnet`, a version prefix such as `claude-sonnet-4-5`, or a full model ID such as `claude-sonnet-4-5-20250929`.

When `availableModels` is set, the allowlist applies everywhere a user can specify a model:

* **Main session model**: `/model`, the `--model` flag, the `ANTHROPIC_MODEL` environment variable, the `model` setting, and the model restored when [resuming a session](#setting-your-model)
* **Alias resolution**: {/* min-version: 2.1.176 */}the `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`, and `ANTHROPIC_DEFAULT_FABLE_MODEL` environment variables cannot redirect an allowed alias to a model outside the list
* **Fast mode**: {/* min-version: 2.1.176 */}`/fast` refuses to toggle when it would implicitly switch to an Opus model outside the list, with the message "is not in your organization's allowed models"
* **Subagent models**: the `model` field in [subagent](/en/sub-agents#choose-a-model) frontmatter, the Agent tool's `model` parameter, `CLAUDE_CODE_SUBAGENT_MODEL`, and, on v2.1.197 and earlier, the model picker in the `/agents` wizard {/* max-version: 2.1.197 */}
* **Skill and command models**: the `model` frontmatter in [skills and commands](/en/skills)
* **Advisor model**: the configured [`advisorModel`](/en/advisor) setting and the `--advisor` flag
* **Background agent model**: the model selected in the [dispatch picker](/en/agent-view)

On the Anthropic API and [Claude Platform on AWS](/en/claude-platform-on-aws), a model family alias, `opus`, `sonnet`, `haiku`, or `fable`, resolves to the newest version of its family that the allowlist permits. When the allowlist pins specific versions, for example `["sonnet", "claude-opus-4-6"]`, both `/model opus` and `--model opus` select Claude Opus 4.6, the newest permitted Opus, and show a notice naming both the requested and substituted models. Before v2.1.205, an alias whose newest released version was outside the list was rejected or replaced like any other blocked selection, even when the list permitted an older version.

Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and [Mantle](/en/amazon-bedrock#use-the-mantle-endpoint) use provider-specific deployment IDs rather than Anthropic model IDs, so a blocked alias there follows the rejection and replacement behavior below.

Claude Code handles any other blocked selection according to where the model was set:

* **`/model`**: the switch is rejected with an error
* **`--model` flag, `ANTHROPIC_MODEL`, or the `model` setting**: the value is replaced at startup with a warning naming both the requested and substituted models, and the session starts on the default model
* **Subagent, skill, or command override**: the override falls back to the inherited or default model rather than failing the request
* **`advisorModel` setting**: the advisor is disabled for the session
* **`--advisor` flag**: Claude Code exits with an error at launch

Excluded models are hidden from the `/model` picker. {/* min-version: 2.1.199 */}A full model ID in the list that has no built-in picker row, such as an older version that the list pins, appears in the `/model` picker as its own labeled row. Before v2.1.199, such an ID was selectable only by typing `/model <id>`.

Model changes that Claude Code makes on your behalf are checked the same way:

* **[Fallback model chains](#fallback-model-chains)**: elements outside the allowlist are dropped
* **Plan-mode upgrades**: on the Anthropic API and Claude Platform on AWS, an upgrade such as [`opusplan`](#opusplan-model-setting) to an excluded model uses the newest permitted version of the upgrade family. On providers with provider-specific model IDs, and when no version is permitted, the upgrade is skipped and planning continues on the session's model
* **[Automatic model fallback](#automatic-model-fallback)**: a fallback whose target is excluded does not run, so the flagged request ends with a refusal instead
* **[Fast mode](/en/fast-mode)**: enabling fast mode is refused when the model the session would run on afterward is outside the allowlist

```json theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### Surface coverage

Every surface enforces the allowlist it receives. Which delivery mechanism reaches each surface differs:

| Delivery mechanism                                                            | CLI and IDE | Desktop local sessions | Web, mobile, and cloud sessions | Agent SDK and non-interactive | Cowork                  |
| :---------------------------------------------------------------------------- | :---------- | :--------------------- | :------------------------------ | :---------------------------- | :---------------------- |
| [Server-managed settings](/en/server-managed-settings) from the admin console | Enforced    | Enforced               | Enforced                        | Enforced                      | Not delivered           |
| [MDM or managed settings files](/en/settings#settings-files)                  | Enforced    | Enforced               | Not delivered                   | Enforced                      | Enforced where deployed |

* Cloud sessions, on [Claude Code on the web](/en/claude-code-on-the-web) or in the Desktop app, run on Anthropic-managed VMs: settings deployed to your device do not reach them, so deliver the allowlist through server-managed settings. A mid-session model switch in a cloud session is rejected when the requested model is excluded by the allowlist. Server-side rejection at session creation applies to [organization model restrictions](#organization-model-restrictions), not the `availableModels` settings key.
* Cowork, the agentic-work tab in the Claude Desktop app, is not a Claude Code surface and does not receive server-managed settings by design. A managed settings file applies to Cowork sessions when it is present where the session runs; remote Cowork sessions run on Anthropic-managed VMs, where a device-deployed file is not present.
* Sessions on [third-party providers](/en/server-managed-settings#platform-availability) such as Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and [Claude Platform on AWS](/en/claude-platform-on-aws) do not receive server-managed settings, so deliver the allowlist through MDM or managed settings files there.
* Server-managed delivery also requires the session to authenticate with an organization login or a directly configured API key. Fleets that generate keys only through an [`apiKeyHelper`](/en/settings#available-settings) script should deliver the allowlist through MDM or managed settings files.
* The Desktop Code tab also hosts [SSH sessions](/en/desktop#ssh-sessions), which read the managed settings file from the remote host they run on. See [Desktop managed settings](/en/desktop#managed-settings).
* The model pickers on claude.ai and in the Desktop app hide or grey out models excluded by your organization's allowlist. The picker state is a convenience for users; enforcement happens in the session.

### Default model behavior

The Default option in the model picker is not affected by `availableModels` unless [`enforceAvailableModels`](#enforce-the-allowlist-for-the-default-model) is also set. On its own, `availableModels` leaves Default available, resolving to the system's [runtime default](#default-model-setting) for the account. If that default is a model you intend to restrict, set `enforceAvailableModels` as well.

An empty `availableModels` array never engages the Default-model enforcement: with `availableModels: []`, named model selections are blocked but the Default model for the account type remains usable regardless of `enforceAvailableModels`.

### Enforce the allowlist for the Default model

Set `enforceAvailableModels: true` alongside a non-empty `availableModels` in managed settings to extend the allowlist to the Default option. This requires Claude Code v2.1.175 or later.

```json theme={null}
{
  "availableModels": ["sonnet", "haiku"],
  "enforceAvailableModels": true
}
```

The Default option resolves to the account-type default, or to the [organization default model](#organization-default-model) when an admin has set one. When that model is not in the allowlist, the Default option instead resolves to the first `availableModels` entry that names an allowed, available model, and the `/model` picker's Default row shows that model. This applies everywhere the default is reached: session startup, selecting Default in `/model`, the `"default"` keyword in [fallback model chains](#fallback-model-chains), and the fallback used when an excluded selection is dropped.

`enforceAvailableModels` has no effect when `availableModels` is unset or empty: with `availableModels: []`, the Default model for the account type remains usable, so the setting cannot lock users out of every model. When `availableModels` is non-empty but no entry resolves to an allowed and available model, enforcement is skipped and Default resolves to the account-type default, with a warning visible only under `--debug`. Keep at least one guaranteed-available entry in the list to avoid this.

Deploy both keys in the [highest-precedence managed source](/en/settings#settings-precedence): admin-deployed managed sources do not merge, so a pair placed in a managed settings file is ignored when the admin console delivers any settings.

### Control the model users run on

The `model` setting is an initial selection, not enforcement. It sets which model is active when a session starts, but users can still open `/model` and pick Default, which resolves to the system's [runtime default](#default-model-setting) regardless of what `model` is set to, unless [`enforceAvailableModels`](#enforce-the-allowlist-for-the-default-model) redirects it.

To fully control the model experience, combine these settings:

* **`availableModels`**: restricts which named models users can switch to
* **`enforceAvailableModels`**: extends the `availableModels` allowlist to the Default option, so Default cannot resolve to a model outside the list
* **`model`**: sets the initial model selection when a session starts
* **`ANTHROPIC_DEFAULT_SONNET_MODEL`** / **`ANTHROPIC_DEFAULT_OPUS_MODEL`** / **`ANTHROPIC_DEFAULT_HAIKU_MODEL`** / **`ANTHROPIC_DEFAULT_FABLE_MODEL`**: control what the Default option and the `sonnet`, `opus`, `haiku`, and `fable` aliases resolve to

This example starts users on Sonnet 4.5, limits the picker to Sonnet and Haiku, and ensures Default resolves to a model on the allowlist rather than the tier default:

```json theme={null}
{
  "model": "claude-sonnet-4-5",
  "availableModels": ["claude-sonnet-4-5", "haiku"],
  "enforceAvailableModels": true,
  "env": {
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5"
  }
}
```

Without `enforceAvailableModels` or the `env` block, a user who selects Default in the picker would get the latest release for their tier, bypassing the version pin in `model` and `availableModels`. The two settings cover different scopes: `enforceAvailableModels` makes Default obey the allowlist, while the `env` block pins which version a permitted alias such as `sonnet` resolves to. Use `enforceAvailableModels` alone when restricting model families is enough; add the `env` block when you also need to pin a specific version.

### Merge behavior

When the [highest-precedence managed settings source](/en/server-managed-settings#settings-precedence) defines `availableModels`, that list alone applies: entries in user, project, or local settings cannot extend it, and admin-deployed managed sources do not merge with each other, so a list deployed in a managed settings file is ignored when server-managed settings deliver any keys. Otherwise, lists from user, project, and local settings are [concatenated and deduplicated](/en/settings#settings-precedence) like other array settings. {/* min-version: 2.1.175 */}As of Claude Code v2.1.175, the managed list replaces lower-precedence entries; earlier versions merge them.

Within the effective list, an entry naming a specific model in a family, whether a version prefix or a full model ID, disables that family's wildcard entry: `["sonnet", "claude-sonnet-4-5"]` allows only Sonnet 4.5 versions, not every Sonnet model.

### Mantle model IDs

When the [Amazon Bedrock Mantle endpoint](/en/amazon-bedrock#use-the-mantle-endpoint) is enabled, entries in `availableModels` that start with `anthropic.` are added to the `/model` picker as custom options and routed to the Mantle endpoint. This is an exception to the alias matching described in [Pin models for third-party deployments](#pin-models-for-third-party-deployments). The setting still restricts the picker to listed entries, and a Mantle ID embeds a family name, so it counts as a specific entry and disables that family's wildcard: alongside any Mantle IDs, list the version prefixes or full IDs you want to keep selectable. See [Merge behavior](#merge-behavior).

### Organization model restrictions

Organization admins on Claude Enterprise plans restrict which models members can run by disabling individual models in the claude.ai admin console. This restriction is delivered with the account's entitlements when Claude Code authenticates, separate from any `availableModels` list in settings, and the server enforces the same restriction independently when a session is created. Requires Claude Code v2.1.187 or later.

The restriction applies when a member signs in or uses their own API key. Organization-scoped credentials, such as organization service keys, are not tied to a user, so the restriction does not apply to them.

The Claude Console has no model restriction control. Organizations without a Claude Enterprise plan, including those whose members authenticate through the Anthropic API, restrict models with [`availableModels`](#restrict-model-selection) in [managed settings](/en/settings#settings-files) instead, adding [`enforceAvailableModels`](#enforce-the-allowlist-for-the-default-model) to cover the Default option. These settings are enforced by Claude Code itself, not by the server.

A restricted model is hidden from the `/model` picker. Selecting it by name with `--model`, the `ANTHROPIC_MODEL` environment variable, or the `model` setting shows the notice `Model "<name>" is restricted by your organization's settings. Using <model> instead.` and the session starts on an allowed model. Typing `/model <name>` for a restricted model is rejected with `Model '<name>' is restricted by your organization's settings. Run /model to choose a different model.` and the session keeps its current model.

A [model family alias](#restrict-model-selection) such as `opus` resolves to the newest version of its family that the organization permits, with the same substitution notice. `/model <alias>` is rejected only when every version of its family is restricted; an alias set with `--model`, `ANTHROPIC_MODEL`, or the `model` setting is still replaced at startup in that case. Before v2.1.205, a family alias was substituted or rejected based on its newest released version alone, even when an older version was allowed.

Restrictions apply org-wide or per role:

* Disabling a model at the organization level removes it for every member.
* Role-level access grants different models to different custom roles, and a member who holds several roles can use any model that one of their roles grants.
* Haiku models are always available and can't be disabled, so every member keeps at least one usable model.
* An access change takes effect on new requests within about a minute; the `/model` picker reflects it the next time a session starts.

Both restrictions apply together: a model is selectable only when it is permitted by `availableModels` and not restricted by the organization. Organization restrictions are delivered to sessions on the Anthropic API and [LLM gateway](/en/llm-gateway) deployments. Sessions on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and Claude Platform on AWS do not receive them, so use `availableModels` on those providers instead.

## Organization default model

{/* plan-availability: feature=org-default-model plans=enterprise */}

Organization admins on Claude Enterprise plans can set a default model for Claude Code members from the claude.ai admin console, for the whole organization or per custom role. When one is set, the Default option resolves to that model instead of the [account-type default](#default-model-setting). Requires Claude Code v2.1.196 or later.

The Default row in the `/model` picker shows the organization default's name with the label Org default. The label reads Org default whether the admin set the default for the whole organization or for your role. A role default covers members of that custom role and takes precedence over the organization-wide default; when several of your roles set different defaults, the most capable model applies.

The organization default is a starting point, not a restriction, and any other model selection takes precedence over it:

* the `--model` flag and the `ANTHROPIC_MODEL` environment variable
* a `model` value in [managed settings](/en/settings#settings-files) or supplied through `--settings`
* a `model` value in your user, project, or local settings, including a model you save with `/model`

Admins can also configure the organization default to override user selection. With override on, it takes precedence over the `model` value in user, project, and local settings, so a model you save with `/model` applies for the current session and the organization default returns on the next launch. When your selection differs, `/model` shows `Your organization's default (<model>) applies on restart`. The `--model` flag, `ANTHROPIC_MODEL`, managed settings, and `--settings` still take precedence even with override on. Override is available to a limited set of organizations; ask your Anthropic account team about availability.

To limit which models members can select, use [organization model restrictions](#organization-model-restrictions) or [`availableModels`](#restrict-model-selection) instead.

Claude Code reads the organization default once at startup, so a default the admin changes mid-session takes effect on the next launch.

When the organization default doesn't override user selection, the first interactive launch after the admin changes it clears the `model` key from your user settings once, so the new default applies. It changes nothing else in the file, and a model you save with `/model` after that launch is kept.

The organization default passes through the same restriction checks as any other Default model before it is adopted:

* [`availableModels`](#restrict-model-selection) on its own never constrains the Default option, so an organization default outside the allowlist still applies. When [`enforceAvailableModels`](#enforce-the-allowlist-for-the-default-model) is also set, an organization default outside the allowlist is remapped to the first allowlist entry, like any other Default
* an organization default that [organization model restrictions](#organization-model-restrictions) deny for your account is replaced by the newest allowed model in its family, or a lower-cost family when every version of it is restricted
* an organization default that isn't available to your account at all, such as Fable 5 under [zero data retention](/en/zero-data-retention), is skipped, and the Default option resolves to the account-type default

As of v2.1.199, when the organization default is a different model family from your account type's usual default, the `/model` picker keeps a separate row for that usual family, so you can still switch to it for a session. In v2.1.196 through v2.1.198 that row is missing from the picker.

The organization default is delivered to sessions authenticated with the Anthropic API. Sessions on [LLM gateway](/en/llm-gateway) deployments, Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and Claude Platform on AWS don't receive it. To set a default on those deployments, use the `model` key in [managed settings](/en/settings#settings-files) instead.

## Organization effort limits

{/* plan-availability: feature=org-effort-limits plans=enterprise */}

Organization admins on Claude Enterprise plans can set a maximum [effort level](#adjust-effort-level) per model for each custom role, alongside role-level [organization model restrictions](#organization-model-restrictions). Levels above the cap aren't offered in the `/effort` picker, and naming a higher level with `--effort` or `/effort` runs at the cap instead. In interactive sessions and plain-text `--print` runs, a warning names the requested and applied levels; with `json` or `stream-json` output or in background agents, the clamp applies silently. Caps are per model, so switching models can change which levels are available. When several of your roles grant the same model, the least restrictive cap applies. Requires Claude Code v2.1.195 or later.

Effort limits are delivered together with [organization model restrictions](#organization-model-restrictions) and follow the same provider availability: sessions on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and Claude Platform on AWS don't receive them.

## Special model behavior

### `default` model setting

The behavior of `default` depends on your account type:

* **Max, Team Premium, Enterprise pay-as-you-go, and Anthropic API**: defaults to Opus 4.8
* **Claude Platform on AWS, Amazon Bedrock, and Google Cloud's Agent Platform**: defaults to Opus 4.8
* **Pro, Team Standard, and Enterprise subscription seats**: defaults to Sonnet 5
* **Microsoft Foundry**: defaults to Sonnet 4.5

Enterprise pay-as-you-go means an Enterprise organization billed by usage rather than by subscription seat.

{/* min-version: 2.1.207 */}Before v2.1.207, `default` resolved to Opus 4.7 on Claude Platform on AWS and to Sonnet 4.5 on Amazon Bedrock and Google Cloud's Agent Platform.

When an admin has set an [organization default model](#organization-default-model), `default` resolves to that model instead of the account-type default above. Requires Claude Code v2.1.196 or later.

When managed settings [enforce the allowlist for the Default model](#enforce-the-allowlist-for-the-default-model) and the account-type default is not in `availableModels`, `default` resolves to the enforced Default instead of the account-type default above. When both apply, the organization default replaces the account-type default first and enforcement then applies to it: an allowlisted organization default is kept, while one outside the list resolves to the enforced Default.

Fable 5 is not the default model on any account type. Sessions use Fable 5 only after you choose it, with `/model fable`, a `model` setting, or the `best` alias where Fable 5 is available. Choosing it with `/model` saves it as the selected model in your user settings, so later sessions start on Fable 5 until you change models.

### `opusplan` model setting

The `opusplan` model alias provides an automated hybrid approach:

* **In plan mode**: uses `opus` for complex reasoning and architecture decisions
* **In execution mode**: automatically switches to `sonnet` for code generation and implementation

This pairs Opus's reasoning for planning with Sonnet's efficiency for execution.

The plan-mode Opus phase uses the same context window as the `opus` model setting. On subscription tiers where Opus is [automatically upgraded to 1M context](#extended-context), `opusplan` receives the upgrade in plan mode as well. To force 1M context for both phases when you are not on an auto-upgrade tier, set the model to `opusplan[1m]`.

When [`availableModels`](#restrict-model-selection) excludes the newest Opus but permits an older version, for example `["sonnet", "claude-opus-4-6"]`, `opusplan` uses the newest permitted Opus for planning and stays on Sonnet only when every Opus is excluded. A Haiku session that would normally upgrade to Sonnet in plan mode likewise uses the newest permitted Sonnet, and stays on Haiku only when every Sonnet is excluded. Before v2.1.205, plan mode stayed on the session's model whenever the newest version of the upgrade family was excluded, even when the allowlist permitted an older one.

The substitution of an older permitted version applies on the Anthropic API and [Claude Platform on AWS](/en/claude-platform-on-aws). On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and Mantle, whose deployments use provider-specific model IDs, plan mode stays on the session's model whenever the upgrade model is excluded.

For a hybrid approach where Claude decides mid-task when to consult a second model rather than switching at the plan boundary, see the [advisor tool](/en/advisor).

### Fallback model chains

When the primary model is overloaded, unavailable, or returns another non-retryable server error, Claude Code can switch to a fallback model instead of failing the request. Authentication, billing, rate-limit, request-size, and transport errors never trigger a switch; those follow their normal retry and error handling.

Configure one or more fallback models and Claude Code tries them in order, showing a notice when it switches. The switch lasts for the current turn only, so your next message tries the primary model first again. Chains are capped at three models after duplicate removal, and extra entries are ignored.

Set a chain for one session with the `--fallback-model` flag, which accepts a comma-separated list:

```bash theme={null}
claude --fallback-model sonnet,haiku
```

To persist a chain across sessions, set `fallbackModel` in [settings](/en/settings) as an array:

```json theme={null}
{
  "fallbackModel": ["claude-sonnet-5", "claude-haiku-4-5"]
}
```

The `--fallback-model` flag takes precedence over the `fallbackModel` setting. Each element accepts a model name or alias, and `"default"` expands to the default model.

Two cases cause an element to be skipped:

* **Unavailable model**: a model that can't be reached, such as a retired model pinned in settings, is skipped and Claude Code continues to the next element.
* **Outside the allowlist**: an element not permitted by [`availableModels`](#restrict-model-selection) is dropped when the chain is read and never tried.

### Automatic model fallback

This section covers content-based fallback from Fable 5. For availability-based fallback when a model is overloaded or unavailable, see [Fallback model chains](#fallback-model-chains).

Fable 5 runs with safety classifiers for cybersecurity and biology content. When a classifier flags a request, Claude Code re-runs that request on your provider's default Opus model and shows a notice in the transcript. On the Anthropic API, [LLM gateway](/en/llm-gateway) deployments, and [Claude Platform on AWS](/en/claude-platform-on-aws), that model is Opus 4.8. On the [Claude apps gateway](/en/claude-apps-gateway), it's Opus 4.7 unless you point the [`opus` alias](#environment-variables) at another model.

The session then continues on that Opus model. To return to Fable 5, run `/model fable`.

The fallback target is checked against [`availableModels`](#restrict-model-selection). When it is blocked, no fallback occurs. The refusal is shown as a normal error and the session's model is unchanged.

#### Check what triggered fallback

Fallback can trigger on the first request of a session, before you send anything unusual, because the first request carries workspace context such as your CLAUDE.md content and git status. A repository that contains security or biology material can trip the classifier on that context alone.

To check whether customizations are the trigger, start a session with `claude --safe-mode`, which disables customizations such as CLAUDE.md, skills, MCP servers, and hooks. Git status and directory names are not customizations and are still included.

#### Ask before switching

To decide what happens each time a request is flagged, rather than switching automatically, run `/config` and turn off "switch models when a message is flagged". A flagged request then pauses the session with two options: switch to the Opus model, or edit the prompt and retry on Fable 5.

Some cases behave differently:

* If both models flag the same request, you can edit the prompt and retry, or start a new session.
* On mobile [Claude Code on the web](/en/claude-code-on-the-web) sessions, editing and retrying is not supported. Switch models, or continue the session from a desktop browser or the desktop app.
* In [non-interactive mode](/en/cli-reference#cli-flags) and SDK integrations that can't show the prompt, a flagged request ends the turn with a refusal instead.
* When the fallback target is blocked by [`availableModels`](#restrict-model-selection), the prompt is not shown. The flagged request ends with the refusal, the same as automatic fallback when the target is blocked.

#### Enable fallback on Bedrock, Agent Platform, and Foundry

On [Amazon Bedrock](/en/amazon-bedrock), [Google Cloud's Agent Platform](/en/google-vertex-ai), and [Microsoft Foundry](/en/microsoft-foundry), model IDs are provider-specific, so automatic fallback only operates when Claude Code can identify both models involved:

* Claude Code must recognize the current model as Fable 5: the model ID contains `claude-fable-5`, matches the value of `ANTHROPIC_DEFAULT_FABLE_MODEL`, or is mapped with [`modelOverrides`](#override-model-ids-per-version).
* The fallback target must resolve to an Opus model: the value of `ANTHROPIC_DEFAULT_OPUS_MODEL` if set, otherwise an Opus 4.8 entry in the provider's model list.

If either model can't be identified, Claude Code does not switch automatically. The flagged request ends with a refusal message, and you can switch models with [`/model`](#setting-your-model) and retry. To enable automatic fallback on these providers, set `ANTHROPIC_DEFAULT_FABLE_MODEL` to your Fable 5 model ID and `ANTHROPIC_DEFAULT_OPUS_MODEL` to your Opus 4.8 model ID.

#### Security research and biology workloads

Workloads in offensive security or biology, including penetration testing, Capture the Flag (CTF) exercises, and biology-adjacent codebases, trigger fallback frequently, often on the first request. For substantive biology work, expect nearly all requests to reroute.

This is expected routing for these domains, not an account flag. If your organization needs Fable-class capability for this work, ask your Anthropic account team about trusted access programs.

### Adjust effort level

[Effort levels](https://platform.claude.com/docs/en/build-with-claude/effort) control adaptive reasoning, which lets the model decide whether and how much to think on each step based on task complexity. Lower effort is faster and cheaper for straightforward tasks, while higher effort provides deeper reasoning for complex problems.

The available effort levels depend on the model. Models not listed here do not support effort:

| Model                            | Levels                                  |
| :------------------------------- | :-------------------------------------- |
| Fable 5                          | `low`, `medium`, `high`, `xhigh`, `max` |
| Sonnet 5, Opus 4.8, and Opus 4.7 | `low`, `medium`, `high`, `xhigh`, `max` |
| Opus 4.6 and Sonnet 4.6          | `low`, `medium`, `high`, `max`          |

If you set a level the active model does not support, Claude Code falls back to the highest supported level at or below the one you set. For example, `xhigh` runs as `high` on Opus 4.6. Your organization can also cap which levels are available for a model; see [Organization effort limits](#organization-effort-limits).

The default effort is `high` on Fable 5, Sonnet 5, Opus 4.8, Opus 4.6, and Sonnet 4.6, and `xhigh` on Opus 4.7.

When you first run Fable 5, Opus 4.8, or Opus 4.7, Claude Code applies that model's default effort even if you previously set a different level for another model: `high` on Fable 5 and Opus 4.8, and `xhigh` on Opus 4.7. Run `/effort` again to choose a different level after switching. That default is held across sessions until you make an explicit effort choice, such as running `/effort` in an interactive session or launching with `--effort`.

`low`, `medium`, `high`, and `xhigh` persist across sessions when you set them in an interactive session. {/* min-version: 2.1.205 */}A level set with `/effort` in [non-interactive mode](/en/headless), with the `-p` flag, applies to the current session only and isn't saved as your default. A non-interactive `/effort` also can't release the model-default hold above: on Fable 5, Opus 4.8, and Opus 4.7 it reports `Not applied` and the session stays at the model's default effort, so pass `--effort` at launch instead. `max` provides the deepest reasoning with no constraint on token spending and applies to the current session only, except when set through the `CLAUDE_CODE_EFFORT_LEVEL` environment variable.

The `/effort` menu also offers `ultracode`. Ultracode is a Claude Code setting rather than a model effort level: it sends `xhigh` to the model and additionally has Claude orchestrate [dynamic workflows](/en/workflows) for substantive tasks. It applies to the current session only.

You can turn on ultracode through any of the following:

* **`/effort`**: run `/effort ultracode`, or select it from the menu
* **`--effort` flag**: launch with `claude --effort ultracode`, which starts the session at `xhigh` effort with ultracode on
* **`--settings` or an Agent SDK control request**: pass `"ultracode": true`. An [`applyFlagSettings()`](/en/agent-sdk/typescript#applyflagsettings) request also accepts `effortLevel: "ultracode"`

Passing `ultracode` to the `--effort` flag or the Agent SDK `effortLevel` value requires Claude Code v2.1.203 or later. Before v2.1.203, `--effort ultracode` printed `Unknown --effort value 'ultracode'` and the session started at the default effort.

The persisted `effortLevel` setting and the `CLAUDE_CODE_EFFORT_LEVEL` environment variable don't accept `ultracode`.

When ultracode isn't available, for example when [workflows are turned off](/en/workflows#turn-workflows-off), `--effort ultracode` sets `xhigh` effort only.

#### Choose an effort level

Each level trades token spend against capability. The default suits most coding tasks; adjust when you want a different balance.

| Level       | When to use it                                                                                                                                  |
| :---------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| `low`       | Reserve for short, scoped, latency-sensitive tasks that are not intelligence-sensitive                                                          |
| `medium`    | Reduces token usage for cost-sensitive work that can trade off some intelligence                                                                |
| `high`      | Balances token usage and intelligence. Default on Fable 5, Sonnet 5, Opus 4.8, Opus 4.6, and Sonnet 4.6                                         |
| `xhigh`     | Deeper reasoning at higher token spend. Default on Opus 4.7                                                                                     |
| `max`       | Can improve performance on demanding tasks but may show diminishing returns and is prone to overthinking. Test before adopting broadly          |
| `ultracode` | A Claude Code setting that plans a [dynamic workflow](/en/workflows) for each substantive task with `xhigh` per-message reasoning. Session-only |

The effort scale is calibrated per model, so the same level name does not represent the same underlying value across models.

#### Use ultrathink for one-off deep reasoning

Include `ultrathink` anywhere in your prompt to request deeper reasoning on that turn without changing your session effort setting. Claude Code recognizes the keyword and adds an in-context instruction. The effort level sent to the API is unchanged. Other phrases such as "think", "think hard", and "think more" are passed through as ordinary prompt text and are not recognized as keywords.

#### Set the effort level

You can change effort through any of the following:

* **`/effort`**: run `/effort` with no arguments to open an interactive slider, `/effort` followed by a level name to set it directly, or `/effort auto` to reset to the model default
* **In `/model`**: use left/right arrow keys to adjust the effort slider when selecting a model
* **`--effort` flag**: pass a level name to set it for a single session when launching Claude Code
* **Environment variable**: set `CLAUDE_CODE_EFFORT_LEVEL` to a level name or `auto`
* **Settings**: set `effortLevel` to `low`, `medium`, `high`, or `xhigh` in your settings file. `max` and `ultracode` are [session-only](#adjust-effort-level) and are not accepted here
* **Skill and subagent frontmatter**: set `effort` in a [skill](/en/skills#frontmatter-reference) or [subagent](/en/sub-agents#supported-frontmatter-fields) markdown file to override the effort level when that skill or subagent runs

The environment variable takes precedence over all other methods, then your configured level, then the model default. Frontmatter effort applies when that skill or subagent is active, overriding the session level but not the environment variable.

The effort slider appears in `/model` when a supported model is selected. The current effort level is also displayed next to the logo and spinner, for example "with low effort", so you can confirm which setting is active without opening `/model`.

#### Adaptive reasoning and fixed thinking budgets

Adaptive reasoning makes thinking optional on each step, so Claude can respond faster to routine prompts and reserve deeper thinking for steps that benefit from it. If you want Claude to think more or less often than the current level produces, you can say so directly in your prompt or in `CLAUDE.md`; the model responds to that guidance within its effort setting.

Fable 5, Sonnet 5, and Opus 4.7 and later always use adaptive reasoning. The fixed thinking budget mode and `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` do not apply to them.

On Opus 4.6 and Sonnet 4.6, you can set `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` to revert to the previous fixed thinking budget controlled by `MAX_THINKING_TOKENS`. See [environment variables](/en/env-vars).

### Extended thinking

Extended thinking is the reasoning Claude emits before responding. On models that support [adaptive reasoning](#adjust-effort-level), the effort level is the primary control for how much thinking happens; the settings below turn thinking on or off and control how it displays.

| Control                        | How to set it                                                                                                                                                                                                                                                                                                                                                             |
| :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Toggle for the current session | Press `Option+T` on macOS or `Alt+T` on Windows and Linux                                                                                                                                                                                                                                                                                                                 |
| Set the global default         | Run `/config` and toggle thinking mode. Saved as `alwaysThinkingEnabled` in `~/.claude/settings.json`                                                                                                                                                                                                                                                                     |
| Disable regardless of effort   | Set [`MAX_THINKING_TOKENS=0`](/en/env-vars), which turns thinking off on the Anthropic API except on Fable 5. On [third-party providers](/en/third-party-integrations) this omits the `thinking` parameter instead, and adaptive-reasoning models may still think. Other values apply only with a [fixed thinking budget](#adaptive-reasoning-and-fixed-thinking-budgets) |

Thinking cannot be turned off on Fable 5. The session toggle, `alwaysThinkingEnabled`, and `MAX_THINKING_TOKENS=0` have no effect there, and Fable 5 decides per step how much to think based on the effort level.

Thinking output is collapsed by default. Press `Ctrl+O` to toggle verbose mode and see the reasoning as gray italic text. Interactive sessions on the Anthropic API receive redacted thinking blocks by default, so set `showThinkingSummaries: true` in [settings](/en/settings) if you want the full summaries available when you expand. You are charged for all thinking tokens generated, even when collapsed or redacted.

### Extended context

Fable 5, Sonnet 5, Opus 4.6 and later, and Sonnet 4.6 support a [1 million token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#context-window-sizes-by-model) for long sessions with large codebases.

Availability varies by model and plan. On the Anthropic API, Fable 5, Sonnet 5, Opus 4.8, and Opus 4.7 always run with the 1M window. On Max, Team, and Enterprise plans, Opus is automatically upgraded to 1M context with no additional configuration. This applies to both Team Standard and Team Premium seats. Sonnet 4.6 with 1M context is not part of the automatic upgrade and requires [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) on every subscription plan, including Max.

| Plan                      | Opus with 1M context                                                                                        | Sonnet 4.6 with 1M context                                                                                  |
| ------------------------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Max, Team, and Enterprise | Included with subscription                                                                                  | Requires [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| Pro                       | Requires [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) | Requires [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| API and pay-as-you-go     | Full access                                                                                                 | Full access                                                                                                 |

To disable 1M context entirely, set `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. This removes 1M model variants from the model picker. See [environment variables](/en/env-vars).

The 1M context window uses standard model pricing with no premium for tokens beyond 200K. For plans where extended context is included with your subscription, usage remains covered by your subscription. For plans that access extended context through usage credits, tokens are billed to usage credits.

If your account supports 1M context, the option appears in the `/model` picker in the latest versions of Claude Code. If you don't see it, try restarting your session.

You can also use the `[1m]` suffix with model aliases or full model names:

```bash theme={null}
# Use the opus[1m] or sonnet[1m] alias
/model opus[1m]
/model sonnet[1m]

# Or append [1m] to a full model name
/model claude-opus-4-8[1m]
```

#### Sonnet 5 context window

On the Anthropic API, Sonnet 5 always runs with the 1M context window. There is no 200K variant, no `[1m]` suffix to select, and no usage credits required on any plan. Sessions auto-compact before the window fills, at about 967K tokens by default; set [`CLAUDE_CODE_AUTO_COMPACT_WINDOW`](/en/env-vars) to choose a different threshold.

Two configurations budget the window at 200K instead and auto-compact at that boundary:

* **LLM gateway**: when `ANTHROPIC_BASE_URL` points at a [gateway](/en/llm-gateway), Claude Code can't verify 1M support. To use the full window, select Sonnet 5 (1M context) in the model picker, which maps to `sonnet[1m]`.
* **`CLAUDE_CODE_DISABLE_1M_CONTEXT=1`**: treats Sonnet 5 sessions as having a 200K window, for deployments that need to cap context.

## Checking your current model

You can see which model you're currently using in two places:

* In the [status line](/en/statusline), if you have one configured
* In `/status`, which also displays your account information

## Add a custom model option

Use `ANTHROPIC_CUSTOM_MODEL_OPTION` to add a single custom entry to the `/model` picker without replacing the built-in aliases. This is useful for testing model IDs that Claude Code does not list by default. For LLM gateway deployments, Claude Code can populate the picker from the gateway's `/v1/models` endpoint when `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` is set, so this variable is needed only when discovery is disabled or does not return the model you want. See [gateway model discovery](/en/llm-gateway-protocol#model-discovery).

This example sets all three variables to make a gateway-routed Opus deployment selectable:

```bash theme={null}
export ANTHROPIC_CUSTOM_MODEL_OPTION="my-gateway/claude-opus-4-8"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Opus via Gateway"
export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="Custom deployment routed through the internal LLM gateway"
```

The custom entry appears at the bottom of the `/model` picker. `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` and `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` are optional. If omitted, the model ID is used as the name and the description defaults to `Custom model (<model-id>)`.

Claude Code skips validation for the model ID set in `ANTHROPIC_CUSTOM_MODEL_OPTION`, so you can use any string your API endpoint accepts. When [`availableModels`](#restrict-model-selection) is set, include the custom model ID in the allowlist as well: the custom entry is filtered from the picker and a `--model` selection of it is rejected like any other excluded model. A custom ID that embeds a family name, such as `my-gateway/claude-opus-4-8`, counts as a specific entry for that family and disables its wildcard, so also list the versions you intend to keep selectable. See [Merge behavior](#merge-behavior).

## Environment variables

You can use the following environment variables to control the model names that the aliases map to. Each value must be a full model name, or the equivalent identifier for your API provider.

| Environment variable             | Description                                                                                                                                                                                                                                                       |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_FABLE_MODEL`  | The model to use for `fable`, and the model ID Claude Code recognizes as Fable 5 for [automatic model fallback](#automatic-model-fallback) on third-party providers                                                                                               |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | The model to use for `opus`, or for `opusplan` when Plan Mode is active.                                                                                                                                                                                          |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | The model to use for `sonnet`, or for `opusplan` when Plan Mode is not active.                                                                                                                                                                                    |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | The model to use for `haiku`, or [background functionality](/en/costs#background-token-usage)                                                                                                                                                                     |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | The model to use for all [subagents](/en/sub-agents#choose-a-model) and [agent teams](/en/agent-teams). Overrides the per-invocation `model` parameter and the subagent definition's `model` frontmatter. Set to `inherit` to use normal model resolution instead |

Note: `ANTHROPIC_SMALL_FAST_MODEL` is deprecated in favor of
`ANTHROPIC_DEFAULT_HAIKU_MODEL`.

### Pin models for third-party deployments

When deploying Claude Code through [Amazon Bedrock](/en/amazon-bedrock), [Google Cloud's Agent Platform](/en/google-vertex-ai), [Microsoft Foundry](/en/microsoft-foundry), or [Claude Platform on AWS](/en/claude-platform-on-aws), pin model versions before rolling out to users.

Without pinning, Claude Code uses model aliases such as `fable`, `opus`, `sonnet`, and `haiku` that resolve to a built-in default model ID for each provider. That default can lag the newest Anthropic release, and the model it points to may not yet be enabled in a user's account. When the default is unavailable, Amazon Bedrock and Google Cloud's Agent Platform users see a notice and the session falls back to an earlier version of the default model, or to the default Sonnet model when the default is an Opus model and no Opus version is available. Microsoft Foundry users see errors instead, because Microsoft Foundry has no equivalent startup check.

<Warning>
  Set the model environment variables to specific version IDs as part of your initial setup. Pinning lets you control when your users move to a new model.
</Warning>

Use the following environment variables with version-specific model IDs for your provider:

| Provider                      | Example                                                              |
| :---------------------------- | :------------------------------------------------------------------- |
| Amazon Bedrock                | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-8'` |
| Google Cloud's Agent Platform | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8'`              |
| Microsoft Foundry             | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8'`              |

Apply the same pattern for `ANTHROPIC_DEFAULT_FABLE_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, and `ANTHROPIC_DEFAULT_HAIKU_MODEL`. For current and legacy model IDs across all providers, see [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). To upgrade users to a new model version, update these environment variables and redeploy.

To enable [extended context](#extended-context) for a pinned model, append `[1m]` to the model ID in `ANTHROPIC_DEFAULT_OPUS_MODEL` or `ANTHROPIC_DEFAULT_SONNET_MODEL`:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8[1m]'
```

The `[1m]` suffix applies the 1M context window to all usage of the `opus` and `sonnet` aliases, including the plan-mode Opus phase of [`opusplan`](#opusplan-model-setting).

* Claude Code strips the suffix before sending the model ID to your provider.
* Only append `[1m]` when the underlying model [supports 1M context](https://platform.claude.com/docs/en/build-with-claude/context-windows#context-window-sizes-by-model).
* The suffix is read per variable, not per model. On Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry, a model ID without `[1m]` in one variable uses 200K context even if another variable sets the same model with the suffix. Sonnet 5 always runs with the 1M window on these providers and never needs the suffix.

<Note>
  An `availableModels` allowlist delivered through [MDM or a managed settings file](/en/settings#settings-files) still applies when using third-party providers; [server-managed settings are not delivered there](/en/server-managed-settings#platform-availability). Filtering matches on a model alias such as `opus`, a version prefix such as `claude-opus-4-8`, or the full provider-form model ID. Provider-specific prefixes such as `us.anthropic.` are not stripped, so to allow a specific model, list the same provider-form ID the picker shows, or map it through [`modelOverrides`](#override-model-ids-per-version). Any `[1m]` suffix is stripped from both the allowlist entry and the requested model before matching.
</Note>

### Customize pinned model display and capabilities

When you pin a model on a third-party provider, the provider-specific ID appears as-is in the `/model` picker and Claude Code may not recognize which features the model supports. You can override the display name and declare capabilities with companion environment variables for each pinned model.

These variables take effect on third-party providers such as Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry. The `_NAME` and `_DESCRIPTION` variables also take effect when `ANTHROPIC_BASE_URL` points to an [LLM gateway](/en/llm-gateway). They have no effect when connecting directly to `api.anthropic.com`.

| Environment variable                                  | Description                                                                                                        |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME`                   | Display name for the pinned Opus model in the `/model` picker. Defaults to the model ID when not set               |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION`            | Display description for the pinned Opus model in the `/model` picker. Defaults to `Custom Opus model` when not set |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` | Comma-separated list of capabilities the pinned Opus model supports                                                |

The same `_NAME`, `_DESCRIPTION`, and `_SUPPORTED_CAPABILITIES` suffixes are available for `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`, `ANTHROPIC_DEFAULT_FABLE_MODEL`, and `ANTHROPIC_CUSTOM_MODEL_OPTION`.

Claude Code enables features like [effort levels](#adjust-effort-level) and [extended thinking](#extended-thinking) by matching the model ID against known patterns. Provider-specific IDs such as Amazon Bedrock ARNs or custom deployment names often don't match these patterns, leaving supported features disabled. Set `_SUPPORTED_CAPABILITIES` to tell Claude Code which features the model actually supports:

| Capability value       | Enables                                                                         |
| ---------------------- | ------------------------------------------------------------------------------- |
| `effort`               | [Effort levels](#adjust-effort-level) and the `/effort` command                 |
| `xhigh_effort`         | {/* min-version: 2.1.111 */}The `xhigh` effort level                            |
| `max_effort`           | The `max` effort level                                                          |
| `thinking`             | [Extended thinking](#extended-thinking)                                         |
| `adaptive_thinking`    | Adaptive reasoning that dynamically allocates thinking based on task complexity |
| `interleaved_thinking` | Thinking between tool calls                                                     |

When `_SUPPORTED_CAPABILITIES` is set, listed capabilities are enabled and unlisted capabilities are disabled for the matching pinned model. When the variable is unset, Claude Code falls back to built-in detection based on the model ID.

This example pins Opus to an Amazon Bedrock custom model ARN, sets a friendly name, and declares its capabilities:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='arn:aws:bedrock:us-east-1:123456789012:custom-model/abc'
export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME='Opus via Bedrock'
export ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION='Opus 4.7 routed through a Bedrock custom endpoint'
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES='effort,xhigh_effort,max_effort,thinking,adaptive_thinking,interleaved_thinking'
```

### Override model IDs per version

The family-level environment variables above configure one model ID per family alias. If you need to map several versions within the same family to distinct provider IDs, use the `modelOverrides` setting instead.

`modelOverrides` maps individual Anthropic model IDs to the provider-specific strings that Claude Code sends to your provider's API. When a user selects a mapped model in the `/model` picker, Claude Code uses your configured value instead of the built-in default.

This lets enterprise administrators route each model version to a specific Amazon Bedrock inference profile ARN, Google Cloud's Agent Platform version name, or Microsoft Foundry deployment name for governance, cost allocation, or regional routing.

Set `modelOverrides` in your [settings file](/en/settings#settings-files):

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

Keys must be Anthropic model IDs as listed in the [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). For dated model IDs, include the date suffix exactly as it appears there. Unknown keys are ignored.

Overrides replace the built-in model IDs that back each entry in the `/model` picker. On Amazon Bedrock, `modelOverrides` entries take precedence over any inference profiles that Claude Code discovers automatically at startup. Claude Code passes values that are already provider-native, such as Amazon Bedrock inference profile ARNs or Microsoft Foundry deployment names, to the provider as-is.

{/* min-version: 2.1.200 */}Overrides also apply when you pass an Anthropic model ID directly through `--model`, the `ANTHROPIC_MODEL` environment variable, or an `ANTHROPIC_DEFAULT_*_MODEL` environment variable. On Amazon Bedrock, Google Cloud's Agent Platform, and [Mantle](/en/amazon-bedrock#use-the-mantle-endpoint), an Anthropic model ID with no `modelOverrides` entry resolves to the same provider-specific ID as the `/model` picker row for that version, when the provider supports that version. Mantle supports a subset of versions. For an Anthropic model ID outside that subset, Claude Code sends the raw ID to Mantle without mapping it, unless a `modelOverrides` entry covers it. Before v2.1.200, `--model` and the environment-variable values reached the provider as-is without going through the override map.

`modelOverrides` works alongside `availableModels`. The allowlist is evaluated against the Anthropic model ID, not the override value, so an entry like `"opus"` in `availableModels` continues to match even when Opus versions are mapped to ARNs. When `enforceAvailableModels` is set in managed settings, the enforced Default resolves through `modelOverrides` from the [highest-precedence managed source](/en/server-managed-settings#settings-precedence) only. An admin's mapping, such as a version pinned to an inference profile ARN, is honored in the enforced Default. Overrides from user or project settings do not affect it.

{/* min-version: 2.1.200 */}When `availableModels` is set in [managed settings](/en/settings#settings-files), only `modelOverrides` from that managed source apply to an Anthropic model ID passed directly through `--model` or the environment variables above. Claude Code ignores overrides in user or project settings for those IDs, and never resolves an ID the managed list excludes through `modelOverrides` from any settings source. This managed-source restriction requires Claude Code v2.1.200 or later. See [Restrict model selection](#restrict-model-selection) for how blocked IDs are handled.

### Prompt caching configuration

Claude Code automatically uses [prompt caching](/en/prompt-caching) to optimize performance and reduce costs. You can disable prompt caching globally or for specific model tiers:

| Environment variable            | Description                                                                                       |
| ------------------------------- | ------------------------------------------------------------------------------------------------- |
| `DISABLE_PROMPT_CACHING`        | Set to `1` to disable prompt caching for all models. Takes precedence over the per-model settings |
| `DISABLE_PROMPT_CACHING_HAIKU`  | Set to `1` to disable prompt caching for Haiku models only                                        |
| `DISABLE_PROMPT_CACHING_SONNET` | Set to `1` to disable prompt caching for Sonnet models only                                       |
| `DISABLE_PROMPT_CACHING_OPUS`   | Set to `1` to disable prompt caching for Opus models only                                         |
| `DISABLE_PROMPT_CACHING_FABLE`  | Set to `1` to disable prompt caching for Fable models only                                        |

To change the cache TTL or learn what triggers a cache miss, see [How Claude Code uses prompt caching](/en/prompt-caching).
