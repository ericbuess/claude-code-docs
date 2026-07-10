# Multilingual support

Claude excels at tasks across multiple languages, maintaining strong cross-lingual performance relative to English.

---

## Overview

Claude demonstrates robust multilingual capabilities, with particularly strong performance in zero-shot tasks across languages. The model maintains consistent relative performance across both widely spoken and lower-resource languages, making it a reliable choice for multilingual applications.

Claude is capable in many languages beyond those benchmarked in the following table. Test with any languages relevant to your specific use cases.

## Performance data

The following table shows zero-shot chain-of-thought evaluation scores for Claude models across languages, expressed as a percentage relative to English performance (100%):

| Language                          | Claude Opus 4.1 (deprecated)1 | Claude Sonnet 4.51 | Claude Haiku 4.51 |
| --------------------------------- | ----------------------------- | ------------------ | ----------------- |
| English (baseline, fixed to 100%) | 100%                          | 100%               | 100%              |
| Spanish                           | 98.1%                         | 98.2%              | 96.4%             |
| Portuguese (Brazil)               | 97.8%                         | 97.8%              | 96.1%             |
| Italian                           | 97.7%                         | 97.9%              | 96.0%             |
| French                            | 97.9%                         | 97.5%              | 95.7%             |
| Indonesian                        | 97.3%                         | 97.3%              | 94.2%             |
| German                            | 97.7%                         | 97.0%              | 94.3%             |
| Arabic                            | 97.1%                         | 97.2%              | 92.5%             |
| Chinese (Simplified)              | 97.1%                         | 96.9%              | 94.2%             |
| Korean                            | 96.6%                         | 96.7%              | 93.3%             |
| Japanese                          | 96.9%                         | 96.8%              | 93.5%             |
| Hindi                             | 96.8%                         | 96.7%              | 92.4%             |
| Bengali                           | 95.7%                         | 95.4%              | 90.4%             |
| Swahili                           | 89.8%                         | 91.1%              | 78.3%             |
| Yoruba                            | 80.3%                         | 79.7%              | 52.7%             |

1 With [extended thinking](/docs/en/build-with-claude/extended-thinking).

<Note>
  These metrics are based on [MMLU (Massive Multitask Language Understanding)](https://en.wikipedia.org/wiki/MMLU) English test sets that were translated into 14 additional languages by professional human translators, as documented in [OpenAI's simple-evals repository](https://github.com/openai/simple-evals/blob/main/multilingual_mmlu_benchmark_results.md). The use of human translators for this evaluation ensures high-quality translations, particularly important for languages with fewer digital resources.
</Note>

***

## Set the response language

Claude infers the response language from the conversation, but for production applications you should state the target language explicitly. The most reliable place to do this is the system prompt, which keeps the instruction stable across every turn of a conversation.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "system": "Always respond in French, regardless of the language the user writes in.",
      "messages": [
        {"role": "user", "content": "How do I reset my password?"}
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --system "Always respond in French, regardless of the language the user writes in." \
    --message '{role: user, content: "How do I reset my password?"}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      system="Always respond in French, regardless of the language the user writes in.",
      messages=[{"role": "user", "content": "How do I reset my password?"}],
  )

  print(message.content)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    system: "Always respond in French, regardless of the language the user writes in.",
    messages: [{ role: "user", content: "How do I reset my password?" }]
  });

  console.log(message.content);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      System = "Always respond in French, regardless of the language the user writes in.",
      Messages =
      [
          new() { Role = Role.User, Content = "How do I reset my password?" }
      ]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	System: []anthropic.TextBlockParam{
  		{Text: "Always respond in French, regardless of the language the user writes in."},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("How do I reset my password?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(message.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024)
      .system("Always respond in French, regardless of the language the user writes in.")
      .addUserMessage("How do I reset my password?")
      .build();

  Message message = client.messages().create(params);
  System.out.println(message.content());
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'How do I reset my password?']
      ],
      model: 'claude-opus-4-8',
      system: 'Always respond in French, regardless of the language the user writes in.',
  );

  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    system: "Always respond in French, regardless of the language the user writes in.",
    messages: [
      { role: "user", content: "How do I reset my password?" }
    ]
  )

  puts message.content
  ```
</CodeGroup>

If your application lets users pick a language at runtime, interpolate that choice into the system prompt rather than relying on Claude to infer it from the user's message. To translate between two specific languages, name both: `Translate the user's message from German to Korean. Respond with only the translation.`

***

## Best practices

When working with multilingual content:

1. **Provide clear language context:** Although Claude can detect the target language automatically, explicitly stating the desired input and output languages improves reliability. For enhanced fluency, you can prompt Claude to use "idiomatic speech as if it were a native speaker."
2. **Use native scripts:** Submit text in its native script rather than transliteration for optimal results.
3. **Consider cultural context:** Effective communication often requires cultural and regional awareness beyond pure translation.

Also follow the general guidance in [Prompt engineering overview](/docs/en/build-with-claude/prompt-engineering/overview) to further improve output quality.

***

## Language support considerations

* Claude processes input and generates output in most world languages that use standard Unicode characters.
* Performance varies by language, with particularly strong capabilities in widely spoken languages.
* Even in languages with fewer digital resources, Claude maintains meaningful capabilities.

## Next steps

<CardGroup cols={2}>
  <Card title="Prompt engineering overview" icon="edit" href="/docs/en/build-with-claude/prompt-engineering/overview">
    Apply general prompting techniques to improve multilingual output quality.
  </Card>

  <Card title="Customer support agent" icon="headset" href="/docs/en/about-claude/use-case-guides/customer-support-chat">
    Build a localized support chatbot using a language-constrained system prompt.
  </Card>

  <Card title="Models overview" icon="table" href="/docs/en/about-claude/models/overview">
    Compare model tiers to balance multilingual quality against cost and latency.
  </Card>

  <Card title="Define success criteria and build evaluations" icon="scales" href="/docs/en/test-and-evaluate/develop-tests">
    Evaluate translation and localization quality before you ship.
  </Card>
</CardGroup>
