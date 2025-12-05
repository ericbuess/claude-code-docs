## Retrieve

`beta.messages.batches.retrieve(message_batch_id, **kwargs) -> BetaMessageBatch`

**get** `/v1/messages/batches/{message_batch_id}`

This endpoint is idempotent and can be used to poll for Message Batch completion. To access the results of a Message Batch, make a request to the `results_url` field in the response.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `message_batch_id: String`

  ID of the Message Batch.

- `anthropic_beta: Array[AnthropicBeta]`

  Optional header to specify the beta version(s) you want to use.

  - `String`

  - `:"message-batches-2024-09-24" | :"prompt-caching-2024-07-31" | :"computer-use-2024-10-22" | 16 more`

    - `:"message-batches-2024-09-24"`

    - `:"prompt-caching-2024-07-31"`

    - `:"computer-use-2024-10-22"`

    - `:"computer-use-2025-01-24"`

    - `:"pdfs-2024-09-25"`

    - `:"token-counting-2024-11-01"`

    - `:"token-efficient-tools-2025-02-19"`

    - `:"output-128k-2025-02-19"`

    - `:"files-api-2025-04-14"`

    - `:"mcp-client-2025-04-04"`

    - `:"mcp-client-2025-11-20"`

    - `:"dev-full-thinking-2025-05-14"`

    - `:"interleaved-thinking-2025-05-14"`

    - `:"code-execution-2025-05-22"`

    - `:"extended-cache-ttl-2025-04-11"`

    - `:"context-1m-2025-08-07"`

    - `:"context-management-2025-06-27"`

    - `:"model-context-window-exceeded-2025-08-26"`

    - `:"skills-2025-10-02"`

### Returns

- `class BetaMessageBatch`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archived_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancel_initiated_at: Time`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `created_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `ended_at: Time`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expires_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processing_status: :in_progress | :canceling | :ended`

    Processing status of the Message Batch.

    - `:in_progress`

    - `:canceling`

    - `:ended`

  - `request_counts: BetaMessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: Integer`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: Integer`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: Integer`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: Integer`

      Number of requests in the Message Batch that are processing.

    - `succeeded: Integer`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `results_url: String`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: :message_batch`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `:message_batch`

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

beta_message_batch = anthropic.beta.messages.batches.retrieve("message_batch_id")

puts(beta_message_batch)
```
