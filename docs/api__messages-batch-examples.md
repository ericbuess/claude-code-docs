# Message Batches examples

> Example usage for the Message Batches API

The Message Batches API supports the same set of features as the Messages API. While this page focuses on how to use the Message Batches API, see [Messages API examples](/en/api/messages-examples) for examples of the Messages API feature set.

## Creating a Message Batch

<CodeGroup>
  ```Python Python
  import anthropic
  from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
  from anthropic.types.messages.batch_create_params import Request

  client = anthropic.Anthropic()

  message_batch = client.messages.batches.create(
      requests=[
          Request(
              custom_id="my-first-request",
              params=MessageCreateParamsNonStreaming(
                  model="claude-sonnet-4-5",
                  max_tokens=1024,
                  messages=[{
                      "role": "user",
                      "content": "Hello, world",
                  }]
              )
          ),
          Request(
              custom_id="my-second-request",
              params=MessageCreateParamsNonStreaming(
                  model="claude-sonnet-4-5",
                  max_tokens=1024,
                  messages=[{
                      "role": "user",
                      "content": "Hi again, friend",
                  }]
              )
          )
      ]
  )
  print(message_batch)
  ```

  ```TypeScript TypeScript
  import Anthropic from '@anthropic-ai/sdk';

  const anthropic = new Anthropic();

  const message_batch = await anthropic.messages.batches.create({
    requests: [{
      custom_id: "my-first-request",
      params: {
        model: "claude-sonnet-4-5",
        max_tokens: 1024,
        messages: [
          {"role": "user", "content": "Hello, Claude"}
        ]
      }
    }, {
      custom_id: "my-second-request",
      params: {
        model: "claude-sonnet-4-5",
        max_tokens: 1024,
        messages: [
          {"role": "user", "content": "Hi again, my friend"}
        ]
      }
    }]
  });
  console.log(message_batch);
  ```

  ```bash Shell
  #!/bin/sh
  curl https://api.anthropic.com/v1/messages/batches \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "content-type: application/json" \
      --data '{
          "requests": [
            {
                "custom_id": "my-first-request",
                "params": {
                    "model": "claude-sonnet-4-5",
                    "max_tokens": 1024,
                    "messages": [
                        {"role": "user", "content": "Hello, Claude"}
                    ]
                }
            },
            {
                "custom_id": "my-second-request",
                "params": {
                    "model": "claude-sonnet-4-5",
                    "max_tokens": 1024,
                    "messages": [
                        {"role": "user", "content": "Hi again, my friend"}
                    ]
                }
            }
        ]
      }'
  ```
</CodeGroup>

```JSON JSON
{
  "id": "msgbatch_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message_batch",
  "processing_status": "in_progress",
  "request_counts": {
    "processing": 2,
    "succeeded": 0,
    "errored": 0,
    "canceled": 0,
    "expired": 0
  },
  "ended_at": null,
  "created_at": "2024-09-24T18:37:24.100435Z",
  "expires_at": "2024-09-25T18:37:24.100435Z",
  "cancel_initiated_at": null,
  "results_url": null
}
```

## Polling for Message Batch completion

To poll a Message Batch, you'll need its `id`, which is provided in the response when [creating](#creating-a-message-batch) request or by [listing](#listing-all-message-batches-in-a-workspace) batches. Example `id`: `msgbatch_013Zva2CMHLNnXjNJJKqJ2EF`.

<CodeGroup>
  ```Python Python
  import anthropic

  client = anthropic.Anthropic()

  message_batch = None
  while True:
      message_batch = client.messages.batches.retrieve(
          MESSAGE_BATCH_ID
      )
      if message_batch.processing_status == "ended":
          break
                
      print(f"Batch {MESSAGE_BATCH_ID} is still processing...")
      time.sleep(60)
  print(message_batch)
  ```

  ```TypeScript TypeScript
  import Anthropic from '@anthropic-ai/sdk';

  const anthropic = new Anthropic();

  let messageBatch;
  while (true) {
    messageBatch = await anthropic.messages.batches.retrieve(
      MESSAGE_BATCH_ID
    );
    if (messageBatch.processing_status === 'ended') {
      break;
    }

    console.log(`Batch ${messageBatch} is still processing... waiting`);
    await new Promise(resolve => setTimeout(resolve, 60_000));
  }
  console.log(messageBatch);
  ```

  ```bash Shell
  #!/bin/sh

  until [[ $(curl -s "https://api.anthropic.com/v1/messages/batches/$MESSAGE_BATCH_ID" \
            --header "x-api-key: $ANTHROPIC_API_KEY" \
            --header "anthropic-version: 2023-06-01" \
            | grep -o '"processing_status":[[:space:]]*"[^"]*"' \
            | cut -d'"' -f4) == "ended" ]]; do
      echo "Batch $MESSAGE_BATCH_ID is still processing..."
      sleep 60
  done

  echo "Batch $MESSAGE_BATCH_ID has finished processing"
  ```
</CodeGroup>

## Listing all Message Batches in a Workspace

<CodeGroup>
  ```Python Python
  import anthropic

  client = anthropic.Anthropic()

  # Automatically fetches more pages as needed.
  for message_batch in client.messages.batches.list(
      limit=20
  ):
      print(message_batch)
  ```

  ```TypeScript TypeScript
  import Anthropic from '@anthropic-ai/sdk';

  const anthropic = new Anthropic();

  // Automatically fetches more pages as needed.
  for await (const messageBatch of anthropic.messages.batches.list({
    limit: 20
  })) {
    console.log(messageBatch);
  }
  ```

  ```bash Shell
  #!/bin/sh

  if ! command -v jq &> /dev/null; then
      echo "Error: This script requires jq. Please install it first."
      exit 1
  fi

  BASE_URL="https://api.anthropic.com/v1/messages/batches"

  has_more=true
  after_id=""

  while [ "$has_more" = true ]; do
      # Construct URL with after_id if it exists
      if [ -n "$after_id" ]; then
          url="${BASE_URL}?limit=20&after_id=${after_id}"
      else
          url="$BASE_URL?limit=20"
      fi

      response=$(curl -s "$url" \
                --header "x-api-key: $ANTHROPIC_API_KEY" \
                --header "anthropic-version: 2023-06-01")

      # Extract values using jq
      has_more=$(echo "$response" | jq -r '.has_more')
      after_id=$(echo "$response" | jq -r '.last_id')

      # Process and print each entry in the data array
      echo "$response" | jq -c '.data[]' | while read -r entry; do
          echo "$entry" | jq '.'
      done
  done
  ```
</CodeGroup>

```Markup Output
{
  "id": "msgbatch_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message_batch",
  ...
}
{
  "id": "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d",
  "type": "message_batch",
  ...
}
```

## Retrieving Message Batch Results

Once your Message Batch status is `ended`, you will be able to view the `results_url` of the batch and retrieve results in the form of a `.jsonl` file.

<CodeGroup>
  ```Python Python
  import anthropic

  client = anthropic.Anthropic()

  # Stream results file in memory-efficient chunks, processing one at a time
  for result in client.messages.batches.results(
      MESSAGE_BATCH_ID,
  ):
      print(result)
  ```

  ```TypeScript TypeScript
  import Anthropic from '@anthropic-ai/sdk';

  const anthropic = new Anthropic();

  // Stream results file in memory-efficient chunks, processing one at a time
  for await (const result of await anthropic.messages.batches.results(
      MESSAGE_BATCH_ID
  )) {
      console.log(result);
  }
  ```

  ```bash Shell
  #!/bin/sh
  curl "https://api.anthropic.com/v1/messages/batches/$MESSAGE_BATCH_ID" \
        --header "anthropic-version: 2023-06-01" \
        --header "x-api-key: $ANTHROPIC_API_KEY" \
  | grep -o '"results_url":[[:space:]]*"[^"]*"' \
  | cut -d'"' -f4 \
  | xargs curl \
        --header "anthropic-version: 2023-06-01" \
        --header "x-api-key: $ANTHROPIC_API_KEY"

  # Optionally, use jq for pretty-printed JSON:
  #| while IFS= read -r line; do
  #    echo "$line" | jq '.'
  #  done
  ```
</CodeGroup>

```Markup Output
{
  "id": "my-second-request",
  "result": {
    "type": "succeeded",
    "message": {
      "id": "msg_018gCsTGsXkYJVqYPxTgDHBU",
      "type": "message",
      ...
    }
  }
}
{
  "custom_id": "my-first-request",
  "result": {
    "type": "succeeded",
    "message": {
      "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
      "type": "message",
      ...
    }
  }
}
```

## Canceling a Message Batch

Immediately after cancellation, a batch's `processing_status` will be `canceling`. You can use the same [polling for batch completion](#polling-for-message-batch-completion) technique to poll for when cancellation is finalized as canceled batches also end up `ended` and may contain results.

<CodeGroup>
  ```Python Python
  import anthropic

  client = anthropic.Anthropic()

  message_batch = client.messages.batches.cancel(
      MESSAGE_BATCH_ID,
  )
  print(message_batch)
  ```

  ```TypeScript TypeScript
  import Anthropic from '@anthropic-ai/sdk';

  const anthropic = new Anthropic();

  const messageBatch = await anthropic.messages.batches.cancel(
      MESSAGE_BATCH_ID
  );
  console.log(messageBatch);
  ```

  ```bash Shell
  #!/bin/sh
  curl --request POST https://api.anthropic.com/v1/messages/batches/$MESSAGE_BATCH_ID/cancel \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01"
  ```
</CodeGroup>

```JSON JSON
{
  "id": "msgbatch_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message_batch",
  "processing_status": "canceling",
  "request_counts": {
    "processing": 2,
    "succeeded": 0,
    "errored": 0,
    "canceled": 0,
    "expired": 0
  },
  "ended_at": null,
  "created_at": "2024-09-24T18:37:24.100435Z",
  "expires_at": "2024-09-25T18:37:24.100435Z",
  "cancel_initiated_at": "2024-09-24T18:39:03.114875Z",
  "results_url": null
}
```
