# Prefill Claude's response for greater output control

---

<Note>
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](/docs/en/build-with-claude/prompt-engineering/extended-thinking-tips).
</Note>

<Note>
Prefilling is only available for non-extended thinking modes. It's not currently supported with extended thinking.
</Note>

When using Claude, you have the unique ability to guide its responses by prefilling the `Assistant` message. This powerful technique allows you to direct Claude's actions, skip preambles, enforce specific formats like JSON or XML, and even help Claude maintain character consistency in role-play scenarios.

In some cases where Claude is not performing as expected, a few prefilled sentences can vastly improve Claude's performance. A little prefilling goes a long way!

## How to prefill Claude's response

To prefill, include the desired initial text in the `Assistant` message (Claude's response will continue from where the `Assistant` message leaves off):

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is your favorite color?"},
        {"role": "assistant", "content": "As an AI assistant, I don't have a favorite color, But if I had to pick, it would be green because"}  # Prefill here
    ]
)
```

<Warning>
  The prefill content cannot end with trailing whitespace. A prefill like `"As an AI assistant, I "` (with a space at the end) will result in an error.
</Warning>

### Examples

#### Example 1: Controlling output formatting and skipping the preamble

<Tip>**Power user tip**: Prefilling `{` forces Claude to skip the preamble and directly output the JSON object. This is cleaner, more concise, and easier for programs to parse without additional processing.
For guaranteed JSON output that conforms to a specific schema, consider using [Structured Outputs](/docs/en/build-with-claude/structured-outputs) instead of prefilling. Structured outputs ensure Claude's response always matches your defined JSON schema, making it ideal for production applications that require strict format compliance.</Tip>

    <section title="Example: Structured data extraction without prefilling">

    | Role | Content |
    | ---- | ------- |
    | User | Extract the name, size, price, and color from this product description as a JSON object:<br/><br/>\<description><br/>The SmartHome Mini is a compact smart home assistant available in black or white for only \$49.99. At just 5 inches wide, it lets you control lights, thermostats, and other connected devices via voice or app—no matter where you place it in your home. This affordable little hub brings convenient hands-free control to your smart devices.<br/>\</description> |
    | Assistant | Here's the extracted information in JSON format:<br/><br/>\`\`\`json<br/>\{<br/>  "name": "SmartHome Mini",<br/>  "size": "5 inches wide",<br/>  "price": "\$49.99",<br/>  "colors": ["black", "white"]<br/>\}<br/>\`\`\`<br/><br/>I've extracted the following details from the product description:<br/>- **Name**: SmartHome Mini<br/>- **Size**: 5 inches wide<br/>- **Price**: \$49.99<br/>- **Colors**: Available in black and white<br/><br/>The JSON object provides a structured format that's easy for programs to parse and use. Let me know if you need any modifications or have any other questions! |
    
</section>

    <section title="Example: Structured data extraction with prefilling">

    | Role | Content |
    | ---- | ------- |
    | User | Extract the name, size, price, and color from this product description as a JSON object:<br/><br/>\<description><br/>The SmartHome Mini is a compact smart home assistant available in black or white for only \$49.99. At just 5 inches wide, it lets you control lights, thermostats, and other connected devices via voice or app—no matter where you place it in your home. This affordable little hub brings convenient hands-free control to your smart devices.<br/>\</description> |
    | Assistant (prefill) | \{ |
    | Assistant (Claude's response) | "name": "SmartHome Mini",<br/>"size": "5 inches wide",<br/>"price": "\$49.99",<br/>"colors": [<br/>  "black",<br/>  "white"<br/>]<br/>\} |
    
</section>

#### Example 2: Maintaining character in roleplay scenarios

<Tip>**Role-play tip**: Prefilling a bracketed `[ROLE_NAME]` can remind Claude stay in character, even for longer and more complex conversations. This is especially powerful when combined with role prompting in the `system` parameter.</Tip>

    <section title="Example: Maintaining character without role prompting">

    | Role | Content |
    | ---- | ------- |
    | User (50 conversation turns in with "Sherlock Holmes" Claude) | What do you deduce about the owner of this shoe? \<image>muddy_shoe.jpg\</image> |
    | Assistant | As an AI assistant, I would be happy to analyze the image of a muddy shoe as if you had provided it. Here's my deduction... |
    
</section>

    <section title="Example: Maintaining character with role prompting">

    | Role | Content |
    | ---- | ------- |
    | User (50 conversation turns in with "Sherlock Holmes" Claude) | What do you deduce about the owner of this shoe? <br/>\<image>muddy_shoe.jpg\</image> |
    | Assistant (prefill) | [Sherlock Holmes] |
    | Assistant (Claude's response) | Ah, what have we here? A most curious specimen, Watson! Let us examine this shoe with a discerning eye. The mud, you see, is not your common London clay, but rather the distinctive reddish hue of the iron-rich soil found only in the environs of Hampstead Heath. And yet, the wear on the sole suggests a gait more suited to the cobblestones of Whitechapel than the gentle slopes of the Heath.<br/><br/>Now, observe the laces! They are tied with a particular knot favored by those in the medical profession—doubtless a habit acquired during years of tying surgical gowns. But the scuff marks on the toe box tell a different tale: they are consistent with the kicking motion one might employ in the martial arts, specifically Baritsu.<br/><br/>We may conclude, then, that our absent shoe owner is a doctor, possibly a surgeon, who resides in Whitechapel but frequents Hampstead Heath—perhaps for a secret Baritsu practice, away from prying eyes. A most intriguing case, Watson! We must make haste; the game is afoot! |
    
</section>

---

<CardGroup cols={3}>
  <Card title="Working with Messages" icon="messages" href="/docs/en/build-with-claude/working-with-messages">
    See more examples of prefill and other Messages API patterns.
  </Card>
  <Card title="Prompt library" icon="link" href="/docs/en/resources/prompt-library/library">
    Get inspired by a curated selection of prompts for various tasks and use cases.
  </Card>
  <Card title="GitHub prompting tutorial" icon="link" href="https://github.com/anthropics/prompt-eng-interactive-tutorial">
    An example-filled tutorial that covers the prompt engineering concepts found in our docs.
  </Card>
  <Card title="Google Sheets prompting tutorial" icon="link" href="https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8">
    A lighter weight version of our prompt engineering tutorial via an interactive spreadsheet.
  </Card>
</CardGroup>