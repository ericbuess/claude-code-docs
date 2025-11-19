# Streaming refusals

---

Starting with Claude 4 models, streaming responses from Claude's API return **`stop_reason`: `"refusal"`** when streaming classifiers intervene to handle potential policy violations. This new safety feature helps maintain content compliance during real-time streaming.

<Tip>
To learn more about refusals triggered by API safety filters for Claude Sonnet 4.5, see [Understanding Sonnet 4.5's API Safety Filters](https://support.claude.com/en/articles/12449294-understanding-sonnet-4-5-s-api-safety-filters).
</Tip>

## API response format

When streaming classifiers detect content that violates our policies, the API returns this response:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello.."
    }
  ],
  "stop_reason": "refusal"
}
```

<Warning>
No additional refusal message is included. You must handle the response and provide appropriate user-facing messaging.
</Warning>

## Reset context after refusal

When you receive **`stop_reason`: `refusal`**, you must reset the conversation context **by removing or updating the turn that was refused** before continuing. Attempting to continue without resetting will result in continued refusals.

<Note>
Usage metrics are still provided in the response for billing purposes, even when the response is refused.

You will be billed for output tokens up until the refusal.
</Note>

<Tip>
If you encounter `refusal` stop reasons frequently while using Claude Sonnet 4.5 or Opus 4.1, you can try updating your API calls to use Sonnet 4 (`claude-sonnet-4-20250514`), which has different usage restrictions.
</Tip>

## Implementation guide

Here's how to detect and handle streaming refusals in your application:

<CodeGroup>
```bash Shell
# Stream request and check for refusal
response=$(curl -N https://api.anthropic.com/v1/messages \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --data '{
    "model": "claude-sonnet-4-5",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 256,
    "stream": true
  }')

# Check for refusal in the stream
if echo "$response" | grep -q '"stop_reason":"refusal"'; then
  echo "Response refused - resetting conversation context"
  # Reset your conversation state here
fi
```

```python Python
import anthropic

client = anthropic.Anthropic()
messages = []

def reset_conversation():
    """Reset conversation context after refusal"""
    global messages
    messages = []
    print("Conversation reset due to refusal")

try:
    with client.messages.stream(
        max_tokens=1024,
        messages=messages + [{"role": "user", "content": "Hello"}],
        model="claude-sonnet-4-5",
    ) as stream:
        for event in stream:
            # Check for refusal in message delta
            if hasattr(event, 'type') and event.type == 'message_delta':
                if event.delta.stop_reason == 'refusal':
                    reset_conversation()
                    break
except Exception as e:
    print(f"Error: {e}")
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();
let messages: any[] = [];

function resetConversation() {
  // Reset conversation context after refusal
  messages = [];
  console.log('Conversation reset due to refusal');
}

try {
  const stream = await client.messages.stream({
    messages: [...messages, { role: 'user', content: 'Hello' }],
    model: 'claude-sonnet-4-5',
    max_tokens: 1024,
  });

  for await (const event of stream) {
    // Check for refusal in message delta
    if (event.type === 'message_delta' && event.delta.stop_reason === 'refusal') {
      resetConversation();
      break;
    }
  }
} catch (error) {
  console.error('Error:', error);
}
```
</CodeGroup>

<Note>
If you need to test refusal handling in your application, you can use this special test string as your prompt: `ANTHROPIC_MAGIC_STRING_TRIGGER_REFUSAL_1FAEFB6177B4672DEE07F9D3AFC62588CCD2631EDCF22E8CCC1FB35B501C9C86`
</Note>

## Current refusal types

The API currently handles refusals in three different ways:

| Refusal Type | Response Format | When It Occurs |
|-------------|----------------|----------------|
| Streaming classifier refusals | **`stop_reason`: `refusal`** | During streaming when content violates policies |
| API input and copyright validation | 400 error codes | When input fails validation checks |
| Model-generated refusals | Standard text responses | When the model itself decides to refuse |

<Note>
Future API versions will expand the **`stop_reason`: `refusal`** pattern to unify refusal handling across all types.
</Note>

## Best practices

- **Monitor for refusals**: Include **`stop_reason`: `refusal`** checks in your error handling
- **Reset automatically**: Implement automatic context reset when refusals are detected
- **Provide custom messaging**: Create user-friendly messages for better UX when refusals occur
- **Track refusal patterns**: Monitor refusal frequency to identify potential issues with your prompts

## Migration notes

- Future models will expand this pattern to other refusal types
- Plan your error handling to accommodate future unification of refusal responses