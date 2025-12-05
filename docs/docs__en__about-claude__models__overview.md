# Models overview

Claude is a family of state-of-the-art large language models developed by Anthropic. This guide introduces our models and compares their performance.

---

## Choosing a model

If you're unsure which model to use, we recommend starting with **Claude Sonnet 4.5**. It offers the best balance of intelligence, speed, and cost for most use cases, with exceptional performance in coding and agentic tasks.

All current Claude models support text and image input, text output, multilingual capabilities, and vision. Models are available via the Anthropic API, AWS Bedrock, and Google Vertex AI.

Once you've picked a model, [learn how to make your first API call](/docs/en/get-started).

### Latest models comparison

| Feature | Claude Sonnet 4.5 | Claude Haiku 4.5 | Claude Opus 4.5 |
|:--------|:------------------|:-----------------|:----------------|
| **Description** | Our smart model for complex agents and coding | Our fastest model with near-frontier intelligence | Premium model combining maximum intelligence with practical performance |
| **Claude API ID** | claude-sonnet-4-5-20250929 | claude-haiku-4-5-20251001 | claude-opus-4-5-20251101 |
| **Claude API alias**<sup>1</sup> | claude-sonnet-4-5 | claude-haiku-4-5 | claude-opus-4-5 |
| **AWS Bedrock ID** | anthropic.claude-sonnet-4-5-20250929-v1:0 | anthropic.claude-haiku-4-5-20251001-v1:0 | anthropic.claude-opus-4-5-20251101-v1:0 |
| **GCP Vertex AI ID** | claude-sonnet-4-5@20250929 | claude-haiku-4-5@20251001 | claude-opus-4-5@20251101 |
| **Pricing**<sup>2</sup> | \$3 / input MTok<br/>\$15 / output MTok | \$1 / input MTok<br/>\$5 / output MTok | \$5 / input MTok<br/>\$25 / output MTok |
| **[Extended thinking](/docs/en/build-with-claude/extended-thinking)** | Yes | Yes | Yes |
| **[Priority Tier](/docs/en/api/service-tiers)** | Yes | Yes | Yes |
| **Comparative latency** | Fast | Fastest | Moderate |
| **Context window** | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> / <br/> <Tooltip tooltipContent="~750K words \ ~3.4M unicode characters">1M tokens</Tooltip> (beta)<sup>3</sup> | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> |
| **Max output** | 64K tokens | 64K tokens | 64K tokens |
| **Reliable knowledge cutoff** | Jan 2025<sup>4</sup> | Feb 2025 | May 2025<sup>4</sup> |
| **Training data cutoff** | Jul 2025 | Jul 2025 | Aug 2025 |

_<sup>1 - Aliases automatically point to the most recent model snapshot. When we release new model snapshots, we migrate aliases to point to the newest version of a model, typically within a week of the new release. While aliases are useful for experimentation, we recommend using specific model versions (e.g., `claude-sonnet-4-5-20250929`) in production applications to ensure consistent behavior.</sup>_

_<sup>2 - See our [pricing page](/docs/en/about-claude/pricing) for complete pricing information including batch API discounts, prompt caching rates, extended thinking costs, and vision processing fees.</sup>_

_<sup>3 - Claude Sonnet 4.5 supports a [1M token context window](/docs/en/build-with-claude/context-windows#1m-token-context-window) when using the `context-1m-2025-08-07` beta header. [Long context pricing](/docs/en/about-claude/pricing#long-context-pricing) applies to requests exceeding 200K tokens.</sup>_

_<sup>4 - **Reliable knowledge cutoff** indicates the date through which a model's knowledge is most extensive and reliable. **Training data cutoff** is the broader date range of training data used. For example, Claude Sonnet 4.5 was trained on publicly available information through July 2025, but its knowledge is most extensive and reliable through January 2025. For more information, see [Anthropic's Transparency Hub](https://www.anthropic.com/transparency).</sup>_

<Note>Models with the same snapshot date (e.g., 20240620) are identical across all platforms and do not change. The snapshot date in the model name ensures consistency and allows developers to rely on stable performance across different environments.</Note>

<Note>Starting with **Claude Sonnet 4.5 and all future models**, AWS Bedrock and Google Vertex AI offer two endpoint types: **global endpoints** (dynamic routing for maximum availability) and **regional endpoints** (guaranteed data routing through specific geographic regions). For more information, see the [third-party platform pricing section](/docs/en/about-claude/pricing#third-party-platform-pricing).</Note>

<section title="Legacy models">

The following models are still available but we recommend migrating to current models for improved performance:

| Feature | Claude Opus 4.1 | Claude Sonnet 4 | Claude Sonnet 3.7 | Claude Opus 4 | Claude Haiku 3.5 | Claude Haiku 3 |
|:--------|:----------------|:----------------|:------------------|:--------------|:-----------------|:---------------|
| **Claude API ID** | claude-opus-4-1-20250805 | claude-sonnet-4-20250514 | claude-3-7-sonnet-20250219 | claude-opus-4-20250514 | claude-3-5-haiku-20241022 | claude-3-haiku-20240307 |
| **Claude API alias** | claude-opus-4-1 | claude-sonnet-4-0 | claude-3-7-sonnet-latest | claude-opus-4-0 | claude-3-5-haiku-latest | — |
| **AWS Bedrock ID** | anthropic.claude-opus-4-1-20250805-v1:0 | anthropic.claude-sonnet-4-20250514-v1:0 | anthropic.claude-3-7-sonnet-20250219-v1:0 | anthropic.claude-opus-4-20250514-v1:0 | anthropic.claude-3-5-haiku-20241022-v1:0 | anthropic.claude-3-haiku-20240307-v1:0 |
| **GCP Vertex AI ID** | claude-opus-4-1@20250805 | claude-sonnet-4@20250514 | claude-3-7-sonnet@20250219 | claude-opus-4@20250514 | claude-3-5-haiku@20241022 | claude-3-haiku@20240307 |
| **Pricing** | \$15 / input MTok<br/>\$75 / output MTok | \$3 / input MTok<br/>\$15 / output MTok | \$3 / input MTok<br/>\$15 / output MTok | \$15 / input MTok<br/>\$75 / output MTok | \$0.80 / input MTok<br/>\$4 / output MTok | \$0.25 / input MTok<br/>\$1.25 / output MTok |
| **[Extended thinking](/docs/en/build-with-claude/extended-thinking)** | Yes | Yes | Yes | Yes | No | No |
| **[Priority Tier](/docs/en/api/service-tiers)** | Yes | Yes | Yes | Yes | Yes | No |
| **Comparative latency** | Moderate | Fast | Fast | Moderate | Fastest | Fast |
| **Context window** | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> / <br/> <Tooltip tooltipContent="~750K words \ ~3.4M unicode characters">1M tokens</Tooltip> (beta)<sup>1</sup> | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> | <Tooltip tooltipContent="~150K words \ ~215K unicode characters">200K tokens</Tooltip> | <Tooltip tooltipContent="~150K words \ ~680K unicode characters">200K tokens</Tooltip> |
| **Max output** | 32K tokens | 64K tokens | 64K tokens / 128K tokens (beta)<sup>4</sup> | 32K tokens | 8K tokens | 4K tokens |
| **Reliable knowledge cutoff** | Jan 2025<sup>2</sup> | Jan 2025<sup>2</sup> | Oct 2024<sup>2</sup> | Jan 2025<sup>2</sup> | <sup>3</sup> | <sup>3</sup> |
| **Training data cutoff** | Mar 2025 | Mar 2025 | Nov 2024 | Mar 2025 | Jul 2024 | Aug 2023 |

_<sup>1 - Claude Sonnet 4 supports a [1M token context window](/docs/en/build-with-claude/context-windows#1m-token-context-window) when using the `context-1m-2025-08-07` beta header. [Long context pricing](/docs/en/about-claude/pricing#long-context-pricing) applies to requests exceeding 200K tokens.</sup>_

_<sup>2 - **Reliable knowledge cutoff** indicates the date through which a model's knowledge is most extensive and reliable. **Training data cutoff** is the broader date range of training data used.</sup>_

_<sup>3 - Some Haiku models have a single training data cutoff date.</sup>_

_<sup>4 - Include the beta header `output-128k-2025-02-19` in your API request to increase the maximum output token length to 128K tokens for Claude Sonnet 3.7. We strongly suggest using our [streaming Messages API](/docs/en/build-with-claude/streaming) to avoid timeouts when generating longer outputs. See our guidance on [long requests](/docs/en/api/errors#long-requests) for more details.</sup>_

</section>

## Prompt and output performance

Claude 4 models excel in:
- **Performance**: Top-tier results in reasoning, coding, multilingual tasks, long-context handling, honesty, and image processing. See the [Claude 4 blog post](http://www.anthropic.com/news/claude-4) for more information.
- **Engaging responses**: Claude models are ideal for applications that require rich, human-like interactions.

    - If you prefer more concise responses, you can adjust your prompts to guide the model toward the desired output length. Refer to our [prompt engineering guides](/docs/en/build-with-claude/prompt-engineering) for details.
    - For specific Claude 4 prompting best practices, see our [Claude 4 best practices guide](/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices).
- **Output quality**: When migrating from previous model generations to Claude 4, you may notice larger improvements in overall performance.

## Migrating to Claude 4.5

If you're currently using Claude 3 models, we recommend migrating to Claude 4.5 to take advantage of improved intelligence and enhanced capabilities. For detailed migration instructions, see [Migrating to Claude 4.5](/docs/en/about-claude/models/migrating-to-claude-4).

## Get started with Claude

If you're ready to start exploring what Claude can do for you, let's dive in! Whether you're a developer looking to integrate Claude into your applications or a user wanting to experience the power of AI firsthand, we've got you covered.

<Note>Looking to chat with Claude? Visit [claude.ai](http://www.claude.ai)!</Note>

<CardGroup cols={3}>
  <Card title="Intro to Claude" icon="check" href="/docs/en/intro">
    Explore Claude's capabilities and development flow.
  </Card>
  <Card title="Quickstart" icon="lightning" href="/docs/en/get-started">
    Learn how to make your first API call in minutes.
  </Card>
  <Card title="Claude Console" icon="code" href="/">
    Craft and test powerful prompts directly in your browser.
  </Card>
</CardGroup>

If you have any questions or need assistance, don't hesitate to reach out to our [support team](https://support.claude.com/) or consult the [Discord community](https://www.anthropic.com/discord).