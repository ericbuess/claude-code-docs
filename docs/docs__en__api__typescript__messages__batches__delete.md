## Delete

`client.messages.batches.delete(stringmessageBatchID, RequestOptionsoptions?): DeletedMessageBatch`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `messageBatchID: string`

  ID of the Message Batch.

### Returns

- `DeletedMessageBatch`

  - `id: string`

    ID of the Message Batch.

  - `type: "message_batch_deleted"`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `"message_batch_deleted"`

### Example

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: 'my-anthropic-api-key',
});

const deletedMessageBatch = await client.messages.batches.delete('message_batch_id');

console.log(deletedMessageBatch.id);
```
