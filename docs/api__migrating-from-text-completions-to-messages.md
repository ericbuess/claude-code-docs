# Migrating from Text Completions

> Migrating from Text Completions to Messages

<Note>
  The Text Completions API has been deprecated in favor of the Messages API.
</Note>

When migrating from Text Completions to [Messages](/en/api/messages), consider the following changes.

### Inputs and outputs

The largest change between Text Completions and the Messages is the way in which you specify model inputs and receive outputs from the model.

With Text Completions, inputs are raw strings:

```Python Python
prompt = "\n\nHuman: Hello there\n\nAssistant: Hi, I'm Claude. How can I help?\n\nHuman: Can you explain Glycolysis to me?\n\nAssistant:"
```

With Messages, you specify a list of input messages instead of a raw prompt:

<CodeGroup>
  ```json Shorthand
  messages = [
    {"role": "user", "content": "Hello there."},
    {"role": "assistant", "content": "Hi, I'm Claude. How can I help?"},
    {"role": "user", "content": "Can you explain Glycolysis to me?"},
  ]
  ```

  ```json Expanded
  messages = [
    {"role": "user", "content": [{"type": "text", "text": "Hello there."}]},
    {"role": "assistant", "content": [{"type": "text", "text": "Hi, I'm Claude. How can I help?"}]},
    {"role": "user", "content":[{"type": "text", "text": "Can you explain Glycolysis to me?"}]},
  ]
  ```
</CodeGroup>

Each input message has a `role` and `content`.

<Tip>
  **Role names**

  The Text Completions API expects alternating `\n\nHuman:` and `\n\nAssistant:` turns, but the Messages API expects `user` and `assistant` roles. You may see documentation referring to either "human" or "user" turns. These refer to the same role, and will be "user" going forward.
</Tip>

With Text Completions, the model's generated text is returned in the `completion` values of the response:

```Python Python
>>> response = anthropic.completions.create(...)
>>> response.completion
" Hi, I'm Claude"
```

With Messages, the response is the `content` value, which is a list of content blocks:

```Python Python
>>> response = anthropic.messages.create(...)
>>> response.content
[{"type": "text", "text": "Hi, I'm Claude"}]
```

### Putting words in Claude's mouth

With Text Completions, you can pre-fill part of Claude's response:

```Python Python
prompt = "\n\nHuman: Hello\n\nAssistant: Hello, my name is"
```

With Messages, you can achieve the same result by making the last input message have the `assistant` role:

```Python Python
messages = [
  {"role": "human", "content": "Hello"},
  {"role": "assistant", "content": "Hello, my name is"},
]
```

When doing so, response `content` will continue from the last input message `content`:

```JSON JSON
{
  "role": "assistant",
  "content": [{"type": "text", "text": " Claude. How can I assist you today?" }],
  ...
}
```

### System prompt

With Text Completions, the [system prompt](/en/docs/build-with-claude/prompt-engineering/system-prompts) is specified by adding text before the first `\n\nHuman:` turn:

```Python Python
prompt = "Today is January 1, 2024.\n\nHuman: Hello, Claude\n\nAssistant:"
```

With Messages, you specify the system prompt with the `system` parameter:

```Python Python
anthropic.Anthropic().messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="Today is January 1, 2024.", # <-- system prompt
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
```

### Model names

The Messages API requires that you specify the full model version (e.g. `claude-sonnet-4-5-20250929`).

We previously supported specifying only the major version number (e.g. `claude-2`), which resulted in automatic upgrades to minor versions. However, we no longer recommend this integration pattern, and Messages do not support it.

### Stop reason

Text Completions always have a `stop_reason` of either:

* `"stop_sequence"`: The model either ended its turn naturally, or one of your custom stop sequences was generated.
* `"max_tokens"`: Either the model generated your specified `max_tokens` of content, or it reached its [absolute maximum](/en/docs/about-claude/models/overview#model-comparison-table).

Messages have a `stop_reason` of one of the following values:

* `"end_turn"`: The conversational turn ended naturally.
* `"stop_sequence"`: One of your specified custom stop sequences was generated.
* `"max_tokens"`: (unchanged)

### Specifying max tokens

* Text Completions: `max_tokens_to_sample` parameter. No validation, but capped values per-model.
* Messages: `max_tokens` parameter. If passing a value higher than the model supports, returns a validation error.

### Streaming format

When using `"stream": true` in with Text Completions, the response included any of `completion`, `ping`, and `error` server-sent-events.

Messages can contain multiple content blocks of varying types, and so its streaming format is somewhat more complex. See [Messages streaming](/en/docs/build-with-claude/streaming) for details.
