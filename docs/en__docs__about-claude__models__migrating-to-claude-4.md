# Migrating to Claude 4.5

This guide covers two key migration paths to Claude 4.5 models:

* **Claude Sonnet 3.7 → Claude Sonnet 4.5**: Our most intelligent model with best-in-class reasoning, coding, and long-running agent capabilities
* **Claude Haiku 3.5 → Claude Haiku 4.5**: Our fastest and most intelligent Haiku model with near-frontier performance for real-time applications and high-volume intelligent processing

Both migrations involve breaking changes that require updates to your implementation. This guide will walk you through each migration path with step-by-step instructions and clearly marked breaking changes.

Before starting your migration, we recommend reviewing [What's new in Claude 4.5](/en/docs/about-claude/models/whats-new-claude-4-5) to understand the new features and capabilities available in these models, including extended thinking, context awareness, and behavioral improvements.

## Migrating from Claude Sonnet 3.7 to Claude Sonnet 4.5

Claude Sonnet 4.5 is our most intelligent model, offering best-in-class performance for reasoning, coding, and long-running autonomous agents. This migration includes several breaking changes that require updates to your implementation.

### Migration steps

1. **Update your model name:**
   ```python  theme={null}
   # Before (Claude Sonnet 3.7)
   model="claude-3-7-sonnet-20250219"

   # After (Claude Sonnet 4.5)
   model="claude-sonnet-4-5-20250929"
   ```

2. **Update sampling parameters**

   <Warning>
     This is a breaking change from the Claude Sonnet 3.7.
   </Warning>

   Use only `temperature` OR `top_p`, not both:

   ```python  theme={null}
   # Before (Claude Sonnet 3.7) - This will error in Sonnet 4.5
   response = client.messages.create(
       model="claude-3-7-sonnet-20250219",
       temperature=0.7,
       top_p=0.9,  # Cannot use both
       ...
   )

   # After (Claude Sonnet 4.5)
   response = client.messages.create(
       model="claude-sonnet-4-5-20250929",
       temperature=0.7,  # Use temperature OR top_p, not both
       ...
   )
   ```

3. **Handle the new `refusal` stop reason**

   Update your application to [handle `refusal` stop reasons](/en/docs/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals):

   ```python  theme={null}
   response = client.messages.create(...)

   if response.stop_reason == "refusal":
       # Handle refusal appropriately
       pass
   ```

4. **Update text editor tool (if applicable)**

   <Warning>
     This is a breaking change from the Claude Sonnet 3.7.
   </Warning>

   Update to `text_editor_20250728` (type) and `str_replace_based_edit_tool` (name). Remove any code using the `undo_edit` command.

   ```python  theme={null}
   # Before (Claude Sonnet 3.7)
   tools=[{"type": "text_editor_20250124", "name": "str_replace_editor"}]

   # After (Claude Sonnet 4.5)
   tools=[{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}]
   ```

   See [Text editor tool documentation](/en/docs/agents-and-tools/tool-use/text-editor-tool) for details.

5. **Update code execution tool (if applicable)**

   Upgrade to `code_execution_20250825`. The legacy version `code_execution_20250522` still works but is not recommended. See [Code execution tool documentation](/en/docs/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version) for migration instructions.

6. **Remove token-efficient tool use beta header**

   [Token-efficient tool use](/en/docs/agents-and-tools/tool-use/token-efficient-tool-use) is a beta feature that only works with Claude 3.7 Sonnet. All Claude 4 models have built-in token-efficient tool use, so you should no longer include the beta header.

   Remove the `token-efficient-tools-2025-02-19` [beta header](/en/api/beta-headers) from your requests:

   ```python  theme={null}
   # Before (Claude Sonnet 3.7)
   client.messages.create(
       model="claude-3-7-sonnet-20250219",
       betas=["token-efficient-tools-2025-02-19"],  # Remove this
       ...
   )

   # After (Claude Sonnet 4.5)
   client.messages.create(
       model="claude-sonnet-4-5-20250929",
       # No token-efficient-tools beta header
       ...
   )
   ```

7. **Remove extended output beta header**

   The `output-128k-2025-02-19` [beta header](/en/api/beta-headers) for extended output is only available in Claude Sonnet 3.7.

   Remove this header from your requests:

   ```python  theme={null}
   # Before (Claude Sonnet 3.7)
   client.messages.create(
       model="claude-3-7-sonnet-20250219",
       betas=["output-128k-2025-02-19"],  # Remove this
       ...
   )

   # After (Claude Sonnet 4.5)
   client.messages.create(
       model="claude-sonnet-4-5-20250929",
       # No output-128k beta header
       ...
   )
   ```

8. **Update your prompts for behavioral changes**

   Claude Sonnet 4.5 has a more concise, direct communication style and requires explicit direction. Review [Claude 4 prompt engineering best practices](/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) for optimization guidance.

9. **Consider enabling extended thinking for complex tasks**

   Enable [extended thinking](/en/docs/build-with-claude/extended-thinking) for significant performance improvements on coding and reasoning tasks (disabled by default):

   ```python  theme={null}
   response = client.messages.create(
       model="claude-sonnet-4-5-20250929",
       max_tokens=16000,
       thinking={"type": "enabled", "budget_tokens": 10000},
       messages=[...]
   )
   ```

   <Note>
     Extended thinking impacts [prompt caching](/en/docs/build-with-claude/prompt-caching#caching-with-thinking-blocks) efficiency.
   </Note>

10. **Test your implementation**

Test in a development environment before deploying to production to ensure all breaking changes are properly handled.

### Sonnet 3.7 → 4.5 migration checklist

* [ ] Update model ID to `claude-sonnet-4-5-20250929`
* [ ] **BREAKING**: Update sampling parameters to use only `temperature` OR `top_p`, not both
* [ ] Handle new `refusal` stop reason in your application
* [ ] **BREAKING**: Update text editor tool to `text_editor_20250728` and `str_replace_based_edit_tool` (if applicable)
* [ ] **BREAKING**: Remove any code using the `undo_edit` command (if applicable)
* [ ] Update code execution tool to `code_execution_20250825` (if applicable)
* [ ] Remove `token-efficient-tools-2025-02-19` beta header (if applicable)
* [ ] Remove `output-128k-2025-02-19` beta header (if applicable)
* [ ] Review and update prompts following [Claude 4 best practices](/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
* [ ] Consider enabling extended thinking for complex reasoning tasks
* [ ] Handle `model_context_window_exceeded` stop reason (Sonnet 4.5 specific)
* [ ] Consider enabling memory tool for long-running agents (beta)
* [ ] Consider using automatic tool call clearing for context editing (beta)
* [ ] Test in development environment before production deployment

### Features removed from Claude Sonnet 3.7

* **Token-efficient tool use**: The `token-efficient-tools-2025-02-19` beta header only works with Claude 3.7 Sonnet and is not supported in Claude 4 models (see step 6)
* **Extended output**: The `output-128k-2025-02-19` beta header is not supported (see step 7)

Both headers can be included in Claude 4 requests but will have no effect.

## Migrating from Claude Haiku 3.5 to Claude Haiku 4.5

Claude Haiku 4.5 is our fastest and most intelligent Haiku model with near-frontier performance, delivering premium model quality with real-time performance for interactive applications and high-volume intelligent processing. This migration includes several breaking changes that require updates to your implementation.

For a complete overview of new capabilities, see [What's new in Claude 4.5](/en/docs/about-claude/models/whats-new-claude-4-5#key-improvements-in-haiku-4-5-over-haiku-3-5).

<Note>
  Haiku 4.5 pricing $1 per million input tokens, $5 per million output tokens. See [Claude pricing](/en/docs/about-claude/pricing) for details.
</Note>

### Migration steps

1. **Update your model name:**
   ```python  theme={null}
   # Before (Haiku 3.5)
   model="claude-3-5-haiku-20241022"

   # After (Haiku 4.5)
   model="claude-haiku-4-5-20251001"
   ```

2. **Update tool versions (if applicable)**

   <Warning>
     This is a breaking change from the Claude Haiku 3.5.
   </Warning>

   Haiku 4.5 only supports the latest tool versions:

   ```python  theme={null}
   # Before (Haiku 3.5)
   tools=[{"type": "text_editor_20250124", "name": "str_replace_editor"}]

   # After (Haiku 4.5)
   tools=[{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}]
   ```

   * **Text editor**: Use `text_editor_20250728` and `str_replace_based_edit_tool`
   * **Code execution**: Use `code_execution_20250825`
   * Remove any code using the `undo_edit` command

3. **Update sampling parameters**

   <Warning>
     This is a breaking change from the Claude Haiku 3.5.
   </Warning>

   Use only `temperature` OR `top_p`, not both:

   ```python  theme={null}
   # Before (Haiku 3.5) - This will error in Haiku 4.5
   response = client.messages.create(
       model="claude-3-5-haiku-20241022",
       temperature=0.7,
       top_p=0.9,  # Cannot use both
       ...
   )

   # After (Haiku 4.5)
   response = client.messages.create(
       model="claude-haiku-4-5-20251001",
       temperature=0.7,  # Use temperature OR top_p, not both
       ...
   )
   ```

4. **Review new rate limits**

   Haiku 4.5 has separate rate limits from Haiku 3.5. See [Rate limits documentation](/en/api/rate-limits) for details.

5. **Handle the new `refusal` stop reason**

   Update your application to [handle refusal stop reasons](/en/docs/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

6. **Consider enabling extended thinking for complex tasks**

   Enable [extended thinking](/en/docs/build-with-claude/extended-thinking) for significant performance improvements on coding and reasoning tasks (disabled by default):

   ```python  theme={null}
   response = client.messages.create(
       model="claude-haiku-4-5-20251001",
       max_tokens=16000,
       thinking={"type": "enabled", "budget_tokens": 5000},
       messages=[...]
   )
   ```

   <Note>
     Extended thinking impacts [prompt caching](/en/docs/build-with-claude/prompt-caching#caching-with-thinking-blocks) efficiency.
   </Note>

7. **Explore new capabilities**

   See [What's new in Claude 4.5](/en/docs/about-claude/models/whats-new-claude-4-5#key-improvements-in-haiku-4-5-over-haiku-3-5) for details on context awareness, increased output capacity (64K tokens), higher intelligence, and improved speed.

8. **Test your implementation**

   Test in a development environment before deploying to production to ensure all breaking changes are properly handled.

### Haiku 3.5 → 4.5 migration checklist

* [ ] Update model ID to `claude-haiku-4-5-20251001`
* [ ] **BREAKING**: Update tool versions to latest (e.g., `text_editor_20250728`, `code_execution_20250825`) - legacy versions not supported
* [ ] **BREAKING**: Remove any code using the `undo_edit` command (if applicable)
* [ ] **BREAKING**: Update sampling parameters to use only `temperature` OR `top_p`, not both
* [ ] Review and adjust for new rate limits (separate from Haiku 3.5)
* [ ] Handle new `refusal` stop reason in your application
* [ ] Consider enabling extended thinking for complex reasoning tasks (new capability)
* [ ] Leverage context awareness for better token management in long sessions
* [ ] Prepare for larger responses (max output increased from 8K to 64K tokens)
* [ ] Review and update prompts following [Claude 4 best practices](/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
* [ ] Test in development environment before production deployment

## Choosing between Sonnet 4.5 and Haiku 4.5

Both Claude Sonnet 4.5 and Claude Haiku 4.5 are powerful Claude 4 models with different strengths:

### Choose Claude Sonnet 4.5 (most intelligent) for:

* **Complex reasoning and analysis**: Best-in-class intelligence for sophisticated tasks
* **Long-running autonomous agents**: Superior performance for agents working independently for extended periods
* **Advanced coding tasks**: Our strongest coding model with advanced planning and security engineering
* **Large context workflows**: Enhanced context management with memory tool and context editing capabilities
* **Tasks requiring maximum capability**: When intelligence and accuracy are the top priorities

### Choose Claude Haiku 4.5 (fastest and most intelligent Haiku) for:

* **Real-time applications**: Fast response times for interactive user experiences with near-frontier performance
* **High-volume intelligent processing**: Cost-effective intelligence at scale with improved speed
* **Cost-sensitive deployments**: Near-frontier performance at lower price points
* **Sub-agent architectures**: Fast, intelligent agents for multi-agent systems
* **Computer use at scale**: Cost-effective autonomous desktop and browser automation
* **Tasks requiring speed**: When low latency is critical while maintaining near-frontier intelligence

### Extended thinking recommendations

Claude 4 models, particularly Sonnet and Haiku 4.5, show significant performance improvements when using [extended thinking](/en/docs/build-with-claude/extended-thinking) for coding and complex reasoning tasks. Extended thinking is **disabled by default** but we recommend enabling it for demanding work.

**Important**: Extended thinking impacts [prompt caching](/en/docs/build-with-claude/prompt-caching#caching-with-thinking-blocks) efficiency. When non-tool-result content is added to a conversation, thinking blocks are stripped from cache, which can increase costs in multi-turn conversations. We recommend enabling thinking when the performance benefits outweigh the caching trade-off.

## Other migration scenarios

The primary migration paths covered above (Sonnet 3.7 → 4.5 and Haiku 3.5 → 4.5) represent the most common upgrades. However, you may be migrating from other Claude models to Claude 4.5. This section covers those scenarios.

### Migrating from Claude Sonnet 4 → Sonnet 4.5

**Breaking change**: Cannot specify both `temperature` and `top_p` in the same request.

All other API calls will work without modification. Update your model ID and adjust sampling parameters if needed:

```python  theme={null}
# Before (Claude Sonnet 4)
model="claude-sonnet-4-20250514"

# After (Claude Sonnet 4.5)
model="claude-sonnet-4-5-20250929"
```

### Migrating from Claude Opus 4.1 → Sonnet 4.5

**No breaking changes.** All API calls will work without modification.

Simply update your model ID:

```python  theme={null}
# Before (Claude Opus 4.1)
model="claude-opus-4-1-20250805"

# After (Claude Sonnet 4.5)
model="claude-sonnet-4-5-20250929"
```

Claude Sonnet 4.5 is our most intelligent model with best-in-class reasoning, coding, and long-running agent capabilities. It offers superior performance compared to Opus 4.1 for most use cases.

## Need help?

* Check our [API documentation](/en/api/overview) for detailed specifications
* Review [model capabilities](/en/docs/about-claude/models/overview) for performance comparisons
* Review [API release notes](/en/release-notes/api) for API updates
* Contact support if you encounter any issues during migration
