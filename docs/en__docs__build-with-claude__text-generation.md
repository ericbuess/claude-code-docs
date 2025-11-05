# Text generation

> Claude excels in a wide range of text-based tasks. Claude has been trained to ingest code, prose, and other natural language inputs, and provide text outputs in response.

Prompts are best written as natural language queries as if you are instructing someone to do something, with the more detail the better. You can further improve your baseline prompt with [prompt engineering](/en/docs/build-with-claude/prompt-engineering/overview).

***

## Text capabilities and use cases

Claude has a broad range of text-based capabilities, including but not limited to:

| Capability                      | This enables you to...                                                                               |
| :------------------------------ | :--------------------------------------------------------------------------------------------------- |
| Text Summarization              | Distill lengthy content into key insights for executives, social media, or product teams.            |
| Content Generation              | Craft compelling content from blog posts and emails to marketing slogans and product descriptions.   |
| Data / Entity Extraction        | Uncover structured insights from unstructured text like reviews, news articles, or transcripts.      |
| Question Answering              | Build intelligent, interactive systems from customer support chatbots to educational AI tutors.      |
| Text Translation                | Seamlessly communicate across languages in products, support, and content creation.                  |
| Text Analysis & Recommendations | Understand sentiment, preferences, and patterns to personalize user experiences and offerings.       |
| Dialogue and Conversation       | Create engaging, context-aware interactions in games, virtual assistants, and storytelling apps.     |
| Code Explanation & Generation   | Accelerate development with instant code reviews, boilerplate generation, and interactive tutorials. |

***

## Claude Cookbook

Dive into practical examples and hands-on tutorials with our collection of Jupyter notebooks.

<CardGroup cols={3}>
  <Card title="PDF Upload & Summarization" icon="file-pdf" href="https://github.com/anthropics/anthropic-cookbook/blob/main/misc/pdf_upload_summarization.ipynb">
    Learn how to upload PDFs and have Claude summarize their content, making it easy to digest long documents.
  </Card>

  <Card title="Tool Use & Function Calling" icon="screwdriver-wrench" href="https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use">
    Discover how to extend Claude's capabilities by integrating external tools and functions into your workflows.
  </Card>

  <Card title="Embeddings with VoyageAI" icon="chart-scatter-3d" href="https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/VoyageAI/how_to_create_embeddings.md">
    Explore how to create and use embeddings with VoyageAI for advanced text similarity and search tasks.
  </Card>
</CardGroup>

## More Resources

From crafting the perfect prompt to understanding API details, we've got you covered.

<CardGroup cols={3}>
  <Card title="Prompt Engineering Guide" icon="pen" href="/en/docs/build-with-claude/prompt-engineering/overview">
    Master the art of prompt crafting to get the most out of Claude. Especially useful for fine-tuning with [legacy models](/en/docs/legacy-model-guide).
  </Card>

  <Card title="Prompt Library" icon="books" href="/en/resources/prompt-library">
    Find a wide range of pre-crafted prompts for various tasks and industries. Perfect for inspiration or quick starts.
  </Card>

  <Card title="API Documentation" icon="code" href="/en/api/overview">
    Everything you need to interact with Claude via our API: request formats, response handling, and troubleshooting.
  </Card>
</CardGroup>
