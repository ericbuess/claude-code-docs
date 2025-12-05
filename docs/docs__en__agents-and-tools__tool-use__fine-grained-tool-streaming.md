# Fine-grained tool streaming

---

Tool use now supports fine-grained [streaming](/docs/en/build-with-claude/streaming) for parameter values. This allows developers to stream tool use parameters without buffering / JSON validation, reducing the latency to begin receiving large parameters.

Fine-grained tool streaming is available via the Claude API, AWS Bedrock, Google Cloud's Vertex AI, and Microsoft Foundry.

<Note>
Fine-grained tool streaming is a beta feature. Please make sure to evaluate your responses before using it in production. 

Please use [this form](https://forms.gle/D4Fjr7GvQRzfTZT96) to provide feedback on the quality of the model responses, the API itself, or the quality of the documentation—we cannot wait to hear from you!
</Note>

<Warning>
When using fine-grained tool streaming, you may potentially receive invalid or partial JSON inputs. Please make sure to account for these edge cases in your code.
</Warning>
## How to use fine-grained tool streaming
To use this beta feature, simply add the beta header `fine-grained-tool-streaming-2025-05-14` to a tool use request and turn on streaming.

Here's an example of how to use fine-grained tool streaming with the API:

<CodeGroup>

  ```bash Shell
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: fine-grained-tool-streaming-2025-05-14" \
    -d '{
      "model": "claude-sonnet-4-5",
      "max_tokens": 65536,
      "tools": [
        {
          "name": "make_file",
          "description": "Write text to a file",
          "input_schema": {
            "type": "object",
            "properties": {
              "filename": {
                "type": "string",
                "description": "The filename to write text to"
              },
              "lines_of_text": {
                "type": "array",
                "description": "An array of lines of text to write to the file"
              }
            },
            "required": ["filename", "lines_of_text"]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "Can you write a long poem and make a file called poem.txt?"
        }
      ],
      "stream": true
    }' | jq '.usage'
  ```

  ```python Python
  import anthropic

  client = anthropic.Anthropic()

  response = client.beta.messages.stream(
      max_tokens=65536,
      model="claude-sonnet-4-5",
      tools=[{
        "name": "make_file",
        "description": "Write text to a file",
        "input_schema": {
          "type": "object",
          "properties": {
            "filename": {
              "type": "string",
              "description": "The filename to write text to"
            },
            "lines_of_text": {
              "type": "array",
              "description": "An array of lines of text to write to the file"
            }
          },
          "required": ["filename", "lines_of_text"]
        }
      }],
      messages=[{
        "role": "user",
        "content": "Can you write a long poem and make a file called poem.txt?"
      }],
      betas=["fine-grained-tool-streaming-2025-05-14"]
  )

  print(response.usage)
  ```

  ```typescript TypeScript
  import Anthropic from '@anthropic-ai/sdk';

  const anthropic = new Anthropic();

  const message = await anthropic.beta.messages.stream({
    model: "claude-sonnet-4-5",
    max_tokens: 65536,
    tools: [{
      "name": "make_file",
      "description": "Write text to a file",
      "input_schema": {
        "type": "object",
        "properties": {
          "filename": {
            "type": "string",
            "description": "The filename to write text to"
          },
          "lines_of_text": {
            "type": "array",
            "description": "An array of lines of text to write to the file"
          }
        },
        "required": ["filename", "lines_of_text"]
      }
    }],
    messages: [{ 
      role: "user", 
      content: "Can you write a long poem and make a file called poem.txt?" 
    }],
    betas: ["fine-grained-tool-streaming-2025-05-14"]
  });

  console.log(message.usage);
  ```
</CodeGroup>

In this example, fine-grained tool streaming enables Claude to stream the lines of a long poem into the tool call `make_file` without buffering to validate if the `lines_of_text` parameter is valid JSON. This means you can see the parameter stream as it arrives, without having to wait for the entire parameter to buffer and validate.

<Note>
With fine-grained tool streaming, tool use chunks start streaming faster, and are often longer and contain fewer word breaks. This is due to differences in chunking behavior.

Example: 

Without fine-grained streaming (15s delay):
```
Chunk 1: '{"'
Chunk 2: 'query": "Ty'
Chunk 3: 'peScri'
Chunk 4: 'pt 5.0 5.1 '
Chunk 5: '5.2 5'
Chunk 6: '.3'
Chunk 8: ' new f'
Chunk 9: 'eatur'
...
```

With fine-grained streaming (3s delay):
```
Chunk 1: '{"query": "TypeScript 5.0 5.1 5.2 5.3'
Chunk 2: ' new features comparison'
```
</Note>

<Warning>
Because fine-grained streaming sends parameters without buffering or JSON validation, there is no guarantee that the resulting stream will complete in a valid JSON string.
Particularly, if the [stop reason](/docs/en/build-with-claude/handling-stop-reasons) `max_tokens` is reached, the stream may end midway through a parameter and may be incomplete. You will generally have to write specific support to handle when `max_tokens` is reached.
</Warning>

## Handling invalid JSON in tool responses

When using fine-grained tool streaming, you may receive invalid or incomplete JSON from the model. If you need to pass this invalid JSON back to the model in an error response block, you may wrap it in a JSON object to ensure proper handling (with a reasonable key). For example:

```json
{
  "INVALID_JSON": "<your invalid json string>"
}
```

This approach helps the model understand that the content is invalid JSON while preserving the original malformed data for debugging purposes.

<Note>
When wrapping invalid JSON, make sure to properly escape any quotes or special characters in the invalid JSON string to maintain valid JSON structure in the wrapper object.
</Note>