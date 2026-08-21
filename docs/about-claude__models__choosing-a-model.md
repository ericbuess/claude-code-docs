---
title: Choosing the right model
url: https://platform.claude.com/docs/en/about-claude/models/choosing-a-model
description: "Selecting the optimal Claude model for your application involves balancing three key considerations: capabilities, speed, and cost. This guide helps you make an informed decision based on your specific requirements."
---

## Establish key criteria

When choosing a Claude model, consider first evaluating these factors:

* **Capabilities:** What specific features or capabilities will you need the model to have to meet your needs?
* **Speed:** How quickly does the model need to respond in your application? Claude Opus 5 and Claude Opus 4.8 support [fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) (research preview), which delivers up to 2.5x higher output speed at premium pricing.
* **Cost:** What's your budget for both development and production usage?
* **Effort:** Recent Opus and Sonnet models support an [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) that trades intelligence for latency and cost within a single model. Tuning effort is often a better lever than switching models. On Claude Opus 5, start with the default (`high`) and adjust up or down based on your evals. On Claude Opus 4.8 and Claude Opus 4.7, the `xhigh` effort level, between `high` and `max`, is the best setting for most coding and agentic use cases.

Knowing these answers in advance will make narrowing down and deciding which model to use much easier.

***

## Choose the best model to start with

There are two general approaches you can use to start testing which Claude model best works for your needs.

### Option 1: Start efficiency-first

For many applications, starting with a faster, more cost-effective model like Claude Haiku 4.5 can be the optimal approach:

1. Begin implementation with Claude Haiku 4.5.
2. Test your use case thoroughly.
3. Evaluate if performance meets your requirements.
4. Upgrade only if necessary for specific capability gaps.

This approach allows for quick iteration, lower development costs, and is often sufficient for many common applications. This approach is best for:

* Initial prototyping and development
* Applications with tight latency requirements
* Cost-sensitive implementations
* High-volume, straightforward tasks

### Option 2: Start capability-first

For complex tasks where intelligence and advanced capabilities are paramount, you may want to start capability-first: implement with the strongest starting point for your task, then optimize to more efficient models down the line:

1. Implement with Claude Opus 5.
2. [Optimize your prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) for this model.
3. Evaluate if performance meets your requirements.
4. Consider increasing efficiency by lowering [effort](https://platform.claude.com/docs/en/build-with-claude/effort) or downgrading models over time with greater workflow optimization.

This approach is best for:

* Complex reasoning tasks
* Scientific or mathematical applications
* Tasks requiring nuanced understanding
* Applications where accuracy outweighs cost considerations
* Advanced coding and high-autonomy agentic work

<Note>
  The [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) defaults to `high` on Claude Opus 5 and Claude Opus 4.8, including in Claude Code and the Messages API. On Claude Opus 5, start at the default and step up to `xhigh` for the most demanding coding and agentic work. On Claude Opus 4.8, use `xhigh` for coding, high-autonomy work, and the most intelligence-demanding tasks.
</Note>

**Claude Opus 5** (`claude-opus-5`) is a step-change improvement over Claude Opus 4.8, strong on deep reasoning, agentic and long-horizon tasks, and test-time compute scaling. Claude Opus 5 supports a 1M token context window by default and up to 128k output tokens, and is priced at $5 USD per million input tokens and $25 USD per million output tokens.

**Claude Fable 5** (`claude-fable-5`) is Anthropic's most capable widely released model, delivering next-generation intelligence for long-running agents. **Claude Mythos 5** (`claude-mythos-5`) is available through [Project Glasswing](https://anthropic.com/glasswing). Both models support a 1M token context window by default, up to 128k output tokens, and always-on [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking). See [Introducing Claude Fable 5 and Claude Mythos 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) for launch details.

Claude Fable 5 and Claude Mythos 5 are priced at $10 USD per million input tokens and $50 USD per million output tokens.

## Model selection matrix

| When you need...                                                                                             | Consider starting with... | Example use cases                                                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------ | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The highest available capability                                                                             | Claude Fable 5            | Long-running agents, deep reasoning, long-horizon agentic tasks, advanced research                                                                                |
| Complex agentic coding and enterprise work                                                                   | Claude Opus 5             | Multihour autonomous coding agents, large-scale refactoring, complex systems engineering, advanced research, knowledge work, vision-heavy workflows, computer use |
| Frontier intelligence at scale, built for coding, agents, and enterprise workflows                           | Claude Sonnet 5           | Code generation, data analysis, content creation, visual understanding, agentic tool use                                                                          |
| Near-frontier performance with lightning-fast speed and extended thinking at the most economical price point | Claude Haiku 4.5          | Real-time applications, high-volume intelligent processing, cost-sensitive deployments needing strong reasoning, sub-agent tasks                                  |

***

## Decide whether to upgrade or change models

To determine if you need to upgrade or change models, you should:

1. [Create benchmark tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) specific to your use case - having a good evaluation set is the most important step in the process.

2. Test with your actual prompts and data.

3. Compare performance across models for:

   * Accuracy of responses
   * Response quality
   * Handling of edge cases

4. Weigh performance and cost tradeoffs.

## Combine models

Multi-model strategies pair a lower-cost model with a frontier model so that most tokens are billed at the lower rate. The two common patterns are an executor that escalates hard decisions to an advisor, and an orchestrator that delegates bulk work to lower-cost workers. See [Optimizing for cost and intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence) for both strategies, measured examples, and implementation options.

## Next steps

<CardGroup cols={2}>
  <Card title="Model comparison chart" icon="settings" href="https://platform.claude.com/docs/en/about-claude/models/overview">
    See detailed specifications and pricing for the latest Claude models
  </Card>

  <Card title="What's new in Claude Opus 5" icon="sparkle" href="https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5">
    Explore the latest improvements in Claude Opus 5
  </Card>

  <Card title="What's new in Claude Sonnet 5" icon="sparkle" href="https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5">
    The best combination of speed and intelligence
  </Card>

  <Card title="Start building" icon="code" href="https://platform.claude.com/docs/en/get-started">
    Get started with your first API call
  </Card>
</CardGroup>
