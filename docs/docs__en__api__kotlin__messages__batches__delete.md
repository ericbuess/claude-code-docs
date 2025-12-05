## Delete

`messages().batches().delete(BatchDeleteParamsparams = BatchDeleteParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : DeletedMessageBatch`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchDeleteParams`

  - `messageBatchId: Optional<String>`

    ID of the Message Batch.

### Returns

- `class DeletedMessageBatch:`

  - `id: String`

    ID of the Message Batch.

  - `type: JsonValue; "message_batch_deleted"constant`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `MESSAGE_BATCH_DELETED("message_batch_deleted")`

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.messages.batches.BatchDeleteParams
import com.anthropic.models.messages.batches.DeletedMessageBatch

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val deletedMessageBatch: DeletedMessageBatch = client.messages().batches().delete("message_batch_id")
}
```
