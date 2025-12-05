## List

`messages().batches().list(BatchListParamsparams = BatchListParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : BatchListPage`

**get** `/v1/messages/batches`

List all Message Batches within a Workspace. Most recently created batches are returned first.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchListParams`

  - `afterId: Optional<String>`

    ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

  - `beforeId: Optional<String>`

    ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

  - `limit: Optional<Long>`

    Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `1000`.

### Returns

- `class MessageBatch:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archivedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancelInitiatedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `createdAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `endedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expiresAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processingStatus: ProcessingStatus`

    Processing status of the Message Batch.

    - `IN_PROGRESS("in_progress")`

    - `CANCELING("canceling")`

    - `ENDED("ended")`

  - `requestCounts: MessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: Long`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: Long`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: Long`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: Long`

      Number of requests in the Message Batch that are processing.

    - `succeeded: Long`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `resultsUrl: Optional<String>`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: JsonValue; "message_batch"constant`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `MESSAGE_BATCH("message_batch")`

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.messages.batches.BatchListPage
import com.anthropic.models.messages.batches.BatchListParams

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val page: BatchListPage = client.messages().batches().list()
}
```
