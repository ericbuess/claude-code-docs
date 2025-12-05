# Use examples (multishot prompting) to guide Claude's behavior

---

<Note>
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](/docs/en/build-with-claude/prompt-engineering/extended-thinking-tips).
</Note>

Examples are your secret weapon shortcut for getting Claude to generate exactly what you need. By providing a few well-crafted examples in your prompt, you can dramatically improve the accuracy, consistency, and quality of Claude's outputs.
This technique, known as few-shot or multishot prompting, is particularly effective for tasks that require structured outputs or adherence to specific formats.

<Tip>**Power up your prompts**: Include 3-5 diverse, relevant examples to show Claude exactly what you want. More examples = better performance, especially for complex tasks.</Tip>

## Why use examples?

- **Accuracy**: Examples reduce misinterpretation of instructions.
- **Consistency**: Examples enforce uniform structure and style.
- **Performance**: Well-chosen examples boost Claude's ability to handle complex tasks.

## Crafting effective examples

For maximum effectiveness, make sure that your examples are:
- **Relevant**: Your examples mirror your actual use case.
- **Diverse**: Your examples cover edge cases and potential challenges, and vary enough that Claude doesn't inadvertently pick up on unintended patterns.
- **Clear**: Your examples are wrapped in `<example>` tags (if multiple, nested within `<examples>` tags) for structure.

<Tip>Ask Claude to evaluate your examples for relevance, diversity, or clarity. Or have Claude generate more examples based on your initial set.</Tip>
<section title="Example: Analyzing customer feedback">

    Notice that in the "no examples" version, Claude does not list multiple options for each category, despite its written analysis indicating that there are multiple categories for certain feedback. It also includes a long explanation when we may not want it to.

    | Role | No Examples | With Examples |
    | --- | --- | --- |
    | User | Analyze this customer feedback and categorize the issues. Use these categories: UI/UX, Performance, Feature Request, Integration, Pricing, and Other. Also rate the sentiment (Positive/Neutral/Negative) and priority (High/Medium/Low).<br/><br/>Here is the feedback: \{\{FEEDBACK\}\} | Our CS team is overwhelmed with unstructured feedback. Your task is to analyze feedback and categorize issues for our product and engineering teams. Use these categories: UI/UX, Performance, Feature Request, Integration, Pricing, and Other. Also rate the sentiment (Positive/Neutral/Negative) and priority (High/Medium/Low). Here is an example:<br/><br/>\<example><br/>Input: The new dashboard is a mess! It takes forever to load, and I can't find the export button. Fix this ASAP!<br/>Category: UI/UX, Performance<br/>Sentiment: Negative<br/>Priority: High\</example><br/><br/>Now, analyze this feedback: \{\{FEEDBACK\}\} |
    | Assistant (Claude's response) | Here's the analysis of the customer feedback:<br/><br/>Issue: UI/UX<br/>Sentiment: Negative<br/>Priority: High<br/>The customer is frustrated with the new dashboard design, which they find cluttered and slow to load. They specifically call out the missing "export" button, which is likely a critical feature. This issue needs to be addressed as a high priority.<br/><br/>Issue: Integration<br/>Sentiment: Positive<br/>Priority: Medium<br/>The customer is pleased with the existing Salesforce integration but would like to see support for Hubspot as well. This is a feature request that could be considered for a future product update.<br/><br/>Issue: Pricing<br/>Sentiment: Negative<br/>Priority: High<br/>The customer finds the pricing to be unreasonable, especially for the basic features. They are threatening to switch to a competitor, so this is a high-priority issue that needs to be reviewed.<br/><br/>Issue: Performance<br/>Sentiment Negative<br/>Priority: High<br/>The customer is experiencing critical issues with the mobile app, where large file uploads consistently result in crashes. This is a significant problem that impacts the customer's ability to use the product effectively and should be addressed as a high priority.<br/><br/>Issue: UI/UX<br/>Sentiment: Positive<br/>Priority: Low<br/>The customer is overall satisfied with the product, specifically calling out the intuitive UI and excellent customer support. This is a positive piece of feedback that does not require any immediate action. | Here's the analysis of the customer feedback:<br/><br/>1. The new dashboard is a mess! It takes forever to load, and I can't find the export button. Fix this ASAP!<br/>Category: UI/UX, Performance<br/>Sentiment: Negative<br/>Priority: High<br/><br/>2. Love the Salesforce integration! But it'd be great if you could add Hubspot too.<br/>Category: Integration, Feature Request<br/>Sentiment: Positive<br/>Priority: Medium<br/><br/>3. Your pricing is ridiculous! $99/mo for basic features? I'm switching to Competitor X.<br/>Category: Pricing<br/>Sentiment: Negative<br/>Priority: High<br/><br/>4. The mobile app keeps crashing when I try to upload large files (>50MB). This is critical for our field agents.<br/>Category: Performance<br/>Sentiment: Negative<br/>Priority: High<br/><br/>5. Overall, I'm happy with the product. The UI is intuitive, and the customer support is top-notch. Keep it up!<br/>Category: UI/UX, Other (Customer Support)<br/>Sentiment: Positive<br/>Priority: Low |

</section>

***

<CardGroup cols={3}>
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