# Completions

## Create

`Completion completions().create(CompletionCreateParamsparams, RequestOptionsrequestOptions = RequestOptions.none())`

**post** `/v1/complete`

[Legacy] Create a Text Completion.

The Text Completions API is a legacy API. We recommend using the [Messages API](https://docs.claude.com/en/api/messages) going forward.

Future models and features will not be compatible with Text Completions. See our [migration guide](https://docs.claude.com/en/api/migrating-from-text-completions-to-messages) for guidance in migrating from Text Completions to Messages.

### Parameters

- `CompletionCreateParams params`

  - `Optional<List<AnthropicBeta>> betas`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

  - `long maxTokensToSample`

    The maximum number of tokens to generate before stopping.

    Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

  - `Model model`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

  - `String prompt`

    The prompt that you want Claude to complete.

    For proper response generation you will need to format your prompt using alternating `

    Human:`and`

    Assistant:` conversational turns. For example:

    ```
    "
    
    Human: {userQuestion}
    
    Assistant:"
    ```

    See [prompt validation](https://docs.claude.com/en/api/prompt-validation) and our guide to [prompt design](https://docs.claude.com/en/docs/intro-to-prompting) for more details.

  - `Optional<Metadata> metadata`

    An object describing metadata about the request.

  - `Optional<List<String>> stopSequences`

    Sequences that will cause the model to stop generating.

    Our models stop on `"

    Human:"`, and may include additional built-in stop sequences in the future. By providing the stop_sequences parameter, you may include additional strings that will cause the model to stop generating.

  - `Optional<Double> temperature`

    Amount of randomness injected into the response.

    Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.

    Note that even with `temperature` of `0.0`, the results will not be fully deterministic.

  - `Optional<Long> topK`

    Only sample from the top K options for each subsequent token.

    Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

    Recommended for advanced use cases only. You usually only need to use `temperature`.

  - `Optional<Double> topP`

    Use nucleus sampling.

    In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

    Recommended for advanced use cases only. You usually only need to use `temperature`.

### Returns

- `class Completion:`

  - `String id`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `String completion`

    The resulting completion up to and excluding the stop sequences.

  - `Model model`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

    - `CLAUDE_OPUS_4_5_20251101("claude-opus-4-5-20251101")`

      Premium model combining maximum intelligence with practical performance

    - `CLAUDE_OPUS_4_5("claude-opus-4-5")`

      Premium model combining maximum intelligence with practical performance

    - `CLAUDE_3_7_SONNET_LATEST("claude-3-7-sonnet-latest")`

      High-performance model with early extended thinking

    - `CLAUDE_3_7_SONNET_20250219("claude-3-7-sonnet-20250219")`

      High-performance model with early extended thinking

    - `CLAUDE_3_5_HAIKU_LATEST("claude-3-5-haiku-latest")`

      Fastest and most compact model for near-instant responsiveness

    - `CLAUDE_3_5_HAIKU_20241022("claude-3-5-haiku-20241022")`

      Our fastest model

    - `CLAUDE_HAIKU_4_5("claude-haiku-4-5")`

      Hybrid model, capable of near-instant responses and extended thinking

    - `CLAUDE_HAIKU_4_5_20251001("claude-haiku-4-5-20251001")`

      Hybrid model, capable of near-instant responses and extended thinking

    - `CLAUDE_SONNET_4_20250514("claude-sonnet-4-20250514")`

      High-performance model with extended thinking

    - `CLAUDE_SONNET_4_0("claude-sonnet-4-0")`

      High-performance model with extended thinking

    - `CLAUDE_4_SONNET_20250514("claude-4-sonnet-20250514")`

      High-performance model with extended thinking

    - `CLAUDE_SONNET_4_5("claude-sonnet-4-5")`

      Our best model for real-world agents and coding

    - `CLAUDE_SONNET_4_5_20250929("claude-sonnet-4-5-20250929")`

      Our best model for real-world agents and coding

    - `CLAUDE_OPUS_4_0("claude-opus-4-0")`

      Our most capable model

    - `CLAUDE_OPUS_4_20250514("claude-opus-4-20250514")`

      Our most capable model

    - `CLAUDE_4_OPUS_20250514("claude-4-opus-20250514")`

      Our most capable model

    - `CLAUDE_OPUS_4_1_20250805("claude-opus-4-1-20250805")`

      Our most capable model

    - `CLAUDE_3_OPUS_LATEST("claude-3-opus-latest")`

      Excels at writing and complex tasks

    - `CLAUDE_3_OPUS_20240229("claude-3-opus-20240229")`

      Excels at writing and complex tasks

    - `CLAUDE_3_HAIKU_20240307("claude-3-haiku-20240307")`

      Our previous most fast and cost-effective

  - `Optional<String> stopReason`

    The reason that we stopped.

    This may be one the following values:

    * `"stop_sequence"`: we reached a stop sequence — either provided by you via the `stop_sequences` parameter, or a stop sequence built into the model
    * `"max_tokens"`: we exceeded `max_tokens_to_sample` or the model's maximum

  - `JsonValue; type "completion"constant`

    Object type.

    For Text Completions, this is always `"completion"`.

    - `COMPLETION("completion")`

### Example

```java
package com.anthropic.example;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.completions.Completion;
import com.anthropic.models.completions.CompletionCreateParams;
import com.anthropic.models.messages.Model;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        CompletionCreateParams params = CompletionCreateParams.builder()
            .maxTokensToSample(256L)
            .model(Model.CLAUDE_OPUS_4_5_20251101)
            .prompt("\n\nHuman: Hello, world!\n\nAssistant:")
            .build();
        Completion completion = client.completions().create(params);
    }
}
```

## Domain Types

### Completion

- `class Completion:`

  - `String id`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `String completion`

    The resulting completion up to and excluding the stop sequences.

  - `Model model`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

    - `CLAUDE_OPUS_4_5_20251101("claude-opus-4-5-20251101")`

      Premium model combining maximum intelligence with practical performance

    - `CLAUDE_OPUS_4_5("claude-opus-4-5")`

      Premium model combining maximum intelligence with practical performance

    - `CLAUDE_3_7_SONNET_LATEST("claude-3-7-sonnet-latest")`

      High-performance model with early extended thinking

    - `CLAUDE_3_7_SONNET_20250219("claude-3-7-sonnet-20250219")`

      High-performance model with early extended thinking

    - `CLAUDE_3_5_HAIKU_LATEST("claude-3-5-haiku-latest")`

      Fastest and most compact model for near-instant responsiveness

    - `CLAUDE_3_5_HAIKU_20241022("claude-3-5-haiku-20241022")`

      Our fastest model

    - `CLAUDE_HAIKU_4_5("claude-haiku-4-5")`

      Hybrid model, capable of near-instant responses and extended thinking

    - `CLAUDE_HAIKU_4_5_20251001("claude-haiku-4-5-20251001")`

      Hybrid model, capable of near-instant responses and extended thinking

    - `CLAUDE_SONNET_4_20250514("claude-sonnet-4-20250514")`

      High-performance model with extended thinking

    - `CLAUDE_SONNET_4_0("claude-sonnet-4-0")`

      High-performance model with extended thinking

    - `CLAUDE_4_SONNET_20250514("claude-4-sonnet-20250514")`

      High-performance model with extended thinking

    - `CLAUDE_SONNET_4_5("claude-sonnet-4-5")`

      Our best model for real-world agents and coding

    - `CLAUDE_SONNET_4_5_20250929("claude-sonnet-4-5-20250929")`

      Our best model for real-world agents and coding

    - `CLAUDE_OPUS_4_0("claude-opus-4-0")`

      Our most capable model

    - `CLAUDE_OPUS_4_20250514("claude-opus-4-20250514")`

      Our most capable model

    - `CLAUDE_4_OPUS_20250514("claude-4-opus-20250514")`

      Our most capable model

    - `CLAUDE_OPUS_4_1_20250805("claude-opus-4-1-20250805")`

      Our most capable model

    - `CLAUDE_3_OPUS_LATEST("claude-3-opus-latest")`

      Excels at writing and complex tasks

    - `CLAUDE_3_OPUS_20240229("claude-3-opus-20240229")`

      Excels at writing and complex tasks

    - `CLAUDE_3_HAIKU_20240307("claude-3-haiku-20240307")`

      Our previous most fast and cost-effective

  - `Optional<String> stopReason`

    The reason that we stopped.

    This may be one the following values:

    * `"stop_sequence"`: we reached a stop sequence — either provided by you via the `stop_sequences` parameter, or a stop sequence built into the model
    * `"max_tokens"`: we exceeded `max_tokens_to_sample` or the model's maximum

  - `JsonValue; type "completion"constant`

    Object type.

    For Text Completions, this is always `"completion"`.

    - `COMPLETION("completion")`
