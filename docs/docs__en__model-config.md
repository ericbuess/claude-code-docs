# Model configuration

> Learn about the Claude Code model configuration, including model aliases like `opusplan`

## Available models

For the `model` setting in Claude Code, you can either configure:

* A **model alias**
* A full **[model name](https://docs.claude.com/en/docs/about-claude/models/overview#model-names)**
* For Bedrock, an ARN

### Model aliases

Model aliases provide a convenient way to select model settings without
remembering exact version numbers:

| Model alias      | Behavior                                                                                                                                                                |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**    | Recommended model setting, depending on your account type                                                                                                               |
| **`sonnet`**     | Uses the latest Sonnet model (currently Sonnet 4.5) for daily coding tasks                                                                                              |
| **`opus`**       | Uses Opus model (currently Opus 4.1) for specialized complex reasoning tasks                                                                                            |
| **`haiku`**      | Uses the fast and efficient Haiku model for simple tasks                                                                                                                |
| **`sonnet[1m]`** | Uses Sonnet with a [1 million token context window](https://docs.claude.com/en/docs/build-with-claude/context-windows#1m-token-context-window) window for long sessions |
| **`opusplan`**   | Special mode that uses `opus` during plan mode, then switches to `sonnet` for execution                                                                                 |

### Setting your model

You can configure your model in several ways, listed in order of priority:

1. **During session** - Use `/model <alias|name>` to switch models mid-session
2. **At startup** - Launch with `claude --model <alias|name>`
3. **Environment variable** - Set `ANTHROPIC_MODEL=<alias|name>`
4. **Settings** - Configure permanently in your settings file using the `model`
   field.

Example usage:

```bash  theme={null}
# Start with Opus
claude --model opus

# Switch to Sonnet during session
/model sonnet
```

Example settings file:

```
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## Special model behavior

### `default` model setting

The behavior of `default` depends on your account type.

For certain Max users, Claude Code will automatically fall back to Sonnet if you
hit a usage threshold with Opus.

### `opusplan` model setting

The `opusplan` model alias provides an automated hybrid approach:

* **In plan mode** - Uses `opus` for complex reasoning and architecture
  decisions
* **In execution mode** - Automatically switches to `sonnet` for code generation
  and implementation

This gives you the best of both worlds: Opus's superior reasoning for planning,
and Sonnet's efficiency for execution.

### Extended context with \[1m]

For Console/API users, the `[1m]` suffix can be added to full model names to
enable a
[1 million token context window](https://docs.claude.com/en/docs/build-with-claude/context-windows#1m-token-context-window).

```bash  theme={null}
# Example of using a full model name with the [1m] suffix
/model anthropic.claude-sonnet-4-5-20250929-v1:0[1m]
```

Note: Extended context models have
[different pricing](https://docs.claude.com/en/docs/about-claude/pricing#long-context-pricing).

## Checking your current model

You can see which model you're currently using in several ways:

1. In [status line](/en/statusline) (if configured)
2. In `/status`, which also displays your account information.

## Environment variables

You can use the following environment variables, which must be full **model
names**, to control the model names that the aliases map to.

| Env var                          | Description                                                                                   |
| -------------------------------- | --------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | The model to use for `opus`, or for `opusplan` when Plan Mode is active.                      |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | The model to use for `sonnet`, or for `opusplan` when Plan Mode is not active.                |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | The model to use for `haiku`, or [background functionality](/en/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | The model to use for [subagents](/en/sub-agents)                                              |

Note: `ANTHROPIC_SMALL_FAST_MODEL` is deprecated in favor of
`ANTHROPIC_DEFAULT_HAIKU_MODEL`.

### Prompt caching configuration

Claude Code automatically uses [prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) to optimize performance and reduce costs. You can disable prompt caching globally or for specific model tiers:

| Env var                         | Description                                                                                    |
| ------------------------------- | ---------------------------------------------------------------------------------------------- |
| `DISABLE_PROMPT_CACHING`        | Set to `1` to disable prompt caching for all models (takes precedence over per-model settings) |
| `DISABLE_PROMPT_CACHING_HAIKU`  | Set to `1` to disable prompt caching for Haiku models only                                     |
| `DISABLE_PROMPT_CACHING_SONNET` | Set to `1` to disable prompt caching for Sonnet models only                                    |
| `DISABLE_PROMPT_CACHING_OPUS`   | Set to `1` to disable prompt caching for Opus models only                                      |

These environment variables give you fine-grained control over prompt caching behavior. The global `DISABLE_PROMPT_CACHING` setting takes precedence over the model-specific settings, allowing you to quickly disable all caching when needed. The per-model settings are useful for selective control, such as when debugging specific models or working with cloud providers that may have different caching implementations.
