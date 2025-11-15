# Features overview

> Explore Claude's advanced features and capabilities.

export const PlatformAvailability = ({claudeApi = false, claudeApiBeta = false, bedrock = false, bedrockBeta = false, vertexAi = false, vertexAiBeta = false}) => {
  const platforms = [];
  if (claudeApi || claudeApiBeta) {
    platforms.push(claudeApiBeta ? 'Claude API (Beta)' : 'Claude API');
  }
  if (bedrock || bedrockBeta) {
    platforms.push(bedrockBeta ? 'Amazon Bedrock (Beta)' : 'Amazon Bedrock');
  }
  if (vertexAi || vertexAiBeta) {
    platforms.push(vertexAiBeta ? "Google Cloud's Vertex AI (Beta)" : "Google Cloud's Vertex AI");
  }
  return <>
      {platforms.map((platform, index) => <span key={index}>
          {platform}
          {index < platforms.length - 1 && <><br /><br /></>}
        </span>)}
    </>;
};

## Core capabilities

These features enhance Claude's fundamental abilities for processing, analyzing, and generating content across various formats and use cases.

| Feature                                                                                       | Description                                                                                                                                                                                                               | Availability                                                    |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [1M token context window](/en/docs/build-with-claude/context-windows#1m-token-context-window) | An extended context window that allows you to process much larger documents, maintain longer conversations, and work with more extensive codebases.                                                                       | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta /> |
| [Agent Skills](/en/docs/agents-and-tools/agent-skills/overview)                               | Extend Claude's capabilities with Skills. Use pre-built Skills (PowerPoint, Excel, Word, PDF) or create custom Skills with instructions and scripts. Skills use progressive disclosure to efficiently manage context.     | <PlatformAvailability claudeApiBeta />                          |
| [Batch processing](/en/docs/build-with-claude/batch-processing)                               | Process large volumes of requests asynchronously for cost savings. Send batches with a large number of queries per batch. Batch API calls costs 50% less than standard API calls.                                         | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [Citations](/en/docs/build-with-claude/citations)                                             | Ground Claude's responses in source documents. With Citations, Claude can provide detailed references to the exact sentences and passages it uses to generate responses, leading to more verifiable, trustworthy outputs. | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [Context editing](/en/docs/build-with-claude/context-editing)                                 | Automatically manage conversation context with configurable strategies. Supports clearing tool results when approaching token limits and managing thinking blocks in extended thinking conversations.                     | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta /> |
| [Extended thinking](/en/docs/build-with-claude/extended-thinking)                             | Enhanced reasoning capabilities for complex tasks, providing transparency into Claude's step-by-step thought process before delivering its final answer.                                                                  | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [Files API](/en/docs/build-with-claude/files)                                                 | Upload and manage files to use with Claude without re-uploading content with each request. Supports PDFs, images, and text files.                                                                                         | <PlatformAvailability claudeApiBeta />                          |
| [PDF support](/en/docs/build-with-claude/pdf-support)                                         | Process and analyze text and visual content from PDF documents.                                                                                                                                                           | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [Prompt caching (5m)](/en/docs/build-with-claude/prompt-caching)                              | Provide Claude with more background knowledge and example outputs to reduce costs and latency.                                                                                                                            | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [Prompt caching (1hr)](/en/docs/build-with-claude/prompt-caching#1-hour-cache-duration)       | Extended 1-hour cache duration for less frequently accessed but important context, complementing the standard 5-minute cache.                                                                                             | <PlatformAvailability claudeApi />                              |
| [Search results](/en/docs/build-with-claude/search-results)                                   | Enable natural citations for RAG applications by providing search results with proper source attribution. Achieve web search-quality citations for custom knowledge bases and tools.                                      | <PlatformAvailability claudeApi vertexAi />                     |
| [Structured outputs](/en/docs/build-with-claude/structured-outputs)                           | Guarantee schema conformance with two approaches: JSON outputs for structured data responses, and strict tool use for validated tool inputs. Available on Sonnet 4.5 and Opus 4.1.                                        | <PlatformAvailability claudeApiBeta />                          |
| [Token counting](/en/api/messages-count-tokens)                                               | Token counting enables you to determine the number of tokens in a message before sending it to Claude, helping you make informed decisions about your prompts and usage.                                                  | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [Tool use](/en/docs/agents-and-tools/tool-use/overview)                                       | Enable Claude to interact with external tools and APIs to perform a wider variety of tasks. For a list of supported tools, see [the Tools table](#tools).                                                                 | <PlatformAvailability claudeApi bedrock vertexAi />             |

## Tools

These features enable Claude to interact with external systems, execute code, and perform automated tasks through various tool interfaces.

| Feature                                                                                       | Description                                                                                                                                                        | Availability                                                    |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| [Bash](/en/docs/agents-and-tools/tool-use/bash-tool)                                          | Execute bash commands and scripts to interact with the system shell and perform command-line operations.                                                           | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [Code execution](/en/docs/agents-and-tools/tool-use/code-execution-tool)                      | Run Python code in a sandboxed environment for advanced data analysis.                                                                                             | <PlatformAvailability claudeApiBeta />                          |
| [Computer use](/en/docs/agents-and-tools/tool-use/computer-use-tool)                          | Control computer interfaces by taking screenshots and issuing mouse and keyboard commands.                                                                         | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta /> |
| [Fine-grained tool streaming](/en/docs/agents-and-tools/tool-use/fine-grained-tool-streaming) | Stream tool use parameters without buffering/JSON validation, reducing latency for receiving large parameters.                                                     | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [MCP connector](/en/docs/agents-and-tools/mcp-connector)                                      | Connect to remote [MCP](/en/docs/mcp) servers directly from the Messages API without a separate MCP client.                                                        | <PlatformAvailability claudeApiBeta />                          |
| [Memory](/en/docs/agents-and-tools/tool-use/memory-tool)                                      | Enable Claude to store and retrieve information across conversations. Build knowledge bases over time, maintain project context, and learn from past interactions. | <PlatformAvailability claudeApiBeta bedrockBeta vertexAiBeta /> |
| [Text editor](/en/docs/agents-and-tools/tool-use/text-editor-tool)                            | Create and edit text files with a built-in text editor interface for file manipulation tasks.                                                                      | <PlatformAvailability claudeApi bedrock vertexAi />             |
| [Web fetch](/en/docs/agents-and-tools/tool-use/web-fetch-tool)                                | Retrieve full content from specified web pages and PDF documents for in-depth analysis.                                                                            | <PlatformAvailability claudeApiBeta />                          |
| [Web search](/en/docs/agents-and-tools/tool-use/web-search-tool)                              | Augment Claude's comprehensive knowledge with current, real-world data from across the web.                                                                        | <PlatformAvailability claudeApi vertexAi />                     |
