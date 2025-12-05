## List

`client.Messages.Batches.List(ctx, query) (*Page[MessageBatch], error)`

**get** `/v1/messages/batches`

List all Message Batches within a Workspace. Most recently created batches are returned first.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `query MessageBatchListParams`

  - `AfterID param.Field[string]`

    ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

  - `BeforeID param.Field[string]`

    ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

  - `Limit param.Field[int64]`

    Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `1000`.

### Returns

- `type MessageBatch struct{…}`

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

  - `ProcessingStatus MessageBatchProcessingStatus`

    Processing status of the Message Batch.

    - `const MessageBatchProcessingStatusInProgress MessageBatchProcessingStatus = "in_progress"`

    - `const MessageBatchProcessingStatusCanceling MessageBatchProcessingStatus = "canceling"`

    - `const MessageBatchProcessingStatusEnded MessageBatchProcessingStatus = "ended"`

  - `RequestCounts MessageBatchRequestCounts`

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
  page, err := client.Messages.Batches.List(context.TODO(), anthropic.MessageBatchListParams{

  })
  if err != nil {
    panic(err.Error())
  }
  fmt.Printf("%+v\n", page)
}
```
