# Prompt caching

Prompt caching is a powerful feature that optimizes your API usage by allowing resuming from specific prefixes in your prompts. This approach significantly reduces processing time and costs for repetitive tasks or prompts with consistent elements.

Here's an example of how to implement prompt caching with the Messages API using a `cache_control` block:

<CodeGroup>
  ```bash Shell theme={null}
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-sonnet-4-5",
      "max_tokens": 1024,
      "system": [
        {
          "type": "text",
          "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
        },
        {
          "type": "text",
          "text": "<the entire contents of Pride and Prejudice>",
          "cache_control": {"type": "ephemeral"}
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "Analyze the major themes in Pride and Prejudice."
        }
      ]
    }'

  # Call the model again with the same inputs up to the cache checkpoint
  curl https://api.anthropic.com/v1/messages # rest of input
  ```

  ```python Python theme={null}
  import anthropic

  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-sonnet-4-5",
      max_tokens=1024,
      system=[
        {
          "type": "text",
          "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n",
        },
        {
          "type": "text",
          "text": "<the entire contents of 'Pride and Prejudice'>",
          "cache_control": {"type": "ephemeral"}
        }
      ],
      messages=[{"role": "user", "content": "Analyze the major themes in 'Pride and Prejudice'."}],
  )
  print(response.usage.model_dump_json())

  # Call the model again with the same inputs up to the cache checkpoint
  response = client.messages.create(.....)
  print(response.usage.model_dump_json())
  ```

  ```typescript TypeScript theme={null}
  import Anthropic from '@anthropic-ai/sdk';

  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-sonnet-4-5",
    max_tokens: 1024,
    system: [
      {
        type: "text",
        text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n",
      },
      {
        type: "text",
        text: "<the entire contents of 'Pride and Prejudice'>",
        cache_control: { type: "ephemeral" }
      }
    ],
    messages: [
      {
        role: "user",
        content: "Analyze the major themes in 'Pride and Prejudice'."
      }
    ]
  });
  console.log(response.usage);

  // Call the model again with the same inputs up to the cache checkpoint
  const new_response = await client.messages.create(...)
  console.log(new_response.usage);
  ```

  ```java Java theme={null}
  import java.util.List;

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.CacheControlEphemeral;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import com.anthropic.models.messages.TextBlockParam;

  public class PromptCachingExample {

      public static void main(String[] args) {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_4_20250514)
                  .maxTokens(1024)
                  .systemOfTextBlockParams(List.of(
                          TextBlockParam.builder()
                                  .text("You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n")
                                  .build(),
                          TextBlockParam.builder()
                                  .text("<the entire contents of 'Pride and Prejudice'>")
                                  .cacheControl(CacheControlEphemeral.builder().build())
                                  .build()
                  ))
                  .addUserMessage("Analyze the major themes in 'Pride and Prejudice'.")
                  .build();

          Message message = client.messages().create(params);
          System.out.println(message.usage());
      }
  }
  ```
</CodeGroup>

```JSON JSON theme={null}
{"cache_creation_input_tokens":188086,"cache_read_input_tokens":0,"input_tokens":21,"output_tokens":393}
{"cache_creation_input_tokens":0,"cache_read_input_tokens":188086,"input_tokens":21,"output_tokens":393}
```

In this example, the entire text of "Pride and Prejudice" is cached using the `cache_control` parameter. This enables reuse of this large text across multiple API calls without reprocessing it each time. Changing only the user message allows you to ask various questions about the book while utilizing the cached content, leading to faster responses and improved efficiency.

***

## How prompt caching works

When you send a request with prompt caching enabled:

1. The system checks if a prompt prefix, up to a specified cache breakpoint, is already cached from a recent query.
2. If found, it uses the cached version, reducing processing time and costs.
3. Otherwise, it processes the full prompt and caches the prefix once the response begins.

This is especially useful for:

* Prompts with many examples
* Large amounts of context or background information
* Repetitive tasks with consistent instructions
* Long multi-turn conversations

By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used.

<Note>
  If you find that 5 minutes is too short, Anthropic also offers a 1-hour cache duration [at additional cost](#pricing).

  For more information, see [1-hour cache duration](#1-hour-cache-duration).
</Note>

<Tip>
  **Prompt caching caches the full prefix**

  Prompt caching references the entire prompt - `tools`, `system`, and `messages` (in that order) up to and including the block designated with `cache_control`.
</Tip>

***

## Pricing

Prompt caching introduces a new pricing structure. The table below shows the price per million tokens for each supported model:

| Model                                                                      | Base Input Tokens | 5m Cache Writes | 1h Cache Writes | Cache Hits & Refreshes | Output Tokens |
| -------------------------------------------------------------------------- | ----------------- | --------------- | --------------- | ---------------------- | ------------- |
| Claude Opus 4.1                                                            | \$15 / MTok       | \$18.75 / MTok  | \$30 / MTok     | \$1.50 / MTok          | \$75 / MTok   |
| Claude Opus 4                                                              | \$15 / MTok       | \$18.75 / MTok  | \$30 / MTok     | \$1.50 / MTok          | \$75 / MTok   |
| Claude Sonnet 4.5                                                          | \$3 / MTok        | \$3.75 / MTok   | \$6 / MTok      | \$0.30 / MTok          | \$15 / MTok   |
| Claude Sonnet 4                                                            | \$3 / MTok        | \$3.75 / MTok   | \$6 / MTok      | \$0.30 / MTok          | \$15 / MTok   |
| Claude Sonnet 3.7 ([deprecated](/en/docs/about-claude/model-deprecations)) | \$3 / MTok        | \$3.75 / MTok   | \$6 / MTok      | \$0.30 / MTok          | \$15 / MTok   |
| Claude Haiku 4.5                                                           | \$1 / MTok        | \$1.25 / MTok   | \$2 / MTok      | \$0.10 / MTok          | \$5 / MTok    |
| Claude Haiku 3.5                                                           | \$0.80 / MTok     | \$1 / MTok      | \$1.6 / MTok    | \$0.08 / MTok          | \$4 / MTok    |
| Claude Opus 3 ([deprecated](/en/docs/about-claude/model-deprecations))     | \$15 / MTok       | \$18.75 / MTok  | \$30 / MTok     | \$1.50 / MTok          | \$75 / MTok   |
| Claude Haiku 3                                                             | \$0.25 / MTok     | \$0.30 / MTok   | \$0.50 / MTok   | \$0.03 / MTok          | \$1.25 / MTok |

<Note>
  The table above reflects the following pricing multipliers for prompt caching:

  * 5-minute cache write tokens are 1.25 times the base input tokens price
  * 1-hour cache write tokens are 2 times the base input tokens price
  * Cache read tokens are 0.1 times the base input tokens price
</Note>

***

## How to implement prompt caching

### Supported models

Prompt caching is currently supported on:

* Claude Opus 4.1
* Claude Opus 4
* Claude Sonnet 4.5
* Claude Sonnet 4
* Claude Sonnet 3.7
* Claude Haiku 4.5
* Claude Haiku 3.5
* Claude Haiku 3
* Claude Opus 3 ([deprecated](/en/docs/about-claude/model-deprecations))

### Structuring your prompt

Place static content (tool definitions, system instructions, context, examples) at the beginning of your prompt. Mark the end of the reusable content for caching using the `cache_control` parameter.

Cache prefixes are created in the following order: `tools`, `system`, then `messages`. This order forms a hierarchy where each level builds upon the previous ones.

#### How automatic prefix checking works

You can use just one cache breakpoint at the end of your static content, and the system will automatically find the longest matching sequence of cached blocks. Understanding how this works helps you optimize your caching strategy.

**Three core principles:**

1. **Cache keys are cumulative**: When you explicitly cache a block with `cache_control`, the cache hash key is generated by hashing all previous blocks in the conversation sequentially. This means the cache for each block depends on all content that came before it.

2. **Backward sequential checking**: The system checks for cache hits by working backwards from your explicit breakpoint, checking each previous block in reverse order. This ensures you get the longest possible cache hit.

3. **20-block lookback window**: The system only checks up to 20 blocks before each explicit `cache_control` breakpoint. After checking 20 blocks without a match, it stops checking and moves to the next explicit breakpoint (if any).

**Example: Understanding the lookback window**

Consider a conversation with 30 content blocks where you set `cache_control` only on block 30:

* **If you send block 31 with no changes to previous blocks**: The system checks block 30 (match!). You get a cache hit at block 30, and only block 31 needs processing.

* **If you modify block 25 and send block 31**: The system checks backwards from block 30 → 29 → 28... → 25 (no match) → 24 (match!). Since block 24 hasn't changed, you get a cache hit at block 24, and only blocks 25-30 need reprocessing.

* **If you modify block 5 and send block 31**: The system checks backwards from block 30 → 29 → 28... → 11 (check #20). After 20 checks without finding a match, it stops looking. Since block 5 is beyond the 20-block window, no cache hit occurs and all blocks need reprocessing. However, if you had set an explicit `cache_control` breakpoint on block 5, the system would continue checking from that breakpoint: block 5 (no match) → block 4 (match!). This allows a cache hit at block 4, demonstrating why you should place breakpoints before editable content.

**Key takeaway**: Always set an explicit cache breakpoint at the end of your conversation to maximize your chances of cache hits. Additionally, set breakpoints just before content blocks that might be editable to ensure those sections can be cached independently.

#### When to use multiple breakpoints

You can define up to 4 cache breakpoints if you want to:

* Cache different sections that change at different frequencies (e.g., tools rarely change, but context updates daily)
* Have more control over exactly what gets cached
* Ensure caching for content more than 20 blocks before your final breakpoint
* Place breakpoints before editable content to guarantee cache hits even when changes occur beyond the 20-block window

<Note>
  **Important limitation**: If your prompt has more than 20 content blocks before your cache breakpoint, and you modify content earlier than those 20 blocks, you won't get a cache hit unless you add additional explicit breakpoints closer to that content.
</Note>

### Cache limitations

The minimum cacheable prompt length is:

* 1024 tokens for Claude Opus 4.1, Claude Opus 4, Claude Sonnet 4.5, Claude Sonnet 4, Claude Sonnet 3.7 ([deprecated](/en/docs/about-claude/model-deprecations)), and Claude Opus 3 ([deprecated](/en/docs/about-claude/model-deprecations))
* 4096 tokens for Claude Haiku 4.5
* 2048 tokens for Claude Haiku 3.5 and Claude Haiku 3

Shorter prompts cannot be cached, even if marked with `cache_control`. Any requests to cache fewer than this number of tokens will be processed without caching. To see if a prompt was cached, see the response usage [fields](/en/docs/build-with-claude/prompt-caching#tracking-cache-performance).

For concurrent requests, note that a cache entry only becomes available after the first response begins. If you need cache hits for parallel requests, wait for the first response before sending subsequent requests.

Currently, "ephemeral" is the only supported cache type, which by default has a 5-minute lifetime.

### Understanding cache breakpoint costs

**Cache breakpoints themselves don't add any cost.** You are only charged for:

* **Cache writes**: When new content is written to the cache (25% more than base input tokens for 5-minute TTL)
* **Cache reads**: When cached content is used (10% of base input token price)
* **Regular input tokens**: For any uncached content

Adding more `cache_control` breakpoints doesn't increase your costs - you still pay the same amount based on what content is actually cached and read. The breakpoints simply give you control over what sections can be cached independently.

### What can be cached

Most blocks in the request can be designated for caching with `cache_control`. This includes:

* Tools: Tool definitions in the `tools` array
* System messages: Content blocks in the `system` array
* Text messages: Content blocks in the `messages.content` array, for both user and assistant turns
* Images & Documents: Content blocks in the `messages.content` array, in user turns
* Tool use and tool results: Content blocks in the `messages.content` array, in both user and assistant turns

Each of these elements can be marked with `cache_control` to enable caching for that portion of the request.

### What cannot be cached

While most request blocks can be cached, there are some exceptions:

* Thinking blocks cannot be cached directly with `cache_control`. However, thinking blocks CAN be cached alongside other content when they appear in previous assistant turns. When cached this way, they DO count as input tokens when read from cache.
* Sub-content blocks (like [citations](/en/docs/build-with-claude/citations)) themselves cannot be cached directly. Instead, cache the top-level block.

  In the case of citations, the top-level document content blocks that serve as the source material for citations can be cached. This allows you to use prompt caching with citations effectively by caching the documents that citations will reference.
* Empty text blocks cannot be cached.

### What invalidates the cache

Modifications to cached content can invalidate some or all of the cache.

As described in [Structuring your prompt](#structuring-your-prompt), the cache follows the hierarchy: `tools` → `system` → `messages`. Changes at each level invalidate that level and all subsequent levels.

The following table shows which parts of the cache are invalidated by different types of changes. ✘ indicates that the cache is invalidated, while ✓ indicates that the cache remains valid.

| What changes                                              | Tools cache | System cache | Messages cache | Impact                                                                                                                                                                                                                                                                                                                           |
| --------------------------------------------------------- | ----------- | ------------ | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tool definitions**                                      | ✘           | ✘            | ✘              | Modifying tool definitions (names, descriptions, parameters) invalidates the entire cache                                                                                                                                                                                                                                        |
| **Web search toggle**                                     | ✓           | ✘            | ✘              | Enabling/disabling web search modifies the system prompt                                                                                                                                                                                                                                                                         |
| **Citations toggle**                                      | ✓           | ✘            | ✘              | Enabling/disabling citations modifies the system prompt                                                                                                                                                                                                                                                                          |
| **Tool choice**                                           | ✓           | ✓            | ✘              | Changes to `tool_choice` parameter only affect message blocks                                                                                                                                                                                                                                                                    |
| **Images**                                                | ✓           | ✓            | ✘              | Adding/removing images anywhere in the prompt affects message blocks                                                                                                                                                                                                                                                             |
| **Thinking parameters**                                   | ✓           | ✓            | ✘              | Changes to extended thinking settings (enable/disable, budget) affect message blocks                                                                                                                                                                                                                                             |
| **Non-tool results passed to extended thinking requests** | ✓           | ✓            | ✘              | When non-tool results are passed in requests while extended thinking is enabled, all previously-cached thinking blocks are stripped from context, and any messages in context that follow those thinking blocks are removed from the cache. For more details, see [Caching with thinking blocks](#caching-with-thinking-blocks). |

### Tracking cache performance

Monitor cache performance using these API response fields, within `usage` in the response (or `message_start` event if [streaming](/en/docs/build-with-claude/streaming)):

* `cache_creation_input_tokens`: Number of tokens written to the cache when creating a new entry.
* `cache_read_input_tokens`: Number of tokens retrieved from the cache for this request.
* `input_tokens`: Number of input tokens which were not read from or used to create a cache (i.e., tokens after the last cache breakpoint).

<Note>
  **Understanding the token breakdown**

  The `input_tokens` field represents only the tokens that come **after the last cache breakpoint** in your request - not all the input tokens you sent.

  To calculate total input tokens:

  ```
  total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
  ```

  **Spatial explanation:**

  * `cache_read_input_tokens` = tokens before breakpoint already cached (reads)
  * `cache_creation_input_tokens` = tokens before breakpoint being cached now (writes)
  * `input_tokens` = tokens after your last breakpoint (not eligible for cache)

  **Example:** If you have a request with 100,000 tokens of cached content (read from cache), 0 tokens of new content being cached, and 50 tokens in your user message (after the cache breakpoint):

  * `cache_read_input_tokens`: 100,000
  * `cache_creation_input_tokens`: 0
  * `input_tokens`: 50
  * **Total input tokens processed**: 100,050 tokens

  This is important for understanding both costs and rate limits, as `input_tokens` will typically be much smaller than your total input when using caching effectively.
</Note>

### Best practices for effective caching

To optimize prompt caching performance:

* Cache stable, reusable content like system instructions, background information, large contexts, or frequent tool definitions.
* Place cached content at the prompt's beginning for best performance.
* Use cache breakpoints strategically to separate different cacheable prefix sections.
* Set cache breakpoints at the end of conversations and just before editable content to maximize cache hit rates, especially when working with prompts that have more than 20 content blocks.
* Regularly analyze cache hit rates and adjust your strategy as needed.

### Optimizing for different use cases

Tailor your prompt caching strategy to your scenario:

* Conversational agents: Reduce cost and latency for extended conversations, especially those with long instructions or uploaded documents.
* Coding assistants: Improve autocomplete and codebase Q\&A by keeping relevant sections or a summarized version of the codebase in the prompt.
* Large document processing: Incorporate complete long-form material including images in your prompt without increasing response latency.
* Detailed instruction sets: Share extensive lists of instructions, procedures, and examples to fine-tune Claude's responses.  Developers often include an example or two in the prompt, but with prompt caching you can get even better performance by including 20+ diverse examples of high quality answers.
* Agentic tool use: Enhance performance for scenarios involving multiple tool calls and iterative code changes, where each step typically requires a new API call.
* Talk to books, papers, documentation, podcast transcripts, and other longform content:  Bring any knowledge base alive by embedding the entire document(s) into the prompt, and letting users ask it questions.

### Troubleshooting common issues

If experiencing unexpected behavior:

* Ensure cached sections are identical and marked with cache\_control in the same locations across calls
* Check that calls are made within the cache lifetime (5 minutes by default)
* Verify that `tool_choice` and image usage remain consistent between calls
* Validate that you are caching at least the minimum number of tokens
* The system automatically checks for cache hits at previous content block boundaries (up to \~20 blocks before your breakpoint). For prompts with more than 20 content blocks, you may need additional `cache_control` parameters earlier in the prompt to ensure all content can be cached
* Verify that the keys in your `tool_use` content blocks have stable ordering as some languages (e.g. Swift, Go) randomize key order during JSON conversion, breaking caches

<Note>
  Changes to `tool_choice` or the presence/absence of images anywhere in the prompt will invalidate the cache, requiring a new cache entry to be created. For more details on cache invalidation, see [What invalidates the cache](#what-invalidates-the-cache).
</Note>

### Caching with thinking blocks

When using [extended thinking](/en/docs/build-with-claude/extended-thinking) with prompt caching, thinking blocks have special behavior:

**Automatic caching alongside other content**: While thinking blocks cannot be explicitly marked with `cache_control`, they get cached as part of the request content when you make subsequent API calls with tool results. This commonly happens during tool use when you pass thinking blocks back to continue the conversation.

**Input token counting**: When thinking blocks are read from cache, they count as input tokens in your usage metrics. This is important for cost calculation and token budgeting.

**Cache invalidation patterns**:

* Cache remains valid when only tool results are provided as user messages
* Cache gets invalidated when non-tool-result user content is added, causing all previous thinking blocks to be stripped
* This caching behavior occurs even without explicit `cache_control` markers

For more details on cache invalidation, see [What invalidates the cache](#what-invalidates-the-cache).

**Example with tool use**:

```
Request 1: User: "What's the weather in Paris?"
Response: [thinking_block_1] + [tool_use block 1]

Request 2:
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True]
Response: [thinking_block_2] + [text block 2]
# Request 2 caches its request content (not the response)
# The cache includes: user message, thinking_block_1, tool_use block 1, and tool_result_1

Request 3:
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [thinking_block_2] + [text block 2],
User: [Text response, cache=True]
# Non-tool-result user block causes all thinking blocks to be ignored
# This request is processed as if thinking blocks were never present
```

When a non-tool-result user block is included, it designates a new assistant loop and all previous thinking blocks are removed from context.

For more detailed information, see the [extended thinking documentation](/en/docs/build-with-claude/extended-thinking#understanding-thinking-block-caching-behavior).

***

## Cache storage and sharing

* **Organization Isolation**: Caches are isolated between organizations. Different organizations never share caches, even if they use identical prompts.

* **Exact Matching**: Cache hits require 100% identical prompt segments, including all text and images up to and including the block marked with cache control.

* **Output Token Generation**: Prompt caching has no effect on output token generation. The response you receive will be identical to what you would get if prompt caching was not used.

***

## 1-hour cache duration

If you find that 5 minutes is too short, Anthropic also offers a 1-hour cache duration [at additional cost](#pricing).

To use the extended cache, include `ttl` in the `cache_control` definition like this:

```JSON  theme={null}
"cache_control": {
    "type": "ephemeral",
    "ttl": "5m" | "1h"
}
```

The response will include detailed cache information like the following:

```JSON  theme={null}
{
    "usage": {
        "input_tokens": ...,
        "cache_read_input_tokens": ...,
        "cache_creation_input_tokens": ...,
        "output_tokens": ...,

        "cache_creation": {
            "ephemeral_5m_input_tokens": 456,
            "ephemeral_1h_input_tokens": 100,
        }
    }
}
```

Note that the current `cache_creation_input_tokens` field equals the sum of the values in the `cache_creation` object.

### When to use the 1-hour cache

If you have prompts that are used at a regular cadence (i.e., system prompts that are used more frequently than every 5 minutes), continue to use the 5-minute cache, since this will continue to be refreshed at no additional charge.

The 1-hour cache is best used in the following scenarios:

* When you have prompts that are likely used less frequently than 5 minutes, but more frequently than every hour. For example, when an agentic side-agent will take longer than 5 minutes, or when storing a long chat conversation with a user and you generally expect that user may not respond in the next 5 minutes.
* When latency is important and your follow up prompts may be sent beyond 5 minutes.
* When you want to improve your rate limit utilization, since cache hits are not deducted against your rate limit.

<Note>
  The 5-minute and 1-hour cache behave the same with respect to latency. You will generally see improved time-to-first-token for long documents.
</Note>

### Mixing different TTLs

You can use both 1-hour and 5-minute cache controls in the same request, but with an important constraint: Cache entries with longer TTL must appear before shorter TTLs (i.e., a 1-hour cache entry must appear before any 5-minute cache entries).

When mixing TTLs, we determine three billing locations in your prompt:

1. Position `A`: The token count at the highest cache hit (or 0 if no hits).
2. Position `B`: The token count at the highest 1-hour `cache_control` block after `A` (or equals `A` if none exist).
3. Position `C`: The token count at the last `cache_control` block.

<Note>
  If `B` and/or `C` are larger than `A`, they will necessarily be cache misses, because `A` is the highest cache hit.
</Note>

You'll be charged for:

1. Cache read tokens for `A`.
2. 1-hour cache write tokens for `(B - A)`.
3. 5-minute cache write tokens for `(C - B)`.

Here are 3 examples. This depicts the input tokens of 3 requests, each of which has different cache hits and cache misses. Each has a different calculated pricing, shown in the colored boxes, as a result.
<img src="https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt-cache-mixed-ttl.svg?fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=10a8997695f0f78953fdac300a3373e9" alt="Mixing TTLs Diagram" data-og-width="1376" width="1376" data-og-height="976" height="976" data-path="images/prompt-cache-mixed-ttl.svg" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt-cache-mixed-ttl.svg?w=280&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=7a8de34e52bbf67c60b2eeda57690ea3 280w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt-cache-mixed-ttl.svg?w=560&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=cdc3a1950dc88fbfb5679320df656ef2 560w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt-cache-mixed-ttl.svg?w=840&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=0df34408f5ec905ade69060ac8b5077b 840w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt-cache-mixed-ttl.svg?w=1100&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=0c434f1b04d12e6a0a20cfe58b22d4e5 1100w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt-cache-mixed-ttl.svg?w=1650&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=c800577f55f6e3383e3807644a5e0743 1650w, https://mintcdn.com/anthropic-claude-docs/LF5WV0SNF6oudpT5/images/prompt-cache-mixed-ttl.svg?w=2500&fit=max&auto=format&n=LF5WV0SNF6oudpT5&q=85&s=7e7079d06a969ea814980f4e570d2fa2 2500w" />

***

## Prompt caching examples

To help you get started with prompt caching, we've prepared a [prompt caching cookbook](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/prompt_caching.ipynb) with detailed examples and best practices.

Below, we've included several code snippets that showcase various prompt caching patterns. These examples demonstrate how to implement caching in different scenarios, helping you understand the practical applications of this feature:

<AccordionGroup>
  <Accordion title="Large context caching example">
    <CodeGroup>
      ```bash Shell theme={null}
      curl https://api.anthropic.com/v1/messages \
           --header "x-api-key: $ANTHROPIC_API_KEY" \
           --header "anthropic-version: 2023-06-01" \
           --header "content-type: application/json" \
           --data \
      '{
          "model": "claude-sonnet-4-5",
          "max_tokens": 1024,
          "system": [
              {
                  "type": "text",
                  "text": "You are an AI assistant tasked with analyzing legal documents."
              },
              {
                  "type": "text",
                  "text": "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
                  "cache_control": {"type": "ephemeral"}
              }
          ],
          "messages": [
              {
                  "role": "user",
                  "content": "What are the key terms and conditions in this agreement?"
              }
          ]
      }'
      ```

      ```Python Python theme={null}
      import anthropic
      client = anthropic.Anthropic()

      response = client.messages.create(
          model="claude-sonnet-4-5",
          max_tokens=1024,
          system=[
              {
                  "type": "text",
                  "text": "You are an AI assistant tasked with analyzing legal documents."
              },
              {
                  "type": "text",
                  "text": "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
                  "cache_control": {"type": "ephemeral"}
              }
          ],
          messages=[
              {
                  "role": "user",
                  "content": "What are the key terms and conditions in this agreement?"
              }
          ]
      )
      print(response.model_dump_json())
      ```

      ```typescript TypeScript theme={null}
      import Anthropic from '@anthropic-ai/sdk';

      const client = new Anthropic();

      const response = await client.messages.create({
        model: "claude-sonnet-4-5",
        max_tokens: 1024,
        system: [
          {
              "type": "text",
              "text": "You are an AI assistant tasked with analyzing legal documents."
          },
          {
              "type": "text",
              "text": "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
              "cache_control": {"type": "ephemeral"}
          }
        ],
        messages: [
          {
              "role": "user",
              "content": "What are the key terms and conditions in this agreement?"
          }
        ]
      });
      console.log(response);
      ```

      ```java Java theme={null}
      import java.util.List;

      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.models.messages.CacheControlEphemeral;
      import com.anthropic.models.messages.Message;
      import com.anthropic.models.messages.MessageCreateParams;
      import com.anthropic.models.messages.Model;
      import com.anthropic.models.messages.TextBlockParam;

      public class LegalDocumentAnalysisExample {

          public static void main(String[] args) {
              AnthropicClient client = AnthropicOkHttpClient.fromEnv();

              MessageCreateParams params = MessageCreateParams.builder()
                      .model(Model.CLAUDE_OPUS_4_20250514)
                      .maxTokens(1024)
                      .systemOfTextBlockParams(List.of(
                              TextBlockParam.builder()
                                      .text("You are an AI assistant tasked with analyzing legal documents.")
                                      .build(),
                              TextBlockParam.builder()
                                      .text("Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]")
                                      .cacheControl(CacheControlEphemeral.builder().build())
                                      .build()
                      ))
                      .addUserMessage("What are the key terms and conditions in this agreement?")
                      .build();

              Message message = client.messages().create(params);
              System.out.println(message);
          }
      }
      ```
    </CodeGroup>

    This example demonstrates basic prompt caching usage, caching the full text of the legal agreement as a prefix while keeping the user instruction uncached.

    For the first request:

    * `input_tokens`: Number of tokens in the user message only
    * `cache_creation_input_tokens`: Number of tokens in the entire system message, including the legal document
    * `cache_read_input_tokens`: 0 (no cache hit on first request)

    For subsequent requests within the cache lifetime:

    * `input_tokens`: Number of tokens in the user message only
    * `cache_creation_input_tokens`: 0 (no new cache creation)
    * `cache_read_input_tokens`: Number of tokens in the entire cached system message
  </Accordion>

  <Accordion title="Caching tool definitions">
    <CodeGroup>
      ```bash Shell theme={null}
      curl https://api.anthropic.com/v1/messages \
           --header "x-api-key: $ANTHROPIC_API_KEY" \
           --header "anthropic-version: 2023-06-01" \
           --header "content-type: application/json" \
           --data \
      '{
          "model": "claude-sonnet-4-5",
          "max_tokens": 1024,
          "tools": [
              {
                  "name": "get_weather",
                  "description": "Get the current weather in a given location",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "location": {
                              "type": "string",
                              "description": "The city and state, e.g. San Francisco, CA"
                          },
                          "unit": {
                              "type": "string",
                              "enum": ["celsius", "fahrenheit"],
                              "description": "The unit of temperature, either celsius or fahrenheit"
                          }
                      },
                      "required": ["location"]
                  }
              },
              # many more tools
              {
                  "name": "get_time",
                  "description": "Get the current time in a given time zone",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "timezone": {
                              "type": "string",
                              "description": "The IANA time zone name, e.g. America/Los_Angeles"
                          }
                      },
                      "required": ["timezone"]
                  },
                  "cache_control": {"type": "ephemeral"}
              }
          ],
          "messages": [
              {
                  "role": "user",
                  "content": "What is the weather and time in New York?"
              }
          ]
      }'
      ```

      ```Python Python theme={null}
      import anthropic
      client = anthropic.Anthropic()

      response = client.messages.create(
          model="claude-sonnet-4-5",
          max_tokens=1024,
          tools=[
              {
                  "name": "get_weather",
                  "description": "Get the current weather in a given location",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "location": {
                              "type": "string",
                              "description": "The city and state, e.g. San Francisco, CA"
                          },
                          "unit": {
                              "type": "string",
                              "enum": ["celsius", "fahrenheit"],
                              "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
                          }
                      },
                      "required": ["location"]
                  },
              },
              # many more tools
              {
                  "name": "get_time",
                  "description": "Get the current time in a given time zone",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "timezone": {
                              "type": "string",
                              "description": "The IANA time zone name, e.g. America/Los_Angeles"
                          }
                      },
                      "required": ["timezone"]
                  },
                  "cache_control": {"type": "ephemeral"}
              }
          ],
          messages=[
              {
                  "role": "user",
                  "content": "What's the weather and time in New York?"
              }
          ]
      )
      print(response.model_dump_json())
      ```

      ```typescript TypeScript theme={null}
      import Anthropic from '@anthropic-ai/sdk';

      const client = new Anthropic();

      const response = await client.messages.create({
          model: "claude-sonnet-4-5",
          max_tokens: 1024,
          tools=[
              {
                  "name": "get_weather",
                  "description": "Get the current weather in a given location",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "location": {
                              "type": "string",
                              "description": "The city and state, e.g. San Francisco, CA"
                          },
                          "unit": {
                              "type": "string",
                              "enum": ["celsius", "fahrenheit"],
                              "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
                          }
                      },
                      "required": ["location"]
                  },
              },
              // many more tools
              {
                  "name": "get_time",
                  "description": "Get the current time in a given time zone",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "timezone": {
                              "type": "string",
                              "description": "The IANA time zone name, e.g. America/Los_Angeles"
                          }
                      },
                      "required": ["timezone"]
                  },
                  "cache_control": {"type": "ephemeral"}
              }
          ],
          messages: [
              {
                  "role": "user",
                  "content": "What's the weather and time in New York?"
              }
          ]
      });
      console.log(response);
      ```

      ```java Java theme={null}
      import java.util.List;
      import java.util.Map;

      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.core.JsonValue;
      import com.anthropic.models.messages.CacheControlEphemeral;
      import com.anthropic.models.messages.Message;
      import com.anthropic.models.messages.MessageCreateParams;
      import com.anthropic.models.messages.Model;
      import com.anthropic.models.messages.Tool;
      import com.anthropic.models.messages.Tool.InputSchema;

      public class ToolsWithCacheControlExample {

          public static void main(String[] args) {
              AnthropicClient client = AnthropicOkHttpClient.fromEnv();

              // Weather tool schema
              InputSchema weatherSchema = InputSchema.builder()
                      .properties(JsonValue.from(Map.of(
                              "location", Map.of(
                                      "type", "string",
                                      "description", "The city and state, e.g. San Francisco, CA"
                              ),
                              "unit", Map.of(
                                      "type", "string",
                                      "enum", List.of("celsius", "fahrenheit"),
                                      "description", "The unit of temperature, either celsius or fahrenheit"
                              )
                      )))
                      .putAdditionalProperty("required", JsonValue.from(List.of("location")))
                      .build();

              // Time tool schema
              InputSchema timeSchema = InputSchema.builder()
                      .properties(JsonValue.from(Map.of(
                              "timezone", Map.of(
                                      "type", "string",
                                      "description", "The IANA time zone name, e.g. America/Los_Angeles"
                              )
                      )))
                      .putAdditionalProperty("required", JsonValue.from(List.of("timezone")))
                      .build();

              MessageCreateParams params = MessageCreateParams.builder()
                      .model(Model.CLAUDE_OPUS_4_20250514)
                      .maxTokens(1024)
                      .addTool(Tool.builder()
                              .name("get_weather")
                              .description("Get the current weather in a given location")
                              .inputSchema(weatherSchema)
                              .build())
                      .addTool(Tool.builder()
                              .name("get_time")
                              .description("Get the current time in a given time zone")
                              .inputSchema(timeSchema)
                              .cacheControl(CacheControlEphemeral.builder().build())
                              .build())
                      .addUserMessage("What is the weather and time in New York?")
                      .build();

              Message message = client.messages().create(params);
              System.out.println(message);
          }
      }
      ```
    </CodeGroup>

    In this example, we demonstrate caching tool definitions.

    The `cache_control` parameter is placed on the final tool (`get_time`) to designate all of the tools as part of the static prefix.

    This means that all tool definitions, including `get_weather` and any other tools defined before `get_time`, will be cached as a single prefix.

    This approach is useful when you have a consistent set of tools that you want to reuse across multiple requests without re-processing them each time.

    For the first request:

    * `input_tokens`: Number of tokens in the user message
    * `cache_creation_input_tokens`: Number of tokens in all tool definitions and system prompt
    * `cache_read_input_tokens`: 0 (no cache hit on first request)

    For subsequent requests within the cache lifetime:

    * `input_tokens`: Number of tokens in the user message
    * `cache_creation_input_tokens`: 0 (no new cache creation)
    * `cache_read_input_tokens`: Number of tokens in all cached tool definitions and system prompt
  </Accordion>

  <Accordion title="Continuing a multi-turn conversation">
    <CodeGroup>
      ```bash Shell theme={null}
      curl https://api.anthropic.com/v1/messages \
           --header "x-api-key: $ANTHROPIC_API_KEY" \
           --header "anthropic-version: 2023-06-01" \
           --header "content-type: application/json" \
           --data \
      '{
          "model": "claude-sonnet-4-5",
          "max_tokens": 1024,
          "system": [
              {
                  "type": "text",
                  "text": "...long system prompt",
                  "cache_control": {"type": "ephemeral"}
              }
          ],
          "messages": [
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "text",
                          "text": "Hello, can you tell me more about the solar system?",
                      }
                  ]
              },
              {
                  "role": "assistant",
                  "content": "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you would like to know more about?"
              },
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "text",
                          "text": "Good to know."
                      },
                      {
                          "type": "text",
                          "text": "Tell me more about Mars.",
                          "cache_control": {"type": "ephemeral"}
                      }
                  ]
              }
          ]
      }'
      ```

      ```Python Python theme={null}
      import anthropic
      client = anthropic.Anthropic()

      response = client.messages.create(
          model="claude-sonnet-4-5",
          max_tokens=1024,
          system=[
              {
                  "type": "text",
                  "text": "...long system prompt",
                  "cache_control": {"type": "ephemeral"}
              }
          ],
          messages=[
              # ...long conversation so far
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "text",
                          "text": "Hello, can you tell me more about the solar system?",
                      }
                  ]
              },
              {
                  "role": "assistant",
                  "content": "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you'd like to know more about?"
              },
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "text",
                          "text": "Good to know."
                      },
                      {
                          "type": "text",
                          "text": "Tell me more about Mars.",
                          "cache_control": {"type": "ephemeral"}
                      }
                  ]
              }
          ]
      )
      print(response.model_dump_json())
      ```

      ```typescript TypeScript theme={null}
      import Anthropic from '@anthropic-ai/sdk';

      const client = new Anthropic();

      const response = await client.messages.create({
          model: "claude-sonnet-4-5",
          max_tokens: 1024,
          system=[
              {
                  "type": "text",
                  "text": "...long system prompt",
                  "cache_control": {"type": "ephemeral"}
              }
          ],
          messages=[
              // ...long conversation so far
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "text",
                          "text": "Hello, can you tell me more about the solar system?",
                      }
                  ]
              },
              {
                  "role": "assistant",
                  "content": "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you'd like to know more about?"
              },
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "text",
                          "text": "Good to know."
                      },
                      {
                          "type": "text",
                          "text": "Tell me more about Mars.",
                          "cache_control": {"type": "ephemeral"}
                      }
                  ]
              }
          ]
      });
      console.log(response);
      ```

      ```java Java theme={null}
      import java.util.List;

      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.models.messages.CacheControlEphemeral;
      import com.anthropic.models.messages.ContentBlockParam;
      import com.anthropic.models.messages.Message;
      import com.anthropic.models.messages.MessageCreateParams;
      import com.anthropic.models.messages.Model;
      import com.anthropic.models.messages.TextBlockParam;

      public class ConversationWithCacheControlExample {

          public static void main(String[] args) {
              AnthropicClient client = AnthropicOkHttpClient.fromEnv();

              // Create ephemeral system prompt
              TextBlockParam systemPrompt = TextBlockParam.builder()
                      .text("...long system prompt")
                      .cacheControl(CacheControlEphemeral.builder().build())
                      .build();

              // Create message params
              MessageCreateParams params = MessageCreateParams.builder()
                      .model(Model.CLAUDE_OPUS_4_20250514)
                      .maxTokens(1024)
                      .systemOfTextBlockParams(List.of(systemPrompt))
                      // First user message (without cache control)
                      .addUserMessage("Hello, can you tell me more about the solar system?")
                      // Assistant response
                      .addAssistantMessage("Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you would like to know more about?")
                      // Second user message (with cache control)
                      .addUserMessageOfBlockParams(List.of(
                              ContentBlockParam.ofText(TextBlockParam.builder()
                                      .text("Good to know.")
                                      .build()),
                              ContentBlockParam.ofText(TextBlockParam.builder()
                                      .text("Tell me more about Mars.")
                                      .cacheControl(CacheControlEphemeral.builder().build())
                                      .build())
                      ))
                      .build();

              Message message = client.messages().create(params);
              System.out.println(message);
          }
      }
      ```
    </CodeGroup>

    In this example, we demonstrate how to use prompt caching in a multi-turn conversation.

    During each turn, we mark the final block of the final message with `cache_control` so the conversation can be incrementally cached. The system will automatically lookup and use the longest previously cached sequence of blocks for follow-up messages. That is, blocks that were previously marked with a `cache_control` block are later not marked with this, but they will still be considered a cache hit (and also a cache refresh!) if they are hit within 5 minutes.

    In addition, note that the `cache_control` parameter is placed on the system message. This is to ensure that if this gets evicted from the cache (after not being used for more than 5 minutes), it will get added back to the cache on the next request.

    This approach is useful for maintaining context in ongoing conversations without repeatedly processing the same information.

    When this is set up properly, you should see the following in the usage response of each request:

    * `input_tokens`: Number of tokens in the new user message (will be minimal)
    * `cache_creation_input_tokens`: Number of tokens in the new assistant and user turns
    * `cache_read_input_tokens`: Number of tokens in the conversation up to the previous turn
  </Accordion>

  <Accordion title="Putting it all together: Multiple cache breakpoints">
    <CodeGroup>
      ```bash Shell theme={null}
      curl https://api.anthropic.com/v1/messages \
           --header "x-api-key: $ANTHROPIC_API_KEY" \
           --header "anthropic-version: 2023-06-01" \
           --header "content-type: application/json" \
           --data \
      '{
          "model": "claude-sonnet-4-5",
          "max_tokens": 1024,
          "tools": [
              {
                  "name": "search_documents",
                  "description": "Search through the knowledge base",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "query": {
                              "type": "string",
                              "description": "Search query"
                          }
                      },
                      "required": ["query"]
                  }
              },
              {
                  "name": "get_document",
                  "description": "Retrieve a specific document by ID",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "doc_id": {
                              "type": "string",
                              "description": "Document ID"
                          }
                      },
                      "required": ["doc_id"]
                  },
                  "cache_control": {"type": "ephemeral"}
              }
          ],
          "system": [
              {
                  "type": "text",
                  "text": "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base",
                  "cache_control": {"type": "ephemeral"}
              },
              {
                  "type": "text",
                  "text": "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]",
                  "cache_control": {"type": "ephemeral"}
              }
          ],
          "messages": [
              {
                  "role": "user",
                  "content": "Can you search for information about Mars rovers?"
              },
              {
                  "role": "assistant",
                  "content": [
                      {
                          "type": "tool_use",
                          "id": "tool_1",
                          "name": "search_documents",
                          "input": {"query": "Mars rovers"}
                      }
                  ]
              },
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "tool_result",
                          "tool_use_id": "tool_1",
                          "content": "Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)"
                      }
                  ]
              },
              {
                  "role": "assistant",
                  "content": [
                      {
                          "type": "text",
                          "text": "I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document."
                      }
                  ]
              },
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "text",
                          "text": "Yes, please tell me about the Perseverance rover specifically.",
                          "cache_control": {"type": "ephemeral"}
                      }
                  ]
              }
          ]
      }'
      ```

      ```Python Python theme={null}
      import anthropic
      client = anthropic.Anthropic()

      response = client.messages.create(
          model="claude-sonnet-4-5",
          max_tokens=1024,
          tools=[
              {
                  "name": "search_documents",
                  "description": "Search through the knowledge base",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "query": {
                              "type": "string",
                              "description": "Search query"
                          }
                      },
                      "required": ["query"]
                  }
              },
              {
                  "name": "get_document",
                  "description": "Retrieve a specific document by ID",
                  "input_schema": {
                      "type": "object",
                      "properties": {
                          "doc_id": {
                              "type": "string",
                              "description": "Document ID"
                          }
                      },
                      "required": ["doc_id"]
                  },
                  "cache_control": {"type": "ephemeral"}
              }
          ],
          system=[
              {
                  "type": "text",
                  "text": "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base",
                  "cache_control": {"type": "ephemeral"}
              },
              {
                  "type": "text",
                  "text": "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]",
                  "cache_control": {"type": "ephemeral"}
              }
          ],
          messages=[
              {
                  "role": "user",
                  "content": "Can you search for information about Mars rovers?"
              },
              {
                  "role": "assistant",
                  "content": [
                      {
                          "type": "tool_use",
                          "id": "tool_1",
                          "name": "search_documents",
                          "input": {"query": "Mars rovers"}
                      }
                  ]
              },
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "tool_result",
                          "tool_use_id": "tool_1",
                          "content": "Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)"
                      }
                  ]
              },
              {
                  "role": "assistant",
                  "content": [
                      {
                          "type": "text",
                          "text": "I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document."
                      }
                  ]
              },
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "text",
                          "text": "Yes, please tell me about the Perseverance rover specifically.",
                          "cache_control": {"type": "ephemeral"}
                      }
                  ]
              }
          ]
      )
      print(response.model_dump_json())
      ```

      ```typescript TypeScript theme={null}
      import Anthropic from '@anthropic-ai/sdk';

      const client = new Anthropic();

      const response = await client.messages.create({
          model: "claude-sonnet-4-5",
          max_tokens: 1024,
          tools: [
              {
                  name: "search_documents",
                  description: "Search through the knowledge base",
                  input_schema: {
                      type: "object",
                      properties: {
                          query: {
                              type: "string",
                              description: "Search query"
                          }
                      },
                      required: ["query"]
                  }
              },
              {
                  name: "get_document",
                  description: "Retrieve a specific document by ID",
                  input_schema: {
                      type: "object",
                      properties: {
                          doc_id: {
                              type: "string",
                              description: "Document ID"
                          }
                      },
                      required: ["doc_id"]
                  },
                  cache_control: { type: "ephemeral" }
              }
          ],
          system: [
              {
                  type: "text",
                  text: "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base",
                  cache_control: { type: "ephemeral" }
              },
              {
                  type: "text",
                  text: "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]",
                  cache_control: { type: "ephemeral" }
              }
          ],
          messages: [
              {
                  role: "user",
                  content: "Can you search for information about Mars rovers?"
              },
              {
                  role: "assistant",
                  content: [
                      {
                          type: "tool_use",
                          id: "tool_1",
                          name: "search_documents",
                          input: { query: "Mars rovers" }
                      }
                  ]
              },
              {
                  role: "user",
                  content: [
                      {
                          type: "tool_result",
                          tool_use_id: "tool_1",
                          content: "Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)"
                      }
                  ]
              },
              {
                  role: "assistant",
                  content: [
                      {
                          type: "text",
                          text: "I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document."
                      }
                  ]
              },
              {
                  role: "user",
                  content: [
                      {
                          type: "text",
                          text: "Yes, please tell me about the Perseverance rover specifically.",
                          cache_control: { type: "ephemeral" }
                      }
                  ]
              }
          ]
      });
      console.log(response);
      ```

      ```java Java theme={null}
      import java.util.List;
      import java.util.Map;

      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.core.JsonValue;
      import com.anthropic.models.messages.CacheControlEphemeral;
      import com.anthropic.models.messages.ContentBlockParam;
      import com.anthropic.models.messages.Message;
      import com.anthropic.models.messages.MessageCreateParams;
      import com.anthropic.models.messages.Model;
      import com.anthropic.models.messages.TextBlockParam;
      import com.anthropic.models.messages.Tool;
      import com.anthropic.models.messages.Tool.InputSchema;
      import com.anthropic.models.messages.ToolResultBlockParam;
      import com.anthropic.models.messages.ToolUseBlockParam;

      public class MultipleCacheBreakpointsExample {

          public static void main(String[] args) {
              AnthropicClient client = AnthropicOkHttpClient.fromEnv();

              // Search tool schema
              InputSchema searchSchema = InputSchema.builder()
                      .properties(JsonValue.from(Map.of(
                              "query", Map.of(
                                      "type", "string",
                                      "description", "Search query"
                              )
                      )))
                      .putAdditionalProperty("required", JsonValue.from(List.of("query")))
                      .build();

              // Get document tool schema
              InputSchema getDocSchema = InputSchema.builder()
                      .properties(JsonValue.from(Map.of(
                              "doc_id", Map.of(
                                      "type", "string",
                                      "description", "Document ID"
                              )
                      )))
                      .putAdditionalProperty("required", JsonValue.from(List.of("doc_id")))
                      .build();

              MessageCreateParams params = MessageCreateParams.builder()
                      .model(Model.CLAUDE_OPUS_4_20250514)
                      .maxTokens(1024)
                      // Tools with cache control on the last one
                      .addTool(Tool.builder()
                              .name("search_documents")
                              .description("Search through the knowledge base")
                              .inputSchema(searchSchema)
                              .build())
                      .addTool(Tool.builder()
                              .name("get_document")
                              .description("Retrieve a specific document by ID")
                              .inputSchema(getDocSchema)
                              .cacheControl(CacheControlEphemeral.builder().build())
                              .build())
                      // System prompts with cache control on instructions and context separately
                      .systemOfTextBlockParams(List.of(
                              TextBlockParam.builder()
                                      .text("You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base")
                                      .cacheControl(CacheControlEphemeral.builder().build())
                                      .build(),
                              TextBlockParam.builder()
                                      .text("# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]")
                                      .cacheControl(CacheControlEphemeral.builder().build())
                                      .build()
                      ))
                      // Conversation history
                      .addUserMessage("Can you search for information about Mars rovers?")
                      .addAssistantMessageOfBlockParams(List.of(
                              ContentBlockParam.ofToolUse(ToolUseBlockParam.builder()
                                      .id("tool_1")
                                      .name("search_documents")
                                      .input(JsonValue.from(Map.of("query", "Mars rovers")))
                                      .build())
                      ))
                      .addUserMessageOfBlockParams(List.of(
                              ContentBlockParam.ofToolResult(ToolResultBlockParam.builder()
                                      .toolUseId("tool_1")
                                      .content("Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)")
                                      .build())
                      ))
                      .addAssistantMessageOfBlockParams(List.of(
                              ContentBlockParam.ofText(TextBlockParam.builder()
                                      .text("I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document.")
                                      .build())
                      ))
                      .addUserMessageOfBlockParams(List.of(
                              ContentBlockParam.ofText(TextBlockParam.builder()
                                      .text("Yes, please tell me about the Perseverance rover specifically.")
                                      .cacheControl(CacheControlEphemeral.builder().build())
                                      .build())
                      ))
                      .build();

              Message message = client.messages().create(params);
              System.out.println(message);
          }
      }
      ```
    </CodeGroup>

    This comprehensive example demonstrates how to use all 4 available cache breakpoints to optimize different parts of your prompt:

    1. **Tools cache** (cache breakpoint 1): The `cache_control` parameter on the last tool definition caches all tool definitions.

    2. **Reusable instructions cache** (cache breakpoint 2): The static instructions in the system prompt are cached separately. These instructions rarely change between requests.

    3. **RAG context cache** (cache breakpoint 3): The knowledge base documents are cached independently, allowing you to update the RAG documents without invalidating the tools or instructions cache.

    4. **Conversation history cache** (cache breakpoint 4): The assistant's response is marked with `cache_control` to enable incremental caching of the conversation as it progresses.

    This approach provides maximum flexibility:

    * If you only update the final user message, all four cache segments are reused
    * If you update the RAG documents but keep the same tools and instructions, the first two cache segments are reused
    * If you change the conversation but keep the same tools, instructions, and documents, the first three segments are reused
    * Each cache breakpoint can be invalidated independently based on what changes in your application

    For the first request:

    * `input_tokens`: Tokens in the final user message
    * `cache_creation_input_tokens`: Tokens in all cached segments (tools + instructions + RAG documents + conversation history)
    * `cache_read_input_tokens`: 0 (no cache hits)

    For subsequent requests with only a new user message:

    * `input_tokens`: Tokens in the new user message only
    * `cache_creation_input_tokens`: Any new tokens added to conversation history
    * `cache_read_input_tokens`: All previously cached tokens (tools + instructions + RAG documents + previous conversation)

    This pattern is especially powerful for:

    * RAG applications with large document contexts
    * Agent systems that use multiple tools
    * Long-running conversations that need to maintain context
    * Applications that need to optimize different parts of the prompt independently
  </Accordion>
</AccordionGroup>

***

## FAQ

<AccordionGroup>
  <Accordion title="Do I need multiple cache breakpoints or is one at the end sufficient?">
    **In most cases, a single cache breakpoint at the end of your static content is sufficient.** The system automatically checks for cache hits at all previous content block boundaries (up to 20 blocks before your breakpoint) and uses the longest matching sequence of cached blocks.

    You only need multiple breakpoints if:

    * You have more than 20 content blocks before your desired cache point
    * You want to cache sections that update at different frequencies independently
    * You need explicit control over what gets cached for cost optimization

    Example: If you have system instructions (rarely change) and RAG context (changes daily), you might use two breakpoints to cache them separately.
  </Accordion>

  <Accordion title="Do cache breakpoints add extra cost?">
    No, cache breakpoints themselves are free. You only pay for:

    * Writing content to cache (25% more than base input tokens for 5-minute TTL)
    * Reading from cache (10% of base input token price)
    * Regular input tokens for uncached content

    The number of breakpoints doesn't affect pricing - only the amount of content cached and read matters.
  </Accordion>

  <Accordion title="How do I calculate total input tokens from the usage fields?">
    The usage response includes three separate input token fields that together represent your total input:

    ```
    total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
    ```

    * `cache_read_input_tokens`: Tokens retrieved from cache (everything before cache breakpoints that was cached)
    * `cache_creation_input_tokens`: New tokens being written to cache (at cache breakpoints)
    * `input_tokens`: Tokens **after the last cache breakpoint** that aren't cached

    **Important:** `input_tokens` does NOT represent all input tokens - only the portion after your last cache breakpoint. If you have cached content, `input_tokens` will typically be much smaller than your total input.

    **Example:** With a 200K token document cached and a 50 token user question:

    * `cache_read_input_tokens`: 200,000
    * `cache_creation_input_tokens`: 0
    * `input_tokens`: 50
    * **Total**: 200,050 tokens

    This breakdown is critical for understanding both your costs and rate limit usage. See [Tracking cache performance](#tracking-cache-performance) for more details.
  </Accordion>

  <Accordion title="What is the cache lifetime?">
    The cache's default minimum lifetime (TTL) is 5 minutes. This lifetime is refreshed each time the cached content is used.

    If you find that 5 minutes is too short, Anthropic also offers a [1-hour cache TTL](#1-hour-cache-duration).
  </Accordion>

  <Accordion title="How many cache breakpoints can I use?">
    You can define up to 4 cache breakpoints (using `cache_control` parameters) in your prompt.
  </Accordion>

  <Accordion title="Is prompt caching available for all models?">
    No, prompt caching is currently only available for Claude Opus 4.1, Claude Opus 4, Claude Sonnet 4.5, Claude Sonnet 4, Claude Sonnet 3.7, Claude Haiku 4.5, Claude Haiku 3.5, Claude Haiku 3, and Claude Opus 3 ([deprecated](/en/docs/about-claude/model-deprecations)).
  </Accordion>

  <Accordion title="How does prompt caching work with extended thinking?">
    Cached system prompts and tools will be reused when thinking parameters change. However, thinking changes (enabling/disabling or budget changes) will invalidate previously cached prompt prefixes with messages content.

    For more details on cache invalidation, see [What invalidates the cache](#what-invalidates-the-cache).

    For more on extended thinking, including its interaction with tool use and prompt caching, see the [extended thinking documentation](/en/docs/build-with-claude/extended-thinking#extended-thinking-and-prompt-caching).
  </Accordion>

  <Accordion title="How do I enable prompt caching?">
    To enable prompt caching, include at least one `cache_control` breakpoint in your API request.
  </Accordion>

  <Accordion title="Can I use prompt caching with other API features?">
    Yes, prompt caching can be used alongside other API features like tool use and vision capabilities. However, changing whether there are images in a prompt or modifying tool use settings will break the cache.

    For more details on cache invalidation, see [What invalidates the cache](#what-invalidates-the-cache).
  </Accordion>

  <Accordion title="How does prompt caching affect pricing?">
    Prompt caching introduces a new pricing structure where cache writes cost 25% more than base input tokens, while cache hits cost only 10% of the base input token price.
  </Accordion>

  <Accordion title="Can I manually clear the cache?">
    Currently, there's no way to manually clear the cache. Cached prefixes automatically expire after a minimum of 5 minutes of inactivity.
  </Accordion>

  <Accordion title="How can I track the effectiveness of my caching strategy?">
    You can monitor cache performance using the `cache_creation_input_tokens` and `cache_read_input_tokens` fields in the API response.
  </Accordion>

  <Accordion title="What can break the cache?">
    See [What invalidates the cache](#what-invalidates-the-cache) for more details on cache invalidation, including a list of changes that require creating a new cache entry.
  </Accordion>

  <Accordion title="How does prompt caching handle privacy and data separation?">
    Prompt caching is designed with strong privacy and data separation measures:

    1. Cache keys are generated using a cryptographic hash of the prompts up to the cache control point. This means only requests with identical prompts can access a specific cache.

    2. Caches are organization-specific. Users within the same organization can access the same cache if they use identical prompts, but caches are not shared across different organizations, even for identical prompts.

    3. The caching mechanism is designed to maintain the integrity and privacy of each unique conversation or context.

    4. It's safe to use `cache_control` anywhere in your prompts. For cost efficiency, it's better to exclude highly variable parts (e.g., user's arbitrary input) from caching.

    These measures ensure that prompt caching maintains data privacy and security while offering performance benefits.
  </Accordion>

  <Accordion title="Can I use prompt caching with the Batches API?">
    Yes, it is possible to use prompt caching with your [Batches API](/en/docs/build-with-claude/batch-processing) requests. However, because asynchronous batch requests can be processed concurrently and in any order, cache hits are provided on a best-effort basis.

    The [1-hour cache](#1-hour-cache-duration) can help improve your cache hits. The most cost effective way of using it is the following:

    * Gather a set of message requests that have a shared prefix.
    * Send a batch request with just a single request that has this shared prefix and a 1-hour cache block. This will get written to the 1-hour cache.
    * As soon as this is complete, submit the rest of the requests. You will have to monitor the job to know when it completes.

    This is typically better than using the 5-minute cache simply because it’s common for batch requests to take between 5 minutes and 1 hour to complete. We’re considering ways to improve these cache hit rates and making this process more straightforward.
  </Accordion>

  <Accordion title="Why am I seeing the error `AttributeError: 'Beta' object has no attribute 'prompt_caching'` in Python?">
    This error typically appears when you have upgraded your SDK or you are using outdated code examples. Prompt caching is now generally available, so you no longer need the beta prefix. Instead of:

    <CodeGroup>
      ```Python Python theme={null}
      python client.beta.prompt_caching.messages.create(...)
      ```
    </CodeGroup>

    Simply use:

    <CodeGroup>
      ```Python Python theme={null}
      python client.messages.create(...)
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="Why am I seeing 'TypeError: Cannot read properties of undefined (reading 'messages')'?">
    This error typically appears when you have upgraded your SDK or you are using outdated code examples. Prompt caching is now generally available, so you no longer need the beta prefix. Instead of:

    ```typescript TypeScript theme={null}
    client.beta.promptCaching.messages.create(...)
    ```

    Simply use:

    ```typescript  theme={null}
    client.messages.create(...)
    ```
  </Accordion>
</AccordionGroup>
