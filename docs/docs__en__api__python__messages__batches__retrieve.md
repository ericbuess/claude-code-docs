## Retrieve

`messages.batches.retrieve(strmessage_batch_id)  -> MessageBatch`

**get** `/v1/messages/batches/{message_batch_id}`

This endpoint is idempotent and can be used to poll for Message Batch completion. To access the results of a Message Batch, make a request to the `results_url` field in the response.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `message_batch_id: str`

  ID of the Message Batch.

### Returns

- `class MessageBatch: …`

  - `id: str`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archived_at: Optional[datetime]`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancel_initiated_at: Optional[datetime]`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `created_at: datetime`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `ended_at: Optional[datetime]`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expires_at: datetime`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processing_status: Literal["in_progress", "canceling", "ended"]`

    Processing status of the Message Batch.

    - `"in_progress"`

    - `"canceling"`

    - `"ended"`

  - `request_counts: MessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: int`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: int`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: int`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: int`

      Number of requests in the Message Batch that are processing.

    - `succeeded: int`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `results_url: Optional[str]`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: Literal["message_batch"]`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `"message_batch"`

### Example

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="my-anthropic-api-key",
)
message_batch = client.messages.batches.retrieve(
    "message_batch_id",
)
print(message_batch.id)
```
