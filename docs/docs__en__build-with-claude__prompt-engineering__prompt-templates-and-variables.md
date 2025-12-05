# Use prompt templates and variables

---

When deploying an LLM-based application with Claude, your API calls will typically consist of two types of content:
- **Fixed content:** Static instructions or context that remain constant across multiple interactions
- **Variable content:** Dynamic elements that change with each request or conversation, such as:
    - User inputs
    - Retrieved content for Retrieval-Augmented Generation (RAG)
    - Conversation context such as user account history
    - System-generated data such as tool use results fed in from other independent calls to Claude

A **prompt template** combines these fixed and variable parts, using placeholders for the dynamic content. In the [Claude Console](/), these placeholders are denoted with **\{\{double brackets\}\}**, making them easily identifiable and allowing for quick testing of different values.

---

# When to use prompt templates and variables
You should always use prompt templates and variables when you expect any part of your prompt to be repeated in another call to Claude (only via the API or the [Claude Console](/). [claude.ai](https://claude.ai/) currently does not support prompt templates or variables).

Prompt templates offer several benefits:
- **Consistency:** Ensure a consistent structure for your prompts across multiple interactions
- **Efficiency:** Easily swap out variable content without rewriting the entire prompt
- **Testability:** Quickly test different inputs and edge cases by changing only the variable portion
- **Scalability:** Simplify prompt management as your application grows in complexity
- **Version control:** Easily track changes to your prompt structure over time by keeping tabs only on the core part of your prompt, separate from dynamic inputs

The [Claude Console](/) heavily uses prompt templates and variables in order to support features and tooling for all the above, such as with the:
- **[Prompt generator](/docs/en/build-with-claude/prompt-engineering/prompt-generator):** Decides what variables your prompt needs and includes them in the template it outputs
- **[Prompt improver](/docs/en/build-with-claude/prompt-engineering/prompt-improver):** Takes your existing template, including all variables, and maintains them in the improved template it outputs
- **[Evaluation tool](/docs/en/test-and-evaluate/eval-tool):** Allows you to easily test, scale, and track versions of your prompts by separating the variable and fixed portions of your prompt template

---

# Example prompt template

Let's consider a simple application that translates English text to Spanish. The translated text would be variable since you would expect this text to change between users or calls to Claude. This translated text could be dynamically retrieved from databases or the user's input.

Thus, for your translation app, you might use this simple prompt template:
```
Translate this text from English to Spanish: {{text}}
```

---

## Next steps

<CardGroup cols={2}>
  <Card title="Generate a prompt" icon="link" href="/docs/en/build-with-claude/prompt-engineering/prompt-generator">
    Learn about the prompt generator in the Claude Console and try your hand at getting Claude to generate a prompt for you.
  </Card>
  <Card title="Apply XML tags" icon="link" href="/docs/en/build-with-claude/prompt-engineering/use-xml-tags">
    If you want to level up your prompt variable game, wrap them in XML tags.
  </Card>
  <Card title="Claude Console" icon="link" href="/">
    Check out the myriad prompt development tools available in the Claude Console.
  </Card>
</CardGroup>