## Count Tokens

`BetaMessageTokensCount beta().messages().countTokens(MessageCountTokensParamsparams, RequestOptionsrequestOptions = RequestOptions.none())`

**post** `/v1/messages/count_tokens`

Count the number of tokens in a Message.

The Token Count API can be used to count the number of tokens in a Message, including tools, images, and documents, without creating it.

Learn more about token counting in our [user guide](https://docs.claude.com/en/docs/build-with-claude/token-counting)

### Parameters

- `MessageCountTokensParams params`

  - `Optional<List<AnthropicBeta>> betas`

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

  - `List<BetaMessageParam> messages`

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

    - `Content content`

      - `String`

      - `List<BetaContentBlockParam>`

        - `class BetaTextBlockParam:`

          - `String text`

          - `JsonValue; type "text"constant`

            - `TEXT("text")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `Optional<List<BetaTextCitationParam>> citations`

            - `class BetaCitationCharLocationParam:`

              - `String citedText`

              - `long documentIndex`

              - `Optional<String> documentTitle`

              - `long endCharIndex`

              - `long startCharIndex`

              - `JsonValue; type "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class BetaCitationPageLocationParam:`

              - `String citedText`

              - `long documentIndex`

              - `Optional<String> documentTitle`

              - `long endPageNumber`

              - `long startPageNumber`

              - `JsonValue; type "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class BetaCitationContentBlockLocationParam:`

              - `String citedText`

              - `long documentIndex`

              - `Optional<String> documentTitle`

              - `long endBlockIndex`

              - `long startBlockIndex`

              - `JsonValue; type "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class BetaCitationWebSearchResultLocationParam:`

              - `String citedText`

              - `String encryptedIndex`

              - `Optional<String> title`

              - `JsonValue; type "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `String url`

            - `class BetaCitationSearchResultLocationParam:`

              - `String citedText`

              - `long endBlockIndex`

              - `long searchResultIndex`

              - `String source`

              - `long startBlockIndex`

              - `Optional<String> title`

              - `JsonValue; type "search_result_location"constant`

                - `SEARCH_RESULT_LOCATION("search_result_location")`

        - `class BetaImageBlockParam:`

          - `Source source`

            - `class BetaBase64ImageSource:`

              - `String data`

              - `MediaType mediaType`

                - `IMAGE_JPEG("image/jpeg")`

                - `IMAGE_PNG("image/png")`

                - `IMAGE_GIF("image/gif")`

                - `IMAGE_WEBP("image/webp")`

              - `JsonValue; type "base64"constant`

                - `BASE64("base64")`

            - `class BetaUrlImageSource:`

              - `JsonValue; type "url"constant`

                - `URL("url")`

              - `String url`

            - `class BetaFileImageSource:`

              - `String fileId`

              - `JsonValue; type "file"constant`

                - `FILE("file")`

          - `JsonValue; type "image"constant`

            - `IMAGE("image")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaRequestDocumentBlock:`

          - `Source source`

            - `class BetaBase64PdfSource:`

              - `String data`

              - `JsonValue; mediaType "application/pdf"constant`

                - `APPLICATION_PDF("application/pdf")`

              - `JsonValue; type "base64"constant`

                - `BASE64("base64")`

            - `class BetaPlainTextSource:`

              - `String data`

              - `JsonValue; mediaType "text/plain"constant`

                - `TEXT_PLAIN("text/plain")`

              - `JsonValue; type "text"constant`

                - `TEXT("text")`

            - `class BetaContentBlockSource:`

              - `Content content`

                - `String`

                - `List<BetaContentBlockSourceContent>`

                  - `class BetaTextBlockParam:`

                    - `String text`

                    - `JsonValue; type "text"constant`

                      - `TEXT("text")`

                    - `Optional<BetaCacheControlEphemeral> cacheControl`

                      Create a cache control breakpoint at this content block.

                      - `JsonValue; type "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `Optional<Ttl> ttl`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                    - `Optional<List<BetaTextCitationParam>> citations`

                      - `class BetaCitationCharLocationParam:`

                        - `String citedText`

                        - `long documentIndex`

                        - `Optional<String> documentTitle`

                        - `long endCharIndex`

                        - `long startCharIndex`

                        - `JsonValue; type "char_location"constant`

                          - `CHAR_LOCATION("char_location")`

                      - `class BetaCitationPageLocationParam:`

                        - `String citedText`

                        - `long documentIndex`

                        - `Optional<String> documentTitle`

                        - `long endPageNumber`

                        - `long startPageNumber`

                        - `JsonValue; type "page_location"constant`

                          - `PAGE_LOCATION("page_location")`

                      - `class BetaCitationContentBlockLocationParam:`

                        - `String citedText`

                        - `long documentIndex`

                        - `Optional<String> documentTitle`

                        - `long endBlockIndex`

                        - `long startBlockIndex`

                        - `JsonValue; type "content_block_location"constant`

                          - `CONTENT_BLOCK_LOCATION("content_block_location")`

                      - `class BetaCitationWebSearchResultLocationParam:`

                        - `String citedText`

                        - `String encryptedIndex`

                        - `Optional<String> title`

                        - `JsonValue; type "web_search_result_location"constant`

                          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                        - `String url`

                      - `class BetaCitationSearchResultLocationParam:`

                        - `String citedText`

                        - `long endBlockIndex`

                        - `long searchResultIndex`

                        - `String source`

                        - `long startBlockIndex`

                        - `Optional<String> title`

                        - `JsonValue; type "search_result_location"constant`

                          - `SEARCH_RESULT_LOCATION("search_result_location")`

                  - `class BetaImageBlockParam:`

                    - `Source source`

                      - `class BetaBase64ImageSource:`

                        - `String data`

                        - `MediaType mediaType`

                          - `IMAGE_JPEG("image/jpeg")`

                          - `IMAGE_PNG("image/png")`

                          - `IMAGE_GIF("image/gif")`

                          - `IMAGE_WEBP("image/webp")`

                        - `JsonValue; type "base64"constant`

                          - `BASE64("base64")`

                      - `class BetaUrlImageSource:`

                        - `JsonValue; type "url"constant`

                          - `URL("url")`

                        - `String url`

                      - `class BetaFileImageSource:`

                        - `String fileId`

                        - `JsonValue; type "file"constant`

                          - `FILE("file")`

                    - `JsonValue; type "image"constant`

                      - `IMAGE("image")`

                    - `Optional<BetaCacheControlEphemeral> cacheControl`

                      Create a cache control breakpoint at this content block.

                      - `JsonValue; type "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `Optional<Ttl> ttl`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

              - `JsonValue; type "content"constant`

                - `CONTENT("content")`

            - `class BetaUrlPdfSource:`

              - `JsonValue; type "url"constant`

                - `URL("url")`

              - `String url`

            - `class BetaFileDocumentSource:`

              - `String fileId`

              - `JsonValue; type "file"constant`

                - `FILE("file")`

          - `JsonValue; type "document"constant`

            - `DOCUMENT("document")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `Optional<BetaCitationsConfigParam> citations`

            - `Optional<Boolean> enabled`

          - `Optional<String> context`

          - `Optional<String> title`

        - `class BetaSearchResultBlockParam:`

          - `List<BetaTextBlockParam> content`

            - `String text`

            - `JsonValue; type "text"constant`

              - `TEXT("text")`

            - `Optional<BetaCacheControlEphemeral> cacheControl`

              Create a cache control breakpoint at this content block.

              - `JsonValue; type "ephemeral"constant`

                - `EPHEMERAL("ephemeral")`

              - `Optional<Ttl> ttl`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `TTL_5M("5m")`

                - `TTL_1H("1h")`

            - `Optional<List<BetaTextCitationParam>> citations`

              - `class BetaCitationCharLocationParam:`

                - `String citedText`

                - `long documentIndex`

                - `Optional<String> documentTitle`

                - `long endCharIndex`

                - `long startCharIndex`

                - `JsonValue; type "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class BetaCitationPageLocationParam:`

                - `String citedText`

                - `long documentIndex`

                - `Optional<String> documentTitle`

                - `long endPageNumber`

                - `long startPageNumber`

                - `JsonValue; type "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class BetaCitationContentBlockLocationParam:`

                - `String citedText`

                - `long documentIndex`

                - `Optional<String> documentTitle`

                - `long endBlockIndex`

                - `long startBlockIndex`

                - `JsonValue; type "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class BetaCitationWebSearchResultLocationParam:`

                - `String citedText`

                - `String encryptedIndex`

                - `Optional<String> title`

                - `JsonValue; type "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `String url`

              - `class BetaCitationSearchResultLocationParam:`

                - `String citedText`

                - `long endBlockIndex`

                - `long searchResultIndex`

                - `String source`

                - `long startBlockIndex`

                - `Optional<String> title`

                - `JsonValue; type "search_result_location"constant`

                  - `SEARCH_RESULT_LOCATION("search_result_location")`

          - `String source`

          - `String title`

          - `JsonValue; type "search_result"constant`

            - `SEARCH_RESULT("search_result")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `Optional<BetaCitationsConfigParam> citations`

            - `Optional<Boolean> enabled`

        - `class BetaThinkingBlockParam:`

          - `String signature`

          - `String thinking`

          - `JsonValue; type "thinking"constant`

            - `THINKING("thinking")`

        - `class BetaRedactedThinkingBlockParam:`

          - `String data`

          - `JsonValue; type "redacted_thinking"constant`

            - `REDACTED_THINKING("redacted_thinking")`

        - `class BetaToolUseBlockParam:`

          - `String id`

          - `Input input`

          - `String name`

          - `JsonValue; type "tool_use"constant`

            - `TOOL_USE("tool_use")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `Optional<Caller> caller`

            Tool invocation directly from the model.

            - `class BetaDirectCaller:`

              Tool invocation directly from the model.

              - `JsonValue; type "direct"constant`

                - `DIRECT("direct")`

            - `class BetaServerToolCaller:`

              Tool invocation generated by a server-side tool.

              - `String toolId`

              - `JsonValue; type "code_execution_20250825"constant`

                - `CODE_EXECUTION_20250825("code_execution_20250825")`

        - `class BetaToolResultBlockParam:`

          - `String toolUseId`

          - `JsonValue; type "tool_result"constant`

            - `TOOL_RESULT("tool_result")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `Optional<Content> content`

            - `String`

            - `List<Block>`

              - `class BetaTextBlockParam:`

                - `String text`

                - `JsonValue; type "text"constant`

                  - `TEXT("text")`

                - `Optional<BetaCacheControlEphemeral> cacheControl`

                  Create a cache control breakpoint at this content block.

                  - `JsonValue; type "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `Optional<Ttl> ttl`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `Optional<List<BetaTextCitationParam>> citations`

                  - `class BetaCitationCharLocationParam:`

                    - `String citedText`

                    - `long documentIndex`

                    - `Optional<String> documentTitle`

                    - `long endCharIndex`

                    - `long startCharIndex`

                    - `JsonValue; type "char_location"constant`

                      - `CHAR_LOCATION("char_location")`

                  - `class BetaCitationPageLocationParam:`

                    - `String citedText`

                    - `long documentIndex`

                    - `Optional<String> documentTitle`

                    - `long endPageNumber`

                    - `long startPageNumber`

                    - `JsonValue; type "page_location"constant`

                      - `PAGE_LOCATION("page_location")`

                  - `class BetaCitationContentBlockLocationParam:`

                    - `String citedText`

                    - `long documentIndex`

                    - `Optional<String> documentTitle`

                    - `long endBlockIndex`

                    - `long startBlockIndex`

                    - `JsonValue; type "content_block_location"constant`

                      - `CONTENT_BLOCK_LOCATION("content_block_location")`

                  - `class BetaCitationWebSearchResultLocationParam:`

                    - `String citedText`

                    - `String encryptedIndex`

                    - `Optional<String> title`

                    - `JsonValue; type "web_search_result_location"constant`

                      - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                    - `String url`

                  - `class BetaCitationSearchResultLocationParam:`

                    - `String citedText`

                    - `long endBlockIndex`

                    - `long searchResultIndex`

                    - `String source`

                    - `long startBlockIndex`

                    - `Optional<String> title`

                    - `JsonValue; type "search_result_location"constant`

                      - `SEARCH_RESULT_LOCATION("search_result_location")`

              - `class BetaImageBlockParam:`

                - `Source source`

                  - `class BetaBase64ImageSource:`

                    - `String data`

                    - `MediaType mediaType`

                      - `IMAGE_JPEG("image/jpeg")`

                      - `IMAGE_PNG("image/png")`

                      - `IMAGE_GIF("image/gif")`

                      - `IMAGE_WEBP("image/webp")`

                    - `JsonValue; type "base64"constant`

                      - `BASE64("base64")`

                  - `class BetaUrlImageSource:`

                    - `JsonValue; type "url"constant`

                      - `URL("url")`

                    - `String url`

                  - `class BetaFileImageSource:`

                    - `String fileId`

                    - `JsonValue; type "file"constant`

                      - `FILE("file")`

                - `JsonValue; type "image"constant`

                  - `IMAGE("image")`

                - `Optional<BetaCacheControlEphemeral> cacheControl`

                  Create a cache control breakpoint at this content block.

                  - `JsonValue; type "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `Optional<Ttl> ttl`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

              - `class BetaSearchResultBlockParam:`

                - `List<BetaTextBlockParam> content`

                  - `String text`

                  - `JsonValue; type "text"constant`

                    - `TEXT("text")`

                  - `Optional<BetaCacheControlEphemeral> cacheControl`

                    Create a cache control breakpoint at this content block.

                    - `JsonValue; type "ephemeral"constant`

                      - `EPHEMERAL("ephemeral")`

                    - `Optional<Ttl> ttl`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `TTL_5M("5m")`

                      - `TTL_1H("1h")`

                  - `Optional<List<BetaTextCitationParam>> citations`

                    - `class BetaCitationCharLocationParam:`

                      - `String citedText`

                      - `long documentIndex`

                      - `Optional<String> documentTitle`

                      - `long endCharIndex`

                      - `long startCharIndex`

                      - `JsonValue; type "char_location"constant`

                        - `CHAR_LOCATION("char_location")`

                    - `class BetaCitationPageLocationParam:`

                      - `String citedText`

                      - `long documentIndex`

                      - `Optional<String> documentTitle`

                      - `long endPageNumber`

                      - `long startPageNumber`

                      - `JsonValue; type "page_location"constant`

                        - `PAGE_LOCATION("page_location")`

                    - `class BetaCitationContentBlockLocationParam:`

                      - `String citedText`

                      - `long documentIndex`

                      - `Optional<String> documentTitle`

                      - `long endBlockIndex`

                      - `long startBlockIndex`

                      - `JsonValue; type "content_block_location"constant`

                        - `CONTENT_BLOCK_LOCATION("content_block_location")`

                    - `class BetaCitationWebSearchResultLocationParam:`

                      - `String citedText`

                      - `String encryptedIndex`

                      - `Optional<String> title`

                      - `JsonValue; type "web_search_result_location"constant`

                        - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                      - `String url`

                    - `class BetaCitationSearchResultLocationParam:`

                      - `String citedText`

                      - `long endBlockIndex`

                      - `long searchResultIndex`

                      - `String source`

                      - `long startBlockIndex`

                      - `Optional<String> title`

                      - `JsonValue; type "search_result_location"constant`

                        - `SEARCH_RESULT_LOCATION("search_result_location")`

                - `String source`

                - `String title`

                - `JsonValue; type "search_result"constant`

                  - `SEARCH_RESULT("search_result")`

                - `Optional<BetaCacheControlEphemeral> cacheControl`

                  Create a cache control breakpoint at this content block.

                  - `JsonValue; type "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `Optional<Ttl> ttl`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `Optional<BetaCitationsConfigParam> citations`

                  - `Optional<Boolean> enabled`

              - `class BetaRequestDocumentBlock:`

                - `Source source`

                  - `class BetaBase64PdfSource:`

                    - `String data`

                    - `JsonValue; mediaType "application/pdf"constant`

                      - `APPLICATION_PDF("application/pdf")`

                    - `JsonValue; type "base64"constant`

                      - `BASE64("base64")`

                  - `class BetaPlainTextSource:`

                    - `String data`

                    - `JsonValue; mediaType "text/plain"constant`

                      - `TEXT_PLAIN("text/plain")`

                    - `JsonValue; type "text"constant`

                      - `TEXT("text")`

                  - `class BetaContentBlockSource:`

                    - `Content content`

                      - `String`

                      - `List<BetaContentBlockSourceContent>`

                        - `class BetaTextBlockParam:`

                          - `String text`

                          - `JsonValue; type "text"constant`

                            - `TEXT("text")`

                          - `Optional<BetaCacheControlEphemeral> cacheControl`

                            Create a cache control breakpoint at this content block.

                            - `JsonValue; type "ephemeral"constant`

                              - `EPHEMERAL("ephemeral")`

                            - `Optional<Ttl> ttl`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `TTL_5M("5m")`

                              - `TTL_1H("1h")`

                          - `Optional<List<BetaTextCitationParam>> citations`

                            - `class BetaCitationCharLocationParam:`

                              - `String citedText`

                              - `long documentIndex`

                              - `Optional<String> documentTitle`

                              - `long endCharIndex`

                              - `long startCharIndex`

                              - `JsonValue; type "char_location"constant`

                                - `CHAR_LOCATION("char_location")`

                            - `class BetaCitationPageLocationParam:`

                              - `String citedText`

                              - `long documentIndex`

                              - `Optional<String> documentTitle`

                              - `long endPageNumber`

                              - `long startPageNumber`

                              - `JsonValue; type "page_location"constant`

                                - `PAGE_LOCATION("page_location")`

                            - `class BetaCitationContentBlockLocationParam:`

                              - `String citedText`

                              - `long documentIndex`

                              - `Optional<String> documentTitle`

                              - `long endBlockIndex`

                              - `long startBlockIndex`

                              - `JsonValue; type "content_block_location"constant`

                                - `CONTENT_BLOCK_LOCATION("content_block_location")`

                            - `class BetaCitationWebSearchResultLocationParam:`

                              - `String citedText`

                              - `String encryptedIndex`

                              - `Optional<String> title`

                              - `JsonValue; type "web_search_result_location"constant`

                                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                              - `String url`

                            - `class BetaCitationSearchResultLocationParam:`

                              - `String citedText`

                              - `long endBlockIndex`

                              - `long searchResultIndex`

                              - `String source`

                              - `long startBlockIndex`

                              - `Optional<String> title`

                              - `JsonValue; type "search_result_location"constant`

                                - `SEARCH_RESULT_LOCATION("search_result_location")`

                        - `class BetaImageBlockParam:`

                          - `Source source`

                            - `class BetaBase64ImageSource:`

                              - `String data`

                              - `MediaType mediaType`

                                - `IMAGE_JPEG("image/jpeg")`

                                - `IMAGE_PNG("image/png")`

                                - `IMAGE_GIF("image/gif")`

                                - `IMAGE_WEBP("image/webp")`

                              - `JsonValue; type "base64"constant`

                                - `BASE64("base64")`

                            - `class BetaUrlImageSource:`

                              - `JsonValue; type "url"constant`

                                - `URL("url")`

                              - `String url`

                            - `class BetaFileImageSource:`

                              - `String fileId`

                              - `JsonValue; type "file"constant`

                                - `FILE("file")`

                          - `JsonValue; type "image"constant`

                            - `IMAGE("image")`

                          - `Optional<BetaCacheControlEphemeral> cacheControl`

                            Create a cache control breakpoint at this content block.

                            - `JsonValue; type "ephemeral"constant`

                              - `EPHEMERAL("ephemeral")`

                            - `Optional<Ttl> ttl`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `TTL_5M("5m")`

                              - `TTL_1H("1h")`

                    - `JsonValue; type "content"constant`

                      - `CONTENT("content")`

                  - `class BetaUrlPdfSource:`

                    - `JsonValue; type "url"constant`

                      - `URL("url")`

                    - `String url`

                  - `class BetaFileDocumentSource:`

                    - `String fileId`

                    - `JsonValue; type "file"constant`

                      - `FILE("file")`

                - `JsonValue; type "document"constant`

                  - `DOCUMENT("document")`

                - `Optional<BetaCacheControlEphemeral> cacheControl`

                  Create a cache control breakpoint at this content block.

                  - `JsonValue; type "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `Optional<Ttl> ttl`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `Optional<BetaCitationsConfigParam> citations`

                  - `Optional<Boolean> enabled`

                - `Optional<String> context`

                - `Optional<String> title`

              - `class BetaToolReferenceBlockParam:`

                Tool reference block that can be included in tool_result content.

                - `String toolName`

                - `JsonValue; type "tool_reference"constant`

                  - `TOOL_REFERENCE("tool_reference")`

                - `Optional<BetaCacheControlEphemeral> cacheControl`

                  Create a cache control breakpoint at this content block.

                  - `JsonValue; type "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `Optional<Ttl> ttl`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

          - `Optional<Boolean> isError`

        - `class BetaServerToolUseBlockParam:`

          - `String id`

          - `Input input`

          - `Name name`

            - `WEB_SEARCH("web_search")`

            - `WEB_FETCH("web_fetch")`

            - `CODE_EXECUTION("code_execution")`

            - `BASH_CODE_EXECUTION("bash_code_execution")`

            - `TEXT_EDITOR_CODE_EXECUTION("text_editor_code_execution")`

            - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

            - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

          - `JsonValue; type "server_tool_use"constant`

            - `SERVER_TOOL_USE("server_tool_use")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `Optional<Caller> caller`

            Tool invocation directly from the model.

            - `class BetaDirectCaller:`

              Tool invocation directly from the model.

              - `JsonValue; type "direct"constant`

                - `DIRECT("direct")`

            - `class BetaServerToolCaller:`

              Tool invocation generated by a server-side tool.

              - `String toolId`

              - `JsonValue; type "code_execution_20250825"constant`

                - `CODE_EXECUTION_20250825("code_execution_20250825")`

        - `class BetaWebSearchToolResultBlockParam:`

          - `BetaWebSearchToolResultBlockParamContent content`

            - `List<BetaWebSearchResultBlockParam>`

              - `String encryptedContent`

              - `String title`

              - `JsonValue; type "web_search_result"constant`

                - `WEB_SEARCH_RESULT("web_search_result")`

              - `String url`

              - `Optional<String> pageAge`

            - `class BetaWebSearchToolRequestError:`

              - `BetaWebSearchToolResultErrorCode errorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `QUERY_TOO_LONG("query_too_long")`

              - `JsonValue; type "web_search_tool_result_error"constant`

                - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

          - `String toolUseId`

          - `JsonValue; type "web_search_tool_result"constant`

            - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaWebFetchToolResultBlockParam:`

          - `Content content`

            - `class BetaWebFetchToolResultErrorBlockParam:`

              - `BetaWebFetchToolResultErrorCode errorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `URL_TOO_LONG("url_too_long")`

                - `URL_NOT_ALLOWED("url_not_allowed")`

                - `URL_NOT_ACCESSIBLE("url_not_accessible")`

                - `UNSUPPORTED_CONTENT_TYPE("unsupported_content_type")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                - `UNAVAILABLE("unavailable")`

              - `JsonValue; type "web_fetch_tool_result_error"constant`

                - `WEB_FETCH_TOOL_RESULT_ERROR("web_fetch_tool_result_error")`

            - `class BetaWebFetchBlockParam:`

              - `BetaRequestDocumentBlock content`

                - `Source source`

                  - `class BetaBase64PdfSource:`

                    - `String data`

                    - `JsonValue; mediaType "application/pdf"constant`

                      - `APPLICATION_PDF("application/pdf")`

                    - `JsonValue; type "base64"constant`

                      - `BASE64("base64")`

                  - `class BetaPlainTextSource:`

                    - `String data`

                    - `JsonValue; mediaType "text/plain"constant`

                      - `TEXT_PLAIN("text/plain")`

                    - `JsonValue; type "text"constant`

                      - `TEXT("text")`

                  - `class BetaContentBlockSource:`

                    - `Content content`

                      - `String`

                      - `List<BetaContentBlockSourceContent>`

                        - `class BetaTextBlockParam:`

                          - `String text`

                          - `JsonValue; type "text"constant`

                            - `TEXT("text")`

                          - `Optional<BetaCacheControlEphemeral> cacheControl`

                            Create a cache control breakpoint at this content block.

                            - `JsonValue; type "ephemeral"constant`

                              - `EPHEMERAL("ephemeral")`

                            - `Optional<Ttl> ttl`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `TTL_5M("5m")`

                              - `TTL_1H("1h")`

                          - `Optional<List<BetaTextCitationParam>> citations`

                            - `class BetaCitationCharLocationParam:`

                              - `String citedText`

                              - `long documentIndex`

                              - `Optional<String> documentTitle`

                              - `long endCharIndex`

                              - `long startCharIndex`

                              - `JsonValue; type "char_location"constant`

                                - `CHAR_LOCATION("char_location")`

                            - `class BetaCitationPageLocationParam:`

                              - `String citedText`

                              - `long documentIndex`

                              - `Optional<String> documentTitle`

                              - `long endPageNumber`

                              - `long startPageNumber`

                              - `JsonValue; type "page_location"constant`

                                - `PAGE_LOCATION("page_location")`

                            - `class BetaCitationContentBlockLocationParam:`

                              - `String citedText`

                              - `long documentIndex`

                              - `Optional<String> documentTitle`

                              - `long endBlockIndex`

                              - `long startBlockIndex`

                              - `JsonValue; type "content_block_location"constant`

                                - `CONTENT_BLOCK_LOCATION("content_block_location")`

                            - `class BetaCitationWebSearchResultLocationParam:`

                              - `String citedText`

                              - `String encryptedIndex`

                              - `Optional<String> title`

                              - `JsonValue; type "web_search_result_location"constant`

                                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                              - `String url`

                            - `class BetaCitationSearchResultLocationParam:`

                              - `String citedText`

                              - `long endBlockIndex`

                              - `long searchResultIndex`

                              - `String source`

                              - `long startBlockIndex`

                              - `Optional<String> title`

                              - `JsonValue; type "search_result_location"constant`

                                - `SEARCH_RESULT_LOCATION("search_result_location")`

                        - `class BetaImageBlockParam:`

                          - `Source source`

                            - `class BetaBase64ImageSource:`

                              - `String data`

                              - `MediaType mediaType`

                                - `IMAGE_JPEG("image/jpeg")`

                                - `IMAGE_PNG("image/png")`

                                - `IMAGE_GIF("image/gif")`

                                - `IMAGE_WEBP("image/webp")`

                              - `JsonValue; type "base64"constant`

                                - `BASE64("base64")`

                            - `class BetaUrlImageSource:`

                              - `JsonValue; type "url"constant`

                                - `URL("url")`

                              - `String url`

                            - `class BetaFileImageSource:`

                              - `String fileId`

                              - `JsonValue; type "file"constant`

                                - `FILE("file")`

                          - `JsonValue; type "image"constant`

                            - `IMAGE("image")`

                          - `Optional<BetaCacheControlEphemeral> cacheControl`

                            Create a cache control breakpoint at this content block.

                            - `JsonValue; type "ephemeral"constant`

                              - `EPHEMERAL("ephemeral")`

                            - `Optional<Ttl> ttl`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `TTL_5M("5m")`

                              - `TTL_1H("1h")`

                    - `JsonValue; type "content"constant`

                      - `CONTENT("content")`

                  - `class BetaUrlPdfSource:`

                    - `JsonValue; type "url"constant`

                      - `URL("url")`

                    - `String url`

                  - `class BetaFileDocumentSource:`

                    - `String fileId`

                    - `JsonValue; type "file"constant`

                      - `FILE("file")`

                - `JsonValue; type "document"constant`

                  - `DOCUMENT("document")`

                - `Optional<BetaCacheControlEphemeral> cacheControl`

                  Create a cache control breakpoint at this content block.

                  - `JsonValue; type "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `Optional<Ttl> ttl`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `Optional<BetaCitationsConfigParam> citations`

                  - `Optional<Boolean> enabled`

                - `Optional<String> context`

                - `Optional<String> title`

              - `JsonValue; type "web_fetch_result"constant`

                - `WEB_FETCH_RESULT("web_fetch_result")`

              - `String url`

                Fetched content URL

              - `Optional<String> retrievedAt`

                ISO 8601 timestamp when the content was retrieved

          - `String toolUseId`

          - `JsonValue; type "web_fetch_tool_result"constant`

            - `WEB_FETCH_TOOL_RESULT("web_fetch_tool_result")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaCodeExecutionToolResultBlockParam:`

          - `BetaCodeExecutionToolResultBlockParamContent content`

            - `class BetaCodeExecutionToolResultErrorParam:`

              - `BetaCodeExecutionToolResultErrorCode errorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `JsonValue; type "code_execution_tool_result_error"constant`

                - `CODE_EXECUTION_TOOL_RESULT_ERROR("code_execution_tool_result_error")`

            - `class BetaCodeExecutionResultBlockParam:`

              - `List<BetaCodeExecutionOutputBlockParam> content`

                - `String fileId`

                - `JsonValue; type "code_execution_output"constant`

                  - `CODE_EXECUTION_OUTPUT("code_execution_output")`

              - `long returnCode`

              - `String stderr`

              - `String stdout`

              - `JsonValue; type "code_execution_result"constant`

                - `CODE_EXECUTION_RESULT("code_execution_result")`

          - `String toolUseId`

          - `JsonValue; type "code_execution_tool_result"constant`

            - `CODE_EXECUTION_TOOL_RESULT("code_execution_tool_result")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaBashCodeExecutionToolResultBlockParam:`

          - `Content content`

            - `class BetaBashCodeExecutionToolResultErrorParam:`

              - `ErrorCode errorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `OUTPUT_FILE_TOO_LARGE("output_file_too_large")`

              - `JsonValue; type "bash_code_execution_tool_result_error"constant`

                - `BASH_CODE_EXECUTION_TOOL_RESULT_ERROR("bash_code_execution_tool_result_error")`

            - `class BetaBashCodeExecutionResultBlockParam:`

              - `List<BetaBashCodeExecutionOutputBlockParam> content`

                - `String fileId`

                - `JsonValue; type "bash_code_execution_output"constant`

                  - `BASH_CODE_EXECUTION_OUTPUT("bash_code_execution_output")`

              - `long returnCode`

              - `String stderr`

              - `String stdout`

              - `JsonValue; type "bash_code_execution_result"constant`

                - `BASH_CODE_EXECUTION_RESULT("bash_code_execution_result")`

          - `String toolUseId`

          - `JsonValue; type "bash_code_execution_tool_result"constant`

            - `BASH_CODE_EXECUTION_TOOL_RESULT("bash_code_execution_tool_result")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaTextEditorCodeExecutionToolResultBlockParam:`

          - `Content content`

            - `class BetaTextEditorCodeExecutionToolResultErrorParam:`

              - `ErrorCode errorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

                - `FILE_NOT_FOUND("file_not_found")`

              - `JsonValue; type "text_editor_code_execution_tool_result_error"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT_ERROR("text_editor_code_execution_tool_result_error")`

              - `Optional<String> errorMessage`

            - `class BetaTextEditorCodeExecutionViewResultBlockParam:`

              - `String content`

              - `FileType fileType`

                - `TEXT("text")`

                - `IMAGE("image")`

                - `PDF("pdf")`

              - `JsonValue; type "text_editor_code_execution_view_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_VIEW_RESULT("text_editor_code_execution_view_result")`

              - `Optional<Long> numLines`

              - `Optional<Long> startLine`

              - `Optional<Long> totalLines`

            - `class BetaTextEditorCodeExecutionCreateResultBlockParam:`

              - `boolean isFileUpdate`

              - `JsonValue; type "text_editor_code_execution_create_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_CREATE_RESULT("text_editor_code_execution_create_result")`

            - `class BetaTextEditorCodeExecutionStrReplaceResultBlockParam:`

              - `JsonValue; type "text_editor_code_execution_str_replace_result"constant`

                - `TEXT_EDITOR_CODE_EXECUTION_STR_REPLACE_RESULT("text_editor_code_execution_str_replace_result")`

              - `Optional<List<String>> lines`

              - `Optional<Long> newLines`

              - `Optional<Long> newStart`

              - `Optional<Long> oldLines`

              - `Optional<Long> oldStart`

          - `String toolUseId`

          - `JsonValue; type "text_editor_code_execution_tool_result"constant`

            - `TEXT_EDITOR_CODE_EXECUTION_TOOL_RESULT("text_editor_code_execution_tool_result")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaToolSearchToolResultBlockParam:`

          - `Content content`

            - `class BetaToolSearchToolResultErrorParam:`

              - `ErrorCode errorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `EXECUTION_TIME_EXCEEDED("execution_time_exceeded")`

              - `JsonValue; type "tool_search_tool_result_error"constant`

                - `TOOL_SEARCH_TOOL_RESULT_ERROR("tool_search_tool_result_error")`

            - `class BetaToolSearchToolSearchResultBlockParam:`

              - `List<BetaToolReferenceBlockParam> toolReferences`

                - `String toolName`

                - `JsonValue; type "tool_reference"constant`

                  - `TOOL_REFERENCE("tool_reference")`

                - `Optional<BetaCacheControlEphemeral> cacheControl`

                  Create a cache control breakpoint at this content block.

                  - `JsonValue; type "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `Optional<Ttl> ttl`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

              - `JsonValue; type "tool_search_tool_search_result"constant`

                - `TOOL_SEARCH_TOOL_SEARCH_RESULT("tool_search_tool_search_result")`

          - `String toolUseId`

          - `JsonValue; type "tool_search_tool_result"constant`

            - `TOOL_SEARCH_TOOL_RESULT("tool_search_tool_result")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaMcpToolUseBlockParam:`

          - `String id`

          - `Input input`

          - `String name`

          - `String serverName`

            The name of the MCP server

          - `JsonValue; type "mcp_tool_use"constant`

            - `MCP_TOOL_USE("mcp_tool_use")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class BetaRequestMcpToolResultBlockParam:`

          - `String toolUseId`

          - `JsonValue; type "mcp_tool_result"constant`

            - `MCP_TOOL_RESULT("mcp_tool_result")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `Optional<Content> content`

            - `String`

            - `List<BetaTextBlockParam>`

              - `String text`

              - `JsonValue; type "text"constant`

                - `TEXT("text")`

              - `Optional<BetaCacheControlEphemeral> cacheControl`

                Create a cache control breakpoint at this content block.

                - `JsonValue; type "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `Optional<Ttl> ttl`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `Optional<List<BetaTextCitationParam>> citations`

                - `class BetaCitationCharLocationParam:`

                  - `String citedText`

                  - `long documentIndex`

                  - `Optional<String> documentTitle`

                  - `long endCharIndex`

                  - `long startCharIndex`

                  - `JsonValue; type "char_location"constant`

                    - `CHAR_LOCATION("char_location")`

                - `class BetaCitationPageLocationParam:`

                  - `String citedText`

                  - `long documentIndex`

                  - `Optional<String> documentTitle`

                  - `long endPageNumber`

                  - `long startPageNumber`

                  - `JsonValue; type "page_location"constant`

                    - `PAGE_LOCATION("page_location")`

                - `class BetaCitationContentBlockLocationParam:`

                  - `String citedText`

                  - `long documentIndex`

                  - `Optional<String> documentTitle`

                  - `long endBlockIndex`

                  - `long startBlockIndex`

                  - `JsonValue; type "content_block_location"constant`

                    - `CONTENT_BLOCK_LOCATION("content_block_location")`

                - `class BetaCitationWebSearchResultLocationParam:`

                  - `String citedText`

                  - `String encryptedIndex`

                  - `Optional<String> title`

                  - `JsonValue; type "web_search_result_location"constant`

                    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                  - `String url`

                - `class BetaCitationSearchResultLocationParam:`

                  - `String citedText`

                  - `long endBlockIndex`

                  - `long searchResultIndex`

                  - `String source`

                  - `long startBlockIndex`

                  - `Optional<String> title`

                  - `JsonValue; type "search_result_location"constant`

                    - `SEARCH_RESULT_LOCATION("search_result_location")`

          - `Optional<Boolean> isError`

        - `class BetaContainerUploadBlockParam:`

          A content block that represents a file to be uploaded to the container
          Files uploaded via this block will be available in the container's input directory.

          - `String fileId`

          - `JsonValue; type "container_upload"constant`

            - `CONTAINER_UPLOAD("container_upload")`

          - `Optional<BetaCacheControlEphemeral> cacheControl`

            Create a cache control breakpoint at this content block.

            - `JsonValue; type "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `Optional<Ttl> ttl`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

    - `Role role`

      - `USER("user")`

      - `ASSISTANT("assistant")`

  - `Model model`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

  - `Optional<BetaContextManagementConfig> contextManagement`

    Context management configuration.

    This allows you to control how Claude manages context across multiple requests, such as whether to clear function results or not.

  - `Optional<List<BetaRequestMcpServerUrlDefinition>> mcpServers`

    MCP servers to be utilized in this request

    - `String name`

    - `JsonValue; type "url"constant`

      - `URL("url")`

    - `String url`

    - `Optional<String> authorizationToken`

    - `Optional<BetaRequestMcpServerToolConfiguration> toolConfiguration`

      - `Optional<List<String>> allowedTools`

      - `Optional<Boolean> enabled`

  - `Optional<BetaOutputConfig> outputConfig`

    Configuration options for the model's output. Controls aspects like how much effort the model puts into its response.

  - `Optional<BetaJsonOutputFormat> outputFormat`

    A schema to specify Claude's output format in responses.

  - `Optional<System> system`

    System prompt.

    A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

    - `String`

    - `List<BetaTextBlockParam>`

      - `String text`

      - `JsonValue; type "text"constant`

        - `TEXT("text")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<List<BetaTextCitationParam>> citations`

        - `class BetaCitationCharLocationParam:`

          - `String citedText`

          - `long documentIndex`

          - `Optional<String> documentTitle`

          - `long endCharIndex`

          - `long startCharIndex`

          - `JsonValue; type "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class BetaCitationPageLocationParam:`

          - `String citedText`

          - `long documentIndex`

          - `Optional<String> documentTitle`

          - `long endPageNumber`

          - `long startPageNumber`

          - `JsonValue; type "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class BetaCitationContentBlockLocationParam:`

          - `String citedText`

          - `long documentIndex`

          - `Optional<String> documentTitle`

          - `long endBlockIndex`

          - `long startBlockIndex`

          - `JsonValue; type "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class BetaCitationWebSearchResultLocationParam:`

          - `String citedText`

          - `String encryptedIndex`

          - `Optional<String> title`

          - `JsonValue; type "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `String url`

        - `class BetaCitationSearchResultLocationParam:`

          - `String citedText`

          - `long endBlockIndex`

          - `long searchResultIndex`

          - `String source`

          - `long startBlockIndex`

          - `Optional<String> title`

          - `JsonValue; type "search_result_location"constant`

            - `SEARCH_RESULT_LOCATION("search_result_location")`

  - `Optional<BetaThinkingConfigParam> thinking`

    Configuration for enabling Claude's extended thinking.

    When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `Optional<BetaToolChoice> toolChoice`

    How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `Optional<List<Tool>> tools`

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

      - `InputSchema inputSchema`

        [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

        This defines the shape of the `input` that your tool accepts and that the model will produce.

        - `JsonValue; type "object"constant`

          - `OBJECT("object")`

        - `Optional<Properties> properties`

        - `Optional<List<String>> required`

      - `String name`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<String> description`

        Description of what this tool does.

        Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

      - `Optional<List<InputExample>> inputExamples`

      - `Optional<Boolean> strict`

      - `Optional<Type> type`

        - `CUSTOM("custom")`

    - `class BetaToolBash20241022:`

      - `JsonValue; name "bash"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `BASH("bash")`

      - `JsonValue; type "bash_20241022"constant`

        - `BASH_20241022("bash_20241022")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<List<InputExample>> inputExamples`

      - `Optional<Boolean> strict`

    - `class BetaToolBash20250124:`

      - `JsonValue; name "bash"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `BASH("bash")`

      - `JsonValue; type "bash_20250124"constant`

        - `BASH_20250124("bash_20250124")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<List<InputExample>> inputExamples`

      - `Optional<Boolean> strict`

    - `class BetaCodeExecutionTool20250522:`

      - `JsonValue; name "code_execution"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `CODE_EXECUTION("code_execution")`

      - `JsonValue; type "code_execution_20250522"constant`

        - `CODE_EXECUTION_20250522("code_execution_20250522")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<Boolean> strict`

    - `class BetaCodeExecutionTool20250825:`

      - `JsonValue; name "code_execution"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `CODE_EXECUTION("code_execution")`

      - `JsonValue; type "code_execution_20250825"constant`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<Boolean> strict`

    - `class BetaToolComputerUse20241022:`

      - `long displayHeightPx`

        The height of the display in pixels.

      - `long displayWidthPx`

        The width of the display in pixels.

      - `JsonValue; name "computer"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `COMPUTER("computer")`

      - `JsonValue; type "computer_20241022"constant`

        - `COMPUTER_20241022("computer_20241022")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<Long> displayNumber`

        The X11 display number (e.g. 0, 1) for the display.

      - `Optional<List<InputExample>> inputExamples`

      - `Optional<Boolean> strict`

    - `class BetaMemoryTool20250818:`

      - `JsonValue; name "memory"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `MEMORY("memory")`

      - `JsonValue; type "memory_20250818"constant`

        - `MEMORY_20250818("memory_20250818")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<List<InputExample>> inputExamples`

      - `Optional<Boolean> strict`

    - `class BetaToolComputerUse20250124:`

      - `long displayHeightPx`

        The height of the display in pixels.

      - `long displayWidthPx`

        The width of the display in pixels.

      - `JsonValue; name "computer"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `COMPUTER("computer")`

      - `JsonValue; type "computer_20250124"constant`

        - `COMPUTER_20250124("computer_20250124")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<Long> displayNumber`

        The X11 display number (e.g. 0, 1) for the display.

      - `Optional<List<InputExample>> inputExamples`

      - `Optional<Boolean> strict`

    - `class BetaToolTextEditor20241022:`

      - `JsonValue; name "str_replace_editor"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_EDITOR("str_replace_editor")`

      - `JsonValue; type "text_editor_20241022"constant`

        - `TEXT_EDITOR_20241022("text_editor_20241022")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<List<InputExample>> inputExamples`

      - `Optional<Boolean> strict`

    - `class BetaToolComputerUse20251124:`

      - `long displayHeightPx`

        The height of the display in pixels.

      - `long displayWidthPx`

        The width of the display in pixels.

      - `JsonValue; name "computer"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `COMPUTER("computer")`

      - `JsonValue; type "computer_20251124"constant`

        - `COMPUTER_20251124("computer_20251124")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<Long> displayNumber`

        The X11 display number (e.g. 0, 1) for the display.

      - `Optional<Boolean> enableZoom`

        Whether to enable an action to take a zoomed-in screenshot of the screen.

      - `Optional<List<InputExample>> inputExamples`

      - `Optional<Boolean> strict`

    - `class BetaToolTextEditor20250124:`

      - `JsonValue; name "str_replace_editor"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_EDITOR("str_replace_editor")`

      - `JsonValue; type "text_editor_20250124"constant`

        - `TEXT_EDITOR_20250124("text_editor_20250124")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<List<InputExample>> inputExamples`

      - `Optional<Boolean> strict`

    - `class BetaToolTextEditor20250429:`

      - `JsonValue; name "str_replace_based_edit_tool"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

      - `JsonValue; type "text_editor_20250429"constant`

        - `TEXT_EDITOR_20250429("text_editor_20250429")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<List<InputExample>> inputExamples`

      - `Optional<Boolean> strict`

    - `class BetaToolTextEditor20250728:`

      - `JsonValue; name "str_replace_based_edit_tool"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

      - `JsonValue; type "text_editor_20250728"constant`

        - `TEXT_EDITOR_20250728("text_editor_20250728")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<List<InputExample>> inputExamples`

      - `Optional<Long> maxCharacters`

        Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

      - `Optional<Boolean> strict`

    - `class BetaWebSearchTool20250305:`

      - `JsonValue; name "web_search"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `WEB_SEARCH("web_search")`

      - `JsonValue; type "web_search_20250305"constant`

        - `WEB_SEARCH_20250305("web_search_20250305")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<List<String>> allowedDomains`

        If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

      - `Optional<List<String>> blockedDomains`

        If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<Long> maxUses`

        Maximum number of times the tool can be used in the API request.

      - `Optional<Boolean> strict`

      - `Optional<UserLocation> userLocation`

        Parameters for the user's location. Used to provide more relevant search results.

        - `JsonValue; type "approximate"constant`

          - `APPROXIMATE("approximate")`

        - `Optional<String> city`

          The city of the user.

        - `Optional<String> country`

          The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

        - `Optional<String> region`

          The region of the user.

        - `Optional<String> timezone`

          The [IANA timezone](https://nodatime.org/TimeZones) of the user.

    - `class BetaWebFetchTool20250910:`

      - `JsonValue; name "web_fetch"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `WEB_FETCH("web_fetch")`

      - `JsonValue; type "web_fetch_20250910"constant`

        - `WEB_FETCH_20250910("web_fetch_20250910")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<List<String>> allowedDomains`

        List of domains to allow fetching from

      - `Optional<List<String>> blockedDomains`

        List of domains to block fetching from

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<BetaCitationsConfigParam> citations`

        Citations configuration for fetched documents. Citations are disabled by default.

        - `Optional<Boolean> enabled`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<Long> maxContentTokens`

        Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

      - `Optional<Long> maxUses`

        Maximum number of times the tool can be used in the API request.

      - `Optional<Boolean> strict`

    - `class BetaToolSearchToolBm25_20251119:`

      - `JsonValue; name "tool_search_tool_bm25"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

      - `Type type`

        - `TOOL_SEARCH_TOOL_BM25_20251119("tool_search_tool_bm25_20251119")`

        - `TOOL_SEARCH_TOOL_BM25("tool_search_tool_bm25")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<Boolean> strict`

    - `class BetaToolSearchToolRegex20251119:`

      - `JsonValue; name "tool_search_tool_regex"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

      - `Type type`

        - `TOOL_SEARCH_TOOL_REGEX_20251119("tool_search_tool_regex_20251119")`

        - `TOOL_SEARCH_TOOL_REGEX("tool_search_tool_regex")`

      - `Optional<List<AllowedCaller>> allowedCallers`

        - `DIRECT("direct")`

        - `CODE_EXECUTION_20250825("code_execution_20250825")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Boolean> deferLoading`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Optional<Boolean> strict`

    - `class BetaMcpToolset:`

      Configuration for a group of tools from an MCP server.

      Allows configuring enabled status and defer_loading for all tools
      from an MCP server, with optional per-tool overrides.

      - `String mcpServerName`

        Name of the MCP server to configure tools for

      - `JsonValue; type "mcp_toolset"constant`

        - `MCP_TOOLSET("mcp_toolset")`

      - `Optional<BetaCacheControlEphemeral> cacheControl`

        Create a cache control breakpoint at this content block.

        - `JsonValue; type "ephemeral"constant`

          - `EPHEMERAL("ephemeral")`

        - `Optional<Ttl> ttl`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `TTL_5M("5m")`

          - `TTL_1H("1h")`

      - `Optional<Configs> configs`

        Configuration overrides for specific tools, keyed by tool name

        - `Optional<Boolean> deferLoading`

        - `Optional<Boolean> enabled`

      - `Optional<BetaMcpToolDefaultConfig> defaultConfig`

        Default configuration applied to all tools from this server

        - `Optional<Boolean> deferLoading`

        - `Optional<Boolean> enabled`

### Returns

- `class BetaMessageTokensCount:`

  - `Optional<BetaCountTokensContextManagementResponse> contextManagement`

    Information about context management applied to the message.

    - `long originalInputTokens`

      The original token count before context management was applied

  - `long inputTokens`

    The total number of tokens across the provided list of messages, system prompt, and tools.

### Example

```java
package com.anthropic.example;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.BetaMessageTokensCount;
import com.anthropic.models.beta.messages.MessageCountTokensParams;
import com.anthropic.models.messages.Model;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCountTokensParams params = MessageCountTokensParams.builder()
            .addUserMessage("Hello, world")
            .model(Model.CLAUDE_OPUS_4_5_20251101)
            .build();
        BetaMessageTokensCount betaMessageTokensCount = client.beta().messages().countTokens(params);
    }
}
```
