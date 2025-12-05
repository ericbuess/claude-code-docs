## Delete

`messages.batches.delete(strmessage_batch_id)  -> DeletedMessageBatch`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `message_batch_id: str`

  ID of the Message Batch.

### Returns

- `class DeletedMessageBatch: …`

  - `id: str`

    ID of the Message Batch.

  - `type: Literal["message_batch_deleted"]`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `"message_batch_deleted"`

### Example

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="my-anthropic-api-key",
)
deleted_message_batch = client.messages.batches.delete(
    "message_batch_id",
)
print(deleted_message_batch.id)
```
