# Build with Claude: Prompt Engineering

This guide covers best practices for prompt engineering with Claude.

## Key Principles

- Be clear and direct
- Use examples (multishot prompting)
- Let Claude think (chain of thought)
- Use XML tags for structure

## Code Example

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ]
)

print(message.content)
```

## Best Practices

1. Assign Claude a role
2. Provide context and examples
3. Break complex tasks into steps

For more information, see the [Build with Claude](/en/docs/build-with-claude) overview.
