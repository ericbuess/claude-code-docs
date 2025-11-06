# Use our prompt improver to optimize your prompts

<Note>
  Our prompt improver is compatible with all Claude models, including those with extended thinking capabilities. For prompting tips specific to extended thinking models, see [here](/en/docs/build-with-claude/extended-thinking).
</Note>

The prompt improver helps you quickly iterate and improve your prompts through automated analysis and enhancement. It excels at making prompts more robust for complex tasks that require high accuracy.

<Frame>
  <img src="https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt_improver.png?fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=01479d382e45cc5cdec882d53f3bbf87" data-og-width="1210" width="1210" data-og-height="498" height="498" data-path="images/prompt_improver.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt_improver.png?w=280&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=a8a5e551ed73c52fa522a558f07b1a68 280w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt_improver.png?w=560&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=425bc1825e1a95df7b9c419eb4d2ccdc 560w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt_improver.png?w=840&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=73e7bcf8692fa22632c26c34ebef281f 840w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt_improver.png?w=1100&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=06b64cdc47098cb8bf1fb68cbe9212a5 1100w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt_improver.png?w=1650&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=0373ee302a7fb52d64fee13d0a3d5dc4 1650w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt_improver.png?w=2500&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=94ecf75d5241f3e68a6dbf2137f447a4 2500w" />
</Frame>

## Before you begin

You'll need:

* A [prompt template](/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables) to improve
* Feedback on current issues with Claude's outputs (optional but recommended)
* Example inputs and ideal outputs (optional but recommended)

## How the prompt improver works

The prompt improver enhances your prompts in 4 steps:

1. **Example identification**: Locates and extracts examples from your prompt template
2. **Initial draft**: Creates a structured template with clear sections and XML tags
3. **Chain of thought refinement**: Adds and refines detailed reasoning instructions
4. **Example enhancement**: Updates examples to demonstrate the new reasoning process

You can watch these steps happen in real-time in the improvement modal.

## What you get

The prompt improver generates templates with:

* Detailed chain-of-thought instructions that guide Claude's reasoning process and typically improve its performance
* Clear organization using XML tags to separate different components
* Standardized example formatting that demonstrates step-by-step reasoning from input to output
* Strategic prefills that guide Claude's initial responses

<Note>
  While examples appear separately in the Workbench UI, they're included at the start of the first user message in the actual API call. View the raw format by clicking "**\</> Get Code**" or insert examples as raw text via the Examples box.
</Note>

## How to use the prompt improver

1. Submit your prompt template
2. Add any feedback about issues with Claude's current outputs (e.g., "summaries are too basic for expert audiences")
3. Include example inputs and ideal outputs
4. Review the improved prompt

## Generate test examples

Don't have examples yet? Use our [Test Case Generator](/en/docs/test-and-evaluate/eval-tool#creating-test-cases) to:

1. Generate sample inputs
2. Get Claude's responses
3. Edit the responses to match your ideal outputs
4. Add the polished examples to your prompt

## When to use the prompt improver

The prompt improver works best for:

* Complex tasks requiring detailed reasoning
* Situations where accuracy is more important than speed
* Problems where Claude's current outputs need significant improvement

<Note>
  For latency or cost-sensitive applications, consider using simpler prompts. The prompt improver creates templates that produce longer, more thorough, but slower responses.
</Note>

## Example improvement

Here's how the prompt improver enhances a basic classification prompt:

<Accordion title="Original prompt">
  ```
  From the following list of Wikipedia article titles, identify which article this sentence came from.
  Respond with just the article title and nothing else.

  Article titles:
  {{titles}}

  Sentence to classify:
  {{sentence}}
  ```
</Accordion>

<Accordion title="Improved prompt">
  ```
  You are an intelligent text classification system specialized in matching sentences to Wikipedia article titles. Your task is to identify which Wikipedia article a given sentence most likely belongs to, based on a provided list of article titles.

  First, review the following list of Wikipedia article titles:
  <article_titles>
  {{titles}}
  </article_titles>

  Now, consider this sentence that needs to be classified:
  <sentence_to_classify>
  {{sentence}}
  </sentence_to_classify>

  Your goal is to determine which article title from the provided list best matches the given sentence. Follow these steps:

  1. List the key concepts from the sentence
  2. Compare each key concept with the article titles
  3. Rank the top 3 most relevant titles and explain why they are relevant
  4. Select the most appropriate article title that best encompasses or relates to the sentence's content

  Wrap your analysis in <analysis> tags. Include the following:
  - List of key concepts from the sentence
  - Comparison of each key concept with the article titles
  - Ranking of top 3 most relevant titles with explanations
  - Your final choice and reasoning

  After your analysis, provide your final answer: the single most appropriate Wikipedia article title from the list.

  Output only the chosen article title, without any additional text or explanation.
  ```
</Accordion>

Notice how the improved prompt:

* Adds clear step-by-step reasoning instructions
* Uses XML tags to organize content
* Provides explicit output formatting requirements
* Guides Claude through the analysis process

## Troubleshooting

Common issues and solutions:

* **Examples not appearing in output**: Check that examples are properly formatted with XML tags and appear at the start of the first user message
* **Chain of thought too verbose**: Add specific instructions about desired output length and level of detail
* **Reasoning steps don't match your needs**: Modify the steps section to match your specific use case

***

## Next steps

<CardGroup cols={3}>
  <Card title="Prompt library" icon="link" href="/en/resources/prompt-library/library">
    Get inspired by example prompts for various tasks.
  </Card>

  <Card title="GitHub prompting tutorial" icon="link" href="https://github.com/anthropics/prompt-eng-interactive-tutorial">
    Learn prompting best practices with our interactive tutorial.
  </Card>

  <Card title="Test your prompts" icon="link" href="/en/docs/test-and-evaluate/eval-tool">
    Use our evaluation tool to test your improved prompts.
  </Card>
</CardGroup>
