## Cancel

`client.Beta.Messages.Batches.Cancel(ctx, messageBatchID, body) (*BetaMessageBatch, error)`

**post** `/v1/messages/batches/{message_batch_id}/cancel`

Batches may be canceled any time before processing ends. Once cancellation is initiated, the batch enters a `canceling` state, at which time the system may complete any in-progress, non-interruptible requests before finalizing cancellation.

The number of canceled requests is specified in `request_counts`. To determine which requests were canceled, check the individual results within the batch. Note that cancellation may not result in any canceled requests if they were non-interruptible.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `messageBatchID string`

  ID of the Message Batch.

- `body BetaMessageBatchCancelParams`

  - `Betas param.Field[[]AnthropicBeta]`

    Optional header to specify the beta version(s) you want to use.

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

- `type BetaMessageBatch struct{…}`

  - `ID string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `ArchivedAt Time`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `CancelInitiatedAt Time`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `CreatedAt Time`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `EndedAt Time`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `ExpiresAt Time`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `ProcessingStatus BetaMessageBatchProcessingStatus`

    Processing status of the Message Batch.

    - `const BetaMessageBatchProcessingStatusInProgress BetaMessageBatchProcessingStatus = "in_progress"`

    - `const BetaMessageBatchProcessingStatusCanceling BetaMessageBatchProcessingStatus = "canceling"`

    - `const BetaMessageBatchProcessingStatusEnded BetaMessageBatchProcessingStatus = "ended"`

  - `RequestCounts BetaMessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `Canceled int64`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `Errored int64`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `Expired int64`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `Processing int64`

      Number of requests in the Message Batch that are processing.

    - `Succeeded int64`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `ResultsURL string`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `Type MessageBatch`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `const MessageBatchMessageBatch MessageBatch = "message_batch"`

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
  betaMessageBatch, err := client.Beta.Messages.Batches.Cancel(
    context.TODO(),
    "message_batch_id",
    anthropic.BetaMessageBatchCancelParams{

    },
  )
  if err != nil {
    panic(err.Error())
  }
  fmt.Printf("%+v\n", betaMessageBatch.ID)
}
```
