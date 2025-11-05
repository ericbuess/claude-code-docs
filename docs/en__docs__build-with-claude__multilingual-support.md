# Multilingual support

> Claude excels at tasks across multiple languages, maintaining strong cross-lingual performance relative to English.

## Overview

Claude demonstrates robust multilingual capabilities, with particularly strong performance in zero-shot tasks across languages. The model maintains consistent relative performance across both widely-spoken and lower-resource languages, making it a reliable choice for multilingual applications.

Note that Claude is capable in many languages beyond those benchmarked below. We encourage testing with any languages relevant to your specific use cases.

## Performance data

Below are the zero-shot chain-of-thought evaluation scores for Claude 4, Claude 3.7 Sonnet and Claude 3.5 models across different languages, shown as a percent relative to English performance (100%):

| Language                          | Claude Opus 4<sup>1</sup> | Claude Sonnet 4<sup>1</sup> | Claude Sonnet 3.7 ([deprecated](/en/docs/about-claude/model-deprecations))<sup>1</sup> | Claude Haiku 3.5 |
| --------------------------------- | ------------------------- | --------------------------- | -------------------------------------------------------------------------------------- | ---------------- |
| English (baseline, fixed to 100%) | 100%                      | 100%                        | 100%                                                                                   | 100%             |
| Spanish                           | 98.0%                     | 97.5%                       | 97.6%                                                                                  | 94.6%            |
| Portuguese (Brazil)               | 97.3%                     | 97.2%                       | 97.3%                                                                                  | 94.6%            |
| Italian                           | 97.5%                     | 97.3%                       | 97.2%                                                                                  | 95.0%            |
| French                            | 97.7%                     | 97.1%                       | 96.9%                                                                                  | 95.3%            |
| Indonesian                        | 97.2%                     | 96.2%                       | 96.3%                                                                                  | 91.2%            |
| German                            | 97.1%                     | 94.7%                       | 96.2%                                                                                  | 92.5%            |
| Arabic                            | 96.9%                     | 96.1%                       | 95.4%                                                                                  | 84.7%            |
| Chinese (Simplified)              | 96.7%                     | 95.9%                       | 95.3%                                                                                  | 90.9%            |
| Korean                            | 96.4%                     | 95.9%                       | 95.2%                                                                                  | 89.1%            |
| Japanese                          | 96.2%                     | 95.6%                       | 95.0%                                                                                  | 90.8%            |
| Hindi                             | 96.7%                     | 95.8%                       | 94.2%                                                                                  | 80.1%            |
| Bengali                           | 95.2%                     | 94.4%                       | 92.4%                                                                                  | 72.9%            |
| Swahili                           | 89.5%                     | 87.1%                       | 89.2%                                                                                  | 64.7%            |
| Yoruba                            | 78.9%                     | 76.4%                       | 76.7%                                                                                  | 46.1%            |

<sup>1</sup> With [extended thinking](/en/docs/build-with-claude/extended-thinking).

<Note>
  These metrics are based on [MMLU (Massive Multitask Language Understanding)](https://en.wikipedia.org/wiki/MMLU) English test sets that were translated into 14 additional languages by professional human translators, as documented in [OpenAI's simple-evals repository](https://github.com/openai/simple-evals/blob/main/multilingual_mmlu_benchmark_results.md). The use of human translators for this evaluation ensures high-quality translations, particularly important for languages with fewer digital resources.
</Note>

***

## Best practices

When working with multilingual content:

1. **Provide clear language context**: While Claude can detect the target language automatically, explicitly stating the desired input/output language improves reliability. For enhanced fluency, you can prompt Claude to use "idiomatic speech as if it were a native speaker."
2. **Use native scripts**: Submit text in its native script rather than transliteration for optimal results
3. **Consider cultural context**: Effective communication often requires cultural and regional awareness beyond pure translation

We also suggest following our general [prompt engineering guidelines](/en/docs/build-with-claude/prompt-engineering/overview) to better improve Claude's performance.

***

## Language support considerations

* Claude processes input and generates output in most world languages that use standard Unicode characters
* Performance varies by language, with particularly strong capabilities in widely-spoken languages
* Even in languages with fewer digital resources, Claude maintains meaningful capabilities

<CardGroup cols={2}>
  <Card title="Prompt Engineering Guide" icon="pen" href="/en/docs/build-with-claude/prompt-engineering/overview">
    Master the art of prompt crafting to get the most out of Claude.
  </Card>

  <Card title="Prompt Library" icon="books" href="/en/resources/prompt-library">
    Find a wide range of pre-crafted prompts for various tasks and industries. Perfect for inspiration or quick starts.
  </Card>
</CardGroup>
