# Multilingual support

Claude excels at tasks across multiple languages, maintaining strong cross-lingual performance relative to English.

---

## Overview

Claude demonstrates robust multilingual capabilities, with particularly strong performance in zero-shot tasks across languages. The model maintains consistent relative performance across both widely-spoken and lower-resource languages, making it a reliable choice for multilingual applications.

Note that Claude is capable in many languages beyond those benchmarked below. We encourage testing with any languages relevant to your specific use cases.

## Performance data

Below are the zero-shot chain-of-thought evaluation scores for Claude models across different languages, shown as a percent relative to English performance (100%):

| Language | Claude Opus 4.1<sup>1</sup> | Claude Opus 4<sup>1</sup> | Claude Sonnet 4.5<sup>1</sup> | Claude Sonnet 4<sup>1</sup> | Claude Haiku 4.5<sup>1</sup> | Claude Haiku 3.5|
|----------|---------------|---------------|---------------|-----------------|------------------|------------------|
| English (baseline, fixed to 100%) | 100% | 100% | 100% | 100% | 100% | 100% |
| Spanish | 98.1% | 98.0% | 98.2% | 97.5% | 96.4% | 94.6% |
| Portuguese (Brazil) | 97.8% | 97.3% | 97.8% | 97.2% | 96.1% | 94.6% |
| Italian | 97.7% | 97.5% | 97.9% | 97.3% | 96.0% | 95.0% |
| French | 97.9% | 97.7% | 97.5% | 97.1% | 95.7% | 95.3% |
| Indonesian | 97.3% | 97.2% | 97.3% | 96.2% | 94.2% | 91.2% |
| German | 97.7% | 97.1% | 97.0% | 94.7% | 94.3% | 92.5% |
| Arabic | 97.1% | 96.9% | 97.2% | 96.1% | 92.5% | 84.7% |
| Chinese (Simplified) | 97.1% | 96.7% | 96.9% | 95.9% | 94.2% | 90.9% |
| Korean | 96.6% | 96.4% | 96.7% | 95.9% | 93.3% | 89.1% |
| Japanese | 96.9% | 96.2% | 96.8% | 95.6% | 93.5% | 90.8% |
| Hindi | 96.8% | 96.7% | 96.7% | 95.8% | 92.4% | 80.1% |
| Bengali | 95.7% | 95.2% | 95.4% | 94.4% | 90.4% | 72.9% |
| Swahili | 89.8% | 89.5% | 91.1% | 87.1% | 78.3% | 64.7% |
| Yoruba | 80.3% | 78.9% | 79.7% | 76.4% | 52.7% | 46.1% |

<sup>1</sup> With [extended thinking](/docs/en/build-with-claude/extended-thinking).

<Note>
These metrics are based on [MMLU (Massive Multitask Language Understanding)](https://en.wikipedia.org/wiki/MMLU) English test sets that were translated into 14 additional languages by professional human translators, as documented in [OpenAI's simple-evals repository](https://github.com/openai/simple-evals/blob/main/multilingual_mmlu_benchmark_results.md). The use of human translators for this evaluation ensures high-quality translations, particularly important for languages with fewer digital resources.
</Note>

***

## Best practices

When working with multilingual content:

1. **Provide clear language context**: While Claude can detect the target language automatically, explicitly stating the desired input/output language improves reliability. For enhanced fluency, you can prompt Claude to use "idiomatic speech as if it were a native speaker."
2. **Use native scripts**: Submit text in its native script rather than transliteration for optimal results
3. **Consider cultural context**: Effective communication often requires cultural and regional awareness beyond pure translation

We also suggest following our general [prompt engineering guidelines](/docs/en/build-with-claude/prompt-engineering/overview) to better improve Claude's performance.

***

## Language support considerations

- Claude processes input and generates output in most world languages that use standard Unicode characters
- Performance varies by language, with particularly strong capabilities in widely-spoken languages
- Even in languages with fewer digital resources, Claude maintains meaningful capabilities

<CardGroup cols={2}>
  <Card title="Prompt Engineering Guide" icon="edit" href="/docs/en/build-with-claude/prompt-engineering/overview">
    Master the art of prompt crafting to get the most out of Claude.
  </Card>
  <Card title="Prompt Library" icon="books" href="/docs/en/resources/prompt-library">
    Find a wide range of pre-crafted prompts for various tasks and industries. Perfect for inspiration or quick starts.
  </Card>
</CardGroup>