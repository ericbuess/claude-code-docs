## Create

`client.Completions.New(ctx, params) (*Completion, error)`

**post** `/v1/complete`

[Legacy] Create a Text Completion.

The Text Completions API is a legacy API. We recommend using the [Messages API](https://docs.claude.com/en/api/messages) going forward.

Future models and features will not be compatible with Text Completions. See our [migration guide](https://docs.claude.com/en/api/migrating-from-text-completions-to-messages) for guidance in migrating from Text Completions to Messages.

### Parameters

- `params CompletionNewParams`

  - `MaxTokensToSample param.Field[int64]`

    Body param: The maximum number of tokens to generate before stopping.

    Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

  - `Model param.Field[Model]`

    Body param: The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

  - `Prompt param.Field[string]`

    Body param: The prompt that you want Claude to complete.

    For proper response generation you will need to format your prompt using alternating `

    Human:`and`

    Assistant:` conversational turns. For example:

    ```
    "
    
    Human: {userQuestion}
    
    Assistant:"
    ```

    See [prompt validation](https://docs.claude.com/en/api/prompt-validation) and our guide to [prompt design](https://docs.claude.com/en/docs/intro-to-prompting) for more details.

  - `Metadata param.Field[Metadata]`

    Body param: An object describing metadata about the request.

  - `StopSequences param.Field[[]string]`

    Body param: Sequences that will cause the model to stop generating.

    Our models stop on `"

    Human:"`, and may include additional built-in stop sequences in the future. By providing the stop_sequences parameter, you may include additional strings that will cause the model to stop generating.

  - ``

  - `Temperature param.Field[float64]`

    Body param: Amount of randomness injected into the response.

    Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.

    Note that even with `temperature` of `0.0`, the results will not be fully deterministic.

  - `TopK param.Field[int64]`

    Body param: Only sample from the top K options for each subsequent token.

    Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

    Recommended for advanced use cases only. You usually only need to use `temperature`.

  - `TopP param.Field[float64]`

    Body param: Use nucleus sampling.

    In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

    Recommended for advanced use cases only. You usually only need to use `temperature`.

  - `Betas param.Field[[]AnthropicBeta]`

    Header param: Optional header to specify the beta version(s) you want to use.

    - `string`

    - `type AnthropicBeta string`

      - `const AnthropicBetaMessageBatches2024_09_24 AnthropicBeta = "message-batches-2024-09-24"`

      - `const AnthropicBetaPromptCaching2024_07_31 AnthropicBeta = "prompt-caching-2024-07-31"`

      - `const AnthropicBetaComputerUse2024_10_22 AnthropicBeta = "computer-use-2024-10-22"`

      - `const AnthropicBetaComputerUse2025_01_24 AnthropicBeta = "computer-use-2025-01-24"`

      - `const AnthropicBetaPDFs2024_09_25 AnthropicBeta = "pdfs-2024-09-25"`

      - `const AnthropicBetaTokenCounting2024_11_01 AnthropicBeta = "token-counting-2024-11-01"`

      - `const AnthropicBetaTokenEfficientTools2025_02_19 AnthropicBeta = "token-efficient-tools-2025-02-19"`

      - `const AnthropicBetaOutput128k2025_02_19 AnthropicBeta = "output-128k-2025-02-19"`

      - `const AnthropicBetaFilesAPI2025_04_14 AnthropicBeta = "files-api-2025-04-14"`

      - `const AnthropicBetaMCPClient2025_04_04 AnthropicBeta = "mcp-client-2025-04-04"`

      - `const AnthropicBetaMCPClient2025_11_20 AnthropicBeta = "mcp-client-2025-11-20"`

      - `const AnthropicBetaDevFullThinking2025_05_14 AnthropicBeta = "dev-full-thinking-2025-05-14"`

      - `const AnthropicBetaInterleavedThinking2025_05_14 AnthropicBeta = "interleaved-thinking-2025-05-14"`

      - `const AnthropicBetaCodeExecution2025_05_22 AnthropicBeta = "code-execution-2025-05-22"`

      - `const AnthropicBetaExtendedCacheTTL2025_04_11 AnthropicBeta = "extended-cache-ttl-2025-04-11"`

      - `const AnthropicBetaContext1m2025_08_07 AnthropicBeta = "context-1m-2025-08-07"`

      - `const AnthropicBetaContextManagement2025_06_27 AnthropicBeta = "context-management-2025-06-27"`

      - `const AnthropicBetaModelContextWindowExceeded2025_08_26 AnthropicBeta = "model-context-window-exceeded-2025-08-26"`

      - `const AnthropicBetaSkills2025_10_02 AnthropicBeta = "skills-2025-10-02"`

### Returns

- `type Completion struct{…}`

  - `ID string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `Completion string`

    The resulting completion up to and excluding the stop sequences.

  - `Model Model`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

    - `type Model string`

      The model that will complete your prompt.

      See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

      - `const ModelClaudeOpus4_5_20251101 Model = "claude-opus-4-5-20251101"`

        Premium model combining maximum intelligence with practical performance

      - `const ModelClaudeOpus4_5 Model = "claude-opus-4-5"`

        Premium model combining maximum intelligence with practical performance

      - `const ModelClaude3_7SonnetLatest Model = "claude-3-7-sonnet-latest"`

        High-performance model with early extended thinking

      - `const ModelClaude3_7Sonnet20250219 Model = "claude-3-7-sonnet-20250219"`

        High-performance model with early extended thinking

      - `const ModelClaude3_5HaikuLatest Model = "claude-3-5-haiku-latest"`

        Fastest and most compact model for near-instant responsiveness

      - `const ModelClaude3_5Haiku20241022 Model = "claude-3-5-haiku-20241022"`

        Our fastest model

      - `const ModelClaudeHaiku4_5 Model = "claude-haiku-4-5"`

        Hybrid model, capable of near-instant responses and extended thinking

      - `const ModelClaudeHaiku4_5_20251001 Model = "claude-haiku-4-5-20251001"`

        Hybrid model, capable of near-instant responses and extended thinking

      - `const ModelClaudeSonnet4_20250514 Model = "claude-sonnet-4-20250514"`

        High-performance model with extended thinking

      - `const ModelClaudeSonnet4_0 Model = "claude-sonnet-4-0"`

        High-performance model with extended thinking

      - `const ModelClaude4Sonnet20250514 Model = "claude-4-sonnet-20250514"`

        High-performance model with extended thinking

      - `const ModelClaudeSonnet4_5 Model = "claude-sonnet-4-5"`

        Our best model for real-world agents and coding

      - `const ModelClaudeSonnet4_5_20250929 Model = "claude-sonnet-4-5-20250929"`

        Our best model for real-world agents and coding

      - `const ModelClaudeOpus4_0 Model = "claude-opus-4-0"`

        Our most capable model

      - `const ModelClaudeOpus4_20250514 Model = "claude-opus-4-20250514"`

        Our most capable model

      - `const ModelClaude4Opus20250514 Model = "claude-4-opus-20250514"`

        Our most capable model

      - `const ModelClaudeOpus4_1_20250805 Model = "claude-opus-4-1-20250805"`

        Our most capable model

      - `const ModelClaude3OpusLatest Model = "claude-3-opus-latest"`

        Excels at writing and complex tasks

      - `const ModelClaude_3_Opus_20240229 Model = "claude-3-opus-20240229"`

        Excels at writing and complex tasks

      - `const ModelClaude_3_Haiku_20240307 Model = "claude-3-haiku-20240307"`

        Our previous most fast and cost-effective

    - `string`

  - `StopReason string`

    The reason that we stopped.

    This may be one the following values:

    * `"stop_sequence"`: we reached a stop sequence — either provided by you via the `stop_sequences` parameter, or a stop sequence built into the model
    * `"max_tokens"`: we exceeded `max_tokens_to_sample` or the model's maximum

  - `Type Completion`

    Object type.

    For Text Completions, this is always `"completion"`.

    - `const CompletionCompletion Completion = "completion"`

### Example

```go
package main

import (
  "context"
  "fmt"

  "github.com/anthropics/anthropic-sdk-go"
  "github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
  client := anthropic.NewClient(
    option.WithAPIKey("my-anthropic-api-key"),
  )
  completion, err := client.Completions.New(context.TODO(), anthropic.CompletionNewParams{
    MaxTokensToSample: 256,
    Model: anthropic.ModelClaudeOpus4_5_20251101,
    Prompt: "\n\nHuman: Hello, world!\n\nAssistant:",
  })
  if err != nil {
    panic(err.Error())
  }
  fmt.Printf("%+v\n", completion.ID)
}
```
