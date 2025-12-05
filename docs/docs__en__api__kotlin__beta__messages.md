# Messages

## Create

`beta().messages().create(MessageCreateParamsparams, RequestOptionsrequestOptions = RequestOptions.none()) : BetaMessage`

**post** `/v1/messages`

Send a structured list of input messages with text and/or image content, and the model will generate the next message in the conversation.

The Messages API can be used for either single queries or stateless multi-turn conversations.

Learn more about the Messages API in our [user guide](https://docs.claude.com/en/docs/initial-setup)

### Parameters

- `params: MessageCreateParams`

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

  - `maxTokens: Long`

    The maximum number of tokens to generate before stopping.

    Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

    Different models have different maximum values for this parameter.  See [models](https://docs.claude.com/en/docs/models-overview) for details.

  - `messages: List<BetaMessageParam>`

    Input messages.

    Our models are trained to operate on alternating `user` and `assistant` conversational turns. When creating a new `Message`, you specify the prior conversational turns with the `messages` parameter, and the model then generates the next `Message` in the conversation. Consecutive `user` or `assistant` turns in your request will be combined into a single turn.

    Each input message must be an object with a `role` and `content`. You can specify a single `user`-role message, or you can include multiple `user` and `assistant` messages.

    If the final message uses the `assistant` role, the response content will continue immediately from the content in that message. This can be used to constrain part of the model's response.

    Example with a single `user` message:

    ```json
    [{"role": "user", "content": "Hello, Claude"}]
    ```

    Example with multiple conversational turns:

    ```json
    [
      {"role": "user", "content": "Hello there."},
      {"role": "assistant", "content": "Hi, I'm Claude. How can I help you?"},
      {"role": "user", "content": "Can you explain LLMs in plain English?"},
    ]
    ```

    Example with a partially-filled response from Claude:

    ```json
    [
      {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
      {"role": "assistant", "content": "The best answer is ("},
    ]
    ```

    Each input message `content` may be either a single `string` or an array of content blocks, where each block has a specific `type`. Using a `string` for `content` is shorthand for an array of one content block of type `"text"`. The following input messages are equivalent:

    ```json
    {"role": "user", "content": "Hello, Claude"}
    ```

    ```json
    {"role": "user", "content": [{"type": "text", "text": "Hello, Claude"}]}
    ```

    See [input examples](https://docs.claude.com/en/api/messages-examples).

    Note that if you want to include a [system prompt](https://docs.claude.com/en/docs/system-prompts), you can use the top-level `system` parameter — there is no `"system"` role for input messages in the Messages API.

    There is a limit of 100,000 messages in a single request.

    - `content: Content`

      - `String`

      - `List<BetaContentBlockParam>`

        - `class BetaTextBlockParam:`

          - `text: String`

          - `type: JsonValue; "text"constant`

            - `TEXT("text")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<List<BetaTextCitationParam>>`

            - `class BetaCitationCharLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class BetaCitationPageLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class BetaCitationContentBlockLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class BetaCitationWebSearchResultLocationParam:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class BetaCitationSearchResultLocationParam:`

              - `citedText: String`

              - `endBlockIndex: Long`

              - `searchResultIndex: Long`

              - `source: String`

              - `startBlockIndex: Long`

              - `title: Optional<String>`

              - `type: JsonValue; "search_result_location"constant`

                - `SEARCH_RESULT_LOCATION("search_result_location")`

        - `class BetaImageBlockParam:`

          - `source: Source`

            - `class BetaBase64ImageSource:`

              - `data: String`

              - `mediaType: MediaType`

                - `IMAGE_JPEG("image/jpeg")`

                - `IMAGE_PNG("image/png")`

                - `IMAGE_GIF("image/gif")`

                - `IMAGE_WEBP("image/webp")`

              - `type: JsonValue; "base64"constant`

                - `BASE64("base64")`

            - `class BetaUrlImageSource:`

              - `type: JsonValue; "url"constant`

                - `URL("url")`

              - `url: String`

            - `class BetaFileImageSource:`

              - `fileId: String`

              - `type: JsonValue; "file"constant`

                - `FILE("file")`

          - `type: JsonValue; "image"constant`

            - `IMAGE("image")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaRequestDocumentBlock:`

          - `source: Source`

            - `class BetaBase64PdfSource:`

              - `data: String`

              - `mediaType: JsonValue; "application/pdf"constant`

                - `APPLICATION_PDF("application/pdf")`

              - `type: JsonValue; "base64"constant`

                - `BASE64("base64")`

            - `class BetaPlainTextSource:`

              - `data: String`

              - `mediaType: JsonValue; "text/plain"constant`

                - `TEXT_PLAIN("text/plain")`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

            - `class BetaContentBlockSource:`

              - `content: Content`

                - `String`

                - `List<BetaContentBlockSourceContent>`

                  - `class BetaTextBlockParam:`

                    - `text: String`

                    - `type: JsonValue; "text"constant`

                      - `TEXT("text")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                    - `citations: Optional<List<BetaTextCitationParam>>`

                      - `class BetaCitationCharLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endCharIndex: Long`

                        - `startCharIndex: Long`

                        - `type: JsonValue; "char_location"constant`

                          - `CHAR_LOCATION("char_location")`

                      - `class BetaCitationPageLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endPageNumber: Long`

                        - `startPageNumber: Long`

                        - `type: JsonValue; "page_location"constant`

                          - `PAGE_LOCATION("page_location")`

                      - `class BetaCitationContentBlockLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endBlockIndex: Long`

                        - `startBlockIndex: Long`

                        - `type: JsonValue; "content_block_location"constant`

                          - `CONTENT_BLOCK_LOCATION("content_block_location")`

                      - `class BetaCitationWebSearchResultLocationParam:`

                        - `citedText: String`

                        - `encryptedIndex: String`

                        - `title: Optional<String>`

                        - `type: JsonValue; "web_search_result_location"constant`

                          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                        - `url: String`

                      - `class BetaCitationSearchResultLocationParam:`

                        - `citedText: String`

                        - `endBlockIndex: Long`

                        - `searchResultIndex: Long`

                        - `source: String`

                        - `startBlockIndex: Long`

                        - `title: Optional<String>`

                        - `type: JsonValue; "search_result_location"constant`

                          - `SEARCH_RESULT_LOCATION("search_result_location")`

                  - `class BetaImageBlockParam:`

                    - `source: Source`

                      - `class BetaBase64ImageSource:`

                        - `data: String`

                        - `mediaType: MediaType`

                          - `IMAGE_JPEG("image/jpeg")`

                          - `IMAGE_PNG("image/png")`

                          - `IMAGE_GIF("image/gif")`

                          - `IMAGE_WEBP("image/webp")`

                        - `type: JsonValue; "base64"constant`

                          - `BASE64("base64")`

                      - `class BetaUrlImageSource:`

                        - `type: JsonValue; "url"constant`

                          - `URL("url")`

                        - `url: String`

                      - `class BetaFileImageSource:`

                        - `fileId: String`

                        - `type: JsonValue; "file"constant`

                          - `FILE("file")`

                    - `type: JsonValue; "image"constant`

                      - `IMAGE("image")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

              - `type: JsonValue; "content"constant`

                - `CONTENT("content")`

            - `class BetaUrlPdfSource:`

              - `type: JsonValue; "url"constant`

                - `URL("url")`

              - `url: String`

            - `class BetaFileDocumentSource:`

              - `fileId: String`

              - `type: JsonValue; "file"constant`

                - `FILE("file")`

          - `type: JsonValue; "document"constant`

            - `DOCUMENT("document")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<BetaCitationsConfigParam>`

            - `enabled: Optional<Boolean>`

          - `context: Optional<String>`

          - `title: Optional<String>`

        - `class BetaSearchResultBlockParam:`

          - `content: List<BetaTextBlockParam>`

            - `text: String`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

            - `cacheControl: Optional<BetaCacheControlEphemeral>`

              Create a cache control breakpoint at this content block.

              - `type: JsonValue; "ephemeral"constant`

                - `EPHEMERAL("ephemeral")`

              - `ttl: Optional<Ttl>`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `TTL_5M("5m")`

                - `TTL_1H("1h")`

            - `citations: Optional<List<BetaTextCitationParam>>`

              - `class BetaCitationCharLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endCharIndex: Long`

                - `startCharIndex: Long`

                - `type: JsonValue; "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class BetaCitationPageLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endPageNumber: Long`

                - `startPageNumber: Long`

                - `type: JsonValue; "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class BetaCitationContentBlockLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endBlockIndex: Long`

                - `startBlockIndex: Long`

                - `type: JsonValue; "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class BetaCitationWebSearchResultLocationParam:`

                - `citedText: String`

                - `encryptedIndex: String`

                - `title: Optional<String>`

                - `type: JsonValue; "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `url: String`

              - `class BetaCitationSearchResultLocationParam:`

                - `citedText: String`

                - `endBlockIndex: Long`

                - `searchResultIndex: Long`

                - `source: String`

                - `startBlockIndex: Long`

                - `title: Optional<String>`

                - `type: JsonValue; "search_result_location"constant`

                  - `SEARCH_RESULT_LOCATION("search_result_location")`

          - `source: String`

          - `title: String`

          - `type: JsonValue; "search_result"constant`

            - `SEARCH_RESULT("search_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<BetaCitationsConfigParam>`

            - `enabled: Optional<Boolean>`

        - `class BetaThinkingBlockParam:`

          - `signature: String`

          - `thinking: String`

          - `type: JsonValue; "thinking"constant`

            - `THINKING("thinking")`

        - `class BetaRedactedThinkingBlockParam:`

          - `data: String`

          - `type: JsonValue; "redacted_thinking"constant`

            - `REDACTED_THINKING("redacted_thinking")`

        - `class BetaToolUseBlockParam:`

          - `id: String`

          - `input: Input`

          - `name: String`

          - `type: JsonValue; "tool_use"constant`

            - `TOOL_USE("tool_use")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `caller: Optional<Caller>`

            Tool invocation directly from the model.

            - `class BetaDirectCaller:`

              Tool invocation directly from the model.

              - `type: JsonValue; "direct"constant`

                - `DIRECT("direct")`

            - `class BetaServerToolCaller:`

              Tool invocation generated by a server-side tool.

              - `toolId: String`

              - `type: JsonValue; "code_execution_20250825"constant`

                - `CODE_EXECUTION_20250825("code_execution_20250825")`

        - `class BetaToolResultBlockParam:`

          - `toolUseId: String`

          - `type: JsonValue; "tool_result"constant`

            - `TOOL_RESULT("tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `content: Optional<Content>`

            - `String`

            - `List<Block>`

              - `class BetaTextBlockParam:`

                - `text: String`

                - `type: JsonValue; "text"constant`

                  - `TEXT("text")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `citations: Optional<List<BetaTextCitationParam>>`

                  - `class BetaCitationCharLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endCharIndex: Long`

                    - `startCharIndex: Long`

                    - `type: JsonValue; "char_location"constant`

                      - `CHAR_LOCATION("char_location")`

                  - `class BetaCitationPageLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endPageNumber: Long`

                    - `startPageNumber: Long`

                    - `type: JsonValue; "page_location"constant`

                      - `PAGE_LOCATION("page_location")`

                  - `class BetaCitationContentBlockLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endBlockIndex: Long`

                    - `startBlockIndex: Long`

                    - `type: JsonValue; "content_block_location"constant`

                      - `CONTENT_BLOCK_LOCATION("content_block_location")`

                  - `class BetaCitationWebSearchResultLocationParam:`

                    - `citedText: String`

                    - `encryptedIndex: String`

                    - `title: Optional<String>`

                    - `type: JsonValue; "web_search_result_location"constant`

                      - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                    - `url: String`

                  - `class BetaCitationSearchResultLocationParam:`

                    - `citedText: String`

                    - `endBlockIndex: Long`

                    - `searchResultIndex: Long`

                    - `source: String`

                    - `startBlockIndex: Long`

                    - `title: Optional<String>`

                    - `type: JsonValue; "search_result_location"constant`

                      - `SEARCH_RESULT_LOCATION("search_result_location")`

              - `class BetaImageBlockParam:`

                - `source: Source`

                  - `class BetaBase64ImageSource:`

                    - `data: String`

                    - `mediaType: MediaType`

                      - `IMAGE_JPEG("image/jpeg")`

                      - `IMAGE_PNG("image/png")`

                      - `IMAGE_GIF("image/gif")`

                      - `IMAGE_WEBP("image/webp")`

                    - `type: JsonValue; "base64"constant`

                      - `BASE64("base64")`

                  - `class BetaUrlImageSource:`

                    - `type: JsonValue; "url"constant`

                      - `URL("url")`

                    - `url: String`

                  - `class BetaFileImageSource:`

                    - `fileId: String`

                    - `type: JsonValue; "file"constant`

                      - `FILE("file")`

                - `type: JsonValue; "image"constant`

                  - `IMAGE("image")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

              - `class BetaSearchResultBlockParam:`

                - `content: List<BetaTextBlockParam>`

                  - `text: String`

                  - `type: JsonValue; "text"constant`

                    - `TEXT("text")`

                  - `cacheControl: Optional<BetaCacheControlEphemeral>`

                    Create a cache control breakpoint at this content block.

                    - `type: JsonValue; "ephemeral"constant`

                      - `EPHEMERAL("ephemeral")`

                    - `ttl: Optional<Ttl>`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `TTL_5M("5m")`

                      - `TTL_1H("1h")`

                  - `citations: Optional<List<BetaTextCitationParam>>`

                    - `class BetaCitationCharLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endCharIndex: Long`

                      - `startCharIndex: Long`

                      - `type: JsonValue; "char_location"constant`

                        - `CHAR_LOCATION("char_location")`

                    - `class BetaCitationPageLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endPageNumber: Long`

                      - `startPageNumber: Long`

                      - `type: JsonValue; "page_location"constant`

                        - `PAGE_LOCATION("page_location")`

                    - `class BetaCitationContentBlockLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endBlockIndex: Long`

                      - `startBlockIndex: Long`

                      - `type: JsonValue; "content_block_location"constant`

                        - `CONTENT_BLOCK_LOCATION("content_block_location")`

                    - `class BetaCitationWebSearchResultLocationParam:`

                      - `citedText: String`

                      - `encryptedIndex: String`

                      - `title: Optional<String>`

                      - `type: JsonValue; "web_search_result_location"constant`

                        - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                      - `url: String`

                    - `class BetaCitationSearchResultLocationParam:`

                      - `citedText: String`

                      - `endBlockIndex: Long`

                      - `searchResultIndex: Long`

                      - `source: String`

                      - `startBlockIndex: Long`

                      - `title: Optional<String>`

                      - `type: JsonValue; "search_result_location"constant`

                        - `SEARCH_RESULT_LOCATION("search_result_location")`

                - `source: String`

                - `title: String`

                - `type: JsonValue; "search_result"constant`

                  - `SEARCH_RESULT("search_result")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `citations: Optional<BetaCitationsConfigParam>`

                  - `enabled: Optional<Boolean>`

              - `class BetaRequestDocumentBlock:`

                - `source: Source`

                  - `class BetaBase64PdfSource:`

                    - `data: String`

                    - `mediaType: JsonValue; "application/pdf"constant`

                      - `APPLICATION_PDF("application/pdf")`

                    - `type: JsonValue; "base64"constant`

                      - `BASE64("base64")`

                  - `class BetaPlainTextSource:`

                    - `data: String`

                    - `mediaType: JsonValue; "text/plain"constant`

                      - `TEXT_PLAIN("text/plain")`

                    - `type: JsonValue; "text"constant`

                      - `TEXT("text")`

                  - `class BetaContentBlockSource:`

                    - `content: Content`

                      - `String`

                      - `List<BetaContentBlockSourceContent>`

                        - `class BetaTextBlockParam:`

                          - `text: String`

                          - `type: JsonValue; "text"constant`

                            - `TEXT("text")`

                          - `cacheControl: Optional<BetaCacheControlEphemeral>`

                            Create a cache control breakpoint at this content block.

                            - `type: JsonValue; "ephemeral"constant`

                              - `EPHEMERAL("ephemeral")`

                            - `ttl: Optional<Ttl>`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `TTL_5M("5m")`

                              - `TTL_1H("1h")`

                          - `citations: Optional<List<BetaTextCitationParam>>`

                            - `class BetaCitationCharLocationParam:`

                              - `citedText: String`

                              - `documentIndex: Long`

                              - `documentTitle: Optional<String>`

                              - `endCharIndex: Long`

                              - `startCharIndex: Long`

                              - `type: JsonValue; "char_location"constant`

                                - `CHAR_LOCATION("char_location")`

                            - `class BetaCitationPageLocationParam:`

                              - `citedText: String`

                              - `documentIndex: Long`

                              - `documentTitle: Optional<String>`

                              - `endPageNumber: Long`

                              - `startPageNumber: Long`

                              - `type: JsonValue; "page_location"constant`

                                - `PAGE_LOCATION("page_location")`

                            - `class BetaCitationContentBlockLocationParam:`

                              - `citedText: String`

                              - `documentIndex: Long`

                              - `documentTitle: Optional<String>`

                              - `endBlockIndex: Long`

                              - `startBlockIndex: Long`

                              - `type: JsonValue; "content_block_location"constant`

                                - `CONTENT_BLOCK_LOCATION("content_block_location")`

                            - `class BetaCitationWebSearchResultLocationParam:`

                              - `citedText: String`

                              - `encryptedIndex: String`

                              - `title: Optional<String>`

                              - `type: JsonValue; "web_search_result_location"constant`

                                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                              - `url: String`

                            - `class BetaCitationSearchResultLocationParam:`

                              - `citedText: String`

                              - `endBlockIndex: Long`

                              - `searchResultIndex: Long`

                              - `source: String`

                              - `startBlockIndex: Long`

                              - `title: Optional<String>`

                              - `type: JsonValue; "search_result_location"constant`

                                - `SEARCH_RESULT_LOCATION("search_result_location")`

                        - `class BetaImageBlockParam:`

                          - `source: Source`

                            - `class BetaBase64ImageSource:`

                              - `data: String`

                              - `mediaType: MediaType`

                                - `IMAGE_JPEG("image/jpeg")`

                                - `IMAGE_PNG("image/png")`

                                - `IMAGE_GIF("image/gif")`

                                - `IMAGE_WEBP("image/webp")`

                              - `type: JsonValue; "base64"constant`

                                - `BASE64("base64")`

                            - `class BetaUrlImageSource:`

                              - `type: JsonValue; "url"constant`

                                - `URL("url")`

                              - `url: String`

                            - `class BetaFileImageSource:`

                              - `fileId: String`

                              - `type: JsonValue; "file"constant`

                                - `FILE("file")`

                          - `type: JsonValue; "image"constant`

                            - `IMAGE("image")`

                          - `cacheControl: Optional<BetaCacheControlEphemeral>`

                            Create a cache control breakpoint at this content block.

                            - `type: JsonValue; "ephemeral"constant`

                              - `EPHEMERAL("ephemeral")`

                            - `ttl: Optional<Ttl>`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `TTL_5M("5m")`

                              - `TTL_1H("1h")`

                    - `type: JsonValue; "content"constant`

                      - `CONTENT("content")`

                  - `class BetaUrlPdfSource:`

                    - `type: JsonValue; "url"constant`

                      - `URL("url")`

                    - `url: String`

                  - `class BetaFileDocumentSource:`

                    - `fileId: String`

                    - `type: JsonValue; "file"constant`

                      - `FILE("file")`

                - `type: JsonValue; "document"constant`

                  - `DOCUMENT("document")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `citations: Optional<BetaCitationsConfigParam>`

                  - `enabled: Optional<Boolean>`

                - `context: Optional<String>`

                - `title: Optional<String>`

              - `class BetaToolReferenceBlockParam:`

                Tool reference block that can be included in tool_result content.

                - `toolName: String`

                - `type: JsonValue; "tool_reference"constant`

                  - `TOOL_REFERENCE("tool_reference")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

          - `isError: Optional<Boolean>`

        - `class BetaServerToolUseBlockParam:`

          - `id: String`

          - `input: Input`

          - `name: Name`

            - `WEB_SEARCH("web_search")`

            - `WEB_FETCH("web_fetch")`

            - `CODE_EXECUTION("code_execution")`

            - `BASH_CODE_EXECUTION("bash_code_execution")`

            - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

            - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

            - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

          - `type: JsonValue; "server_tool_use"constant`

            - `SERVER_TOOL_USE("server_tool_use")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `caller: Optional<Caller>`

            Tool invocation directly from the model.

            - `class BetaDirectCaller:`

              Tool invocation directly from the model.

              - `type: JsonValue; "direct"constant`

                - `DIRECT("direct")`

            - `class BetaServerToolCaller:`

              Tool invocation generated by a server-side tool.

              - `toolId: String`

              - `type: JsonValue; "code_execution_20250825"constant`

                - `CODE_EXECUTION_20250825("code_execution_20250825")`

        - `class BetaWebSearchToolResultBlockParam:`

          - `content: BetaWebSearchToolResultBlockParamContent`

            - `List<BetaWebSearchResultBlockParam>`

              - `encryptedContent: String`

              - `title: String`

              - `type: JsonValue; "web_search_result"constant`

                - `WEB_SEARCH_RESULT("web_search_result")`

              - `url: String`

              - `pageAge: Optional<String>`

            - `class BetaWebSearchToolRequestError:`

              - `errorCode: BetaWebSearchToolResultErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `QUERY_TOO_LONG("query_too_long")`

              - `type: JsonValue; "web_search_tool_result_error"constant`

                - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

          - `toolUseId: String`

          - `type: JsonValue; "web_search_tool_result"constant`

            - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaWebFetchToolResultBlockParam:`

          - `content: Content`

            - `class BetaWebFetchToolResultErrorBlockParam:`

              - `errorCode: BetaWebFetchToolResultErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `URL_TOO_LONG("url_too_long")`

                - `URL_NOT_ALLOWED("url_not_allowed")`

                - `URL_NOT_ACCESSIBLE("url_not_accessible")`

                - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                - `UNAVAILABLE("unavailable")`

              - `type: JsonValue; "web_fetch_tool_result_error"constant`

                - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

            - `class BetaWebFetchBlockParam:`

              - `content: BetaRequestDocumentBlock`

                - `source: Source`

                  - `class BetaBase64PdfSource:`

                    - `data: String`

                    - `mediaType: JsonValue; "application/pdf"constant`

                      - `APPLICATION_PDF("application/pdf")`

                    - `type: JsonValue; "base64"constant`

                      - `BASE64("base64")`

                  - `class BetaPlainTextSource:`

                    - `data: String`

                    - `mediaType: JsonValue; "text/plain"constant`

                      - `TEXT_PLAIN("text/plain")`

                    - `type: JsonValue; "text"constant`

                      - `TEXT("text")`

                  - `class BetaContentBlockSource:`

                    - `content: Content`

                      - `String`

                      - `List<BetaContentBlockSourceContent>`

                        - `class BetaTextBlockParam:`

                          - `text: String`

                          - `type: JsonValue; "text"constant`

                            - `TEXT("text")`

                          - `cacheControl: Optional<BetaCacheControlEphemeral>`

                            Create a cache control breakpoint at this content block.

                            - `type: JsonValue; "ephemeral"constant`

                              - `EPHEMERAL("ephemeral")`

                            - `ttl: Optional<Ttl>`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `TTL_5M("5m")`

                              - `TTL_1H("1h")`

                          - `citations: Optional<List<BetaTextCitationParam>>`

                            - `class BetaCitationCharLocationParam:`

                              - `citedText: String`

                              - `documentIndex: Long`

                              - `documentTitle: Optional<String>`

                              - `endCharIndex: Long`

                              - `startCharIndex: Long`

                              - `type: JsonValue; "char_location"constant`

                                - `CHAR_LOCATION("char_location")`

                            - `class BetaCitationPageLocationParam:`

                              - `citedText: String`

                              - `documentIndex: Long`

                              - `documentTitle: Optional<String>`

                              - `endPageNumber: Long`

                              - `startPageNumber: Long`

                              - `type: JsonValue; "page_location"constant`

                                - `PAGE_LOCATION("page_location")`

                            - `class BetaCitationContentBlockLocationParam:`

                              - `citedText: String`

                              - `documentIndex: Long`

                              - `documentTitle: Optional<String>`

                              - `endBlockIndex: Long`

                              - `startBlockIndex: Long`

                              - `type: JsonValue; "content_block_location"constant`

                                - `CONTENT_BLOCK_LOCATION("content_block_location")`

                            - `class BetaCitationWebSearchResultLocationParam:`

                              - `citedText: String`

                              - `encryptedIndex: String`

                              - `title: Optional<String>`

                              - `type: JsonValue; "web_search_result_location"constant`

                                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                              - `url: String`

                            - `class BetaCitationSearchResultLocationParam:`

                              - `citedText: String`

                              - `endBlockIndex: Long`

                              - `searchResultIndex: Long`

                              - `source: String`

                              - `startBlockIndex: Long`

                              - `title: Optional<String>`

                              - `type: JsonValue; "search_result_location"constant`

                                - `SEARCH_RESULT_LOCATION("search_result_location")`

                        - `class BetaImageBlockParam:`

                          - `source: Source`

                            - `class BetaBase64ImageSource:`

                              - `data: String`

                              - `mediaType: MediaType`

                                - `IMAGE_JPEG("image/jpeg")`

                                - `IMAGE_PNG("image/png")`

                                - `IMAGE_GIF("image/gif")`

                                - `IMAGE_WEBP("image/webp")`

                              - `type: JsonValue; "base64"constant`

                                - `BASE64("base64")`

                            - `class BetaUrlImageSource:`

                              - `type: JsonValue; "url"constant`

                                - `URL("url")`

                              - `url: String`

                            - `class BetaFileImageSource:`

                              - `fileId: String`

                              - `type: JsonValue; "file"constant`

                                - `FILE("file")`

                          - `type: JsonValue; "image"constant`

                            - `IMAGE("image")`

                          - `cacheControl: Optional<BetaCacheControlEphemeral>`

                            Create a cache control breakpoint at this content block.

                            - `type: JsonValue; "ephemeral"constant`

                              - `EPHEMERAL("ephemeral")`

                            - `ttl: Optional<Ttl>`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `TTL_5M("5m")`

                              - `TTL_1H("1h")`

                    - `type: JsonValue; "content"constant`

                      - `CONTENT("content")`

                  - `class BetaUrlPdfSource:`

                    - `type: JsonValue; "url"constant`

                      - `URL("url")`

                    - `url: String`

                  - `class BetaFileDocumentSource:`

                    - `fileId: String`

                    - `type: JsonValue; "file"constant`

                      - `FILE("file")`

                - `type: JsonValue; "document"constant`

                  - `DOCUMENT("document")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `citations: Optional<BetaCitationsConfigParam>`

                  - `enabled: Optional<Boolean>`

                - `context: Optional<String>`

                - `title: Optional<String>`

              - `type: JsonValue; "web_fetch_result"constant`

                - `WEB_FETCH_RESULT("web_fetch_result")`

              - `url: String`

                Fetched content URL

              - `retrievedAt: Optional<String>`

                ISO 8601 timestamp when the content was retrieved

          - `toolUseId: String`

          - `type: JsonValue; "web_fetch_tool_result"constant`

            - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaCodeExecutionToolResultBlockParam:`

          - `content: BetaCodeExecutionToolResultBlockParamContent`

            - `class BetaCodeExecutionToolResultErrorParam:`

              - `errorCode: BetaCodeExecutionToolResultErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `type: JsonValue; "code_execution_tool_result_error"constant`

                - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

            - `class BetaCodeExecutionResultBlockParam:`

              - `content: List<BetaCodeExecutionOutputBlockParam>`

                - `fileId: String`

                - `type: JsonValue; "code_execution_output"constant`

                  - `CODE_EXECUTION_OUTPUT("code_execution_output")`

              - `returnCode: Long`

              - `stderr: String`

              - `stdout: String`

              - `type: JsonValue; "code_execution_result"constant`

                - `CODE_EXECUTION_RESULT("code_execution_result")`

          - `toolUseId: String`

          - `type: JsonValue; "code_execution_tool_result"constant`

            - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaBashCodeExecutionToolResultBlockParam:`

          - `content: Content`

            - `class BetaBashCodeExecutionToolResultErrorParam:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

              - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

                - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

            - `class BetaBashCodeExecutionResultBlockParam:`

              - `content: List<BetaBashCodeExecutionOutputBlockParam>`

                - `fileId: String`

                - `type: JsonValue; "bash_code_execution_output"constant`

                  - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

              - `returnCode: Long`

              - `stderr: String`

              - `stdout: String`

              - `type: JsonValue; "bash_code_execution_result"constant`

                - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

          - `toolUseId: String`

          - `type: JsonValue; "bash_code_execution_tool_result"constant`

            - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaTextEditorCodeExecutionToolResultBlockParam:`

          - `content: Content`

            - `class BetaTextEditorCodeExecutionToolResultErrorParam:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `FILE_NOT_FOUND("file_not_found")`

              - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

              - `errorMessage: Optional<String>`

            - `class BetaTextEditorCodeExecutionViewResultBlockParam:`

              - `content: String`

              - `fileType: FileType`

                - `TEXT("text")`

                - `IMAGE("image")`

                - `PDF("pdf")`

              - `type: JsonValue; "text_editor_code_execution_view_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

              - `numLines: Optional<Long>`

              - `startLine: Optional<Long>`

              - `totalLines: Optional<Long>`

            - `class BetaTextEditorCodeExecutionCreateResultBlockParam:`

              - `isFileUpdate: Boolean`

              - `type: JsonValue; "text_editor_code_execution_create_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

            - `class BetaTextEditorCodeExecutionStrReplaceResultBlockParam:`

              - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

              - `lines: Optional<List<String>>`

              - `newLines: Optional<Long>`

              - `newStart: Optional<Long>`

              - `oldLines: Optional<Long>`

              - `oldStart: Optional<Long>`

          - `toolUseId: String`

          - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaToolSearchToolResultBlockParam:`

          - `content: Content`

            - `class BetaToolSearchToolResultErrorParam:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `type: JsonValue; "tool_search_tool_result_error"constant`

                - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

            - `class BetaToolSearchToolSearchResultBlockParam:`

              - `toolReferences: List<BetaToolReferenceBlockParam>`

                - `toolName: String`

                - `type: JsonValue; "tool_reference"constant`

                  - `TOOL_REFERENCE("tool_reference")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

              - `type: JsonValue; "tool_search_tool_search_result"constant`

                - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

          - `toolUseId: String`

          - `type: JsonValue; "tool_search_tool_result"constant`

            - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaMcpToolUseBlockParam:`

          - `id: String`

          - `input: Input`

          - `name: String`

          - `serverName: String`

            The name of the MCP server

          - `type: JsonValue; "mcp_tool_use"constant`

            - `MCP_TOOL_USE("mcp_tool_use")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaRequestMcpToolResultBlockParam:`

          - `toolUseId: String`

          - `type: JsonValue; "mcp_tool_result"constant`

            - `MCP_TOOL_RESULT("mcp_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `content: Optional<Content>`

            - `String`

            - `List<BetaTextBlockParam>`

              - `text: String`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<List<BetaTextCitationParam>>`

                - `class BetaCitationCharLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endCharIndex: Long`

                  - `startCharIndex: Long`

                  - `type: JsonValue; "char_location"constant`

                    - `CHAR_LOCATION("char_location")`

                - `class BetaCitationPageLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endPageNumber: Long`

                  - `startPageNumber: Long`

                  - `type: JsonValue; "page_location"constant`

                    - `PAGE_LOCATION("page_location")`

                - `class BetaCitationContentBlockLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endBlockIndex: Long`

                  - `startBlockIndex: Long`

                  - `type: JsonValue; "content_block_location"constant`

                    - `CONTENT_BLOCK_LOCATION("content_block_location")`

                - `class BetaCitationWebSearchResultLocationParam:`

                  - `citedText: String`

                  - `encryptedIndex: String`

                  - `title: Optional<String>`

                  - `type: JsonValue; "web_search_result_location"constant`

                    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                  - `url: String`

                - `class BetaCitationSearchResultLocationParam:`

                  - `citedText: String`

                  - `endBlockIndex: Long`

                  - `searchResultIndex: Long`

                  - `source: String`

                  - `startBlockIndex: Long`

                  - `title: Optional<String>`

                  - `type: JsonValue; "search_result_location"constant`

                    - `SEARCH_RESULT_LOCATION("search_result_location")`

          - `isError: Optional<Boolean>`

        - `class BetaContainerUploadBlockParam:`

          A content block that represents a file to be uploaded to the container
          Files uploaded via this block will be available in the container's input directory.

          - `fileId: String`

          - `type: JsonValue; "container_upload"constant`

            - `CONTAINER_UPLOAD("container_upload")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

    - `role: Role`

      - `USER("user")`

      - `ASSISTANT("assistant")`

  - `model: Model`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

  - `container: Optional<Container>`

    Container identifier for reuse across requests.

    - `class BetaContainerParams:`

      Container parameters with skills to be loaded.

      - `id: Optional<String>`

        Container id

      - `skills: Optional<List<BetaSkillParams>>`

        List of skills to load in the container

        - `skillId: String`

          Skill ID

        - `type: Type`

          Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

          - `ANTHROPIC("anthropic")`

          - `CUSTOM("custom")`

        - `version: Optional<String>`

          Skill version or 'latest' for most recent version

    - `String`

  - `contextManagement: Optional<BetaContextManagementConfig>`

    Context management configuration.

    This allows you to control how Claude manages context across multiple requests, such as whether to clear function results or not.

  - `mcpServers: Optional<List<BetaRequestMcpServerUrlDefinition>>`

    MCP servers to be utilized in this request

    - `name: String`

    - `type: JsonValue; "url"constant`

      - `URL("url")`

    - `url: String`

    - `authorizationToken: Optional<String>`

    - `toolConfiguration: Optional<BetaRequestMcpServerToolConfiguration>`

      - `allowedTools: Optional<List<String>>`

      - `enabled: Optional<Boolean>`

  - `metadata: Optional<BetaMetadata>`

    An object describing metadata about the request.

  - `outputConfig: Optional<BetaOutputConfig>`

    Configuration options for the model's output. Controls aspects like how much effort the model puts into its response.

  - `outputFormat: Optional<BetaJsonOutputFormat>`

    A schema to specify Claude's output format in responses.

  - `serviceTier: Optional<ServiceTier>`

    Determines whether to use priority capacity (if available) or standard capacity for this request.

    Anthropic offers different levels of service for your API requests. See [service-tiers](https://docs.claude.com/en/api/service-tiers) for details.

    - `AUTO("auto")`

    - `STANDARD_ONLY("standard_only")`

  - `stopSequences: Optional<List<String>>`

    Custom text sequences that will cause the model to stop generating.

    Our models will normally stop when they have naturally completed their turn, which will result in a response `stop_reason` of `"end_turn"`.

    If you want the model to stop generating when it encounters custom strings of text, you can use the `stop_sequences` parameter. If the model encounters one of the custom sequences, the response `stop_reason` value will be `"stop_sequence"` and the response `stop_sequence` value will contain the matched stop sequence.

  - `system: Optional<System>`

    System prompt.

    A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

    - `String`

    - `List<BetaTextBlockParam>`

      - `text: String`

      - `type: JsonValue; "text"constant`

        - `TEXT("text")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `citations: Optional<List<BetaTextCitationParam>>`

        - `class BetaCitationCharLocationParam:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endCharIndex: Long`

          - `startCharIndex: Long`

          - `type: JsonValue; "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class BetaCitationPageLocationParam:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endPageNumber: Long`

          - `startPageNumber: Long`

          - `type: JsonValue; "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class BetaCitationContentBlockLocationParam:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endBlockIndex: Long`

          - `startBlockIndex: Long`

          - `type: JsonValue; "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class BetaCitationWebSearchResultLocationParam:`

          - `citedText: String`

          - `encryptedIndex: String`

          - `title: Optional<String>`

          - `type: JsonValue; "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `url: String`

        - `class BetaCitationSearchResultLocationParam:`

          - `citedText: String`

          - `endBlockIndex: Long`

          - `searchResultIndex: Long`

          - `source: String`

          - `startBlockIndex: Long`

          - `title: Optional<String>`

          - `type: JsonValue; "search_result_location"constant`

            - `SEARCH_RESULT_LOCATION("search_result_location")`

  - `temperature: Optional<Double>`

    Amount of randomness injected into the response.

    Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.

    Note that even with `temperature` of `0.0`, the results will not be fully deterministic.

  - `thinking: Optional<BetaThinkingConfigParam>`

    Configuration for enabling Claude's extended thinking.

    When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `toolChoice: Optional<BetaToolChoice>`

    How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `tools: Optional<List<BetaToolUnion>>`

    Definitions of tools that the model may use.

    If you include `tools` in your API request, the model may return `tool_use` content blocks that represent the model's use of those tools. You can then run those tools using the tool input generated by the model and then optionally return results back to the model using `tool_result` content blocks.

    There are two types of tools: **client tools** and **server tools**. The behavior described below applies to client tools. For [server tools](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview#server-tools), see their individual documentation as each has its own behavior (e.g., the [web search tool](https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-search-tool)).

    Each tool definition includes:

    * `name`: Name of the tool.
    * `description`: Optional, but strongly-recommended description of the tool.
    * `input_schema`: [JSON schema](https://json-schema.org/draft/2020-12) for the tool `input` shape that the model will produce in `tool_use` output content blocks.

    For example, if you defined `tools` as:

    ```json
    [
      {
        "name": "get_stock_price",
        "description": "Get the current stock price for a given ticker symbol.",
        "input_schema": {
          "type": "object",
          "properties": {
            "ticker": {
              "type": "string",
              "description": "The stock ticker symbol, e.g. AAPL for Apple Inc."
            }
          },
          "required": ["ticker"]
        }
      }
    ]
    ```

    And then asked the model "What's the S&P 500 at today?", the model might produce `tool_use` content blocks in the response like this:

    ```json
    [
      {
        "type": "tool_use",
        "id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
        "name": "get_stock_price",
        "input": { "ticker": "^GSPC" }
      }
    ]
    ```

    You might then run your `get_stock_price` tool with `{"ticker": "^GSPC"}` as an input, and return the following back to the model in a subsequent `user` message:

    ```json
    [
      {
        "type": "tool_result",
        "tool_use_id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
        "content": "259.75 USD"
      }
    ]
    ```

    Tools can be used for workflows that include running client-side tools and functions, or more generally whenever you want the model to produce a particular JSON structure of output.

    See our [guide](https://docs.claude.com/en/docs/tool-use) for more details.

    - `class BetaTool:`

      - `inputSchema: InputSchema`

        [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

        This defines the shape of the `input` that your tool accepts and that the model will produce.

        - `type: JsonValue; "object"constant`

          - `OBJECT("object")`

        - `properties: Optional<Properties>`

        - `required: Optional<List<String>>`

      - `name: String`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `description: Optional<String>`

        Description of what this tool does.

        Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

      - `type: Optional<Type>`

        - `CUSTOM("custom")`

    - `class BetaToolBash20241022:`

      - `name: JsonValue; "bash"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `BASH("bash")`

      - `type: JsonValue; "bash_20241022"constant`

        - `BASH_20241022("bash_20241022")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolBash20250124:`

      - `name: JsonValue; "bash"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `BASH("bash")`

      - `type: JsonValue; "bash_20250124"constant`

        - `BASH_20250124("bash_20250124")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaCodeExecutionTool20250522:`

      - `name: JsonValue; "code_execution"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `CODE_EXECUTION("code_execution")`

      - `type: JsonValue; "code_execution_20250522"constant`

        - `CODE_EXECUTION_20250522("code_execution_20250522")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `strict: Optional<Boolean>`

    - `class BetaCodeExecutionTool20250825:`

      - `name: JsonValue; "code_execution"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `CODE_EXECUTION("code_execution")`

      - `type: JsonValue; "code_execution_20250825"constant`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `strict: Optional<Boolean>`

    - `class BetaToolComputerUse20241022:`

      - `displayHeightPx: Long`

        The height of the display in pixels.

      - `displayWidthPx: Long`

        The width of the display in pixels.

      - `name: JsonValue; "computer"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `COMPUTER("computer")`

      - `type: JsonValue; "computer_20241022"constant`

        - `COMPUTER_20241022("computer_20241022")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `displayNumber: Optional<Long>`

        The X11 display number (e.g. 0, 1) for the display.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaMemoryTool20250818:`

      - `name: JsonValue; "memory"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `MEMORY("memory")`

      - `type: JsonValue; "memory_20250818"constant`

        - `MEMORY_20250818("memory_20250818")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolComputerUse20250124:`

      - `displayHeightPx: Long`

        The height of the display in pixels.

      - `displayWidthPx: Long`

        The width of the display in pixels.

      - `name: JsonValue; "computer"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `COMPUTER("computer")`

      - `type: JsonValue; "computer_20250124"constant`

        - `COMPUTER_20250124("computer_20250124")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `displayNumber: Optional<Long>`

        The X11 display number (e.g. 0, 1) for the display.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolTextEditor20241022:`

      - `name: JsonValue; "str_replace_editor"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_EDITOR("str_replace_editor")`

      - `type: JsonValue; "text_editor_20241022"constant`

        - `TEXT_EDITOR_20241022("text_editor_20241022")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolComputerUse20251124:`

      - `displayHeightPx: Long`

        The height of the display in pixels.

      - `displayWidthPx: Long`

        The width of the display in pixels.

      - `name: JsonValue; "computer"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `COMPUTER("computer")`

      - `type: JsonValue; "computer_20251124"constant`

        - `COMPUTER_20251124("computer_20251124")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `displayNumber: Optional<Long>`

        The X11 display number (e.g. 0, 1) for the display.

      - `enableZoom: Optional<Boolean>`

        Whether to enable an action to take a zoomed-in screenshot of the screen.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolTextEditor20250124:`

      - `name: JsonValue; "str_replace_editor"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_EDITOR("str_replace_editor")`

      - `type: JsonValue; "text_editor_20250124"constant`

        - `TEXT_EDITOR_20250124("text_editor_20250124")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolTextEditor20250429:`

      - `name: JsonValue; "str_replace_based_edit_tool"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

      - `type: JsonValue; "text_editor_20250429"constant`

        - `TEXT_EDITOR_20250429("text_editor_20250429")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolTextEditor20250728:`

      - `name: JsonValue; "str_replace_based_edit_tool"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

      - `type: JsonValue; "text_editor_20250728"constant`

        - `TEXT_EDITOR_20250728("text_editor_20250728")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `maxCharacters: Optional<Long>`

        Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

      - `strict: Optional<Boolean>`

    - `class BetaWebSearchTool20250305:`

      - `name: JsonValue; "web_search"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `WEB_SEARCH("web_search")`

      - `type: JsonValue; "web_search_20250305"constant`

        - `WEB_SEARCH_20250305("web_search_20250305")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `allowedDomains: Optional<List<String>>`

        If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

      - `blockedDomains: Optional<List<String>>`

        If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `maxUses: Optional<Long>`

        Maximum number of times the tool can be used in the API request.

      - `strict: Optional<Boolean>`

      - `userLocation: Optional<UserLocation>`

        Parameters for the user's location. Used to provide more relevant search results.

        - `type: JsonValue; "approximate"constant`

          - `APPROXIMATE("approximate")`

        - `city: Optional<String>`

          The city of the user.

        - `country: Optional<String>`

          The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

        - `region: Optional<String>`

          The region of the user.

        - `timezone: Optional<String>`

          The [IANA timezone](https://nodatime.org/TimeZones) of the user.

    - `class BetaWebFetchTool20250910:`

      - `name: JsonValue; "web_fetch"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `WEB_FETCH("web_fetch")`

      - `type: JsonValue; "web_fetch_20250910"constant`

        - `WEB_FETCH_20250910("web_fetch_20250910")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `allowedDomains: Optional<List<String>>`

        List of domains to allow fetching from

      - `blockedDomains: Optional<List<String>>`

        List of domains to block fetching from

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `citations: Optional<BetaCitationsConfigParam>`

        Citations configuration for fetched documents. Citations are disabled by default.

        - `enabled: Optional<Boolean>`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `maxContentTokens: Optional<Long>`

        Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

      - `maxUses: Optional<Long>`

        Maximum number of times the tool can be used in the API request.

      - `strict: Optional<Boolean>`

    - `class BetaToolSearchToolBm25_20251119:`

      - `name: JsonValue; "tool_search_tool_bm25"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

      - `type: Type`

        - `TOOL_SEARCH_TOOL_BM25_20251119("tool_search_tool_bm25_20251119")`

        - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `strict: Optional<Boolean>`

    - `class BetaToolSearchToolRegex20251119:`

      - `name: JsonValue; "tool_search_tool_regex"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

      - `type: Type`

        - `TOOL_SEARCH_TOOL_REGEX_20251119("tool_search_tool_regex_20251119")`

        - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `strict: Optional<Boolean>`

    - `class BetaMcpToolset:`

      Configuration for a group of tools from an MCP server.

      Allows configuring enabled status and defer_loading for all tools
      from an MCP server, with optional per-tool overrides.

      - `mcpServerName: String`

        Name of the MCP server to configure tools for

      - `type: JsonValue; "mcp_toolset"constant`

        - `MCP_TOOLSET("mcp_toolset")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `configs: Optional<Configs>`

        Configuration overrides for specific tools, keyed by tool name

        - `deferLoading: Optional<Boolean>`

        - `enabled: Optional<Boolean>`

      - `defaultConfig: Optional<BetaMcpToolDefaultConfig>`

        Default configuration applied to all tools from this server

        - `deferLoading: Optional<Boolean>`

        - `enabled: Optional<Boolean>`

  - `topK: Optional<Long>`

    Only sample from the top K options for each subsequent token.

    Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

    Recommended for advanced use cases only. You usually only need to use `temperature`.

  - `topP: Optional<Double>`

    Use nucleus sampling.

    In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

    Recommended for advanced use cases only. You usually only need to use `temperature`.

### Returns

- `class BetaMessage:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `container: Optional<BetaContainer>`

    Information about the container used in the request (for the code execution tool)

    - `id: String`

      Identifier for the container used in this request

    - `expiresAt: LocalDateTime`

      The time at which the container will expire.

    - `skills: Optional<List<BetaSkill>>`

      Skills loaded in the container

      - `skillId: String`

        Skill ID

      - `type: Type`

        Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

        - `ANTHROPIC("anthropic")`

        - `CUSTOM("custom")`

      - `version: String`

        Skill version or 'latest' for most recent version

  - `content: List<BetaContentBlock>`

    Content generated by the model.

    This is an array of content blocks, each of which has a `type` that determines its shape.

    Example:

    ```json
    [{"type": "text", "text": "Hi, I'm Claude."}]
    ```

    If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

    For example, if the input `messages` were:

    ```json
    [
      {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
      {"role": "assistant", "content": "The best answer is ("}
    ]
    ```

    Then the response `content` might be:

    ```json
    [{"type": "text", "text": "B)"}]
    ```

    - `class BetaTextBlock:`

      - `citations: Optional<List<BetaTextCitation>>`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `class BetaCitationCharLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endCharIndex: Long`

          - `fileId: Optional<String>`

          - `startCharIndex: Long`

          - `type: JsonValue; "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class BetaCitationPageLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endPageNumber: Long`

          - `fileId: Optional<String>`

          - `startPageNumber: Long`

          - `type: JsonValue; "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class BetaCitationContentBlockLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endBlockIndex: Long`

          - `fileId: Optional<String>`

          - `startBlockIndex: Long`

          - `type: JsonValue; "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class BetaCitationsWebSearchResultLocation:`

          - `citedText: String`

          - `encryptedIndex: String`

          - `title: Optional<String>`

          - `type: JsonValue; "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `url: String`

        - `class BetaCitationSearchResultLocation:`

          - `citedText: String`

          - `endBlockIndex: Long`

          - `searchResultIndex: Long`

          - `source: String`

          - `startBlockIndex: Long`

          - `title: Optional<String>`

          - `type: JsonValue; "search_result_location"constant`

            - `SEARCH_RESULT_LOCATION("search_result_location")`

      - `text: String`

      - `type: JsonValue; "text"constant`

        - `TEXT("text")`

    - `class BetaThinkingBlock:`

      - `signature: String`

      - `thinking: String`

      - `type: JsonValue; "thinking"constant`

        - `THINKING("thinking")`

    - `class BetaRedactedThinkingBlock:`

      - `data: String`

      - `type: JsonValue; "redacted_thinking"constant`

        - `REDACTED_THINKING("redacted_thinking")`

    - `class BetaToolUseBlock:`

      - `id: String`

      - `input: Input`

      - `name: String`

      - `type: JsonValue; "tool_use"constant`

        - `TOOL_USE("tool_use")`

      - `caller: Optional<Caller>`

        Tool invocation directly from the model.

        - `class BetaDirectCaller:`

          Tool invocation directly from the model.

          - `type: JsonValue; "direct"constant`

            - `DIRECT("direct")`

        - `class BetaServerToolCaller:`

          Tool invocation generated by a server-side tool.

          - `toolId: String`

          - `type: JsonValue; "code_execution_20250825"constant`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `class BetaServerToolUseBlock:`

      - `id: String`

      - `caller: Caller`

        Tool invocation directly from the model.

        - `class BetaDirectCaller:`

          Tool invocation directly from the model.

          - `type: JsonValue; "direct"constant`

            - `DIRECT("direct")`

        - `class BetaServerToolCaller:`

          Tool invocation generated by a server-side tool.

          - `toolId: String`

          - `type: JsonValue; "code_execution_20250825"constant`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `input: Input`

      - `name: Name`

        - `WEB_SEARCH("web_search")`

        - `WEB_FETCH("web_fetch")`

        - `CODE_EXECUTION("code_execution")`

        - `BASH_CODE_EXECUTION("bash_code_execution")`

        - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

        - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

        - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

      - `type: JsonValue; "server_tool_use"constant`

        - `SERVER_TOOL_USE("server_tool_use")`

    - `class BetaWebSearchToolResultBlock:`

      - `content: BetaWebSearchToolResultBlockContent`

        - `class BetaWebSearchToolResultError:`

          - `errorCode: BetaWebSearchToolResultErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `MAX_USES_EXCEEDED("max_uses_exceeded")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `QUERY_TOO_LONG("query_too_long")`

          - `type: JsonValue; "web_search_tool_result_error"constant`

            - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

        - `List<BetaWebSearchResultBlock>`

          - `encryptedContent: String`

          - `pageAge: Optional<String>`

          - `title: String`

          - `type: JsonValue; "web_search_result"constant`

            - `WEB_SEARCH_RESULT("web_search_result")`

          - `url: String`

      - `toolUseId: String`

      - `type: JsonValue; "web_search_tool_result"constant`

        - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

    - `class BetaWebFetchToolResultBlock:`

      - `content: Content`

        - `class BetaWebFetchToolResultErrorBlock:`

          - `errorCode: BetaWebFetchToolResultErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `URL_TOO_LONG("url_too_long")`

            - `URL_NOT_ALLOWED("url_not_allowed")`

            - `URL_NOT_ACCESSIBLE("url_not_accessible")`

            - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `MAX_USES_EXCEEDED("max_uses_exceeded")`

            - `UNAVAILABLE("unavailable")`

          - `type: JsonValue; "web_fetch_tool_result_error"constant`

            - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

        - `class BetaWebFetchBlock:`

          - `content: BetaDocumentBlock`

            - `citations: Optional<BetaCitationConfig>`

              Citation configuration for the document

              - `enabled: Boolean`

            - `source: Source`

              - `class BetaBase64PdfSource:`

                - `data: String`

                - `mediaType: JsonValue; "application/pdf"constant`

                  - `APPLICATION_PDF("application/pdf")`

                - `type: JsonValue; "base64"constant`

                  - `BASE64("base64")`

              - `class BetaPlainTextSource:`

                - `data: String`

                - `mediaType: JsonValue; "text/plain"constant`

                  - `TEXT_PLAIN("text/plain")`

                - `type: JsonValue; "text"constant`

                  - `TEXT("text")`

            - `title: Optional<String>`

              The title of the document

            - `type: JsonValue; "document"constant`

              - `DOCUMENT("document")`

          - `retrievedAt: Optional<String>`

            ISO 8601 timestamp when the content was retrieved

          - `type: JsonValue; "web_fetch_result"constant`

            - `WEB_FETCH_RESULT("web_fetch_result")`

          - `url: String`

            Fetched content URL

      - `toolUseId: String`

      - `type: JsonValue; "web_fetch_tool_result"constant`

        - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

    - `class BetaCodeExecutionToolResultBlock:`

      - `content: BetaCodeExecutionToolResultBlockContent`

        - `class BetaCodeExecutionToolResultError:`

          - `errorCode: BetaCodeExecutionToolResultErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

          - `type: JsonValue; "code_execution_tool_result_error"constant`

            - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

        - `class BetaCodeExecutionResultBlock:`

          - `content: List<BetaCodeExecutionOutputBlock>`

            - `fileId: String`

            - `type: JsonValue; "code_execution_output"constant`

              - `CODE_EXECUTION_OUTPUT("code_execution_output")`

          - `returnCode: Long`

          - `stderr: String`

          - `stdout: String`

          - `type: JsonValue; "code_execution_result"constant`

            - `CODE_EXECUTION_RESULT("code_execution_result")`

      - `toolUseId: String`

      - `type: JsonValue; "code_execution_tool_result"constant`

        - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

    - `class BetaBashCodeExecutionToolResultBlock:`

      - `content: Content`

        - `class BetaBashCodeExecutionToolResultError:`

          - `errorCode: ErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

          - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

            - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

        - `class BetaBashCodeExecutionResultBlock:`

          - `content: List<BetaBashCodeExecutionOutputBlock>`

            - `fileId: String`

            - `type: JsonValue; "bash_code_execution_output"constant`

              - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

          - `returnCode: Long`

          - `stderr: String`

          - `stdout: String`

          - `type: JsonValue; "bash_code_execution_result"constant`

            - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

      - `toolUseId: String`

      - `type: JsonValue; "bash_code_execution_tool_result"constant`

        - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

    - `class BetaTextEditorCodeExecutionToolResultBlock:`

      - `content: Content`

        - `class BetaTextEditorCodeExecutionToolResultError:`

          - `errorCode: ErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `FILE_NOT_FOUND("file_not_found")`

          - `errorMessage: Optional<String>`

          - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

        - `class BetaTextEditorCodeExecutionViewResultBlock:`

          - `content: String`

          - `fileType: FileType`

            - `TEXT("text")`

            - `IMAGE("image")`

            - `PDF("pdf")`

          - `numLines: Optional<Long>`

          - `startLine: Optional<Long>`

          - `totalLines: Optional<Long>`

          - `type: JsonValue; "text_editor_code_execution_view_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

        - `class BetaTextEditorCodeExecutionCreateResultBlock:`

          - `isFileUpdate: Boolean`

          - `type: JsonValue; "text_editor_code_execution_create_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

        - `class BetaTextEditorCodeExecutionStrReplaceResultBlock:`

          - `lines: Optional<List<String>>`

          - `newLines: Optional<Long>`

          - `newStart: Optional<Long>`

          - `oldLines: Optional<Long>`

          - `oldStart: Optional<Long>`

          - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

      - `toolUseId: String`

      - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

        - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

    - `class BetaToolSearchToolResultBlock:`

      - `content: Content`

        - `class BetaToolSearchToolResultError:`

          - `errorCode: ErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

          - `errorMessage: Optional<String>`

          - `type: JsonValue; "tool_search_tool_result_error"constant`

            - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

        - `class BetaToolSearchToolSearchResultBlock:`

          - `toolReferences: List<BetaToolReferenceBlock>`

            - `toolName: String`

            - `type: JsonValue; "tool_reference"constant`

              - `TOOL_REFERENCE("tool_reference")`

          - `type: JsonValue; "tool_search_tool_search_result"constant`

            - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

      - `toolUseId: String`

      - `type: JsonValue; "tool_search_tool_result"constant`

        - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

    - `class BetaMcpToolUseBlock:`

      - `id: String`

      - `input: Input`

      - `name: String`

        The name of the MCP tool

      - `serverName: String`

        The name of the MCP server

      - `type: JsonValue; "mcp_tool_use"constant`

        - `MCP_TOOL_USE("mcp_tool_use")`

    - `class BetaMcpToolResultBlock:`

      - `content: Content`

        - `String`

        - `List<BetaTextBlock>`

          - `citations: Optional<List<BetaTextCitation>>`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `class BetaCitationCharLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `fileId: Optional<String>`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class BetaCitationPageLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `fileId: Optional<String>`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class BetaCitationContentBlockLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `fileId: Optional<String>`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class BetaCitationsWebSearchResultLocation:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class BetaCitationSearchResultLocation:`

              - `citedText: String`

              - `endBlockIndex: Long`

              - `searchResultIndex: Long`

              - `source: String`

              - `startBlockIndex: Long`

              - `title: Optional<String>`

              - `type: JsonValue; "search_result_location"constant`

                - `SEARCH_RESULT_LOCATION("search_result_location")`

          - `text: String`

          - `type: JsonValue; "text"constant`

            - `TEXT("text")`

      - `isError: Boolean`

      - `toolUseId: String`

      - `type: JsonValue; "mcp_tool_result"constant`

        - `MCP_TOOL_RESULT("mcp_tool_result")`

    - `class BetaContainerUploadBlock:`

      Response model for a file uploaded to the container.

      - `fileId: String`

      - `type: JsonValue; "container_upload"constant`

        - `CONTAINER_UPLOAD("container_upload")`

  - `contextManagement: Optional<BetaContextManagementResponse>`

    Context management response.

    Information about context management strategies applied during the request.

    - `appliedEdits: List<AppliedEdit>`

      List of context management edits that were applied.

      - `class BetaClearToolUses20250919EditResponse:`

        - `clearedInputTokens: Long`

          Number of input tokens cleared by this edit.

        - `clearedToolUses: Long`

          Number of tool uses that were cleared.

        - `type: JsonValue; "clear_tool_uses_20250919"constant`

          The type of context management edit applied.

          - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

      - `class BetaClearThinking20251015EditResponse:`

        - `clearedInputTokens: Long`

          Number of input tokens cleared by this edit.

        - `clearedThinkingTurns: Long`

          Number of thinking turns that were cleared.

        - `type: JsonValue; "clear_thinking_20251015"constant`

          The type of context management edit applied.

          - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

  - `model: Model`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

    - `CLAUDE_OPUS_4_5_20251101("claude-opus-4-5-20251101")`

      Premium model combining maximum intelligence with practical performance

    - `CLAUDE_OPUS_4_5("claude-opus-4-5")`

      Premium model combining maximum intelligence with practical performance

    - `CLAUDE_3_7_SONNET_LATEST("claude-3-7-sonnet-latest")`

      High-performance model with early extended thinking

    - `CLAUDE_3_7_SONNET_20250219("claude-3-7-sonnet-20250219")`

      High-performance model with early extended thinking

    - `CLAUDE_3_5_HAIKU_LATEST("claude-3-5-haiku-latest")`

      Fastest and most compact model for near-instant responsiveness

    - `CLAUDE_3_5_HAIKU_20241022("claude-3-5-haiku-20241022")`

      Our fastest model

    - `CLAUDE_HAIKU_4_5("claude-haiku-4-5")`

      Hybrid model, capable of near-instant responses and extended thinking

    - `CLAUDE_HAIKU_4_5_20251001("claude-haiku-4-5-20251001")`

      Hybrid model, capable of near-instant responses and extended thinking

    - `CLAUDE_SONNET_4_20250514("claude-sonnet-4-20250514")`

      High-performance model with extended thinking

    - `CLAUDE_SONNET_4_0("claude-sonnet-4-0")`

      High-performance model with extended thinking

    - `CLAUDE_4_SONNET_20250514("claude-4-sonnet-20250514")`

      High-performance model with extended thinking

    - `CLAUDE_SONNET_4_5("claude-sonnet-4-5")`

      Our best model for real-world agents and coding

    - `CLAUDE_SONNET_4_5_20250929("claude-sonnet-4-5-20250929")`

      Our best model for real-world agents and coding

    - `CLAUDE_OPUS_4_0("claude-opus-4-0")`

      Our most capable model

    - `CLAUDE_OPUS_4_20250514("claude-opus-4-20250514")`

      Our most capable model

    - `CLAUDE_4_OPUS_20250514("claude-4-opus-20250514")`

      Our most capable model

    - `CLAUDE_OPUS_4_1_20250805("claude-opus-4-1-20250805")`

      Our most capable model

    - `CLAUDE_3_OPUS_LATEST("claude-3-opus-latest")`

      Excels at writing and complex tasks

    - `CLAUDE_3_OPUS_20240229("claude-3-opus-20240229")`

      Excels at writing and complex tasks

    - `CLAUDE_3_HAIKU_20240307("claude-3-haiku-20240307")`

      Our previous most fast and cost-effective

  - `role: JsonValue; "assistant"constant`

    Conversational role of the generated message.

    This will always be `"assistant"`.

    - `ASSISTANT("assistant")`

  - `stopReason: Optional<BetaStopReason>`

    The reason that we stopped.

    This may be one the following values:

    * `"end_turn"`: the model reached a natural stopping point
    * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
    * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
    * `"tool_use"`: the model invoked one or more tools
    * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
    * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

    In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

    - `END_TURN("end_turn")`

    - `MAX_TOKENS("max_tokens")`

    - `STOP_SEQUENCE("stop_sequence")`

    - `TOOL_USE("tool_use")`

    - `PAUSE_TURN("pause_turn")`

    - `REFUSAL("refusal")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED("model_context_window_exceeded")`

  - `stopSequence: Optional<String>`

    Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was generated.

  - `type: JsonValue; "message"constant`

    Object type.

    For Messages, this is always `"message"`.

    - `MESSAGE("message")`

  - `usage: BetaUsage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cacheCreation: Optional<BetaCacheCreation>`

      Breakdown of cached tokens by TTL

      - `ephemeral1hInputTokens: Long`

        The number of input tokens used to create the 1 hour cache entry.

      - `ephemeral5mInputTokens: Long`

        The number of input tokens used to create the 5 minute cache entry.

    - `cacheCreationInputTokens: Optional<Long>`

      The number of input tokens used to create the cache entry.

    - `cacheReadInputTokens: Optional<Long>`

      The number of input tokens read from the cache.

    - `inputTokens: Long`

      The number of input tokens which were used.

    - `outputTokens: Long`

      The number of output tokens which were used.

    - `serverToolUse: Optional<BetaServerToolUsage>`

      The number of server tool requests.

      - `webFetchRequests: Long`

        The number of web fetch tool requests.

      - `webSearchRequests: Long`

        The number of web search tool requests.

    - `serviceTier: Optional<ServiceTier>`

      If the request used the priority, standard, or batch tier.

      - `STANDARD("standard")`

      - `PRIORITY("priority")`

      - `BATCH("batch")`

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.messages.BetaMessage
import com.anthropic.models.beta.messages.MessageCreateParams
import com.anthropic.models.messages.Model

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val params: MessageCreateParams = MessageCreateParams.builder()
        .maxTokens(1024L)
        .addUserMessage("Hello, world")
        .model(Model.CLAUDE_OPUS_4_5_20251101)
        .build()
    val betaMessage: BetaMessage = client.beta().messages().create(params)
}
```

## Count Tokens

`beta().messages().countTokens(MessageCountTokensParamsparams, RequestOptionsrequestOptions = RequestOptions.none()) : BetaMessageTokensCount`

**post** `/v1/messages/count_tokens`

Count the number of tokens in a Message.

The Token Count API can be used to count the number of tokens in a Message, including tools, images, and documents, without creating it.

Learn more about token counting in our [user guide](https://docs.claude.com/en/docs/build-with-claude/token-counting)

### Parameters

- `params: MessageCountTokensParams`

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

  - `messages: List<BetaMessageParam>`

    Input messages.

    Our models are trained to operate on alternating `user` and `assistant` conversational turns. When creating a new `Message`, you specify the prior conversational turns with the `messages` parameter, and the model then generates the next `Message` in the conversation. Consecutive `user` or `assistant` turns in your request will be combined into a single turn.

    Each input message must be an object with a `role` and `content`. You can specify a single `user`-role message, or you can include multiple `user` and `assistant` messages.

    If the final message uses the `assistant` role, the response content will continue immediately from the content in that message. This can be used to constrain part of the model's response.

    Example with a single `user` message:

    ```json
    [{"role": "user", "content": "Hello, Claude"}]
    ```

    Example with multiple conversational turns:

    ```json
    [
      {"role": "user", "content": "Hello there."},
      {"role": "assistant", "content": "Hi, I'm Claude. How can I help you?"},
      {"role": "user", "content": "Can you explain LLMs in plain English?"},
    ]
    ```

    Example with a partially-filled response from Claude:

    ```json
    [
      {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
      {"role": "assistant", "content": "The best answer is ("},
    ]
    ```

    Each input message `content` may be either a single `string` or an array of content blocks, where each block has a specific `type`. Using a `string` for `content` is shorthand for an array of one content block of type `"text"`. The following input messages are equivalent:

    ```json
    {"role": "user", "content": "Hello, Claude"}
    ```

    ```json
    {"role": "user", "content": [{"type": "text", "text": "Hello, Claude"}]}
    ```

    See [input examples](https://docs.claude.com/en/api/messages-examples).

    Note that if you want to include a [system prompt](https://docs.claude.com/en/docs/system-prompts), you can use the top-level `system` parameter — there is no `"system"` role for input messages in the Messages API.

    There is a limit of 100,000 messages in a single request.

    - `content: Content`

      - `String`

      - `List<BetaContentBlockParam>`

        - `class BetaTextBlockParam:`

          - `text: String`

          - `type: JsonValue; "text"constant`

            - `TEXT("text")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<List<BetaTextCitationParam>>`

            - `class BetaCitationCharLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class BetaCitationPageLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class BetaCitationContentBlockLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class BetaCitationWebSearchResultLocationParam:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class BetaCitationSearchResultLocationParam:`

              - `citedText: String`

              - `endBlockIndex: Long`

              - `searchResultIndex: Long`

              - `source: String`

              - `startBlockIndex: Long`

              - `title: Optional<String>`

              - `type: JsonValue; "search_result_location"constant`

                - `SEARCH_RESULT_LOCATION("search_result_location")`

        - `class BetaImageBlockParam:`

          - `source: Source`

            - `class BetaBase64ImageSource:`

              - `data: String`

              - `mediaType: MediaType`

                - `IMAGE_JPEG("image/jpeg")`

                - `IMAGE_PNG("image/png")`

                - `IMAGE_GIF("image/gif")`

                - `IMAGE_WEBP("image/webp")`

              - `type: JsonValue; "base64"constant`

                - `BASE64("base64")`

            - `class BetaUrlImageSource:`

              - `type: JsonValue; "url"constant`

                - `URL("url")`

              - `url: String`

            - `class BetaFileImageSource:`

              - `fileId: String`

              - `type: JsonValue; "file"constant`

                - `FILE("file")`

          - `type: JsonValue; "image"constant`

            - `IMAGE("image")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaRequestDocumentBlock:`

          - `source: Source`

            - `class BetaBase64PdfSource:`

              - `data: String`

              - `mediaType: JsonValue; "application/pdf"constant`

                - `APPLICATION_PDF("application/pdf")`

              - `type: JsonValue; "base64"constant`

                - `BASE64("base64")`

            - `class BetaPlainTextSource:`

              - `data: String`

              - `mediaType: JsonValue; "text/plain"constant`

                - `TEXT_PLAIN("text/plain")`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

            - `class BetaContentBlockSource:`

              - `content: Content`

                - `String`

                - `List<BetaContentBlockSourceContent>`

                  - `class BetaTextBlockParam:`

                    - `text: String`

                    - `type: JsonValue; "text"constant`

                      - `TEXT("text")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                    - `citations: Optional<List<BetaTextCitationParam>>`

                      - `class BetaCitationCharLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endCharIndex: Long`

                        - `startCharIndex: Long`

                        - `type: JsonValue; "char_location"constant`

                          - `CHAR_LOCATION("char_location")`

                      - `class BetaCitationPageLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endPageNumber: Long`

                        - `startPageNumber: Long`

                        - `type: JsonValue; "page_location"constant`

                          - `PAGE_LOCATION("page_location")`

                      - `class BetaCitationContentBlockLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endBlockIndex: Long`

                        - `startBlockIndex: Long`

                        - `type: JsonValue; "content_block_location"constant`

                          - `CONTENT_BLOCK_LOCATION("content_block_location")`

                      - `class BetaCitationWebSearchResultLocationParam:`

                        - `citedText: String`

                        - `encryptedIndex: String`

                        - `title: Optional<String>`

                        - `type: JsonValue; "web_search_result_location"constant`

                          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                        - `url: String`

                      - `class BetaCitationSearchResultLocationParam:`

                        - `citedText: String`

                        - `endBlockIndex: Long`

                        - `searchResultIndex: Long`

                        - `source: String`

                        - `startBlockIndex: Long`

                        - `title: Optional<String>`

                        - `type: JsonValue; "search_result_location"constant`

                          - `SEARCH_RESULT_LOCATION("search_result_location")`

                  - `class BetaImageBlockParam:`

                    - `source: Source`

                      - `class BetaBase64ImageSource:`

                        - `data: String`

                        - `mediaType: MediaType`

                          - `IMAGE_JPEG("image/jpeg")`

                          - `IMAGE_PNG("image/png")`

                          - `IMAGE_GIF("image/gif")`

                          - `IMAGE_WEBP("image/webp")`

                        - `type: JsonValue; "base64"constant`

                          - `BASE64("base64")`

                      - `class BetaUrlImageSource:`

                        - `type: JsonValue; "url"constant`

                          - `URL("url")`

                        - `url: String`

                      - `class BetaFileImageSource:`

                        - `fileId: String`

                        - `type: JsonValue; "file"constant`

                          - `FILE("file")`

                    - `type: JsonValue; "image"constant`

                      - `IMAGE("image")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

              - `type: JsonValue; "content"constant`

                - `CONTENT("content")`

            - `class BetaUrlPdfSource:`

              - `type: JsonValue; "url"constant`

                - `URL("url")`

              - `url: String`

            - `class BetaFileDocumentSource:`

              - `fileId: String`

              - `type: JsonValue; "file"constant`

                - `FILE("file")`

          - `type: JsonValue; "document"constant`

            - `DOCUMENT("document")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<BetaCitationsConfigParam>`

            - `enabled: Optional<Boolean>`

          - `context: Optional<String>`

          - `title: Optional<String>`

        - `class BetaSearchResultBlockParam:`

          - `content: List<BetaTextBlockParam>`

            - `text: String`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

            - `cacheControl: Optional<BetaCacheControlEphemeral>`

              Create a cache control breakpoint at this content block.

              - `type: JsonValue; "ephemeral"constant`

                - `EPHEMERAL("ephemeral")`

              - `ttl: Optional<Ttl>`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `TTL_5M("5m")`

                - `TTL_1H("1h")`

            - `citations: Optional<List<BetaTextCitationParam>>`

              - `class BetaCitationCharLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endCharIndex: Long`

                - `startCharIndex: Long`

                - `type: JsonValue; "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class BetaCitationPageLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endPageNumber: Long`

                - `startPageNumber: Long`

                - `type: JsonValue; "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class BetaCitationContentBlockLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endBlockIndex: Long`

                - `startBlockIndex: Long`

                - `type: JsonValue; "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class BetaCitationWebSearchResultLocationParam:`

                - `citedText: String`

                - `encryptedIndex: String`

                - `title: Optional<String>`

                - `type: JsonValue; "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `url: String`

              - `class BetaCitationSearchResultLocationParam:`

                - `citedText: String`

                - `endBlockIndex: Long`

                - `searchResultIndex: Long`

                - `source: String`

                - `startBlockIndex: Long`

                - `title: Optional<String>`

                - `type: JsonValue; "search_result_location"constant`

                  - `SEARCH_RESULT_LOCATION("search_result_location")`

          - `source: String`

          - `title: String`

          - `type: JsonValue; "search_result"constant`

            - `SEARCH_RESULT("search_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<BetaCitationsConfigParam>`

            - `enabled: Optional<Boolean>`

        - `class BetaThinkingBlockParam:`

          - `signature: String`

          - `thinking: String`

          - `type: JsonValue; "thinking"constant`

            - `THINKING("thinking")`

        - `class BetaRedactedThinkingBlockParam:`

          - `data: String`

          - `type: JsonValue; "redacted_thinking"constant`

            - `REDACTED_THINKING("redacted_thinking")`

        - `class BetaToolUseBlockParam:`

          - `id: String`

          - `input: Input`

          - `name: String`

          - `type: JsonValue; "tool_use"constant`

            - `TOOL_USE("tool_use")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `caller: Optional<Caller>`

            Tool invocation directly from the model.

            - `class BetaDirectCaller:`

              Tool invocation directly from the model.

              - `type: JsonValue; "direct"constant`

                - `DIRECT("direct")`

            - `class BetaServerToolCaller:`

              Tool invocation generated by a server-side tool.

              - `toolId: String`

              - `type: JsonValue; "code_execution_20250825"constant`

                - `CODE_EXECUTION_20250825("code_execution_20250825")`

        - `class BetaToolResultBlockParam:`

          - `toolUseId: String`

          - `type: JsonValue; "tool_result"constant`

            - `TOOL_RESULT("tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `content: Optional<Content>`

            - `String`

            - `List<Block>`

              - `class BetaTextBlockParam:`

                - `text: String`

                - `type: JsonValue; "text"constant`

                  - `TEXT("text")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `citations: Optional<List<BetaTextCitationParam>>`

                  - `class BetaCitationCharLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endCharIndex: Long`

                    - `startCharIndex: Long`

                    - `type: JsonValue; "char_location"constant`

                      - `CHAR_LOCATION("char_location")`

                  - `class BetaCitationPageLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endPageNumber: Long`

                    - `startPageNumber: Long`

                    - `type: JsonValue; "page_location"constant`

                      - `PAGE_LOCATION("page_location")`

                  - `class BetaCitationContentBlockLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endBlockIndex: Long`

                    - `startBlockIndex: Long`

                    - `type: JsonValue; "content_block_location"constant`

                      - `CONTENT_BLOCK_LOCATION("content_block_location")`

                  - `class BetaCitationWebSearchResultLocationParam:`

                    - `citedText: String`

                    - `encryptedIndex: String`

                    - `title: Optional<String>`

                    - `type: JsonValue; "web_search_result_location"constant`

                      - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                    - `url: String`

                  - `class BetaCitationSearchResultLocationParam:`

                    - `citedText: String`

                    - `endBlockIndex: Long`

                    - `searchResultIndex: Long`

                    - `source: String`

                    - `startBlockIndex: Long`

                    - `title: Optional<String>`

                    - `type: JsonValue; "search_result_location"constant`

                      - `SEARCH_RESULT_LOCATION("search_result_location")`

              - `class BetaImageBlockParam:`

                - `source: Source`

                  - `class BetaBase64ImageSource:`

                    - `data: String`

                    - `mediaType: MediaType`

                      - `IMAGE_JPEG("image/jpeg")`

                      - `IMAGE_PNG("image/png")`

                      - `IMAGE_GIF("image/gif")`

                      - `IMAGE_WEBP("image/webp")`

                    - `type: JsonValue; "base64"constant`

                      - `BASE64("base64")`

                  - `class BetaUrlImageSource:`

                    - `type: JsonValue; "url"constant`

                      - `URL("url")`

                    - `url: String`

                  - `class BetaFileImageSource:`

                    - `fileId: String`

                    - `type: JsonValue; "file"constant`

                      - `FILE("file")`

                - `type: JsonValue; "image"constant`

                  - `IMAGE("image")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

              - `class BetaSearchResultBlockParam:`

                - `content: List<BetaTextBlockParam>`

                  - `text: String`

                  - `type: JsonValue; "text"constant`

                    - `TEXT("text")`

                  - `cacheControl: Optional<BetaCacheControlEphemeral>`

                    Create a cache control breakpoint at this content block.

                    - `type: JsonValue; "ephemeral"constant`

                      - `EPHEMERAL("ephemeral")`

                    - `ttl: Optional<Ttl>`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `TTL_5M("5m")`

                      - `TTL_1H("1h")`

                  - `citations: Optional<List<BetaTextCitationParam>>`

                    - `class BetaCitationCharLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endCharIndex: Long`

                      - `startCharIndex: Long`

                      - `type: JsonValue; "char_location"constant`

                        - `CHAR_LOCATION("char_location")`

                    - `class BetaCitationPageLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endPageNumber: Long`

                      - `startPageNumber: Long`

                      - `type: JsonValue; "page_location"constant`

                        - `PAGE_LOCATION("page_location")`

                    - `class BetaCitationContentBlockLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endBlockIndex: Long`

                      - `startBlockIndex: Long`

                      - `type: JsonValue; "content_block_location"constant`

                        - `CONTENT_BLOCK_LOCATION("content_block_location")`

                    - `class BetaCitationWebSearchResultLocationParam:`

                      - `citedText: String`

                      - `encryptedIndex: String`

                      - `title: Optional<String>`

                      - `type: JsonValue; "web_search_result_location"constant`

                        - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                      - `url: String`

                    - `class BetaCitationSearchResultLocationParam:`

                      - `citedText: String`

                      - `endBlockIndex: Long`

                      - `searchResultIndex: Long`

                      - `source: String`

                      - `startBlockIndex: Long`

                      - `title: Optional<String>`

                      - `type: JsonValue; "search_result_location"constant`

                        - `SEARCH_RESULT_LOCATION("search_result_location")`

                - `source: String`

                - `title: String`

                - `type: JsonValue; "search_result"constant`

                  - `SEARCH_RESULT("search_result")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `citations: Optional<BetaCitationsConfigParam>`

                  - `enabled: Optional<Boolean>`

              - `class BetaRequestDocumentBlock:`

                - `source: Source`

                  - `class BetaBase64PdfSource:`

                    - `data: String`

                    - `mediaType: JsonValue; "application/pdf"constant`

                      - `APPLICATION_PDF("application/pdf")`

                    - `type: JsonValue; "base64"constant`

                      - `BASE64("base64")`

                  - `class BetaPlainTextSource:`

                    - `data: String`

                    - `mediaType: JsonValue; "text/plain"constant`

                      - `TEXT_PLAIN("text/plain")`

                    - `type: JsonValue; "text"constant`

                      - `TEXT("text")`

                  - `class BetaContentBlockSource:`

                    - `content: Content`

                      - `String`

                      - `List<BetaContentBlockSourceContent>`

                        - `class BetaTextBlockParam:`

                          - `text: String`

                          - `type: JsonValue; "text"constant`

                            - `TEXT("text")`

                          - `cacheControl: Optional<BetaCacheControlEphemeral>`

                            Create a cache control breakpoint at this content block.

                            - `type: JsonValue; "ephemeral"constant`

                              - `EPHEMERAL("ephemeral")`

                            - `ttl: Optional<Ttl>`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `TTL_5M("5m")`

                              - `TTL_1H("1h")`

                          - `citations: Optional<List<BetaTextCitationParam>>`

                            - `class BetaCitationCharLocationParam:`

                              - `citedText: String`

                              - `documentIndex: Long`

                              - `documentTitle: Optional<String>`

                              - `endCharIndex: Long`

                              - `startCharIndex: Long`

                              - `type: JsonValue; "char_location"constant`

                                - `CHAR_LOCATION("char_location")`

                            - `class BetaCitationPageLocationParam:`

                              - `citedText: String`

                              - `documentIndex: Long`

                              - `documentTitle: Optional<String>`

                              - `endPageNumber: Long`

                              - `startPageNumber: Long`

                              - `type: JsonValue; "page_location"constant`

                                - `PAGE_LOCATION("page_location")`

                            - `class BetaCitationContentBlockLocationParam:`

                              - `citedText: String`

                              - `documentIndex: Long`

                              - `documentTitle: Optional<String>`

                              - `endBlockIndex: Long`

                              - `startBlockIndex: Long`

                              - `type: JsonValue; "content_block_location"constant`

                                - `CONTENT_BLOCK_LOCATION("content_block_location")`

                            - `class BetaCitationWebSearchResultLocationParam:`

                              - `citedText: String`

                              - `encryptedIndex: String`

                              - `title: Optional<String>`

                              - `type: JsonValue; "web_search_result_location"constant`

                                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                              - `url: String`

                            - `class BetaCitationSearchResultLocationParam:`

                              - `citedText: String`

                              - `endBlockIndex: Long`

                              - `searchResultIndex: Long`

                              - `source: String`

                              - `startBlockIndex: Long`

                              - `title: Optional<String>`

                              - `type: JsonValue; "search_result_location"constant`

                                - `SEARCH_RESULT_LOCATION("search_result_location")`

                        - `class BetaImageBlockParam:`

                          - `source: Source`

                            - `class BetaBase64ImageSource:`

                              - `data: String`

                              - `mediaType: MediaType`

                                - `IMAGE_JPEG("image/jpeg")`

                                - `IMAGE_PNG("image/png")`

                                - `IMAGE_GIF("image/gif")`

                                - `IMAGE_WEBP("image/webp")`

                              - `type: JsonValue; "base64"constant`

                                - `BASE64("base64")`

                            - `class BetaUrlImageSource:`

                              - `type: JsonValue; "url"constant`

                                - `URL("url")`

                              - `url: String`

                            - `class BetaFileImageSource:`

                              - `fileId: String`

                              - `type: JsonValue; "file"constant`

                                - `FILE("file")`

                          - `type: JsonValue; "image"constant`

                            - `IMAGE("image")`

                          - `cacheControl: Optional<BetaCacheControlEphemeral>`

                            Create a cache control breakpoint at this content block.

                            - `type: JsonValue; "ephemeral"constant`

                              - `EPHEMERAL("ephemeral")`

                            - `ttl: Optional<Ttl>`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `TTL_5M("5m")`

                              - `TTL_1H("1h")`

                    - `type: JsonValue; "content"constant`

                      - `CONTENT("content")`

                  - `class BetaUrlPdfSource:`

                    - `type: JsonValue; "url"constant`

                      - `URL("url")`

                    - `url: String`

                  - `class BetaFileDocumentSource:`

                    - `fileId: String`

                    - `type: JsonValue; "file"constant`

                      - `FILE("file")`

                - `type: JsonValue; "document"constant`

                  - `DOCUMENT("document")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `citations: Optional<BetaCitationsConfigParam>`

                  - `enabled: Optional<Boolean>`

                - `context: Optional<String>`

                - `title: Optional<String>`

              - `class BetaToolReferenceBlockParam:`

                Tool reference block that can be included in tool_result content.

                - `toolName: String`

                - `type: JsonValue; "tool_reference"constant`

                  - `TOOL_REFERENCE("tool_reference")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

          - `isError: Optional<Boolean>`

        - `class BetaServerToolUseBlockParam:`

          - `id: String`

          - `input: Input`

          - `name: Name`

            - `WEB_SEARCH("web_search")`

            - `WEB_FETCH("web_fetch")`

            - `CODE_EXECUTION("code_execution")`

            - `BASH_CODE_EXECUTION("bash_code_execution")`

            - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

            - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

            - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

          - `type: JsonValue; "server_tool_use"constant`

            - `SERVER_TOOL_USE("server_tool_use")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `caller: Optional<Caller>`

            Tool invocation directly from the model.

            - `class BetaDirectCaller:`

              Tool invocation directly from the model.

              - `type: JsonValue; "direct"constant`

                - `DIRECT("direct")`

            - `class BetaServerToolCaller:`

              Tool invocation generated by a server-side tool.

              - `toolId: String`

              - `type: JsonValue; "code_execution_20250825"constant`

                - `CODE_EXECUTION_20250825("code_execution_20250825")`

        - `class BetaWebSearchToolResultBlockParam:`

          - `content: BetaWebSearchToolResultBlockParamContent`

            - `List<BetaWebSearchResultBlockParam>`

              - `encryptedContent: String`

              - `title: String`

              - `type: JsonValue; "web_search_result"constant`

                - `WEB_SEARCH_RESULT("web_search_result")`

              - `url: String`

              - `pageAge: Optional<String>`

            - `class BetaWebSearchToolRequestError:`

              - `errorCode: BetaWebSearchToolResultErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `QUERY_TOO_LONG("query_too_long")`

              - `type: JsonValue; "web_search_tool_result_error"constant`

                - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

          - `toolUseId: String`

          - `type: JsonValue; "web_search_tool_result"constant`

            - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaWebFetchToolResultBlockParam:`

          - `content: Content`

            - `class BetaWebFetchToolResultErrorBlockParam:`

              - `errorCode: BetaWebFetchToolResultErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `URL_TOO_LONG("url_too_long")`

                - `URL_NOT_ALLOWED("url_not_allowed")`

                - `URL_NOT_ACCESSIBLE("url_not_accessible")`

                - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                - `UNAVAILABLE("unavailable")`

              - `type: JsonValue; "web_fetch_tool_result_error"constant`

                - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

            - `class BetaWebFetchBlockParam:`

              - `content: BetaRequestDocumentBlock`

                - `source: Source`

                  - `class BetaBase64PdfSource:`

                    - `data: String`

                    - `mediaType: JsonValue; "application/pdf"constant`

                      - `APPLICATION_PDF("application/pdf")`

                    - `type: JsonValue; "base64"constant`

                      - `BASE64("base64")`

                  - `class BetaPlainTextSource:`

                    - `data: String`

                    - `mediaType: JsonValue; "text/plain"constant`

                      - `TEXT_PLAIN("text/plain")`

                    - `type: JsonValue; "text"constant`

                      - `TEXT("text")`

                  - `class BetaContentBlockSource:`

                    - `content: Content`

                      - `String`

                      - `List<BetaContentBlockSourceContent>`

                        - `class BetaTextBlockParam:`

                          - `text: String`

                          - `type: JsonValue; "text"constant`

                            - `TEXT("text")`

                          - `cacheControl: Optional<BetaCacheControlEphemeral>`

                            Create a cache control breakpoint at this content block.

                            - `type: JsonValue; "ephemeral"constant`

                              - `EPHEMERAL("ephemeral")`

                            - `ttl: Optional<Ttl>`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `TTL_5M("5m")`

                              - `TTL_1H("1h")`

                          - `citations: Optional<List<BetaTextCitationParam>>`

                            - `class BetaCitationCharLocationParam:`

                              - `citedText: String`

                              - `documentIndex: Long`

                              - `documentTitle: Optional<String>`

                              - `endCharIndex: Long`

                              - `startCharIndex: Long`

                              - `type: JsonValue; "char_location"constant`

                                - `CHAR_LOCATION("char_location")`

                            - `class BetaCitationPageLocationParam:`

                              - `citedText: String`

                              - `documentIndex: Long`

                              - `documentTitle: Optional<String>`

                              - `endPageNumber: Long`

                              - `startPageNumber: Long`

                              - `type: JsonValue; "page_location"constant`

                                - `PAGE_LOCATION("page_location")`

                            - `class BetaCitationContentBlockLocationParam:`

                              - `citedText: String`

                              - `documentIndex: Long`

                              - `documentTitle: Optional<String>`

                              - `endBlockIndex: Long`

                              - `startBlockIndex: Long`

                              - `type: JsonValue; "content_block_location"constant`

                                - `CONTENT_BLOCK_LOCATION("content_block_location")`

                            - `class BetaCitationWebSearchResultLocationParam:`

                              - `citedText: String`

                              - `encryptedIndex: String`

                              - `title: Optional<String>`

                              - `type: JsonValue; "web_search_result_location"constant`

                                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                              - `url: String`

                            - `class BetaCitationSearchResultLocationParam:`

                              - `citedText: String`

                              - `endBlockIndex: Long`

                              - `searchResultIndex: Long`

                              - `source: String`

                              - `startBlockIndex: Long`

                              - `title: Optional<String>`

                              - `type: JsonValue; "search_result_location"constant`

                                - `SEARCH_RESULT_LOCATION("search_result_location")`

                        - `class BetaImageBlockParam:`

                          - `source: Source`

                            - `class BetaBase64ImageSource:`

                              - `data: String`

                              - `mediaType: MediaType`

                                - `IMAGE_JPEG("image/jpeg")`

                                - `IMAGE_PNG("image/png")`

                                - `IMAGE_GIF("image/gif")`

                                - `IMAGE_WEBP("image/webp")`

                              - `type: JsonValue; "base64"constant`

                                - `BASE64("base64")`

                            - `class BetaUrlImageSource:`

                              - `type: JsonValue; "url"constant`

                                - `URL("url")`

                              - `url: String`

                            - `class BetaFileImageSource:`

                              - `fileId: String`

                              - `type: JsonValue; "file"constant`

                                - `FILE("file")`

                          - `type: JsonValue; "image"constant`

                            - `IMAGE("image")`

                          - `cacheControl: Optional<BetaCacheControlEphemeral>`

                            Create a cache control breakpoint at this content block.

                            - `type: JsonValue; "ephemeral"constant`

                              - `EPHEMERAL("ephemeral")`

                            - `ttl: Optional<Ttl>`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `TTL_5M("5m")`

                              - `TTL_1H("1h")`

                    - `type: JsonValue; "content"constant`

                      - `CONTENT("content")`

                  - `class BetaUrlPdfSource:`

                    - `type: JsonValue; "url"constant`

                      - `URL("url")`

                    - `url: String`

                  - `class BetaFileDocumentSource:`

                    - `fileId: String`

                    - `type: JsonValue; "file"constant`

                      - `FILE("file")`

                - `type: JsonValue; "document"constant`

                  - `DOCUMENT("document")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `citations: Optional<BetaCitationsConfigParam>`

                  - `enabled: Optional<Boolean>`

                - `context: Optional<String>`

                - `title: Optional<String>`

              - `type: JsonValue; "web_fetch_result"constant`

                - `WEB_FETCH_RESULT("web_fetch_result")`

              - `url: String`

                Fetched content URL

              - `retrievedAt: Optional<String>`

                ISO 8601 timestamp when the content was retrieved

          - `toolUseId: String`

          - `type: JsonValue; "web_fetch_tool_result"constant`

            - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaCodeExecutionToolResultBlockParam:`

          - `content: BetaCodeExecutionToolResultBlockParamContent`

            - `class BetaCodeExecutionToolResultErrorParam:`

              - `errorCode: BetaCodeExecutionToolResultErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `type: JsonValue; "code_execution_tool_result_error"constant`

                - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

            - `class BetaCodeExecutionResultBlockParam:`

              - `content: List<BetaCodeExecutionOutputBlockParam>`

                - `fileId: String`

                - `type: JsonValue; "code_execution_output"constant`

                  - `CODE_EXECUTION_OUTPUT("code_execution_output")`

              - `returnCode: Long`

              - `stderr: String`

              - `stdout: String`

              - `type: JsonValue; "code_execution_result"constant`

                - `CODE_EXECUTION_RESULT("code_execution_result")`

          - `toolUseId: String`

          - `type: JsonValue; "code_execution_tool_result"constant`

            - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaBashCodeExecutionToolResultBlockParam:`

          - `content: Content`

            - `class BetaBashCodeExecutionToolResultErrorParam:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

              - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

                - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

            - `class BetaBashCodeExecutionResultBlockParam:`

              - `content: List<BetaBashCodeExecutionOutputBlockParam>`

                - `fileId: String`

                - `type: JsonValue; "bash_code_execution_output"constant`

                  - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

              - `returnCode: Long`

              - `stderr: String`

              - `stdout: String`

              - `type: JsonValue; "bash_code_execution_result"constant`

                - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

          - `toolUseId: String`

          - `type: JsonValue; "bash_code_execution_tool_result"constant`

            - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaTextEditorCodeExecutionToolResultBlockParam:`

          - `content: Content`

            - `class BetaTextEditorCodeExecutionToolResultErrorParam:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `FILE_NOT_FOUND("file_not_found")`

              - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

              - `errorMessage: Optional<String>`

            - `class BetaTextEditorCodeExecutionViewResultBlockParam:`

              - `content: String`

              - `fileType: FileType`

                - `TEXT("text")`

                - `IMAGE("image")`

                - `PDF("pdf")`

              - `type: JsonValue; "text_editor_code_execution_view_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

              - `numLines: Optional<Long>`

              - `startLine: Optional<Long>`

              - `totalLines: Optional<Long>`

            - `class BetaTextEditorCodeExecutionCreateResultBlockParam:`

              - `isFileUpdate: Boolean`

              - `type: JsonValue; "text_editor_code_execution_create_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

            - `class BetaTextEditorCodeExecutionStrReplaceResultBlockParam:`

              - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

              - `lines: Optional<List<String>>`

              - `newLines: Optional<Long>`

              - `newStart: Optional<Long>`

              - `oldLines: Optional<Long>`

              - `oldStart: Optional<Long>`

          - `toolUseId: String`

          - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaToolSearchToolResultBlockParam:`

          - `content: Content`

            - `class BetaToolSearchToolResultErrorParam:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `type: JsonValue; "tool_search_tool_result_error"constant`

                - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

            - `class BetaToolSearchToolSearchResultBlockParam:`

              - `toolReferences: List<BetaToolReferenceBlockParam>`

                - `toolName: String`

                - `type: JsonValue; "tool_reference"constant`

                  - `TOOL_REFERENCE("tool_reference")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

              - `type: JsonValue; "tool_search_tool_search_result"constant`

                - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

          - `toolUseId: String`

          - `type: JsonValue; "tool_search_tool_result"constant`

            - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaMcpToolUseBlockParam:`

          - `id: String`

          - `input: Input`

          - `name: String`

          - `serverName: String`

            The name of the MCP server

          - `type: JsonValue; "mcp_tool_use"constant`

            - `MCP_TOOL_USE("mcp_tool_use")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaRequestMcpToolResultBlockParam:`

          - `toolUseId: String`

          - `type: JsonValue; "mcp_tool_result"constant`

            - `MCP_TOOL_RESULT("mcp_tool_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `content: Optional<Content>`

            - `String`

            - `List<BetaTextBlockParam>`

              - `text: String`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<List<BetaTextCitationParam>>`

                - `class BetaCitationCharLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endCharIndex: Long`

                  - `startCharIndex: Long`

                  - `type: JsonValue; "char_location"constant`

                    - `CHAR_LOCATION("char_location")`

                - `class BetaCitationPageLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endPageNumber: Long`

                  - `startPageNumber: Long`

                  - `type: JsonValue; "page_location"constant`

                    - `PAGE_LOCATION("page_location")`

                - `class BetaCitationContentBlockLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endBlockIndex: Long`

                  - `startBlockIndex: Long`

                  - `type: JsonValue; "content_block_location"constant`

                    - `CONTENT_BLOCK_LOCATION("content_block_location")`

                - `class BetaCitationWebSearchResultLocationParam:`

                  - `citedText: String`

                  - `encryptedIndex: String`

                  - `title: Optional<String>`

                  - `type: JsonValue; "web_search_result_location"constant`

                    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                  - `url: String`

                - `class BetaCitationSearchResultLocationParam:`

                  - `citedText: String`

                  - `endBlockIndex: Long`

                  - `searchResultIndex: Long`

                  - `source: String`

                  - `startBlockIndex: Long`

                  - `title: Optional<String>`

                  - `type: JsonValue; "search_result_location"constant`

                    - `SEARCH_RESULT_LOCATION("search_result_location")`

          - `isError: Optional<Boolean>`

        - `class BetaContainerUploadBlockParam:`

          A content block that represents a file to be uploaded to the container
          Files uploaded via this block will be available in the container's input directory.

          - `fileId: String`

          - `type: JsonValue; "container_upload"constant`

            - `CONTAINER_UPLOAD("container_upload")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

    - `role: Role`

      - `USER("user")`

      - `ASSISTANT("assistant")`

  - `model: Model`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

  - `contextManagement: Optional<BetaContextManagementConfig>`

    Context management configuration.

    This allows you to control how Claude manages context across multiple requests, such as whether to clear function results or not.

  - `mcpServers: Optional<List<BetaRequestMcpServerUrlDefinition>>`

    MCP servers to be utilized in this request

    - `name: String`

    - `type: JsonValue; "url"constant`

      - `URL("url")`

    - `url: String`

    - `authorizationToken: Optional<String>`

    - `toolConfiguration: Optional<BetaRequestMcpServerToolConfiguration>`

      - `allowedTools: Optional<List<String>>`

      - `enabled: Optional<Boolean>`

  - `outputConfig: Optional<BetaOutputConfig>`

    Configuration options for the model's output. Controls aspects like how much effort the model puts into its response.

  - `outputFormat: Optional<BetaJsonOutputFormat>`

    A schema to specify Claude's output format in responses.

  - `system: Optional<System>`

    System prompt.

    A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

    - `String`

    - `List<BetaTextBlockParam>`

      - `text: String`

      - `type: JsonValue; "text"constant`

        - `TEXT("text")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `citations: Optional<List<BetaTextCitationParam>>`

        - `class BetaCitationCharLocationParam:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endCharIndex: Long`

          - `startCharIndex: Long`

          - `type: JsonValue; "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class BetaCitationPageLocationParam:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endPageNumber: Long`

          - `startPageNumber: Long`

          - `type: JsonValue; "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class BetaCitationContentBlockLocationParam:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endBlockIndex: Long`

          - `startBlockIndex: Long`

          - `type: JsonValue; "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class BetaCitationWebSearchResultLocationParam:`

          - `citedText: String`

          - `encryptedIndex: String`

          - `title: Optional<String>`

          - `type: JsonValue; "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `url: String`

        - `class BetaCitationSearchResultLocationParam:`

          - `citedText: String`

          - `endBlockIndex: Long`

          - `searchResultIndex: Long`

          - `source: String`

          - `startBlockIndex: Long`

          - `title: Optional<String>`

          - `type: JsonValue; "search_result_location"constant`

            - `SEARCH_RESULT_LOCATION("search_result_location")`

  - `thinking: Optional<BetaThinkingConfigParam>`

    Configuration for enabling Claude's extended thinking.

    When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `toolChoice: Optional<BetaToolChoice>`

    How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `tools: Optional<List<Tool>>`

    Definitions of tools that the model may use.

    If you include `tools` in your API request, the model may return `tool_use` content blocks that represent the model's use of those tools. You can then run those tools using the tool input generated by the model and then optionally return results back to the model using `tool_result` content blocks.

    There are two types of tools: **client tools** and **server tools**. The behavior described below applies to client tools. For [server tools](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview#server-tools), see their individual documentation as each has its own behavior (e.g., the [web search tool](https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-search-tool)).

    Each tool definition includes:

    * `name`: Name of the tool.
    * `description`: Optional, but strongly-recommended description of the tool.
    * `input_schema`: [JSON schema](https://json-schema.org/draft/2020-12) for the tool `input` shape that the model will produce in `tool_use` output content blocks.

    For example, if you defined `tools` as:

    ```json
    [
      {
        "name": "get_stock_price",
        "description": "Get the current stock price for a given ticker symbol.",
        "input_schema": {
          "type": "object",
          "properties": {
            "ticker": {
              "type": "string",
              "description": "The stock ticker symbol, e.g. AAPL for Apple Inc."
            }
          },
          "required": ["ticker"]
        }
      }
    ]
    ```

    And then asked the model "What's the S&P 500 at today?", the model might produce `tool_use` content blocks in the response like this:

    ```json
    [
      {
        "type": "tool_use",
        "id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
        "name": "get_stock_price",
        "input": { "ticker": "^GSPC" }
      }
    ]
    ```

    You might then run your `get_stock_price` tool with `{"ticker": "^GSPC"}` as an input, and return the following back to the model in a subsequent `user` message:

    ```json
    [
      {
        "type": "tool_result",
        "tool_use_id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
        "content": "259.75 USD"
      }
    ]
    ```

    Tools can be used for workflows that include running client-side tools and functions, or more generally whenever you want the model to produce a particular JSON structure of output.

    See our [guide](https://docs.claude.com/en/docs/tool-use) for more details.

    - `class BetaTool:`

      - `inputSchema: InputSchema`

        [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

        This defines the shape of the `input` that your tool accepts and that the model will produce.

        - `type: JsonValue; "object"constant`

          - `OBJECT("object")`

        - `properties: Optional<Properties>`

        - `required: Optional<List<String>>`

      - `name: String`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `description: Optional<String>`

        Description of what this tool does.

        Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

      - `type: Optional<Type>`

        - `CUSTOM("custom")`

    - `class BetaToolBash20241022:`

      - `name: JsonValue; "bash"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `BASH("bash")`

      - `type: JsonValue; "bash_20241022"constant`

        - `BASH_20241022("bash_20241022")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolBash20250124:`

      - `name: JsonValue; "bash"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `BASH("bash")`

      - `type: JsonValue; "bash_20250124"constant`

        - `BASH_20250124("bash_20250124")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaCodeExecutionTool20250522:`

      - `name: JsonValue; "code_execution"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `CODE_EXECUTION("code_execution")`

      - `type: JsonValue; "code_execution_20250522"constant`

        - `CODE_EXECUTION_20250522("code_execution_20250522")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `strict: Optional<Boolean>`

    - `class BetaCodeExecutionTool20250825:`

      - `name: JsonValue; "code_execution"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `CODE_EXECUTION("code_execution")`

      - `type: JsonValue; "code_execution_20250825"constant`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `strict: Optional<Boolean>`

    - `class BetaToolComputerUse20241022:`

      - `displayHeightPx: Long`

        The height of the display in pixels.

      - `displayWidthPx: Long`

        The width of the display in pixels.

      - `name: JsonValue; "computer"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `COMPUTER("computer")`

      - `type: JsonValue; "computer_20241022"constant`

        - `COMPUTER_20241022("computer_20241022")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `displayNumber: Optional<Long>`

        The X11 display number (e.g. 0, 1) for the display.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaMemoryTool20250818:`

      - `name: JsonValue; "memory"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `MEMORY("memory")`

      - `type: JsonValue; "memory_20250818"constant`

        - `MEMORY_20250818("memory_20250818")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolComputerUse20250124:`

      - `displayHeightPx: Long`

        The height of the display in pixels.

      - `displayWidthPx: Long`

        The width of the display in pixels.

      - `name: JsonValue; "computer"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `COMPUTER("computer")`

      - `type: JsonValue; "computer_20250124"constant`

        - `COMPUTER_20250124("computer_20250124")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `displayNumber: Optional<Long>`

        The X11 display number (e.g. 0, 1) for the display.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolTextEditor20241022:`

      - `name: JsonValue; "str_replace_editor"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_EDITOR("str_replace_editor")`

      - `type: JsonValue; "text_editor_20241022"constant`

        - `TEXT_EDITOR_20241022("text_editor_20241022")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolComputerUse20251124:`

      - `displayHeightPx: Long`

        The height of the display in pixels.

      - `displayWidthPx: Long`

        The width of the display in pixels.

      - `name: JsonValue; "computer"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `COMPUTER("computer")`

      - `type: JsonValue; "computer_20251124"constant`

        - `COMPUTER_20251124("computer_20251124")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `displayNumber: Optional<Long>`

        The X11 display number (e.g. 0, 1) for the display.

      - `enableZoom: Optional<Boolean>`

        Whether to enable an action to take a zoomed-in screenshot of the screen.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolTextEditor20250124:`

      - `name: JsonValue; "str_replace_editor"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_EDITOR("str_replace_editor")`

      - `type: JsonValue; "text_editor_20250124"constant`

        - `TEXT_EDITOR_20250124("text_editor_20250124")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolTextEditor20250429:`

      - `name: JsonValue; "str_replace_based_edit_tool"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

      - `type: JsonValue; "text_editor_20250429"constant`

        - `TEXT_EDITOR_20250429("text_editor_20250429")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `strict: Optional<Boolean>`

    - `class BetaToolTextEditor20250728:`

      - `name: JsonValue; "str_replace_based_edit_tool"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

      - `type: JsonValue; "text_editor_20250728"constant`

        - `TEXT_EDITOR_20250728("text_editor_20250728")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `inputExamples: Optional<List<InputExample>>`

      - `maxCharacters: Optional<Long>`

        Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

      - `strict: Optional<Boolean>`

    - `class BetaWebSearchTool20250305:`

      - `name: JsonValue; "web_search"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `WEB_SEARCH("web_search")`

      - `type: JsonValue; "web_search_20250305"constant`

        - `WEB_SEARCH_20250305("web_search_20250305")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `allowedDomains: Optional<List<String>>`

        If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

      - `blockedDomains: Optional<List<String>>`

        If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `maxUses: Optional<Long>`

        Maximum number of times the tool can be used in the API request.

      - `strict: Optional<Boolean>`

      - `userLocation: Optional<UserLocation>`

        Parameters for the user's location. Used to provide more relevant search results.

        - `type: JsonValue; "approximate"constant`

          - `APPROXIMATE("approximate")`

        - `city: Optional<String>`

          The city of the user.

        - `country: Optional<String>`

          The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

        - `region: Optional<String>`

          The region of the user.

        - `timezone: Optional<String>`

          The [IANA timezone](https://nodatime.org/TimeZones) of the user.

    - `class BetaWebFetchTool20250910:`

      - `name: JsonValue; "web_fetch"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `WEB_FETCH("web_fetch")`

      - `type: JsonValue; "web_fetch_20250910"constant`

        - `WEB_FETCH_20250910("web_fetch_20250910")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `allowedDomains: Optional<List<String>>`

        List of domains to allow fetching from

      - `blockedDomains: Optional<List<String>>`

        List of domains to block fetching from

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `citations: Optional<BetaCitationsConfigParam>`

        Citations configuration for fetched documents. Citations are disabled by default.

        - `enabled: Optional<Boolean>`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `maxContentTokens: Optional<Long>`

        Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

      - `maxUses: Optional<Long>`

        Maximum number of times the tool can be used in the API request.

      - `strict: Optional<Boolean>`

    - `class BetaToolSearchToolBm25_20251119:`

      - `name: JsonValue; "tool_search_tool_bm25"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

      - `type: Type`

        - `TOOL_SEARCH_TOOL_BM25_20251119("tool_search_tool_bm25_20251119")`

        - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `strict: Optional<Boolean>`

    - `class BetaToolSearchToolRegex20251119:`

      - `name: JsonValue; "tool_search_tool_regex"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

      - `type: Type`

        - `TOOL_SEARCH_TOOL_REGEX_20251119("tool_search_tool_regex_20251119")`

        - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

      - `allowedCallers: Optional<List<AllowedCaller>>`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `deferLoading: Optional<Boolean>`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `strict: Optional<Boolean>`

    - `class BetaMcpToolset:`

      Configuration for a group of tools from an MCP server.

      Allows configuring enabled status and defer_loading for all tools
      from an MCP server, with optional per-tool overrides.

      - `mcpServerName: String`

        Name of the MCP server to configure tools for

      - `type: JsonValue; "mcp_toolset"constant`

        - `MCP_TOOLSET("mcp_toolset")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `configs: Optional<Configs>`

        Configuration overrides for specific tools, keyed by tool name

        - `deferLoading: Optional<Boolean>`

        - `enabled: Optional<Boolean>`

      - `defaultConfig: Optional<BetaMcpToolDefaultConfig>`

        Default configuration applied to all tools from this server

        - `deferLoading: Optional<Boolean>`

        - `enabled: Optional<Boolean>`

### Returns

- `class BetaMessageTokensCount:`

  - `contextManagement: Optional<BetaCountTokensContextManagementResponse>`

    Information about context management applied to the message.

    - `originalInputTokens: Long`

      The original token count before context management was applied

  - `inputTokens: Long`

    The total number of tokens across the provided list of messages, system prompt, and tools.

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.messages.BetaMessageTokensCount
import com.anthropic.models.beta.messages.MessageCountTokensParams
import com.anthropic.models.messages.Model

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val params: MessageCountTokensParams = MessageCountTokensParams.builder()
        .addUserMessage("Hello, world")
        .model(Model.CLAUDE_OPUS_4_5_20251101)
        .build()
    val betaMessageTokensCount: BetaMessageTokensCount = client.beta().messages().countTokens(params)
}
```

## Domain Types

### Beta All Thinking Turns

- `class BetaAllThinkingTurns:`

  - `type: JsonValue; "all"constant`

    - `ALL("all")`

### Beta Base64 Image Source

- `class BetaBase64ImageSource:`

  - `data: String`

  - `mediaType: MediaType`

    - `IMAGE_JPEG("image/jpeg")`

    - `IMAGE_PNG("image/png")`

    - `IMAGE_GIF("image/gif")`

    - `IMAGE_WEBP("image/webp")`

  - `type: JsonValue; "base64"constant`

    - `BASE64("base64")`

### Beta Base64 PDF Source

- `class BetaBase64PdfSource:`

  - `data: String`

  - `mediaType: JsonValue; "application/pdf"constant`

    - `APPLICATION_PDF("application/pdf")`

  - `type: JsonValue; "base64"constant`

    - `BASE64("base64")`

### Beta Bash Code Execution Output Block

- `class BetaBashCodeExecutionOutputBlock:`

  - `fileId: String`

  - `type: JsonValue; "bash_code_execution_output"constant`

    - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

### Beta Bash Code Execution Output Block Param

- `class BetaBashCodeExecutionOutputBlockParam:`

  - `fileId: String`

  - `type: JsonValue; "bash_code_execution_output"constant`

    - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

### Beta Bash Code Execution Result Block

- `class BetaBashCodeExecutionResultBlock:`

  - `content: List<BetaBashCodeExecutionOutputBlock>`

    - `fileId: String`

    - `type: JsonValue; "bash_code_execution_output"constant`

      - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

  - `returnCode: Long`

  - `stderr: String`

  - `stdout: String`

  - `type: JsonValue; "bash_code_execution_result"constant`

    - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

### Beta Bash Code Execution Result Block Param

- `class BetaBashCodeExecutionResultBlockParam:`

  - `content: List<BetaBashCodeExecutionOutputBlockParam>`

    - `fileId: String`

    - `type: JsonValue; "bash_code_execution_output"constant`

      - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

  - `returnCode: Long`

  - `stderr: String`

  - `stdout: String`

  - `type: JsonValue; "bash_code_execution_result"constant`

    - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

### Beta Bash Code Execution Tool Result Block

- `class BetaBashCodeExecutionToolResultBlock:`

  - `content: Content`

    - `class BetaBashCodeExecutionToolResultError:`

      - `errorCode: ErrorCode`

        - `INVALID_TOOL_INPUT("invalid_tool_input")`

        - `UNAVAILABLE("unavailable")`

        - `TOO_MANY_REQUESTS("too_many_requests")`

        - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

        - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

      - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

        - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

    - `class BetaBashCodeExecutionResultBlock:`

      - `content: List<BetaBashCodeExecutionOutputBlock>`

        - `fileId: String`

        - `type: JsonValue; "bash_code_execution_output"constant`

          - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

      - `returnCode: Long`

      - `stderr: String`

      - `stdout: String`

      - `type: JsonValue; "bash_code_execution_result"constant`

        - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

  - `toolUseId: String`

  - `type: JsonValue; "bash_code_execution_tool_result"constant`

    - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

### Beta Bash Code Execution Tool Result Block Param

- `class BetaBashCodeExecutionToolResultBlockParam:`

  - `content: Content`

    - `class BetaBashCodeExecutionToolResultErrorParam:`

      - `errorCode: ErrorCode`

        - `INVALID_TOOL_INPUT("invalid_tool_input")`

        - `UNAVAILABLE("unavailable")`

        - `TOO_MANY_REQUESTS("too_many_requests")`

        - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

        - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

      - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

        - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

    - `class BetaBashCodeExecutionResultBlockParam:`

      - `content: List<BetaBashCodeExecutionOutputBlockParam>`

        - `fileId: String`

        - `type: JsonValue; "bash_code_execution_output"constant`

          - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

      - `returnCode: Long`

      - `stderr: String`

      - `stdout: String`

      - `type: JsonValue; "bash_code_execution_result"constant`

        - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

  - `toolUseId: String`

  - `type: JsonValue; "bash_code_execution_tool_result"constant`

    - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

### Beta Bash Code Execution Tool Result Error

- `class BetaBashCodeExecutionToolResultError:`

  - `errorCode: ErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `UNAVAILABLE("unavailable")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

    - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

  - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

    - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

### Beta Bash Code Execution Tool Result Error Param

- `class BetaBashCodeExecutionToolResultErrorParam:`

  - `errorCode: ErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `UNAVAILABLE("unavailable")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

    - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

  - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

    - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

### Beta Cache Control Ephemeral

- `class BetaCacheControlEphemeral:`

  - `type: JsonValue; "ephemeral"constant`

    - `EPHEMERAL("ephemeral")`

  - `ttl: Optional<Ttl>`

    The time-to-live for the cache control breakpoint.

    This may be one the following values:

    - `5m`: 5 minutes
    - `1h`: 1 hour

    Defaults to `5m`.

    - `TTL_5M("5m")`

    - `TTL_1H("1h")`

### Beta Cache Creation

- `class BetaCacheCreation:`

  - `ephemeral1hInputTokens: Long`

    The number of input tokens used to create the 1 hour cache entry.

  - `ephemeral5mInputTokens: Long`

    The number of input tokens used to create the 5 minute cache entry.

### Beta Citation Char Location

- `class BetaCitationCharLocation:`

  - `citedText: String`

  - `documentIndex: Long`

  - `documentTitle: Optional<String>`

  - `endCharIndex: Long`

  - `fileId: Optional<String>`

  - `startCharIndex: Long`

  - `type: JsonValue; "char_location"constant`

    - `CHAR_LOCATION("char_location")`

### Beta Citation Char Location Param

- `class BetaCitationCharLocationParam:`

  - `citedText: String`

  - `documentIndex: Long`

  - `documentTitle: Optional<String>`

  - `endCharIndex: Long`

  - `startCharIndex: Long`

  - `type: JsonValue; "char_location"constant`

    - `CHAR_LOCATION("char_location")`

### Beta Citation Config

- `class BetaCitationConfig:`

  - `enabled: Boolean`

### Beta Citation Content Block Location

- `class BetaCitationContentBlockLocation:`

  - `citedText: String`

  - `documentIndex: Long`

  - `documentTitle: Optional<String>`

  - `endBlockIndex: Long`

  - `fileId: Optional<String>`

  - `startBlockIndex: Long`

  - `type: JsonValue; "content_block_location"constant`

    - `CONTENT_BLOCK_LOCATION("content_block_location")`

### Beta Citation Content Block Location Param

- `class BetaCitationContentBlockLocationParam:`

  - `citedText: String`

  - `documentIndex: Long`

  - `documentTitle: Optional<String>`

  - `endBlockIndex: Long`

  - `startBlockIndex: Long`

  - `type: JsonValue; "content_block_location"constant`

    - `CONTENT_BLOCK_LOCATION("content_block_location")`

### Beta Citation Page Location

- `class BetaCitationPageLocation:`

  - `citedText: String`

  - `documentIndex: Long`

  - `documentTitle: Optional<String>`

  - `endPageNumber: Long`

  - `fileId: Optional<String>`

  - `startPageNumber: Long`

  - `type: JsonValue; "page_location"constant`

    - `PAGE_LOCATION("page_location")`

### Beta Citation Page Location Param

- `class BetaCitationPageLocationParam:`

  - `citedText: String`

  - `documentIndex: Long`

  - `documentTitle: Optional<String>`

  - `endPageNumber: Long`

  - `startPageNumber: Long`

  - `type: JsonValue; "page_location"constant`

    - `PAGE_LOCATION("page_location")`

### Beta Citation Search Result Location

- `class BetaCitationSearchResultLocation:`

  - `citedText: String`

  - `endBlockIndex: Long`

  - `searchResultIndex: Long`

  - `source: String`

  - `startBlockIndex: Long`

  - `title: Optional<String>`

  - `type: JsonValue; "search_result_location"constant`

    - `SEARCH_RESULT_LOCATION("search_result_location")`

### Beta Citation Search Result Location Param

- `class BetaCitationSearchResultLocationParam:`

  - `citedText: String`

  - `endBlockIndex: Long`

  - `searchResultIndex: Long`

  - `source: String`

  - `startBlockIndex: Long`

  - `title: Optional<String>`

  - `type: JsonValue; "search_result_location"constant`

    - `SEARCH_RESULT_LOCATION("search_result_location")`

### Beta Citation Web Search Result Location Param

- `class BetaCitationWebSearchResultLocationParam:`

  - `citedText: String`

  - `encryptedIndex: String`

  - `title: Optional<String>`

  - `type: JsonValue; "web_search_result_location"constant`

    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

  - `url: String`

### Beta Citations Config Param

- `class BetaCitationsConfigParam:`

  - `enabled: Optional<Boolean>`

### Beta Citations Delta

- `class BetaCitationsDelta:`

  - `citation: Citation`

    - `class BetaCitationCharLocation:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endCharIndex: Long`

      - `fileId: Optional<String>`

      - `startCharIndex: Long`

      - `type: JsonValue; "char_location"constant`

        - `CHAR_LOCATION("char_location")`

    - `class BetaCitationPageLocation:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endPageNumber: Long`

      - `fileId: Optional<String>`

      - `startPageNumber: Long`

      - `type: JsonValue; "page_location"constant`

        - `PAGE_LOCATION("page_location")`

    - `class BetaCitationContentBlockLocation:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endBlockIndex: Long`

      - `fileId: Optional<String>`

      - `startBlockIndex: Long`

      - `type: JsonValue; "content_block_location"constant`

        - `CONTENT_BLOCK_LOCATION("content_block_location")`

    - `class BetaCitationsWebSearchResultLocation:`

      - `citedText: String`

      - `encryptedIndex: String`

      - `title: Optional<String>`

      - `type: JsonValue; "web_search_result_location"constant`

        - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

      - `url: String`

    - `class BetaCitationSearchResultLocation:`

      - `citedText: String`

      - `endBlockIndex: Long`

      - `searchResultIndex: Long`

      - `source: String`

      - `startBlockIndex: Long`

      - `title: Optional<String>`

      - `type: JsonValue; "search_result_location"constant`

        - `SEARCH_RESULT_LOCATION("search_result_location")`

  - `type: JsonValue; "citations_delta"constant`

    - `CITATIONS_DELTA("citations_delta")`

### Beta Citations Web Search Result Location

- `class BetaCitationsWebSearchResultLocation:`

  - `citedText: String`

  - `encryptedIndex: String`

  - `title: Optional<String>`

  - `type: JsonValue; "web_search_result_location"constant`

    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

  - `url: String`

### Beta Clear Thinking 20251015 Edit

- `class BetaClearThinking20251015Edit:`

  - `type: JsonValue; "clear_thinking_20251015"constant`

    - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

  - `keep: Optional<Keep>`

    Number of most recent assistant turns to keep thinking blocks for. Older turns will have their thinking blocks removed.

    - `class BetaThinkingTurns:`

      - `type: JsonValue; "thinking_turns"constant`

        - `THINKING_TURNS("thinking_turns")`

      - `value: Long`

    - `class BetaAllThinkingTurns:`

      - `type: JsonValue; "all"constant`

        - `ALL("all")`

    - `JsonValue;`

      - `ALL("all")`

### Beta Clear Thinking 20251015 Edit Response

- `class BetaClearThinking20251015EditResponse:`

  - `clearedInputTokens: Long`

    Number of input tokens cleared by this edit.

  - `clearedThinkingTurns: Long`

    Number of thinking turns that were cleared.

  - `type: JsonValue; "clear_thinking_20251015"constant`

    The type of context management edit applied.

    - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

### Beta Clear Tool Uses 20250919 Edit

- `class BetaClearToolUses20250919Edit:`

  - `type: JsonValue; "clear_tool_uses_20250919"constant`

    - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

  - `clearAtLeast: Optional<BetaInputTokensClearAtLeast>`

    Minimum number of tokens that must be cleared when triggered. Context will only be modified if at least this many tokens can be removed.

    - `type: JsonValue; "input_tokens"constant`

      - `INPUT_TOKENS("input_tokens")`

    - `value: Long`

  - `clearToolInputs: Optional<ClearToolInputs>`

    Whether to clear all tool inputs (bool) or specific tool inputs to clear (list)

    - `Boolean`

    - `List<String>`

  - `excludeTools: Optional<List<String>>`

    Tool names whose uses are preserved from clearing

  - `keep: Optional<BetaToolUsesKeep>`

    Number of tool uses to retain in the conversation

    - `type: JsonValue; "tool_uses"constant`

      - `TOOL_USES("tool_uses")`

    - `value: Long`

  - `trigger: Optional<Trigger>`

    Condition that triggers the context management strategy

    - `class BetaInputTokensTrigger:`

      - `type: JsonValue; "input_tokens"constant`

        - `INPUT_TOKENS("input_tokens")`

      - `value: Long`

    - `class BetaToolUsesTrigger:`

      - `type: JsonValue; "tool_uses"constant`

        - `TOOL_USES("tool_uses")`

      - `value: Long`

### Beta Clear Tool Uses 20250919 Edit Response

- `class BetaClearToolUses20250919EditResponse:`

  - `clearedInputTokens: Long`

    Number of input tokens cleared by this edit.

  - `clearedToolUses: Long`

    Number of tool uses that were cleared.

  - `type: JsonValue; "clear_tool_uses_20250919"constant`

    The type of context management edit applied.

    - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

### Beta Code Execution Output Block

- `class BetaCodeExecutionOutputBlock:`

  - `fileId: String`

  - `type: JsonValue; "code_execution_output"constant`

    - `CODE_EXECUTION_OUTPUT("code_execution_output")`

### Beta Code Execution Output Block Param

- `class BetaCodeExecutionOutputBlockParam:`

  - `fileId: String`

  - `type: JsonValue; "code_execution_output"constant`

    - `CODE_EXECUTION_OUTPUT("code_execution_output")`

### Beta Code Execution Result Block

- `class BetaCodeExecutionResultBlock:`

  - `content: List<BetaCodeExecutionOutputBlock>`

    - `fileId: String`

    - `type: JsonValue; "code_execution_output"constant`

      - `CODE_EXECUTION_OUTPUT("code_execution_output")`

  - `returnCode: Long`

  - `stderr: String`

  - `stdout: String`

  - `type: JsonValue; "code_execution_result"constant`

    - `CODE_EXECUTION_RESULT("code_execution_result")`

### Beta Code Execution Result Block Param

- `class BetaCodeExecutionResultBlockParam:`

  - `content: List<BetaCodeExecutionOutputBlockParam>`

    - `fileId: String`

    - `type: JsonValue; "code_execution_output"constant`

      - `CODE_EXECUTION_OUTPUT("code_execution_output")`

  - `returnCode: Long`

  - `stderr: String`

  - `stdout: String`

  - `type: JsonValue; "code_execution_result"constant`

    - `CODE_EXECUTION_RESULT("code_execution_result")`

### Beta Code Execution Tool 20250522

- `class BetaCodeExecutionTool20250522:`

  - `name: JsonValue; "code_execution"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `CODE_EXECUTION("code_execution")`

  - `type: JsonValue; "code_execution_20250522"constant`

    - `CODE_EXECUTION_20250522("code_execution_20250522")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `strict: Optional<Boolean>`

### Beta Code Execution Tool 20250825

- `class BetaCodeExecutionTool20250825:`

  - `name: JsonValue; "code_execution"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `CODE_EXECUTION("code_execution")`

  - `type: JsonValue; "code_execution_20250825"constant`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `strict: Optional<Boolean>`

### Beta Code Execution Tool Result Block

- `class BetaCodeExecutionToolResultBlock:`

  - `content: BetaCodeExecutionToolResultBlockContent`

    - `class BetaCodeExecutionToolResultError:`

      - `errorCode: BetaCodeExecutionToolResultErrorCode`

        - `INVALID_TOOL_INPUT("invalid_tool_input")`

        - `UNAVAILABLE("unavailable")`

        - `TOO_MANY_REQUESTS("too_many_requests")`

        - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

      - `type: JsonValue; "code_execution_tool_result_error"constant`

        - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

    - `class BetaCodeExecutionResultBlock:`

      - `content: List<BetaCodeExecutionOutputBlock>`

        - `fileId: String`

        - `type: JsonValue; "code_execution_output"constant`

          - `CODE_EXECUTION_OUTPUT("code_execution_output")`

      - `returnCode: Long`

      - `stderr: String`

      - `stdout: String`

      - `type: JsonValue; "code_execution_result"constant`

        - `CODE_EXECUTION_RESULT("code_execution_result")`

  - `toolUseId: String`

  - `type: JsonValue; "code_execution_tool_result"constant`

    - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

### Beta Code Execution Tool Result Block Content

- `class BetaCodeExecutionToolResultBlockContent: A class that can be one of several variants.union`

  - `class BetaCodeExecutionToolResultError:`

    - `errorCode: BetaCodeExecutionToolResultErrorCode`

      - `INVALID_TOOL_INPUT("invalid_tool_input")`

      - `UNAVAILABLE("unavailable")`

      - `TOO_MANY_REQUESTS("too_many_requests")`

      - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

    - `type: JsonValue; "code_execution_tool_result_error"constant`

      - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

  - `class BetaCodeExecutionResultBlock:`

    - `content: List<BetaCodeExecutionOutputBlock>`

      - `fileId: String`

      - `type: JsonValue; "code_execution_output"constant`

        - `CODE_EXECUTION_OUTPUT("code_execution_output")`

    - `returnCode: Long`

    - `stderr: String`

    - `stdout: String`

    - `type: JsonValue; "code_execution_result"constant`

      - `CODE_EXECUTION_RESULT("code_execution_result")`

### Beta Code Execution Tool Result Block Param

- `class BetaCodeExecutionToolResultBlockParam:`

  - `content: BetaCodeExecutionToolResultBlockParamContent`

    - `class BetaCodeExecutionToolResultErrorParam:`

      - `errorCode: BetaCodeExecutionToolResultErrorCode`

        - `INVALID_TOOL_INPUT("invalid_tool_input")`

        - `UNAVAILABLE("unavailable")`

        - `TOO_MANY_REQUESTS("too_many_requests")`

        - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

      - `type: JsonValue; "code_execution_tool_result_error"constant`

        - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

    - `class BetaCodeExecutionResultBlockParam:`

      - `content: List<BetaCodeExecutionOutputBlockParam>`

        - `fileId: String`

        - `type: JsonValue; "code_execution_output"constant`

          - `CODE_EXECUTION_OUTPUT("code_execution_output")`

      - `returnCode: Long`

      - `stderr: String`

      - `stdout: String`

      - `type: JsonValue; "code_execution_result"constant`

        - `CODE_EXECUTION_RESULT("code_execution_result")`

  - `toolUseId: String`

  - `type: JsonValue; "code_execution_tool_result"constant`

    - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

### Beta Code Execution Tool Result Block Param Content

- `class BetaCodeExecutionToolResultBlockParamContent: A class that can be one of several variants.union`

  - `class BetaCodeExecutionToolResultErrorParam:`

    - `errorCode: BetaCodeExecutionToolResultErrorCode`

      - `INVALID_TOOL_INPUT("invalid_tool_input")`

      - `UNAVAILABLE("unavailable")`

      - `TOO_MANY_REQUESTS("too_many_requests")`

      - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

    - `type: JsonValue; "code_execution_tool_result_error"constant`

      - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

  - `class BetaCodeExecutionResultBlockParam:`

    - `content: List<BetaCodeExecutionOutputBlockParam>`

      - `fileId: String`

      - `type: JsonValue; "code_execution_output"constant`

        - `CODE_EXECUTION_OUTPUT("code_execution_output")`

    - `returnCode: Long`

    - `stderr: String`

    - `stdout: String`

    - `type: JsonValue; "code_execution_result"constant`

      - `CODE_EXECUTION_RESULT("code_execution_result")`

### Beta Code Execution Tool Result Error

- `class BetaCodeExecutionToolResultError:`

  - `errorCode: BetaCodeExecutionToolResultErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `UNAVAILABLE("unavailable")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

  - `type: JsonValue; "code_execution_tool_result_error"constant`

    - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

### Beta Code Execution Tool Result Error Code

- `enum class BetaCodeExecutionToolResultErrorCode:`

  - `INVALID_TOOL_INPUT("invalid_tool_input")`

  - `UNAVAILABLE("unavailable")`

  - `TOO_MANY_REQUESTS("too_many_requests")`

  - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

### Beta Code Execution Tool Result Error Param

- `class BetaCodeExecutionToolResultErrorParam:`

  - `errorCode: BetaCodeExecutionToolResultErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `UNAVAILABLE("unavailable")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

  - `type: JsonValue; "code_execution_tool_result_error"constant`

    - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

### Beta Container

- `class BetaContainer:`

  Information about the container used in the request (for the code execution tool)

  - `id: String`

    Identifier for the container used in this request

  - `expiresAt: LocalDateTime`

    The time at which the container will expire.

  - `skills: Optional<List<BetaSkill>>`

    Skills loaded in the container

    - `skillId: String`

      Skill ID

    - `type: Type`

      Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

      - `ANTHROPIC("anthropic")`

      - `CUSTOM("custom")`

    - `version: String`

      Skill version or 'latest' for most recent version

### Beta Container Params

- `class BetaContainerParams:`

  Container parameters with skills to be loaded.

  - `id: Optional<String>`

    Container id

  - `skills: Optional<List<BetaSkillParams>>`

    List of skills to load in the container

    - `skillId: String`

      Skill ID

    - `type: Type`

      Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

      - `ANTHROPIC("anthropic")`

      - `CUSTOM("custom")`

    - `version: Optional<String>`

      Skill version or 'latest' for most recent version

### Beta Container Upload Block

- `class BetaContainerUploadBlock:`

  Response model for a file uploaded to the container.

  - `fileId: String`

  - `type: JsonValue; "container_upload"constant`

    - `CONTAINER_UPLOAD("container_upload")`

### Beta Container Upload Block Param

- `class BetaContainerUploadBlockParam:`

  A content block that represents a file to be uploaded to the container
  Files uploaded via this block will be available in the container's input directory.

  - `fileId: String`

  - `type: JsonValue; "container_upload"constant`

    - `CONTAINER_UPLOAD("container_upload")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

### Beta Content Block

- `class BetaContentBlock: A class that can be one of several variants.union`

  Response model for a file uploaded to the container.

  - `class BetaTextBlock:`

    - `citations: Optional<List<BetaTextCitation>>`

      Citations supporting the text block.

      The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

      - `class BetaCitationCharLocation:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endCharIndex: Long`

        - `fileId: Optional<String>`

        - `startCharIndex: Long`

        - `type: JsonValue; "char_location"constant`

          - `CHAR_LOCATION("char_location")`

      - `class BetaCitationPageLocation:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endPageNumber: Long`

        - `fileId: Optional<String>`

        - `startPageNumber: Long`

        - `type: JsonValue; "page_location"constant`

          - `PAGE_LOCATION("page_location")`

      - `class BetaCitationContentBlockLocation:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endBlockIndex: Long`

        - `fileId: Optional<String>`

        - `startBlockIndex: Long`

        - `type: JsonValue; "content_block_location"constant`

          - `CONTENT_BLOCK_LOCATION("content_block_location")`

      - `class BetaCitationsWebSearchResultLocation:`

        - `citedText: String`

        - `encryptedIndex: String`

        - `title: Optional<String>`

        - `type: JsonValue; "web_search_result_location"constant`

          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

        - `url: String`

      - `class BetaCitationSearchResultLocation:`

        - `citedText: String`

        - `endBlockIndex: Long`

        - `searchResultIndex: Long`

        - `source: String`

        - `startBlockIndex: Long`

        - `title: Optional<String>`

        - `type: JsonValue; "search_result_location"constant`

          - `SEARCH_RESULT_LOCATION("search_result_location")`

    - `text: String`

    - `type: JsonValue; "text"constant`

      - `TEXT("text")`

  - `class BetaThinkingBlock:`

    - `signature: String`

    - `thinking: String`

    - `type: JsonValue; "thinking"constant`

      - `THINKING("thinking")`

  - `class BetaRedactedThinkingBlock:`

    - `data: String`

    - `type: JsonValue; "redacted_thinking"constant`

      - `REDACTED_THINKING("redacted_thinking")`

  - `class BetaToolUseBlock:`

    - `id: String`

    - `input: Input`

    - `name: String`

    - `type: JsonValue; "tool_use"constant`

      - `TOOL_USE("tool_use")`

    - `caller: Optional<Caller>`

      Tool invocation directly from the model.

      - `class BetaDirectCaller:`

        Tool invocation directly from the model.

        - `type: JsonValue; "direct"constant`

          - `DIRECT("direct")`

      - `class BetaServerToolCaller:`

        Tool invocation generated by a server-side tool.

        - `toolId: String`

        - `type: JsonValue; "code_execution_20250825"constant`

          - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `class BetaServerToolUseBlock:`

    - `id: String`

    - `caller: Caller`

      Tool invocation directly from the model.

      - `class BetaDirectCaller:`

        Tool invocation directly from the model.

        - `type: JsonValue; "direct"constant`

          - `DIRECT("direct")`

      - `class BetaServerToolCaller:`

        Tool invocation generated by a server-side tool.

        - `toolId: String`

        - `type: JsonValue; "code_execution_20250825"constant`

          - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `input: Input`

    - `name: Name`

      - `WEB_SEARCH("web_search")`

      - `WEB_FETCH("web_fetch")`

      - `CODE_EXECUTION("code_execution")`

      - `BASH_CODE_EXECUTION("bash_code_execution")`

      - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

      - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

      - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

    - `type: JsonValue; "server_tool_use"constant`

      - `SERVER_TOOL_USE("server_tool_use")`

  - `class BetaWebSearchToolResultBlock:`

    - `content: BetaWebSearchToolResultBlockContent`

      - `class BetaWebSearchToolResultError:`

        - `errorCode: BetaWebSearchToolResultErrorCode`

          - `INVALID_TOOL_INPUT("invalid_tool_input")`

          - `UNAVAILABLE("unavailable")`

          - `MAX_USES_EXCEEDED("max_uses_exceeded")`

          - `TOO_MANY_REQUESTS("too_many_requests")`

          - `QUERY_TOO_LONG("query_too_long")`

        - `type: JsonValue; "web_search_tool_result_error"constant`

          - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

      - `List<BetaWebSearchResultBlock>`

        - `encryptedContent: String`

        - `pageAge: Optional<String>`

        - `title: String`

        - `type: JsonValue; "web_search_result"constant`

          - `WEB_SEARCH_RESULT("web_search_result")`

        - `url: String`

    - `toolUseId: String`

    - `type: JsonValue; "web_search_tool_result"constant`

      - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

  - `class BetaWebFetchToolResultBlock:`

    - `content: Content`

      - `class BetaWebFetchToolResultErrorBlock:`

        - `errorCode: BetaWebFetchToolResultErrorCode`

          - `INVALID_TOOL_INPUT("invalid_tool_input")`

          - `URL_TOO_LONG("url_too_long")`

          - `URL_NOT_ALLOWED("url_not_allowed")`

          - `URL_NOT_ACCESSIBLE("url_not_accessible")`

          - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

          - `TOO_MANY_REQUESTS("too_many_requests")`

          - `MAX_USES_EXCEEDED("max_uses_exceeded")`

          - `UNAVAILABLE("unavailable")`

        - `type: JsonValue; "web_fetch_tool_result_error"constant`

          - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

      - `class BetaWebFetchBlock:`

        - `content: BetaDocumentBlock`

          - `citations: Optional<BetaCitationConfig>`

            Citation configuration for the document

            - `enabled: Boolean`

          - `source: Source`

            - `class BetaBase64PdfSource:`

              - `data: String`

              - `mediaType: JsonValue; "application/pdf"constant`

                - `APPLICATION_PDF("application/pdf")`

              - `type: JsonValue; "base64"constant`

                - `BASE64("base64")`

            - `class BetaPlainTextSource:`

              - `data: String`

              - `mediaType: JsonValue; "text/plain"constant`

                - `TEXT_PLAIN("text/plain")`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

          - `title: Optional<String>`

            The title of the document

          - `type: JsonValue; "document"constant`

            - `DOCUMENT("document")`

        - `retrievedAt: Optional<String>`

          ISO 8601 timestamp when the content was retrieved

        - `type: JsonValue; "web_fetch_result"constant`

          - `WEB_FETCH_RESULT("web_fetch_result")`

        - `url: String`

          Fetched content URL

    - `toolUseId: String`

    - `type: JsonValue; "web_fetch_tool_result"constant`

      - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

  - `class BetaCodeExecutionToolResultBlock:`

    - `content: BetaCodeExecutionToolResultBlockContent`

      - `class BetaCodeExecutionToolResultError:`

        - `errorCode: BetaCodeExecutionToolResultErrorCode`

          - `INVALID_TOOL_INPUT("invalid_tool_input")`

          - `UNAVAILABLE("unavailable")`

          - `TOO_MANY_REQUESTS("too_many_requests")`

          - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

        - `type: JsonValue; "code_execution_tool_result_error"constant`

          - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

      - `class BetaCodeExecutionResultBlock:`

        - `content: List<BetaCodeExecutionOutputBlock>`

          - `fileId: String`

          - `type: JsonValue; "code_execution_output"constant`

            - `CODE_EXECUTION_OUTPUT("code_execution_output")`

        - `returnCode: Long`

        - `stderr: String`

        - `stdout: String`

        - `type: JsonValue; "code_execution_result"constant`

          - `CODE_EXECUTION_RESULT("code_execution_result")`

    - `toolUseId: String`

    - `type: JsonValue; "code_execution_tool_result"constant`

      - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

  - `class BetaBashCodeExecutionToolResultBlock:`

    - `content: Content`

      - `class BetaBashCodeExecutionToolResultError:`

        - `errorCode: ErrorCode`

          - `INVALID_TOOL_INPUT("invalid_tool_input")`

          - `UNAVAILABLE("unavailable")`

          - `TOO_MANY_REQUESTS("too_many_requests")`

          - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

          - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

        - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

          - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

      - `class BetaBashCodeExecutionResultBlock:`

        - `content: List<BetaBashCodeExecutionOutputBlock>`

          - `fileId: String`

          - `type: JsonValue; "bash_code_execution_output"constant`

            - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

        - `returnCode: Long`

        - `stderr: String`

        - `stdout: String`

        - `type: JsonValue; "bash_code_execution_result"constant`

          - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

    - `toolUseId: String`

    - `type: JsonValue; "bash_code_execution_tool_result"constant`

      - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

  - `class BetaTextEditorCodeExecutionToolResultBlock:`

    - `content: Content`

      - `class BetaTextEditorCodeExecutionToolResultError:`

        - `errorCode: ErrorCode`

          - `INVALID_TOOL_INPUT("invalid_tool_input")`

          - `UNAVAILABLE("unavailable")`

          - `TOO_MANY_REQUESTS("too_many_requests")`

          - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

          - `FILE_NOT_FOUND("file_not_found")`

        - `errorMessage: Optional<String>`

        - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

          - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

      - `class BetaTextEditorCodeExecutionViewResultBlock:`

        - `content: String`

        - `fileType: FileType`

          - `TEXT("text")`

          - `IMAGE("image")`

          - `PDF("pdf")`

        - `numLines: Optional<Long>`

        - `startLine: Optional<Long>`

        - `totalLines: Optional<Long>`

        - `type: JsonValue; "text_editor_code_execution_view_result"constant`

          - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

      - `class BetaTextEditorCodeExecutionCreateResultBlock:`

        - `isFileUpdate: Boolean`

        - `type: JsonValue; "text_editor_code_execution_create_result"constant`

          - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

      - `class BetaTextEditorCodeExecutionStrReplaceResultBlock:`

        - `lines: Optional<List<String>>`

        - `newLines: Optional<Long>`

        - `newStart: Optional<Long>`

        - `oldLines: Optional<Long>`

        - `oldStart: Optional<Long>`

        - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

          - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

    - `toolUseId: String`

    - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

      - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

  - `class BetaToolSearchToolResultBlock:`

    - `content: Content`

      - `class BetaToolSearchToolResultError:`

        - `errorCode: ErrorCode`

          - `INVALID_TOOL_INPUT("invalid_tool_input")`

          - `UNAVAILABLE("unavailable")`

          - `TOO_MANY_REQUESTS("too_many_requests")`

          - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

        - `errorMessage: Optional<String>`

        - `type: JsonValue; "tool_search_tool_result_error"constant`

          - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

      - `class BetaToolSearchToolSearchResultBlock:`

        - `toolReferences: List<BetaToolReferenceBlock>`

          - `toolName: String`

          - `type: JsonValue; "tool_reference"constant`

            - `TOOL_REFERENCE("tool_reference")`

        - `type: JsonValue; "tool_search_tool_search_result"constant`

          - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

    - `toolUseId: String`

    - `type: JsonValue; "tool_search_tool_result"constant`

      - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

  - `class BetaMcpToolUseBlock:`

    - `id: String`

    - `input: Input`

    - `name: String`

      The name of the MCP tool

    - `serverName: String`

      The name of the MCP server

    - `type: JsonValue; "mcp_tool_use"constant`

      - `MCP_TOOL_USE("mcp_tool_use")`

  - `class BetaMcpToolResultBlock:`

    - `content: Content`

      - `String`

      - `List<BetaTextBlock>`

        - `citations: Optional<List<BetaTextCitation>>`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `class BetaCitationCharLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endCharIndex: Long`

            - `fileId: Optional<String>`

            - `startCharIndex: Long`

            - `type: JsonValue; "char_location"constant`

              - `CHAR_LOCATION("char_location")`

          - `class BetaCitationPageLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endPageNumber: Long`

            - `fileId: Optional<String>`

            - `startPageNumber: Long`

            - `type: JsonValue; "page_location"constant`

              - `PAGE_LOCATION("page_location")`

          - `class BetaCitationContentBlockLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endBlockIndex: Long`

            - `fileId: Optional<String>`

            - `startBlockIndex: Long`

            - `type: JsonValue; "content_block_location"constant`

              - `CONTENT_BLOCK_LOCATION("content_block_location")`

          - `class BetaCitationsWebSearchResultLocation:`

            - `citedText: String`

            - `encryptedIndex: String`

            - `title: Optional<String>`

            - `type: JsonValue; "web_search_result_location"constant`

              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

            - `url: String`

          - `class BetaCitationSearchResultLocation:`

            - `citedText: String`

            - `endBlockIndex: Long`

            - `searchResultIndex: Long`

            - `source: String`

            - `startBlockIndex: Long`

            - `title: Optional<String>`

            - `type: JsonValue; "search_result_location"constant`

              - `SEARCH_RESULT_LOCATION("search_result_location")`

        - `text: String`

        - `type: JsonValue; "text"constant`

          - `TEXT("text")`

    - `isError: Boolean`

    - `toolUseId: String`

    - `type: JsonValue; "mcp_tool_result"constant`

      - `MCP_TOOL_RESULT("mcp_tool_result")`

  - `class BetaContainerUploadBlock:`

    Response model for a file uploaded to the container.

    - `fileId: String`

    - `type: JsonValue; "container_upload"constant`

      - `CONTAINER_UPLOAD("container_upload")`

### Beta Content Block Param

- `class BetaContentBlockParam: A class that can be one of several variants.union`

  Regular text content.

  - `class BetaTextBlockParam:`

    - `text: String`

    - `type: JsonValue; "text"constant`

      - `TEXT("text")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `citations: Optional<List<BetaTextCitationParam>>`

      - `class BetaCitationCharLocationParam:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endCharIndex: Long`

        - `startCharIndex: Long`

        - `type: JsonValue; "char_location"constant`

          - `CHAR_LOCATION("char_location")`

      - `class BetaCitationPageLocationParam:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endPageNumber: Long`

        - `startPageNumber: Long`

        - `type: JsonValue; "page_location"constant`

          - `PAGE_LOCATION("page_location")`

      - `class BetaCitationContentBlockLocationParam:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endBlockIndex: Long`

        - `startBlockIndex: Long`

        - `type: JsonValue; "content_block_location"constant`

          - `CONTENT_BLOCK_LOCATION("content_block_location")`

      - `class BetaCitationWebSearchResultLocationParam:`

        - `citedText: String`

        - `encryptedIndex: String`

        - `title: Optional<String>`

        - `type: JsonValue; "web_search_result_location"constant`

          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

        - `url: String`

      - `class BetaCitationSearchResultLocationParam:`

        - `citedText: String`

        - `endBlockIndex: Long`

        - `searchResultIndex: Long`

        - `source: String`

        - `startBlockIndex: Long`

        - `title: Optional<String>`

        - `type: JsonValue; "search_result_location"constant`

          - `SEARCH_RESULT_LOCATION("search_result_location")`

  - `class BetaImageBlockParam:`

    - `source: Source`

      - `class BetaBase64ImageSource:`

        - `data: String`

        - `mediaType: MediaType`

          - `IMAGE_JPEG("image/jpeg")`

          - `IMAGE_PNG("image/png")`

          - `IMAGE_GIF("image/gif")`

          - `IMAGE_WEBP("image/webp")`

        - `type: JsonValue; "base64"constant`

          - `BASE64("base64")`

      - `class BetaUrlImageSource:`

        - `type: JsonValue; "url"constant`

          - `URL("url")`

        - `url: String`

      - `class BetaFileImageSource:`

        - `fileId: String`

        - `type: JsonValue; "file"constant`

          - `FILE("file")`

    - `type: JsonValue; "image"constant`

      - `IMAGE("image")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

  - `class BetaRequestDocumentBlock:`

    - `source: Source`

      - `class BetaBase64PdfSource:`

        - `data: String`

        - `mediaType: JsonValue; "application/pdf"constant`

          - `APPLICATION_PDF("application/pdf")`

        - `type: JsonValue; "base64"constant`

          - `BASE64("base64")`

      - `class BetaPlainTextSource:`

        - `data: String`

        - `mediaType: JsonValue; "text/plain"constant`

          - `TEXT_PLAIN("text/plain")`

        - `type: JsonValue; "text"constant`

          - `TEXT("text")`

      - `class BetaContentBlockSource:`

        - `content: Content`

          - `String`

          - `List<BetaContentBlockSourceContent>`

            - `class BetaTextBlockParam:`

              - `text: String`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<List<BetaTextCitationParam>>`

                - `class BetaCitationCharLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endCharIndex: Long`

                  - `startCharIndex: Long`

                  - `type: JsonValue; "char_location"constant`

                    - `CHAR_LOCATION("char_location")`

                - `class BetaCitationPageLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endPageNumber: Long`

                  - `startPageNumber: Long`

                  - `type: JsonValue; "page_location"constant`

                    - `PAGE_LOCATION("page_location")`

                - `class BetaCitationContentBlockLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endBlockIndex: Long`

                  - `startBlockIndex: Long`

                  - `type: JsonValue; "content_block_location"constant`

                    - `CONTENT_BLOCK_LOCATION("content_block_location")`

                - `class BetaCitationWebSearchResultLocationParam:`

                  - `citedText: String`

                  - `encryptedIndex: String`

                  - `title: Optional<String>`

                  - `type: JsonValue; "web_search_result_location"constant`

                    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                  - `url: String`

                - `class BetaCitationSearchResultLocationParam:`

                  - `citedText: String`

                  - `endBlockIndex: Long`

                  - `searchResultIndex: Long`

                  - `source: String`

                  - `startBlockIndex: Long`

                  - `title: Optional<String>`

                  - `type: JsonValue; "search_result_location"constant`

                    - `SEARCH_RESULT_LOCATION("search_result_location")`

            - `class BetaImageBlockParam:`

              - `source: Source`

                - `class BetaBase64ImageSource:`

                  - `data: String`

                  - `mediaType: MediaType`

                    - `IMAGE_JPEG("image/jpeg")`

                    - `IMAGE_PNG("image/png")`

                    - `IMAGE_GIF("image/gif")`

                    - `IMAGE_WEBP("image/webp")`

                  - `type: JsonValue; "base64"constant`

                    - `BASE64("base64")`

                - `class BetaUrlImageSource:`

                  - `type: JsonValue; "url"constant`

                    - `URL("url")`

                  - `url: String`

                - `class BetaFileImageSource:`

                  - `fileId: String`

                  - `type: JsonValue; "file"constant`

                    - `FILE("file")`

              - `type: JsonValue; "image"constant`

                - `IMAGE("image")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

        - `type: JsonValue; "content"constant`

          - `CONTENT("content")`

      - `class BetaUrlPdfSource:`

        - `type: JsonValue; "url"constant`

          - `URL("url")`

        - `url: String`

      - `class BetaFileDocumentSource:`

        - `fileId: String`

        - `type: JsonValue; "file"constant`

          - `FILE("file")`

    - `type: JsonValue; "document"constant`

      - `DOCUMENT("document")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `citations: Optional<BetaCitationsConfigParam>`

      - `enabled: Optional<Boolean>`

    - `context: Optional<String>`

    - `title: Optional<String>`

  - `class BetaSearchResultBlockParam:`

    - `content: List<BetaTextBlockParam>`

      - `text: String`

      - `type: JsonValue; "text"constant`

        - `TEXT("text")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `citations: Optional<List<BetaTextCitationParam>>`

        - `class BetaCitationCharLocationParam:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endCharIndex: Long`

          - `startCharIndex: Long`

          - `type: JsonValue; "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class BetaCitationPageLocationParam:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endPageNumber: Long`

          - `startPageNumber: Long`

          - `type: JsonValue; "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class BetaCitationContentBlockLocationParam:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endBlockIndex: Long`

          - `startBlockIndex: Long`

          - `type: JsonValue; "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class BetaCitationWebSearchResultLocationParam:`

          - `citedText: String`

          - `encryptedIndex: String`

          - `title: Optional<String>`

          - `type: JsonValue; "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `url: String`

        - `class BetaCitationSearchResultLocationParam:`

          - `citedText: String`

          - `endBlockIndex: Long`

          - `searchResultIndex: Long`

          - `source: String`

          - `startBlockIndex: Long`

          - `title: Optional<String>`

          - `type: JsonValue; "search_result_location"constant`

            - `SEARCH_RESULT_LOCATION("search_result_location")`

    - `source: String`

    - `title: String`

    - `type: JsonValue; "search_result"constant`

      - `SEARCH_RESULT("search_result")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `citations: Optional<BetaCitationsConfigParam>`

      - `enabled: Optional<Boolean>`

  - `class BetaThinkingBlockParam:`

    - `signature: String`

    - `thinking: String`

    - `type: JsonValue; "thinking"constant`

      - `THINKING("thinking")`

  - `class BetaRedactedThinkingBlockParam:`

    - `data: String`

    - `type: JsonValue; "redacted_thinking"constant`

      - `REDACTED_THINKING("redacted_thinking")`

  - `class BetaToolUseBlockParam:`

    - `id: String`

    - `input: Input`

    - `name: String`

    - `type: JsonValue; "tool_use"constant`

      - `TOOL_USE("tool_use")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `caller: Optional<Caller>`

      Tool invocation directly from the model.

      - `class BetaDirectCaller:`

        Tool invocation directly from the model.

        - `type: JsonValue; "direct"constant`

          - `DIRECT("direct")`

      - `class BetaServerToolCaller:`

        Tool invocation generated by a server-side tool.

        - `toolId: String`

        - `type: JsonValue; "code_execution_20250825"constant`

          - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `class BetaToolResultBlockParam:`

    - `toolUseId: String`

    - `type: JsonValue; "tool_result"constant`

      - `TOOL_RESULT("tool_result")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `content: Optional<Content>`

      - `String`

      - `List<Block>`

        - `class BetaTextBlockParam:`

          - `text: String`

          - `type: JsonValue; "text"constant`

            - `TEXT("text")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<List<BetaTextCitationParam>>`

            - `class BetaCitationCharLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class BetaCitationPageLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class BetaCitationContentBlockLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class BetaCitationWebSearchResultLocationParam:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class BetaCitationSearchResultLocationParam:`

              - `citedText: String`

              - `endBlockIndex: Long`

              - `searchResultIndex: Long`

              - `source: String`

              - `startBlockIndex: Long`

              - `title: Optional<String>`

              - `type: JsonValue; "search_result_location"constant`

                - `SEARCH_RESULT_LOCATION("search_result_location")`

        - `class BetaImageBlockParam:`

          - `source: Source`

            - `class BetaBase64ImageSource:`

              - `data: String`

              - `mediaType: MediaType`

                - `IMAGE_JPEG("image/jpeg")`

                - `IMAGE_PNG("image/png")`

                - `IMAGE_GIF("image/gif")`

                - `IMAGE_WEBP("image/webp")`

              - `type: JsonValue; "base64"constant`

                - `BASE64("base64")`

            - `class BetaUrlImageSource:`

              - `type: JsonValue; "url"constant`

                - `URL("url")`

              - `url: String`

            - `class BetaFileImageSource:`

              - `fileId: String`

              - `type: JsonValue; "file"constant`

                - `FILE("file")`

          - `type: JsonValue; "image"constant`

            - `IMAGE("image")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaSearchResultBlockParam:`

          - `content: List<BetaTextBlockParam>`

            - `text: String`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

            - `cacheControl: Optional<BetaCacheControlEphemeral>`

              Create a cache control breakpoint at this content block.

              - `type: JsonValue; "ephemeral"constant`

                - `EPHEMERAL("ephemeral")`

              - `ttl: Optional<Ttl>`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `TTL_5M("5m")`

                - `TTL_1H("1h")`

            - `citations: Optional<List<BetaTextCitationParam>>`

              - `class BetaCitationCharLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endCharIndex: Long`

                - `startCharIndex: Long`

                - `type: JsonValue; "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class BetaCitationPageLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endPageNumber: Long`

                - `startPageNumber: Long`

                - `type: JsonValue; "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class BetaCitationContentBlockLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endBlockIndex: Long`

                - `startBlockIndex: Long`

                - `type: JsonValue; "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class BetaCitationWebSearchResultLocationParam:`

                - `citedText: String`

                - `encryptedIndex: String`

                - `title: Optional<String>`

                - `type: JsonValue; "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `url: String`

              - `class BetaCitationSearchResultLocationParam:`

                - `citedText: String`

                - `endBlockIndex: Long`

                - `searchResultIndex: Long`

                - `source: String`

                - `startBlockIndex: Long`

                - `title: Optional<String>`

                - `type: JsonValue; "search_result_location"constant`

                  - `SEARCH_RESULT_LOCATION("search_result_location")`

          - `source: String`

          - `title: String`

          - `type: JsonValue; "search_result"constant`

            - `SEARCH_RESULT("search_result")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<BetaCitationsConfigParam>`

            - `enabled: Optional<Boolean>`

        - `class BetaRequestDocumentBlock:`

          - `source: Source`

            - `class BetaBase64PdfSource:`

              - `data: String`

              - `mediaType: JsonValue; "application/pdf"constant`

                - `APPLICATION_PDF("application/pdf")`

              - `type: JsonValue; "base64"constant`

                - `BASE64("base64")`

            - `class BetaPlainTextSource:`

              - `data: String`

              - `mediaType: JsonValue; "text/plain"constant`

                - `TEXT_PLAIN("text/plain")`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

            - `class BetaContentBlockSource:`

              - `content: Content`

                - `String`

                - `List<BetaContentBlockSourceContent>`

                  - `class BetaTextBlockParam:`

                    - `text: String`

                    - `type: JsonValue; "text"constant`

                      - `TEXT("text")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                    - `citations: Optional<List<BetaTextCitationParam>>`

                      - `class BetaCitationCharLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endCharIndex: Long`

                        - `startCharIndex: Long`

                        - `type: JsonValue; "char_location"constant`

                          - `CHAR_LOCATION("char_location")`

                      - `class BetaCitationPageLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endPageNumber: Long`

                        - `startPageNumber: Long`

                        - `type: JsonValue; "page_location"constant`

                          - `PAGE_LOCATION("page_location")`

                      - `class BetaCitationContentBlockLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endBlockIndex: Long`

                        - `startBlockIndex: Long`

                        - `type: JsonValue; "content_block_location"constant`

                          - `CONTENT_BLOCK_LOCATION("content_block_location")`

                      - `class BetaCitationWebSearchResultLocationParam:`

                        - `citedText: String`

                        - `encryptedIndex: String`

                        - `title: Optional<String>`

                        - `type: JsonValue; "web_search_result_location"constant`

                          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                        - `url: String`

                      - `class BetaCitationSearchResultLocationParam:`

                        - `citedText: String`

                        - `endBlockIndex: Long`

                        - `searchResultIndex: Long`

                        - `source: String`

                        - `startBlockIndex: Long`

                        - `title: Optional<String>`

                        - `type: JsonValue; "search_result_location"constant`

                          - `SEARCH_RESULT_LOCATION("search_result_location")`

                  - `class BetaImageBlockParam:`

                    - `source: Source`

                      - `class BetaBase64ImageSource:`

                        - `data: String`

                        - `mediaType: MediaType`

                          - `IMAGE_JPEG("image/jpeg")`

                          - `IMAGE_PNG("image/png")`

                          - `IMAGE_GIF("image/gif")`

                          - `IMAGE_WEBP("image/webp")`

                        - `type: JsonValue; "base64"constant`

                          - `BASE64("base64")`

                      - `class BetaUrlImageSource:`

                        - `type: JsonValue; "url"constant`

                          - `URL("url")`

                        - `url: String`

                      - `class BetaFileImageSource:`

                        - `fileId: String`

                        - `type: JsonValue; "file"constant`

                          - `FILE("file")`

                    - `type: JsonValue; "image"constant`

                      - `IMAGE("image")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

              - `type: JsonValue; "content"constant`

                - `CONTENT("content")`

            - `class BetaUrlPdfSource:`

              - `type: JsonValue; "url"constant`

                - `URL("url")`

              - `url: String`

            - `class BetaFileDocumentSource:`

              - `fileId: String`

              - `type: JsonValue; "file"constant`

                - `FILE("file")`

          - `type: JsonValue; "document"constant`

            - `DOCUMENT("document")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<BetaCitationsConfigParam>`

            - `enabled: Optional<Boolean>`

          - `context: Optional<String>`

          - `title: Optional<String>`

        - `class BetaToolReferenceBlockParam:`

          Tool reference block that can be included in tool_result content.

          - `toolName: String`

          - `type: JsonValue; "tool_reference"constant`

            - `TOOL_REFERENCE("tool_reference")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

    - `isError: Optional<Boolean>`

  - `class BetaServerToolUseBlockParam:`

    - `id: String`

    - `input: Input`

    - `name: Name`

      - `WEB_SEARCH("web_search")`

      - `WEB_FETCH("web_fetch")`

      - `CODE_EXECUTION("code_execution")`

      - `BASH_CODE_EXECUTION("bash_code_execution")`

      - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

      - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

      - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

    - `type: JsonValue; "server_tool_use"constant`

      - `SERVER_TOOL_USE("server_tool_use")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `caller: Optional<Caller>`

      Tool invocation directly from the model.

      - `class BetaDirectCaller:`

        Tool invocation directly from the model.

        - `type: JsonValue; "direct"constant`

          - `DIRECT("direct")`

      - `class BetaServerToolCaller:`

        Tool invocation generated by a server-side tool.

        - `toolId: String`

        - `type: JsonValue; "code_execution_20250825"constant`

          - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `class BetaWebSearchToolResultBlockParam:`

    - `content: BetaWebSearchToolResultBlockParamContent`

      - `List<BetaWebSearchResultBlockParam>`

        - `encryptedContent: String`

        - `title: String`

        - `type: JsonValue; "web_search_result"constant`

          - `WEB_SEARCH_RESULT("web_search_result")`

        - `url: String`

        - `pageAge: Optional<String>`

      - `class BetaWebSearchToolRequestError:`

        - `errorCode: BetaWebSearchToolResultErrorCode`

          - `INVALID_TOOL_INPUT("invalid_tool_input")`

          - `UNAVAILABLE("unavailable")`

          - `MAX_USES_EXCEEDED("max_uses_exceeded")`

          - `TOO_MANY_REQUESTS("too_many_requests")`

          - `QUERY_TOO_LONG("query_too_long")`

        - `type: JsonValue; "web_search_tool_result_error"constant`

          - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

    - `toolUseId: String`

    - `type: JsonValue; "web_search_tool_result"constant`

      - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

  - `class BetaWebFetchToolResultBlockParam:`

    - `content: Content`

      - `class BetaWebFetchToolResultErrorBlockParam:`

        - `errorCode: BetaWebFetchToolResultErrorCode`

          - `INVALID_TOOL_INPUT("invalid_tool_input")`

          - `URL_TOO_LONG("url_too_long")`

          - `URL_NOT_ALLOWED("url_not_allowed")`

          - `URL_NOT_ACCESSIBLE("url_not_accessible")`

          - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

          - `TOO_MANY_REQUESTS("too_many_requests")`

          - `MAX_USES_EXCEEDED("max_uses_exceeded")`

          - `UNAVAILABLE("unavailable")`

        - `type: JsonValue; "web_fetch_tool_result_error"constant`

          - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

      - `class BetaWebFetchBlockParam:`

        - `content: BetaRequestDocumentBlock`

          - `source: Source`

            - `class BetaBase64PdfSource:`

              - `data: String`

              - `mediaType: JsonValue; "application/pdf"constant`

                - `APPLICATION_PDF("application/pdf")`

              - `type: JsonValue; "base64"constant`

                - `BASE64("base64")`

            - `class BetaPlainTextSource:`

              - `data: String`

              - `mediaType: JsonValue; "text/plain"constant`

                - `TEXT_PLAIN("text/plain")`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

            - `class BetaContentBlockSource:`

              - `content: Content`

                - `String`

                - `List<BetaContentBlockSourceContent>`

                  - `class BetaTextBlockParam:`

                    - `text: String`

                    - `type: JsonValue; "text"constant`

                      - `TEXT("text")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                    - `citations: Optional<List<BetaTextCitationParam>>`

                      - `class BetaCitationCharLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endCharIndex: Long`

                        - `startCharIndex: Long`

                        - `type: JsonValue; "char_location"constant`

                          - `CHAR_LOCATION("char_location")`

                      - `class BetaCitationPageLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endPageNumber: Long`

                        - `startPageNumber: Long`

                        - `type: JsonValue; "page_location"constant`

                          - `PAGE_LOCATION("page_location")`

                      - `class BetaCitationContentBlockLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endBlockIndex: Long`

                        - `startBlockIndex: Long`

                        - `type: JsonValue; "content_block_location"constant`

                          - `CONTENT_BLOCK_LOCATION("content_block_location")`

                      - `class BetaCitationWebSearchResultLocationParam:`

                        - `citedText: String`

                        - `encryptedIndex: String`

                        - `title: Optional<String>`

                        - `type: JsonValue; "web_search_result_location"constant`

                          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                        - `url: String`

                      - `class BetaCitationSearchResultLocationParam:`

                        - `citedText: String`

                        - `endBlockIndex: Long`

                        - `searchResultIndex: Long`

                        - `source: String`

                        - `startBlockIndex: Long`

                        - `title: Optional<String>`

                        - `type: JsonValue; "search_result_location"constant`

                          - `SEARCH_RESULT_LOCATION("search_result_location")`

                  - `class BetaImageBlockParam:`

                    - `source: Source`

                      - `class BetaBase64ImageSource:`

                        - `data: String`

                        - `mediaType: MediaType`

                          - `IMAGE_JPEG("image/jpeg")`

                          - `IMAGE_PNG("image/png")`

                          - `IMAGE_GIF("image/gif")`

                          - `IMAGE_WEBP("image/webp")`

                        - `type: JsonValue; "base64"constant`

                          - `BASE64("base64")`

                      - `class BetaUrlImageSource:`

                        - `type: JsonValue; "url"constant`

                          - `URL("url")`

                        - `url: String`

                      - `class BetaFileImageSource:`

                        - `fileId: String`

                        - `type: JsonValue; "file"constant`

                          - `FILE("file")`

                    - `type: JsonValue; "image"constant`

                      - `IMAGE("image")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

              - `type: JsonValue; "content"constant`

                - `CONTENT("content")`

            - `class BetaUrlPdfSource:`

              - `type: JsonValue; "url"constant`

                - `URL("url")`

              - `url: String`

            - `class BetaFileDocumentSource:`

              - `fileId: String`

              - `type: JsonValue; "file"constant`

                - `FILE("file")`

          - `type: JsonValue; "document"constant`

            - `DOCUMENT("document")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<BetaCitationsConfigParam>`

            - `enabled: Optional<Boolean>`

          - `context: Optional<String>`

          - `title: Optional<String>`

        - `type: JsonValue; "web_fetch_result"constant`

          - `WEB_FETCH_RESULT("web_fetch_result")`

        - `url: String`

          Fetched content URL

        - `retrievedAt: Optional<String>`

          ISO 8601 timestamp when the content was retrieved

    - `toolUseId: String`

    - `type: JsonValue; "web_fetch_tool_result"constant`

      - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

  - `class BetaCodeExecutionToolResultBlockParam:`

    - `content: BetaCodeExecutionToolResultBlockParamContent`

      - `class BetaCodeExecutionToolResultErrorParam:`

        - `errorCode: BetaCodeExecutionToolResultErrorCode`

          - `INVALID_TOOL_INPUT("invalid_tool_input")`

          - `UNAVAILABLE("unavailable")`

          - `TOO_MANY_REQUESTS("too_many_requests")`

          - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

        - `type: JsonValue; "code_execution_tool_result_error"constant`

          - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

      - `class BetaCodeExecutionResultBlockParam:`

        - `content: List<BetaCodeExecutionOutputBlockParam>`

          - `fileId: String`

          - `type: JsonValue; "code_execution_output"constant`

            - `CODE_EXECUTION_OUTPUT("code_execution_output")`

        - `returnCode: Long`

        - `stderr: String`

        - `stdout: String`

        - `type: JsonValue; "code_execution_result"constant`

          - `CODE_EXECUTION_RESULT("code_execution_result")`

    - `toolUseId: String`

    - `type: JsonValue; "code_execution_tool_result"constant`

      - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

  - `class BetaBashCodeExecutionToolResultBlockParam:`

    - `content: Content`

      - `class BetaBashCodeExecutionToolResultErrorParam:`

        - `errorCode: ErrorCode`

          - `INVALID_TOOL_INPUT("invalid_tool_input")`

          - `UNAVAILABLE("unavailable")`

          - `TOO_MANY_REQUESTS("too_many_requests")`

          - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

          - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

        - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

          - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

      - `class BetaBashCodeExecutionResultBlockParam:`

        - `content: List<BetaBashCodeExecutionOutputBlockParam>`

          - `fileId: String`

          - `type: JsonValue; "bash_code_execution_output"constant`

            - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

        - `returnCode: Long`

        - `stderr: String`

        - `stdout: String`

        - `type: JsonValue; "bash_code_execution_result"constant`

          - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

    - `toolUseId: String`

    - `type: JsonValue; "bash_code_execution_tool_result"constant`

      - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

  - `class BetaTextEditorCodeExecutionToolResultBlockParam:`

    - `content: Content`

      - `class BetaTextEditorCodeExecutionToolResultErrorParam:`

        - `errorCode: ErrorCode`

          - `INVALID_TOOL_INPUT("invalid_tool_input")`

          - `UNAVAILABLE("unavailable")`

          - `TOO_MANY_REQUESTS("too_many_requests")`

          - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

          - `FILE_NOT_FOUND("file_not_found")`

        - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

          - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

        - `errorMessage: Optional<String>`

      - `class BetaTextEditorCodeExecutionViewResultBlockParam:`

        - `content: String`

        - `fileType: FileType`

          - `TEXT("text")`

          - `IMAGE("image")`

          - `PDF("pdf")`

        - `type: JsonValue; "text_editor_code_execution_view_result"constant`

          - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

        - `numLines: Optional<Long>`

        - `startLine: Optional<Long>`

        - `totalLines: Optional<Long>`

      - `class BetaTextEditorCodeExecutionCreateResultBlockParam:`

        - `isFileUpdate: Boolean`

        - `type: JsonValue; "text_editor_code_execution_create_result"constant`

          - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

      - `class BetaTextEditorCodeExecutionStrReplaceResultBlockParam:`

        - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

          - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

        - `lines: Optional<List<String>>`

        - `newLines: Optional<Long>`

        - `newStart: Optional<Long>`

        - `oldLines: Optional<Long>`

        - `oldStart: Optional<Long>`

    - `toolUseId: String`

    - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

      - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

  - `class BetaToolSearchToolResultBlockParam:`

    - `content: Content`

      - `class BetaToolSearchToolResultErrorParam:`

        - `errorCode: ErrorCode`

          - `INVALID_TOOL_INPUT("invalid_tool_input")`

          - `UNAVAILABLE("unavailable")`

          - `TOO_MANY_REQUESTS("too_many_requests")`

          - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

        - `type: JsonValue; "tool_search_tool_result_error"constant`

          - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

      - `class BetaToolSearchToolSearchResultBlockParam:`

        - `toolReferences: List<BetaToolReferenceBlockParam>`

          - `toolName: String`

          - `type: JsonValue; "tool_reference"constant`

            - `TOOL_REFERENCE("tool_reference")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `type: JsonValue; "tool_search_tool_search_result"constant`

          - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

    - `toolUseId: String`

    - `type: JsonValue; "tool_search_tool_result"constant`

      - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

  - `class BetaMcpToolUseBlockParam:`

    - `id: String`

    - `input: Input`

    - `name: String`

    - `serverName: String`

      The name of the MCP server

    - `type: JsonValue; "mcp_tool_use"constant`

      - `MCP_TOOL_USE("mcp_tool_use")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

  - `class BetaRequestMcpToolResultBlockParam:`

    - `toolUseId: String`

    - `type: JsonValue; "mcp_tool_result"constant`

      - `MCP_TOOL_RESULT("mcp_tool_result")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `content: Optional<Content>`

      - `String`

      - `List<BetaTextBlockParam>`

        - `text: String`

        - `type: JsonValue; "text"constant`

          - `TEXT("text")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

        - `citations: Optional<List<BetaTextCitationParam>>`

          - `class BetaCitationCharLocationParam:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endCharIndex: Long`

            - `startCharIndex: Long`

            - `type: JsonValue; "char_location"constant`

              - `CHAR_LOCATION("char_location")`

          - `class BetaCitationPageLocationParam:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endPageNumber: Long`

            - `startPageNumber: Long`

            - `type: JsonValue; "page_location"constant`

              - `PAGE_LOCATION("page_location")`

          - `class BetaCitationContentBlockLocationParam:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endBlockIndex: Long`

            - `startBlockIndex: Long`

            - `type: JsonValue; "content_block_location"constant`

              - `CONTENT_BLOCK_LOCATION("content_block_location")`

          - `class BetaCitationWebSearchResultLocationParam:`

            - `citedText: String`

            - `encryptedIndex: String`

            - `title: Optional<String>`

            - `type: JsonValue; "web_search_result_location"constant`

              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

            - `url: String`

          - `class BetaCitationSearchResultLocationParam:`

            - `citedText: String`

            - `endBlockIndex: Long`

            - `searchResultIndex: Long`

            - `source: String`

            - `startBlockIndex: Long`

            - `title: Optional<String>`

            - `type: JsonValue; "search_result_location"constant`

              - `SEARCH_RESULT_LOCATION("search_result_location")`

    - `isError: Optional<Boolean>`

  - `class BetaContainerUploadBlockParam:`

    A content block that represents a file to be uploaded to the container
    Files uploaded via this block will be available in the container's input directory.

    - `fileId: String`

    - `type: JsonValue; "container_upload"constant`

      - `CONTAINER_UPLOAD("container_upload")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

### Beta Content Block Source

- `class BetaContentBlockSource:`

  - `content: Content`

    - `String`

    - `List<BetaContentBlockSourceContent>`

      - `class BetaTextBlockParam:`

        - `text: String`

        - `type: JsonValue; "text"constant`

          - `TEXT("text")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

        - `citations: Optional<List<BetaTextCitationParam>>`

          - `class BetaCitationCharLocationParam:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endCharIndex: Long`

            - `startCharIndex: Long`

            - `type: JsonValue; "char_location"constant`

              - `CHAR_LOCATION("char_location")`

          - `class BetaCitationPageLocationParam:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endPageNumber: Long`

            - `startPageNumber: Long`

            - `type: JsonValue; "page_location"constant`

              - `PAGE_LOCATION("page_location")`

          - `class BetaCitationContentBlockLocationParam:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endBlockIndex: Long`

            - `startBlockIndex: Long`

            - `type: JsonValue; "content_block_location"constant`

              - `CONTENT_BLOCK_LOCATION("content_block_location")`

          - `class BetaCitationWebSearchResultLocationParam:`

            - `citedText: String`

            - `encryptedIndex: String`

            - `title: Optional<String>`

            - `type: JsonValue; "web_search_result_location"constant`

              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

            - `url: String`

          - `class BetaCitationSearchResultLocationParam:`

            - `citedText: String`

            - `endBlockIndex: Long`

            - `searchResultIndex: Long`

            - `source: String`

            - `startBlockIndex: Long`

            - `title: Optional<String>`

            - `type: JsonValue; "search_result_location"constant`

              - `SEARCH_RESULT_LOCATION("search_result_location")`

      - `class BetaImageBlockParam:`

        - `source: Source`

          - `class BetaBase64ImageSource:`

            - `data: String`

            - `mediaType: MediaType`

              - `IMAGE_JPEG("image/jpeg")`

              - `IMAGE_PNG("image/png")`

              - `IMAGE_GIF("image/gif")`

              - `IMAGE_WEBP("image/webp")`

            - `type: JsonValue; "base64"constant`

              - `BASE64("base64")`

          - `class BetaUrlImageSource:`

            - `type: JsonValue; "url"constant`

              - `URL("url")`

            - `url: String`

          - `class BetaFileImageSource:`

            - `fileId: String`

            - `type: JsonValue; "file"constant`

              - `FILE("file")`

        - `type: JsonValue; "image"constant`

          - `IMAGE("image")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

  - `type: JsonValue; "content"constant`

    - `CONTENT("content")`

### Beta Content Block Source Content

- `class BetaContentBlockSourceContent: A class that can be one of several variants.union`

  - `class BetaTextBlockParam:`

    - `text: String`

    - `type: JsonValue; "text"constant`

      - `TEXT("text")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `citations: Optional<List<BetaTextCitationParam>>`

      - `class BetaCitationCharLocationParam:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endCharIndex: Long`

        - `startCharIndex: Long`

        - `type: JsonValue; "char_location"constant`

          - `CHAR_LOCATION("char_location")`

      - `class BetaCitationPageLocationParam:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endPageNumber: Long`

        - `startPageNumber: Long`

        - `type: JsonValue; "page_location"constant`

          - `PAGE_LOCATION("page_location")`

      - `class BetaCitationContentBlockLocationParam:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endBlockIndex: Long`

        - `startBlockIndex: Long`

        - `type: JsonValue; "content_block_location"constant`

          - `CONTENT_BLOCK_LOCATION("content_block_location")`

      - `class BetaCitationWebSearchResultLocationParam:`

        - `citedText: String`

        - `encryptedIndex: String`

        - `title: Optional<String>`

        - `type: JsonValue; "web_search_result_location"constant`

          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

        - `url: String`

      - `class BetaCitationSearchResultLocationParam:`

        - `citedText: String`

        - `endBlockIndex: Long`

        - `searchResultIndex: Long`

        - `source: String`

        - `startBlockIndex: Long`

        - `title: Optional<String>`

        - `type: JsonValue; "search_result_location"constant`

          - `SEARCH_RESULT_LOCATION("search_result_location")`

  - `class BetaImageBlockParam:`

    - `source: Source`

      - `class BetaBase64ImageSource:`

        - `data: String`

        - `mediaType: MediaType`

          - `IMAGE_JPEG("image/jpeg")`

          - `IMAGE_PNG("image/png")`

          - `IMAGE_GIF("image/gif")`

          - `IMAGE_WEBP("image/webp")`

        - `type: JsonValue; "base64"constant`

          - `BASE64("base64")`

      - `class BetaUrlImageSource:`

        - `type: JsonValue; "url"constant`

          - `URL("url")`

        - `url: String`

      - `class BetaFileImageSource:`

        - `fileId: String`

        - `type: JsonValue; "file"constant`

          - `FILE("file")`

    - `type: JsonValue; "image"constant`

      - `IMAGE("image")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

### Beta Context Management Config

- `class BetaContextManagementConfig:`

  - `edits: Optional<List<Edit>>`

    List of context management edits to apply

    - `class BetaClearToolUses20250919Edit:`

      - `type: JsonValue; "clear_tool_uses_20250919"constant`

        - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

      - `clearAtLeast: Optional<BetaInputTokensClearAtLeast>`

        Minimum number of tokens that must be cleared when triggered. Context will only be modified if at least this many tokens can be removed.

        - `type: JsonValue; "input_tokens"constant`

          - `INPUT_TOKENS("input_tokens")`

        - `value: Long`

      - `clearToolInputs: Optional<ClearToolInputs>`

        Whether to clear all tool inputs (bool) or specific tool inputs to clear (list)

        - `Boolean`

        - `List<String>`

      - `excludeTools: Optional<List<String>>`

        Tool names whose uses are preserved from clearing

      - `keep: Optional<BetaToolUsesKeep>`

        Number of tool uses to retain in the conversation

        - `type: JsonValue; "tool_uses"constant`

          - `TOOL_USES("tool_uses")`

        - `value: Long`

      - `trigger: Optional<Trigger>`

        Condition that triggers the context management strategy

        - `class BetaInputTokensTrigger:`

          - `type: JsonValue; "input_tokens"constant`

            - `INPUT_TOKENS("input_tokens")`

          - `value: Long`

        - `class BetaToolUsesTrigger:`

          - `type: JsonValue; "tool_uses"constant`

            - `TOOL_USES("tool_uses")`

          - `value: Long`

    - `class BetaClearThinking20251015Edit:`

      - `type: JsonValue; "clear_thinking_20251015"constant`

        - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

      - `keep: Optional<Keep>`

        Number of most recent assistant turns to keep thinking blocks for. Older turns will have their thinking blocks removed.

        - `class BetaThinkingTurns:`

          - `type: JsonValue; "thinking_turns"constant`

            - `THINKING_TURNS("thinking_turns")`

          - `value: Long`

        - `class BetaAllThinkingTurns:`

          - `type: JsonValue; "all"constant`

            - `ALL("all")`

        - `JsonValue;`

          - `ALL("all")`

### Beta Context Management Response

- `class BetaContextManagementResponse:`

  - `appliedEdits: List<AppliedEdit>`

    List of context management edits that were applied.

    - `class BetaClearToolUses20250919EditResponse:`

      - `clearedInputTokens: Long`

        Number of input tokens cleared by this edit.

      - `clearedToolUses: Long`

        Number of tool uses that were cleared.

      - `type: JsonValue; "clear_tool_uses_20250919"constant`

        The type of context management edit applied.

        - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

    - `class BetaClearThinking20251015EditResponse:`

      - `clearedInputTokens: Long`

        Number of input tokens cleared by this edit.

      - `clearedThinkingTurns: Long`

        Number of thinking turns that were cleared.

      - `type: JsonValue; "clear_thinking_20251015"constant`

        The type of context management edit applied.

        - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

### Beta Count Tokens Context Management Response

- `class BetaCountTokensContextManagementResponse:`

  - `originalInputTokens: Long`

    The original token count before context management was applied

### Beta Direct Caller

- `class BetaDirectCaller:`

  Tool invocation directly from the model.

  - `type: JsonValue; "direct"constant`

    - `DIRECT("direct")`

### Beta Document Block

- `class BetaDocumentBlock:`

  - `citations: Optional<BetaCitationConfig>`

    Citation configuration for the document

    - `enabled: Boolean`

  - `source: Source`

    - `class BetaBase64PdfSource:`

      - `data: String`

      - `mediaType: JsonValue; "application/pdf"constant`

        - `APPLICATION_PDF("application/pdf")`

      - `type: JsonValue; "base64"constant`

        - `BASE64("base64")`

    - `class BetaPlainTextSource:`

      - `data: String`

      - `mediaType: JsonValue; "text/plain"constant`

        - `TEXT_PLAIN("text/plain")`

      - `type: JsonValue; "text"constant`

        - `TEXT("text")`

  - `title: Optional<String>`

    The title of the document

  - `type: JsonValue; "document"constant`

    - `DOCUMENT("document")`

### Beta File Document Source

- `class BetaFileDocumentSource:`

  - `fileId: String`

  - `type: JsonValue; "file"constant`

    - `FILE("file")`

### Beta File Image Source

- `class BetaFileImageSource:`

  - `fileId: String`

  - `type: JsonValue; "file"constant`

    - `FILE("file")`

### Beta Image Block Param

- `class BetaImageBlockParam:`

  - `source: Source`

    - `class BetaBase64ImageSource:`

      - `data: String`

      - `mediaType: MediaType`

        - `IMAGE_JPEG("image/jpeg")`

        - `IMAGE_PNG("image/png")`

        - `IMAGE_GIF("image/gif")`

        - `IMAGE_WEBP("image/webp")`

      - `type: JsonValue; "base64"constant`

        - `BASE64("base64")`

    - `class BetaUrlImageSource:`

      - `type: JsonValue; "url"constant`

        - `URL("url")`

      - `url: String`

    - `class BetaFileImageSource:`

      - `fileId: String`

      - `type: JsonValue; "file"constant`

        - `FILE("file")`

  - `type: JsonValue; "image"constant`

    - `IMAGE("image")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

### Beta Input JSON Delta

- `class BetaInputJsonDelta:`

  - `partialJson: String`

  - `type: JsonValue; "input_json_delta"constant`

    - `INPUT_JSON_DELTA("input_json_delta")`

### Beta Input Tokens Clear At Least

- `class BetaInputTokensClearAtLeast:`

  - `type: JsonValue; "input_tokens"constant`

    - `INPUT_TOKENS("input_tokens")`

  - `value: Long`

### Beta Input Tokens Trigger

- `class BetaInputTokensTrigger:`

  - `type: JsonValue; "input_tokens"constant`

    - `INPUT_TOKENS("input_tokens")`

  - `value: Long`

### Beta JSON Output Format

- `class BetaJsonOutputFormat:`

  - `schema: Schema`

    The JSON schema of the format

  - `type: JsonValue; "json_schema"constant`

    - `JSON_SCHEMA("json_schema")`

### Beta MCP Tool Config

- `class BetaMcpToolConfig:`

  Configuration for a specific tool in an MCP toolset.

  - `deferLoading: Optional<Boolean>`

  - `enabled: Optional<Boolean>`

### Beta MCP Tool Default Config

- `class BetaMcpToolDefaultConfig:`

  Default configuration for tools in an MCP toolset.

  - `deferLoading: Optional<Boolean>`

  - `enabled: Optional<Boolean>`

### Beta MCP Tool Result Block

- `class BetaMcpToolResultBlock:`

  - `content: Content`

    - `String`

    - `List<BetaTextBlock>`

      - `citations: Optional<List<BetaTextCitation>>`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `class BetaCitationCharLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endCharIndex: Long`

          - `fileId: Optional<String>`

          - `startCharIndex: Long`

          - `type: JsonValue; "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class BetaCitationPageLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endPageNumber: Long`

          - `fileId: Optional<String>`

          - `startPageNumber: Long`

          - `type: JsonValue; "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class BetaCitationContentBlockLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endBlockIndex: Long`

          - `fileId: Optional<String>`

          - `startBlockIndex: Long`

          - `type: JsonValue; "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class BetaCitationsWebSearchResultLocation:`

          - `citedText: String`

          - `encryptedIndex: String`

          - `title: Optional<String>`

          - `type: JsonValue; "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `url: String`

        - `class BetaCitationSearchResultLocation:`

          - `citedText: String`

          - `endBlockIndex: Long`

          - `searchResultIndex: Long`

          - `source: String`

          - `startBlockIndex: Long`

          - `title: Optional<String>`

          - `type: JsonValue; "search_result_location"constant`

            - `SEARCH_RESULT_LOCATION("search_result_location")`

      - `text: String`

      - `type: JsonValue; "text"constant`

        - `TEXT("text")`

  - `isError: Boolean`

  - `toolUseId: String`

  - `type: JsonValue; "mcp_tool_result"constant`

    - `MCP_TOOL_RESULT("mcp_tool_result")`

### Beta MCP Tool Use Block

- `class BetaMcpToolUseBlock:`

  - `id: String`

  - `input: Input`

  - `name: String`

    The name of the MCP tool

  - `serverName: String`

    The name of the MCP server

  - `type: JsonValue; "mcp_tool_use"constant`

    - `MCP_TOOL_USE("mcp_tool_use")`

### Beta MCP Tool Use Block Param

- `class BetaMcpToolUseBlockParam:`

  - `id: String`

  - `input: Input`

  - `name: String`

  - `serverName: String`

    The name of the MCP server

  - `type: JsonValue; "mcp_tool_use"constant`

    - `MCP_TOOL_USE("mcp_tool_use")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

### Beta MCP Toolset

- `class BetaMcpToolset:`

  Configuration for a group of tools from an MCP server.

  Allows configuring enabled status and defer_loading for all tools
  from an MCP server, with optional per-tool overrides.

  - `mcpServerName: String`

    Name of the MCP server to configure tools for

  - `type: JsonValue; "mcp_toolset"constant`

    - `MCP_TOOLSET("mcp_toolset")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `configs: Optional<Configs>`

    Configuration overrides for specific tools, keyed by tool name

    - `deferLoading: Optional<Boolean>`

    - `enabled: Optional<Boolean>`

  - `defaultConfig: Optional<BetaMcpToolDefaultConfig>`

    Default configuration applied to all tools from this server

    - `deferLoading: Optional<Boolean>`

    - `enabled: Optional<Boolean>`

### Beta Memory Tool 20250818

- `class BetaMemoryTool20250818:`

  - `name: JsonValue; "memory"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `MEMORY("memory")`

  - `type: JsonValue; "memory_20250818"constant`

    - `MEMORY_20250818("memory_20250818")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `inputExamples: Optional<List<InputExample>>`

  - `strict: Optional<Boolean>`

### Beta Memory Tool 20250818 Command

- `class BetaMemoryTool20250818Command: A class that can be one of several variants.union`

  - `class BetaMemoryTool20250818ViewCommand:`

    - `command: JsonValue; "view"constant`

      Command type identifier

      - `VIEW("view")`

    - `path: String`

      Path to directory or file to view

    - `viewRange: Optional<List<Long>>`

      Optional line range for viewing specific lines

  - `class BetaMemoryTool20250818CreateCommand:`

    - `command: JsonValue; "create"constant`

      Command type identifier

      - `CREATE("create")`

    - `fileText: String`

      Content to write to the file

    - `path: String`

      Path where the file should be created

  - `class BetaMemoryTool20250818StrReplaceCommand:`

    - `command: JsonValue; "str_replace"constant`

      Command type identifier

      - `STR_REPLACE("str_replace")`

    - `newStr: String`

      Text to replace with

    - `oldStr: String`

      Text to search for and replace

    - `path: String`

      Path to the file where text should be replaced

  - `class BetaMemoryTool20250818InsertCommand:`

    - `command: JsonValue; "insert"constant`

      Command type identifier

      - `INSERT("insert")`

    - `insertLine: Long`

      Line number where text should be inserted

    - `insertText: String`

      Text to insert at the specified line

    - `path: String`

      Path to the file where text should be inserted

  - `class BetaMemoryTool20250818DeleteCommand:`

    - `command: JsonValue; "delete"constant`

      Command type identifier

      - `DELETE("delete")`

    - `path: String`

      Path to the file or directory to delete

  - `class BetaMemoryTool20250818RenameCommand:`

    - `command: JsonValue; "rename"constant`

      Command type identifier

      - `RENAME("rename")`

    - `newPath: String`

      New path for the file or directory

    - `oldPath: String`

      Current path of the file or directory

### Beta Memory Tool 20250818 Create Command

- `class BetaMemoryTool20250818CreateCommand:`

  - `command: JsonValue; "create"constant`

    Command type identifier

    - `CREATE("create")`

  - `fileText: String`

    Content to write to the file

  - `path: String`

    Path where the file should be created

### Beta Memory Tool 20250818 Delete Command

- `class BetaMemoryTool20250818DeleteCommand:`

  - `command: JsonValue; "delete"constant`

    Command type identifier

    - `DELETE("delete")`

  - `path: String`

    Path to the file or directory to delete

### Beta Memory Tool 20250818 Insert Command

- `class BetaMemoryTool20250818InsertCommand:`

  - `command: JsonValue; "insert"constant`

    Command type identifier

    - `INSERT("insert")`

  - `insertLine: Long`

    Line number where text should be inserted

  - `insertText: String`

    Text to insert at the specified line

  - `path: String`

    Path to the file where text should be inserted

### Beta Memory Tool 20250818 Rename Command

- `class BetaMemoryTool20250818RenameCommand:`

  - `command: JsonValue; "rename"constant`

    Command type identifier

    - `RENAME("rename")`

  - `newPath: String`

    New path for the file or directory

  - `oldPath: String`

    Current path of the file or directory

### Beta Memory Tool 20250818 Str Replace Command

- `class BetaMemoryTool20250818StrReplaceCommand:`

  - `command: JsonValue; "str_replace"constant`

    Command type identifier

    - `STR_REPLACE("str_replace")`

  - `newStr: String`

    Text to replace with

  - `oldStr: String`

    Text to search for and replace

  - `path: String`

    Path to the file where text should be replaced

### Beta Memory Tool 20250818 View Command

- `class BetaMemoryTool20250818ViewCommand:`

  - `command: JsonValue; "view"constant`

    Command type identifier

    - `VIEW("view")`

  - `path: String`

    Path to directory or file to view

  - `viewRange: Optional<List<Long>>`

    Optional line range for viewing specific lines

### Beta Message

- `class BetaMessage:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `container: Optional<BetaContainer>`

    Information about the container used in the request (for the code execution tool)

    - `id: String`

      Identifier for the container used in this request

    - `expiresAt: LocalDateTime`

      The time at which the container will expire.

    - `skills: Optional<List<BetaSkill>>`

      Skills loaded in the container

      - `skillId: String`

        Skill ID

      - `type: Type`

        Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

        - `ANTHROPIC("anthropic")`

        - `CUSTOM("custom")`

      - `version: String`

        Skill version or 'latest' for most recent version

  - `content: List<BetaContentBlock>`

    Content generated by the model.

    This is an array of content blocks, each of which has a `type` that determines its shape.

    Example:

    ```json
    [{"type": "text", "text": "Hi, I'm Claude."}]
    ```

    If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

    For example, if the input `messages` were:

    ```json
    [
      {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
      {"role": "assistant", "content": "The best answer is ("}
    ]
    ```

    Then the response `content` might be:

    ```json
    [{"type": "text", "text": "B)"}]
    ```

    - `class BetaTextBlock:`

      - `citations: Optional<List<BetaTextCitation>>`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `class BetaCitationCharLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endCharIndex: Long`

          - `fileId: Optional<String>`

          - `startCharIndex: Long`

          - `type: JsonValue; "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class BetaCitationPageLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endPageNumber: Long`

          - `fileId: Optional<String>`

          - `startPageNumber: Long`

          - `type: JsonValue; "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class BetaCitationContentBlockLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endBlockIndex: Long`

          - `fileId: Optional<String>`

          - `startBlockIndex: Long`

          - `type: JsonValue; "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class BetaCitationsWebSearchResultLocation:`

          - `citedText: String`

          - `encryptedIndex: String`

          - `title: Optional<String>`

          - `type: JsonValue; "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `url: String`

        - `class BetaCitationSearchResultLocation:`

          - `citedText: String`

          - `endBlockIndex: Long`

          - `searchResultIndex: Long`

          - `source: String`

          - `startBlockIndex: Long`

          - `title: Optional<String>`

          - `type: JsonValue; "search_result_location"constant`

            - `SEARCH_RESULT_LOCATION("search_result_location")`

      - `text: String`

      - `type: JsonValue; "text"constant`

        - `TEXT("text")`

    - `class BetaThinkingBlock:`

      - `signature: String`

      - `thinking: String`

      - `type: JsonValue; "thinking"constant`

        - `THINKING("thinking")`

    - `class BetaRedactedThinkingBlock:`

      - `data: String`

      - `type: JsonValue; "redacted_thinking"constant`

        - `REDACTED_THINKING("redacted_thinking")`

    - `class BetaToolUseBlock:`

      - `id: String`

      - `input: Input`

      - `name: String`

      - `type: JsonValue; "tool_use"constant`

        - `TOOL_USE("tool_use")`

      - `caller: Optional<Caller>`

        Tool invocation directly from the model.

        - `class BetaDirectCaller:`

          Tool invocation directly from the model.

          - `type: JsonValue; "direct"constant`

            - `DIRECT("direct")`

        - `class BetaServerToolCaller:`

          Tool invocation generated by a server-side tool.

          - `toolId: String`

          - `type: JsonValue; "code_execution_20250825"constant`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `class BetaServerToolUseBlock:`

      - `id: String`

      - `caller: Caller`

        Tool invocation directly from the model.

        - `class BetaDirectCaller:`

          Tool invocation directly from the model.

          - `type: JsonValue; "direct"constant`

            - `DIRECT("direct")`

        - `class BetaServerToolCaller:`

          Tool invocation generated by a server-side tool.

          - `toolId: String`

          - `type: JsonValue; "code_execution_20250825"constant`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `input: Input`

      - `name: Name`

        - `WEB_SEARCH("web_search")`

        - `WEB_FETCH("web_fetch")`

        - `CODE_EXECUTION("code_execution")`

        - `BASH_CODE_EXECUTION("bash_code_execution")`

        - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

        - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

        - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

      - `type: JsonValue; "server_tool_use"constant`

        - `SERVER_TOOL_USE("server_tool_use")`

    - `class BetaWebSearchToolResultBlock:`

      - `content: BetaWebSearchToolResultBlockContent`

        - `class BetaWebSearchToolResultError:`

          - `errorCode: BetaWebSearchToolResultErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `MAX_USES_EXCEEDED("max_uses_exceeded")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `QUERY_TOO_LONG("query_too_long")`

          - `type: JsonValue; "web_search_tool_result_error"constant`

            - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

        - `List<BetaWebSearchResultBlock>`

          - `encryptedContent: String`

          - `pageAge: Optional<String>`

          - `title: String`

          - `type: JsonValue; "web_search_result"constant`

            - `WEB_SEARCH_RESULT("web_search_result")`

          - `url: String`

      - `toolUseId: String`

      - `type: JsonValue; "web_search_tool_result"constant`

        - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

    - `class BetaWebFetchToolResultBlock:`

      - `content: Content`

        - `class BetaWebFetchToolResultErrorBlock:`

          - `errorCode: BetaWebFetchToolResultErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `URL_TOO_LONG("url_too_long")`

            - `URL_NOT_ALLOWED("url_not_allowed")`

            - `URL_NOT_ACCESSIBLE("url_not_accessible")`

            - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `MAX_USES_EXCEEDED("max_uses_exceeded")`

            - `UNAVAILABLE("unavailable")`

          - `type: JsonValue; "web_fetch_tool_result_error"constant`

            - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

        - `class BetaWebFetchBlock:`

          - `content: BetaDocumentBlock`

            - `citations: Optional<BetaCitationConfig>`

              Citation configuration for the document

              - `enabled: Boolean`

            - `source: Source`

              - `class BetaBase64PdfSource:`

                - `data: String`

                - `mediaType: JsonValue; "application/pdf"constant`

                  - `APPLICATION_PDF("application/pdf")`

                - `type: JsonValue; "base64"constant`

                  - `BASE64("base64")`

              - `class BetaPlainTextSource:`

                - `data: String`

                - `mediaType: JsonValue; "text/plain"constant`

                  - `TEXT_PLAIN("text/plain")`

                - `type: JsonValue; "text"constant`

                  - `TEXT("text")`

            - `title: Optional<String>`

              The title of the document

            - `type: JsonValue; "document"constant`

              - `DOCUMENT("document")`

          - `retrievedAt: Optional<String>`

            ISO 8601 timestamp when the content was retrieved

          - `type: JsonValue; "web_fetch_result"constant`

            - `WEB_FETCH_RESULT("web_fetch_result")`

          - `url: String`

            Fetched content URL

      - `toolUseId: String`

      - `type: JsonValue; "web_fetch_tool_result"constant`

        - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

    - `class BetaCodeExecutionToolResultBlock:`

      - `content: BetaCodeExecutionToolResultBlockContent`

        - `class BetaCodeExecutionToolResultError:`

          - `errorCode: BetaCodeExecutionToolResultErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

          - `type: JsonValue; "code_execution_tool_result_error"constant`

            - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

        - `class BetaCodeExecutionResultBlock:`

          - `content: List<BetaCodeExecutionOutputBlock>`

            - `fileId: String`

            - `type: JsonValue; "code_execution_output"constant`

              - `CODE_EXECUTION_OUTPUT("code_execution_output")`

          - `returnCode: Long`

          - `stderr: String`

          - `stdout: String`

          - `type: JsonValue; "code_execution_result"constant`

            - `CODE_EXECUTION_RESULT("code_execution_result")`

      - `toolUseId: String`

      - `type: JsonValue; "code_execution_tool_result"constant`

        - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

    - `class BetaBashCodeExecutionToolResultBlock:`

      - `content: Content`

        - `class BetaBashCodeExecutionToolResultError:`

          - `errorCode: ErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

          - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

            - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

        - `class BetaBashCodeExecutionResultBlock:`

          - `content: List<BetaBashCodeExecutionOutputBlock>`

            - `fileId: String`

            - `type: JsonValue; "bash_code_execution_output"constant`

              - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

          - `returnCode: Long`

          - `stderr: String`

          - `stdout: String`

          - `type: JsonValue; "bash_code_execution_result"constant`

            - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

      - `toolUseId: String`

      - `type: JsonValue; "bash_code_execution_tool_result"constant`

        - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

    - `class BetaTextEditorCodeExecutionToolResultBlock:`

      - `content: Content`

        - `class BetaTextEditorCodeExecutionToolResultError:`

          - `errorCode: ErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `FILE_NOT_FOUND("file_not_found")`

          - `errorMessage: Optional<String>`

          - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

        - `class BetaTextEditorCodeExecutionViewResultBlock:`

          - `content: String`

          - `fileType: FileType`

            - `TEXT("text")`

            - `IMAGE("image")`

            - `PDF("pdf")`

          - `numLines: Optional<Long>`

          - `startLine: Optional<Long>`

          - `totalLines: Optional<Long>`

          - `type: JsonValue; "text_editor_code_execution_view_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

        - `class BetaTextEditorCodeExecutionCreateResultBlock:`

          - `isFileUpdate: Boolean`

          - `type: JsonValue; "text_editor_code_execution_create_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

        - `class BetaTextEditorCodeExecutionStrReplaceResultBlock:`

          - `lines: Optional<List<String>>`

          - `newLines: Optional<Long>`

          - `newStart: Optional<Long>`

          - `oldLines: Optional<Long>`

          - `oldStart: Optional<Long>`

          - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

      - `toolUseId: String`

      - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

        - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

    - `class BetaToolSearchToolResultBlock:`

      - `content: Content`

        - `class BetaToolSearchToolResultError:`

          - `errorCode: ErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

          - `errorMessage: Optional<String>`

          - `type: JsonValue; "tool_search_tool_result_error"constant`

            - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

        - `class BetaToolSearchToolSearchResultBlock:`

          - `toolReferences: List<BetaToolReferenceBlock>`

            - `toolName: String`

            - `type: JsonValue; "tool_reference"constant`

              - `TOOL_REFERENCE("tool_reference")`

          - `type: JsonValue; "tool_search_tool_search_result"constant`

            - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

      - `toolUseId: String`

      - `type: JsonValue; "tool_search_tool_result"constant`

        - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

    - `class BetaMcpToolUseBlock:`

      - `id: String`

      - `input: Input`

      - `name: String`

        The name of the MCP tool

      - `serverName: String`

        The name of the MCP server

      - `type: JsonValue; "mcp_tool_use"constant`

        - `MCP_TOOL_USE("mcp_tool_use")`

    - `class BetaMcpToolResultBlock:`

      - `content: Content`

        - `String`

        - `List<BetaTextBlock>`

          - `citations: Optional<List<BetaTextCitation>>`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `class BetaCitationCharLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `fileId: Optional<String>`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class BetaCitationPageLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `fileId: Optional<String>`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class BetaCitationContentBlockLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `fileId: Optional<String>`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class BetaCitationsWebSearchResultLocation:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class BetaCitationSearchResultLocation:`

              - `citedText: String`

              - `endBlockIndex: Long`

              - `searchResultIndex: Long`

              - `source: String`

              - `startBlockIndex: Long`

              - `title: Optional<String>`

              - `type: JsonValue; "search_result_location"constant`

                - `SEARCH_RESULT_LOCATION("search_result_location")`

          - `text: String`

          - `type: JsonValue; "text"constant`

            - `TEXT("text")`

      - `isError: Boolean`

      - `toolUseId: String`

      - `type: JsonValue; "mcp_tool_result"constant`

        - `MCP_TOOL_RESULT("mcp_tool_result")`

    - `class BetaContainerUploadBlock:`

      Response model for a file uploaded to the container.

      - `fileId: String`

      - `type: JsonValue; "container_upload"constant`

        - `CONTAINER_UPLOAD("container_upload")`

  - `contextManagement: Optional<BetaContextManagementResponse>`

    Context management response.

    Information about context management strategies applied during the request.

    - `appliedEdits: List<AppliedEdit>`

      List of context management edits that were applied.

      - `class BetaClearToolUses20250919EditResponse:`

        - `clearedInputTokens: Long`

          Number of input tokens cleared by this edit.

        - `clearedToolUses: Long`

          Number of tool uses that were cleared.

        - `type: JsonValue; "clear_tool_uses_20250919"constant`

          The type of context management edit applied.

          - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

      - `class BetaClearThinking20251015EditResponse:`

        - `clearedInputTokens: Long`

          Number of input tokens cleared by this edit.

        - `clearedThinkingTurns: Long`

          Number of thinking turns that were cleared.

        - `type: JsonValue; "clear_thinking_20251015"constant`

          The type of context management edit applied.

          - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

  - `model: Model`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

    - `CLAUDE_OPUS_4_5_20251101("claude-opus-4-5-20251101")`

      Premium model combining maximum intelligence with practical performance

    - `CLAUDE_OPUS_4_5("claude-opus-4-5")`

      Premium model combining maximum intelligence with practical performance

    - `CLAUDE_3_7_SONNET_LATEST("claude-3-7-sonnet-latest")`

      High-performance model with early extended thinking

    - `CLAUDE_3_7_SONNET_20250219("claude-3-7-sonnet-20250219")`

      High-performance model with early extended thinking

    - `CLAUDE_3_5_HAIKU_LATEST("claude-3-5-haiku-latest")`

      Fastest and most compact model for near-instant responsiveness

    - `CLAUDE_3_5_HAIKU_20241022("claude-3-5-haiku-20241022")`

      Our fastest model

    - `CLAUDE_HAIKU_4_5("claude-haiku-4-5")`

      Hybrid model, capable of near-instant responses and extended thinking

    - `CLAUDE_HAIKU_4_5_20251001("claude-haiku-4-5-20251001")`

      Hybrid model, capable of near-instant responses and extended thinking

    - `CLAUDE_SONNET_4_20250514("claude-sonnet-4-20250514")`

      High-performance model with extended thinking

    - `CLAUDE_SONNET_4_0("claude-sonnet-4-0")`

      High-performance model with extended thinking

    - `CLAUDE_4_SONNET_20250514("claude-4-sonnet-20250514")`

      High-performance model with extended thinking

    - `CLAUDE_SONNET_4_5("claude-sonnet-4-5")`

      Our best model for real-world agents and coding

    - `CLAUDE_SONNET_4_5_20250929("claude-sonnet-4-5-20250929")`

      Our best model for real-world agents and coding

    - `CLAUDE_OPUS_4_0("claude-opus-4-0")`

      Our most capable model

    - `CLAUDE_OPUS_4_20250514("claude-opus-4-20250514")`

      Our most capable model

    - `CLAUDE_4_OPUS_20250514("claude-4-opus-20250514")`

      Our most capable model

    - `CLAUDE_OPUS_4_1_20250805("claude-opus-4-1-20250805")`

      Our most capable model

    - `CLAUDE_3_OPUS_LATEST("claude-3-opus-latest")`

      Excels at writing and complex tasks

    - `CLAUDE_3_OPUS_20240229("claude-3-opus-20240229")`

      Excels at writing and complex tasks

    - `CLAUDE_3_HAIKU_20240307("claude-3-haiku-20240307")`

      Our previous most fast and cost-effective

  - `role: JsonValue; "assistant"constant`

    Conversational role of the generated message.

    This will always be `"assistant"`.

    - `ASSISTANT("assistant")`

  - `stopReason: Optional<BetaStopReason>`

    The reason that we stopped.

    This may be one the following values:

    * `"end_turn"`: the model reached a natural stopping point
    * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
    * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
    * `"tool_use"`: the model invoked one or more tools
    * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
    * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

    In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

    - `END_TURN("end_turn")`

    - `MAX_TOKENS("max_tokens")`

    - `STOP_SEQUENCE("stop_sequence")`

    - `TOOL_USE("tool_use")`

    - `PAUSE_TURN("pause_turn")`

    - `REFUSAL("refusal")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED("model_context_window_exceeded")`

  - `stopSequence: Optional<String>`

    Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was generated.

  - `type: JsonValue; "message"constant`

    Object type.

    For Messages, this is always `"message"`.

    - `MESSAGE("message")`

  - `usage: BetaUsage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cacheCreation: Optional<BetaCacheCreation>`

      Breakdown of cached tokens by TTL

      - `ephemeral1hInputTokens: Long`

        The number of input tokens used to create the 1 hour cache entry.

      - `ephemeral5mInputTokens: Long`

        The number of input tokens used to create the 5 minute cache entry.

    - `cacheCreationInputTokens: Optional<Long>`

      The number of input tokens used to create the cache entry.

    - `cacheReadInputTokens: Optional<Long>`

      The number of input tokens read from the cache.

    - `inputTokens: Long`

      The number of input tokens which were used.

    - `outputTokens: Long`

      The number of output tokens which were used.

    - `serverToolUse: Optional<BetaServerToolUsage>`

      The number of server tool requests.

      - `webFetchRequests: Long`

        The number of web fetch tool requests.

      - `webSearchRequests: Long`

        The number of web search tool requests.

    - `serviceTier: Optional<ServiceTier>`

      If the request used the priority, standard, or batch tier.

      - `STANDARD("standard")`

      - `PRIORITY("priority")`

      - `BATCH("batch")`

### Beta Message Delta Usage

- `class BetaMessageDeltaUsage:`

  - `cacheCreationInputTokens: Optional<Long>`

    The cumulative number of input tokens used to create the cache entry.

  - `cacheReadInputTokens: Optional<Long>`

    The cumulative number of input tokens read from the cache.

  - `inputTokens: Optional<Long>`

    The cumulative number of input tokens which were used.

  - `outputTokens: Long`

    The cumulative number of output tokens which were used.

  - `serverToolUse: Optional<BetaServerToolUsage>`

    The number of server tool requests.

    - `webFetchRequests: Long`

      The number of web fetch tool requests.

    - `webSearchRequests: Long`

      The number of web search tool requests.

### Beta Message Param

- `class BetaMessageParam:`

  - `content: Content`

    - `String`

    - `List<BetaContentBlockParam>`

      - `class BetaTextBlockParam:`

        - `text: String`

        - `type: JsonValue; "text"constant`

          - `TEXT("text")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

        - `citations: Optional<List<BetaTextCitationParam>>`

          - `class BetaCitationCharLocationParam:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endCharIndex: Long`

            - `startCharIndex: Long`

            - `type: JsonValue; "char_location"constant`

              - `CHAR_LOCATION("char_location")`

          - `class BetaCitationPageLocationParam:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endPageNumber: Long`

            - `startPageNumber: Long`

            - `type: JsonValue; "page_location"constant`

              - `PAGE_LOCATION("page_location")`

          - `class BetaCitationContentBlockLocationParam:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endBlockIndex: Long`

            - `startBlockIndex: Long`

            - `type: JsonValue; "content_block_location"constant`

              - `CONTENT_BLOCK_LOCATION("content_block_location")`

          - `class BetaCitationWebSearchResultLocationParam:`

            - `citedText: String`

            - `encryptedIndex: String`

            - `title: Optional<String>`

            - `type: JsonValue; "web_search_result_location"constant`

              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

            - `url: String`

          - `class BetaCitationSearchResultLocationParam:`

            - `citedText: String`

            - `endBlockIndex: Long`

            - `searchResultIndex: Long`

            - `source: String`

            - `startBlockIndex: Long`

            - `title: Optional<String>`

            - `type: JsonValue; "search_result_location"constant`

              - `SEARCH_RESULT_LOCATION("search_result_location")`

      - `class BetaImageBlockParam:`

        - `source: Source`

          - `class BetaBase64ImageSource:`

            - `data: String`

            - `mediaType: MediaType`

              - `IMAGE_JPEG("image/jpeg")`

              - `IMAGE_PNG("image/png")`

              - `IMAGE_GIF("image/gif")`

              - `IMAGE_WEBP("image/webp")`

            - `type: JsonValue; "base64"constant`

              - `BASE64("base64")`

          - `class BetaUrlImageSource:`

            - `type: JsonValue; "url"constant`

              - `URL("url")`

            - `url: String`

          - `class BetaFileImageSource:`

            - `fileId: String`

            - `type: JsonValue; "file"constant`

              - `FILE("file")`

        - `type: JsonValue; "image"constant`

          - `IMAGE("image")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

      - `class BetaRequestDocumentBlock:`

        - `source: Source`

          - `class BetaBase64PdfSource:`

            - `data: String`

            - `mediaType: JsonValue; "application/pdf"constant`

              - `APPLICATION_PDF("application/pdf")`

            - `type: JsonValue; "base64"constant`

              - `BASE64("base64")`

          - `class BetaPlainTextSource:`

            - `data: String`

            - `mediaType: JsonValue; "text/plain"constant`

              - `TEXT_PLAIN("text/plain")`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

          - `class BetaContentBlockSource:`

            - `content: Content`

              - `String`

              - `List<BetaContentBlockSourceContent>`

                - `class BetaTextBlockParam:`

                  - `text: String`

                  - `type: JsonValue; "text"constant`

                    - `TEXT("text")`

                  - `cacheControl: Optional<BetaCacheControlEphemeral>`

                    Create a cache control breakpoint at this content block.

                    - `type: JsonValue; "ephemeral"constant`

                      - `EPHEMERAL("ephemeral")`

                    - `ttl: Optional<Ttl>`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `TTL_5M("5m")`

                      - `TTL_1H("1h")`

                  - `citations: Optional<List<BetaTextCitationParam>>`

                    - `class BetaCitationCharLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endCharIndex: Long`

                      - `startCharIndex: Long`

                      - `type: JsonValue; "char_location"constant`

                        - `CHAR_LOCATION("char_location")`

                    - `class BetaCitationPageLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endPageNumber: Long`

                      - `startPageNumber: Long`

                      - `type: JsonValue; "page_location"constant`

                        - `PAGE_LOCATION("page_location")`

                    - `class BetaCitationContentBlockLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endBlockIndex: Long`

                      - `startBlockIndex: Long`

                      - `type: JsonValue; "content_block_location"constant`

                        - `CONTENT_BLOCK_LOCATION("content_block_location")`

                    - `class BetaCitationWebSearchResultLocationParam:`

                      - `citedText: String`

                      - `encryptedIndex: String`

                      - `title: Optional<String>`

                      - `type: JsonValue; "web_search_result_location"constant`

                        - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                      - `url: String`

                    - `class BetaCitationSearchResultLocationParam:`

                      - `citedText: String`

                      - `endBlockIndex: Long`

                      - `searchResultIndex: Long`

                      - `source: String`

                      - `startBlockIndex: Long`

                      - `title: Optional<String>`

                      - `type: JsonValue; "search_result_location"constant`

                        - `SEARCH_RESULT_LOCATION("search_result_location")`

                - `class BetaImageBlockParam:`

                  - `source: Source`

                    - `class BetaBase64ImageSource:`

                      - `data: String`

                      - `mediaType: MediaType`

                        - `IMAGE_JPEG("image/jpeg")`

                        - `IMAGE_PNG("image/png")`

                        - `IMAGE_GIF("image/gif")`

                        - `IMAGE_WEBP("image/webp")`

                      - `type: JsonValue; "base64"constant`

                        - `BASE64("base64")`

                    - `class BetaUrlImageSource:`

                      - `type: JsonValue; "url"constant`

                        - `URL("url")`

                      - `url: String`

                    - `class BetaFileImageSource:`

                      - `fileId: String`

                      - `type: JsonValue; "file"constant`

                        - `FILE("file")`

                  - `type: JsonValue; "image"constant`

                    - `IMAGE("image")`

                  - `cacheControl: Optional<BetaCacheControlEphemeral>`

                    Create a cache control breakpoint at this content block.

                    - `type: JsonValue; "ephemeral"constant`

                      - `EPHEMERAL("ephemeral")`

                    - `ttl: Optional<Ttl>`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `TTL_5M("5m")`

                      - `TTL_1H("1h")`

            - `type: JsonValue; "content"constant`

              - `CONTENT("content")`

          - `class BetaUrlPdfSource:`

            - `type: JsonValue; "url"constant`

              - `URL("url")`

            - `url: String`

          - `class BetaFileDocumentSource:`

            - `fileId: String`

            - `type: JsonValue; "file"constant`

              - `FILE("file")`

        - `type: JsonValue; "document"constant`

          - `DOCUMENT("document")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

        - `citations: Optional<BetaCitationsConfigParam>`

          - `enabled: Optional<Boolean>`

        - `context: Optional<String>`

        - `title: Optional<String>`

      - `class BetaSearchResultBlockParam:`

        - `content: List<BetaTextBlockParam>`

          - `text: String`

          - `type: JsonValue; "text"constant`

            - `TEXT("text")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<List<BetaTextCitationParam>>`

            - `class BetaCitationCharLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class BetaCitationPageLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class BetaCitationContentBlockLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class BetaCitationWebSearchResultLocationParam:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class BetaCitationSearchResultLocationParam:`

              - `citedText: String`

              - `endBlockIndex: Long`

              - `searchResultIndex: Long`

              - `source: String`

              - `startBlockIndex: Long`

              - `title: Optional<String>`

              - `type: JsonValue; "search_result_location"constant`

                - `SEARCH_RESULT_LOCATION("search_result_location")`

        - `source: String`

        - `title: String`

        - `type: JsonValue; "search_result"constant`

          - `SEARCH_RESULT("search_result")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

        - `citations: Optional<BetaCitationsConfigParam>`

          - `enabled: Optional<Boolean>`

      - `class BetaThinkingBlockParam:`

        - `signature: String`

        - `thinking: String`

        - `type: JsonValue; "thinking"constant`

          - `THINKING("thinking")`

      - `class BetaRedactedThinkingBlockParam:`

        - `data: String`

        - `type: JsonValue; "redacted_thinking"constant`

          - `REDACTED_THINKING("redacted_thinking")`

      - `class BetaToolUseBlockParam:`

        - `id: String`

        - `input: Input`

        - `name: String`

        - `type: JsonValue; "tool_use"constant`

          - `TOOL_USE("tool_use")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

        - `caller: Optional<Caller>`

          Tool invocation directly from the model.

          - `class BetaDirectCaller:`

            Tool invocation directly from the model.

            - `type: JsonValue; "direct"constant`

              - `DIRECT("direct")`

          - `class BetaServerToolCaller:`

            Tool invocation generated by a server-side tool.

            - `toolId: String`

            - `type: JsonValue; "code_execution_20250825"constant`

              - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `class BetaToolResultBlockParam:`

        - `toolUseId: String`

        - `type: JsonValue; "tool_result"constant`

          - `TOOL_RESULT("tool_result")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

        - `content: Optional<Content>`

          - `String`

          - `List<Block>`

            - `class BetaTextBlockParam:`

              - `text: String`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<List<BetaTextCitationParam>>`

                - `class BetaCitationCharLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endCharIndex: Long`

                  - `startCharIndex: Long`

                  - `type: JsonValue; "char_location"constant`

                    - `CHAR_LOCATION("char_location")`

                - `class BetaCitationPageLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endPageNumber: Long`

                  - `startPageNumber: Long`

                  - `type: JsonValue; "page_location"constant`

                    - `PAGE_LOCATION("page_location")`

                - `class BetaCitationContentBlockLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endBlockIndex: Long`

                  - `startBlockIndex: Long`

                  - `type: JsonValue; "content_block_location"constant`

                    - `CONTENT_BLOCK_LOCATION("content_block_location")`

                - `class BetaCitationWebSearchResultLocationParam:`

                  - `citedText: String`

                  - `encryptedIndex: String`

                  - `title: Optional<String>`

                  - `type: JsonValue; "web_search_result_location"constant`

                    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                  - `url: String`

                - `class BetaCitationSearchResultLocationParam:`

                  - `citedText: String`

                  - `endBlockIndex: Long`

                  - `searchResultIndex: Long`

                  - `source: String`

                  - `startBlockIndex: Long`

                  - `title: Optional<String>`

                  - `type: JsonValue; "search_result_location"constant`

                    - `SEARCH_RESULT_LOCATION("search_result_location")`

            - `class BetaImageBlockParam:`

              - `source: Source`

                - `class BetaBase64ImageSource:`

                  - `data: String`

                  - `mediaType: MediaType`

                    - `IMAGE_JPEG("image/jpeg")`

                    - `IMAGE_PNG("image/png")`

                    - `IMAGE_GIF("image/gif")`

                    - `IMAGE_WEBP("image/webp")`

                  - `type: JsonValue; "base64"constant`

                    - `BASE64("base64")`

                - `class BetaUrlImageSource:`

                  - `type: JsonValue; "url"constant`

                    - `URL("url")`

                  - `url: String`

                - `class BetaFileImageSource:`

                  - `fileId: String`

                  - `type: JsonValue; "file"constant`

                    - `FILE("file")`

              - `type: JsonValue; "image"constant`

                - `IMAGE("image")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

            - `class BetaSearchResultBlockParam:`

              - `content: List<BetaTextBlockParam>`

                - `text: String`

                - `type: JsonValue; "text"constant`

                  - `TEXT("text")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `citations: Optional<List<BetaTextCitationParam>>`

                  - `class BetaCitationCharLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endCharIndex: Long`

                    - `startCharIndex: Long`

                    - `type: JsonValue; "char_location"constant`

                      - `CHAR_LOCATION("char_location")`

                  - `class BetaCitationPageLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endPageNumber: Long`

                    - `startPageNumber: Long`

                    - `type: JsonValue; "page_location"constant`

                      - `PAGE_LOCATION("page_location")`

                  - `class BetaCitationContentBlockLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endBlockIndex: Long`

                    - `startBlockIndex: Long`

                    - `type: JsonValue; "content_block_location"constant`

                      - `CONTENT_BLOCK_LOCATION("content_block_location")`

                  - `class BetaCitationWebSearchResultLocationParam:`

                    - `citedText: String`

                    - `encryptedIndex: String`

                    - `title: Optional<String>`

                    - `type: JsonValue; "web_search_result_location"constant`

                      - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                    - `url: String`

                  - `class BetaCitationSearchResultLocationParam:`

                    - `citedText: String`

                    - `endBlockIndex: Long`

                    - `searchResultIndex: Long`

                    - `source: String`

                    - `startBlockIndex: Long`

                    - `title: Optional<String>`

                    - `type: JsonValue; "search_result_location"constant`

                      - `SEARCH_RESULT_LOCATION("search_result_location")`

              - `source: String`

              - `title: String`

              - `type: JsonValue; "search_result"constant`

                - `SEARCH_RESULT("search_result")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<BetaCitationsConfigParam>`

                - `enabled: Optional<Boolean>`

            - `class BetaRequestDocumentBlock:`

              - `source: Source`

                - `class BetaBase64PdfSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "application/pdf"constant`

                    - `APPLICATION_PDF("application/pdf")`

                  - `type: JsonValue; "base64"constant`

                    - `BASE64("base64")`

                - `class BetaPlainTextSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "text/plain"constant`

                    - `TEXT_PLAIN("text/plain")`

                  - `type: JsonValue; "text"constant`

                    - `TEXT("text")`

                - `class BetaContentBlockSource:`

                  - `content: Content`

                    - `String`

                    - `List<BetaContentBlockSourceContent>`

                      - `class BetaTextBlockParam:`

                        - `text: String`

                        - `type: JsonValue; "text"constant`

                          - `TEXT("text")`

                        - `cacheControl: Optional<BetaCacheControlEphemeral>`

                          Create a cache control breakpoint at this content block.

                          - `type: JsonValue; "ephemeral"constant`

                            - `EPHEMERAL("ephemeral")`

                          - `ttl: Optional<Ttl>`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `TTL_5M("5m")`

                            - `TTL_1H("1h")`

                        - `citations: Optional<List<BetaTextCitationParam>>`

                          - `class BetaCitationCharLocationParam:`

                            - `citedText: String`

                            - `documentIndex: Long`

                            - `documentTitle: Optional<String>`

                            - `endCharIndex: Long`

                            - `startCharIndex: Long`

                            - `type: JsonValue; "char_location"constant`

                              - `CHAR_LOCATION("char_location")`

                          - `class BetaCitationPageLocationParam:`

                            - `citedText: String`

                            - `documentIndex: Long`

                            - `documentTitle: Optional<String>`

                            - `endPageNumber: Long`

                            - `startPageNumber: Long`

                            - `type: JsonValue; "page_location"constant`

                              - `PAGE_LOCATION("page_location")`

                          - `class BetaCitationContentBlockLocationParam:`

                            - `citedText: String`

                            - `documentIndex: Long`

                            - `documentTitle: Optional<String>`

                            - `endBlockIndex: Long`

                            - `startBlockIndex: Long`

                            - `type: JsonValue; "content_block_location"constant`

                              - `CONTENT_BLOCK_LOCATION("content_block_location")`

                          - `class BetaCitationWebSearchResultLocationParam:`

                            - `citedText: String`

                            - `encryptedIndex: String`

                            - `title: Optional<String>`

                            - `type: JsonValue; "web_search_result_location"constant`

                              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                            - `url: String`

                          - `class BetaCitationSearchResultLocationParam:`

                            - `citedText: String`

                            - `endBlockIndex: Long`

                            - `searchResultIndex: Long`

                            - `source: String`

                            - `startBlockIndex: Long`

                            - `title: Optional<String>`

                            - `type: JsonValue; "search_result_location"constant`

                              - `SEARCH_RESULT_LOCATION("search_result_location")`

                      - `class BetaImageBlockParam:`

                        - `source: Source`

                          - `class BetaBase64ImageSource:`

                            - `data: String`

                            - `mediaType: MediaType`

                              - `IMAGE_JPEG("image/jpeg")`

                              - `IMAGE_PNG("image/png")`

                              - `IMAGE_GIF("image/gif")`

                              - `IMAGE_WEBP("image/webp")`

                            - `type: JsonValue; "base64"constant`

                              - `BASE64("base64")`

                          - `class BetaUrlImageSource:`

                            - `type: JsonValue; "url"constant`

                              - `URL("url")`

                            - `url: String`

                          - `class BetaFileImageSource:`

                            - `fileId: String`

                            - `type: JsonValue; "file"constant`

                              - `FILE("file")`

                        - `type: JsonValue; "image"constant`

                          - `IMAGE("image")`

                        - `cacheControl: Optional<BetaCacheControlEphemeral>`

                          Create a cache control breakpoint at this content block.

                          - `type: JsonValue; "ephemeral"constant`

                            - `EPHEMERAL("ephemeral")`

                          - `ttl: Optional<Ttl>`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `TTL_5M("5m")`

                            - `TTL_1H("1h")`

                  - `type: JsonValue; "content"constant`

                    - `CONTENT("content")`

                - `class BetaUrlPdfSource:`

                  - `type: JsonValue; "url"constant`

                    - `URL("url")`

                  - `url: String`

                - `class BetaFileDocumentSource:`

                  - `fileId: String`

                  - `type: JsonValue; "file"constant`

                    - `FILE("file")`

              - `type: JsonValue; "document"constant`

                - `DOCUMENT("document")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<BetaCitationsConfigParam>`

                - `enabled: Optional<Boolean>`

              - `context: Optional<String>`

              - `title: Optional<String>`

            - `class BetaToolReferenceBlockParam:`

              Tool reference block that can be included in tool_result content.

              - `toolName: String`

              - `type: JsonValue; "tool_reference"constant`

                - `TOOL_REFERENCE("tool_reference")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

        - `isError: Optional<Boolean>`

      - `class BetaServerToolUseBlockParam:`

        - `id: String`

        - `input: Input`

        - `name: Name`

          - `WEB_SEARCH("web_search")`

          - `WEB_FETCH("web_fetch")`

          - `CODE_EXECUTION("code_execution")`

          - `BASH_CODE_EXECUTION("bash_code_execution")`

          - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

          - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

          - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

        - `type: JsonValue; "server_tool_use"constant`

          - `SERVER_TOOL_USE("server_tool_use")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

        - `caller: Optional<Caller>`

          Tool invocation directly from the model.

          - `class BetaDirectCaller:`

            Tool invocation directly from the model.

            - `type: JsonValue; "direct"constant`

              - `DIRECT("direct")`

          - `class BetaServerToolCaller:`

            Tool invocation generated by a server-side tool.

            - `toolId: String`

            - `type: JsonValue; "code_execution_20250825"constant`

              - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `class BetaWebSearchToolResultBlockParam:`

        - `content: BetaWebSearchToolResultBlockParamContent`

          - `List<BetaWebSearchResultBlockParam>`

            - `encryptedContent: String`

            - `title: String`

            - `type: JsonValue; "web_search_result"constant`

              - `WEB_SEARCH_RESULT("web_search_result")`

            - `url: String`

            - `pageAge: Optional<String>`

          - `class BetaWebSearchToolRequestError:`

            - `errorCode: BetaWebSearchToolResultErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `MAX_USES_EXCEEDED("max_uses_exceeded")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `QUERY_TOO_LONG("query_too_long")`

            - `type: JsonValue; "web_search_tool_result_error"constant`

              - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

        - `toolUseId: String`

        - `type: JsonValue; "web_search_tool_result"constant`

          - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

      - `class BetaWebFetchToolResultBlockParam:`

        - `content: Content`

          - `class BetaWebFetchToolResultErrorBlockParam:`

            - `errorCode: BetaWebFetchToolResultErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `URL_TOO_LONG("url_too_long")`

              - `URL_NOT_ALLOWED("url_not_allowed")`

              - `URL_NOT_ACCESSIBLE("url_not_accessible")`

              - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `MAX_USES_EXCEEDED("max_uses_exceeded")`

              - `UNAVAILABLE("unavailable")`

            - `type: JsonValue; "web_fetch_tool_result_error"constant`

              - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

          - `class BetaWebFetchBlockParam:`

            - `content: BetaRequestDocumentBlock`

              - `source: Source`

                - `class BetaBase64PdfSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "application/pdf"constant`

                    - `APPLICATION_PDF("application/pdf")`

                  - `type: JsonValue; "base64"constant`

                    - `BASE64("base64")`

                - `class BetaPlainTextSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "text/plain"constant`

                    - `TEXT_PLAIN("text/plain")`

                  - `type: JsonValue; "text"constant`

                    - `TEXT("text")`

                - `class BetaContentBlockSource:`

                  - `content: Content`

                    - `String`

                    - `List<BetaContentBlockSourceContent>`

                      - `class BetaTextBlockParam:`

                        - `text: String`

                        - `type: JsonValue; "text"constant`

                          - `TEXT("text")`

                        - `cacheControl: Optional<BetaCacheControlEphemeral>`

                          Create a cache control breakpoint at this content block.

                          - `type: JsonValue; "ephemeral"constant`

                            - `EPHEMERAL("ephemeral")`

                          - `ttl: Optional<Ttl>`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `TTL_5M("5m")`

                            - `TTL_1H("1h")`

                        - `citations: Optional<List<BetaTextCitationParam>>`

                          - `class BetaCitationCharLocationParam:`

                            - `citedText: String`

                            - `documentIndex: Long`

                            - `documentTitle: Optional<String>`

                            - `endCharIndex: Long`

                            - `startCharIndex: Long`

                            - `type: JsonValue; "char_location"constant`

                              - `CHAR_LOCATION("char_location")`

                          - `class BetaCitationPageLocationParam:`

                            - `citedText: String`

                            - `documentIndex: Long`

                            - `documentTitle: Optional<String>`

                            - `endPageNumber: Long`

                            - `startPageNumber: Long`

                            - `type: JsonValue; "page_location"constant`

                              - `PAGE_LOCATION("page_location")`

                          - `class BetaCitationContentBlockLocationParam:`

                            - `citedText: String`

                            - `documentIndex: Long`

                            - `documentTitle: Optional<String>`

                            - `endBlockIndex: Long`

                            - `startBlockIndex: Long`

                            - `type: JsonValue; "content_block_location"constant`

                              - `CONTENT_BLOCK_LOCATION("content_block_location")`

                          - `class BetaCitationWebSearchResultLocationParam:`

                            - `citedText: String`

                            - `encryptedIndex: String`

                            - `title: Optional<String>`

                            - `type: JsonValue; "web_search_result_location"constant`

                              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                            - `url: String`

                          - `class BetaCitationSearchResultLocationParam:`

                            - `citedText: String`

                            - `endBlockIndex: Long`

                            - `searchResultIndex: Long`

                            - `source: String`

                            - `startBlockIndex: Long`

                            - `title: Optional<String>`

                            - `type: JsonValue; "search_result_location"constant`

                              - `SEARCH_RESULT_LOCATION("search_result_location")`

                      - `class BetaImageBlockParam:`

                        - `source: Source`

                          - `class BetaBase64ImageSource:`

                            - `data: String`

                            - `mediaType: MediaType`

                              - `IMAGE_JPEG("image/jpeg")`

                              - `IMAGE_PNG("image/png")`

                              - `IMAGE_GIF("image/gif")`

                              - `IMAGE_WEBP("image/webp")`

                            - `type: JsonValue; "base64"constant`

                              - `BASE64("base64")`

                          - `class BetaUrlImageSource:`

                            - `type: JsonValue; "url"constant`

                              - `URL("url")`

                            - `url: String`

                          - `class BetaFileImageSource:`

                            - `fileId: String`

                            - `type: JsonValue; "file"constant`

                              - `FILE("file")`

                        - `type: JsonValue; "image"constant`

                          - `IMAGE("image")`

                        - `cacheControl: Optional<BetaCacheControlEphemeral>`

                          Create a cache control breakpoint at this content block.

                          - `type: JsonValue; "ephemeral"constant`

                            - `EPHEMERAL("ephemeral")`

                          - `ttl: Optional<Ttl>`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `TTL_5M("5m")`

                            - `TTL_1H("1h")`

                  - `type: JsonValue; "content"constant`

                    - `CONTENT("content")`

                - `class BetaUrlPdfSource:`

                  - `type: JsonValue; "url"constant`

                    - `URL("url")`

                  - `url: String`

                - `class BetaFileDocumentSource:`

                  - `fileId: String`

                  - `type: JsonValue; "file"constant`

                    - `FILE("file")`

              - `type: JsonValue; "document"constant`

                - `DOCUMENT("document")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<BetaCitationsConfigParam>`

                - `enabled: Optional<Boolean>`

              - `context: Optional<String>`

              - `title: Optional<String>`

            - `type: JsonValue; "web_fetch_result"constant`

              - `WEB_FETCH_RESULT("web_fetch_result")`

            - `url: String`

              Fetched content URL

            - `retrievedAt: Optional<String>`

              ISO 8601 timestamp when the content was retrieved

        - `toolUseId: String`

        - `type: JsonValue; "web_fetch_tool_result"constant`

          - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

      - `class BetaCodeExecutionToolResultBlockParam:`

        - `content: BetaCodeExecutionToolResultBlockParamContent`

          - `class BetaCodeExecutionToolResultErrorParam:`

            - `errorCode: BetaCodeExecutionToolResultErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `type: JsonValue; "code_execution_tool_result_error"constant`

              - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

          - `class BetaCodeExecutionResultBlockParam:`

            - `content: List<BetaCodeExecutionOutputBlockParam>`

              - `fileId: String`

              - `type: JsonValue; "code_execution_output"constant`

                - `CODE_EXECUTION_OUTPUT("code_execution_output")`

            - `returnCode: Long`

            - `stderr: String`

            - `stdout: String`

            - `type: JsonValue; "code_execution_result"constant`

              - `CODE_EXECUTION_RESULT("code_execution_result")`

        - `toolUseId: String`

        - `type: JsonValue; "code_execution_tool_result"constant`

          - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

      - `class BetaBashCodeExecutionToolResultBlockParam:`

        - `content: Content`

          - `class BetaBashCodeExecutionToolResultErrorParam:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

            - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

              - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

          - `class BetaBashCodeExecutionResultBlockParam:`

            - `content: List<BetaBashCodeExecutionOutputBlockParam>`

              - `fileId: String`

              - `type: JsonValue; "bash_code_execution_output"constant`

                - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

            - `returnCode: Long`

            - `stderr: String`

            - `stdout: String`

            - `type: JsonValue; "bash_code_execution_result"constant`

              - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

        - `toolUseId: String`

        - `type: JsonValue; "bash_code_execution_tool_result"constant`

          - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

      - `class BetaTextEditorCodeExecutionToolResultBlockParam:`

        - `content: Content`

          - `class BetaTextEditorCodeExecutionToolResultErrorParam:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `FILE_NOT_FOUND("file_not_found")`

            - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

            - `errorMessage: Optional<String>`

          - `class BetaTextEditorCodeExecutionViewResultBlockParam:`

            - `content: String`

            - `fileType: FileType`

              - `TEXT("text")`

              - `IMAGE("image")`

              - `PDF("pdf")`

            - `type: JsonValue; "text_editor_code_execution_view_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

            - `numLines: Optional<Long>`

            - `startLine: Optional<Long>`

            - `totalLines: Optional<Long>`

          - `class BetaTextEditorCodeExecutionCreateResultBlockParam:`

            - `isFileUpdate: Boolean`

            - `type: JsonValue; "text_editor_code_execution_create_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

          - `class BetaTextEditorCodeExecutionStrReplaceResultBlockParam:`

            - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

            - `lines: Optional<List<String>>`

            - `newLines: Optional<Long>`

            - `newStart: Optional<Long>`

            - `oldLines: Optional<Long>`

            - `oldStart: Optional<Long>`

        - `toolUseId: String`

        - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

          - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

      - `class BetaToolSearchToolResultBlockParam:`

        - `content: Content`

          - `class BetaToolSearchToolResultErrorParam:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `type: JsonValue; "tool_search_tool_result_error"constant`

              - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

          - `class BetaToolSearchToolSearchResultBlockParam:`

            - `toolReferences: List<BetaToolReferenceBlockParam>`

              - `toolName: String`

              - `type: JsonValue; "tool_reference"constant`

                - `TOOL_REFERENCE("tool_reference")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

            - `type: JsonValue; "tool_search_tool_search_result"constant`

              - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

        - `toolUseId: String`

        - `type: JsonValue; "tool_search_tool_result"constant`

          - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

      - `class BetaMcpToolUseBlockParam:`

        - `id: String`

        - `input: Input`

        - `name: String`

        - `serverName: String`

          The name of the MCP server

        - `type: JsonValue; "mcp_tool_use"constant`

          - `MCP_TOOL_USE("mcp_tool_use")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

      - `class BetaRequestMcpToolResultBlockParam:`

        - `toolUseId: String`

        - `type: JsonValue; "mcp_tool_result"constant`

          - `MCP_TOOL_RESULT("mcp_tool_result")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

        - `content: Optional<Content>`

          - `String`

          - `List<BetaTextBlockParam>`

            - `text: String`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

            - `cacheControl: Optional<BetaCacheControlEphemeral>`

              Create a cache control breakpoint at this content block.

              - `type: JsonValue; "ephemeral"constant`

                - `EPHEMERAL("ephemeral")`

              - `ttl: Optional<Ttl>`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `TTL_5M("5m")`

                - `TTL_1H("1h")`

            - `citations: Optional<List<BetaTextCitationParam>>`

              - `class BetaCitationCharLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endCharIndex: Long`

                - `startCharIndex: Long`

                - `type: JsonValue; "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class BetaCitationPageLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endPageNumber: Long`

                - `startPageNumber: Long`

                - `type: JsonValue; "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class BetaCitationContentBlockLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endBlockIndex: Long`

                - `startBlockIndex: Long`

                - `type: JsonValue; "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class BetaCitationWebSearchResultLocationParam:`

                - `citedText: String`

                - `encryptedIndex: String`

                - `title: Optional<String>`

                - `type: JsonValue; "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `url: String`

              - `class BetaCitationSearchResultLocationParam:`

                - `citedText: String`

                - `endBlockIndex: Long`

                - `searchResultIndex: Long`

                - `source: String`

                - `startBlockIndex: Long`

                - `title: Optional<String>`

                - `type: JsonValue; "search_result_location"constant`

                  - `SEARCH_RESULT_LOCATION("search_result_location")`

        - `isError: Optional<Boolean>`

      - `class BetaContainerUploadBlockParam:`

        A content block that represents a file to be uploaded to the container
        Files uploaded via this block will be available in the container's input directory.

        - `fileId: String`

        - `type: JsonValue; "container_upload"constant`

          - `CONTAINER_UPLOAD("container_upload")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

  - `role: Role`

    - `USER("user")`

    - `ASSISTANT("assistant")`

### Beta Message Tokens Count

- `class BetaMessageTokensCount:`

  - `contextManagement: Optional<BetaCountTokensContextManagementResponse>`

    Information about context management applied to the message.

    - `originalInputTokens: Long`

      The original token count before context management was applied

  - `inputTokens: Long`

    The total number of tokens across the provided list of messages, system prompt, and tools.

### Beta Metadata

- `class BetaMetadata:`

  - `userId: Optional<String>`

    An external identifier for the user who is associated with the request.

    This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

### Beta Output Config

- `class BetaOutputConfig:`

  - `effort: Optional<Effort>`

    All possible effort levels.

    - `LOW("low")`

    - `MEDIUM("medium")`

    - `HIGH("high")`

### Beta Plain Text Source

- `class BetaPlainTextSource:`

  - `data: String`

  - `mediaType: JsonValue; "text/plain"constant`

    - `TEXT_PLAIN("text/plain")`

  - `type: JsonValue; "text"constant`

    - `TEXT("text")`

### Beta Raw Content Block Delta

- `class BetaRawContentBlockDelta: A class that can be one of several variants.union`

  - `class BetaTextDelta:`

    - `text: String`

    - `type: JsonValue; "text_delta"constant`

      - `TEXT_DELTA("text_delta")`

  - `class BetaInputJsonDelta:`

    - `partialJson: String`

    - `type: JsonValue; "input_json_delta"constant`

      - `INPUT_JSON_DELTA("input_json_delta")`

  - `class BetaCitationsDelta:`

    - `citation: Citation`

      - `class BetaCitationCharLocation:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endCharIndex: Long`

        - `fileId: Optional<String>`

        - `startCharIndex: Long`

        - `type: JsonValue; "char_location"constant`

          - `CHAR_LOCATION("char_location")`

      - `class BetaCitationPageLocation:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endPageNumber: Long`

        - `fileId: Optional<String>`

        - `startPageNumber: Long`

        - `type: JsonValue; "page_location"constant`

          - `PAGE_LOCATION("page_location")`

      - `class BetaCitationContentBlockLocation:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endBlockIndex: Long`

        - `fileId: Optional<String>`

        - `startBlockIndex: Long`

        - `type: JsonValue; "content_block_location"constant`

          - `CONTENT_BLOCK_LOCATION("content_block_location")`

      - `class BetaCitationsWebSearchResultLocation:`

        - `citedText: String`

        - `encryptedIndex: String`

        - `title: Optional<String>`

        - `type: JsonValue; "web_search_result_location"constant`

          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

        - `url: String`

      - `class BetaCitationSearchResultLocation:`

        - `citedText: String`

        - `endBlockIndex: Long`

        - `searchResultIndex: Long`

        - `source: String`

        - `startBlockIndex: Long`

        - `title: Optional<String>`

        - `type: JsonValue; "search_result_location"constant`

          - `SEARCH_RESULT_LOCATION("search_result_location")`

    - `type: JsonValue; "citations_delta"constant`

      - `CITATIONS_DELTA("citations_delta")`

  - `class BetaThinkingDelta:`

    - `thinking: String`

    - `type: JsonValue; "thinking_delta"constant`

      - `THINKING_DELTA("thinking_delta")`

  - `class BetaSignatureDelta:`

    - `signature: String`

    - `type: JsonValue; "signature_delta"constant`

      - `SIGNATURE_DELTA("signature_delta")`

### Beta Raw Content Block Delta Event

- `class BetaRawContentBlockDeltaEvent:`

  - `delta: BetaRawContentBlockDelta`

    - `class BetaTextDelta:`

      - `text: String`

      - `type: JsonValue; "text_delta"constant`

        - `TEXT_DELTA("text_delta")`

    - `class BetaInputJsonDelta:`

      - `partialJson: String`

      - `type: JsonValue; "input_json_delta"constant`

        - `INPUT_JSON_DELTA("input_json_delta")`

    - `class BetaCitationsDelta:`

      - `citation: Citation`

        - `class BetaCitationCharLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endCharIndex: Long`

          - `fileId: Optional<String>`

          - `startCharIndex: Long`

          - `type: JsonValue; "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class BetaCitationPageLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endPageNumber: Long`

          - `fileId: Optional<String>`

          - `startPageNumber: Long`

          - `type: JsonValue; "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class BetaCitationContentBlockLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endBlockIndex: Long`

          - `fileId: Optional<String>`

          - `startBlockIndex: Long`

          - `type: JsonValue; "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class BetaCitationsWebSearchResultLocation:`

          - `citedText: String`

          - `encryptedIndex: String`

          - `title: Optional<String>`

          - `type: JsonValue; "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `url: String`

        - `class BetaCitationSearchResultLocation:`

          - `citedText: String`

          - `endBlockIndex: Long`

          - `searchResultIndex: Long`

          - `source: String`

          - `startBlockIndex: Long`

          - `title: Optional<String>`

          - `type: JsonValue; "search_result_location"constant`

            - `SEARCH_RESULT_LOCATION("search_result_location")`

      - `type: JsonValue; "citations_delta"constant`

        - `CITATIONS_DELTA("citations_delta")`

    - `class BetaThinkingDelta:`

      - `thinking: String`

      - `type: JsonValue; "thinking_delta"constant`

        - `THINKING_DELTA("thinking_delta")`

    - `class BetaSignatureDelta:`

      - `signature: String`

      - `type: JsonValue; "signature_delta"constant`

        - `SIGNATURE_DELTA("signature_delta")`

  - `index: Long`

  - `type: JsonValue; "content_block_delta"constant`

    - `CONTENT_BLOCK_DELTA("content_block_delta")`

### Beta Raw Content Block Start Event

- `class BetaRawContentBlockStartEvent:`

  - `contentBlock: ContentBlock`

    Response model for a file uploaded to the container.

    - `class BetaTextBlock:`

      - `citations: Optional<List<BetaTextCitation>>`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `class BetaCitationCharLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endCharIndex: Long`

          - `fileId: Optional<String>`

          - `startCharIndex: Long`

          - `type: JsonValue; "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class BetaCitationPageLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endPageNumber: Long`

          - `fileId: Optional<String>`

          - `startPageNumber: Long`

          - `type: JsonValue; "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class BetaCitationContentBlockLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endBlockIndex: Long`

          - `fileId: Optional<String>`

          - `startBlockIndex: Long`

          - `type: JsonValue; "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class BetaCitationsWebSearchResultLocation:`

          - `citedText: String`

          - `encryptedIndex: String`

          - `title: Optional<String>`

          - `type: JsonValue; "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `url: String`

        - `class BetaCitationSearchResultLocation:`

          - `citedText: String`

          - `endBlockIndex: Long`

          - `searchResultIndex: Long`

          - `source: String`

          - `startBlockIndex: Long`

          - `title: Optional<String>`

          - `type: JsonValue; "search_result_location"constant`

            - `SEARCH_RESULT_LOCATION("search_result_location")`

      - `text: String`

      - `type: JsonValue; "text"constant`

        - `TEXT("text")`

    - `class BetaThinkingBlock:`

      - `signature: String`

      - `thinking: String`

      - `type: JsonValue; "thinking"constant`

        - `THINKING("thinking")`

    - `class BetaRedactedThinkingBlock:`

      - `data: String`

      - `type: JsonValue; "redacted_thinking"constant`

        - `REDACTED_THINKING("redacted_thinking")`

    - `class BetaToolUseBlock:`

      - `id: String`

      - `input: Input`

      - `name: String`

      - `type: JsonValue; "tool_use"constant`

        - `TOOL_USE("tool_use")`

      - `caller: Optional<Caller>`

        Tool invocation directly from the model.

        - `class BetaDirectCaller:`

          Tool invocation directly from the model.

          - `type: JsonValue; "direct"constant`

            - `DIRECT("direct")`

        - `class BetaServerToolCaller:`

          Tool invocation generated by a server-side tool.

          - `toolId: String`

          - `type: JsonValue; "code_execution_20250825"constant`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `class BetaServerToolUseBlock:`

      - `id: String`

      - `caller: Caller`

        Tool invocation directly from the model.

        - `class BetaDirectCaller:`

          Tool invocation directly from the model.

          - `type: JsonValue; "direct"constant`

            - `DIRECT("direct")`

        - `class BetaServerToolCaller:`

          Tool invocation generated by a server-side tool.

          - `toolId: String`

          - `type: JsonValue; "code_execution_20250825"constant`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `input: Input`

      - `name: Name`

        - `WEB_SEARCH("web_search")`

        - `WEB_FETCH("web_fetch")`

        - `CODE_EXECUTION("code_execution")`

        - `BASH_CODE_EXECUTION("bash_code_execution")`

        - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

        - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

        - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

      - `type: JsonValue; "server_tool_use"constant`

        - `SERVER_TOOL_USE("server_tool_use")`

    - `class BetaWebSearchToolResultBlock:`

      - `content: BetaWebSearchToolResultBlockContent`

        - `class BetaWebSearchToolResultError:`

          - `errorCode: BetaWebSearchToolResultErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `MAX_USES_EXCEEDED("max_uses_exceeded")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `QUERY_TOO_LONG("query_too_long")`

          - `type: JsonValue; "web_search_tool_result_error"constant`

            - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

        - `List<BetaWebSearchResultBlock>`

          - `encryptedContent: String`

          - `pageAge: Optional<String>`

          - `title: String`

          - `type: JsonValue; "web_search_result"constant`

            - `WEB_SEARCH_RESULT("web_search_result")`

          - `url: String`

      - `toolUseId: String`

      - `type: JsonValue; "web_search_tool_result"constant`

        - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

    - `class BetaWebFetchToolResultBlock:`

      - `content: Content`

        - `class BetaWebFetchToolResultErrorBlock:`

          - `errorCode: BetaWebFetchToolResultErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `URL_TOO_LONG("url_too_long")`

            - `URL_NOT_ALLOWED("url_not_allowed")`

            - `URL_NOT_ACCESSIBLE("url_not_accessible")`

            - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `MAX_USES_EXCEEDED("max_uses_exceeded")`

            - `UNAVAILABLE("unavailable")`

          - `type: JsonValue; "web_fetch_tool_result_error"constant`

            - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

        - `class BetaWebFetchBlock:`

          - `content: BetaDocumentBlock`

            - `citations: Optional<BetaCitationConfig>`

              Citation configuration for the document

              - `enabled: Boolean`

            - `source: Source`

              - `class BetaBase64PdfSource:`

                - `data: String`

                - `mediaType: JsonValue; "application/pdf"constant`

                  - `APPLICATION_PDF("application/pdf")`

                - `type: JsonValue; "base64"constant`

                  - `BASE64("base64")`

              - `class BetaPlainTextSource:`

                - `data: String`

                - `mediaType: JsonValue; "text/plain"constant`

                  - `TEXT_PLAIN("text/plain")`

                - `type: JsonValue; "text"constant`

                  - `TEXT("text")`

            - `title: Optional<String>`

              The title of the document

            - `type: JsonValue; "document"constant`

              - `DOCUMENT("document")`

          - `retrievedAt: Optional<String>`

            ISO 8601 timestamp when the content was retrieved

          - `type: JsonValue; "web_fetch_result"constant`

            - `WEB_FETCH_RESULT("web_fetch_result")`

          - `url: String`

            Fetched content URL

      - `toolUseId: String`

      - `type: JsonValue; "web_fetch_tool_result"constant`

        - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

    - `class BetaCodeExecutionToolResultBlock:`

      - `content: BetaCodeExecutionToolResultBlockContent`

        - `class BetaCodeExecutionToolResultError:`

          - `errorCode: BetaCodeExecutionToolResultErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

          - `type: JsonValue; "code_execution_tool_result_error"constant`

            - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

        - `class BetaCodeExecutionResultBlock:`

          - `content: List<BetaCodeExecutionOutputBlock>`

            - `fileId: String`

            - `type: JsonValue; "code_execution_output"constant`

              - `CODE_EXECUTION_OUTPUT("code_execution_output")`

          - `returnCode: Long`

          - `stderr: String`

          - `stdout: String`

          - `type: JsonValue; "code_execution_result"constant`

            - `CODE_EXECUTION_RESULT("code_execution_result")`

      - `toolUseId: String`

      - `type: JsonValue; "code_execution_tool_result"constant`

        - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

    - `class BetaBashCodeExecutionToolResultBlock:`

      - `content: Content`

        - `class BetaBashCodeExecutionToolResultError:`

          - `errorCode: ErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

          - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

            - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

        - `class BetaBashCodeExecutionResultBlock:`

          - `content: List<BetaBashCodeExecutionOutputBlock>`

            - `fileId: String`

            - `type: JsonValue; "bash_code_execution_output"constant`

              - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

          - `returnCode: Long`

          - `stderr: String`

          - `stdout: String`

          - `type: JsonValue; "bash_code_execution_result"constant`

            - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

      - `toolUseId: String`

      - `type: JsonValue; "bash_code_execution_tool_result"constant`

        - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

    - `class BetaTextEditorCodeExecutionToolResultBlock:`

      - `content: Content`

        - `class BetaTextEditorCodeExecutionToolResultError:`

          - `errorCode: ErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `FILE_NOT_FOUND("file_not_found")`

          - `errorMessage: Optional<String>`

          - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

        - `class BetaTextEditorCodeExecutionViewResultBlock:`

          - `content: String`

          - `fileType: FileType`

            - `TEXT("text")`

            - `IMAGE("image")`

            - `PDF("pdf")`

          - `numLines: Optional<Long>`

          - `startLine: Optional<Long>`

          - `totalLines: Optional<Long>`

          - `type: JsonValue; "text_editor_code_execution_view_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

        - `class BetaTextEditorCodeExecutionCreateResultBlock:`

          - `isFileUpdate: Boolean`

          - `type: JsonValue; "text_editor_code_execution_create_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

        - `class BetaTextEditorCodeExecutionStrReplaceResultBlock:`

          - `lines: Optional<List<String>>`

          - `newLines: Optional<Long>`

          - `newStart: Optional<Long>`

          - `oldLines: Optional<Long>`

          - `oldStart: Optional<Long>`

          - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

      - `toolUseId: String`

      - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

        - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

    - `class BetaToolSearchToolResultBlock:`

      - `content: Content`

        - `class BetaToolSearchToolResultError:`

          - `errorCode: ErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

          - `errorMessage: Optional<String>`

          - `type: JsonValue; "tool_search_tool_result_error"constant`

            - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

        - `class BetaToolSearchToolSearchResultBlock:`

          - `toolReferences: List<BetaToolReferenceBlock>`

            - `toolName: String`

            - `type: JsonValue; "tool_reference"constant`

              - `TOOL_REFERENCE("tool_reference")`

          - `type: JsonValue; "tool_search_tool_search_result"constant`

            - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

      - `toolUseId: String`

      - `type: JsonValue; "tool_search_tool_result"constant`

        - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

    - `class BetaMcpToolUseBlock:`

      - `id: String`

      - `input: Input`

      - `name: String`

        The name of the MCP tool

      - `serverName: String`

        The name of the MCP server

      - `type: JsonValue; "mcp_tool_use"constant`

        - `MCP_TOOL_USE("mcp_tool_use")`

    - `class BetaMcpToolResultBlock:`

      - `content: Content`

        - `String`

        - `List<BetaTextBlock>`

          - `citations: Optional<List<BetaTextCitation>>`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `class BetaCitationCharLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `fileId: Optional<String>`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class BetaCitationPageLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `fileId: Optional<String>`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class BetaCitationContentBlockLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `fileId: Optional<String>`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class BetaCitationsWebSearchResultLocation:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class BetaCitationSearchResultLocation:`

              - `citedText: String`

              - `endBlockIndex: Long`

              - `searchResultIndex: Long`

              - `source: String`

              - `startBlockIndex: Long`

              - `title: Optional<String>`

              - `type: JsonValue; "search_result_location"constant`

                - `SEARCH_RESULT_LOCATION("search_result_location")`

          - `text: String`

          - `type: JsonValue; "text"constant`

            - `TEXT("text")`

      - `isError: Boolean`

      - `toolUseId: String`

      - `type: JsonValue; "mcp_tool_result"constant`

        - `MCP_TOOL_RESULT("mcp_tool_result")`

    - `class BetaContainerUploadBlock:`

      Response model for a file uploaded to the container.

      - `fileId: String`

      - `type: JsonValue; "container_upload"constant`

        - `CONTAINER_UPLOAD("container_upload")`

  - `index: Long`

  - `type: JsonValue; "content_block_start"constant`

    - `CONTENT_BLOCK_START("content_block_start")`

### Beta Raw Content Block Stop Event

- `class BetaRawContentBlockStopEvent:`

  - `index: Long`

  - `type: JsonValue; "content_block_stop"constant`

    - `CONTENT_BLOCK_STOP("content_block_stop")`

### Beta Raw Message Delta Event

- `class BetaRawMessageDeltaEvent:`

  - `contextManagement: Optional<BetaContextManagementResponse>`

    Information about context management strategies applied during the request

    - `appliedEdits: List<AppliedEdit>`

      List of context management edits that were applied.

      - `class BetaClearToolUses20250919EditResponse:`

        - `clearedInputTokens: Long`

          Number of input tokens cleared by this edit.

        - `clearedToolUses: Long`

          Number of tool uses that were cleared.

        - `type: JsonValue; "clear_tool_uses_20250919"constant`

          The type of context management edit applied.

          - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

      - `class BetaClearThinking20251015EditResponse:`

        - `clearedInputTokens: Long`

          Number of input tokens cleared by this edit.

        - `clearedThinkingTurns: Long`

          Number of thinking turns that were cleared.

        - `type: JsonValue; "clear_thinking_20251015"constant`

          The type of context management edit applied.

          - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

  - `delta: Delta`

    - `container: Optional<BetaContainer>`

      Information about the container used in the request (for the code execution tool)

      - `id: String`

        Identifier for the container used in this request

      - `expiresAt: LocalDateTime`

        The time at which the container will expire.

      - `skills: Optional<List<BetaSkill>>`

        Skills loaded in the container

        - `skillId: String`

          Skill ID

        - `type: Type`

          Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

          - `ANTHROPIC("anthropic")`

          - `CUSTOM("custom")`

        - `version: String`

          Skill version or 'latest' for most recent version

    - `stopReason: Optional<BetaStopReason>`

      - `END_TURN("end_turn")`

      - `MAX_TOKENS("max_tokens")`

      - `STOP_SEQUENCE("stop_sequence")`

      - `TOOL_USE("tool_use")`

      - `PAUSE_TURN("pause_turn")`

      - `REFUSAL("refusal")`

      - `MODEL_CONTEXT_WINDOW_EXCEEDED("model_context_window_exceeded")`

    - `stopSequence: Optional<String>`

  - `type: JsonValue; "message_delta"constant`

    - `MESSAGE_DELTA("message_delta")`

  - `usage: BetaMessageDeltaUsage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cacheCreationInputTokens: Optional<Long>`

      The cumulative number of input tokens used to create the cache entry.

    - `cacheReadInputTokens: Optional<Long>`

      The cumulative number of input tokens read from the cache.

    - `inputTokens: Optional<Long>`

      The cumulative number of input tokens which were used.

    - `outputTokens: Long`

      The cumulative number of output tokens which were used.

    - `serverToolUse: Optional<BetaServerToolUsage>`

      The number of server tool requests.

      - `webFetchRequests: Long`

        The number of web fetch tool requests.

      - `webSearchRequests: Long`

        The number of web search tool requests.

### Beta Raw Message Start Event

- `class BetaRawMessageStartEvent:`

  - `message: BetaMessage`

    - `id: String`

      Unique object identifier.

      The format and length of IDs may change over time.

    - `container: Optional<BetaContainer>`

      Information about the container used in the request (for the code execution tool)

      - `id: String`

        Identifier for the container used in this request

      - `expiresAt: LocalDateTime`

        The time at which the container will expire.

      - `skills: Optional<List<BetaSkill>>`

        Skills loaded in the container

        - `skillId: String`

          Skill ID

        - `type: Type`

          Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

          - `ANTHROPIC("anthropic")`

          - `CUSTOM("custom")`

        - `version: String`

          Skill version or 'latest' for most recent version

    - `content: List<BetaContentBlock>`

      Content generated by the model.

      This is an array of content blocks, each of which has a `type` that determines its shape.

      Example:

      ```json
      [{"type": "text", "text": "Hi, I'm Claude."}]
      ```

      If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

      For example, if the input `messages` were:

      ```json
      [
        {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
        {"role": "assistant", "content": "The best answer is ("}
      ]
      ```

      Then the response `content` might be:

      ```json
      [{"type": "text", "text": "B)"}]
      ```

      - `class BetaTextBlock:`

        - `citations: Optional<List<BetaTextCitation>>`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `class BetaCitationCharLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endCharIndex: Long`

            - `fileId: Optional<String>`

            - `startCharIndex: Long`

            - `type: JsonValue; "char_location"constant`

              - `CHAR_LOCATION("char_location")`

          - `class BetaCitationPageLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endPageNumber: Long`

            - `fileId: Optional<String>`

            - `startPageNumber: Long`

            - `type: JsonValue; "page_location"constant`

              - `PAGE_LOCATION("page_location")`

          - `class BetaCitationContentBlockLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endBlockIndex: Long`

            - `fileId: Optional<String>`

            - `startBlockIndex: Long`

            - `type: JsonValue; "content_block_location"constant`

              - `CONTENT_BLOCK_LOCATION("content_block_location")`

          - `class BetaCitationsWebSearchResultLocation:`

            - `citedText: String`

            - `encryptedIndex: String`

            - `title: Optional<String>`

            - `type: JsonValue; "web_search_result_location"constant`

              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

            - `url: String`

          - `class BetaCitationSearchResultLocation:`

            - `citedText: String`

            - `endBlockIndex: Long`

            - `searchResultIndex: Long`

            - `source: String`

            - `startBlockIndex: Long`

            - `title: Optional<String>`

            - `type: JsonValue; "search_result_location"constant`

              - `SEARCH_RESULT_LOCATION("search_result_location")`

        - `text: String`

        - `type: JsonValue; "text"constant`

          - `TEXT("text")`

      - `class BetaThinkingBlock:`

        - `signature: String`

        - `thinking: String`

        - `type: JsonValue; "thinking"constant`

          - `THINKING("thinking")`

      - `class BetaRedactedThinkingBlock:`

        - `data: String`

        - `type: JsonValue; "redacted_thinking"constant`

          - `REDACTED_THINKING("redacted_thinking")`

      - `class BetaToolUseBlock:`

        - `id: String`

        - `input: Input`

        - `name: String`

        - `type: JsonValue; "tool_use"constant`

          - `TOOL_USE("tool_use")`

        - `caller: Optional<Caller>`

          Tool invocation directly from the model.

          - `class BetaDirectCaller:`

            Tool invocation directly from the model.

            - `type: JsonValue; "direct"constant`

              - `DIRECT("direct")`

          - `class BetaServerToolCaller:`

            Tool invocation generated by a server-side tool.

            - `toolId: String`

            - `type: JsonValue; "code_execution_20250825"constant`

              - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `class BetaServerToolUseBlock:`

        - `id: String`

        - `caller: Caller`

          Tool invocation directly from the model.

          - `class BetaDirectCaller:`

            Tool invocation directly from the model.

            - `type: JsonValue; "direct"constant`

              - `DIRECT("direct")`

          - `class BetaServerToolCaller:`

            Tool invocation generated by a server-side tool.

            - `toolId: String`

            - `type: JsonValue; "code_execution_20250825"constant`

              - `CODE_EXECUTION_20250825("code_execution_20250825")`

        - `input: Input`

        - `name: Name`

          - `WEB_SEARCH("web_search")`

          - `WEB_FETCH("web_fetch")`

          - `CODE_EXECUTION("code_execution")`

          - `BASH_CODE_EXECUTION("bash_code_execution")`

          - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

          - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

          - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

        - `type: JsonValue; "server_tool_use"constant`

          - `SERVER_TOOL_USE("server_tool_use")`

      - `class BetaWebSearchToolResultBlock:`

        - `content: BetaWebSearchToolResultBlockContent`

          - `class BetaWebSearchToolResultError:`

            - `errorCode: BetaWebSearchToolResultErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `MAX_USES_EXCEEDED("max_uses_exceeded")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `QUERY_TOO_LONG("query_too_long")`

            - `type: JsonValue; "web_search_tool_result_error"constant`

              - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

          - `List<BetaWebSearchResultBlock>`

            - `encryptedContent: String`

            - `pageAge: Optional<String>`

            - `title: String`

            - `type: JsonValue; "web_search_result"constant`

              - `WEB_SEARCH_RESULT("web_search_result")`

            - `url: String`

        - `toolUseId: String`

        - `type: JsonValue; "web_search_tool_result"constant`

          - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

      - `class BetaWebFetchToolResultBlock:`

        - `content: Content`

          - `class BetaWebFetchToolResultErrorBlock:`

            - `errorCode: BetaWebFetchToolResultErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `URL_TOO_LONG("url_too_long")`

              - `URL_NOT_ALLOWED("url_not_allowed")`

              - `URL_NOT_ACCESSIBLE("url_not_accessible")`

              - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `MAX_USES_EXCEEDED("max_uses_exceeded")`

              - `UNAVAILABLE("unavailable")`

            - `type: JsonValue; "web_fetch_tool_result_error"constant`

              - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

          - `class BetaWebFetchBlock:`

            - `content: BetaDocumentBlock`

              - `citations: Optional<BetaCitationConfig>`

                Citation configuration for the document

                - `enabled: Boolean`

              - `source: Source`

                - `class BetaBase64PdfSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "application/pdf"constant`

                    - `APPLICATION_PDF("application/pdf")`

                  - `type: JsonValue; "base64"constant`

                    - `BASE64("base64")`

                - `class BetaPlainTextSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "text/plain"constant`

                    - `TEXT_PLAIN("text/plain")`

                  - `type: JsonValue; "text"constant`

                    - `TEXT("text")`

              - `title: Optional<String>`

                The title of the document

              - `type: JsonValue; "document"constant`

                - `DOCUMENT("document")`

            - `retrievedAt: Optional<String>`

              ISO 8601 timestamp when the content was retrieved

            - `type: JsonValue; "web_fetch_result"constant`

              - `WEB_FETCH_RESULT("web_fetch_result")`

            - `url: String`

              Fetched content URL

        - `toolUseId: String`

        - `type: JsonValue; "web_fetch_tool_result"constant`

          - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

      - `class BetaCodeExecutionToolResultBlock:`

        - `content: BetaCodeExecutionToolResultBlockContent`

          - `class BetaCodeExecutionToolResultError:`

            - `errorCode: BetaCodeExecutionToolResultErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `type: JsonValue; "code_execution_tool_result_error"constant`

              - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

          - `class BetaCodeExecutionResultBlock:`

            - `content: List<BetaCodeExecutionOutputBlock>`

              - `fileId: String`

              - `type: JsonValue; "code_execution_output"constant`

                - `CODE_EXECUTION_OUTPUT("code_execution_output")`

            - `returnCode: Long`

            - `stderr: String`

            - `stdout: String`

            - `type: JsonValue; "code_execution_result"constant`

              - `CODE_EXECUTION_RESULT("code_execution_result")`

        - `toolUseId: String`

        - `type: JsonValue; "code_execution_tool_result"constant`

          - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

      - `class BetaBashCodeExecutionToolResultBlock:`

        - `content: Content`

          - `class BetaBashCodeExecutionToolResultError:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

            - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

              - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

          - `class BetaBashCodeExecutionResultBlock:`

            - `content: List<BetaBashCodeExecutionOutputBlock>`

              - `fileId: String`

              - `type: JsonValue; "bash_code_execution_output"constant`

                - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

            - `returnCode: Long`

            - `stderr: String`

            - `stdout: String`

            - `type: JsonValue; "bash_code_execution_result"constant`

              - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

        - `toolUseId: String`

        - `type: JsonValue; "bash_code_execution_tool_result"constant`

          - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

      - `class BetaTextEditorCodeExecutionToolResultBlock:`

        - `content: Content`

          - `class BetaTextEditorCodeExecutionToolResultError:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `FILE_NOT_FOUND("file_not_found")`

            - `errorMessage: Optional<String>`

            - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

          - `class BetaTextEditorCodeExecutionViewResultBlock:`

            - `content: String`

            - `fileType: FileType`

              - `TEXT("text")`

              - `IMAGE("image")`

              - `PDF("pdf")`

            - `numLines: Optional<Long>`

            - `startLine: Optional<Long>`

            - `totalLines: Optional<Long>`

            - `type: JsonValue; "text_editor_code_execution_view_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

          - `class BetaTextEditorCodeExecutionCreateResultBlock:`

            - `isFileUpdate: Boolean`

            - `type: JsonValue; "text_editor_code_execution_create_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

          - `class BetaTextEditorCodeExecutionStrReplaceResultBlock:`

            - `lines: Optional<List<String>>`

            - `newLines: Optional<Long>`

            - `newStart: Optional<Long>`

            - `oldLines: Optional<Long>`

            - `oldStart: Optional<Long>`

            - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

        - `toolUseId: String`

        - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

          - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

      - `class BetaToolSearchToolResultBlock:`

        - `content: Content`

          - `class BetaToolSearchToolResultError:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `errorMessage: Optional<String>`

            - `type: JsonValue; "tool_search_tool_result_error"constant`

              - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

          - `class BetaToolSearchToolSearchResultBlock:`

            - `toolReferences: List<BetaToolReferenceBlock>`

              - `toolName: String`

              - `type: JsonValue; "tool_reference"constant`

                - `TOOL_REFERENCE("tool_reference")`

            - `type: JsonValue; "tool_search_tool_search_result"constant`

              - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

        - `toolUseId: String`

        - `type: JsonValue; "tool_search_tool_result"constant`

          - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

      - `class BetaMcpToolUseBlock:`

        - `id: String`

        - `input: Input`

        - `name: String`

          The name of the MCP tool

        - `serverName: String`

          The name of the MCP server

        - `type: JsonValue; "mcp_tool_use"constant`

          - `MCP_TOOL_USE("mcp_tool_use")`

      - `class BetaMcpToolResultBlock:`

        - `content: Content`

          - `String`

          - `List<BetaTextBlock>`

            - `citations: Optional<List<BetaTextCitation>>`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class BetaCitationCharLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endCharIndex: Long`

                - `fileId: Optional<String>`

                - `startCharIndex: Long`

                - `type: JsonValue; "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class BetaCitationPageLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endPageNumber: Long`

                - `fileId: Optional<String>`

                - `startPageNumber: Long`

                - `type: JsonValue; "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class BetaCitationContentBlockLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endBlockIndex: Long`

                - `fileId: Optional<String>`

                - `startBlockIndex: Long`

                - `type: JsonValue; "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class BetaCitationsWebSearchResultLocation:`

                - `citedText: String`

                - `encryptedIndex: String`

                - `title: Optional<String>`

                - `type: JsonValue; "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `url: String`

              - `class BetaCitationSearchResultLocation:`

                - `citedText: String`

                - `endBlockIndex: Long`

                - `searchResultIndex: Long`

                - `source: String`

                - `startBlockIndex: Long`

                - `title: Optional<String>`

                - `type: JsonValue; "search_result_location"constant`

                  - `SEARCH_RESULT_LOCATION("search_result_location")`

            - `text: String`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

        - `isError: Boolean`

        - `toolUseId: String`

        - `type: JsonValue; "mcp_tool_result"constant`

          - `MCP_TOOL_RESULT("mcp_tool_result")`

      - `class BetaContainerUploadBlock:`

        Response model for a file uploaded to the container.

        - `fileId: String`

        - `type: JsonValue; "container_upload"constant`

          - `CONTAINER_UPLOAD("container_upload")`

    - `contextManagement: Optional<BetaContextManagementResponse>`

      Context management response.

      Information about context management strategies applied during the request.

      - `appliedEdits: List<AppliedEdit>`

        List of context management edits that were applied.

        - `class BetaClearToolUses20250919EditResponse:`

          - `clearedInputTokens: Long`

            Number of input tokens cleared by this edit.

          - `clearedToolUses: Long`

            Number of tool uses that were cleared.

          - `type: JsonValue; "clear_tool_uses_20250919"constant`

            The type of context management edit applied.

            - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

        - `class BetaClearThinking20251015EditResponse:`

          - `clearedInputTokens: Long`

            Number of input tokens cleared by this edit.

          - `clearedThinkingTurns: Long`

            Number of thinking turns that were cleared.

          - `type: JsonValue; "clear_thinking_20251015"constant`

            The type of context management edit applied.

            - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

    - `model: Model`

      The model that will complete your prompt.

      See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

      - `CLAUDE_OPUS_4_5_20251101("claude-opus-4-5-20251101")`

        Premium model combining maximum intelligence with practical performance

      - `CLAUDE_OPUS_4_5("claude-opus-4-5")`

        Premium model combining maximum intelligence with practical performance

      - `CLAUDE_3_7_SONNET_LATEST("claude-3-7-sonnet-latest")`

        High-performance model with early extended thinking

      - `CLAUDE_3_7_SONNET_20250219("claude-3-7-sonnet-20250219")`

        High-performance model with early extended thinking

      - `CLAUDE_3_5_HAIKU_LATEST("claude-3-5-haiku-latest")`

        Fastest and most compact model for near-instant responsiveness

      - `CLAUDE_3_5_HAIKU_20241022("claude-3-5-haiku-20241022")`

        Our fastest model

      - `CLAUDE_HAIKU_4_5("claude-haiku-4-5")`

        Hybrid model, capable of near-instant responses and extended thinking

      - `CLAUDE_HAIKU_4_5_20251001("claude-haiku-4-5-20251001")`

        Hybrid model, capable of near-instant responses and extended thinking

      - `CLAUDE_SONNET_4_20250514("claude-sonnet-4-20250514")`

        High-performance model with extended thinking

      - `CLAUDE_SONNET_4_0("claude-sonnet-4-0")`

        High-performance model with extended thinking

      - `CLAUDE_4_SONNET_20250514("claude-4-sonnet-20250514")`

        High-performance model with extended thinking

      - `CLAUDE_SONNET_4_5("claude-sonnet-4-5")`

        Our best model for real-world agents and coding

      - `CLAUDE_SONNET_4_5_20250929("claude-sonnet-4-5-20250929")`

        Our best model for real-world agents and coding

      - `CLAUDE_OPUS_4_0("claude-opus-4-0")`

        Our most capable model

      - `CLAUDE_OPUS_4_20250514("claude-opus-4-20250514")`

        Our most capable model

      - `CLAUDE_4_OPUS_20250514("claude-4-opus-20250514")`

        Our most capable model

      - `CLAUDE_OPUS_4_1_20250805("claude-opus-4-1-20250805")`

        Our most capable model

      - `CLAUDE_3_OPUS_LATEST("claude-3-opus-latest")`

        Excels at writing and complex tasks

      - `CLAUDE_3_OPUS_20240229("claude-3-opus-20240229")`

        Excels at writing and complex tasks

      - `CLAUDE_3_HAIKU_20240307("claude-3-haiku-20240307")`

        Our previous most fast and cost-effective

    - `role: JsonValue; "assistant"constant`

      Conversational role of the generated message.

      This will always be `"assistant"`.

      - `ASSISTANT("assistant")`

    - `stopReason: Optional<BetaStopReason>`

      The reason that we stopped.

      This may be one the following values:

      * `"end_turn"`: the model reached a natural stopping point
      * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
      * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
      * `"tool_use"`: the model invoked one or more tools
      * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
      * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

      In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

      - `END_TURN("end_turn")`

      - `MAX_TOKENS("max_tokens")`

      - `STOP_SEQUENCE("stop_sequence")`

      - `TOOL_USE("tool_use")`

      - `PAUSE_TURN("pause_turn")`

      - `REFUSAL("refusal")`

      - `MODEL_CONTEXT_WINDOW_EXCEEDED("model_context_window_exceeded")`

    - `stopSequence: Optional<String>`

      Which custom stop sequence was generated, if any.

      This value will be a non-null string if one of your custom stop sequences was generated.

    - `type: JsonValue; "message"constant`

      Object type.

      For Messages, this is always `"message"`.

      - `MESSAGE("message")`

    - `usage: BetaUsage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cacheCreation: Optional<BetaCacheCreation>`

        Breakdown of cached tokens by TTL

        - `ephemeral1hInputTokens: Long`

          The number of input tokens used to create the 1 hour cache entry.

        - `ephemeral5mInputTokens: Long`

          The number of input tokens used to create the 5 minute cache entry.

      - `cacheCreationInputTokens: Optional<Long>`

        The number of input tokens used to create the cache entry.

      - `cacheReadInputTokens: Optional<Long>`

        The number of input tokens read from the cache.

      - `inputTokens: Long`

        The number of input tokens which were used.

      - `outputTokens: Long`

        The number of output tokens which were used.

      - `serverToolUse: Optional<BetaServerToolUsage>`

        The number of server tool requests.

        - `webFetchRequests: Long`

          The number of web fetch tool requests.

        - `webSearchRequests: Long`

          The number of web search tool requests.

      - `serviceTier: Optional<ServiceTier>`

        If the request used the priority, standard, or batch tier.

        - `STANDARD("standard")`

        - `PRIORITY("priority")`

        - `BATCH("batch")`

  - `type: JsonValue; "message_start"constant`

    - `MESSAGE_START("message_start")`

### Beta Raw Message Stop Event

- `class BetaRawMessageStopEvent:`

  - `type: JsonValue; "message_stop"constant`

    - `MESSAGE_STOP("message_stop")`

### Beta Raw Message Stream Event

- `class BetaRawMessageStreamEvent: A class that can be one of several variants.union`

  - `class BetaRawMessageStartEvent:`

    - `message: BetaMessage`

      - `id: String`

        Unique object identifier.

        The format and length of IDs may change over time.

      - `container: Optional<BetaContainer>`

        Information about the container used in the request (for the code execution tool)

        - `id: String`

          Identifier for the container used in this request

        - `expiresAt: LocalDateTime`

          The time at which the container will expire.

        - `skills: Optional<List<BetaSkill>>`

          Skills loaded in the container

          - `skillId: String`

            Skill ID

          - `type: Type`

            Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

            - `ANTHROPIC("anthropic")`

            - `CUSTOM("custom")`

          - `version: String`

            Skill version or 'latest' for most recent version

      - `content: List<BetaContentBlock>`

        Content generated by the model.

        This is an array of content blocks, each of which has a `type` that determines its shape.

        Example:

        ```json
        [{"type": "text", "text": "Hi, I'm Claude."}]
        ```

        If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

        For example, if the input `messages` were:

        ```json
        [
          {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
          {"role": "assistant", "content": "The best answer is ("}
        ]
        ```

        Then the response `content` might be:

        ```json
        [{"type": "text", "text": "B)"}]
        ```

        - `class BetaTextBlock:`

          - `citations: Optional<List<BetaTextCitation>>`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `class BetaCitationCharLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `fileId: Optional<String>`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class BetaCitationPageLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `fileId: Optional<String>`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class BetaCitationContentBlockLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `fileId: Optional<String>`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class BetaCitationsWebSearchResultLocation:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class BetaCitationSearchResultLocation:`

              - `citedText: String`

              - `endBlockIndex: Long`

              - `searchResultIndex: Long`

              - `source: String`

              - `startBlockIndex: Long`

              - `title: Optional<String>`

              - `type: JsonValue; "search_result_location"constant`

                - `SEARCH_RESULT_LOCATION("search_result_location")`

          - `text: String`

          - `type: JsonValue; "text"constant`

            - `TEXT("text")`

        - `class BetaThinkingBlock:`

          - `signature: String`

          - `thinking: String`

          - `type: JsonValue; "thinking"constant`

            - `THINKING("thinking")`

        - `class BetaRedactedThinkingBlock:`

          - `data: String`

          - `type: JsonValue; "redacted_thinking"constant`

            - `REDACTED_THINKING("redacted_thinking")`

        - `class BetaToolUseBlock:`

          - `id: String`

          - `input: Input`

          - `name: String`

          - `type: JsonValue; "tool_use"constant`

            - `TOOL_USE("tool_use")`

          - `caller: Optional<Caller>`

            Tool invocation directly from the model.

            - `class BetaDirectCaller:`

              Tool invocation directly from the model.

              - `type: JsonValue; "direct"constant`

                - `DIRECT("direct")`

            - `class BetaServerToolCaller:`

              Tool invocation generated by a server-side tool.

              - `toolId: String`

              - `type: JsonValue; "code_execution_20250825"constant`

                - `CODE_EXECUTION_20250825("code_execution_20250825")`

        - `class BetaServerToolUseBlock:`

          - `id: String`

          - `caller: Caller`

            Tool invocation directly from the model.

            - `class BetaDirectCaller:`

              Tool invocation directly from the model.

              - `type: JsonValue; "direct"constant`

                - `DIRECT("direct")`

            - `class BetaServerToolCaller:`

              Tool invocation generated by a server-side tool.

              - `toolId: String`

              - `type: JsonValue; "code_execution_20250825"constant`

                - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `input: Input`

          - `name: Name`

            - `WEB_SEARCH("web_search")`

            - `WEB_FETCH("web_fetch")`

            - `CODE_EXECUTION("code_execution")`

            - `BASH_CODE_EXECUTION("bash_code_execution")`

            - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

            - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

            - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

          - `type: JsonValue; "server_tool_use"constant`

            - `SERVER_TOOL_USE("server_tool_use")`

        - `class BetaWebSearchToolResultBlock:`

          - `content: BetaWebSearchToolResultBlockContent`

            - `class BetaWebSearchToolResultError:`

              - `errorCode: BetaWebSearchToolResultErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `QUERY_TOO_LONG("query_too_long")`

              - `type: JsonValue; "web_search_tool_result_error"constant`

                - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

            - `List<BetaWebSearchResultBlock>`

              - `encryptedContent: String`

              - `pageAge: Optional<String>`

              - `title: String`

              - `type: JsonValue; "web_search_result"constant`

                - `WEB_SEARCH_RESULT("web_search_result")`

              - `url: String`

          - `toolUseId: String`

          - `type: JsonValue; "web_search_tool_result"constant`

            - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

        - `class BetaWebFetchToolResultBlock:`

          - `content: Content`

            - `class BetaWebFetchToolResultErrorBlock:`

              - `errorCode: BetaWebFetchToolResultErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `URL_TOO_LONG("url_too_long")`

                - `URL_NOT_ALLOWED("url_not_allowed")`

                - `URL_NOT_ACCESSIBLE("url_not_accessible")`

                - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                - `UNAVAILABLE("unavailable")`

              - `type: JsonValue; "web_fetch_tool_result_error"constant`

                - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

            - `class BetaWebFetchBlock:`

              - `content: BetaDocumentBlock`

                - `citations: Optional<BetaCitationConfig>`

                  Citation configuration for the document

                  - `enabled: Boolean`

                - `source: Source`

                  - `class BetaBase64PdfSource:`

                    - `data: String`

                    - `mediaType: JsonValue; "application/pdf"constant`

                      - `APPLICATION_PDF("application/pdf")`

                    - `type: JsonValue; "base64"constant`

                      - `BASE64("base64")`

                  - `class BetaPlainTextSource:`

                    - `data: String`

                    - `mediaType: JsonValue; "text/plain"constant`

                      - `TEXT_PLAIN("text/plain")`

                    - `type: JsonValue; "text"constant`

                      - `TEXT("text")`

                - `title: Optional<String>`

                  The title of the document

                - `type: JsonValue; "document"constant`

                  - `DOCUMENT("document")`

              - `retrievedAt: Optional<String>`

                ISO 8601 timestamp when the content was retrieved

              - `type: JsonValue; "web_fetch_result"constant`

                - `WEB_FETCH_RESULT("web_fetch_result")`

              - `url: String`

                Fetched content URL

          - `toolUseId: String`

          - `type: JsonValue; "web_fetch_tool_result"constant`

            - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

        - `class BetaCodeExecutionToolResultBlock:`

          - `content: BetaCodeExecutionToolResultBlockContent`

            - `class BetaCodeExecutionToolResultError:`

              - `errorCode: BetaCodeExecutionToolResultErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `type: JsonValue; "code_execution_tool_result_error"constant`

                - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

            - `class BetaCodeExecutionResultBlock:`

              - `content: List<BetaCodeExecutionOutputBlock>`

                - `fileId: String`

                - `type: JsonValue; "code_execution_output"constant`

                  - `CODE_EXECUTION_OUTPUT("code_execution_output")`

              - `returnCode: Long`

              - `stderr: String`

              - `stdout: String`

              - `type: JsonValue; "code_execution_result"constant`

                - `CODE_EXECUTION_RESULT("code_execution_result")`

          - `toolUseId: String`

          - `type: JsonValue; "code_execution_tool_result"constant`

            - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

        - `class BetaBashCodeExecutionToolResultBlock:`

          - `content: Content`

            - `class BetaBashCodeExecutionToolResultError:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

              - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

                - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

            - `class BetaBashCodeExecutionResultBlock:`

              - `content: List<BetaBashCodeExecutionOutputBlock>`

                - `fileId: String`

                - `type: JsonValue; "bash_code_execution_output"constant`

                  - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

              - `returnCode: Long`

              - `stderr: String`

              - `stdout: String`

              - `type: JsonValue; "bash_code_execution_result"constant`

                - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

          - `toolUseId: String`

          - `type: JsonValue; "bash_code_execution_tool_result"constant`

            - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

        - `class BetaTextEditorCodeExecutionToolResultBlock:`

          - `content: Content`

            - `class BetaTextEditorCodeExecutionToolResultError:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `FILE_NOT_FOUND("file_not_found")`

              - `errorMessage: Optional<String>`

              - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

            - `class BetaTextEditorCodeExecutionViewResultBlock:`

              - `content: String`

              - `fileType: FileType`

                - `TEXT("text")`

                - `IMAGE("image")`

                - `PDF("pdf")`

              - `numLines: Optional<Long>`

              - `startLine: Optional<Long>`

              - `totalLines: Optional<Long>`

              - `type: JsonValue; "text_editor_code_execution_view_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

            - `class BetaTextEditorCodeExecutionCreateResultBlock:`

              - `isFileUpdate: Boolean`

              - `type: JsonValue; "text_editor_code_execution_create_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

            - `class BetaTextEditorCodeExecutionStrReplaceResultBlock:`

              - `lines: Optional<List<String>>`

              - `newLines: Optional<Long>`

              - `newStart: Optional<Long>`

              - `oldLines: Optional<Long>`

              - `oldStart: Optional<Long>`

              - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

          - `toolUseId: String`

          - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

        - `class BetaToolSearchToolResultBlock:`

          - `content: Content`

            - `class BetaToolSearchToolResultError:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `errorMessage: Optional<String>`

              - `type: JsonValue; "tool_search_tool_result_error"constant`

                - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

            - `class BetaToolSearchToolSearchResultBlock:`

              - `toolReferences: List<BetaToolReferenceBlock>`

                - `toolName: String`

                - `type: JsonValue; "tool_reference"constant`

                  - `TOOL_REFERENCE("tool_reference")`

              - `type: JsonValue; "tool_search_tool_search_result"constant`

                - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

          - `toolUseId: String`

          - `type: JsonValue; "tool_search_tool_result"constant`

            - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

        - `class BetaMcpToolUseBlock:`

          - `id: String`

          - `input: Input`

          - `name: String`

            The name of the MCP tool

          - `serverName: String`

            The name of the MCP server

          - `type: JsonValue; "mcp_tool_use"constant`

            - `MCP_TOOL_USE("mcp_tool_use")`

        - `class BetaMcpToolResultBlock:`

          - `content: Content`

            - `String`

            - `List<BetaTextBlock>`

              - `citations: Optional<List<BetaTextCitation>>`

                Citations supporting the text block.

                The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

                - `class BetaCitationCharLocation:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endCharIndex: Long`

                  - `fileId: Optional<String>`

                  - `startCharIndex: Long`

                  - `type: JsonValue; "char_location"constant`

                    - `CHAR_LOCATION("char_location")`

                - `class BetaCitationPageLocation:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endPageNumber: Long`

                  - `fileId: Optional<String>`

                  - `startPageNumber: Long`

                  - `type: JsonValue; "page_location"constant`

                    - `PAGE_LOCATION("page_location")`

                - `class BetaCitationContentBlockLocation:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endBlockIndex: Long`

                  - `fileId: Optional<String>`

                  - `startBlockIndex: Long`

                  - `type: JsonValue; "content_block_location"constant`

                    - `CONTENT_BLOCK_LOCATION("content_block_location")`

                - `class BetaCitationsWebSearchResultLocation:`

                  - `citedText: String`

                  - `encryptedIndex: String`

                  - `title: Optional<String>`

                  - `type: JsonValue; "web_search_result_location"constant`

                    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                  - `url: String`

                - `class BetaCitationSearchResultLocation:`

                  - `citedText: String`

                  - `endBlockIndex: Long`

                  - `searchResultIndex: Long`

                  - `source: String`

                  - `startBlockIndex: Long`

                  - `title: Optional<String>`

                  - `type: JsonValue; "search_result_location"constant`

                    - `SEARCH_RESULT_LOCATION("search_result_location")`

              - `text: String`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

          - `isError: Boolean`

          - `toolUseId: String`

          - `type: JsonValue; "mcp_tool_result"constant`

            - `MCP_TOOL_RESULT("mcp_tool_result")`

        - `class BetaContainerUploadBlock:`

          Response model for a file uploaded to the container.

          - `fileId: String`

          - `type: JsonValue; "container_upload"constant`

            - `CONTAINER_UPLOAD("container_upload")`

      - `contextManagement: Optional<BetaContextManagementResponse>`

        Context management response.

        Information about context management strategies applied during the request.

        - `appliedEdits: List<AppliedEdit>`

          List of context management edits that were applied.

          - `class BetaClearToolUses20250919EditResponse:`

            - `clearedInputTokens: Long`

              Number of input tokens cleared by this edit.

            - `clearedToolUses: Long`

              Number of tool uses that were cleared.

            - `type: JsonValue; "clear_tool_uses_20250919"constant`

              The type of context management edit applied.

              - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

          - `class BetaClearThinking20251015EditResponse:`

            - `clearedInputTokens: Long`

              Number of input tokens cleared by this edit.

            - `clearedThinkingTurns: Long`

              Number of thinking turns that were cleared.

            - `type: JsonValue; "clear_thinking_20251015"constant`

              The type of context management edit applied.

              - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

      - `model: Model`

        The model that will complete your prompt.

        See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

        - `CLAUDE_OPUS_4_5_20251101("claude-opus-4-5-20251101")`

          Premium model combining maximum intelligence with practical performance

        - `CLAUDE_OPUS_4_5("claude-opus-4-5")`

          Premium model combining maximum intelligence with practical performance

        - `CLAUDE_3_7_SONNET_LATEST("claude-3-7-sonnet-latest")`

          High-performance model with early extended thinking

        - `CLAUDE_3_7_SONNET_20250219("claude-3-7-sonnet-20250219")`

          High-performance model with early extended thinking

        - `CLAUDE_3_5_HAIKU_LATEST("claude-3-5-haiku-latest")`

          Fastest and most compact model for near-instant responsiveness

        - `CLAUDE_3_5_HAIKU_20241022("claude-3-5-haiku-20241022")`

          Our fastest model

        - `CLAUDE_HAIKU_4_5("claude-haiku-4-5")`

          Hybrid model, capable of near-instant responses and extended thinking

        - `CLAUDE_HAIKU_4_5_20251001("claude-haiku-4-5-20251001")`

          Hybrid model, capable of near-instant responses and extended thinking

        - `CLAUDE_SONNET_4_20250514("claude-sonnet-4-20250514")`

          High-performance model with extended thinking

        - `CLAUDE_SONNET_4_0("claude-sonnet-4-0")`

          High-performance model with extended thinking

        - `CLAUDE_4_SONNET_20250514("claude-4-sonnet-20250514")`

          High-performance model with extended thinking

        - `CLAUDE_SONNET_4_5("claude-sonnet-4-5")`

          Our best model for real-world agents and coding

        - `CLAUDE_SONNET_4_5_20250929("claude-sonnet-4-5-20250929")`

          Our best model for real-world agents and coding

        - `CLAUDE_OPUS_4_0("claude-opus-4-0")`

          Our most capable model

        - `CLAUDE_OPUS_4_20250514("claude-opus-4-20250514")`

          Our most capable model

        - `CLAUDE_4_OPUS_20250514("claude-4-opus-20250514")`

          Our most capable model

        - `CLAUDE_OPUS_4_1_20250805("claude-opus-4-1-20250805")`

          Our most capable model

        - `CLAUDE_3_OPUS_LATEST("claude-3-opus-latest")`

          Excels at writing and complex tasks

        - `CLAUDE_3_OPUS_20240229("claude-3-opus-20240229")`

          Excels at writing and complex tasks

        - `CLAUDE_3_HAIKU_20240307("claude-3-haiku-20240307")`

          Our previous most fast and cost-effective

      - `role: JsonValue; "assistant"constant`

        Conversational role of the generated message.

        This will always be `"assistant"`.

        - `ASSISTANT("assistant")`

      - `stopReason: Optional<BetaStopReason>`

        The reason that we stopped.

        This may be one the following values:

        * `"end_turn"`: the model reached a natural stopping point
        * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
        * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
        * `"tool_use"`: the model invoked one or more tools
        * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
        * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

        In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

        - `END_TURN("end_turn")`

        - `MAX_TOKENS("max_tokens")`

        - `STOP_SEQUENCE("stop_sequence")`

        - `TOOL_USE("tool_use")`

        - `PAUSE_TURN("pause_turn")`

        - `REFUSAL("refusal")`

        - `MODEL_CONTEXT_WINDOW_EXCEEDED("model_context_window_exceeded")`

      - `stopSequence: Optional<String>`

        Which custom stop sequence was generated, if any.

        This value will be a non-null string if one of your custom stop sequences was generated.

      - `type: JsonValue; "message"constant`

        Object type.

        For Messages, this is always `"message"`.

        - `MESSAGE("message")`

      - `usage: BetaUsage`

        Billing and rate-limit usage.

        Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

        Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

        For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

        Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

        - `cacheCreation: Optional<BetaCacheCreation>`

          Breakdown of cached tokens by TTL

          - `ephemeral1hInputTokens: Long`

            The number of input tokens used to create the 1 hour cache entry.

          - `ephemeral5mInputTokens: Long`

            The number of input tokens used to create the 5 minute cache entry.

        - `cacheCreationInputTokens: Optional<Long>`

          The number of input tokens used to create the cache entry.

        - `cacheReadInputTokens: Optional<Long>`

          The number of input tokens read from the cache.

        - `inputTokens: Long`

          The number of input tokens which were used.

        - `outputTokens: Long`

          The number of output tokens which were used.

        - `serverToolUse: Optional<BetaServerToolUsage>`

          The number of server tool requests.

          - `webFetchRequests: Long`

            The number of web fetch tool requests.

          - `webSearchRequests: Long`

            The number of web search tool requests.

        - `serviceTier: Optional<ServiceTier>`

          If the request used the priority, standard, or batch tier.

          - `STANDARD("standard")`

          - `PRIORITY("priority")`

          - `BATCH("batch")`

    - `type: JsonValue; "message_start"constant`

      - `MESSAGE_START("message_start")`

  - `class BetaRawMessageDeltaEvent:`

    - `contextManagement: Optional<BetaContextManagementResponse>`

      Information about context management strategies applied during the request

      - `appliedEdits: List<AppliedEdit>`

        List of context management edits that were applied.

        - `class BetaClearToolUses20250919EditResponse:`

          - `clearedInputTokens: Long`

            Number of input tokens cleared by this edit.

          - `clearedToolUses: Long`

            Number of tool uses that were cleared.

          - `type: JsonValue; "clear_tool_uses_20250919"constant`

            The type of context management edit applied.

            - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

        - `class BetaClearThinking20251015EditResponse:`

          - `clearedInputTokens: Long`

            Number of input tokens cleared by this edit.

          - `clearedThinkingTurns: Long`

            Number of thinking turns that were cleared.

          - `type: JsonValue; "clear_thinking_20251015"constant`

            The type of context management edit applied.

            - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

    - `delta: Delta`

      - `container: Optional<BetaContainer>`

        Information about the container used in the request (for the code execution tool)

        - `id: String`

          Identifier for the container used in this request

        - `expiresAt: LocalDateTime`

          The time at which the container will expire.

        - `skills: Optional<List<BetaSkill>>`

          Skills loaded in the container

          - `skillId: String`

            Skill ID

          - `type: Type`

            Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

            - `ANTHROPIC("anthropic")`

            - `CUSTOM("custom")`

          - `version: String`

            Skill version or 'latest' for most recent version

      - `stopReason: Optional<BetaStopReason>`

        - `END_TURN("end_turn")`

        - `MAX_TOKENS("max_tokens")`

        - `STOP_SEQUENCE("stop_sequence")`

        - `TOOL_USE("tool_use")`

        - `PAUSE_TURN("pause_turn")`

        - `REFUSAL("refusal")`

        - `MODEL_CONTEXT_WINDOW_EXCEEDED("model_context_window_exceeded")`

      - `stopSequence: Optional<String>`

    - `type: JsonValue; "message_delta"constant`

      - `MESSAGE_DELTA("message_delta")`

    - `usage: BetaMessageDeltaUsage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cacheCreationInputTokens: Optional<Long>`

        The cumulative number of input tokens used to create the cache entry.

      - `cacheReadInputTokens: Optional<Long>`

        The cumulative number of input tokens read from the cache.

      - `inputTokens: Optional<Long>`

        The cumulative number of input tokens which were used.

      - `outputTokens: Long`

        The cumulative number of output tokens which were used.

      - `serverToolUse: Optional<BetaServerToolUsage>`

        The number of server tool requests.

        - `webFetchRequests: Long`

          The number of web fetch tool requests.

        - `webSearchRequests: Long`

          The number of web search tool requests.

  - `class BetaRawMessageStopEvent:`

    - `type: JsonValue; "message_stop"constant`

      - `MESSAGE_STOP("message_stop")`

  - `class BetaRawContentBlockStartEvent:`

    - `contentBlock: ContentBlock`

      Response model for a file uploaded to the container.

      - `class BetaTextBlock:`

        - `citations: Optional<List<BetaTextCitation>>`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `class BetaCitationCharLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endCharIndex: Long`

            - `fileId: Optional<String>`

            - `startCharIndex: Long`

            - `type: JsonValue; "char_location"constant`

              - `CHAR_LOCATION("char_location")`

          - `class BetaCitationPageLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endPageNumber: Long`

            - `fileId: Optional<String>`

            - `startPageNumber: Long`

            - `type: JsonValue; "page_location"constant`

              - `PAGE_LOCATION("page_location")`

          - `class BetaCitationContentBlockLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endBlockIndex: Long`

            - `fileId: Optional<String>`

            - `startBlockIndex: Long`

            - `type: JsonValue; "content_block_location"constant`

              - `CONTENT_BLOCK_LOCATION("content_block_location")`

          - `class BetaCitationsWebSearchResultLocation:`

            - `citedText: String`

            - `encryptedIndex: String`

            - `title: Optional<String>`

            - `type: JsonValue; "web_search_result_location"constant`

              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

            - `url: String`

          - `class BetaCitationSearchResultLocation:`

            - `citedText: String`

            - `endBlockIndex: Long`

            - `searchResultIndex: Long`

            - `source: String`

            - `startBlockIndex: Long`

            - `title: Optional<String>`

            - `type: JsonValue; "search_result_location"constant`

              - `SEARCH_RESULT_LOCATION("search_result_location")`

        - `text: String`

        - `type: JsonValue; "text"constant`

          - `TEXT("text")`

      - `class BetaThinkingBlock:`

        - `signature: String`

        - `thinking: String`

        - `type: JsonValue; "thinking"constant`

          - `THINKING("thinking")`

      - `class BetaRedactedThinkingBlock:`

        - `data: String`

        - `type: JsonValue; "redacted_thinking"constant`

          - `REDACTED_THINKING("redacted_thinking")`

      - `class BetaToolUseBlock:`

        - `id: String`

        - `input: Input`

        - `name: String`

        - `type: JsonValue; "tool_use"constant`

          - `TOOL_USE("tool_use")`

        - `caller: Optional<Caller>`

          Tool invocation directly from the model.

          - `class BetaDirectCaller:`

            Tool invocation directly from the model.

            - `type: JsonValue; "direct"constant`

              - `DIRECT("direct")`

          - `class BetaServerToolCaller:`

            Tool invocation generated by a server-side tool.

            - `toolId: String`

            - `type: JsonValue; "code_execution_20250825"constant`

              - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `class BetaServerToolUseBlock:`

        - `id: String`

        - `caller: Caller`

          Tool invocation directly from the model.

          - `class BetaDirectCaller:`

            Tool invocation directly from the model.

            - `type: JsonValue; "direct"constant`

              - `DIRECT("direct")`

          - `class BetaServerToolCaller:`

            Tool invocation generated by a server-side tool.

            - `toolId: String`

            - `type: JsonValue; "code_execution_20250825"constant`

              - `CODE_EXECUTION_20250825("code_execution_20250825")`

        - `input: Input`

        - `name: Name`

          - `WEB_SEARCH("web_search")`

          - `WEB_FETCH("web_fetch")`

          - `CODE_EXECUTION("code_execution")`

          - `BASH_CODE_EXECUTION("bash_code_execution")`

          - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

          - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

          - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

        - `type: JsonValue; "server_tool_use"constant`

          - `SERVER_TOOL_USE("server_tool_use")`

      - `class BetaWebSearchToolResultBlock:`

        - `content: BetaWebSearchToolResultBlockContent`

          - `class BetaWebSearchToolResultError:`

            - `errorCode: BetaWebSearchToolResultErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `MAX_USES_EXCEEDED("max_uses_exceeded")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `QUERY_TOO_LONG("query_too_long")`

            - `type: JsonValue; "web_search_tool_result_error"constant`

              - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

          - `List<BetaWebSearchResultBlock>`

            - `encryptedContent: String`

            - `pageAge: Optional<String>`

            - `title: String`

            - `type: JsonValue; "web_search_result"constant`

              - `WEB_SEARCH_RESULT("web_search_result")`

            - `url: String`

        - `toolUseId: String`

        - `type: JsonValue; "web_search_tool_result"constant`

          - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

      - `class BetaWebFetchToolResultBlock:`

        - `content: Content`

          - `class BetaWebFetchToolResultErrorBlock:`

            - `errorCode: BetaWebFetchToolResultErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `URL_TOO_LONG("url_too_long")`

              - `URL_NOT_ALLOWED("url_not_allowed")`

              - `URL_NOT_ACCESSIBLE("url_not_accessible")`

              - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `MAX_USES_EXCEEDED("max_uses_exceeded")`

              - `UNAVAILABLE("unavailable")`

            - `type: JsonValue; "web_fetch_tool_result_error"constant`

              - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

          - `class BetaWebFetchBlock:`

            - `content: BetaDocumentBlock`

              - `citations: Optional<BetaCitationConfig>`

                Citation configuration for the document

                - `enabled: Boolean`

              - `source: Source`

                - `class BetaBase64PdfSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "application/pdf"constant`

                    - `APPLICATION_PDF("application/pdf")`

                  - `type: JsonValue; "base64"constant`

                    - `BASE64("base64")`

                - `class BetaPlainTextSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "text/plain"constant`

                    - `TEXT_PLAIN("text/plain")`

                  - `type: JsonValue; "text"constant`

                    - `TEXT("text")`

              - `title: Optional<String>`

                The title of the document

              - `type: JsonValue; "document"constant`

                - `DOCUMENT("document")`

            - `retrievedAt: Optional<String>`

              ISO 8601 timestamp when the content was retrieved

            - `type: JsonValue; "web_fetch_result"constant`

              - `WEB_FETCH_RESULT("web_fetch_result")`

            - `url: String`

              Fetched content URL

        - `toolUseId: String`

        - `type: JsonValue; "web_fetch_tool_result"constant`

          - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

      - `class BetaCodeExecutionToolResultBlock:`

        - `content: BetaCodeExecutionToolResultBlockContent`

          - `class BetaCodeExecutionToolResultError:`

            - `errorCode: BetaCodeExecutionToolResultErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `type: JsonValue; "code_execution_tool_result_error"constant`

              - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

          - `class BetaCodeExecutionResultBlock:`

            - `content: List<BetaCodeExecutionOutputBlock>`

              - `fileId: String`

              - `type: JsonValue; "code_execution_output"constant`

                - `CODE_EXECUTION_OUTPUT("code_execution_output")`

            - `returnCode: Long`

            - `stderr: String`

            - `stdout: String`

            - `type: JsonValue; "code_execution_result"constant`

              - `CODE_EXECUTION_RESULT("code_execution_result")`

        - `toolUseId: String`

        - `type: JsonValue; "code_execution_tool_result"constant`

          - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

      - `class BetaBashCodeExecutionToolResultBlock:`

        - `content: Content`

          - `class BetaBashCodeExecutionToolResultError:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

            - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

              - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

          - `class BetaBashCodeExecutionResultBlock:`

            - `content: List<BetaBashCodeExecutionOutputBlock>`

              - `fileId: String`

              - `type: JsonValue; "bash_code_execution_output"constant`

                - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

            - `returnCode: Long`

            - `stderr: String`

            - `stdout: String`

            - `type: JsonValue; "bash_code_execution_result"constant`

              - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

        - `toolUseId: String`

        - `type: JsonValue; "bash_code_execution_tool_result"constant`

          - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

      - `class BetaTextEditorCodeExecutionToolResultBlock:`

        - `content: Content`

          - `class BetaTextEditorCodeExecutionToolResultError:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `FILE_NOT_FOUND("file_not_found")`

            - `errorMessage: Optional<String>`

            - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

          - `class BetaTextEditorCodeExecutionViewResultBlock:`

            - `content: String`

            - `fileType: FileType`

              - `TEXT("text")`

              - `IMAGE("image")`

              - `PDF("pdf")`

            - `numLines: Optional<Long>`

            - `startLine: Optional<Long>`

            - `totalLines: Optional<Long>`

            - `type: JsonValue; "text_editor_code_execution_view_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

          - `class BetaTextEditorCodeExecutionCreateResultBlock:`

            - `isFileUpdate: Boolean`

            - `type: JsonValue; "text_editor_code_execution_create_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

          - `class BetaTextEditorCodeExecutionStrReplaceResultBlock:`

            - `lines: Optional<List<String>>`

            - `newLines: Optional<Long>`

            - `newStart: Optional<Long>`

            - `oldLines: Optional<Long>`

            - `oldStart: Optional<Long>`

            - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

        - `toolUseId: String`

        - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

          - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

      - `class BetaToolSearchToolResultBlock:`

        - `content: Content`

          - `class BetaToolSearchToolResultError:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `errorMessage: Optional<String>`

            - `type: JsonValue; "tool_search_tool_result_error"constant`

              - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

          - `class BetaToolSearchToolSearchResultBlock:`

            - `toolReferences: List<BetaToolReferenceBlock>`

              - `toolName: String`

              - `type: JsonValue; "tool_reference"constant`

                - `TOOL_REFERENCE("tool_reference")`

            - `type: JsonValue; "tool_search_tool_search_result"constant`

              - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

        - `toolUseId: String`

        - `type: JsonValue; "tool_search_tool_result"constant`

          - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

      - `class BetaMcpToolUseBlock:`

        - `id: String`

        - `input: Input`

        - `name: String`

          The name of the MCP tool

        - `serverName: String`

          The name of the MCP server

        - `type: JsonValue; "mcp_tool_use"constant`

          - `MCP_TOOL_USE("mcp_tool_use")`

      - `class BetaMcpToolResultBlock:`

        - `content: Content`

          - `String`

          - `List<BetaTextBlock>`

            - `citations: Optional<List<BetaTextCitation>>`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class BetaCitationCharLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endCharIndex: Long`

                - `fileId: Optional<String>`

                - `startCharIndex: Long`

                - `type: JsonValue; "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class BetaCitationPageLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endPageNumber: Long`

                - `fileId: Optional<String>`

                - `startPageNumber: Long`

                - `type: JsonValue; "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class BetaCitationContentBlockLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endBlockIndex: Long`

                - `fileId: Optional<String>`

                - `startBlockIndex: Long`

                - `type: JsonValue; "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class BetaCitationsWebSearchResultLocation:`

                - `citedText: String`

                - `encryptedIndex: String`

                - `title: Optional<String>`

                - `type: JsonValue; "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `url: String`

              - `class BetaCitationSearchResultLocation:`

                - `citedText: String`

                - `endBlockIndex: Long`

                - `searchResultIndex: Long`

                - `source: String`

                - `startBlockIndex: Long`

                - `title: Optional<String>`

                - `type: JsonValue; "search_result_location"constant`

                  - `SEARCH_RESULT_LOCATION("search_result_location")`

            - `text: String`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

        - `isError: Boolean`

        - `toolUseId: String`

        - `type: JsonValue; "mcp_tool_result"constant`

          - `MCP_TOOL_RESULT("mcp_tool_result")`

      - `class BetaContainerUploadBlock:`

        Response model for a file uploaded to the container.

        - `fileId: String`

        - `type: JsonValue; "container_upload"constant`

          - `CONTAINER_UPLOAD("container_upload")`

    - `index: Long`

    - `type: JsonValue; "content_block_start"constant`

      - `CONTENT_BLOCK_START("content_block_start")`

  - `class BetaRawContentBlockDeltaEvent:`

    - `delta: BetaRawContentBlockDelta`

      - `class BetaTextDelta:`

        - `text: String`

        - `type: JsonValue; "text_delta"constant`

          - `TEXT_DELTA("text_delta")`

      - `class BetaInputJsonDelta:`

        - `partialJson: String`

        - `type: JsonValue; "input_json_delta"constant`

          - `INPUT_JSON_DELTA("input_json_delta")`

      - `class BetaCitationsDelta:`

        - `citation: Citation`

          - `class BetaCitationCharLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endCharIndex: Long`

            - `fileId: Optional<String>`

            - `startCharIndex: Long`

            - `type: JsonValue; "char_location"constant`

              - `CHAR_LOCATION("char_location")`

          - `class BetaCitationPageLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endPageNumber: Long`

            - `fileId: Optional<String>`

            - `startPageNumber: Long`

            - `type: JsonValue; "page_location"constant`

              - `PAGE_LOCATION("page_location")`

          - `class BetaCitationContentBlockLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endBlockIndex: Long`

            - `fileId: Optional<String>`

            - `startBlockIndex: Long`

            - `type: JsonValue; "content_block_location"constant`

              - `CONTENT_BLOCK_LOCATION("content_block_location")`

          - `class BetaCitationsWebSearchResultLocation:`

            - `citedText: String`

            - `encryptedIndex: String`

            - `title: Optional<String>`

            - `type: JsonValue; "web_search_result_location"constant`

              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

            - `url: String`

          - `class BetaCitationSearchResultLocation:`

            - `citedText: String`

            - `endBlockIndex: Long`

            - `searchResultIndex: Long`

            - `source: String`

            - `startBlockIndex: Long`

            - `title: Optional<String>`

            - `type: JsonValue; "search_result_location"constant`

              - `SEARCH_RESULT_LOCATION("search_result_location")`

        - `type: JsonValue; "citations_delta"constant`

          - `CITATIONS_DELTA("citations_delta")`

      - `class BetaThinkingDelta:`

        - `thinking: String`

        - `type: JsonValue; "thinking_delta"constant`

          - `THINKING_DELTA("thinking_delta")`

      - `class BetaSignatureDelta:`

        - `signature: String`

        - `type: JsonValue; "signature_delta"constant`

          - `SIGNATURE_DELTA("signature_delta")`

    - `index: Long`

    - `type: JsonValue; "content_block_delta"constant`

      - `CONTENT_BLOCK_DELTA("content_block_delta")`

  - `class BetaRawContentBlockStopEvent:`

    - `index: Long`

    - `type: JsonValue; "content_block_stop"constant`

      - `CONTENT_BLOCK_STOP("content_block_stop")`

### Beta Redacted Thinking Block

- `class BetaRedactedThinkingBlock:`

  - `data: String`

  - `type: JsonValue; "redacted_thinking"constant`

    - `REDACTED_THINKING("redacted_thinking")`

### Beta Redacted Thinking Block Param

- `class BetaRedactedThinkingBlockParam:`

  - `data: String`

  - `type: JsonValue; "redacted_thinking"constant`

    - `REDACTED_THINKING("redacted_thinking")`

### Beta Request Document Block

- `class BetaRequestDocumentBlock:`

  - `source: Source`

    - `class BetaBase64PdfSource:`

      - `data: String`

      - `mediaType: JsonValue; "application/pdf"constant`

        - `APPLICATION_PDF("application/pdf")`

      - `type: JsonValue; "base64"constant`

        - `BASE64("base64")`

    - `class BetaPlainTextSource:`

      - `data: String`

      - `mediaType: JsonValue; "text/plain"constant`

        - `TEXT_PLAIN("text/plain")`

      - `type: JsonValue; "text"constant`

        - `TEXT("text")`

    - `class BetaContentBlockSource:`

      - `content: Content`

        - `String`

        - `List<BetaContentBlockSourceContent>`

          - `class BetaTextBlockParam:`

            - `text: String`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

            - `cacheControl: Optional<BetaCacheControlEphemeral>`

              Create a cache control breakpoint at this content block.

              - `type: JsonValue; "ephemeral"constant`

                - `EPHEMERAL("ephemeral")`

              - `ttl: Optional<Ttl>`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `TTL_5M("5m")`

                - `TTL_1H("1h")`

            - `citations: Optional<List<BetaTextCitationParam>>`

              - `class BetaCitationCharLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endCharIndex: Long`

                - `startCharIndex: Long`

                - `type: JsonValue; "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class BetaCitationPageLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endPageNumber: Long`

                - `startPageNumber: Long`

                - `type: JsonValue; "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class BetaCitationContentBlockLocationParam:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endBlockIndex: Long`

                - `startBlockIndex: Long`

                - `type: JsonValue; "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class BetaCitationWebSearchResultLocationParam:`

                - `citedText: String`

                - `encryptedIndex: String`

                - `title: Optional<String>`

                - `type: JsonValue; "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `url: String`

              - `class BetaCitationSearchResultLocationParam:`

                - `citedText: String`

                - `endBlockIndex: Long`

                - `searchResultIndex: Long`

                - `source: String`

                - `startBlockIndex: Long`

                - `title: Optional<String>`

                - `type: JsonValue; "search_result_location"constant`

                  - `SEARCH_RESULT_LOCATION("search_result_location")`

          - `class BetaImageBlockParam:`

            - `source: Source`

              - `class BetaBase64ImageSource:`

                - `data: String`

                - `mediaType: MediaType`

                  - `IMAGE_JPEG("image/jpeg")`

                  - `IMAGE_PNG("image/png")`

                  - `IMAGE_GIF("image/gif")`

                  - `IMAGE_WEBP("image/webp")`

                - `type: JsonValue; "base64"constant`

                  - `BASE64("base64")`

              - `class BetaUrlImageSource:`

                - `type: JsonValue; "url"constant`

                  - `URL("url")`

                - `url: String`

              - `class BetaFileImageSource:`

                - `fileId: String`

                - `type: JsonValue; "file"constant`

                  - `FILE("file")`

            - `type: JsonValue; "image"constant`

              - `IMAGE("image")`

            - `cacheControl: Optional<BetaCacheControlEphemeral>`

              Create a cache control breakpoint at this content block.

              - `type: JsonValue; "ephemeral"constant`

                - `EPHEMERAL("ephemeral")`

              - `ttl: Optional<Ttl>`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `TTL_5M("5m")`

                - `TTL_1H("1h")`

      - `type: JsonValue; "content"constant`

        - `CONTENT("content")`

    - `class BetaUrlPdfSource:`

      - `type: JsonValue; "url"constant`

        - `URL("url")`

      - `url: String`

    - `class BetaFileDocumentSource:`

      - `fileId: String`

      - `type: JsonValue; "file"constant`

        - `FILE("file")`

  - `type: JsonValue; "document"constant`

    - `DOCUMENT("document")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `citations: Optional<BetaCitationsConfigParam>`

    - `enabled: Optional<Boolean>`

  - `context: Optional<String>`

  - `title: Optional<String>`

### Beta Request MCP Server Tool Configuration

- `class BetaRequestMcpServerToolConfiguration:`

  - `allowedTools: Optional<List<String>>`

  - `enabled: Optional<Boolean>`

### Beta Request MCP Server URL Definition

- `class BetaRequestMcpServerUrlDefinition:`

  - `name: String`

  - `type: JsonValue; "url"constant`

    - `URL("url")`

  - `url: String`

  - `authorizationToken: Optional<String>`

  - `toolConfiguration: Optional<BetaRequestMcpServerToolConfiguration>`

    - `allowedTools: Optional<List<String>>`

    - `enabled: Optional<Boolean>`

### Beta Request MCP Tool Result Block Param

- `class BetaRequestMcpToolResultBlockParam:`

  - `toolUseId: String`

  - `type: JsonValue; "mcp_tool_result"constant`

    - `MCP_TOOL_RESULT("mcp_tool_result")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `content: Optional<Content>`

    - `String`

    - `List<BetaTextBlockParam>`

      - `text: String`

      - `type: JsonValue; "text"constant`

        - `TEXT("text")`

      - `cacheControl: Optional<BetaCacheControlEphemeral>`

        Create a cache control breakpoint at this content block.

        - `type: JsonValue; "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `ttl: Optional<Ttl>`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `citations: Optional<List<BetaTextCitationParam>>`

        - `class BetaCitationCharLocationParam:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endCharIndex: Long`

          - `startCharIndex: Long`

          - `type: JsonValue; "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class BetaCitationPageLocationParam:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endPageNumber: Long`

          - `startPageNumber: Long`

          - `type: JsonValue; "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class BetaCitationContentBlockLocationParam:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endBlockIndex: Long`

          - `startBlockIndex: Long`

          - `type: JsonValue; "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class BetaCitationWebSearchResultLocationParam:`

          - `citedText: String`

          - `encryptedIndex: String`

          - `title: Optional<String>`

          - `type: JsonValue; "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `url: String`

        - `class BetaCitationSearchResultLocationParam:`

          - `citedText: String`

          - `endBlockIndex: Long`

          - `searchResultIndex: Long`

          - `source: String`

          - `startBlockIndex: Long`

          - `title: Optional<String>`

          - `type: JsonValue; "search_result_location"constant`

            - `SEARCH_RESULT_LOCATION("search_result_location")`

  - `isError: Optional<Boolean>`

### Beta Search Result Block Param

- `class BetaSearchResultBlockParam:`

  - `content: List<BetaTextBlockParam>`

    - `text: String`

    - `type: JsonValue; "text"constant`

      - `TEXT("text")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `citations: Optional<List<BetaTextCitationParam>>`

      - `class BetaCitationCharLocationParam:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endCharIndex: Long`

        - `startCharIndex: Long`

        - `type: JsonValue; "char_location"constant`

          - `CHAR_LOCATION("char_location")`

      - `class BetaCitationPageLocationParam:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endPageNumber: Long`

        - `startPageNumber: Long`

        - `type: JsonValue; "page_location"constant`

          - `PAGE_LOCATION("page_location")`

      - `class BetaCitationContentBlockLocationParam:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endBlockIndex: Long`

        - `startBlockIndex: Long`

        - `type: JsonValue; "content_block_location"constant`

          - `CONTENT_BLOCK_LOCATION("content_block_location")`

      - `class BetaCitationWebSearchResultLocationParam:`

        - `citedText: String`

        - `encryptedIndex: String`

        - `title: Optional<String>`

        - `type: JsonValue; "web_search_result_location"constant`

          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

        - `url: String`

      - `class BetaCitationSearchResultLocationParam:`

        - `citedText: String`

        - `endBlockIndex: Long`

        - `searchResultIndex: Long`

        - `source: String`

        - `startBlockIndex: Long`

        - `title: Optional<String>`

        - `type: JsonValue; "search_result_location"constant`

          - `SEARCH_RESULT_LOCATION("search_result_location")`

  - `source: String`

  - `title: String`

  - `type: JsonValue; "search_result"constant`

    - `SEARCH_RESULT("search_result")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `citations: Optional<BetaCitationsConfigParam>`

    - `enabled: Optional<Boolean>`

### Beta Server Tool Caller

- `class BetaServerToolCaller:`

  Tool invocation generated by a server-side tool.

  - `toolId: String`

  - `type: JsonValue; "code_execution_20250825"constant`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

### Beta Server Tool Usage

- `class BetaServerToolUsage:`

  - `webFetchRequests: Long`

    The number of web fetch tool requests.

  - `webSearchRequests: Long`

    The number of web search tool requests.

### Beta Server Tool Use Block

- `class BetaServerToolUseBlock:`

  - `id: String`

  - `caller: Caller`

    Tool invocation directly from the model.

    - `class BetaDirectCaller:`

      Tool invocation directly from the model.

      - `type: JsonValue; "direct"constant`

        - `DIRECT("direct")`

    - `class BetaServerToolCaller:`

      Tool invocation generated by a server-side tool.

      - `toolId: String`

      - `type: JsonValue; "code_execution_20250825"constant`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `input: Input`

  - `name: Name`

    - `WEB_SEARCH("web_search")`

    - `WEB_FETCH("web_fetch")`

    - `CODE_EXECUTION("code_execution")`

    - `BASH_CODE_EXECUTION("bash_code_execution")`

    - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

    - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

    - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

  - `type: JsonValue; "server_tool_use"constant`

    - `SERVER_TOOL_USE("server_tool_use")`

### Beta Server Tool Use Block Param

- `class BetaServerToolUseBlockParam:`

  - `id: String`

  - `input: Input`

  - `name: Name`

    - `WEB_SEARCH("web_search")`

    - `WEB_FETCH("web_fetch")`

    - `CODE_EXECUTION("code_execution")`

    - `BASH_CODE_EXECUTION("bash_code_execution")`

    - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

    - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

    - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

  - `type: JsonValue; "server_tool_use"constant`

    - `SERVER_TOOL_USE("server_tool_use")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `caller: Optional<Caller>`

    Tool invocation directly from the model.

    - `class BetaDirectCaller:`

      Tool invocation directly from the model.

      - `type: JsonValue; "direct"constant`

        - `DIRECT("direct")`

    - `class BetaServerToolCaller:`

      Tool invocation generated by a server-side tool.

      - `toolId: String`

      - `type: JsonValue; "code_execution_20250825"constant`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

### Beta Signature Delta

- `class BetaSignatureDelta:`

  - `signature: String`

  - `type: JsonValue; "signature_delta"constant`

    - `SIGNATURE_DELTA("signature_delta")`

### Beta Skill

- `class BetaSkill:`

  A skill that was loaded in a container (response model).

  - `skillId: String`

    Skill ID

  - `type: Type`

    Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

    - `ANTHROPIC("anthropic")`

    - `CUSTOM("custom")`

  - `version: String`

    Skill version or 'latest' for most recent version

### Beta Skill Params

- `class BetaSkillParams:`

  Specification for a skill to be loaded in a container (request model).

  - `skillId: String`

    Skill ID

  - `type: Type`

    Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

    - `ANTHROPIC("anthropic")`

    - `CUSTOM("custom")`

  - `version: Optional<String>`

    Skill version or 'latest' for most recent version

### Beta Stop Reason

- `enum class BetaStopReason:`

  - `END_TURN("end_turn")`

  - `MAX_TOKENS("max_tokens")`

  - `STOP_SEQUENCE("stop_sequence")`

  - `TOOL_USE("tool_use")`

  - `PAUSE_TURN("pause_turn")`

  - `REFUSAL("refusal")`

  - `MODEL_CONTEXT_WINDOW_EXCEEDED("model_context_window_exceeded")`

### Beta Text Block

- `class BetaTextBlock:`

  - `citations: Optional<List<BetaTextCitation>>`

    Citations supporting the text block.

    The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

    - `class BetaCitationCharLocation:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endCharIndex: Long`

      - `fileId: Optional<String>`

      - `startCharIndex: Long`

      - `type: JsonValue; "char_location"constant`

        - `CHAR_LOCATION("char_location")`

    - `class BetaCitationPageLocation:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endPageNumber: Long`

      - `fileId: Optional<String>`

      - `startPageNumber: Long`

      - `type: JsonValue; "page_location"constant`

        - `PAGE_LOCATION("page_location")`

    - `class BetaCitationContentBlockLocation:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endBlockIndex: Long`

      - `fileId: Optional<String>`

      - `startBlockIndex: Long`

      - `type: JsonValue; "content_block_location"constant`

        - `CONTENT_BLOCK_LOCATION("content_block_location")`

    - `class BetaCitationsWebSearchResultLocation:`

      - `citedText: String`

      - `encryptedIndex: String`

      - `title: Optional<String>`

      - `type: JsonValue; "web_search_result_location"constant`

        - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

      - `url: String`

    - `class BetaCitationSearchResultLocation:`

      - `citedText: String`

      - `endBlockIndex: Long`

      - `searchResultIndex: Long`

      - `source: String`

      - `startBlockIndex: Long`

      - `title: Optional<String>`

      - `type: JsonValue; "search_result_location"constant`

        - `SEARCH_RESULT_LOCATION("search_result_location")`

  - `text: String`

  - `type: JsonValue; "text"constant`

    - `TEXT("text")`

### Beta Text Block Param

- `class BetaTextBlockParam:`

  - `text: String`

  - `type: JsonValue; "text"constant`

    - `TEXT("text")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `citations: Optional<List<BetaTextCitationParam>>`

    - `class BetaCitationCharLocationParam:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endCharIndex: Long`

      - `startCharIndex: Long`

      - `type: JsonValue; "char_location"constant`

        - `CHAR_LOCATION("char_location")`

    - `class BetaCitationPageLocationParam:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endPageNumber: Long`

      - `startPageNumber: Long`

      - `type: JsonValue; "page_location"constant`

        - `PAGE_LOCATION("page_location")`

    - `class BetaCitationContentBlockLocationParam:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endBlockIndex: Long`

      - `startBlockIndex: Long`

      - `type: JsonValue; "content_block_location"constant`

        - `CONTENT_BLOCK_LOCATION("content_block_location")`

    - `class BetaCitationWebSearchResultLocationParam:`

      - `citedText: String`

      - `encryptedIndex: String`

      - `title: Optional<String>`

      - `type: JsonValue; "web_search_result_location"constant`

        - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

      - `url: String`

    - `class BetaCitationSearchResultLocationParam:`

      - `citedText: String`

      - `endBlockIndex: Long`

      - `searchResultIndex: Long`

      - `source: String`

      - `startBlockIndex: Long`

      - `title: Optional<String>`

      - `type: JsonValue; "search_result_location"constant`

        - `SEARCH_RESULT_LOCATION("search_result_location")`

### Beta Text Citation

- `class BetaTextCitation: A class that can be one of several variants.union`

  - `class BetaCitationCharLocation:`

    - `citedText: String`

    - `documentIndex: Long`

    - `documentTitle: Optional<String>`

    - `endCharIndex: Long`

    - `fileId: Optional<String>`

    - `startCharIndex: Long`

    - `type: JsonValue; "char_location"constant`

      - `CHAR_LOCATION("char_location")`

  - `class BetaCitationPageLocation:`

    - `citedText: String`

    - `documentIndex: Long`

    - `documentTitle: Optional<String>`

    - `endPageNumber: Long`

    - `fileId: Optional<String>`

    - `startPageNumber: Long`

    - `type: JsonValue; "page_location"constant`

      - `PAGE_LOCATION("page_location")`

  - `class BetaCitationContentBlockLocation:`

    - `citedText: String`

    - `documentIndex: Long`

    - `documentTitle: Optional<String>`

    - `endBlockIndex: Long`

    - `fileId: Optional<String>`

    - `startBlockIndex: Long`

    - `type: JsonValue; "content_block_location"constant`

      - `CONTENT_BLOCK_LOCATION("content_block_location")`

  - `class BetaCitationsWebSearchResultLocation:`

    - `citedText: String`

    - `encryptedIndex: String`

    - `title: Optional<String>`

    - `type: JsonValue; "web_search_result_location"constant`

      - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

    - `url: String`

  - `class BetaCitationSearchResultLocation:`

    - `citedText: String`

    - `endBlockIndex: Long`

    - `searchResultIndex: Long`

    - `source: String`

    - `startBlockIndex: Long`

    - `title: Optional<String>`

    - `type: JsonValue; "search_result_location"constant`

      - `SEARCH_RESULT_LOCATION("search_result_location")`

### Beta Text Citation Param

- `class BetaTextCitationParam: A class that can be one of several variants.union`

  - `class BetaCitationCharLocationParam:`

    - `citedText: String`

    - `documentIndex: Long`

    - `documentTitle: Optional<String>`

    - `endCharIndex: Long`

    - `startCharIndex: Long`

    - `type: JsonValue; "char_location"constant`

      - `CHAR_LOCATION("char_location")`

  - `class BetaCitationPageLocationParam:`

    - `citedText: String`

    - `documentIndex: Long`

    - `documentTitle: Optional<String>`

    - `endPageNumber: Long`

    - `startPageNumber: Long`

    - `type: JsonValue; "page_location"constant`

      - `PAGE_LOCATION("page_location")`

  - `class BetaCitationContentBlockLocationParam:`

    - `citedText: String`

    - `documentIndex: Long`

    - `documentTitle: Optional<String>`

    - `endBlockIndex: Long`

    - `startBlockIndex: Long`

    - `type: JsonValue; "content_block_location"constant`

      - `CONTENT_BLOCK_LOCATION("content_block_location")`

  - `class BetaCitationWebSearchResultLocationParam:`

    - `citedText: String`

    - `encryptedIndex: String`

    - `title: Optional<String>`

    - `type: JsonValue; "web_search_result_location"constant`

      - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

    - `url: String`

  - `class BetaCitationSearchResultLocationParam:`

    - `citedText: String`

    - `endBlockIndex: Long`

    - `searchResultIndex: Long`

    - `source: String`

    - `startBlockIndex: Long`

    - `title: Optional<String>`

    - `type: JsonValue; "search_result_location"constant`

      - `SEARCH_RESULT_LOCATION("search_result_location")`

### Beta Text Delta

- `class BetaTextDelta:`

  - `text: String`

  - `type: JsonValue; "text_delta"constant`

    - `TEXT_DELTA("text_delta")`

### Beta Text Editor Code Execution Create Result Block

- `class BetaTextEditorCodeExecutionCreateResultBlock:`

  - `isFileUpdate: Boolean`

  - `type: JsonValue; "text_editor_code_execution_create_result"constant`

    - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

### Beta Text Editor Code Execution Create Result Block Param

- `class BetaTextEditorCodeExecutionCreateResultBlockParam:`

  - `isFileUpdate: Boolean`

  - `type: JsonValue; "text_editor_code_execution_create_result"constant`

    - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

### Beta Text Editor Code Execution Str Replace Result Block

- `class BetaTextEditorCodeExecutionStrReplaceResultBlock:`

  - `lines: Optional<List<String>>`

  - `newLines: Optional<Long>`

  - `newStart: Optional<Long>`

  - `oldLines: Optional<Long>`

  - `oldStart: Optional<Long>`

  - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

    - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

### Beta Text Editor Code Execution Str Replace Result Block Param

- `class BetaTextEditorCodeExecutionStrReplaceResultBlockParam:`

  - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

    - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

  - `lines: Optional<List<String>>`

  - `newLines: Optional<Long>`

  - `newStart: Optional<Long>`

  - `oldLines: Optional<Long>`

  - `oldStart: Optional<Long>`

### Beta Text Editor Code Execution Tool Result Block

- `class BetaTextEditorCodeExecutionToolResultBlock:`

  - `content: Content`

    - `class BetaTextEditorCodeExecutionToolResultError:`

      - `errorCode: ErrorCode`

        - `INVALID_TOOL_INPUT("invalid_tool_input")`

        - `UNAVAILABLE("unavailable")`

        - `TOO_MANY_REQUESTS("too_many_requests")`

        - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

        - `FILE_NOT_FOUND("file_not_found")`

      - `errorMessage: Optional<String>`

      - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

        - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

    - `class BetaTextEditorCodeExecutionViewResultBlock:`

      - `content: String`

      - `fileType: FileType`

        - `TEXT("text")`

        - `IMAGE("image")`

        - `PDF("pdf")`

      - `numLines: Optional<Long>`

      - `startLine: Optional<Long>`

      - `totalLines: Optional<Long>`

      - `type: JsonValue; "text_editor_code_execution_view_result"constant`

        - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

    - `class BetaTextEditorCodeExecutionCreateResultBlock:`

      - `isFileUpdate: Boolean`

      - `type: JsonValue; "text_editor_code_execution_create_result"constant`

        - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

    - `class BetaTextEditorCodeExecutionStrReplaceResultBlock:`

      - `lines: Optional<List<String>>`

      - `newLines: Optional<Long>`

      - `newStart: Optional<Long>`

      - `oldLines: Optional<Long>`

      - `oldStart: Optional<Long>`

      - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

        - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

  - `toolUseId: String`

  - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

    - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

### Beta Text Editor Code Execution Tool Result Block Param

- `class BetaTextEditorCodeExecutionToolResultBlockParam:`

  - `content: Content`

    - `class BetaTextEditorCodeExecutionToolResultErrorParam:`

      - `errorCode: ErrorCode`

        - `INVALID_TOOL_INPUT("invalid_tool_input")`

        - `UNAVAILABLE("unavailable")`

        - `TOO_MANY_REQUESTS("too_many_requests")`

        - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

        - `FILE_NOT_FOUND("file_not_found")`

      - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

        - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

      - `errorMessage: Optional<String>`

    - `class BetaTextEditorCodeExecutionViewResultBlockParam:`

      - `content: String`

      - `fileType: FileType`

        - `TEXT("text")`

        - `IMAGE("image")`

        - `PDF("pdf")`

      - `type: JsonValue; "text_editor_code_execution_view_result"constant`

        - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

      - `numLines: Optional<Long>`

      - `startLine: Optional<Long>`

      - `totalLines: Optional<Long>`

    - `class BetaTextEditorCodeExecutionCreateResultBlockParam:`

      - `isFileUpdate: Boolean`

      - `type: JsonValue; "text_editor_code_execution_create_result"constant`

        - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

    - `class BetaTextEditorCodeExecutionStrReplaceResultBlockParam:`

      - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

        - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

      - `lines: Optional<List<String>>`

      - `newLines: Optional<Long>`

      - `newStart: Optional<Long>`

      - `oldLines: Optional<Long>`

      - `oldStart: Optional<Long>`

  - `toolUseId: String`

  - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

    - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

### Beta Text Editor Code Execution Tool Result Error

- `class BetaTextEditorCodeExecutionToolResultError:`

  - `errorCode: ErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `UNAVAILABLE("unavailable")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

    - `FILE_NOT_FOUND("file_not_found")`

  - `errorMessage: Optional<String>`

  - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

    - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

### Beta Text Editor Code Execution Tool Result Error Param

- `class BetaTextEditorCodeExecutionToolResultErrorParam:`

  - `errorCode: ErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `UNAVAILABLE("unavailable")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

    - `FILE_NOT_FOUND("file_not_found")`

  - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

    - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

  - `errorMessage: Optional<String>`

### Beta Text Editor Code Execution View Result Block

- `class BetaTextEditorCodeExecutionViewResultBlock:`

  - `content: String`

  - `fileType: FileType`

    - `TEXT("text")`

    - `IMAGE("image")`

    - `PDF("pdf")`

  - `numLines: Optional<Long>`

  - `startLine: Optional<Long>`

  - `totalLines: Optional<Long>`

  - `type: JsonValue; "text_editor_code_execution_view_result"constant`

    - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

### Beta Text Editor Code Execution View Result Block Param

- `class BetaTextEditorCodeExecutionViewResultBlockParam:`

  - `content: String`

  - `fileType: FileType`

    - `TEXT("text")`

    - `IMAGE("image")`

    - `PDF("pdf")`

  - `type: JsonValue; "text_editor_code_execution_view_result"constant`

    - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

  - `numLines: Optional<Long>`

  - `startLine: Optional<Long>`

  - `totalLines: Optional<Long>`

### Beta Thinking Block

- `class BetaThinkingBlock:`

  - `signature: String`

  - `thinking: String`

  - `type: JsonValue; "thinking"constant`

    - `THINKING("thinking")`

### Beta Thinking Block Param

- `class BetaThinkingBlockParam:`

  - `signature: String`

  - `thinking: String`

  - `type: JsonValue; "thinking"constant`

    - `THINKING("thinking")`

### Beta Thinking Config Disabled

- `class BetaThinkingConfigDisabled:`

  - `type: JsonValue; "disabled"constant`

    - `DISABLED("disabled")`

### Beta Thinking Config Enabled

- `class BetaThinkingConfigEnabled:`

  - `budgetTokens: Long`

    Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

    Must be ≥1024 and less than `max_tokens`.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `type: JsonValue; "enabled"constant`

    - `ENABLED("enabled")`

### Beta Thinking Config Param

- `class BetaThinkingConfigParam: A class that can be one of several variants.union`

  Configuration for enabling Claude's extended thinking.

  When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

  See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `class BetaThinkingConfigEnabled:`

    - `budgetTokens: Long`

      Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

      Must be ≥1024 and less than `max_tokens`.

      See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

    - `type: JsonValue; "enabled"constant`

      - `ENABLED("enabled")`

  - `class BetaThinkingConfigDisabled:`

    - `type: JsonValue; "disabled"constant`

      - `DISABLED("disabled")`

### Beta Thinking Delta

- `class BetaThinkingDelta:`

  - `thinking: String`

  - `type: JsonValue; "thinking_delta"constant`

    - `THINKING_DELTA("thinking_delta")`

### Beta Thinking Turns

- `class BetaThinkingTurns:`

  - `type: JsonValue; "thinking_turns"constant`

    - `THINKING_TURNS("thinking_turns")`

  - `value: Long`

### Beta Tool

- `class BetaTool:`

  - `inputSchema: InputSchema`

    [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

    This defines the shape of the `input` that your tool accepts and that the model will produce.

    - `type: JsonValue; "object"constant`

      - `OBJECT("object")`

    - `properties: Optional<Properties>`

    - `required: Optional<List<String>>`

  - `name: String`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `description: Optional<String>`

    Description of what this tool does.

    Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

  - `inputExamples: Optional<List<InputExample>>`

  - `strict: Optional<Boolean>`

  - `type: Optional<Type>`

    - `CUSTOM("custom")`

### Beta Tool Bash 20241022

- `class BetaToolBash20241022:`

  - `name: JsonValue; "bash"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `BASH("bash")`

  - `type: JsonValue; "bash_20241022"constant`

    - `BASH_20241022("bash_20241022")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `inputExamples: Optional<List<InputExample>>`

  - `strict: Optional<Boolean>`

### Beta Tool Bash 20250124

- `class BetaToolBash20250124:`

  - `name: JsonValue; "bash"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `BASH("bash")`

  - `type: JsonValue; "bash_20250124"constant`

    - `BASH_20250124("bash_20250124")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `inputExamples: Optional<List<InputExample>>`

  - `strict: Optional<Boolean>`

### Beta Tool Choice

- `class BetaToolChoice: A class that can be one of several variants.union`

  How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `class BetaToolChoiceAuto:`

    The model will automatically decide whether to use tools.

    - `type: JsonValue; "auto"constant`

      - `AUTO("auto")`

    - `disableParallelToolUse: Optional<Boolean>`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output at most one tool use.

  - `class BetaToolChoiceAny:`

    The model will use any available tools.

    - `type: JsonValue; "any"constant`

      - `ANY("any")`

    - `disableParallelToolUse: Optional<Boolean>`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output exactly one tool use.

  - `class BetaToolChoiceTool:`

    The model will use the specified tool with `tool_choice.name`.

    - `name: String`

      The name of the tool to use.

    - `type: JsonValue; "tool"constant`

      - `TOOL("tool")`

    - `disableParallelToolUse: Optional<Boolean>`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output exactly one tool use.

  - `class BetaToolChoiceNone:`

    The model will not be allowed to use tools.

    - `type: JsonValue; "none"constant`

      - `NONE("none")`

### Beta Tool Choice Any

- `class BetaToolChoiceAny:`

  The model will use any available tools.

  - `type: JsonValue; "any"constant`

    - `ANY("any")`

  - `disableParallelToolUse: Optional<Boolean>`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output exactly one tool use.

### Beta Tool Choice Auto

- `class BetaToolChoiceAuto:`

  The model will automatically decide whether to use tools.

  - `type: JsonValue; "auto"constant`

    - `AUTO("auto")`

  - `disableParallelToolUse: Optional<Boolean>`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output at most one tool use.

### Beta Tool Choice None

- `class BetaToolChoiceNone:`

  The model will not be allowed to use tools.

  - `type: JsonValue; "none"constant`

    - `NONE("none")`

### Beta Tool Choice Tool

- `class BetaToolChoiceTool:`

  The model will use the specified tool with `tool_choice.name`.

  - `name: String`

    The name of the tool to use.

  - `type: JsonValue; "tool"constant`

    - `TOOL("tool")`

  - `disableParallelToolUse: Optional<Boolean>`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output exactly one tool use.

### Beta Tool Computer Use 20241022

- `class BetaToolComputerUse20241022:`

  - `displayHeightPx: Long`

    The height of the display in pixels.

  - `displayWidthPx: Long`

    The width of the display in pixels.

  - `name: JsonValue; "computer"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `COMPUTER("computer")`

  - `type: JsonValue; "computer_20241022"constant`

    - `COMPUTER_20241022("computer_20241022")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `displayNumber: Optional<Long>`

    The X11 display number (e.g. 0, 1) for the display.

  - `inputExamples: Optional<List<InputExample>>`

  - `strict: Optional<Boolean>`

### Beta Tool Computer Use 20250124

- `class BetaToolComputerUse20250124:`

  - `displayHeightPx: Long`

    The height of the display in pixels.

  - `displayWidthPx: Long`

    The width of the display in pixels.

  - `name: JsonValue; "computer"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `COMPUTER("computer")`

  - `type: JsonValue; "computer_20250124"constant`

    - `COMPUTER_20250124("computer_20250124")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `displayNumber: Optional<Long>`

    The X11 display number (e.g. 0, 1) for the display.

  - `inputExamples: Optional<List<InputExample>>`

  - `strict: Optional<Boolean>`

### Beta Tool Computer Use 20251124

- `class BetaToolComputerUse20251124:`

  - `displayHeightPx: Long`

    The height of the display in pixels.

  - `displayWidthPx: Long`

    The width of the display in pixels.

  - `name: JsonValue; "computer"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `COMPUTER("computer")`

  - `type: JsonValue; "computer_20251124"constant`

    - `COMPUTER_20251124("computer_20251124")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `displayNumber: Optional<Long>`

    The X11 display number (e.g. 0, 1) for the display.

  - `enableZoom: Optional<Boolean>`

    Whether to enable an action to take a zoomed-in screenshot of the screen.

  - `inputExamples: Optional<List<InputExample>>`

  - `strict: Optional<Boolean>`

### Beta Tool Reference Block

- `class BetaToolReferenceBlock:`

  - `toolName: String`

  - `type: JsonValue; "tool_reference"constant`

    - `TOOL_REFERENCE("tool_reference")`

### Beta Tool Reference Block Param

- `class BetaToolReferenceBlockParam:`

  Tool reference block that can be included in tool_result content.

  - `toolName: String`

  - `type: JsonValue; "tool_reference"constant`

    - `TOOL_REFERENCE("tool_reference")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

### Beta Tool Result Block Param

- `class BetaToolResultBlockParam:`

  - `toolUseId: String`

  - `type: JsonValue; "tool_result"constant`

    - `TOOL_RESULT("tool_result")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `content: Optional<Content>`

    - `String`

    - `List<Block>`

      - `class BetaTextBlockParam:`

        - `text: String`

        - `type: JsonValue; "text"constant`

          - `TEXT("text")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

        - `citations: Optional<List<BetaTextCitationParam>>`

          - `class BetaCitationCharLocationParam:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endCharIndex: Long`

            - `startCharIndex: Long`

            - `type: JsonValue; "char_location"constant`

              - `CHAR_LOCATION("char_location")`

          - `class BetaCitationPageLocationParam:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endPageNumber: Long`

            - `startPageNumber: Long`

            - `type: JsonValue; "page_location"constant`

              - `PAGE_LOCATION("page_location")`

          - `class BetaCitationContentBlockLocationParam:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endBlockIndex: Long`

            - `startBlockIndex: Long`

            - `type: JsonValue; "content_block_location"constant`

              - `CONTENT_BLOCK_LOCATION("content_block_location")`

          - `class BetaCitationWebSearchResultLocationParam:`

            - `citedText: String`

            - `encryptedIndex: String`

            - `title: Optional<String>`

            - `type: JsonValue; "web_search_result_location"constant`

              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

            - `url: String`

          - `class BetaCitationSearchResultLocationParam:`

            - `citedText: String`

            - `endBlockIndex: Long`

            - `searchResultIndex: Long`

            - `source: String`

            - `startBlockIndex: Long`

            - `title: Optional<String>`

            - `type: JsonValue; "search_result_location"constant`

              - `SEARCH_RESULT_LOCATION("search_result_location")`

      - `class BetaImageBlockParam:`

        - `source: Source`

          - `class BetaBase64ImageSource:`

            - `data: String`

            - `mediaType: MediaType`

              - `IMAGE_JPEG("image/jpeg")`

              - `IMAGE_PNG("image/png")`

              - `IMAGE_GIF("image/gif")`

              - `IMAGE_WEBP("image/webp")`

            - `type: JsonValue; "base64"constant`

              - `BASE64("base64")`

          - `class BetaUrlImageSource:`

            - `type: JsonValue; "url"constant`

              - `URL("url")`

            - `url: String`

          - `class BetaFileImageSource:`

            - `fileId: String`

            - `type: JsonValue; "file"constant`

              - `FILE("file")`

        - `type: JsonValue; "image"constant`

          - `IMAGE("image")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

      - `class BetaSearchResultBlockParam:`

        - `content: List<BetaTextBlockParam>`

          - `text: String`

          - `type: JsonValue; "text"constant`

            - `TEXT("text")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<List<BetaTextCitationParam>>`

            - `class BetaCitationCharLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class BetaCitationPageLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class BetaCitationContentBlockLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class BetaCitationWebSearchResultLocationParam:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class BetaCitationSearchResultLocationParam:`

              - `citedText: String`

              - `endBlockIndex: Long`

              - `searchResultIndex: Long`

              - `source: String`

              - `startBlockIndex: Long`

              - `title: Optional<String>`

              - `type: JsonValue; "search_result_location"constant`

                - `SEARCH_RESULT_LOCATION("search_result_location")`

        - `source: String`

        - `title: String`

        - `type: JsonValue; "search_result"constant`

          - `SEARCH_RESULT("search_result")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

        - `citations: Optional<BetaCitationsConfigParam>`

          - `enabled: Optional<Boolean>`

      - `class BetaRequestDocumentBlock:`

        - `source: Source`

          - `class BetaBase64PdfSource:`

            - `data: String`

            - `mediaType: JsonValue; "application/pdf"constant`

              - `APPLICATION_PDF("application/pdf")`

            - `type: JsonValue; "base64"constant`

              - `BASE64("base64")`

          - `class BetaPlainTextSource:`

            - `data: String`

            - `mediaType: JsonValue; "text/plain"constant`

              - `TEXT_PLAIN("text/plain")`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

          - `class BetaContentBlockSource:`

            - `content: Content`

              - `String`

              - `List<BetaContentBlockSourceContent>`

                - `class BetaTextBlockParam:`

                  - `text: String`

                  - `type: JsonValue; "text"constant`

                    - `TEXT("text")`

                  - `cacheControl: Optional<BetaCacheControlEphemeral>`

                    Create a cache control breakpoint at this content block.

                    - `type: JsonValue; "ephemeral"constant`

                      - `EPHEMERAL("ephemeral")`

                    - `ttl: Optional<Ttl>`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `TTL_5M("5m")`

                      - `TTL_1H("1h")`

                  - `citations: Optional<List<BetaTextCitationParam>>`

                    - `class BetaCitationCharLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endCharIndex: Long`

                      - `startCharIndex: Long`

                      - `type: JsonValue; "char_location"constant`

                        - `CHAR_LOCATION("char_location")`

                    - `class BetaCitationPageLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endPageNumber: Long`

                      - `startPageNumber: Long`

                      - `type: JsonValue; "page_location"constant`

                        - `PAGE_LOCATION("page_location")`

                    - `class BetaCitationContentBlockLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endBlockIndex: Long`

                      - `startBlockIndex: Long`

                      - `type: JsonValue; "content_block_location"constant`

                        - `CONTENT_BLOCK_LOCATION("content_block_location")`

                    - `class BetaCitationWebSearchResultLocationParam:`

                      - `citedText: String`

                      - `encryptedIndex: String`

                      - `title: Optional<String>`

                      - `type: JsonValue; "web_search_result_location"constant`

                        - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                      - `url: String`

                    - `class BetaCitationSearchResultLocationParam:`

                      - `citedText: String`

                      - `endBlockIndex: Long`

                      - `searchResultIndex: Long`

                      - `source: String`

                      - `startBlockIndex: Long`

                      - `title: Optional<String>`

                      - `type: JsonValue; "search_result_location"constant`

                        - `SEARCH_RESULT_LOCATION("search_result_location")`

                - `class BetaImageBlockParam:`

                  - `source: Source`

                    - `class BetaBase64ImageSource:`

                      - `data: String`

                      - `mediaType: MediaType`

                        - `IMAGE_JPEG("image/jpeg")`

                        - `IMAGE_PNG("image/png")`

                        - `IMAGE_GIF("image/gif")`

                        - `IMAGE_WEBP("image/webp")`

                      - `type: JsonValue; "base64"constant`

                        - `BASE64("base64")`

                    - `class BetaUrlImageSource:`

                      - `type: JsonValue; "url"constant`

                        - `URL("url")`

                      - `url: String`

                    - `class BetaFileImageSource:`

                      - `fileId: String`

                      - `type: JsonValue; "file"constant`

                        - `FILE("file")`

                  - `type: JsonValue; "image"constant`

                    - `IMAGE("image")`

                  - `cacheControl: Optional<BetaCacheControlEphemeral>`

                    Create a cache control breakpoint at this content block.

                    - `type: JsonValue; "ephemeral"constant`

                      - `EPHEMERAL("ephemeral")`

                    - `ttl: Optional<Ttl>`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `TTL_5M("5m")`

                      - `TTL_1H("1h")`

            - `type: JsonValue; "content"constant`

              - `CONTENT("content")`

          - `class BetaUrlPdfSource:`

            - `type: JsonValue; "url"constant`

              - `URL("url")`

            - `url: String`

          - `class BetaFileDocumentSource:`

            - `fileId: String`

            - `type: JsonValue; "file"constant`

              - `FILE("file")`

        - `type: JsonValue; "document"constant`

          - `DOCUMENT("document")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

        - `citations: Optional<BetaCitationsConfigParam>`

          - `enabled: Optional<Boolean>`

        - `context: Optional<String>`

        - `title: Optional<String>`

      - `class BetaToolReferenceBlockParam:`

        Tool reference block that can be included in tool_result content.

        - `toolName: String`

        - `type: JsonValue; "tool_reference"constant`

          - `TOOL_REFERENCE("tool_reference")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

  - `isError: Optional<Boolean>`

### Beta Tool Search Tool Bm25 20251119

- `class BetaToolSearchToolBm25_20251119:`

  - `name: JsonValue; "tool_search_tool_bm25"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

  - `type: Type`

    - `TOOL_SEARCH_TOOL_BM25_20251119("tool_search_tool_bm25_20251119")`

    - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `strict: Optional<Boolean>`

### Beta Tool Search Tool Regex 20251119

- `class BetaToolSearchToolRegex20251119:`

  - `name: JsonValue; "tool_search_tool_regex"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

  - `type: Type`

    - `TOOL_SEARCH_TOOL_REGEX_20251119("tool_search_tool_regex_20251119")`

    - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `strict: Optional<Boolean>`

### Beta Tool Search Tool Result Block

- `class BetaToolSearchToolResultBlock:`

  - `content: Content`

    - `class BetaToolSearchToolResultError:`

      - `errorCode: ErrorCode`

        - `INVALID_TOOL_INPUT("invalid_tool_input")`

        - `UNAVAILABLE("unavailable")`

        - `TOO_MANY_REQUESTS("too_many_requests")`

        - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

      - `errorMessage: Optional<String>`

      - `type: JsonValue; "tool_search_tool_result_error"constant`

        - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

    - `class BetaToolSearchToolSearchResultBlock:`

      - `toolReferences: List<BetaToolReferenceBlock>`

        - `toolName: String`

        - `type: JsonValue; "tool_reference"constant`

          - `TOOL_REFERENCE("tool_reference")`

      - `type: JsonValue; "tool_search_tool_search_result"constant`

        - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

  - `toolUseId: String`

  - `type: JsonValue; "tool_search_tool_result"constant`

    - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

### Beta Tool Search Tool Result Block Param

- `class BetaToolSearchToolResultBlockParam:`

  - `content: Content`

    - `class BetaToolSearchToolResultErrorParam:`

      - `errorCode: ErrorCode`

        - `INVALID_TOOL_INPUT("invalid_tool_input")`

        - `UNAVAILABLE("unavailable")`

        - `TOO_MANY_REQUESTS("too_many_requests")`

        - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

      - `type: JsonValue; "tool_search_tool_result_error"constant`

        - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

    - `class BetaToolSearchToolSearchResultBlockParam:`

      - `toolReferences: List<BetaToolReferenceBlockParam>`

        - `toolName: String`

        - `type: JsonValue; "tool_reference"constant`

          - `TOOL_REFERENCE("tool_reference")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

      - `type: JsonValue; "tool_search_tool_search_result"constant`

        - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

  - `toolUseId: String`

  - `type: JsonValue; "tool_search_tool_result"constant`

    - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

### Beta Tool Search Tool Result Error

- `class BetaToolSearchToolResultError:`

  - `errorCode: ErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `UNAVAILABLE("unavailable")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

  - `errorMessage: Optional<String>`

  - `type: JsonValue; "tool_search_tool_result_error"constant`

    - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

### Beta Tool Search Tool Result Error Param

- `class BetaToolSearchToolResultErrorParam:`

  - `errorCode: ErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `UNAVAILABLE("unavailable")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

  - `type: JsonValue; "tool_search_tool_result_error"constant`

    - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

### Beta Tool Search Tool Search Result Block

- `class BetaToolSearchToolSearchResultBlock:`

  - `toolReferences: List<BetaToolReferenceBlock>`

    - `toolName: String`

    - `type: JsonValue; "tool_reference"constant`

      - `TOOL_REFERENCE("tool_reference")`

  - `type: JsonValue; "tool_search_tool_search_result"constant`

    - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

### Beta Tool Search Tool Search Result Block Param

- `class BetaToolSearchToolSearchResultBlockParam:`

  - `toolReferences: List<BetaToolReferenceBlockParam>`

    - `toolName: String`

    - `type: JsonValue; "tool_reference"constant`

      - `TOOL_REFERENCE("tool_reference")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

  - `type: JsonValue; "tool_search_tool_search_result"constant`

    - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

### Beta Tool Text Editor 20241022

- `class BetaToolTextEditor20241022:`

  - `name: JsonValue; "str_replace_editor"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `STR_REPLACE_EDITOR("str_replace_editor")`

  - `type: JsonValue; "text_editor_20241022"constant`

    - `TEXT_EDITOR_20241022("text_editor_20241022")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `inputExamples: Optional<List<InputExample>>`

  - `strict: Optional<Boolean>`

### Beta Tool Text Editor 20250124

- `class BetaToolTextEditor20250124:`

  - `name: JsonValue; "str_replace_editor"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `STR_REPLACE_EDITOR("str_replace_editor")`

  - `type: JsonValue; "text_editor_20250124"constant`

    - `TEXT_EDITOR_20250124("text_editor_20250124")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `inputExamples: Optional<List<InputExample>>`

  - `strict: Optional<Boolean>`

### Beta Tool Text Editor 20250429

- `class BetaToolTextEditor20250429:`

  - `name: JsonValue; "str_replace_based_edit_tool"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

  - `type: JsonValue; "text_editor_20250429"constant`

    - `TEXT_EDITOR_20250429("text_editor_20250429")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `inputExamples: Optional<List<InputExample>>`

  - `strict: Optional<Boolean>`

### Beta Tool Text Editor 20250728

- `class BetaToolTextEditor20250728:`

  - `name: JsonValue; "str_replace_based_edit_tool"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

  - `type: JsonValue; "text_editor_20250728"constant`

    - `TEXT_EDITOR_20250728("text_editor_20250728")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `inputExamples: Optional<List<InputExample>>`

  - `maxCharacters: Optional<Long>`

    Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

  - `strict: Optional<Boolean>`

### Beta Tool Union

- `class BetaToolUnion: A class that can be one of several variants.union`

  Configuration for a group of tools from an MCP server.

  Allows configuring enabled status and defer_loading for all tools
  from an MCP server, with optional per-tool overrides.

  - `class BetaTool:`

    - `inputSchema: InputSchema`

      [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

      This defines the shape of the `input` that your tool accepts and that the model will produce.

      - `type: JsonValue; "object"constant`

        - `OBJECT("object")`

      - `properties: Optional<Properties>`

      - `required: Optional<List<String>>`

    - `name: String`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `description: Optional<String>`

      Description of what this tool does.

      Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

    - `inputExamples: Optional<List<InputExample>>`

    - `strict: Optional<Boolean>`

    - `type: Optional<Type>`

      - `CUSTOM("custom")`

  - `class BetaToolBash20241022:`

    - `name: JsonValue; "bash"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `BASH("bash")`

    - `type: JsonValue; "bash_20241022"constant`

      - `BASH_20241022("bash_20241022")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `inputExamples: Optional<List<InputExample>>`

    - `strict: Optional<Boolean>`

  - `class BetaToolBash20250124:`

    - `name: JsonValue; "bash"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `BASH("bash")`

    - `type: JsonValue; "bash_20250124"constant`

      - `BASH_20250124("bash_20250124")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `inputExamples: Optional<List<InputExample>>`

    - `strict: Optional<Boolean>`

  - `class BetaCodeExecutionTool20250522:`

    - `name: JsonValue; "code_execution"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `CODE_EXECUTION("code_execution")`

    - `type: JsonValue; "code_execution_20250522"constant`

      - `CODE_EXECUTION_20250522("code_execution_20250522")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `strict: Optional<Boolean>`

  - `class BetaCodeExecutionTool20250825:`

    - `name: JsonValue; "code_execution"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `CODE_EXECUTION("code_execution")`

    - `type: JsonValue; "code_execution_20250825"constant`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `strict: Optional<Boolean>`

  - `class BetaToolComputerUse20241022:`

    - `displayHeightPx: Long`

      The height of the display in pixels.

    - `displayWidthPx: Long`

      The width of the display in pixels.

    - `name: JsonValue; "computer"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `COMPUTER("computer")`

    - `type: JsonValue; "computer_20241022"constant`

      - `COMPUTER_20241022("computer_20241022")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `displayNumber: Optional<Long>`

      The X11 display number (e.g. 0, 1) for the display.

    - `inputExamples: Optional<List<InputExample>>`

    - `strict: Optional<Boolean>`

  - `class BetaMemoryTool20250818:`

    - `name: JsonValue; "memory"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `MEMORY("memory")`

    - `type: JsonValue; "memory_20250818"constant`

      - `MEMORY_20250818("memory_20250818")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `inputExamples: Optional<List<InputExample>>`

    - `strict: Optional<Boolean>`

  - `class BetaToolComputerUse20250124:`

    - `displayHeightPx: Long`

      The height of the display in pixels.

    - `displayWidthPx: Long`

      The width of the display in pixels.

    - `name: JsonValue; "computer"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `COMPUTER("computer")`

    - `type: JsonValue; "computer_20250124"constant`

      - `COMPUTER_20250124("computer_20250124")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `displayNumber: Optional<Long>`

      The X11 display number (e.g. 0, 1) for the display.

    - `inputExamples: Optional<List<InputExample>>`

    - `strict: Optional<Boolean>`

  - `class BetaToolTextEditor20241022:`

    - `name: JsonValue; "str_replace_editor"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `STR_REPLACE_EDITOR("str_replace_editor")`

    - `type: JsonValue; "text_editor_20241022"constant`

      - `TEXT_EDITOR_20241022("text_editor_20241022")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `inputExamples: Optional<List<InputExample>>`

    - `strict: Optional<Boolean>`

  - `class BetaToolComputerUse20251124:`

    - `displayHeightPx: Long`

      The height of the display in pixels.

    - `displayWidthPx: Long`

      The width of the display in pixels.

    - `name: JsonValue; "computer"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `COMPUTER("computer")`

    - `type: JsonValue; "computer_20251124"constant`

      - `COMPUTER_20251124("computer_20251124")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `displayNumber: Optional<Long>`

      The X11 display number (e.g. 0, 1) for the display.

    - `enableZoom: Optional<Boolean>`

      Whether to enable an action to take a zoomed-in screenshot of the screen.

    - `inputExamples: Optional<List<InputExample>>`

    - `strict: Optional<Boolean>`

  - `class BetaToolTextEditor20250124:`

    - `name: JsonValue; "str_replace_editor"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `STR_REPLACE_EDITOR("str_replace_editor")`

    - `type: JsonValue; "text_editor_20250124"constant`

      - `TEXT_EDITOR_20250124("text_editor_20250124")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `inputExamples: Optional<List<InputExample>>`

    - `strict: Optional<Boolean>`

  - `class BetaToolTextEditor20250429:`

    - `name: JsonValue; "str_replace_based_edit_tool"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

    - `type: JsonValue; "text_editor_20250429"constant`

      - `TEXT_EDITOR_20250429("text_editor_20250429")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `inputExamples: Optional<List<InputExample>>`

    - `strict: Optional<Boolean>`

  - `class BetaToolTextEditor20250728:`

    - `name: JsonValue; "str_replace_based_edit_tool"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

    - `type: JsonValue; "text_editor_20250728"constant`

      - `TEXT_EDITOR_20250728("text_editor_20250728")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `inputExamples: Optional<List<InputExample>>`

    - `maxCharacters: Optional<Long>`

      Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

    - `strict: Optional<Boolean>`

  - `class BetaWebSearchTool20250305:`

    - `name: JsonValue; "web_search"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `WEB_SEARCH("web_search")`

    - `type: JsonValue; "web_search_20250305"constant`

      - `WEB_SEARCH_20250305("web_search_20250305")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `allowedDomains: Optional<List<String>>`

      If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

    - `blockedDomains: Optional<List<String>>`

      If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `maxUses: Optional<Long>`

      Maximum number of times the tool can be used in the API request.

    - `strict: Optional<Boolean>`

    - `userLocation: Optional<UserLocation>`

      Parameters for the user's location. Used to provide more relevant search results.

      - `type: JsonValue; "approximate"constant`

        - `APPROXIMATE("approximate")`

      - `city: Optional<String>`

        The city of the user.

      - `country: Optional<String>`

        The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

      - `region: Optional<String>`

        The region of the user.

      - `timezone: Optional<String>`

        The [IANA timezone](https://nodatime.org/TimeZones) of the user.

  - `class BetaWebFetchTool20250910:`

    - `name: JsonValue; "web_fetch"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `WEB_FETCH("web_fetch")`

    - `type: JsonValue; "web_fetch_20250910"constant`

      - `WEB_FETCH_20250910("web_fetch_20250910")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `allowedDomains: Optional<List<String>>`

      List of domains to allow fetching from

    - `blockedDomains: Optional<List<String>>`

      List of domains to block fetching from

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `citations: Optional<BetaCitationsConfigParam>`

      Citations configuration for fetched documents. Citations are disabled by default.

      - `enabled: Optional<Boolean>`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `maxContentTokens: Optional<Long>`

      Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

    - `maxUses: Optional<Long>`

      Maximum number of times the tool can be used in the API request.

    - `strict: Optional<Boolean>`

  - `class BetaToolSearchToolBm25_20251119:`

    - `name: JsonValue; "tool_search_tool_bm25"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

    - `type: Type`

      - `TOOL_SEARCH_TOOL_BM25_20251119("tool_search_tool_bm25_20251119")`

      - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `strict: Optional<Boolean>`

  - `class BetaToolSearchToolRegex20251119:`

    - `name: JsonValue; "tool_search_tool_regex"constant`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

    - `type: Type`

      - `TOOL_SEARCH_TOOL_REGEX_20251119("tool_search_tool_regex_20251119")`

      - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

    - `allowedCallers: Optional<List<AllowedCaller>>`

      - `DIRECT("direct")`

      - `CODE_EXECUTION_20250825("code_execution_20250825")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `deferLoading: Optional<Boolean>`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `strict: Optional<Boolean>`

  - `class BetaMcpToolset:`

    Configuration for a group of tools from an MCP server.

    Allows configuring enabled status and defer_loading for all tools
    from an MCP server, with optional per-tool overrides.

    - `mcpServerName: String`

      Name of the MCP server to configure tools for

    - `type: JsonValue; "mcp_toolset"constant`

      - `MCP_TOOLSET("mcp_toolset")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `configs: Optional<Configs>`

      Configuration overrides for specific tools, keyed by tool name

      - `deferLoading: Optional<Boolean>`

      - `enabled: Optional<Boolean>`

    - `defaultConfig: Optional<BetaMcpToolDefaultConfig>`

      Default configuration applied to all tools from this server

      - `deferLoading: Optional<Boolean>`

      - `enabled: Optional<Boolean>`

### Beta Tool Use Block

- `class BetaToolUseBlock:`

  - `id: String`

  - `input: Input`

  - `name: String`

  - `type: JsonValue; "tool_use"constant`

    - `TOOL_USE("tool_use")`

  - `caller: Optional<Caller>`

    Tool invocation directly from the model.

    - `class BetaDirectCaller:`

      Tool invocation directly from the model.

      - `type: JsonValue; "direct"constant`

        - `DIRECT("direct")`

    - `class BetaServerToolCaller:`

      Tool invocation generated by a server-side tool.

      - `toolId: String`

      - `type: JsonValue; "code_execution_20250825"constant`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

### Beta Tool Use Block Param

- `class BetaToolUseBlockParam:`

  - `id: String`

  - `input: Input`

  - `name: String`

  - `type: JsonValue; "tool_use"constant`

    - `TOOL_USE("tool_use")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `caller: Optional<Caller>`

    Tool invocation directly from the model.

    - `class BetaDirectCaller:`

      Tool invocation directly from the model.

      - `type: JsonValue; "direct"constant`

        - `DIRECT("direct")`

    - `class BetaServerToolCaller:`

      Tool invocation generated by a server-side tool.

      - `toolId: String`

      - `type: JsonValue; "code_execution_20250825"constant`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

### Beta Tool Uses Keep

- `class BetaToolUsesKeep:`

  - `type: JsonValue; "tool_uses"constant`

    - `TOOL_USES("tool_uses")`

  - `value: Long`

### Beta Tool Uses Trigger

- `class BetaToolUsesTrigger:`

  - `type: JsonValue; "tool_uses"constant`

    - `TOOL_USES("tool_uses")`

  - `value: Long`

### Beta URL Image Source

- `class BetaUrlImageSource:`

  - `type: JsonValue; "url"constant`

    - `URL("url")`

  - `url: String`

### Beta URL PDF Source

- `class BetaUrlPdfSource:`

  - `type: JsonValue; "url"constant`

    - `URL("url")`

  - `url: String`

### Beta Usage

- `class BetaUsage:`

  - `cacheCreation: Optional<BetaCacheCreation>`

    Breakdown of cached tokens by TTL

    - `ephemeral1hInputTokens: Long`

      The number of input tokens used to create the 1 hour cache entry.

    - `ephemeral5mInputTokens: Long`

      The number of input tokens used to create the 5 minute cache entry.

  - `cacheCreationInputTokens: Optional<Long>`

    The number of input tokens used to create the cache entry.

  - `cacheReadInputTokens: Optional<Long>`

    The number of input tokens read from the cache.

  - `inputTokens: Long`

    The number of input tokens which were used.

  - `outputTokens: Long`

    The number of output tokens which were used.

  - `serverToolUse: Optional<BetaServerToolUsage>`

    The number of server tool requests.

    - `webFetchRequests: Long`

      The number of web fetch tool requests.

    - `webSearchRequests: Long`

      The number of web search tool requests.

  - `serviceTier: Optional<ServiceTier>`

    If the request used the priority, standard, or batch tier.

    - `STANDARD("standard")`

    - `PRIORITY("priority")`

    - `BATCH("batch")`

### Beta Web Fetch Block

- `class BetaWebFetchBlock:`

  - `content: BetaDocumentBlock`

    - `citations: Optional<BetaCitationConfig>`

      Citation configuration for the document

      - `enabled: Boolean`

    - `source: Source`

      - `class BetaBase64PdfSource:`

        - `data: String`

        - `mediaType: JsonValue; "application/pdf"constant`

          - `APPLICATION_PDF("application/pdf")`

        - `type: JsonValue; "base64"constant`

          - `BASE64("base64")`

      - `class BetaPlainTextSource:`

        - `data: String`

        - `mediaType: JsonValue; "text/plain"constant`

          - `TEXT_PLAIN("text/plain")`

        - `type: JsonValue; "text"constant`

          - `TEXT("text")`

    - `title: Optional<String>`

      The title of the document

    - `type: JsonValue; "document"constant`

      - `DOCUMENT("document")`

  - `retrievedAt: Optional<String>`

    ISO 8601 timestamp when the content was retrieved

  - `type: JsonValue; "web_fetch_result"constant`

    - `WEB_FETCH_RESULT("web_fetch_result")`

  - `url: String`

    Fetched content URL

### Beta Web Fetch Block Param

- `class BetaWebFetchBlockParam:`

  - `content: BetaRequestDocumentBlock`

    - `source: Source`

      - `class BetaBase64PdfSource:`

        - `data: String`

        - `mediaType: JsonValue; "application/pdf"constant`

          - `APPLICATION_PDF("application/pdf")`

        - `type: JsonValue; "base64"constant`

          - `BASE64("base64")`

      - `class BetaPlainTextSource:`

        - `data: String`

        - `mediaType: JsonValue; "text/plain"constant`

          - `TEXT_PLAIN("text/plain")`

        - `type: JsonValue; "text"constant`

          - `TEXT("text")`

      - `class BetaContentBlockSource:`

        - `content: Content`

          - `String`

          - `List<BetaContentBlockSourceContent>`

            - `class BetaTextBlockParam:`

              - `text: String`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<List<BetaTextCitationParam>>`

                - `class BetaCitationCharLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endCharIndex: Long`

                  - `startCharIndex: Long`

                  - `type: JsonValue; "char_location"constant`

                    - `CHAR_LOCATION("char_location")`

                - `class BetaCitationPageLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endPageNumber: Long`

                  - `startPageNumber: Long`

                  - `type: JsonValue; "page_location"constant`

                    - `PAGE_LOCATION("page_location")`

                - `class BetaCitationContentBlockLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endBlockIndex: Long`

                  - `startBlockIndex: Long`

                  - `type: JsonValue; "content_block_location"constant`

                    - `CONTENT_BLOCK_LOCATION("content_block_location")`

                - `class BetaCitationWebSearchResultLocationParam:`

                  - `citedText: String`

                  - `encryptedIndex: String`

                  - `title: Optional<String>`

                  - `type: JsonValue; "web_search_result_location"constant`

                    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                  - `url: String`

                - `class BetaCitationSearchResultLocationParam:`

                  - `citedText: String`

                  - `endBlockIndex: Long`

                  - `searchResultIndex: Long`

                  - `source: String`

                  - `startBlockIndex: Long`

                  - `title: Optional<String>`

                  - `type: JsonValue; "search_result_location"constant`

                    - `SEARCH_RESULT_LOCATION("search_result_location")`

            - `class BetaImageBlockParam:`

              - `source: Source`

                - `class BetaBase64ImageSource:`

                  - `data: String`

                  - `mediaType: MediaType`

                    - `IMAGE_JPEG("image/jpeg")`

                    - `IMAGE_PNG("image/png")`

                    - `IMAGE_GIF("image/gif")`

                    - `IMAGE_WEBP("image/webp")`

                  - `type: JsonValue; "base64"constant`

                    - `BASE64("base64")`

                - `class BetaUrlImageSource:`

                  - `type: JsonValue; "url"constant`

                    - `URL("url")`

                  - `url: String`

                - `class BetaFileImageSource:`

                  - `fileId: String`

                  - `type: JsonValue; "file"constant`

                    - `FILE("file")`

              - `type: JsonValue; "image"constant`

                - `IMAGE("image")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

        - `type: JsonValue; "content"constant`

          - `CONTENT("content")`

      - `class BetaUrlPdfSource:`

        - `type: JsonValue; "url"constant`

          - `URL("url")`

        - `url: String`

      - `class BetaFileDocumentSource:`

        - `fileId: String`

        - `type: JsonValue; "file"constant`

          - `FILE("file")`

    - `type: JsonValue; "document"constant`

      - `DOCUMENT("document")`

    - `cacheControl: Optional<BetaCacheControlEphemeral>`

      Create a cache control breakpoint at this content block.

      - `type: JsonValue; "ephemeral"constant`

        - `EPHEMERAL("ephemeral")`

      - `ttl: Optional<Ttl>`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `TTL_5M("5m")`

        - `TTL_1H("1h")`

    - `citations: Optional<BetaCitationsConfigParam>`

      - `enabled: Optional<Boolean>`

    - `context: Optional<String>`

    - `title: Optional<String>`

  - `type: JsonValue; "web_fetch_result"constant`

    - `WEB_FETCH_RESULT("web_fetch_result")`

  - `url: String`

    Fetched content URL

  - `retrievedAt: Optional<String>`

    ISO 8601 timestamp when the content was retrieved

### Beta Web Fetch Tool 20250910

- `class BetaWebFetchTool20250910:`

  - `name: JsonValue; "web_fetch"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `WEB_FETCH("web_fetch")`

  - `type: JsonValue; "web_fetch_20250910"constant`

    - `WEB_FETCH_20250910("web_fetch_20250910")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `allowedDomains: Optional<List<String>>`

    List of domains to allow fetching from

  - `blockedDomains: Optional<List<String>>`

    List of domains to block fetching from

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `citations: Optional<BetaCitationsConfigParam>`

    Citations configuration for fetched documents. Citations are disabled by default.

    - `enabled: Optional<Boolean>`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `maxContentTokens: Optional<Long>`

    Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

  - `maxUses: Optional<Long>`

    Maximum number of times the tool can be used in the API request.

  - `strict: Optional<Boolean>`

### Beta Web Fetch Tool Result Block

- `class BetaWebFetchToolResultBlock:`

  - `content: Content`

    - `class BetaWebFetchToolResultErrorBlock:`

      - `errorCode: BetaWebFetchToolResultErrorCode`

        - `INVALID_TOOL_INPUT("invalid_tool_input")`

        - `URL_TOO_LONG("url_too_long")`

        - `URL_NOT_ALLOWED("url_not_allowed")`

        - `URL_NOT_ACCESSIBLE("url_not_accessible")`

        - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

        - `TOO_MANY_REQUESTS("too_many_requests")`

        - `MAX_USES_EXCEEDED("max_uses_exceeded")`

        - `UNAVAILABLE("unavailable")`

      - `type: JsonValue; "web_fetch_tool_result_error"constant`

        - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

    - `class BetaWebFetchBlock:`

      - `content: BetaDocumentBlock`

        - `citations: Optional<BetaCitationConfig>`

          Citation configuration for the document

          - `enabled: Boolean`

        - `source: Source`

          - `class BetaBase64PdfSource:`

            - `data: String`

            - `mediaType: JsonValue; "application/pdf"constant`

              - `APPLICATION_PDF("application/pdf")`

            - `type: JsonValue; "base64"constant`

              - `BASE64("base64")`

          - `class BetaPlainTextSource:`

            - `data: String`

            - `mediaType: JsonValue; "text/plain"constant`

              - `TEXT_PLAIN("text/plain")`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

        - `title: Optional<String>`

          The title of the document

        - `type: JsonValue; "document"constant`

          - `DOCUMENT("document")`

      - `retrievedAt: Optional<String>`

        ISO 8601 timestamp when the content was retrieved

      - `type: JsonValue; "web_fetch_result"constant`

        - `WEB_FETCH_RESULT("web_fetch_result")`

      - `url: String`

        Fetched content URL

  - `toolUseId: String`

  - `type: JsonValue; "web_fetch_tool_result"constant`

    - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

### Beta Web Fetch Tool Result Block Param

- `class BetaWebFetchToolResultBlockParam:`

  - `content: Content`

    - `class BetaWebFetchToolResultErrorBlockParam:`

      - `errorCode: BetaWebFetchToolResultErrorCode`

        - `INVALID_TOOL_INPUT("invalid_tool_input")`

        - `URL_TOO_LONG("url_too_long")`

        - `URL_NOT_ALLOWED("url_not_allowed")`

        - `URL_NOT_ACCESSIBLE("url_not_accessible")`

        - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

        - `TOO_MANY_REQUESTS("too_many_requests")`

        - `MAX_USES_EXCEEDED("max_uses_exceeded")`

        - `UNAVAILABLE("unavailable")`

      - `type: JsonValue; "web_fetch_tool_result_error"constant`

        - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

    - `class BetaWebFetchBlockParam:`

      - `content: BetaRequestDocumentBlock`

        - `source: Source`

          - `class BetaBase64PdfSource:`

            - `data: String`

            - `mediaType: JsonValue; "application/pdf"constant`

              - `APPLICATION_PDF("application/pdf")`

            - `type: JsonValue; "base64"constant`

              - `BASE64("base64")`

          - `class BetaPlainTextSource:`

            - `data: String`

            - `mediaType: JsonValue; "text/plain"constant`

              - `TEXT_PLAIN("text/plain")`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

          - `class BetaContentBlockSource:`

            - `content: Content`

              - `String`

              - `List<BetaContentBlockSourceContent>`

                - `class BetaTextBlockParam:`

                  - `text: String`

                  - `type: JsonValue; "text"constant`

                    - `TEXT("text")`

                  - `cacheControl: Optional<BetaCacheControlEphemeral>`

                    Create a cache control breakpoint at this content block.

                    - `type: JsonValue; "ephemeral"constant`

                      - `EPHEMERAL("ephemeral")`

                    - `ttl: Optional<Ttl>`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `TTL_5M("5m")`

                      - `TTL_1H("1h")`

                  - `citations: Optional<List<BetaTextCitationParam>>`

                    - `class BetaCitationCharLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endCharIndex: Long`

                      - `startCharIndex: Long`

                      - `type: JsonValue; "char_location"constant`

                        - `CHAR_LOCATION("char_location")`

                    - `class BetaCitationPageLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endPageNumber: Long`

                      - `startPageNumber: Long`

                      - `type: JsonValue; "page_location"constant`

                        - `PAGE_LOCATION("page_location")`

                    - `class BetaCitationContentBlockLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endBlockIndex: Long`

                      - `startBlockIndex: Long`

                      - `type: JsonValue; "content_block_location"constant`

                        - `CONTENT_BLOCK_LOCATION("content_block_location")`

                    - `class BetaCitationWebSearchResultLocationParam:`

                      - `citedText: String`

                      - `encryptedIndex: String`

                      - `title: Optional<String>`

                      - `type: JsonValue; "web_search_result_location"constant`

                        - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                      - `url: String`

                    - `class BetaCitationSearchResultLocationParam:`

                      - `citedText: String`

                      - `endBlockIndex: Long`

                      - `searchResultIndex: Long`

                      - `source: String`

                      - `startBlockIndex: Long`

                      - `title: Optional<String>`

                      - `type: JsonValue; "search_result_location"constant`

                        - `SEARCH_RESULT_LOCATION("search_result_location")`

                - `class BetaImageBlockParam:`

                  - `source: Source`

                    - `class BetaBase64ImageSource:`

                      - `data: String`

                      - `mediaType: MediaType`

                        - `IMAGE_JPEG("image/jpeg")`

                        - `IMAGE_PNG("image/png")`

                        - `IMAGE_GIF("image/gif")`

                        - `IMAGE_WEBP("image/webp")`

                      - `type: JsonValue; "base64"constant`

                        - `BASE64("base64")`

                    - `class BetaUrlImageSource:`

                      - `type: JsonValue; "url"constant`

                        - `URL("url")`

                      - `url: String`

                    - `class BetaFileImageSource:`

                      - `fileId: String`

                      - `type: JsonValue; "file"constant`

                        - `FILE("file")`

                  - `type: JsonValue; "image"constant`

                    - `IMAGE("image")`

                  - `cacheControl: Optional<BetaCacheControlEphemeral>`

                    Create a cache control breakpoint at this content block.

                    - `type: JsonValue; "ephemeral"constant`

                      - `EPHEMERAL("ephemeral")`

                    - `ttl: Optional<Ttl>`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `TTL_5M("5m")`

                      - `TTL_1H("1h")`

            - `type: JsonValue; "content"constant`

              - `CONTENT("content")`

          - `class BetaUrlPdfSource:`

            - `type: JsonValue; "url"constant`

              - `URL("url")`

            - `url: String`

          - `class BetaFileDocumentSource:`

            - `fileId: String`

            - `type: JsonValue; "file"constant`

              - `FILE("file")`

        - `type: JsonValue; "document"constant`

          - `DOCUMENT("document")`

        - `cacheControl: Optional<BetaCacheControlEphemeral>`

          Create a cache control breakpoint at this content block.

          - `type: JsonValue; "ephemeral"constant`

            - `EPHEMERAL("ephemeral")`

          - `ttl: Optional<Ttl>`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `TTL_5M("5m")`

            - `TTL_1H("1h")`

        - `citations: Optional<BetaCitationsConfigParam>`

          - `enabled: Optional<Boolean>`

        - `context: Optional<String>`

        - `title: Optional<String>`

      - `type: JsonValue; "web_fetch_result"constant`

        - `WEB_FETCH_RESULT("web_fetch_result")`

      - `url: String`

        Fetched content URL

      - `retrievedAt: Optional<String>`

        ISO 8601 timestamp when the content was retrieved

  - `toolUseId: String`

  - `type: JsonValue; "web_fetch_tool_result"constant`

    - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

### Beta Web Fetch Tool Result Error Block

- `class BetaWebFetchToolResultErrorBlock:`

  - `errorCode: BetaWebFetchToolResultErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `URL_TOO_LONG("url_too_long")`

    - `URL_NOT_ALLOWED("url_not_allowed")`

    - `URL_NOT_ACCESSIBLE("url_not_accessible")`

    - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `MAX_USES_EXCEEDED("max_uses_exceeded")`

    - `UNAVAILABLE("unavailable")`

  - `type: JsonValue; "web_fetch_tool_result_error"constant`

    - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

### Beta Web Fetch Tool Result Error Block Param

- `class BetaWebFetchToolResultErrorBlockParam:`

  - `errorCode: BetaWebFetchToolResultErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `URL_TOO_LONG("url_too_long")`

    - `URL_NOT_ALLOWED("url_not_allowed")`

    - `URL_NOT_ACCESSIBLE("url_not_accessible")`

    - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `MAX_USES_EXCEEDED("max_uses_exceeded")`

    - `UNAVAILABLE("unavailable")`

  - `type: JsonValue; "web_fetch_tool_result_error"constant`

    - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

### Beta Web Fetch Tool Result Error Code

- `enum class BetaWebFetchToolResultErrorCode:`

  - `INVALID_TOOL_INPUT("invalid_tool_input")`

  - `URL_TOO_LONG("url_too_long")`

  - `URL_NOT_ALLOWED("url_not_allowed")`

  - `URL_NOT_ACCESSIBLE("url_not_accessible")`

  - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

  - `TOO_MANY_REQUESTS("too_many_requests")`

  - `MAX_USES_EXCEEDED("max_uses_exceeded")`

  - `UNAVAILABLE("unavailable")`

### Beta Web Search Result Block

- `class BetaWebSearchResultBlock:`

  - `encryptedContent: String`

  - `pageAge: Optional<String>`

  - `title: String`

  - `type: JsonValue; "web_search_result"constant`

    - `WEB_SEARCH_RESULT("web_search_result")`

  - `url: String`

### Beta Web Search Result Block Param

- `class BetaWebSearchResultBlockParam:`

  - `encryptedContent: String`

  - `title: String`

  - `type: JsonValue; "web_search_result"constant`

    - `WEB_SEARCH_RESULT("web_search_result")`

  - `url: String`

  - `pageAge: Optional<String>`

### Beta Web Search Tool 20250305

- `class BetaWebSearchTool20250305:`

  - `name: JsonValue; "web_search"constant`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `WEB_SEARCH("web_search")`

  - `type: JsonValue; "web_search_20250305"constant`

    - `WEB_SEARCH_20250305("web_search_20250305")`

  - `allowedCallers: Optional<List<AllowedCaller>>`

    - `DIRECT("direct")`

    - `CODE_EXECUTION_20250825("code_execution_20250825")`

  - `allowedDomains: Optional<List<String>>`

    If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

  - `blockedDomains: Optional<List<String>>`

    If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

  - `deferLoading: Optional<Boolean>`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `maxUses: Optional<Long>`

    Maximum number of times the tool can be used in the API request.

  - `strict: Optional<Boolean>`

  - `userLocation: Optional<UserLocation>`

    Parameters for the user's location. Used to provide more relevant search results.

    - `type: JsonValue; "approximate"constant`

      - `APPROXIMATE("approximate")`

    - `city: Optional<String>`

      The city of the user.

    - `country: Optional<String>`

      The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

    - `region: Optional<String>`

      The region of the user.

    - `timezone: Optional<String>`

      The [IANA timezone](https://nodatime.org/TimeZones) of the user.

### Beta Web Search Tool Request Error

- `class BetaWebSearchToolRequestError:`

  - `errorCode: BetaWebSearchToolResultErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `UNAVAILABLE("unavailable")`

    - `MAX_USES_EXCEEDED("max_uses_exceeded")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `QUERY_TOO_LONG("query_too_long")`

  - `type: JsonValue; "web_search_tool_result_error"constant`

    - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

### Beta Web Search Tool Result Block

- `class BetaWebSearchToolResultBlock:`

  - `content: BetaWebSearchToolResultBlockContent`

    - `class BetaWebSearchToolResultError:`

      - `errorCode: BetaWebSearchToolResultErrorCode`

        - `INVALID_TOOL_INPUT("invalid_tool_input")`

        - `UNAVAILABLE("unavailable")`

        - `MAX_USES_EXCEEDED("max_uses_exceeded")`

        - `TOO_MANY_REQUESTS("too_many_requests")`

        - `QUERY_TOO_LONG("query_too_long")`

      - `type: JsonValue; "web_search_tool_result_error"constant`

        - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

    - `List<BetaWebSearchResultBlock>`

      - `encryptedContent: String`

      - `pageAge: Optional<String>`

      - `title: String`

      - `type: JsonValue; "web_search_result"constant`

        - `WEB_SEARCH_RESULT("web_search_result")`

      - `url: String`

  - `toolUseId: String`

  - `type: JsonValue; "web_search_tool_result"constant`

    - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

### Beta Web Search Tool Result Block Content

- `class BetaWebSearchToolResultBlockContent: A class that can be one of several variants.union`

  - `class BetaWebSearchToolResultError:`

    - `errorCode: BetaWebSearchToolResultErrorCode`

      - `INVALID_TOOL_INPUT("invalid_tool_input")`

      - `UNAVAILABLE("unavailable")`

      - `MAX_USES_EXCEEDED("max_uses_exceeded")`

      - `TOO_MANY_REQUESTS("too_many_requests")`

      - `QUERY_TOO_LONG("query_too_long")`

    - `type: JsonValue; "web_search_tool_result_error"constant`

      - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

  - `List<BetaWebSearchResultBlock>`

    - `encryptedContent: String`

    - `pageAge: Optional<String>`

    - `title: String`

    - `type: JsonValue; "web_search_result"constant`

      - `WEB_SEARCH_RESULT("web_search_result")`

    - `url: String`

### Beta Web Search Tool Result Block Param

- `class BetaWebSearchToolResultBlockParam:`

  - `content: BetaWebSearchToolResultBlockParamContent`

    - `List<BetaWebSearchResultBlockParam>`

      - `encryptedContent: String`

      - `title: String`

      - `type: JsonValue; "web_search_result"constant`

        - `WEB_SEARCH_RESULT("web_search_result")`

      - `url: String`

      - `pageAge: Optional<String>`

    - `class BetaWebSearchToolRequestError:`

      - `errorCode: BetaWebSearchToolResultErrorCode`

        - `INVALID_TOOL_INPUT("invalid_tool_input")`

        - `UNAVAILABLE("unavailable")`

        - `MAX_USES_EXCEEDED("max_uses_exceeded")`

        - `TOO_MANY_REQUESTS("too_many_requests")`

        - `QUERY_TOO_LONG("query_too_long")`

      - `type: JsonValue; "web_search_tool_result_error"constant`

        - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

  - `toolUseId: String`

  - `type: JsonValue; "web_search_tool_result"constant`

    - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

  - `cacheControl: Optional<BetaCacheControlEphemeral>`

    Create a cache control breakpoint at this content block.

    - `type: JsonValue; "ephemeral"constant`

      - `EPHEMERAL("ephemeral")`

    - `ttl: Optional<Ttl>`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `TTL_5M("5m")`

      - `TTL_1H("1h")`

### Beta Web Search Tool Result Block Param Content

- `class BetaWebSearchToolResultBlockParamContent: A class that can be one of several variants.union`

  - `List<BetaWebSearchResultBlockParam>`

    - `encryptedContent: String`

    - `title: String`

    - `type: JsonValue; "web_search_result"constant`

      - `WEB_SEARCH_RESULT("web_search_result")`

    - `url: String`

    - `pageAge: Optional<String>`

  - `class BetaWebSearchToolRequestError:`

    - `errorCode: BetaWebSearchToolResultErrorCode`

      - `INVALID_TOOL_INPUT("invalid_tool_input")`

      - `UNAVAILABLE("unavailable")`

      - `MAX_USES_EXCEEDED("max_uses_exceeded")`

      - `TOO_MANY_REQUESTS("too_many_requests")`

      - `QUERY_TOO_LONG("query_too_long")`

    - `type: JsonValue; "web_search_tool_result_error"constant`

      - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

### Beta Web Search Tool Result Error

- `class BetaWebSearchToolResultError:`

  - `errorCode: BetaWebSearchToolResultErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `UNAVAILABLE("unavailable")`

    - `MAX_USES_EXCEEDED("max_uses_exceeded")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `QUERY_TOO_LONG("query_too_long")`

  - `type: JsonValue; "web_search_tool_result_error"constant`

    - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

### Beta Web Search Tool Result Error Code

- `enum class BetaWebSearchToolResultErrorCode:`

  - `INVALID_TOOL_INPUT("invalid_tool_input")`

  - `UNAVAILABLE("unavailable")`

  - `MAX_USES_EXCEEDED("max_uses_exceeded")`

  - `TOO_MANY_REQUESTS("too_many_requests")`

  - `QUERY_TOO_LONG("query_too_long")`

# Batches

## Create

`beta().messages().batches().create(BatchCreateParamsparams, RequestOptionsrequestOptions = RequestOptions.none()) : BetaMessageBatch`

**post** `/v1/messages/batches`

Send a batch of Message creation requests.

The Message Batches API can be used to process multiple Messages API requests at once. Once a Message Batch is created, it begins processing immediately. Batches can take up to 24 hours to complete.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchCreateParams`

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

  - `requests: List<Request>`

    List of requests for prompt completion. Each is an individual request to create a Message.

    - `customId: String`

      Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

      Must be unique for each request within the Message Batch.

    - `params: Params`

      Messages API creation parameters for the individual request.

      See the [Messages API reference](https://docs.claude.com/en/api/messages) for full documentation on available parameters.

      - `maxTokens: Long`

        The maximum number of tokens to generate before stopping.

        Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

        Different models have different maximum values for this parameter.  See [models](https://docs.claude.com/en/docs/models-overview) for details.

      - `messages: List<BetaMessageParam>`

        Input messages.

        Our models are trained to operate on alternating `user` and `assistant` conversational turns. When creating a new `Message`, you specify the prior conversational turns with the `messages` parameter, and the model then generates the next `Message` in the conversation. Consecutive `user` or `assistant` turns in your request will be combined into a single turn.

        Each input message must be an object with a `role` and `content`. You can specify a single `user`-role message, or you can include multiple `user` and `assistant` messages.

        If the final message uses the `assistant` role, the response content will continue immediately from the content in that message. This can be used to constrain part of the model's response.

        Example with a single `user` message:

        ```json
        [{"role": "user", "content": "Hello, Claude"}]
        ```

        Example with multiple conversational turns:

        ```json
        [
          {"role": "user", "content": "Hello there."},
          {"role": "assistant", "content": "Hi, I'm Claude. How can I help you?"},
          {"role": "user", "content": "Can you explain LLMs in plain English?"},
        ]
        ```

        Example with a partially-filled response from Claude:

        ```json
        [
          {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
          {"role": "assistant", "content": "The best answer is ("},
        ]
        ```

        Each input message `content` may be either a single `string` or an array of content blocks, where each block has a specific `type`. Using a `string` for `content` is shorthand for an array of one content block of type `"text"`. The following input messages are equivalent:

        ```json
        {"role": "user", "content": "Hello, Claude"}
        ```

        ```json
        {"role": "user", "content": [{"type": "text", "text": "Hello, Claude"}]}
        ```

        See [input examples](https://docs.claude.com/en/api/messages-examples).

        Note that if you want to include a [system prompt](https://docs.claude.com/en/docs/system-prompts), you can use the top-level `system` parameter — there is no `"system"` role for input messages in the Messages API.

        There is a limit of 100,000 messages in a single request.

        - `content: Content`

          - `String`

          - `List<BetaContentBlockParam>`

            - `class BetaTextBlockParam:`

              - `text: String`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<List<BetaTextCitationParam>>`

                - `class BetaCitationCharLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endCharIndex: Long`

                  - `startCharIndex: Long`

                  - `type: JsonValue; "char_location"constant`

                    - `CHAR_LOCATION("char_location")`

                - `class BetaCitationPageLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endPageNumber: Long`

                  - `startPageNumber: Long`

                  - `type: JsonValue; "page_location"constant`

                    - `PAGE_LOCATION("page_location")`

                - `class BetaCitationContentBlockLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endBlockIndex: Long`

                  - `startBlockIndex: Long`

                  - `type: JsonValue; "content_block_location"constant`

                    - `CONTENT_BLOCK_LOCATION("content_block_location")`

                - `class BetaCitationWebSearchResultLocationParam:`

                  - `citedText: String`

                  - `encryptedIndex: String`

                  - `title: Optional<String>`

                  - `type: JsonValue; "web_search_result_location"constant`

                    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                  - `url: String`

                - `class BetaCitationSearchResultLocationParam:`

                  - `citedText: String`

                  - `endBlockIndex: Long`

                  - `searchResultIndex: Long`

                  - `source: String`

                  - `startBlockIndex: Long`

                  - `title: Optional<String>`

                  - `type: JsonValue; "search_result_location"constant`

                    - `SEARCH_RESULT_LOCATION("search_result_location")`

            - `class BetaImageBlockParam:`

              - `source: Source`

                - `class BetaBase64ImageSource:`

                  - `data: String`

                  - `mediaType: MediaType`

                    - `IMAGE_JPEG("image/jpeg")`

                    - `IMAGE_PNG("image/png")`

                    - `IMAGE_GIF("image/gif")`

                    - `IMAGE_WEBP("image/webp")`

                  - `type: JsonValue; "base64"constant`

                    - `BASE64("base64")`

                - `class BetaUrlImageSource:`

                  - `type: JsonValue; "url"constant`

                    - `URL("url")`

                  - `url: String`

                - `class BetaFileImageSource:`

                  - `fileId: String`

                  - `type: JsonValue; "file"constant`

                    - `FILE("file")`

              - `type: JsonValue; "image"constant`

                - `IMAGE("image")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

            - `class BetaRequestDocumentBlock:`

              - `source: Source`

                - `class BetaBase64PdfSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "application/pdf"constant`

                    - `APPLICATION_PDF("application/pdf")`

                  - `type: JsonValue; "base64"constant`

                    - `BASE64("base64")`

                - `class BetaPlainTextSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "text/plain"constant`

                    - `TEXT_PLAIN("text/plain")`

                  - `type: JsonValue; "text"constant`

                    - `TEXT("text")`

                - `class BetaContentBlockSource:`

                  - `content: Content`

                    - `String`

                    - `List<BetaContentBlockSourceContent>`

                      - `class BetaTextBlockParam:`

                        - `text: String`

                        - `type: JsonValue; "text"constant`

                          - `TEXT("text")`

                        - `cacheControl: Optional<BetaCacheControlEphemeral>`

                          Create a cache control breakpoint at this content block.

                          - `type: JsonValue; "ephemeral"constant`

                            - `EPHEMERAL("ephemeral")`

                          - `ttl: Optional<Ttl>`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `TTL_5M("5m")`

                            - `TTL_1H("1h")`

                        - `citations: Optional<List<BetaTextCitationParam>>`

                          - `class BetaCitationCharLocationParam:`

                            - `citedText: String`

                            - `documentIndex: Long`

                            - `documentTitle: Optional<String>`

                            - `endCharIndex: Long`

                            - `startCharIndex: Long`

                            - `type: JsonValue; "char_location"constant`

                              - `CHAR_LOCATION("char_location")`

                          - `class BetaCitationPageLocationParam:`

                            - `citedText: String`

                            - `documentIndex: Long`

                            - `documentTitle: Optional<String>`

                            - `endPageNumber: Long`

                            - `startPageNumber: Long`

                            - `type: JsonValue; "page_location"constant`

                              - `PAGE_LOCATION("page_location")`

                          - `class BetaCitationContentBlockLocationParam:`

                            - `citedText: String`

                            - `documentIndex: Long`

                            - `documentTitle: Optional<String>`

                            - `endBlockIndex: Long`

                            - `startBlockIndex: Long`

                            - `type: JsonValue; "content_block_location"constant`

                              - `CONTENT_BLOCK_LOCATION("content_block_location")`

                          - `class BetaCitationWebSearchResultLocationParam:`

                            - `citedText: String`

                            - `encryptedIndex: String`

                            - `title: Optional<String>`

                            - `type: JsonValue; "web_search_result_location"constant`

                              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                            - `url: String`

                          - `class BetaCitationSearchResultLocationParam:`

                            - `citedText: String`

                            - `endBlockIndex: Long`

                            - `searchResultIndex: Long`

                            - `source: String`

                            - `startBlockIndex: Long`

                            - `title: Optional<String>`

                            - `type: JsonValue; "search_result_location"constant`

                              - `SEARCH_RESULT_LOCATION("search_result_location")`

                      - `class BetaImageBlockParam:`

                        - `source: Source`

                          - `class BetaBase64ImageSource:`

                            - `data: String`

                            - `mediaType: MediaType`

                              - `IMAGE_JPEG("image/jpeg")`

                              - `IMAGE_PNG("image/png")`

                              - `IMAGE_GIF("image/gif")`

                              - `IMAGE_WEBP("image/webp")`

                            - `type: JsonValue; "base64"constant`

                              - `BASE64("base64")`

                          - `class BetaUrlImageSource:`

                            - `type: JsonValue; "url"constant`

                              - `URL("url")`

                            - `url: String`

                          - `class BetaFileImageSource:`

                            - `fileId: String`

                            - `type: JsonValue; "file"constant`

                              - `FILE("file")`

                        - `type: JsonValue; "image"constant`

                          - `IMAGE("image")`

                        - `cacheControl: Optional<BetaCacheControlEphemeral>`

                          Create a cache control breakpoint at this content block.

                          - `type: JsonValue; "ephemeral"constant`

                            - `EPHEMERAL("ephemeral")`

                          - `ttl: Optional<Ttl>`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `TTL_5M("5m")`

                            - `TTL_1H("1h")`

                  - `type: JsonValue; "content"constant`

                    - `CONTENT("content")`

                - `class BetaUrlPdfSource:`

                  - `type: JsonValue; "url"constant`

                    - `URL("url")`

                  - `url: String`

                - `class BetaFileDocumentSource:`

                  - `fileId: String`

                  - `type: JsonValue; "file"constant`

                    - `FILE("file")`

              - `type: JsonValue; "document"constant`

                - `DOCUMENT("document")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<BetaCitationsConfigParam>`

                - `enabled: Optional<Boolean>`

              - `context: Optional<String>`

              - `title: Optional<String>`

            - `class BetaSearchResultBlockParam:`

              - `content: List<BetaTextBlockParam>`

                - `text: String`

                - `type: JsonValue; "text"constant`

                  - `TEXT("text")`

                - `cacheControl: Optional<BetaCacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `citations: Optional<List<BetaTextCitationParam>>`

                  - `class BetaCitationCharLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endCharIndex: Long`

                    - `startCharIndex: Long`

                    - `type: JsonValue; "char_location"constant`

                      - `CHAR_LOCATION("char_location")`

                  - `class BetaCitationPageLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endPageNumber: Long`

                    - `startPageNumber: Long`

                    - `type: JsonValue; "page_location"constant`

                      - `PAGE_LOCATION("page_location")`

                  - `class BetaCitationContentBlockLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endBlockIndex: Long`

                    - `startBlockIndex: Long`

                    - `type: JsonValue; "content_block_location"constant`

                      - `CONTENT_BLOCK_LOCATION("content_block_location")`

                  - `class BetaCitationWebSearchResultLocationParam:`

                    - `citedText: String`

                    - `encryptedIndex: String`

                    - `title: Optional<String>`

                    - `type: JsonValue; "web_search_result_location"constant`

                      - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                    - `url: String`

                  - `class BetaCitationSearchResultLocationParam:`

                    - `citedText: String`

                    - `endBlockIndex: Long`

                    - `searchResultIndex: Long`

                    - `source: String`

                    - `startBlockIndex: Long`

                    - `title: Optional<String>`

                    - `type: JsonValue; "search_result_location"constant`

                      - `SEARCH_RESULT_LOCATION("search_result_location")`

              - `source: String`

              - `title: String`

              - `type: JsonValue; "search_result"constant`

                - `SEARCH_RESULT("search_result")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<BetaCitationsConfigParam>`

                - `enabled: Optional<Boolean>`

            - `class BetaThinkingBlockParam:`

              - `signature: String`

              - `thinking: String`

              - `type: JsonValue; "thinking"constant`

                - `THINKING("thinking")`

            - `class BetaRedactedThinkingBlockParam:`

              - `data: String`

              - `type: JsonValue; "redacted_thinking"constant`

                - `REDACTED_THINKING("redacted_thinking")`

            - `class BetaToolUseBlockParam:`

              - `id: String`

              - `input: Input`

              - `name: String`

              - `type: JsonValue; "tool_use"constant`

                - `TOOL_USE("tool_use")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `caller: Optional<Caller>`

                Tool invocation directly from the model.

                - `class BetaDirectCaller:`

                  Tool invocation directly from the model.

                  - `type: JsonValue; "direct"constant`

                    - `DIRECT("direct")`

                - `class BetaServerToolCaller:`

                  Tool invocation generated by a server-side tool.

                  - `toolId: String`

                  - `type: JsonValue; "code_execution_20250825"constant`

                    - `CODE_EXECUTION_20250825("code_execution_20250825")`

            - `class BetaToolResultBlockParam:`

              - `toolUseId: String`

              - `type: JsonValue; "tool_result"constant`

                - `TOOL_RESULT("tool_result")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `content: Optional<Content>`

                - `String`

                - `List<Block>`

                  - `class BetaTextBlockParam:`

                    - `text: String`

                    - `type: JsonValue; "text"constant`

                      - `TEXT("text")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                    - `citations: Optional<List<BetaTextCitationParam>>`

                      - `class BetaCitationCharLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endCharIndex: Long`

                        - `startCharIndex: Long`

                        - `type: JsonValue; "char_location"constant`

                          - `CHAR_LOCATION("char_location")`

                      - `class BetaCitationPageLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endPageNumber: Long`

                        - `startPageNumber: Long`

                        - `type: JsonValue; "page_location"constant`

                          - `PAGE_LOCATION("page_location")`

                      - `class BetaCitationContentBlockLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endBlockIndex: Long`

                        - `startBlockIndex: Long`

                        - `type: JsonValue; "content_block_location"constant`

                          - `CONTENT_BLOCK_LOCATION("content_block_location")`

                      - `class BetaCitationWebSearchResultLocationParam:`

                        - `citedText: String`

                        - `encryptedIndex: String`

                        - `title: Optional<String>`

                        - `type: JsonValue; "web_search_result_location"constant`

                          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                        - `url: String`

                      - `class BetaCitationSearchResultLocationParam:`

                        - `citedText: String`

                        - `endBlockIndex: Long`

                        - `searchResultIndex: Long`

                        - `source: String`

                        - `startBlockIndex: Long`

                        - `title: Optional<String>`

                        - `type: JsonValue; "search_result_location"constant`

                          - `SEARCH_RESULT_LOCATION("search_result_location")`

                  - `class BetaImageBlockParam:`

                    - `source: Source`

                      - `class BetaBase64ImageSource:`

                        - `data: String`

                        - `mediaType: MediaType`

                          - `IMAGE_JPEG("image/jpeg")`

                          - `IMAGE_PNG("image/png")`

                          - `IMAGE_GIF("image/gif")`

                          - `IMAGE_WEBP("image/webp")`

                        - `type: JsonValue; "base64"constant`

                          - `BASE64("base64")`

                      - `class BetaUrlImageSource:`

                        - `type: JsonValue; "url"constant`

                          - `URL("url")`

                        - `url: String`

                      - `class BetaFileImageSource:`

                        - `fileId: String`

                        - `type: JsonValue; "file"constant`

                          - `FILE("file")`

                    - `type: JsonValue; "image"constant`

                      - `IMAGE("image")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                  - `class BetaSearchResultBlockParam:`

                    - `content: List<BetaTextBlockParam>`

                      - `text: String`

                      - `type: JsonValue; "text"constant`

                        - `TEXT("text")`

                      - `cacheControl: Optional<BetaCacheControlEphemeral>`

                        Create a cache control breakpoint at this content block.

                        - `type: JsonValue; "ephemeral"constant`

                          - `EPHEMERAL("ephemeral")`

                        - `ttl: Optional<Ttl>`

                          The time-to-live for the cache control breakpoint.

                          This may be one the following values:

                          - `5m`: 5 minutes
                          - `1h`: 1 hour

                          Defaults to `5m`.

                          - `TTL_5M("5m")`

                          - `TTL_1H("1h")`

                      - `citations: Optional<List<BetaTextCitationParam>>`

                        - `class BetaCitationCharLocationParam:`

                          - `citedText: String`

                          - `documentIndex: Long`

                          - `documentTitle: Optional<String>`

                          - `endCharIndex: Long`

                          - `startCharIndex: Long`

                          - `type: JsonValue; "char_location"constant`

                            - `CHAR_LOCATION("char_location")`

                        - `class BetaCitationPageLocationParam:`

                          - `citedText: String`

                          - `documentIndex: Long`

                          - `documentTitle: Optional<String>`

                          - `endPageNumber: Long`

                          - `startPageNumber: Long`

                          - `type: JsonValue; "page_location"constant`

                            - `PAGE_LOCATION("page_location")`

                        - `class BetaCitationContentBlockLocationParam:`

                          - `citedText: String`

                          - `documentIndex: Long`

                          - `documentTitle: Optional<String>`

                          - `endBlockIndex: Long`

                          - `startBlockIndex: Long`

                          - `type: JsonValue; "content_block_location"constant`

                            - `CONTENT_BLOCK_LOCATION("content_block_location")`

                        - `class BetaCitationWebSearchResultLocationParam:`

                          - `citedText: String`

                          - `encryptedIndex: String`

                          - `title: Optional<String>`

                          - `type: JsonValue; "web_search_result_location"constant`

                            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                          - `url: String`

                        - `class BetaCitationSearchResultLocationParam:`

                          - `citedText: String`

                          - `endBlockIndex: Long`

                          - `searchResultIndex: Long`

                          - `source: String`

                          - `startBlockIndex: Long`

                          - `title: Optional<String>`

                          - `type: JsonValue; "search_result_location"constant`

                            - `SEARCH_RESULT_LOCATION("search_result_location")`

                    - `source: String`

                    - `title: String`

                    - `type: JsonValue; "search_result"constant`

                      - `SEARCH_RESULT("search_result")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                    - `citations: Optional<BetaCitationsConfigParam>`

                      - `enabled: Optional<Boolean>`

                  - `class BetaRequestDocumentBlock:`

                    - `source: Source`

                      - `class BetaBase64PdfSource:`

                        - `data: String`

                        - `mediaType: JsonValue; "application/pdf"constant`

                          - `APPLICATION_PDF("application/pdf")`

                        - `type: JsonValue; "base64"constant`

                          - `BASE64("base64")`

                      - `class BetaPlainTextSource:`

                        - `data: String`

                        - `mediaType: JsonValue; "text/plain"constant`

                          - `TEXT_PLAIN("text/plain")`

                        - `type: JsonValue; "text"constant`

                          - `TEXT("text")`

                      - `class BetaContentBlockSource:`

                        - `content: Content`

                          - `String`

                          - `List<BetaContentBlockSourceContent>`

                            - `class BetaTextBlockParam:`

                              - `text: String`

                              - `type: JsonValue; "text"constant`

                                - `TEXT("text")`

                              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                                Create a cache control breakpoint at this content block.

                                - `type: JsonValue; "ephemeral"constant`

                                  - `EPHEMERAL("ephemeral")`

                                - `ttl: Optional<Ttl>`

                                  The time-to-live for the cache control breakpoint.

                                  This may be one the following values:

                                  - `5m`: 5 minutes
                                  - `1h`: 1 hour

                                  Defaults to `5m`.

                                  - `TTL_5M("5m")`

                                  - `TTL_1H("1h")`

                              - `citations: Optional<List<BetaTextCitationParam>>`

                                - `class BetaCitationCharLocationParam:`

                                  - `citedText: String`

                                  - `documentIndex: Long`

                                  - `documentTitle: Optional<String>`

                                  - `endCharIndex: Long`

                                  - `startCharIndex: Long`

                                  - `type: JsonValue; "char_location"constant`

                                    - `CHAR_LOCATION("char_location")`

                                - `class BetaCitationPageLocationParam:`

                                  - `citedText: String`

                                  - `documentIndex: Long`

                                  - `documentTitle: Optional<String>`

                                  - `endPageNumber: Long`

                                  - `startPageNumber: Long`

                                  - `type: JsonValue; "page_location"constant`

                                    - `PAGE_LOCATION("page_location")`

                                - `class BetaCitationContentBlockLocationParam:`

                                  - `citedText: String`

                                  - `documentIndex: Long`

                                  - `documentTitle: Optional<String>`

                                  - `endBlockIndex: Long`

                                  - `startBlockIndex: Long`

                                  - `type: JsonValue; "content_block_location"constant`

                                    - `CONTENT_BLOCK_LOCATION("content_block_location")`

                                - `class BetaCitationWebSearchResultLocationParam:`

                                  - `citedText: String`

                                  - `encryptedIndex: String`

                                  - `title: Optional<String>`

                                  - `type: JsonValue; "web_search_result_location"constant`

                                    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                                  - `url: String`

                                - `class BetaCitationSearchResultLocationParam:`

                                  - `citedText: String`

                                  - `endBlockIndex: Long`

                                  - `searchResultIndex: Long`

                                  - `source: String`

                                  - `startBlockIndex: Long`

                                  - `title: Optional<String>`

                                  - `type: JsonValue; "search_result_location"constant`

                                    - `SEARCH_RESULT_LOCATION("search_result_location")`

                            - `class BetaImageBlockParam:`

                              - `source: Source`

                                - `class BetaBase64ImageSource:`

                                  - `data: String`

                                  - `mediaType: MediaType`

                                    - `IMAGE_JPEG("image/jpeg")`

                                    - `IMAGE_PNG("image/png")`

                                    - `IMAGE_GIF("image/gif")`

                                    - `IMAGE_WEBP("image/webp")`

                                  - `type: JsonValue; "base64"constant`

                                    - `BASE64("base64")`

                                - `class BetaUrlImageSource:`

                                  - `type: JsonValue; "url"constant`

                                    - `URL("url")`

                                  - `url: String`

                                - `class BetaFileImageSource:`

                                  - `fileId: String`

                                  - `type: JsonValue; "file"constant`

                                    - `FILE("file")`

                              - `type: JsonValue; "image"constant`

                                - `IMAGE("image")`

                              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                                Create a cache control breakpoint at this content block.

                                - `type: JsonValue; "ephemeral"constant`

                                  - `EPHEMERAL("ephemeral")`

                                - `ttl: Optional<Ttl>`

                                  The time-to-live for the cache control breakpoint.

                                  This may be one the following values:

                                  - `5m`: 5 minutes
                                  - `1h`: 1 hour

                                  Defaults to `5m`.

                                  - `TTL_5M("5m")`

                                  - `TTL_1H("1h")`

                        - `type: JsonValue; "content"constant`

                          - `CONTENT("content")`

                      - `class BetaUrlPdfSource:`

                        - `type: JsonValue; "url"constant`

                          - `URL("url")`

                        - `url: String`

                      - `class BetaFileDocumentSource:`

                        - `fileId: String`

                        - `type: JsonValue; "file"constant`

                          - `FILE("file")`

                    - `type: JsonValue; "document"constant`

                      - `DOCUMENT("document")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                    - `citations: Optional<BetaCitationsConfigParam>`

                      - `enabled: Optional<Boolean>`

                    - `context: Optional<String>`

                    - `title: Optional<String>`

                  - `class BetaToolReferenceBlockParam:`

                    Tool reference block that can be included in tool_result content.

                    - `toolName: String`

                    - `type: JsonValue; "tool_reference"constant`

                      - `TOOL_REFERENCE("tool_reference")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

              - `isError: Optional<Boolean>`

            - `class BetaServerToolUseBlockParam:`

              - `id: String`

              - `input: Input`

              - `name: Name`

                - `WEB_SEARCH("web_search")`

                - `WEB_FETCH("web_fetch")`

                - `CODE_EXECUTION("code_execution")`

                - `BASH_CODE_EXECUTION("bash_code_execution")`

                - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

                - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

                - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

              - `type: JsonValue; "server_tool_use"constant`

                - `SERVER_TOOL_USE("server_tool_use")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `caller: Optional<Caller>`

                Tool invocation directly from the model.

                - `class BetaDirectCaller:`

                  Tool invocation directly from the model.

                  - `type: JsonValue; "direct"constant`

                    - `DIRECT("direct")`

                - `class BetaServerToolCaller:`

                  Tool invocation generated by a server-side tool.

                  - `toolId: String`

                  - `type: JsonValue; "code_execution_20250825"constant`

                    - `CODE_EXECUTION_20250825("code_execution_20250825")`

            - `class BetaWebSearchToolResultBlockParam:`

              - `content: BetaWebSearchToolResultBlockParamContent`

                - `List<BetaWebSearchResultBlockParam>`

                  - `encryptedContent: String`

                  - `title: String`

                  - `type: JsonValue; "web_search_result"constant`

                    - `WEB_SEARCH_RESULT("web_search_result")`

                  - `url: String`

                  - `pageAge: Optional<String>`

                - `class BetaWebSearchToolRequestError:`

                  - `errorCode: BetaWebSearchToolResultErrorCode`

                    - `INVALID_TOOL_INPUT("invalid_tool_input")`

                    - `UNAVAILABLE("unavailable")`

                    - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                    - `TOO_MANY_REQUESTS("too_many_requests")`

                    - `QUERY_TOO_LONG("query_too_long")`

                  - `type: JsonValue; "web_search_tool_result_error"constant`

                    - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

              - `toolUseId: String`

              - `type: JsonValue; "web_search_tool_result"constant`

                - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

            - `class BetaWebFetchToolResultBlockParam:`

              - `content: Content`

                - `class BetaWebFetchToolResultErrorBlockParam:`

                  - `errorCode: BetaWebFetchToolResultErrorCode`

                    - `INVALID_TOOL_INPUT("invalid_tool_input")`

                    - `URL_TOO_LONG("url_too_long")`

                    - `URL_NOT_ALLOWED("url_not_allowed")`

                    - `URL_NOT_ACCESSIBLE("url_not_accessible")`

                    - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

                    - `TOO_MANY_REQUESTS("too_many_requests")`

                    - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                    - `UNAVAILABLE("unavailable")`

                  - `type: JsonValue; "web_fetch_tool_result_error"constant`

                    - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

                - `class BetaWebFetchBlockParam:`

                  - `content: BetaRequestDocumentBlock`

                    - `source: Source`

                      - `class BetaBase64PdfSource:`

                        - `data: String`

                        - `mediaType: JsonValue; "application/pdf"constant`

                          - `APPLICATION_PDF("application/pdf")`

                        - `type: JsonValue; "base64"constant`

                          - `BASE64("base64")`

                      - `class BetaPlainTextSource:`

                        - `data: String`

                        - `mediaType: JsonValue; "text/plain"constant`

                          - `TEXT_PLAIN("text/plain")`

                        - `type: JsonValue; "text"constant`

                          - `TEXT("text")`

                      - `class BetaContentBlockSource:`

                        - `content: Content`

                          - `String`

                          - `List<BetaContentBlockSourceContent>`

                            - `class BetaTextBlockParam:`

                              - `text: String`

                              - `type: JsonValue; "text"constant`

                                - `TEXT("text")`

                              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                                Create a cache control breakpoint at this content block.

                                - `type: JsonValue; "ephemeral"constant`

                                  - `EPHEMERAL("ephemeral")`

                                - `ttl: Optional<Ttl>`

                                  The time-to-live for the cache control breakpoint.

                                  This may be one the following values:

                                  - `5m`: 5 minutes
                                  - `1h`: 1 hour

                                  Defaults to `5m`.

                                  - `TTL_5M("5m")`

                                  - `TTL_1H("1h")`

                              - `citations: Optional<List<BetaTextCitationParam>>`

                                - `class BetaCitationCharLocationParam:`

                                  - `citedText: String`

                                  - `documentIndex: Long`

                                  - `documentTitle: Optional<String>`

                                  - `endCharIndex: Long`

                                  - `startCharIndex: Long`

                                  - `type: JsonValue; "char_location"constant`

                                    - `CHAR_LOCATION("char_location")`

                                - `class BetaCitationPageLocationParam:`

                                  - `citedText: String`

                                  - `documentIndex: Long`

                                  - `documentTitle: Optional<String>`

                                  - `endPageNumber: Long`

                                  - `startPageNumber: Long`

                                  - `type: JsonValue; "page_location"constant`

                                    - `PAGE_LOCATION("page_location")`

                                - `class BetaCitationContentBlockLocationParam:`

                                  - `citedText: String`

                                  - `documentIndex: Long`

                                  - `documentTitle: Optional<String>`

                                  - `endBlockIndex: Long`

                                  - `startBlockIndex: Long`

                                  - `type: JsonValue; "content_block_location"constant`

                                    - `CONTENT_BLOCK_LOCATION("content_block_location")`

                                - `class BetaCitationWebSearchResultLocationParam:`

                                  - `citedText: String`

                                  - `encryptedIndex: String`

                                  - `title: Optional<String>`

                                  - `type: JsonValue; "web_search_result_location"constant`

                                    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                                  - `url: String`

                                - `class BetaCitationSearchResultLocationParam:`

                                  - `citedText: String`

                                  - `endBlockIndex: Long`

                                  - `searchResultIndex: Long`

                                  - `source: String`

                                  - `startBlockIndex: Long`

                                  - `title: Optional<String>`

                                  - `type: JsonValue; "search_result_location"constant`

                                    - `SEARCH_RESULT_LOCATION("search_result_location")`

                            - `class BetaImageBlockParam:`

                              - `source: Source`

                                - `class BetaBase64ImageSource:`

                                  - `data: String`

                                  - `mediaType: MediaType`

                                    - `IMAGE_JPEG("image/jpeg")`

                                    - `IMAGE_PNG("image/png")`

                                    - `IMAGE_GIF("image/gif")`

                                    - `IMAGE_WEBP("image/webp")`

                                  - `type: JsonValue; "base64"constant`

                                    - `BASE64("base64")`

                                - `class BetaUrlImageSource:`

                                  - `type: JsonValue; "url"constant`

                                    - `URL("url")`

                                  - `url: String`

                                - `class BetaFileImageSource:`

                                  - `fileId: String`

                                  - `type: JsonValue; "file"constant`

                                    - `FILE("file")`

                              - `type: JsonValue; "image"constant`

                                - `IMAGE("image")`

                              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                                Create a cache control breakpoint at this content block.

                                - `type: JsonValue; "ephemeral"constant`

                                  - `EPHEMERAL("ephemeral")`

                                - `ttl: Optional<Ttl>`

                                  The time-to-live for the cache control breakpoint.

                                  This may be one the following values:

                                  - `5m`: 5 minutes
                                  - `1h`: 1 hour

                                  Defaults to `5m`.

                                  - `TTL_5M("5m")`

                                  - `TTL_1H("1h")`

                        - `type: JsonValue; "content"constant`

                          - `CONTENT("content")`

                      - `class BetaUrlPdfSource:`

                        - `type: JsonValue; "url"constant`

                          - `URL("url")`

                        - `url: String`

                      - `class BetaFileDocumentSource:`

                        - `fileId: String`

                        - `type: JsonValue; "file"constant`

                          - `FILE("file")`

                    - `type: JsonValue; "document"constant`

                      - `DOCUMENT("document")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                    - `citations: Optional<BetaCitationsConfigParam>`

                      - `enabled: Optional<Boolean>`

                    - `context: Optional<String>`

                    - `title: Optional<String>`

                  - `type: JsonValue; "web_fetch_result"constant`

                    - `WEB_FETCH_RESULT("web_fetch_result")`

                  - `url: String`

                    Fetched content URL

                  - `retrievedAt: Optional<String>`

                    ISO 8601 timestamp when the content was retrieved

              - `toolUseId: String`

              - `type: JsonValue; "web_fetch_tool_result"constant`

                - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

            - `class BetaCodeExecutionToolResultBlockParam:`

              - `content: BetaCodeExecutionToolResultBlockParamContent`

                - `class BetaCodeExecutionToolResultErrorParam:`

                  - `errorCode: BetaCodeExecutionToolResultErrorCode`

                    - `INVALID_TOOL_INPUT("invalid_tool_input")`

                    - `UNAVAILABLE("unavailable")`

                    - `TOO_MANY_REQUESTS("too_many_requests")`

                    - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                  - `type: JsonValue; "code_execution_tool_result_error"constant`

                    - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

                - `class BetaCodeExecutionResultBlockParam:`

                  - `content: List<BetaCodeExecutionOutputBlockParam>`

                    - `fileId: String`

                    - `type: JsonValue; "code_execution_output"constant`

                      - `CODE_EXECUTION_OUTPUT("code_execution_output")`

                  - `returnCode: Long`

                  - `stderr: String`

                  - `stdout: String`

                  - `type: JsonValue; "code_execution_result"constant`

                    - `CODE_EXECUTION_RESULT("code_execution_result")`

              - `toolUseId: String`

              - `type: JsonValue; "code_execution_tool_result"constant`

                - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

            - `class BetaBashCodeExecutionToolResultBlockParam:`

              - `content: Content`

                - `class BetaBashCodeExecutionToolResultErrorParam:`

                  - `errorCode: ErrorCode`

                    - `INVALID_TOOL_INPUT("invalid_tool_input")`

                    - `UNAVAILABLE("unavailable")`

                    - `TOO_MANY_REQUESTS("too_many_requests")`

                    - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                    - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

                  - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

                    - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

                - `class BetaBashCodeExecutionResultBlockParam:`

                  - `content: List<BetaBashCodeExecutionOutputBlockParam>`

                    - `fileId: String`

                    - `type: JsonValue; "bash_code_execution_output"constant`

                      - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

                  - `returnCode: Long`

                  - `stderr: String`

                  - `stdout: String`

                  - `type: JsonValue; "bash_code_execution_result"constant`

                    - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

              - `toolUseId: String`

              - `type: JsonValue; "bash_code_execution_tool_result"constant`

                - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

            - `class BetaTextEditorCodeExecutionToolResultBlockParam:`

              - `content: Content`

                - `class BetaTextEditorCodeExecutionToolResultErrorParam:`

                  - `errorCode: ErrorCode`

                    - `INVALID_TOOL_INPUT("invalid_tool_input")`

                    - `UNAVAILABLE("unavailable")`

                    - `TOO_MANY_REQUESTS("too_many_requests")`

                    - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                    - `FILE_NOT_FOUND("file_not_found")`

                  - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

                    - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

                  - `errorMessage: Optional<String>`

                - `class BetaTextEditorCodeExecutionViewResultBlockParam:`

                  - `content: String`

                  - `fileType: FileType`

                    - `TEXT("text")`

                    - `IMAGE("image")`

                    - `PDF("pdf")`

                  - `type: JsonValue; "text_editor_code_execution_view_result"constant`

                    - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

                  - `numLines: Optional<Long>`

                  - `startLine: Optional<Long>`

                  - `totalLines: Optional<Long>`

                - `class BetaTextEditorCodeExecutionCreateResultBlockParam:`

                  - `isFileUpdate: Boolean`

                  - `type: JsonValue; "text_editor_code_execution_create_result"constant`

                    - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

                - `class BetaTextEditorCodeExecutionStrReplaceResultBlockParam:`

                  - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

                    - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

                  - `lines: Optional<List<String>>`

                  - `newLines: Optional<Long>`

                  - `newStart: Optional<Long>`

                  - `oldLines: Optional<Long>`

                  - `oldStart: Optional<Long>`

              - `toolUseId: String`

              - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

            - `class BetaToolSearchToolResultBlockParam:`

              - `content: Content`

                - `class BetaToolSearchToolResultErrorParam:`

                  - `errorCode: ErrorCode`

                    - `INVALID_TOOL_INPUT("invalid_tool_input")`

                    - `UNAVAILABLE("unavailable")`

                    - `TOO_MANY_REQUESTS("too_many_requests")`

                    - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                  - `type: JsonValue; "tool_search_tool_result_error"constant`

                    - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

                - `class BetaToolSearchToolSearchResultBlockParam:`

                  - `toolReferences: List<BetaToolReferenceBlockParam>`

                    - `toolName: String`

                    - `type: JsonValue; "tool_reference"constant`

                      - `TOOL_REFERENCE("tool_reference")`

                    - `cacheControl: Optional<BetaCacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                  - `type: JsonValue; "tool_search_tool_search_result"constant`

                    - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

              - `toolUseId: String`

              - `type: JsonValue; "tool_search_tool_result"constant`

                - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

            - `class BetaMcpToolUseBlockParam:`

              - `id: String`

              - `input: Input`

              - `name: String`

              - `serverName: String`

                The name of the MCP server

              - `type: JsonValue; "mcp_tool_use"constant`

                - `MCP_TOOL_USE("mcp_tool_use")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

            - `class BetaRequestMcpToolResultBlockParam:`

              - `toolUseId: String`

              - `type: JsonValue; "mcp_tool_result"constant`

                - `MCP_TOOL_RESULT("mcp_tool_result")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `content: Optional<Content>`

                - `String`

                - `List<BetaTextBlockParam>`

                  - `text: String`

                  - `type: JsonValue; "text"constant`

                    - `TEXT("text")`

                  - `cacheControl: Optional<BetaCacheControlEphemeral>`

                    Create a cache control breakpoint at this content block.

                    - `type: JsonValue; "ephemeral"constant`

                      - `EPHEMERAL("ephemeral")`

                    - `ttl: Optional<Ttl>`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `TTL_5M("5m")`

                      - `TTL_1H("1h")`

                  - `citations: Optional<List<BetaTextCitationParam>>`

                    - `class BetaCitationCharLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endCharIndex: Long`

                      - `startCharIndex: Long`

                      - `type: JsonValue; "char_location"constant`

                        - `CHAR_LOCATION("char_location")`

                    - `class BetaCitationPageLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endPageNumber: Long`

                      - `startPageNumber: Long`

                      - `type: JsonValue; "page_location"constant`

                        - `PAGE_LOCATION("page_location")`

                    - `class BetaCitationContentBlockLocationParam:`

                      - `citedText: String`

                      - `documentIndex: Long`

                      - `documentTitle: Optional<String>`

                      - `endBlockIndex: Long`

                      - `startBlockIndex: Long`

                      - `type: JsonValue; "content_block_location"constant`

                        - `CONTENT_BLOCK_LOCATION("content_block_location")`

                    - `class BetaCitationWebSearchResultLocationParam:`

                      - `citedText: String`

                      - `encryptedIndex: String`

                      - `title: Optional<String>`

                      - `type: JsonValue; "web_search_result_location"constant`

                        - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                      - `url: String`

                    - `class BetaCitationSearchResultLocationParam:`

                      - `citedText: String`

                      - `endBlockIndex: Long`

                      - `searchResultIndex: Long`

                      - `source: String`

                      - `startBlockIndex: Long`

                      - `title: Optional<String>`

                      - `type: JsonValue; "search_result_location"constant`

                        - `SEARCH_RESULT_LOCATION("search_result_location")`

              - `isError: Optional<Boolean>`

            - `class BetaContainerUploadBlockParam:`

              A content block that represents a file to be uploaded to the container
              Files uploaded via this block will be available in the container's input directory.

              - `fileId: String`

              - `type: JsonValue; "container_upload"constant`

                - `CONTAINER_UPLOAD("container_upload")`

              - `cacheControl: Optional<BetaCacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

        - `role: Role`

          - `USER("user")`

          - `ASSISTANT("assistant")`

      - `model: Model`

        The model that will complete your prompt.

        See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

        - `CLAUDE_OPUS_4_5_20251101("claude-opus-4-5-20251101")`

          Premium model combining maximum intelligence with practical performance

        - `CLAUDE_OPUS_4_5("claude-opus-4-5")`

          Premium model combining maximum intelligence with practical performance

        - `CLAUDE_3_7_SONNET_LATEST("claude-3-7-sonnet-latest")`

          High-performance model with early extended thinking

        - `CLAUDE_3_7_SONNET_20250219("claude-3-7-sonnet-20250219")`

          High-performance model with early extended thinking

        - `CLAUDE_3_5_HAIKU_LATEST("claude-3-5-haiku-latest")`

          Fastest and most compact model for near-instant responsiveness

        - `CLAUDE_3_5_HAIKU_20241022("claude-3-5-haiku-20241022")`

          Our fastest model

        - `CLAUDE_HAIKU_4_5("claude-haiku-4-5")`

          Hybrid model, capable of near-instant responses and extended thinking

        - `CLAUDE_HAIKU_4_5_20251001("claude-haiku-4-5-20251001")`

          Hybrid model, capable of near-instant responses and extended thinking

        - `CLAUDE_SONNET_4_20250514("claude-sonnet-4-20250514")`

          High-performance model with extended thinking

        - `CLAUDE_SONNET_4_0("claude-sonnet-4-0")`

          High-performance model with extended thinking

        - `CLAUDE_4_SONNET_20250514("claude-4-sonnet-20250514")`

          High-performance model with extended thinking

        - `CLAUDE_SONNET_4_5("claude-sonnet-4-5")`

          Our best model for real-world agents and coding

        - `CLAUDE_SONNET_4_5_20250929("claude-sonnet-4-5-20250929")`

          Our best model for real-world agents and coding

        - `CLAUDE_OPUS_4_0("claude-opus-4-0")`

          Our most capable model

        - `CLAUDE_OPUS_4_20250514("claude-opus-4-20250514")`

          Our most capable model

        - `CLAUDE_4_OPUS_20250514("claude-4-opus-20250514")`

          Our most capable model

        - `CLAUDE_OPUS_4_1_20250805("claude-opus-4-1-20250805")`

          Our most capable model

        - `CLAUDE_3_OPUS_LATEST("claude-3-opus-latest")`

          Excels at writing and complex tasks

        - `CLAUDE_3_OPUS_20240229("claude-3-opus-20240229")`

          Excels at writing and complex tasks

        - `CLAUDE_3_HAIKU_20240307("claude-3-haiku-20240307")`

          Our previous most fast and cost-effective

      - `container: Optional<Container>`

        Container identifier for reuse across requests.

        - `class BetaContainerParams:`

          Container parameters with skills to be loaded.

          - `id: Optional<String>`

            Container id

          - `skills: Optional<List<BetaSkillParams>>`

            List of skills to load in the container

            - `skillId: String`

              Skill ID

            - `type: Type`

              Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

              - `ANTHROPIC("anthropic")`

              - `CUSTOM("custom")`

            - `version: Optional<String>`

              Skill version or 'latest' for most recent version

        - `String`

      - `contextManagement: Optional<BetaContextManagementConfig>`

        Context management configuration.

        This allows you to control how Claude manages context across multiple requests, such as whether to clear function results or not.

        - `edits: Optional<List<Edit>>`

          List of context management edits to apply

          - `class BetaClearToolUses20250919Edit:`

            - `type: JsonValue; "clear_tool_uses_20250919"constant`

              - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

            - `clearAtLeast: Optional<BetaInputTokensClearAtLeast>`

              Minimum number of tokens that must be cleared when triggered. Context will only be modified if at least this many tokens can be removed.

              - `type: JsonValue; "input_tokens"constant`

                - `INPUT_TOKENS("input_tokens")`

              - `value: Long`

            - `clearToolInputs: Optional<ClearToolInputs>`

              Whether to clear all tool inputs (bool) or specific tool inputs to clear (list)

              - `Boolean`

              - `List<String>`

            - `excludeTools: Optional<List<String>>`

              Tool names whose uses are preserved from clearing

            - `keep: Optional<BetaToolUsesKeep>`

              Number of tool uses to retain in the conversation

              - `type: JsonValue; "tool_uses"constant`

                - `TOOL_USES("tool_uses")`

              - `value: Long`

            - `trigger: Optional<Trigger>`

              Condition that triggers the context management strategy

              - `class BetaInputTokensTrigger:`

                - `type: JsonValue; "input_tokens"constant`

                  - `INPUT_TOKENS("input_tokens")`

                - `value: Long`

              - `class BetaToolUsesTrigger:`

                - `type: JsonValue; "tool_uses"constant`

                  - `TOOL_USES("tool_uses")`

                - `value: Long`

          - `class BetaClearThinking20251015Edit:`

            - `type: JsonValue; "clear_thinking_20251015"constant`

              - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

            - `keep: Optional<Keep>`

              Number of most recent assistant turns to keep thinking blocks for. Older turns will have their thinking blocks removed.

              - `class BetaThinkingTurns:`

                - `type: JsonValue; "thinking_turns"constant`

                  - `THINKING_TURNS("thinking_turns")`

                - `value: Long`

              - `class BetaAllThinkingTurns:`

                - `type: JsonValue; "all"constant`

                  - `ALL("all")`

              - `JsonValue;`

                - `ALL("all")`

      - `mcpServers: Optional<List<BetaRequestMcpServerUrlDefinition>>`

        MCP servers to be utilized in this request

        - `name: String`

        - `type: JsonValue; "url"constant`

          - `URL("url")`

        - `url: String`

        - `authorizationToken: Optional<String>`

        - `toolConfiguration: Optional<BetaRequestMcpServerToolConfiguration>`

          - `allowedTools: Optional<List<String>>`

          - `enabled: Optional<Boolean>`

      - `metadata: Optional<BetaMetadata>`

        An object describing metadata about the request.

        - `userId: Optional<String>`

          An external identifier for the user who is associated with the request.

          This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

      - `outputConfig: Optional<BetaOutputConfig>`

        Configuration options for the model's output. Controls aspects like how much effort the model puts into its response.

        - `effort: Optional<Effort>`

          All possible effort levels.

          - `LOW("low")`

          - `MEDIUM("medium")`

          - `HIGH("high")`

      - `outputFormat: Optional<BetaJsonOutputFormat>`

        A schema to specify Claude's output format in responses.

        - `schema: Schema`

          The JSON schema of the format

        - `type: JsonValue; "json_schema"constant`

          - `JSON_SCHEMA("json_schema")`

      - `serviceTier: Optional<ServiceTier>`

        Determines whether to use priority capacity (if available) or standard capacity for this request.

        Anthropic offers different levels of service for your API requests. See [service-tiers](https://docs.claude.com/en/api/service-tiers) for details.

        - `AUTO("auto")`

        - `STANDARD_ONLY("standard_only")`

      - `stopSequences: Optional<List<String>>`

        Custom text sequences that will cause the model to stop generating.

        Our models will normally stop when they have naturally completed their turn, which will result in a response `stop_reason` of `"end_turn"`.

        If you want the model to stop generating when it encounters custom strings of text, you can use the `stop_sequences` parameter. If the model encounters one of the custom sequences, the response `stop_reason` value will be `"stop_sequence"` and the response `stop_sequence` value will contain the matched stop sequence.

      - `stream: Optional<Boolean>`

        Whether to incrementally stream the response using server-sent events.

        See [streaming](https://docs.claude.com/en/api/messages-streaming) for details.

      - `system: Optional<System>`

        System prompt.

        A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

        - `String`

        - `List<BetaTextBlockParam>`

          - `text: String`

          - `type: JsonValue; "text"constant`

            - `TEXT("text")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<List<BetaTextCitationParam>>`

            - `class BetaCitationCharLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class BetaCitationPageLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class BetaCitationContentBlockLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class BetaCitationWebSearchResultLocationParam:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class BetaCitationSearchResultLocationParam:`

              - `citedText: String`

              - `endBlockIndex: Long`

              - `searchResultIndex: Long`

              - `source: String`

              - `startBlockIndex: Long`

              - `title: Optional<String>`

              - `type: JsonValue; "search_result_location"constant`

                - `SEARCH_RESULT_LOCATION("search_result_location")`

      - `temperature: Optional<Double>`

        Amount of randomness injected into the response.

        Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.

        Note that even with `temperature` of `0.0`, the results will not be fully deterministic.

      - `thinking: Optional<BetaThinkingConfigParam>`

        Configuration for enabling Claude's extended thinking.

        When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

        See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

        - `class BetaThinkingConfigEnabled:`

          - `budgetTokens: Long`

            Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

            Must be ≥1024 and less than `max_tokens`.

            See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

          - `type: JsonValue; "enabled"constant`

            - `ENABLED("enabled")`

        - `class BetaThinkingConfigDisabled:`

          - `type: JsonValue; "disabled"constant`

            - `DISABLED("disabled")`

      - `toolChoice: Optional<BetaToolChoice>`

        How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

        - `class BetaToolChoiceAuto:`

          The model will automatically decide whether to use tools.

          - `type: JsonValue; "auto"constant`

            - `AUTO("auto")`

          - `disableParallelToolUse: Optional<Boolean>`

            Whether to disable parallel tool use.

            Defaults to `false`. If set to `true`, the model will output at most one tool use.

        - `class BetaToolChoiceAny:`

          The model will use any available tools.

          - `type: JsonValue; "any"constant`

            - `ANY("any")`

          - `disableParallelToolUse: Optional<Boolean>`

            Whether to disable parallel tool use.

            Defaults to `false`. If set to `true`, the model will output exactly one tool use.

        - `class BetaToolChoiceTool:`

          The model will use the specified tool with `tool_choice.name`.

          - `name: String`

            The name of the tool to use.

          - `type: JsonValue; "tool"constant`

            - `TOOL("tool")`

          - `disableParallelToolUse: Optional<Boolean>`

            Whether to disable parallel tool use.

            Defaults to `false`. If set to `true`, the model will output exactly one tool use.

        - `class BetaToolChoiceNone:`

          The model will not be allowed to use tools.

          - `type: JsonValue; "none"constant`

            - `NONE("none")`

      - `tools: Optional<List<BetaToolUnion>>`

        Definitions of tools that the model may use.

        If you include `tools` in your API request, the model may return `tool_use` content blocks that represent the model's use of those tools. You can then run those tools using the tool input generated by the model and then optionally return results back to the model using `tool_result` content blocks.

        There are two types of tools: **client tools** and **server tools**. The behavior described below applies to client tools. For [server tools](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview#server-tools), see their individual documentation as each has its own behavior (e.g., the [web search tool](https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-search-tool)).

        Each tool definition includes:

        * `name`: Name of the tool.
        * `description`: Optional, but strongly-recommended description of the tool.
        * `input_schema`: [JSON schema](https://json-schema.org/draft/2020-12) for the tool `input` shape that the model will produce in `tool_use` output content blocks.

        For example, if you defined `tools` as:

        ```json
        [
          {
            "name": "get_stock_price",
            "description": "Get the current stock price for a given ticker symbol.",
            "input_schema": {
              "type": "object",
              "properties": {
                "ticker": {
                  "type": "string",
                  "description": "The stock ticker symbol, e.g. AAPL for Apple Inc."
                }
              },
              "required": ["ticker"]
            }
          }
        ]
        ```

        And then asked the model "What's the S&P 500 at today?", the model might produce `tool_use` content blocks in the response like this:

        ```json
        [
          {
            "type": "tool_use",
            "id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
            "name": "get_stock_price",
            "input": { "ticker": "^GSPC" }
          }
        ]
        ```

        You might then run your `get_stock_price` tool with `{"ticker": "^GSPC"}` as an input, and return the following back to the model in a subsequent `user` message:

        ```json
        [
          {
            "type": "tool_result",
            "tool_use_id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
            "content": "259.75 USD"
          }
        ]
        ```

        Tools can be used for workflows that include running client-side tools and functions, or more generally whenever you want the model to produce a particular JSON structure of output.

        See our [guide](https://docs.claude.com/en/docs/tool-use) for more details.

        - `class BetaTool:`

          - `inputSchema: InputSchema`

            [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

            This defines the shape of the `input` that your tool accepts and that the model will produce.

            - `type: JsonValue; "object"constant`

              - `OBJECT("object")`

            - `properties: Optional<Properties>`

            - `required: Optional<List<String>>`

          - `name: String`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `description: Optional<String>`

            Description of what this tool does.

            Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

          - `inputExamples: Optional<List<InputExample>>`

          - `strict: Optional<Boolean>`

          - `type: Optional<Type>`

            - `CUSTOM("custom")`

        - `class BetaToolBash20241022:`

          - `name: JsonValue; "bash"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `BASH("bash")`

          - `type: JsonValue; "bash_20241022"constant`

            - `BASH_20241022("bash_20241022")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `inputExamples: Optional<List<InputExample>>`

          - `strict: Optional<Boolean>`

        - `class BetaToolBash20250124:`

          - `name: JsonValue; "bash"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `BASH("bash")`

          - `type: JsonValue; "bash_20250124"constant`

            - `BASH_20250124("bash_20250124")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `inputExamples: Optional<List<InputExample>>`

          - `strict: Optional<Boolean>`

        - `class BetaCodeExecutionTool20250522:`

          - `name: JsonValue; "code_execution"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `CODE_EXECUTION("code_execution")`

          - `type: JsonValue; "code_execution_20250522"constant`

            - `CODE_EXECUTION_20250522("code_execution_20250522")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `strict: Optional<Boolean>`

        - `class BetaCodeExecutionTool20250825:`

          - `name: JsonValue; "code_execution"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `CODE_EXECUTION("code_execution")`

          - `type: JsonValue; "code_execution_20250825"constant`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `strict: Optional<Boolean>`

        - `class BetaToolComputerUse20241022:`

          - `displayHeightPx: Long`

            The height of the display in pixels.

          - `displayWidthPx: Long`

            The width of the display in pixels.

          - `name: JsonValue; "computer"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `COMPUTER("computer")`

          - `type: JsonValue; "computer_20241022"constant`

            - `COMPUTER_20241022("computer_20241022")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `displayNumber: Optional<Long>`

            The X11 display number (e.g. 0, 1) for the display.

          - `inputExamples: Optional<List<InputExample>>`

          - `strict: Optional<Boolean>`

        - `class BetaMemoryTool20250818:`

          - `name: JsonValue; "memory"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `MEMORY("memory")`

          - `type: JsonValue; "memory_20250818"constant`

            - `MEMORY_20250818("memory_20250818")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `inputExamples: Optional<List<InputExample>>`

          - `strict: Optional<Boolean>`

        - `class BetaToolComputerUse20250124:`

          - `displayHeightPx: Long`

            The height of the display in pixels.

          - `displayWidthPx: Long`

            The width of the display in pixels.

          - `name: JsonValue; "computer"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `COMPUTER("computer")`

          - `type: JsonValue; "computer_20250124"constant`

            - `COMPUTER_20250124("computer_20250124")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `displayNumber: Optional<Long>`

            The X11 display number (e.g. 0, 1) for the display.

          - `inputExamples: Optional<List<InputExample>>`

          - `strict: Optional<Boolean>`

        - `class BetaToolTextEditor20241022:`

          - `name: JsonValue; "str_replace_editor"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `STR_REPLACE_EDITOR("str_replace_editor")`

          - `type: JsonValue; "text_editor_20241022"constant`

            - `TEXT_EDITOR_20241022("text_editor_20241022")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `inputExamples: Optional<List<InputExample>>`

          - `strict: Optional<Boolean>`

        - `class BetaToolComputerUse20251124:`

          - `displayHeightPx: Long`

            The height of the display in pixels.

          - `displayWidthPx: Long`

            The width of the display in pixels.

          - `name: JsonValue; "computer"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `COMPUTER("computer")`

          - `type: JsonValue; "computer_20251124"constant`

            - `COMPUTER_20251124("computer_20251124")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `displayNumber: Optional<Long>`

            The X11 display number (e.g. 0, 1) for the display.

          - `enableZoom: Optional<Boolean>`

            Whether to enable an action to take a zoomed-in screenshot of the screen.

          - `inputExamples: Optional<List<InputExample>>`

          - `strict: Optional<Boolean>`

        - `class BetaToolTextEditor20250124:`

          - `name: JsonValue; "str_replace_editor"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `STR_REPLACE_EDITOR("str_replace_editor")`

          - `type: JsonValue; "text_editor_20250124"constant`

            - `TEXT_EDITOR_20250124("text_editor_20250124")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `inputExamples: Optional<List<InputExample>>`

          - `strict: Optional<Boolean>`

        - `class BetaToolTextEditor20250429:`

          - `name: JsonValue; "str_replace_based_edit_tool"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

          - `type: JsonValue; "text_editor_20250429"constant`

            - `TEXT_EDITOR_20250429("text_editor_20250429")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `inputExamples: Optional<List<InputExample>>`

          - `strict: Optional<Boolean>`

        - `class BetaToolTextEditor20250728:`

          - `name: JsonValue; "str_replace_based_edit_tool"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

          - `type: JsonValue; "text_editor_20250728"constant`

            - `TEXT_EDITOR_20250728("text_editor_20250728")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `inputExamples: Optional<List<InputExample>>`

          - `maxCharacters: Optional<Long>`

            Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

          - `strict: Optional<Boolean>`

        - `class BetaWebSearchTool20250305:`

          - `name: JsonValue; "web_search"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `WEB_SEARCH("web_search")`

          - `type: JsonValue; "web_search_20250305"constant`

            - `WEB_SEARCH_20250305("web_search_20250305")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `allowedDomains: Optional<List<String>>`

            If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

          - `blockedDomains: Optional<List<String>>`

            If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `maxUses: Optional<Long>`

            Maximum number of times the tool can be used in the API request.

          - `strict: Optional<Boolean>`

          - `userLocation: Optional<UserLocation>`

            Parameters for the user's location. Used to provide more relevant search results.

            - `type: JsonValue; "approximate"constant`

              - `APPROXIMATE("approximate")`

            - `city: Optional<String>`

              The city of the user.

            - `country: Optional<String>`

              The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

            - `region: Optional<String>`

              The region of the user.

            - `timezone: Optional<String>`

              The [IANA timezone](https://nodatime.org/TimeZones) of the user.

        - `class BetaWebFetchTool20250910:`

          - `name: JsonValue; "web_fetch"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `WEB_FETCH("web_fetch")`

          - `type: JsonValue; "web_fetch_20250910"constant`

            - `WEB_FETCH_20250910("web_fetch_20250910")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `allowedDomains: Optional<List<String>>`

            List of domains to allow fetching from

          - `blockedDomains: Optional<List<String>>`

            List of domains to block fetching from

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<BetaCitationsConfigParam>`

            Citations configuration for fetched documents. Citations are disabled by default.

            - `enabled: Optional<Boolean>`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `maxContentTokens: Optional<Long>`

            Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

          - `maxUses: Optional<Long>`

            Maximum number of times the tool can be used in the API request.

          - `strict: Optional<Boolean>`

        - `class BetaToolSearchToolBm25_20251119:`

          - `name: JsonValue; "tool_search_tool_bm25"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

          - `type: Type`

            - `TOOL_SEARCH_TOOL_BM25_20251119("tool_search_tool_bm25_20251119")`

            - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `strict: Optional<Boolean>`

        - `class BetaToolSearchToolRegex20251119:`

          - `name: JsonValue; "tool_search_tool_regex"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

          - `type: Type`

            - `TOOL_SEARCH_TOOL_REGEX_20251119("tool_search_tool_regex_20251119")`

            - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

          - `allowedCallers: Optional<List<AllowedCaller>>`

            - `DIRECT("direct")`

            - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `deferLoading: Optional<Boolean>`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `strict: Optional<Boolean>`

        - `class BetaMcpToolset:`

          Configuration for a group of tools from an MCP server.

          Allows configuring enabled status and defer_loading for all tools
          from an MCP server, with optional per-tool overrides.

          - `mcpServerName: String`

            Name of the MCP server to configure tools for

          - `type: JsonValue; "mcp_toolset"constant`

            - `MCP_TOOLSET("mcp_toolset")`

          - `cacheControl: Optional<BetaCacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `configs: Optional<Configs>`

            Configuration overrides for specific tools, keyed by tool name

            - `deferLoading: Optional<Boolean>`

            - `enabled: Optional<Boolean>`

          - `defaultConfig: Optional<BetaMcpToolDefaultConfig>`

            Default configuration applied to all tools from this server

            - `deferLoading: Optional<Boolean>`

            - `enabled: Optional<Boolean>`

      - `topK: Optional<Long>`

        Only sample from the top K options for each subsequent token.

        Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

        Recommended for advanced use cases only. You usually only need to use `temperature`.

      - `topP: Optional<Double>`

        Use nucleus sampling.

        In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

        Recommended for advanced use cases only. You usually only need to use `temperature`.

### Returns

- `class BetaMessageBatch:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archivedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancelInitiatedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `createdAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `endedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expiresAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processingStatus: ProcessingStatus`

    Processing status of the Message Batch.

    - `IN_PROGRESS("in_progress")`

    - `CANCELING("canceling")`

    - `ENDED("ended")`

  - `requestCounts: BetaMessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: Long`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: Long`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: Long`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: Long`

      Number of requests in the Message Batch that are processing.

    - `succeeded: Long`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `resultsUrl: Optional<String>`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: JsonValue; "message_batch"constant`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `MESSAGE_BATCH("message_batch")`

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.messages.batches.BatchCreateParams
import com.anthropic.models.beta.messages.batches.BetaMessageBatch
import com.anthropic.models.messages.Model

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val params: BatchCreateParams = BatchCreateParams.builder()
        .addRequest(BatchCreateParams.Request.builder()
            .customId("my-custom-id-1")
            .params(BatchCreateParams.Request.Params.builder()
                .maxTokens(1024L)
                .addUserMessage("Hello, world")
                .model(Model.CLAUDE_OPUS_4_5_20251101)
                .build())
            .build())
        .build()
    val betaMessageBatch: BetaMessageBatch = client.beta().messages().batches().create(params)
}
```

## Retrieve

`beta().messages().batches().retrieve(BatchRetrieveParamsparams = BatchRetrieveParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : BetaMessageBatch`

**get** `/v1/messages/batches/{message_batch_id}`

This endpoint is idempotent and can be used to poll for Message Batch completion. To access the results of a Message Batch, make a request to the `results_url` field in the response.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchRetrieveParams`

  - `messageBatchId: Optional<String>`

    ID of the Message Batch.

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

### Returns

- `class BetaMessageBatch:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archivedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancelInitiatedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `createdAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `endedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expiresAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processingStatus: ProcessingStatus`

    Processing status of the Message Batch.

    - `IN_PROGRESS("in_progress")`

    - `CANCELING("canceling")`

    - `ENDED("ended")`

  - `requestCounts: BetaMessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: Long`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: Long`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: Long`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: Long`

      Number of requests in the Message Batch that are processing.

    - `succeeded: Long`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `resultsUrl: Optional<String>`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: JsonValue; "message_batch"constant`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `MESSAGE_BATCH("message_batch")`

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.messages.batches.BatchRetrieveParams
import com.anthropic.models.beta.messages.batches.BetaMessageBatch

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val betaMessageBatch: BetaMessageBatch = client.beta().messages().batches().retrieve("message_batch_id")
}
```

## List

`beta().messages().batches().list(BatchListParamsparams = BatchListParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : BatchListPage`

**get** `/v1/messages/batches`

List all Message Batches within a Workspace. Most recently created batches are returned first.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchListParams`

  - `afterId: Optional<String>`

    ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

  - `beforeId: Optional<String>`

    ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

  - `limit: Optional<Long>`

    Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `1000`.

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

### Returns

- `class BetaMessageBatch:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archivedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancelInitiatedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `createdAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `endedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expiresAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processingStatus: ProcessingStatus`

    Processing status of the Message Batch.

    - `IN_PROGRESS("in_progress")`

    - `CANCELING("canceling")`

    - `ENDED("ended")`

  - `requestCounts: BetaMessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: Long`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: Long`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: Long`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: Long`

      Number of requests in the Message Batch that are processing.

    - `succeeded: Long`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `resultsUrl: Optional<String>`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: JsonValue; "message_batch"constant`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `MESSAGE_BATCH("message_batch")`

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.messages.batches.BatchListPage
import com.anthropic.models.beta.messages.batches.BatchListParams

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val page: BatchListPage = client.beta().messages().batches().list()
}
```

## Cancel

`beta().messages().batches().cancel(BatchCancelParamsparams = BatchCancelParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : BetaMessageBatch`

**post** `/v1/messages/batches/{message_batch_id}/cancel`

Batches may be canceled any time before processing ends. Once cancellation is initiated, the batch enters a `canceling` state, at which time the system may complete any in-progress, non-interruptible requests before finalizing cancellation.

The number of canceled requests is specified in `request_counts`. To determine which requests were canceled, check the individual results within the batch. Note that cancellation may not result in any canceled requests if they were non-interruptible.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchCancelParams`

  - `messageBatchId: Optional<String>`

    ID of the Message Batch.

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

### Returns

- `class BetaMessageBatch:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archivedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancelInitiatedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `createdAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `endedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expiresAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processingStatus: ProcessingStatus`

    Processing status of the Message Batch.

    - `IN_PROGRESS("in_progress")`

    - `CANCELING("canceling")`

    - `ENDED("ended")`

  - `requestCounts: BetaMessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: Long`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: Long`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: Long`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: Long`

      Number of requests in the Message Batch that are processing.

    - `succeeded: Long`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `resultsUrl: Optional<String>`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: JsonValue; "message_batch"constant`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `MESSAGE_BATCH("message_batch")`

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.messages.batches.BatchCancelParams
import com.anthropic.models.beta.messages.batches.BetaMessageBatch

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val betaMessageBatch: BetaMessageBatch = client.beta().messages().batches().cancel("message_batch_id")
}
```

## Delete

`beta().messages().batches().delete(BatchDeleteParamsparams = BatchDeleteParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : BetaDeletedMessageBatch`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchDeleteParams`

  - `messageBatchId: Optional<String>`

    ID of the Message Batch.

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

### Returns

- `class BetaDeletedMessageBatch:`

  - `id: String`

    ID of the Message Batch.

  - `type: JsonValue; "message_batch_deleted"constant`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `MESSAGE_BATCH_DELETED("message_batch_deleted")`

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.messages.batches.BatchDeleteParams
import com.anthropic.models.beta.messages.batches.BetaDeletedMessageBatch

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val betaDeletedMessageBatch: BetaDeletedMessageBatch = client.beta().messages().batches().delete("message_batch_id")
}
```

## Results

`beta().messages().batches().resultsStreaming(BatchResultsParamsparams = BatchResultsParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : BetaMessageBatchIndividualResponse`

**get** `/v1/messages/batches/{message_batch_id}/results`

Streams the results of a Message Batch as a `.jsonl` file.

Each line in the file is a JSON object containing the result of a single request in the Message Batch. Results are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchResultsParams`

  - `messageBatchId: Optional<String>`

    ID of the Message Batch.

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

### Returns

- `class BetaMessageBatchIndividualResponse:`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `customId: String`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: BetaMessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `class BetaMessageBatchSucceededResult:`

      - `message: BetaMessage`

        - `id: String`

          Unique object identifier.

          The format and length of IDs may change over time.

        - `container: Optional<BetaContainer>`

          Information about the container used in the request (for the code execution tool)

          - `id: String`

            Identifier for the container used in this request

          - `expiresAt: LocalDateTime`

            The time at which the container will expire.

          - `skills: Optional<List<BetaSkill>>`

            Skills loaded in the container

            - `skillId: String`

              Skill ID

            - `type: Type`

              Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

              - `ANTHROPIC("anthropic")`

              - `CUSTOM("custom")`

            - `version: String`

              Skill version or 'latest' for most recent version

        - `content: List<BetaContentBlock>`

          Content generated by the model.

          This is an array of content blocks, each of which has a `type` that determines its shape.

          Example:

          ```json
          [{"type": "text", "text": "Hi, I'm Claude."}]
          ```

          If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

          For example, if the input `messages` were:

          ```json
          [
            {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
            {"role": "assistant", "content": "The best answer is ("}
          ]
          ```

          Then the response `content` might be:

          ```json
          [{"type": "text", "text": "B)"}]
          ```

          - `class BetaTextBlock:`

            - `citations: Optional<List<BetaTextCitation>>`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class BetaCitationCharLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endCharIndex: Long`

                - `fileId: Optional<String>`

                - `startCharIndex: Long`

                - `type: JsonValue; "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class BetaCitationPageLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endPageNumber: Long`

                - `fileId: Optional<String>`

                - `startPageNumber: Long`

                - `type: JsonValue; "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class BetaCitationContentBlockLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endBlockIndex: Long`

                - `fileId: Optional<String>`

                - `startBlockIndex: Long`

                - `type: JsonValue; "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class BetaCitationsWebSearchResultLocation:`

                - `citedText: String`

                - `encryptedIndex: String`

                - `title: Optional<String>`

                - `type: JsonValue; "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `url: String`

              - `class BetaCitationSearchResultLocation:`

                - `citedText: String`

                - `endBlockIndex: Long`

                - `searchResultIndex: Long`

                - `source: String`

                - `startBlockIndex: Long`

                - `title: Optional<String>`

                - `type: JsonValue; "search_result_location"constant`

                  - `SEARCH_RESULT_LOCATION("search_result_location")`

            - `text: String`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

          - `class BetaThinkingBlock:`

            - `signature: String`

            - `thinking: String`

            - `type: JsonValue; "thinking"constant`

              - `THINKING("thinking")`

          - `class BetaRedactedThinkingBlock:`

            - `data: String`

            - `type: JsonValue; "redacted_thinking"constant`

              - `REDACTED_THINKING("redacted_thinking")`

          - `class BetaToolUseBlock:`

            - `id: String`

            - `input: Input`

            - `name: String`

            - `type: JsonValue; "tool_use"constant`

              - `TOOL_USE("tool_use")`

            - `caller: Optional<Caller>`

              Tool invocation directly from the model.

              - `class BetaDirectCaller:`

                Tool invocation directly from the model.

                - `type: JsonValue; "direct"constant`

                  - `DIRECT("direct")`

              - `class BetaServerToolCaller:`

                Tool invocation generated by a server-side tool.

                - `toolId: String`

                - `type: JsonValue; "code_execution_20250825"constant`

                  - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `class BetaServerToolUseBlock:`

            - `id: String`

            - `caller: Caller`

              Tool invocation directly from the model.

              - `class BetaDirectCaller:`

                Tool invocation directly from the model.

                - `type: JsonValue; "direct"constant`

                  - `DIRECT("direct")`

              - `class BetaServerToolCaller:`

                Tool invocation generated by a server-side tool.

                - `toolId: String`

                - `type: JsonValue; "code_execution_20250825"constant`

                  - `CODE_EXECUTION_20250825("code_execution_20250825")`

            - `input: Input`

            - `name: Name`

              - `WEB_SEARCH("web_search")`

              - `WEB_FETCH("web_fetch")`

              - `CODE_EXECUTION("code_execution")`

              - `BASH_CODE_EXECUTION("bash_code_execution")`

              - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

              - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

              - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

            - `type: JsonValue; "server_tool_use"constant`

              - `SERVER_TOOL_USE("server_tool_use")`

          - `class BetaWebSearchToolResultBlock:`

            - `content: BetaWebSearchToolResultBlockContent`

              - `class BetaWebSearchToolResultError:`

                - `errorCode: BetaWebSearchToolResultErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `UNAVAILABLE("unavailable")`

                  - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `QUERY_TOO_LONG("query_too_long")`

                - `type: JsonValue; "web_search_tool_result_error"constant`

                  - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

              - `List<BetaWebSearchResultBlock>`

                - `encryptedContent: String`

                - `pageAge: Optional<String>`

                - `title: String`

                - `type: JsonValue; "web_search_result"constant`

                  - `WEB_SEARCH_RESULT("web_search_result")`

                - `url: String`

            - `toolUseId: String`

            - `type: JsonValue; "web_search_tool_result"constant`

              - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

          - `class BetaWebFetchToolResultBlock:`

            - `content: Content`

              - `class BetaWebFetchToolResultErrorBlock:`

                - `errorCode: BetaWebFetchToolResultErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `URL_TOO_LONG("url_too_long")`

                  - `URL_NOT_ALLOWED("url_not_allowed")`

                  - `URL_NOT_ACCESSIBLE("url_not_accessible")`

                  - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                  - `UNAVAILABLE("unavailable")`

                - `type: JsonValue; "web_fetch_tool_result_error"constant`

                  - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

              - `class BetaWebFetchBlock:`

                - `content: BetaDocumentBlock`

                  - `citations: Optional<BetaCitationConfig>`

                    Citation configuration for the document

                    - `enabled: Boolean`

                  - `source: Source`

                    - `class BetaBase64PdfSource:`

                      - `data: String`

                      - `mediaType: JsonValue; "application/pdf"constant`

                        - `APPLICATION_PDF("application/pdf")`

                      - `type: JsonValue; "base64"constant`

                        - `BASE64("base64")`

                    - `class BetaPlainTextSource:`

                      - `data: String`

                      - `mediaType: JsonValue; "text/plain"constant`

                        - `TEXT_PLAIN("text/plain")`

                      - `type: JsonValue; "text"constant`

                        - `TEXT("text")`

                  - `title: Optional<String>`

                    The title of the document

                  - `type: JsonValue; "document"constant`

                    - `DOCUMENT("document")`

                - `retrievedAt: Optional<String>`

                  ISO 8601 timestamp when the content was retrieved

                - `type: JsonValue; "web_fetch_result"constant`

                  - `WEB_FETCH_RESULT("web_fetch_result")`

                - `url: String`

                  Fetched content URL

            - `toolUseId: String`

            - `type: JsonValue; "web_fetch_tool_result"constant`

              - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

          - `class BetaCodeExecutionToolResultBlock:`

            - `content: BetaCodeExecutionToolResultBlockContent`

              - `class BetaCodeExecutionToolResultError:`

                - `errorCode: BetaCodeExecutionToolResultErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `UNAVAILABLE("unavailable")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `type: JsonValue; "code_execution_tool_result_error"constant`

                  - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

              - `class BetaCodeExecutionResultBlock:`

                - `content: List<BetaCodeExecutionOutputBlock>`

                  - `fileId: String`

                  - `type: JsonValue; "code_execution_output"constant`

                    - `CODE_EXECUTION_OUTPUT("code_execution_output")`

                - `returnCode: Long`

                - `stderr: String`

                - `stdout: String`

                - `type: JsonValue; "code_execution_result"constant`

                  - `CODE_EXECUTION_RESULT("code_execution_result")`

            - `toolUseId: String`

            - `type: JsonValue; "code_execution_tool_result"constant`

              - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

          - `class BetaBashCodeExecutionToolResultBlock:`

            - `content: Content`

              - `class BetaBashCodeExecutionToolResultError:`

                - `errorCode: ErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `UNAVAILABLE("unavailable")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                  - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

                - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

                  - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

              - `class BetaBashCodeExecutionResultBlock:`

                - `content: List<BetaBashCodeExecutionOutputBlock>`

                  - `fileId: String`

                  - `type: JsonValue; "bash_code_execution_output"constant`

                    - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

                - `returnCode: Long`

                - `stderr: String`

                - `stdout: String`

                - `type: JsonValue; "bash_code_execution_result"constant`

                  - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

            - `toolUseId: String`

            - `type: JsonValue; "bash_code_execution_tool_result"constant`

              - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

          - `class BetaTextEditorCodeExecutionToolResultBlock:`

            - `content: Content`

              - `class BetaTextEditorCodeExecutionToolResultError:`

                - `errorCode: ErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `UNAVAILABLE("unavailable")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                  - `FILE_NOT_FOUND("file_not_found")`

                - `errorMessage: Optional<String>`

                - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

                  - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

              - `class BetaTextEditorCodeExecutionViewResultBlock:`

                - `content: String`

                - `fileType: FileType`

                  - `TEXT("text")`

                  - `IMAGE("image")`

                  - `PDF("pdf")`

                - `numLines: Optional<Long>`

                - `startLine: Optional<Long>`

                - `totalLines: Optional<Long>`

                - `type: JsonValue; "text_editor_code_execution_view_result"constant`

                  - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

              - `class BetaTextEditorCodeExecutionCreateResultBlock:`

                - `isFileUpdate: Boolean`

                - `type: JsonValue; "text_editor_code_execution_create_result"constant`

                  - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

              - `class BetaTextEditorCodeExecutionStrReplaceResultBlock:`

                - `lines: Optional<List<String>>`

                - `newLines: Optional<Long>`

                - `newStart: Optional<Long>`

                - `oldLines: Optional<Long>`

                - `oldStart: Optional<Long>`

                - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

                  - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

            - `toolUseId: String`

            - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

          - `class BetaToolSearchToolResultBlock:`

            - `content: Content`

              - `class BetaToolSearchToolResultError:`

                - `errorCode: ErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `UNAVAILABLE("unavailable")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `errorMessage: Optional<String>`

                - `type: JsonValue; "tool_search_tool_result_error"constant`

                  - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

              - `class BetaToolSearchToolSearchResultBlock:`

                - `toolReferences: List<BetaToolReferenceBlock>`

                  - `toolName: String`

                  - `type: JsonValue; "tool_reference"constant`

                    - `TOOL_REFERENCE("tool_reference")`

                - `type: JsonValue; "tool_search_tool_search_result"constant`

                  - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

            - `toolUseId: String`

            - `type: JsonValue; "tool_search_tool_result"constant`

              - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

          - `class BetaMcpToolUseBlock:`

            - `id: String`

            - `input: Input`

            - `name: String`

              The name of the MCP tool

            - `serverName: String`

              The name of the MCP server

            - `type: JsonValue; "mcp_tool_use"constant`

              - `MCP_TOOL_USE("mcp_tool_use")`

          - `class BetaMcpToolResultBlock:`

            - `content: Content`

              - `String`

              - `List<BetaTextBlock>`

                - `citations: Optional<List<BetaTextCitation>>`

                  Citations supporting the text block.

                  The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

                  - `class BetaCitationCharLocation:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endCharIndex: Long`

                    - `fileId: Optional<String>`

                    - `startCharIndex: Long`

                    - `type: JsonValue; "char_location"constant`

                      - `CHAR_LOCATION("char_location")`

                  - `class BetaCitationPageLocation:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endPageNumber: Long`

                    - `fileId: Optional<String>`

                    - `startPageNumber: Long`

                    - `type: JsonValue; "page_location"constant`

                      - `PAGE_LOCATION("page_location")`

                  - `class BetaCitationContentBlockLocation:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endBlockIndex: Long`

                    - `fileId: Optional<String>`

                    - `startBlockIndex: Long`

                    - `type: JsonValue; "content_block_location"constant`

                      - `CONTENT_BLOCK_LOCATION("content_block_location")`

                  - `class BetaCitationsWebSearchResultLocation:`

                    - `citedText: String`

                    - `encryptedIndex: String`

                    - `title: Optional<String>`

                    - `type: JsonValue; "web_search_result_location"constant`

                      - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                    - `url: String`

                  - `class BetaCitationSearchResultLocation:`

                    - `citedText: String`

                    - `endBlockIndex: Long`

                    - `searchResultIndex: Long`

                    - `source: String`

                    - `startBlockIndex: Long`

                    - `title: Optional<String>`

                    - `type: JsonValue; "search_result_location"constant`

                      - `SEARCH_RESULT_LOCATION("search_result_location")`

                - `text: String`

                - `type: JsonValue; "text"constant`

                  - `TEXT("text")`

            - `isError: Boolean`

            - `toolUseId: String`

            - `type: JsonValue; "mcp_tool_result"constant`

              - `MCP_TOOL_RESULT("mcp_tool_result")`

          - `class BetaContainerUploadBlock:`

            Response model for a file uploaded to the container.

            - `fileId: String`

            - `type: JsonValue; "container_upload"constant`

              - `CONTAINER_UPLOAD("container_upload")`

        - `contextManagement: Optional<BetaContextManagementResponse>`

          Context management response.

          Information about context management strategies applied during the request.

          - `appliedEdits: List<AppliedEdit>`

            List of context management edits that were applied.

            - `class BetaClearToolUses20250919EditResponse:`

              - `clearedInputTokens: Long`

                Number of input tokens cleared by this edit.

              - `clearedToolUses: Long`

                Number of tool uses that were cleared.

              - `type: JsonValue; "clear_tool_uses_20250919"constant`

                The type of context management edit applied.

                - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

            - `class BetaClearThinking20251015EditResponse:`

              - `clearedInputTokens: Long`

                Number of input tokens cleared by this edit.

              - `clearedThinkingTurns: Long`

                Number of thinking turns that were cleared.

              - `type: JsonValue; "clear_thinking_20251015"constant`

                The type of context management edit applied.

                - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

        - `model: Model`

          The model that will complete your prompt.

          See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

          - `CLAUDE_OPUS_4_5_20251101("claude-opus-4-5-20251101")`

            Premium model combining maximum intelligence with practical performance

          - `CLAUDE_OPUS_4_5("claude-opus-4-5")`

            Premium model combining maximum intelligence with practical performance

          - `CLAUDE_3_7_SONNET_LATEST("claude-3-7-sonnet-latest")`

            High-performance model with early extended thinking

          - `CLAUDE_3_7_SONNET_20250219("claude-3-7-sonnet-20250219")`

            High-performance model with early extended thinking

          - `CLAUDE_3_5_HAIKU_LATEST("claude-3-5-haiku-latest")`

            Fastest and most compact model for near-instant responsiveness

          - `CLAUDE_3_5_HAIKU_20241022("claude-3-5-haiku-20241022")`

            Our fastest model

          - `CLAUDE_HAIKU_4_5("claude-haiku-4-5")`

            Hybrid model, capable of near-instant responses and extended thinking

          - `CLAUDE_HAIKU_4_5_20251001("claude-haiku-4-5-20251001")`

            Hybrid model, capable of near-instant responses and extended thinking

          - `CLAUDE_SONNET_4_20250514("claude-sonnet-4-20250514")`

            High-performance model with extended thinking

          - `CLAUDE_SONNET_4_0("claude-sonnet-4-0")`

            High-performance model with extended thinking

          - `CLAUDE_4_SONNET_20250514("claude-4-sonnet-20250514")`

            High-performance model with extended thinking

          - `CLAUDE_SONNET_4_5("claude-sonnet-4-5")`

            Our best model for real-world agents and coding

          - `CLAUDE_SONNET_4_5_20250929("claude-sonnet-4-5-20250929")`

            Our best model for real-world agents and coding

          - `CLAUDE_OPUS_4_0("claude-opus-4-0")`

            Our most capable model

          - `CLAUDE_OPUS_4_20250514("claude-opus-4-20250514")`

            Our most capable model

          - `CLAUDE_4_OPUS_20250514("claude-4-opus-20250514")`

            Our most capable model

          - `CLAUDE_OPUS_4_1_20250805("claude-opus-4-1-20250805")`

            Our most capable model

          - `CLAUDE_3_OPUS_LATEST("claude-3-opus-latest")`

            Excels at writing and complex tasks

          - `CLAUDE_3_OPUS_20240229("claude-3-opus-20240229")`

            Excels at writing and complex tasks

          - `CLAUDE_3_HAIKU_20240307("claude-3-haiku-20240307")`

            Our previous most fast and cost-effective

        - `role: JsonValue; "assistant"constant`

          Conversational role of the generated message.

          This will always be `"assistant"`.

          - `ASSISTANT("assistant")`

        - `stopReason: Optional<BetaStopReason>`

          The reason that we stopped.

          This may be one the following values:

          * `"end_turn"`: the model reached a natural stopping point
          * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
          * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
          * `"tool_use"`: the model invoked one or more tools
          * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
          * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

          In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

          - `END_TURN("end_turn")`

          - `MAX_TOKENS("max_tokens")`

          - `STOP_SEQUENCE("stop_sequence")`

          - `TOOL_USE("tool_use")`

          - `PAUSE_TURN("pause_turn")`

          - `REFUSAL("refusal")`

          - `MODEL_CONTEXT_WINDOW_EXCEEDED("model_context_window_exceeded")`

        - `stopSequence: Optional<String>`

          Which custom stop sequence was generated, if any.

          This value will be a non-null string if one of your custom stop sequences was generated.

        - `type: JsonValue; "message"constant`

          Object type.

          For Messages, this is always `"message"`.

          - `MESSAGE("message")`

        - `usage: BetaUsage`

          Billing and rate-limit usage.

          Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

          Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

          For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

          Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

          - `cacheCreation: Optional<BetaCacheCreation>`

            Breakdown of cached tokens by TTL

            - `ephemeral1hInputTokens: Long`

              The number of input tokens used to create the 1 hour cache entry.

            - `ephemeral5mInputTokens: Long`

              The number of input tokens used to create the 5 minute cache entry.

          - `cacheCreationInputTokens: Optional<Long>`

            The number of input tokens used to create the cache entry.

          - `cacheReadInputTokens: Optional<Long>`

            The number of input tokens read from the cache.

          - `inputTokens: Long`

            The number of input tokens which were used.

          - `outputTokens: Long`

            The number of output tokens which were used.

          - `serverToolUse: Optional<BetaServerToolUsage>`

            The number of server tool requests.

            - `webFetchRequests: Long`

              The number of web fetch tool requests.

            - `webSearchRequests: Long`

              The number of web search tool requests.

          - `serviceTier: Optional<ServiceTier>`

            If the request used the priority, standard, or batch tier.

            - `STANDARD("standard")`

            - `PRIORITY("priority")`

            - `BATCH("batch")`

      - `type: JsonValue; "succeeded"constant`

        - `SUCCEEDED("succeeded")`

    - `class BetaMessageBatchErroredResult:`

      - `error: BetaErrorResponse`

        - `error: BetaError`

          - `class BetaInvalidRequestError:`

            - `message: String`

            - `type: JsonValue; "invalid_request_error"constant`

              - `INVALID_REQUEST_ERROR("invalid_request_error")`

          - `class BetaAuthenticationError:`

            - `message: String`

            - `type: JsonValue; "authentication_error"constant`

              - `AUTHENTICATION_ERROR("authentication_error")`

          - `class BetaBillingError:`

            - `message: String`

            - `type: JsonValue; "billing_error"constant`

              - `BILLING_ERROR("billing_error")`

          - `class BetaPermissionError:`

            - `message: String`

            - `type: JsonValue; "permission_error"constant`

              - `PERMISSION_ERROR("permission_error")`

          - `class BetaNotFoundError:`

            - `message: String`

            - `type: JsonValue; "not_found_error"constant`

              - `NOT_FOUND_ERROR("not_found_error")`

          - `class BetaRateLimitError:`

            - `message: String`

            - `type: JsonValue; "rate_limit_error"constant`

              - `RATE_LIMIT_ERROR("rate_limit_error")`

          - `class BetaGatewayTimeoutError:`

            - `message: String`

            - `type: JsonValue; "timeout_error"constant`

              - `TIMEOUT_ERROR("timeout_error")`

          - `class BetaApiError:`

            - `message: String`

            - `type: JsonValue; "api_error"constant`

              - `API_ERROR("api_error")`

          - `class BetaOverloadedError:`

            - `message: String`

            - `type: JsonValue; "overloaded_error"constant`

              - `OVERLOADED_ERROR("overloaded_error")`

        - `requestId: Optional<String>`

        - `type: JsonValue; "error"constant`

          - `ERROR("error")`

      - `type: JsonValue; "errored"constant`

        - `ERRORED("errored")`

    - `class BetaMessageBatchCanceledResult:`

      - `type: JsonValue; "canceled"constant`

        - `CANCELED("canceled")`

    - `class BetaMessageBatchExpiredResult:`

      - `type: JsonValue; "expired"constant`

        - `EXPIRED("expired")`

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.core.http.StreamResponse
import com.anthropic.models.beta.messages.batches.BatchResultsParams
import com.anthropic.models.beta.messages.batches.BetaMessageBatchIndividualResponse

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val betaMessageBatchIndividualResponse: StreamResponse<BetaMessageBatchIndividualResponse> = client.beta().messages().batches().resultsStreaming("message_batch_id")
}
```

## Domain Types

### Beta Deleted Message Batch

- `class BetaDeletedMessageBatch:`

  - `id: String`

    ID of the Message Batch.

  - `type: JsonValue; "message_batch_deleted"constant`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `MESSAGE_BATCH_DELETED("message_batch_deleted")`

### Beta Message Batch

- `class BetaMessageBatch:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archivedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancelInitiatedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `createdAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `endedAt: Optional<LocalDateTime>`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expiresAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processingStatus: ProcessingStatus`

    Processing status of the Message Batch.

    - `IN_PROGRESS("in_progress")`

    - `CANCELING("canceling")`

    - `ENDED("ended")`

  - `requestCounts: BetaMessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: Long`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: Long`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: Long`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: Long`

      Number of requests in the Message Batch that are processing.

    - `succeeded: Long`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `resultsUrl: Optional<String>`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: JsonValue; "message_batch"constant`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `MESSAGE_BATCH("message_batch")`

### Beta Message Batch Canceled Result

- `class BetaMessageBatchCanceledResult:`

  - `type: JsonValue; "canceled"constant`

    - `CANCELED("canceled")`

### Beta Message Batch Errored Result

- `class BetaMessageBatchErroredResult:`

  - `error: BetaErrorResponse`

    - `error: BetaError`

      - `class BetaInvalidRequestError:`

        - `message: String`

        - `type: JsonValue; "invalid_request_error"constant`

          - `INVALID_REQUEST_ERROR("invalid_request_error")`

      - `class BetaAuthenticationError:`

        - `message: String`

        - `type: JsonValue; "authentication_error"constant`

          - `AUTHENTICATION_ERROR("authentication_error")`

      - `class BetaBillingError:`

        - `message: String`

        - `type: JsonValue; "billing_error"constant`

          - `BILLING_ERROR("billing_error")`

      - `class BetaPermissionError:`

        - `message: String`

        - `type: JsonValue; "permission_error"constant`

          - `PERMISSION_ERROR("permission_error")`

      - `class BetaNotFoundError:`

        - `message: String`

        - `type: JsonValue; "not_found_error"constant`

          - `NOT_FOUND_ERROR("not_found_error")`

      - `class BetaRateLimitError:`

        - `message: String`

        - `type: JsonValue; "rate_limit_error"constant`

          - `RATE_LIMIT_ERROR("rate_limit_error")`

      - `class BetaGatewayTimeoutError:`

        - `message: String`

        - `type: JsonValue; "timeout_error"constant`

          - `TIMEOUT_ERROR("timeout_error")`

      - `class BetaApiError:`

        - `message: String`

        - `type: JsonValue; "api_error"constant`

          - `API_ERROR("api_error")`

      - `class BetaOverloadedError:`

        - `message: String`

        - `type: JsonValue; "overloaded_error"constant`

          - `OVERLOADED_ERROR("overloaded_error")`

    - `requestId: Optional<String>`

    - `type: JsonValue; "error"constant`

      - `ERROR("error")`

  - `type: JsonValue; "errored"constant`

    - `ERRORED("errored")`

### Beta Message Batch Expired Result

- `class BetaMessageBatchExpiredResult:`

  - `type: JsonValue; "expired"constant`

    - `EXPIRED("expired")`

### Beta Message Batch Individual Response

- `class BetaMessageBatchIndividualResponse:`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `customId: String`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: BetaMessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `class BetaMessageBatchSucceededResult:`

      - `message: BetaMessage`

        - `id: String`

          Unique object identifier.

          The format and length of IDs may change over time.

        - `container: Optional<BetaContainer>`

          Information about the container used in the request (for the code execution tool)

          - `id: String`

            Identifier for the container used in this request

          - `expiresAt: LocalDateTime`

            The time at which the container will expire.

          - `skills: Optional<List<BetaSkill>>`

            Skills loaded in the container

            - `skillId: String`

              Skill ID

            - `type: Type`

              Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

              - `ANTHROPIC("anthropic")`

              - `CUSTOM("custom")`

            - `version: String`

              Skill version or 'latest' for most recent version

        - `content: List<BetaContentBlock>`

          Content generated by the model.

          This is an array of content blocks, each of which has a `type` that determines its shape.

          Example:

          ```json
          [{"type": "text", "text": "Hi, I'm Claude."}]
          ```

          If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

          For example, if the input `messages` were:

          ```json
          [
            {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
            {"role": "assistant", "content": "The best answer is ("}
          ]
          ```

          Then the response `content` might be:

          ```json
          [{"type": "text", "text": "B)"}]
          ```

          - `class BetaTextBlock:`

            - `citations: Optional<List<BetaTextCitation>>`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class BetaCitationCharLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endCharIndex: Long`

                - `fileId: Optional<String>`

                - `startCharIndex: Long`

                - `type: JsonValue; "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class BetaCitationPageLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endPageNumber: Long`

                - `fileId: Optional<String>`

                - `startPageNumber: Long`

                - `type: JsonValue; "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class BetaCitationContentBlockLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endBlockIndex: Long`

                - `fileId: Optional<String>`

                - `startBlockIndex: Long`

                - `type: JsonValue; "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class BetaCitationsWebSearchResultLocation:`

                - `citedText: String`

                - `encryptedIndex: String`

                - `title: Optional<String>`

                - `type: JsonValue; "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `url: String`

              - `class BetaCitationSearchResultLocation:`

                - `citedText: String`

                - `endBlockIndex: Long`

                - `searchResultIndex: Long`

                - `source: String`

                - `startBlockIndex: Long`

                - `title: Optional<String>`

                - `type: JsonValue; "search_result_location"constant`

                  - `SEARCH_RESULT_LOCATION("search_result_location")`

            - `text: String`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

          - `class BetaThinkingBlock:`

            - `signature: String`

            - `thinking: String`

            - `type: JsonValue; "thinking"constant`

              - `THINKING("thinking")`

          - `class BetaRedactedThinkingBlock:`

            - `data: String`

            - `type: JsonValue; "redacted_thinking"constant`

              - `REDACTED_THINKING("redacted_thinking")`

          - `class BetaToolUseBlock:`

            - `id: String`

            - `input: Input`

            - `name: String`

            - `type: JsonValue; "tool_use"constant`

              - `TOOL_USE("tool_use")`

            - `caller: Optional<Caller>`

              Tool invocation directly from the model.

              - `class BetaDirectCaller:`

                Tool invocation directly from the model.

                - `type: JsonValue; "direct"constant`

                  - `DIRECT("direct")`

              - `class BetaServerToolCaller:`

                Tool invocation generated by a server-side tool.

                - `toolId: String`

                - `type: JsonValue; "code_execution_20250825"constant`

                  - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `class BetaServerToolUseBlock:`

            - `id: String`

            - `caller: Caller`

              Tool invocation directly from the model.

              - `class BetaDirectCaller:`

                Tool invocation directly from the model.

                - `type: JsonValue; "direct"constant`

                  - `DIRECT("direct")`

              - `class BetaServerToolCaller:`

                Tool invocation generated by a server-side tool.

                - `toolId: String`

                - `type: JsonValue; "code_execution_20250825"constant`

                  - `CODE_EXECUTION_20250825("code_execution_20250825")`

            - `input: Input`

            - `name: Name`

              - `WEB_SEARCH("web_search")`

              - `WEB_FETCH("web_fetch")`

              - `CODE_EXECUTION("code_execution")`

              - `BASH_CODE_EXECUTION("bash_code_execution")`

              - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

              - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

              - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

            - `type: JsonValue; "server_tool_use"constant`

              - `SERVER_TOOL_USE("server_tool_use")`

          - `class BetaWebSearchToolResultBlock:`

            - `content: BetaWebSearchToolResultBlockContent`

              - `class BetaWebSearchToolResultError:`

                - `errorCode: BetaWebSearchToolResultErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `UNAVAILABLE("unavailable")`

                  - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `QUERY_TOO_LONG("query_too_long")`

                - `type: JsonValue; "web_search_tool_result_error"constant`

                  - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

              - `List<BetaWebSearchResultBlock>`

                - `encryptedContent: String`

                - `pageAge: Optional<String>`

                - `title: String`

                - `type: JsonValue; "web_search_result"constant`

                  - `WEB_SEARCH_RESULT("web_search_result")`

                - `url: String`

            - `toolUseId: String`

            - `type: JsonValue; "web_search_tool_result"constant`

              - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

          - `class BetaWebFetchToolResultBlock:`

            - `content: Content`

              - `class BetaWebFetchToolResultErrorBlock:`

                - `errorCode: BetaWebFetchToolResultErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `URL_TOO_LONG("url_too_long")`

                  - `URL_NOT_ALLOWED("url_not_allowed")`

                  - `URL_NOT_ACCESSIBLE("url_not_accessible")`

                  - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                  - `UNAVAILABLE("unavailable")`

                - `type: JsonValue; "web_fetch_tool_result_error"constant`

                  - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

              - `class BetaWebFetchBlock:`

                - `content: BetaDocumentBlock`

                  - `citations: Optional<BetaCitationConfig>`

                    Citation configuration for the document

                    - `enabled: Boolean`

                  - `source: Source`

                    - `class BetaBase64PdfSource:`

                      - `data: String`

                      - `mediaType: JsonValue; "application/pdf"constant`

                        - `APPLICATION_PDF("application/pdf")`

                      - `type: JsonValue; "base64"constant`

                        - `BASE64("base64")`

                    - `class BetaPlainTextSource:`

                      - `data: String`

                      - `mediaType: JsonValue; "text/plain"constant`

                        - `TEXT_PLAIN("text/plain")`

                      - `type: JsonValue; "text"constant`

                        - `TEXT("text")`

                  - `title: Optional<String>`

                    The title of the document

                  - `type: JsonValue; "document"constant`

                    - `DOCUMENT("document")`

                - `retrievedAt: Optional<String>`

                  ISO 8601 timestamp when the content was retrieved

                - `type: JsonValue; "web_fetch_result"constant`

                  - `WEB_FETCH_RESULT("web_fetch_result")`

                - `url: String`

                  Fetched content URL

            - `toolUseId: String`

            - `type: JsonValue; "web_fetch_tool_result"constant`

              - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

          - `class BetaCodeExecutionToolResultBlock:`

            - `content: BetaCodeExecutionToolResultBlockContent`

              - `class BetaCodeExecutionToolResultError:`

                - `errorCode: BetaCodeExecutionToolResultErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `UNAVAILABLE("unavailable")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `type: JsonValue; "code_execution_tool_result_error"constant`

                  - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

              - `class BetaCodeExecutionResultBlock:`

                - `content: List<BetaCodeExecutionOutputBlock>`

                  - `fileId: String`

                  - `type: JsonValue; "code_execution_output"constant`

                    - `CODE_EXECUTION_OUTPUT("code_execution_output")`

                - `returnCode: Long`

                - `stderr: String`

                - `stdout: String`

                - `type: JsonValue; "code_execution_result"constant`

                  - `CODE_EXECUTION_RESULT("code_execution_result")`

            - `toolUseId: String`

            - `type: JsonValue; "code_execution_tool_result"constant`

              - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

          - `class BetaBashCodeExecutionToolResultBlock:`

            - `content: Content`

              - `class BetaBashCodeExecutionToolResultError:`

                - `errorCode: ErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `UNAVAILABLE("unavailable")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                  - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

                - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

                  - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

              - `class BetaBashCodeExecutionResultBlock:`

                - `content: List<BetaBashCodeExecutionOutputBlock>`

                  - `fileId: String`

                  - `type: JsonValue; "bash_code_execution_output"constant`

                    - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

                - `returnCode: Long`

                - `stderr: String`

                - `stdout: String`

                - `type: JsonValue; "bash_code_execution_result"constant`

                  - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

            - `toolUseId: String`

            - `type: JsonValue; "bash_code_execution_tool_result"constant`

              - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

          - `class BetaTextEditorCodeExecutionToolResultBlock:`

            - `content: Content`

              - `class BetaTextEditorCodeExecutionToolResultError:`

                - `errorCode: ErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `UNAVAILABLE("unavailable")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                  - `FILE_NOT_FOUND("file_not_found")`

                - `errorMessage: Optional<String>`

                - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

                  - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

              - `class BetaTextEditorCodeExecutionViewResultBlock:`

                - `content: String`

                - `fileType: FileType`

                  - `TEXT("text")`

                  - `IMAGE("image")`

                  - `PDF("pdf")`

                - `numLines: Optional<Long>`

                - `startLine: Optional<Long>`

                - `totalLines: Optional<Long>`

                - `type: JsonValue; "text_editor_code_execution_view_result"constant`

                  - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

              - `class BetaTextEditorCodeExecutionCreateResultBlock:`

                - `isFileUpdate: Boolean`

                - `type: JsonValue; "text_editor_code_execution_create_result"constant`

                  - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

              - `class BetaTextEditorCodeExecutionStrReplaceResultBlock:`

                - `lines: Optional<List<String>>`

                - `newLines: Optional<Long>`

                - `newStart: Optional<Long>`

                - `oldLines: Optional<Long>`

                - `oldStart: Optional<Long>`

                - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

                  - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

            - `toolUseId: String`

            - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

          - `class BetaToolSearchToolResultBlock:`

            - `content: Content`

              - `class BetaToolSearchToolResultError:`

                - `errorCode: ErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `UNAVAILABLE("unavailable")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `errorMessage: Optional<String>`

                - `type: JsonValue; "tool_search_tool_result_error"constant`

                  - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

              - `class BetaToolSearchToolSearchResultBlock:`

                - `toolReferences: List<BetaToolReferenceBlock>`

                  - `toolName: String`

                  - `type: JsonValue; "tool_reference"constant`

                    - `TOOL_REFERENCE("tool_reference")`

                - `type: JsonValue; "tool_search_tool_search_result"constant`

                  - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

            - `toolUseId: String`

            - `type: JsonValue; "tool_search_tool_result"constant`

              - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

          - `class BetaMcpToolUseBlock:`

            - `id: String`

            - `input: Input`

            - `name: String`

              The name of the MCP tool

            - `serverName: String`

              The name of the MCP server

            - `type: JsonValue; "mcp_tool_use"constant`

              - `MCP_TOOL_USE("mcp_tool_use")`

          - `class BetaMcpToolResultBlock:`

            - `content: Content`

              - `String`

              - `List<BetaTextBlock>`

                - `citations: Optional<List<BetaTextCitation>>`

                  Citations supporting the text block.

                  The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

                  - `class BetaCitationCharLocation:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endCharIndex: Long`

                    - `fileId: Optional<String>`

                    - `startCharIndex: Long`

                    - `type: JsonValue; "char_location"constant`

                      - `CHAR_LOCATION("char_location")`

                  - `class BetaCitationPageLocation:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endPageNumber: Long`

                    - `fileId: Optional<String>`

                    - `startPageNumber: Long`

                    - `type: JsonValue; "page_location"constant`

                      - `PAGE_LOCATION("page_location")`

                  - `class BetaCitationContentBlockLocation:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endBlockIndex: Long`

                    - `fileId: Optional<String>`

                    - `startBlockIndex: Long`

                    - `type: JsonValue; "content_block_location"constant`

                      - `CONTENT_BLOCK_LOCATION("content_block_location")`

                  - `class BetaCitationsWebSearchResultLocation:`

                    - `citedText: String`

                    - `encryptedIndex: String`

                    - `title: Optional<String>`

                    - `type: JsonValue; "web_search_result_location"constant`

                      - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                    - `url: String`

                  - `class BetaCitationSearchResultLocation:`

                    - `citedText: String`

                    - `endBlockIndex: Long`

                    - `searchResultIndex: Long`

                    - `source: String`

                    - `startBlockIndex: Long`

                    - `title: Optional<String>`

                    - `type: JsonValue; "search_result_location"constant`

                      - `SEARCH_RESULT_LOCATION("search_result_location")`

                - `text: String`

                - `type: JsonValue; "text"constant`

                  - `TEXT("text")`

            - `isError: Boolean`

            - `toolUseId: String`

            - `type: JsonValue; "mcp_tool_result"constant`

              - `MCP_TOOL_RESULT("mcp_tool_result")`

          - `class BetaContainerUploadBlock:`

            Response model for a file uploaded to the container.

            - `fileId: String`

            - `type: JsonValue; "container_upload"constant`

              - `CONTAINER_UPLOAD("container_upload")`

        - `contextManagement: Optional<BetaContextManagementResponse>`

          Context management response.

          Information about context management strategies applied during the request.

          - `appliedEdits: List<AppliedEdit>`

            List of context management edits that were applied.

            - `class BetaClearToolUses20250919EditResponse:`

              - `clearedInputTokens: Long`

                Number of input tokens cleared by this edit.

              - `clearedToolUses: Long`

                Number of tool uses that were cleared.

              - `type: JsonValue; "clear_tool_uses_20250919"constant`

                The type of context management edit applied.

                - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

            - `class BetaClearThinking20251015EditResponse:`

              - `clearedInputTokens: Long`

                Number of input tokens cleared by this edit.

              - `clearedThinkingTurns: Long`

                Number of thinking turns that were cleared.

              - `type: JsonValue; "clear_thinking_20251015"constant`

                The type of context management edit applied.

                - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

        - `model: Model`

          The model that will complete your prompt.

          See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

          - `CLAUDE_OPUS_4_5_20251101("claude-opus-4-5-20251101")`

            Premium model combining maximum intelligence with practical performance

          - `CLAUDE_OPUS_4_5("claude-opus-4-5")`

            Premium model combining maximum intelligence with practical performance

          - `CLAUDE_3_7_SONNET_LATEST("claude-3-7-sonnet-latest")`

            High-performance model with early extended thinking

          - `CLAUDE_3_7_SONNET_20250219("claude-3-7-sonnet-20250219")`

            High-performance model with early extended thinking

          - `CLAUDE_3_5_HAIKU_LATEST("claude-3-5-haiku-latest")`

            Fastest and most compact model for near-instant responsiveness

          - `CLAUDE_3_5_HAIKU_20241022("claude-3-5-haiku-20241022")`

            Our fastest model

          - `CLAUDE_HAIKU_4_5("claude-haiku-4-5")`

            Hybrid model, capable of near-instant responses and extended thinking

          - `CLAUDE_HAIKU_4_5_20251001("claude-haiku-4-5-20251001")`

            Hybrid model, capable of near-instant responses and extended thinking

          - `CLAUDE_SONNET_4_20250514("claude-sonnet-4-20250514")`

            High-performance model with extended thinking

          - `CLAUDE_SONNET_4_0("claude-sonnet-4-0")`

            High-performance model with extended thinking

          - `CLAUDE_4_SONNET_20250514("claude-4-sonnet-20250514")`

            High-performance model with extended thinking

          - `CLAUDE_SONNET_4_5("claude-sonnet-4-5")`

            Our best model for real-world agents and coding

          - `CLAUDE_SONNET_4_5_20250929("claude-sonnet-4-5-20250929")`

            Our best model for real-world agents and coding

          - `CLAUDE_OPUS_4_0("claude-opus-4-0")`

            Our most capable model

          - `CLAUDE_OPUS_4_20250514("claude-opus-4-20250514")`

            Our most capable model

          - `CLAUDE_4_OPUS_20250514("claude-4-opus-20250514")`

            Our most capable model

          - `CLAUDE_OPUS_4_1_20250805("claude-opus-4-1-20250805")`

            Our most capable model

          - `CLAUDE_3_OPUS_LATEST("claude-3-opus-latest")`

            Excels at writing and complex tasks

          - `CLAUDE_3_OPUS_20240229("claude-3-opus-20240229")`

            Excels at writing and complex tasks

          - `CLAUDE_3_HAIKU_20240307("claude-3-haiku-20240307")`

            Our previous most fast and cost-effective

        - `role: JsonValue; "assistant"constant`

          Conversational role of the generated message.

          This will always be `"assistant"`.

          - `ASSISTANT("assistant")`

        - `stopReason: Optional<BetaStopReason>`

          The reason that we stopped.

          This may be one the following values:

          * `"end_turn"`: the model reached a natural stopping point
          * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
          * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
          * `"tool_use"`: the model invoked one or more tools
          * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
          * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

          In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

          - `END_TURN("end_turn")`

          - `MAX_TOKENS("max_tokens")`

          - `STOP_SEQUENCE("stop_sequence")`

          - `TOOL_USE("tool_use")`

          - `PAUSE_TURN("pause_turn")`

          - `REFUSAL("refusal")`

          - `MODEL_CONTEXT_WINDOW_EXCEEDED("model_context_window_exceeded")`

        - `stopSequence: Optional<String>`

          Which custom stop sequence was generated, if any.

          This value will be a non-null string if one of your custom stop sequences was generated.

        - `type: JsonValue; "message"constant`

          Object type.

          For Messages, this is always `"message"`.

          - `MESSAGE("message")`

        - `usage: BetaUsage`

          Billing and rate-limit usage.

          Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

          Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

          For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

          Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

          - `cacheCreation: Optional<BetaCacheCreation>`

            Breakdown of cached tokens by TTL

            - `ephemeral1hInputTokens: Long`

              The number of input tokens used to create the 1 hour cache entry.

            - `ephemeral5mInputTokens: Long`

              The number of input tokens used to create the 5 minute cache entry.

          - `cacheCreationInputTokens: Optional<Long>`

            The number of input tokens used to create the cache entry.

          - `cacheReadInputTokens: Optional<Long>`

            The number of input tokens read from the cache.

          - `inputTokens: Long`

            The number of input tokens which were used.

          - `outputTokens: Long`

            The number of output tokens which were used.

          - `serverToolUse: Optional<BetaServerToolUsage>`

            The number of server tool requests.

            - `webFetchRequests: Long`

              The number of web fetch tool requests.

            - `webSearchRequests: Long`

              The number of web search tool requests.

          - `serviceTier: Optional<ServiceTier>`

            If the request used the priority, standard, or batch tier.

            - `STANDARD("standard")`

            - `PRIORITY("priority")`

            - `BATCH("batch")`

      - `type: JsonValue; "succeeded"constant`

        - `SUCCEEDED("succeeded")`

    - `class BetaMessageBatchErroredResult:`

      - `error: BetaErrorResponse`

        - `error: BetaError`

          - `class BetaInvalidRequestError:`

            - `message: String`

            - `type: JsonValue; "invalid_request_error"constant`

              - `INVALID_REQUEST_ERROR("invalid_request_error")`

          - `class BetaAuthenticationError:`

            - `message: String`

            - `type: JsonValue; "authentication_error"constant`

              - `AUTHENTICATION_ERROR("authentication_error")`

          - `class BetaBillingError:`

            - `message: String`

            - `type: JsonValue; "billing_error"constant`

              - `BILLING_ERROR("billing_error")`

          - `class BetaPermissionError:`

            - `message: String`

            - `type: JsonValue; "permission_error"constant`

              - `PERMISSION_ERROR("permission_error")`

          - `class BetaNotFoundError:`

            - `message: String`

            - `type: JsonValue; "not_found_error"constant`

              - `NOT_FOUND_ERROR("not_found_error")`

          - `class BetaRateLimitError:`

            - `message: String`

            - `type: JsonValue; "rate_limit_error"constant`

              - `RATE_LIMIT_ERROR("rate_limit_error")`

          - `class BetaGatewayTimeoutError:`

            - `message: String`

            - `type: JsonValue; "timeout_error"constant`

              - `TIMEOUT_ERROR("timeout_error")`

          - `class BetaApiError:`

            - `message: String`

            - `type: JsonValue; "api_error"constant`

              - `API_ERROR("api_error")`

          - `class BetaOverloadedError:`

            - `message: String`

            - `type: JsonValue; "overloaded_error"constant`

              - `OVERLOADED_ERROR("overloaded_error")`

        - `requestId: Optional<String>`

        - `type: JsonValue; "error"constant`

          - `ERROR("error")`

      - `type: JsonValue; "errored"constant`

        - `ERRORED("errored")`

    - `class BetaMessageBatchCanceledResult:`

      - `type: JsonValue; "canceled"constant`

        - `CANCELED("canceled")`

    - `class BetaMessageBatchExpiredResult:`

      - `type: JsonValue; "expired"constant`

        - `EXPIRED("expired")`

### Beta Message Batch Request Counts

- `class BetaMessageBatchRequestCounts:`

  - `canceled: Long`

    Number of requests in the Message Batch that have been canceled.

    This is zero until processing of the entire Message Batch has ended.

  - `errored: Long`

    Number of requests in the Message Batch that encountered an error.

    This is zero until processing of the entire Message Batch has ended.

  - `expired: Long`

    Number of requests in the Message Batch that have expired.

    This is zero until processing of the entire Message Batch has ended.

  - `processing: Long`

    Number of requests in the Message Batch that are processing.

  - `succeeded: Long`

    Number of requests in the Message Batch that have completed successfully.

    This is zero until processing of the entire Message Batch has ended.

### Beta Message Batch Result

- `class BetaMessageBatchResult: A class that can be one of several variants.union`

  Processing result for this request.

  Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

  - `class BetaMessageBatchSucceededResult:`

    - `message: BetaMessage`

      - `id: String`

        Unique object identifier.

        The format and length of IDs may change over time.

      - `container: Optional<BetaContainer>`

        Information about the container used in the request (for the code execution tool)

        - `id: String`

          Identifier for the container used in this request

        - `expiresAt: LocalDateTime`

          The time at which the container will expire.

        - `skills: Optional<List<BetaSkill>>`

          Skills loaded in the container

          - `skillId: String`

            Skill ID

          - `type: Type`

            Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

            - `ANTHROPIC("anthropic")`

            - `CUSTOM("custom")`

          - `version: String`

            Skill version or 'latest' for most recent version

      - `content: List<BetaContentBlock>`

        Content generated by the model.

        This is an array of content blocks, each of which has a `type` that determines its shape.

        Example:

        ```json
        [{"type": "text", "text": "Hi, I'm Claude."}]
        ```

        If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

        For example, if the input `messages` were:

        ```json
        [
          {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
          {"role": "assistant", "content": "The best answer is ("}
        ]
        ```

        Then the response `content` might be:

        ```json
        [{"type": "text", "text": "B)"}]
        ```

        - `class BetaTextBlock:`

          - `citations: Optional<List<BetaTextCitation>>`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `class BetaCitationCharLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `fileId: Optional<String>`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class BetaCitationPageLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `fileId: Optional<String>`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class BetaCitationContentBlockLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `fileId: Optional<String>`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class BetaCitationsWebSearchResultLocation:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class BetaCitationSearchResultLocation:`

              - `citedText: String`

              - `endBlockIndex: Long`

              - `searchResultIndex: Long`

              - `source: String`

              - `startBlockIndex: Long`

              - `title: Optional<String>`

              - `type: JsonValue; "search_result_location"constant`

                - `SEARCH_RESULT_LOCATION("search_result_location")`

          - `text: String`

          - `type: JsonValue; "text"constant`

            - `TEXT("text")`

        - `class BetaThinkingBlock:`

          - `signature: String`

          - `thinking: String`

          - `type: JsonValue; "thinking"constant`

            - `THINKING("thinking")`

        - `class BetaRedactedThinkingBlock:`

          - `data: String`

          - `type: JsonValue; "redacted_thinking"constant`

            - `REDACTED_THINKING("redacted_thinking")`

        - `class BetaToolUseBlock:`

          - `id: String`

          - `input: Input`

          - `name: String`

          - `type: JsonValue; "tool_use"constant`

            - `TOOL_USE("tool_use")`

          - `caller: Optional<Caller>`

            Tool invocation directly from the model.

            - `class BetaDirectCaller:`

              Tool invocation directly from the model.

              - `type: JsonValue; "direct"constant`

                - `DIRECT("direct")`

            - `class BetaServerToolCaller:`

              Tool invocation generated by a server-side tool.

              - `toolId: String`

              - `type: JsonValue; "code_execution_20250825"constant`

                - `CODE_EXECUTION_20250825("code_execution_20250825")`

        - `class BetaServerToolUseBlock:`

          - `id: String`

          - `caller: Caller`

            Tool invocation directly from the model.

            - `class BetaDirectCaller:`

              Tool invocation directly from the model.

              - `type: JsonValue; "direct"constant`

                - `DIRECT("direct")`

            - `class BetaServerToolCaller:`

              Tool invocation generated by a server-side tool.

              - `toolId: String`

              - `type: JsonValue; "code_execution_20250825"constant`

                - `CODE_EXECUTION_20250825("code_execution_20250825")`

          - `input: Input`

          - `name: Name`

            - `WEB_SEARCH("web_search")`

            - `WEB_FETCH("web_fetch")`

            - `CODE_EXECUTION("code_execution")`

            - `BASH_CODE_EXECUTION("bash_code_execution")`

            - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

            - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

            - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

          - `type: JsonValue; "server_tool_use"constant`

            - `SERVER_TOOL_USE("server_tool_use")`

        - `class BetaWebSearchToolResultBlock:`

          - `content: BetaWebSearchToolResultBlockContent`

            - `class BetaWebSearchToolResultError:`

              - `errorCode: BetaWebSearchToolResultErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `QUERY_TOO_LONG("query_too_long")`

              - `type: JsonValue; "web_search_tool_result_error"constant`

                - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

            - `List<BetaWebSearchResultBlock>`

              - `encryptedContent: String`

              - `pageAge: Optional<String>`

              - `title: String`

              - `type: JsonValue; "web_search_result"constant`

                - `WEB_SEARCH_RESULT("web_search_result")`

              - `url: String`

          - `toolUseId: String`

          - `type: JsonValue; "web_search_tool_result"constant`

            - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

        - `class BetaWebFetchToolResultBlock:`

          - `content: Content`

            - `class BetaWebFetchToolResultErrorBlock:`

              - `errorCode: BetaWebFetchToolResultErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `URL_TOO_LONG("url_too_long")`

                - `URL_NOT_ALLOWED("url_not_allowed")`

                - `URL_NOT_ACCESSIBLE("url_not_accessible")`

                - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                - `UNAVAILABLE("unavailable")`

              - `type: JsonValue; "web_fetch_tool_result_error"constant`

                - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

            - `class BetaWebFetchBlock:`

              - `content: BetaDocumentBlock`

                - `citations: Optional<BetaCitationConfig>`

                  Citation configuration for the document

                  - `enabled: Boolean`

                - `source: Source`

                  - `class BetaBase64PdfSource:`

                    - `data: String`

                    - `mediaType: JsonValue; "application/pdf"constant`

                      - `APPLICATION_PDF("application/pdf")`

                    - `type: JsonValue; "base64"constant`

                      - `BASE64("base64")`

                  - `class BetaPlainTextSource:`

                    - `data: String`

                    - `mediaType: JsonValue; "text/plain"constant`

                      - `TEXT_PLAIN("text/plain")`

                    - `type: JsonValue; "text"constant`

                      - `TEXT("text")`

                - `title: Optional<String>`

                  The title of the document

                - `type: JsonValue; "document"constant`

                  - `DOCUMENT("document")`

              - `retrievedAt: Optional<String>`

                ISO 8601 timestamp when the content was retrieved

              - `type: JsonValue; "web_fetch_result"constant`

                - `WEB_FETCH_RESULT("web_fetch_result")`

              - `url: String`

                Fetched content URL

          - `toolUseId: String`

          - `type: JsonValue; "web_fetch_tool_result"constant`

            - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

        - `class BetaCodeExecutionToolResultBlock:`

          - `content: BetaCodeExecutionToolResultBlockContent`

            - `class BetaCodeExecutionToolResultError:`

              - `errorCode: BetaCodeExecutionToolResultErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `type: JsonValue; "code_execution_tool_result_error"constant`

                - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

            - `class BetaCodeExecutionResultBlock:`

              - `content: List<BetaCodeExecutionOutputBlock>`

                - `fileId: String`

                - `type: JsonValue; "code_execution_output"constant`

                  - `CODE_EXECUTION_OUTPUT("code_execution_output")`

              - `returnCode: Long`

              - `stderr: String`

              - `stdout: String`

              - `type: JsonValue; "code_execution_result"constant`

                - `CODE_EXECUTION_RESULT("code_execution_result")`

          - `toolUseId: String`

          - `type: JsonValue; "code_execution_tool_result"constant`

            - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

        - `class BetaBashCodeExecutionToolResultBlock:`

          - `content: Content`

            - `class BetaBashCodeExecutionToolResultError:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

              - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

                - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

            - `class BetaBashCodeExecutionResultBlock:`

              - `content: List<BetaBashCodeExecutionOutputBlock>`

                - `fileId: String`

                - `type: JsonValue; "bash_code_execution_output"constant`

                  - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

              - `returnCode: Long`

              - `stderr: String`

              - `stdout: String`

              - `type: JsonValue; "bash_code_execution_result"constant`

                - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

          - `toolUseId: String`

          - `type: JsonValue; "bash_code_execution_tool_result"constant`

            - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

        - `class BetaTextEditorCodeExecutionToolResultBlock:`

          - `content: Content`

            - `class BetaTextEditorCodeExecutionToolResultError:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `FILE_NOT_FOUND("file_not_found")`

              - `errorMessage: Optional<String>`

              - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

            - `class BetaTextEditorCodeExecutionViewResultBlock:`

              - `content: String`

              - `fileType: FileType`

                - `TEXT("text")`

                - `IMAGE("image")`

                - `PDF("pdf")`

              - `numLines: Optional<Long>`

              - `startLine: Optional<Long>`

              - `totalLines: Optional<Long>`

              - `type: JsonValue; "text_editor_code_execution_view_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

            - `class BetaTextEditorCodeExecutionCreateResultBlock:`

              - `isFileUpdate: Boolean`

              - `type: JsonValue; "text_editor_code_execution_create_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

            - `class BetaTextEditorCodeExecutionStrReplaceResultBlock:`

              - `lines: Optional<List<String>>`

              - `newLines: Optional<Long>`

              - `newStart: Optional<Long>`

              - `oldLines: Optional<Long>`

              - `oldStart: Optional<Long>`

              - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

          - `toolUseId: String`

          - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

        - `class BetaToolSearchToolResultBlock:`

          - `content: Content`

            - `class BetaToolSearchToolResultError:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `errorMessage: Optional<String>`

              - `type: JsonValue; "tool_search_tool_result_error"constant`

                - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

            - `class BetaToolSearchToolSearchResultBlock:`

              - `toolReferences: List<BetaToolReferenceBlock>`

                - `toolName: String`

                - `type: JsonValue; "tool_reference"constant`

                  - `TOOL_REFERENCE("tool_reference")`

              - `type: JsonValue; "tool_search_tool_search_result"constant`

                - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

          - `toolUseId: String`

          - `type: JsonValue; "tool_search_tool_result"constant`

            - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

        - `class BetaMcpToolUseBlock:`

          - `id: String`

          - `input: Input`

          - `name: String`

            The name of the MCP tool

          - `serverName: String`

            The name of the MCP server

          - `type: JsonValue; "mcp_tool_use"constant`

            - `MCP_TOOL_USE("mcp_tool_use")`

        - `class BetaMcpToolResultBlock:`

          - `content: Content`

            - `String`

            - `List<BetaTextBlock>`

              - `citations: Optional<List<BetaTextCitation>>`

                Citations supporting the text block.

                The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

                - `class BetaCitationCharLocation:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endCharIndex: Long`

                  - `fileId: Optional<String>`

                  - `startCharIndex: Long`

                  - `type: JsonValue; "char_location"constant`

                    - `CHAR_LOCATION("char_location")`

                - `class BetaCitationPageLocation:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endPageNumber: Long`

                  - `fileId: Optional<String>`

                  - `startPageNumber: Long`

                  - `type: JsonValue; "page_location"constant`

                    - `PAGE_LOCATION("page_location")`

                - `class BetaCitationContentBlockLocation:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endBlockIndex: Long`

                  - `fileId: Optional<String>`

                  - `startBlockIndex: Long`

                  - `type: JsonValue; "content_block_location"constant`

                    - `CONTENT_BLOCK_LOCATION("content_block_location")`

                - `class BetaCitationsWebSearchResultLocation:`

                  - `citedText: String`

                  - `encryptedIndex: String`

                  - `title: Optional<String>`

                  - `type: JsonValue; "web_search_result_location"constant`

                    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                  - `url: String`

                - `class BetaCitationSearchResultLocation:`

                  - `citedText: String`

                  - `endBlockIndex: Long`

                  - `searchResultIndex: Long`

                  - `source: String`

                  - `startBlockIndex: Long`

                  - `title: Optional<String>`

                  - `type: JsonValue; "search_result_location"constant`

                    - `SEARCH_RESULT_LOCATION("search_result_location")`

              - `text: String`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

          - `isError: Boolean`

          - `toolUseId: String`

          - `type: JsonValue; "mcp_tool_result"constant`

            - `MCP_TOOL_RESULT("mcp_tool_result")`

        - `class BetaContainerUploadBlock:`

          Response model for a file uploaded to the container.

          - `fileId: String`

          - `type: JsonValue; "container_upload"constant`

            - `CONTAINER_UPLOAD("container_upload")`

      - `contextManagement: Optional<BetaContextManagementResponse>`

        Context management response.

        Information about context management strategies applied during the request.

        - `appliedEdits: List<AppliedEdit>`

          List of context management edits that were applied.

          - `class BetaClearToolUses20250919EditResponse:`

            - `clearedInputTokens: Long`

              Number of input tokens cleared by this edit.

            - `clearedToolUses: Long`

              Number of tool uses that were cleared.

            - `type: JsonValue; "clear_tool_uses_20250919"constant`

              The type of context management edit applied.

              - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

          - `class BetaClearThinking20251015EditResponse:`

            - `clearedInputTokens: Long`

              Number of input tokens cleared by this edit.

            - `clearedThinkingTurns: Long`

              Number of thinking turns that were cleared.

            - `type: JsonValue; "clear_thinking_20251015"constant`

              The type of context management edit applied.

              - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

      - `model: Model`

        The model that will complete your prompt.

        See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

        - `CLAUDE_OPUS_4_5_20251101("claude-opus-4-5-20251101")`

          Premium model combining maximum intelligence with practical performance

        - `CLAUDE_OPUS_4_5("claude-opus-4-5")`

          Premium model combining maximum intelligence with practical performance

        - `CLAUDE_3_7_SONNET_LATEST("claude-3-7-sonnet-latest")`

          High-performance model with early extended thinking

        - `CLAUDE_3_7_SONNET_20250219("claude-3-7-sonnet-20250219")`

          High-performance model with early extended thinking

        - `CLAUDE_3_5_HAIKU_LATEST("claude-3-5-haiku-latest")`

          Fastest and most compact model for near-instant responsiveness

        - `CLAUDE_3_5_HAIKU_20241022("claude-3-5-haiku-20241022")`

          Our fastest model

        - `CLAUDE_HAIKU_4_5("claude-haiku-4-5")`

          Hybrid model, capable of near-instant responses and extended thinking

        - `CLAUDE_HAIKU_4_5_20251001("claude-haiku-4-5-20251001")`

          Hybrid model, capable of near-instant responses and extended thinking

        - `CLAUDE_SONNET_4_20250514("claude-sonnet-4-20250514")`

          High-performance model with extended thinking

        - `CLAUDE_SONNET_4_0("claude-sonnet-4-0")`

          High-performance model with extended thinking

        - `CLAUDE_4_SONNET_20250514("claude-4-sonnet-20250514")`

          High-performance model with extended thinking

        - `CLAUDE_SONNET_4_5("claude-sonnet-4-5")`

          Our best model for real-world agents and coding

        - `CLAUDE_SONNET_4_5_20250929("claude-sonnet-4-5-20250929")`

          Our best model for real-world agents and coding

        - `CLAUDE_OPUS_4_0("claude-opus-4-0")`

          Our most capable model

        - `CLAUDE_OPUS_4_20250514("claude-opus-4-20250514")`

          Our most capable model

        - `CLAUDE_4_OPUS_20250514("claude-4-opus-20250514")`

          Our most capable model

        - `CLAUDE_OPUS_4_1_20250805("claude-opus-4-1-20250805")`

          Our most capable model

        - `CLAUDE_3_OPUS_LATEST("claude-3-opus-latest")`

          Excels at writing and complex tasks

        - `CLAUDE_3_OPUS_20240229("claude-3-opus-20240229")`

          Excels at writing and complex tasks

        - `CLAUDE_3_HAIKU_20240307("claude-3-haiku-20240307")`

          Our previous most fast and cost-effective

      - `role: JsonValue; "assistant"constant`

        Conversational role of the generated message.

        This will always be `"assistant"`.

        - `ASSISTANT("assistant")`

      - `stopReason: Optional<BetaStopReason>`

        The reason that we stopped.

        This may be one the following values:

        * `"end_turn"`: the model reached a natural stopping point
        * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
        * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
        * `"tool_use"`: the model invoked one or more tools
        * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
        * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

        In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

        - `END_TURN("end_turn")`

        - `MAX_TOKENS("max_tokens")`

        - `STOP_SEQUENCE("stop_sequence")`

        - `TOOL_USE("tool_use")`

        - `PAUSE_TURN("pause_turn")`

        - `REFUSAL("refusal")`

        - `MODEL_CONTEXT_WINDOW_EXCEEDED("model_context_window_exceeded")`

      - `stopSequence: Optional<String>`

        Which custom stop sequence was generated, if any.

        This value will be a non-null string if one of your custom stop sequences was generated.

      - `type: JsonValue; "message"constant`

        Object type.

        For Messages, this is always `"message"`.

        - `MESSAGE("message")`

      - `usage: BetaUsage`

        Billing and rate-limit usage.

        Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

        Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

        For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

        Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

        - `cacheCreation: Optional<BetaCacheCreation>`

          Breakdown of cached tokens by TTL

          - `ephemeral1hInputTokens: Long`

            The number of input tokens used to create the 1 hour cache entry.

          - `ephemeral5mInputTokens: Long`

            The number of input tokens used to create the 5 minute cache entry.

        - `cacheCreationInputTokens: Optional<Long>`

          The number of input tokens used to create the cache entry.

        - `cacheReadInputTokens: Optional<Long>`

          The number of input tokens read from the cache.

        - `inputTokens: Long`

          The number of input tokens which were used.

        - `outputTokens: Long`

          The number of output tokens which were used.

        - `serverToolUse: Optional<BetaServerToolUsage>`

          The number of server tool requests.

          - `webFetchRequests: Long`

            The number of web fetch tool requests.

          - `webSearchRequests: Long`

            The number of web search tool requests.

        - `serviceTier: Optional<ServiceTier>`

          If the request used the priority, standard, or batch tier.

          - `STANDARD("standard")`

          - `PRIORITY("priority")`

          - `BATCH("batch")`

    - `type: JsonValue; "succeeded"constant`

      - `SUCCEEDED("succeeded")`

  - `class BetaMessageBatchErroredResult:`

    - `error: BetaErrorResponse`

      - `error: BetaError`

        - `class BetaInvalidRequestError:`

          - `message: String`

          - `type: JsonValue; "invalid_request_error"constant`

            - `INVALID_REQUEST_ERROR("invalid_request_error")`

        - `class BetaAuthenticationError:`

          - `message: String`

          - `type: JsonValue; "authentication_error"constant`

            - `AUTHENTICATION_ERROR("authentication_error")`

        - `class BetaBillingError:`

          - `message: String`

          - `type: JsonValue; "billing_error"constant`

            - `BILLING_ERROR("billing_error")`

        - `class BetaPermissionError:`

          - `message: String`

          - `type: JsonValue; "permission_error"constant`

            - `PERMISSION_ERROR("permission_error")`

        - `class BetaNotFoundError:`

          - `message: String`

          - `type: JsonValue; "not_found_error"constant`

            - `NOT_FOUND_ERROR("not_found_error")`

        - `class BetaRateLimitError:`

          - `message: String`

          - `type: JsonValue; "rate_limit_error"constant`

            - `RATE_LIMIT_ERROR("rate_limit_error")`

        - `class BetaGatewayTimeoutError:`

          - `message: String`

          - `type: JsonValue; "timeout_error"constant`

            - `TIMEOUT_ERROR("timeout_error")`

        - `class BetaApiError:`

          - `message: String`

          - `type: JsonValue; "api_error"constant`

            - `API_ERROR("api_error")`

        - `class BetaOverloadedError:`

          - `message: String`

          - `type: JsonValue; "overloaded_error"constant`

            - `OVERLOADED_ERROR("overloaded_error")`

      - `requestId: Optional<String>`

      - `type: JsonValue; "error"constant`

        - `ERROR("error")`

    - `type: JsonValue; "errored"constant`

      - `ERRORED("errored")`

  - `class BetaMessageBatchCanceledResult:`

    - `type: JsonValue; "canceled"constant`

      - `CANCELED("canceled")`

  - `class BetaMessageBatchExpiredResult:`

    - `type: JsonValue; "expired"constant`

      - `EXPIRED("expired")`

### Beta Message Batch Succeeded Result

- `class BetaMessageBatchSucceededResult:`

  - `message: BetaMessage`

    - `id: String`

      Unique object identifier.

      The format and length of IDs may change over time.

    - `container: Optional<BetaContainer>`

      Information about the container used in the request (for the code execution tool)

      - `id: String`

        Identifier for the container used in this request

      - `expiresAt: LocalDateTime`

        The time at which the container will expire.

      - `skills: Optional<List<BetaSkill>>`

        Skills loaded in the container

        - `skillId: String`

          Skill ID

        - `type: Type`

          Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

          - `ANTHROPIC("anthropic")`

          - `CUSTOM("custom")`

        - `version: String`

          Skill version or 'latest' for most recent version

    - `content: List<BetaContentBlock>`

      Content generated by the model.

      This is an array of content blocks, each of which has a `type` that determines its shape.

      Example:

      ```json
      [{"type": "text", "text": "Hi, I'm Claude."}]
      ```

      If the request input `messages` ended with an `assistant` turn, then the response `content` will continue directly from that last turn. You can use this to constrain the model's output.

      For example, if the input `messages` were:

      ```json
      [
        {"role": "user", "content": "What's the Greek name for Sun? (A) Sol (B) Helios (C) Sun"},
        {"role": "assistant", "content": "The best answer is ("}
      ]
      ```

      Then the response `content` might be:

      ```json
      [{"type": "text", "text": "B)"}]
      ```

      - `class BetaTextBlock:`

        - `citations: Optional<List<BetaTextCitation>>`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `class BetaCitationCharLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endCharIndex: Long`

            - `fileId: Optional<String>`

            - `startCharIndex: Long`

            - `type: JsonValue; "char_location"constant`

              - `CHAR_LOCATION("char_location")`

          - `class BetaCitationPageLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endPageNumber: Long`

            - `fileId: Optional<String>`

            - `startPageNumber: Long`

            - `type: JsonValue; "page_location"constant`

              - `PAGE_LOCATION("page_location")`

          - `class BetaCitationContentBlockLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endBlockIndex: Long`

            - `fileId: Optional<String>`

            - `startBlockIndex: Long`

            - `type: JsonValue; "content_block_location"constant`

              - `CONTENT_BLOCK_LOCATION("content_block_location")`

          - `class BetaCitationsWebSearchResultLocation:`

            - `citedText: String`

            - `encryptedIndex: String`

            - `title: Optional<String>`

            - `type: JsonValue; "web_search_result_location"constant`

              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

            - `url: String`

          - `class BetaCitationSearchResultLocation:`

            - `citedText: String`

            - `endBlockIndex: Long`

            - `searchResultIndex: Long`

            - `source: String`

            - `startBlockIndex: Long`

            - `title: Optional<String>`

            - `type: JsonValue; "search_result_location"constant`

              - `SEARCH_RESULT_LOCATION("search_result_location")`

        - `text: String`

        - `type: JsonValue; "text"constant`

          - `TEXT("text")`

      - `class BetaThinkingBlock:`

        - `signature: String`

        - `thinking: String`

        - `type: JsonValue; "thinking"constant`

          - `THINKING("thinking")`

      - `class BetaRedactedThinkingBlock:`

        - `data: String`

        - `type: JsonValue; "redacted_thinking"constant`

          - `REDACTED_THINKING("redacted_thinking")`

      - `class BetaToolUseBlock:`

        - `id: String`

        - `input: Input`

        - `name: String`

        - `type: JsonValue; "tool_use"constant`

          - `TOOL_USE("tool_use")`

        - `caller: Optional<Caller>`

          Tool invocation directly from the model.

          - `class BetaDirectCaller:`

            Tool invocation directly from the model.

            - `type: JsonValue; "direct"constant`

              - `DIRECT("direct")`

          - `class BetaServerToolCaller:`

            Tool invocation generated by a server-side tool.

            - `toolId: String`

            - `type: JsonValue; "code_execution_20250825"constant`

              - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `class BetaServerToolUseBlock:`

        - `id: String`

        - `caller: Caller`

          Tool invocation directly from the model.

          - `class BetaDirectCaller:`

            Tool invocation directly from the model.

            - `type: JsonValue; "direct"constant`

              - `DIRECT("direct")`

          - `class BetaServerToolCaller:`

            Tool invocation generated by a server-side tool.

            - `toolId: String`

            - `type: JsonValue; "code_execution_20250825"constant`

              - `CODE_EXECUTION_20250825("code_execution_20250825")`

        - `input: Input`

        - `name: Name`

          - `WEB_SEARCH("web_search")`

          - `WEB_FETCH("web_fetch")`

          - `CODE_EXECUTION("code_execution")`

          - `BASH_CODE_EXECUTION("bash_code_execution")`

          - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

          - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

          - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

        - `type: JsonValue; "server_tool_use"constant`

          - `SERVER_TOOL_USE("server_tool_use")`

      - `class BetaWebSearchToolResultBlock:`

        - `content: BetaWebSearchToolResultBlockContent`

          - `class BetaWebSearchToolResultError:`

            - `errorCode: BetaWebSearchToolResultErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `MAX_USES_EXCEEDED("max_uses_exceeded")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `QUERY_TOO_LONG("query_too_long")`

            - `type: JsonValue; "web_search_tool_result_error"constant`

              - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

          - `List<BetaWebSearchResultBlock>`

            - `encryptedContent: String`

            - `pageAge: Optional<String>`

            - `title: String`

            - `type: JsonValue; "web_search_result"constant`

              - `WEB_SEARCH_RESULT("web_search_result")`

            - `url: String`

        - `toolUseId: String`

        - `type: JsonValue; "web_search_tool_result"constant`

          - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

      - `class BetaWebFetchToolResultBlock:`

        - `content: Content`

          - `class BetaWebFetchToolResultErrorBlock:`

            - `errorCode: BetaWebFetchToolResultErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `URL_TOO_LONG("url_too_long")`

              - `URL_NOT_ALLOWED("url_not_allowed")`

              - `URL_NOT_ACCESSIBLE("url_not_accessible")`

              - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `MAX_USES_EXCEEDED("max_uses_exceeded")`

              - `UNAVAILABLE("unavailable")`

            - `type: JsonValue; "web_fetch_tool_result_error"constant`

              - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

          - `class BetaWebFetchBlock:`

            - `content: BetaDocumentBlock`

              - `citations: Optional<BetaCitationConfig>`

                Citation configuration for the document

                - `enabled: Boolean`

              - `source: Source`

                - `class BetaBase64PdfSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "application/pdf"constant`

                    - `APPLICATION_PDF("application/pdf")`

                  - `type: JsonValue; "base64"constant`

                    - `BASE64("base64")`

                - `class BetaPlainTextSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "text/plain"constant`

                    - `TEXT_PLAIN("text/plain")`

                  - `type: JsonValue; "text"constant`

                    - `TEXT("text")`

              - `title: Optional<String>`

                The title of the document

              - `type: JsonValue; "document"constant`

                - `DOCUMENT("document")`

            - `retrievedAt: Optional<String>`

              ISO 8601 timestamp when the content was retrieved

            - `type: JsonValue; "web_fetch_result"constant`

              - `WEB_FETCH_RESULT("web_fetch_result")`

            - `url: String`

              Fetched content URL

        - `toolUseId: String`

        - `type: JsonValue; "web_fetch_tool_result"constant`

          - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

      - `class BetaCodeExecutionToolResultBlock:`

        - `content: BetaCodeExecutionToolResultBlockContent`

          - `class BetaCodeExecutionToolResultError:`

            - `errorCode: BetaCodeExecutionToolResultErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `type: JsonValue; "code_execution_tool_result_error"constant`

              - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

          - `class BetaCodeExecutionResultBlock:`

            - `content: List<BetaCodeExecutionOutputBlock>`

              - `fileId: String`

              - `type: JsonValue; "code_execution_output"constant`

                - `CODE_EXECUTION_OUTPUT("code_execution_output")`

            - `returnCode: Long`

            - `stderr: String`

            - `stdout: String`

            - `type: JsonValue; "code_execution_result"constant`

              - `CODE_EXECUTION_RESULT("code_execution_result")`

        - `toolUseId: String`

        - `type: JsonValue; "code_execution_tool_result"constant`

          - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

      - `class BetaBashCodeExecutionToolResultBlock:`

        - `content: Content`

          - `class BetaBashCodeExecutionToolResultError:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

            - `type: JsonValue; "bash_code_execution_tool_result_error"constant`

              - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

          - `class BetaBashCodeExecutionResultBlock:`

            - `content: List<BetaBashCodeExecutionOutputBlock>`

              - `fileId: String`

              - `type: JsonValue; "bash_code_execution_output"constant`

                - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

            - `returnCode: Long`

            - `stderr: String`

            - `stdout: String`

            - `type: JsonValue; "bash_code_execution_result"constant`

              - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

        - `toolUseId: String`

        - `type: JsonValue; "bash_code_execution_tool_result"constant`

          - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

      - `class BetaTextEditorCodeExecutionToolResultBlock:`

        - `content: Content`

          - `class BetaTextEditorCodeExecutionToolResultError:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `FILE_NOT_FOUND("file_not_found")`

            - `errorMessage: Optional<String>`

            - `type: JsonValue; "text_editor_code_execution_tool_result_error"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

          - `class BetaTextEditorCodeExecutionViewResultBlock:`

            - `content: String`

            - `fileType: FileType`

              - `TEXT("text")`

              - `IMAGE("image")`

              - `PDF("pdf")`

            - `numLines: Optional<Long>`

            - `startLine: Optional<Long>`

            - `totalLines: Optional<Long>`

            - `type: JsonValue; "text_editor_code_execution_view_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

          - `class BetaTextEditorCodeExecutionCreateResultBlock:`

            - `isFileUpdate: Boolean`

            - `type: JsonValue; "text_editor_code_execution_create_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

          - `class BetaTextEditorCodeExecutionStrReplaceResultBlock:`

            - `lines: Optional<List<String>>`

            - `newLines: Optional<Long>`

            - `newStart: Optional<Long>`

            - `oldLines: Optional<Long>`

            - `oldStart: Optional<Long>`

            - `type: JsonValue; "text_editor_code_execution_str_replace_result"constant`

              - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

        - `toolUseId: String`

        - `type: JsonValue; "text_editor_code_execution_tool_result"constant`

          - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

      - `class BetaToolSearchToolResultBlock:`

        - `content: Content`

          - `class BetaToolSearchToolResultError:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

            - `errorMessage: Optional<String>`

            - `type: JsonValue; "tool_search_tool_result_error"constant`

              - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

          - `class BetaToolSearchToolSearchResultBlock:`

            - `toolReferences: List<BetaToolReferenceBlock>`

              - `toolName: String`

              - `type: JsonValue; "tool_reference"constant`

                - `TOOL_REFERENCE("tool_reference")`

            - `type: JsonValue; "tool_search_tool_search_result"constant`

              - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

        - `toolUseId: String`

        - `type: JsonValue; "tool_search_tool_result"constant`

          - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

      - `class BetaMcpToolUseBlock:`

        - `id: String`

        - `input: Input`

        - `name: String`

          The name of the MCP tool

        - `serverName: String`

          The name of the MCP server

        - `type: JsonValue; "mcp_tool_use"constant`

          - `MCP_TOOL_USE("mcp_tool_use")`

      - `class BetaMcpToolResultBlock:`

        - `content: Content`

          - `String`

          - `List<BetaTextBlock>`

            - `citations: Optional<List<BetaTextCitation>>`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class BetaCitationCharLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endCharIndex: Long`

                - `fileId: Optional<String>`

                - `startCharIndex: Long`

                - `type: JsonValue; "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class BetaCitationPageLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endPageNumber: Long`

                - `fileId: Optional<String>`

                - `startPageNumber: Long`

                - `type: JsonValue; "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class BetaCitationContentBlockLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endBlockIndex: Long`

                - `fileId: Optional<String>`

                - `startBlockIndex: Long`

                - `type: JsonValue; "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class BetaCitationsWebSearchResultLocation:`

                - `citedText: String`

                - `encryptedIndex: String`

                - `title: Optional<String>`

                - `type: JsonValue; "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `url: String`

              - `class BetaCitationSearchResultLocation:`

                - `citedText: String`

                - `endBlockIndex: Long`

                - `searchResultIndex: Long`

                - `source: String`

                - `startBlockIndex: Long`

                - `title: Optional<String>`

                - `type: JsonValue; "search_result_location"constant`

                  - `SEARCH_RESULT_LOCATION("search_result_location")`

            - `text: String`

            - `type: JsonValue; "text"constant`

              - `TEXT("text")`

        - `isError: Boolean`

        - `toolUseId: String`

        - `type: JsonValue; "mcp_tool_result"constant`

          - `MCP_TOOL_RESULT("mcp_tool_result")`

      - `class BetaContainerUploadBlock:`

        Response model for a file uploaded to the container.

        - `fileId: String`

        - `type: JsonValue; "container_upload"constant`

          - `CONTAINER_UPLOAD("container_upload")`

    - `contextManagement: Optional<BetaContextManagementResponse>`

      Context management response.

      Information about context management strategies applied during the request.

      - `appliedEdits: List<AppliedEdit>`

        List of context management edits that were applied.

        - `class BetaClearToolUses20250919EditResponse:`

          - `clearedInputTokens: Long`

            Number of input tokens cleared by this edit.

          - `clearedToolUses: Long`

            Number of tool uses that were cleared.

          - `type: JsonValue; "clear_tool_uses_20250919"constant`

            The type of context management edit applied.

            - `CLEAR_TOOL_USES_20250919("clear_tool_uses_20250919")`

        - `class BetaClearThinking20251015EditResponse:`

          - `clearedInputTokens: Long`

            Number of input tokens cleared by this edit.

          - `clearedThinkingTurns: Long`

            Number of thinking turns that were cleared.

          - `type: JsonValue; "clear_thinking_20251015"constant`

            The type of context management edit applied.

            - `CLEAR_THINKING_20251015("clear_thinking_20251015")`

    - `model: Model`

      The model that will complete your prompt.

      See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

      - `CLAUDE_OPUS_4_5_20251101("claude-opus-4-5-20251101")`

        Premium model combining maximum intelligence with practical performance

      - `CLAUDE_OPUS_4_5("claude-opus-4-5")`

        Premium model combining maximum intelligence with practical performance

      - `CLAUDE_3_7_SONNET_LATEST("claude-3-7-sonnet-latest")`

        High-performance model with early extended thinking

      - `CLAUDE_3_7_SONNET_20250219("claude-3-7-sonnet-20250219")`

        High-performance model with early extended thinking

      - `CLAUDE_3_5_HAIKU_LATEST("claude-3-5-haiku-latest")`

        Fastest and most compact model for near-instant responsiveness

      - `CLAUDE_3_5_HAIKU_20241022("claude-3-5-haiku-20241022")`

        Our fastest model

      - `CLAUDE_HAIKU_4_5("claude-haiku-4-5")`

        Hybrid model, capable of near-instant responses and extended thinking

      - `CLAUDE_HAIKU_4_5_20251001("claude-haiku-4-5-20251001")`

        Hybrid model, capable of near-instant responses and extended thinking

      - `CLAUDE_SONNET_4_20250514("claude-sonnet-4-20250514")`

        High-performance model with extended thinking

      - `CLAUDE_SONNET_4_0("claude-sonnet-4-0")`

        High-performance model with extended thinking

      - `CLAUDE_4_SONNET_20250514("claude-4-sonnet-20250514")`

        High-performance model with extended thinking

      - `CLAUDE_SONNET_4_5("claude-sonnet-4-5")`

        Our best model for real-world agents and coding

      - `CLAUDE_SONNET_4_5_20250929("claude-sonnet-4-5-20250929")`

        Our best model for real-world agents and coding

      - `CLAUDE_OPUS_4_0("claude-opus-4-0")`

        Our most capable model

      - `CLAUDE_OPUS_4_20250514("claude-opus-4-20250514")`

        Our most capable model

      - `CLAUDE_4_OPUS_20250514("claude-4-opus-20250514")`

        Our most capable model

      - `CLAUDE_OPUS_4_1_20250805("claude-opus-4-1-20250805")`

        Our most capable model

      - `CLAUDE_3_OPUS_LATEST("claude-3-opus-latest")`

        Excels at writing and complex tasks

      - `CLAUDE_3_OPUS_20240229("claude-3-opus-20240229")`

        Excels at writing and complex tasks

      - `CLAUDE_3_HAIKU_20240307("claude-3-haiku-20240307")`

        Our previous most fast and cost-effective

    - `role: JsonValue; "assistant"constant`

      Conversational role of the generated message.

      This will always be `"assistant"`.

      - `ASSISTANT("assistant")`

    - `stopReason: Optional<BetaStopReason>`

      The reason that we stopped.

      This may be one the following values:

      * `"end_turn"`: the model reached a natural stopping point
      * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
      * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
      * `"tool_use"`: the model invoked one or more tools
      * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
      * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

      In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

      - `END_TURN("end_turn")`

      - `MAX_TOKENS("max_tokens")`

      - `STOP_SEQUENCE("stop_sequence")`

      - `TOOL_USE("tool_use")`

      - `PAUSE_TURN("pause_turn")`

      - `REFUSAL("refusal")`

      - `MODEL_CONTEXT_WINDOW_EXCEEDED("model_context_window_exceeded")`

    - `stopSequence: Optional<String>`

      Which custom stop sequence was generated, if any.

      This value will be a non-null string if one of your custom stop sequences was generated.

    - `type: JsonValue; "message"constant`

      Object type.

      For Messages, this is always `"message"`.

      - `MESSAGE("message")`

    - `usage: BetaUsage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cacheCreation: Optional<BetaCacheCreation>`

        Breakdown of cached tokens by TTL

        - `ephemeral1hInputTokens: Long`

          The number of input tokens used to create the 1 hour cache entry.

        - `ephemeral5mInputTokens: Long`

          The number of input tokens used to create the 5 minute cache entry.

      - `cacheCreationInputTokens: Optional<Long>`

        The number of input tokens used to create the cache entry.

      - `cacheReadInputTokens: Optional<Long>`

        The number of input tokens read from the cache.

      - `inputTokens: Long`

        The number of input tokens which were used.

      - `outputTokens: Long`

        The number of output tokens which were used.

      - `serverToolUse: Optional<BetaServerToolUsage>`

        The number of server tool requests.

        - `webFetchRequests: Long`

          The number of web fetch tool requests.

        - `webSearchRequests: Long`

          The number of web search tool requests.

      - `serviceTier: Optional<ServiceTier>`

        If the request used the priority, standard, or batch tier.

        - `STANDARD("standard")`

        - `PRIORITY("priority")`

        - `BATCH("batch")`

  - `type: JsonValue; "succeeded"constant`

    - `SUCCEEDED("succeeded")`
