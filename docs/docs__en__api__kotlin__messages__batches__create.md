## Create

`messages().batches().create(BatchCreateParamsparams, RequestOptionsrequestOptions = RequestOptions.none()) : MessageBatch`

**post** `/v1/messages/batches`

Send a batch of Message creation requests.

The Message Batches API can be used to process multiple Messages API requests at once. Once a Message Batch is created, it begins processing immediately. Batches can take up to 24 hours to complete.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchCreateParams`

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

      - `messages: List<MessageParam>`

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

          - `List<ContentBlockParam>`

            - `class TextBlockParam:`

              - `text: String`

              - `type: JsonValue; "text"constant`

                - `TEXT("text")`

              - `cacheControl: Optional<CacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<List<TextCitationParam>>`

                - `class CitationCharLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endCharIndex: Long`

                  - `startCharIndex: Long`

                  - `type: JsonValue; "char_location"constant`

                    - `CHAR_LOCATION("char_location")`

                - `class CitationPageLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endPageNumber: Long`

                  - `startPageNumber: Long`

                  - `type: JsonValue; "page_location"constant`

                    - `PAGE_LOCATION("page_location")`

                - `class CitationContentBlockLocationParam:`

                  - `citedText: String`

                  - `documentIndex: Long`

                  - `documentTitle: Optional<String>`

                  - `endBlockIndex: Long`

                  - `startBlockIndex: Long`

                  - `type: JsonValue; "content_block_location"constant`

                    - `CONTENT_BLOCK_LOCATION("content_block_location")`

                - `class CitationWebSearchResultLocationParam:`

                  - `citedText: String`

                  - `encryptedIndex: String`

                  - `title: Optional<String>`

                  - `type: JsonValue; "web_search_result_location"constant`

                    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                  - `url: String`

                - `class CitationSearchResultLocationParam:`

                  - `citedText: String`

                  - `endBlockIndex: Long`

                  - `searchResultIndex: Long`

                  - `source: String`

                  - `startBlockIndex: Long`

                  - `title: Optional<String>`

                  - `type: JsonValue; "search_result_location"constant`

                    - `SEARCH_RESULT_LOCATION("search_result_location")`

            - `class ImageBlockParam:`

              - `source: Source`

                - `class Base64ImageSource:`

                  - `data: String`

                  - `mediaType: MediaType`

                    - `IMAGE_JPEG("image/jpeg")`

                    - `IMAGE_PNG("image/png")`

                    - `IMAGE_GIF("image/gif")`

                    - `IMAGE_WEBP("image/webp")`

                  - `type: JsonValue; "base64"constant`

                    - `BASE64("base64")`

                - `class UrlImageSource:`

                  - `type: JsonValue; "url"constant`

                    - `URL("url")`

                  - `url: String`

              - `type: JsonValue; "image"constant`

                - `IMAGE("image")`

              - `cacheControl: Optional<CacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

            - `class DocumentBlockParam:`

              - `source: Source`

                - `class Base64PdfSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "application/pdf"constant`

                    - `APPLICATION_PDF("application/pdf")`

                  - `type: JsonValue; "base64"constant`

                    - `BASE64("base64")`

                - `class PlainTextSource:`

                  - `data: String`

                  - `mediaType: JsonValue; "text/plain"constant`

                    - `TEXT_PLAIN("text/plain")`

                  - `type: JsonValue; "text"constant`

                    - `TEXT("text")`

                - `class ContentBlockSource:`

                  - `content: Content`

                    - `String`

                    - `List<ContentBlockSourceContent>`

                      - `class TextBlockParam:`

                        - `text: String`

                        - `type: JsonValue; "text"constant`

                          - `TEXT("text")`

                        - `cacheControl: Optional<CacheControlEphemeral>`

                          Create a cache control breakpoint at this content block.

                          - `type: JsonValue; "ephemeral"constant`

                            - `EPHEMERAL("ephemeral")`

                          - `ttl: Optional<Ttl>`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `TTL_5M("5m")`

                            - `TTL_1H("1h")`

                        - `citations: Optional<List<TextCitationParam>>`

                          - `class CitationCharLocationParam:`

                            - `citedText: String`

                            - `documentIndex: Long`

                            - `documentTitle: Optional<String>`

                            - `endCharIndex: Long`

                            - `startCharIndex: Long`

                            - `type: JsonValue; "char_location"constant`

                              - `CHAR_LOCATION("char_location")`

                          - `class CitationPageLocationParam:`

                            - `citedText: String`

                            - `documentIndex: Long`

                            - `documentTitle: Optional<String>`

                            - `endPageNumber: Long`

                            - `startPageNumber: Long`

                            - `type: JsonValue; "page_location"constant`

                              - `PAGE_LOCATION("page_location")`

                          - `class CitationContentBlockLocationParam:`

                            - `citedText: String`

                            - `documentIndex: Long`

                            - `documentTitle: Optional<String>`

                            - `endBlockIndex: Long`

                            - `startBlockIndex: Long`

                            - `type: JsonValue; "content_block_location"constant`

                              - `CONTENT_BLOCK_LOCATION("content_block_location")`

                          - `class CitationWebSearchResultLocationParam:`

                            - `citedText: String`

                            - `encryptedIndex: String`

                            - `title: Optional<String>`

                            - `type: JsonValue; "web_search_result_location"constant`

                              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                            - `url: String`

                          - `class CitationSearchResultLocationParam:`

                            - `citedText: String`

                            - `endBlockIndex: Long`

                            - `searchResultIndex: Long`

                            - `source: String`

                            - `startBlockIndex: Long`

                            - `title: Optional<String>`

                            - `type: JsonValue; "search_result_location"constant`

                              - `SEARCH_RESULT_LOCATION("search_result_location")`

                      - `class ImageBlockParam:`

                        - `source: Source`

                          - `class Base64ImageSource:`

                            - `data: String`

                            - `mediaType: MediaType`

                              - `IMAGE_JPEG("image/jpeg")`

                              - `IMAGE_PNG("image/png")`

                              - `IMAGE_GIF("image/gif")`

                              - `IMAGE_WEBP("image/webp")`

                            - `type: JsonValue; "base64"constant`

                              - `BASE64("base64")`

                          - `class UrlImageSource:`

                            - `type: JsonValue; "url"constant`

                              - `URL("url")`

                            - `url: String`

                        - `type: JsonValue; "image"constant`

                          - `IMAGE("image")`

                        - `cacheControl: Optional<CacheControlEphemeral>`

                          Create a cache control breakpoint at this content block.

                          - `type: JsonValue; "ephemeral"constant`

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

                - `class UrlPdfSource:`

                  - `type: JsonValue; "url"constant`

                    - `URL("url")`

                  - `url: String`

              - `type: JsonValue; "document"constant`

                - `DOCUMENT("document")`

              - `cacheControl: Optional<CacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<CitationsConfigParam>`

                - `enabled: Optional<Boolean>`

              - `context: Optional<String>`

              - `title: Optional<String>`

            - `class SearchResultBlockParam:`

              - `content: List<TextBlockParam>`

                - `text: String`

                - `type: JsonValue; "text"constant`

                  - `TEXT("text")`

                - `cacheControl: Optional<CacheControlEphemeral>`

                  Create a cache control breakpoint at this content block.

                  - `type: JsonValue; "ephemeral"constant`

                    - `EPHEMERAL("ephemeral")`

                  - `ttl: Optional<Ttl>`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `TTL_5M("5m")`

                    - `TTL_1H("1h")`

                - `citations: Optional<List<TextCitationParam>>`

                  - `class CitationCharLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endCharIndex: Long`

                    - `startCharIndex: Long`

                    - `type: JsonValue; "char_location"constant`

                      - `CHAR_LOCATION("char_location")`

                  - `class CitationPageLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endPageNumber: Long`

                    - `startPageNumber: Long`

                    - `type: JsonValue; "page_location"constant`

                      - `PAGE_LOCATION("page_location")`

                  - `class CitationContentBlockLocationParam:`

                    - `citedText: String`

                    - `documentIndex: Long`

                    - `documentTitle: Optional<String>`

                    - `endBlockIndex: Long`

                    - `startBlockIndex: Long`

                    - `type: JsonValue; "content_block_location"constant`

                      - `CONTENT_BLOCK_LOCATION("content_block_location")`

                  - `class CitationWebSearchResultLocationParam:`

                    - `citedText: String`

                    - `encryptedIndex: String`

                    - `title: Optional<String>`

                    - `type: JsonValue; "web_search_result_location"constant`

                      - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                    - `url: String`

                  - `class CitationSearchResultLocationParam:`

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

              - `cacheControl: Optional<CacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

              - `citations: Optional<CitationsConfigParam>`

                - `enabled: Optional<Boolean>`

            - `class ThinkingBlockParam:`

              - `signature: String`

              - `thinking: String`

              - `type: JsonValue; "thinking"constant`

                - `THINKING("thinking")`

            - `class RedactedThinkingBlockParam:`

              - `data: String`

              - `type: JsonValue; "redacted_thinking"constant`

                - `REDACTED_THINKING("redacted_thinking")`

            - `class ToolUseBlockParam:`

              - `id: String`

              - `input: Input`

              - `name: String`

              - `type: JsonValue; "tool_use"constant`

                - `TOOL_USE("tool_use")`

              - `cacheControl: Optional<CacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

            - `class ToolResultBlockParam:`

              - `toolUseId: String`

              - `type: JsonValue; "tool_result"constant`

                - `TOOL_RESULT("tool_result")`

              - `cacheControl: Optional<CacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

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

                  - `class TextBlockParam:`

                    - `text: String`

                    - `type: JsonValue; "text"constant`

                      - `TEXT("text")`

                    - `cacheControl: Optional<CacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                    - `citations: Optional<List<TextCitationParam>>`

                      - `class CitationCharLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endCharIndex: Long`

                        - `startCharIndex: Long`

                        - `type: JsonValue; "char_location"constant`

                          - `CHAR_LOCATION("char_location")`

                      - `class CitationPageLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endPageNumber: Long`

                        - `startPageNumber: Long`

                        - `type: JsonValue; "page_location"constant`

                          - `PAGE_LOCATION("page_location")`

                      - `class CitationContentBlockLocationParam:`

                        - `citedText: String`

                        - `documentIndex: Long`

                        - `documentTitle: Optional<String>`

                        - `endBlockIndex: Long`

                        - `startBlockIndex: Long`

                        - `type: JsonValue; "content_block_location"constant`

                          - `CONTENT_BLOCK_LOCATION("content_block_location")`

                      - `class CitationWebSearchResultLocationParam:`

                        - `citedText: String`

                        - `encryptedIndex: String`

                        - `title: Optional<String>`

                        - `type: JsonValue; "web_search_result_location"constant`

                          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                        - `url: String`

                      - `class CitationSearchResultLocationParam:`

                        - `citedText: String`

                        - `endBlockIndex: Long`

                        - `searchResultIndex: Long`

                        - `source: String`

                        - `startBlockIndex: Long`

                        - `title: Optional<String>`

                        - `type: JsonValue; "search_result_location"constant`

                          - `SEARCH_RESULT_LOCATION("search_result_location")`

                  - `class ImageBlockParam:`

                    - `source: Source`

                      - `class Base64ImageSource:`

                        - `data: String`

                        - `mediaType: MediaType`

                          - `IMAGE_JPEG("image/jpeg")`

                          - `IMAGE_PNG("image/png")`

                          - `IMAGE_GIF("image/gif")`

                          - `IMAGE_WEBP("image/webp")`

                        - `type: JsonValue; "base64"constant`

                          - `BASE64("base64")`

                      - `class UrlImageSource:`

                        - `type: JsonValue; "url"constant`

                          - `URL("url")`

                        - `url: String`

                    - `type: JsonValue; "image"constant`

                      - `IMAGE("image")`

                    - `cacheControl: Optional<CacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                  - `class SearchResultBlockParam:`

                    - `content: List<TextBlockParam>`

                      - `text: String`

                      - `type: JsonValue; "text"constant`

                        - `TEXT("text")`

                      - `cacheControl: Optional<CacheControlEphemeral>`

                        Create a cache control breakpoint at this content block.

                        - `type: JsonValue; "ephemeral"constant`

                          - `EPHEMERAL("ephemeral")`

                        - `ttl: Optional<Ttl>`

                          The time-to-live for the cache control breakpoint.

                          This may be one the following values:

                          - `5m`: 5 minutes
                          - `1h`: 1 hour

                          Defaults to `5m`.

                          - `TTL_5M("5m")`

                          - `TTL_1H("1h")`

                      - `citations: Optional<List<TextCitationParam>>`

                        - `class CitationCharLocationParam:`

                          - `citedText: String`

                          - `documentIndex: Long`

                          - `documentTitle: Optional<String>`

                          - `endCharIndex: Long`

                          - `startCharIndex: Long`

                          - `type: JsonValue; "char_location"constant`

                            - `CHAR_LOCATION("char_location")`

                        - `class CitationPageLocationParam:`

                          - `citedText: String`

                          - `documentIndex: Long`

                          - `documentTitle: Optional<String>`

                          - `endPageNumber: Long`

                          - `startPageNumber: Long`

                          - `type: JsonValue; "page_location"constant`

                            - `PAGE_LOCATION("page_location")`

                        - `class CitationContentBlockLocationParam:`

                          - `citedText: String`

                          - `documentIndex: Long`

                          - `documentTitle: Optional<String>`

                          - `endBlockIndex: Long`

                          - `startBlockIndex: Long`

                          - `type: JsonValue; "content_block_location"constant`

                            - `CONTENT_BLOCK_LOCATION("content_block_location")`

                        - `class CitationWebSearchResultLocationParam:`

                          - `citedText: String`

                          - `encryptedIndex: String`

                          - `title: Optional<String>`

                          - `type: JsonValue; "web_search_result_location"constant`

                            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                          - `url: String`

                        - `class CitationSearchResultLocationParam:`

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

                    - `cacheControl: Optional<CacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                    - `citations: Optional<CitationsConfigParam>`

                      - `enabled: Optional<Boolean>`

                  - `class DocumentBlockParam:`

                    - `source: Source`

                      - `class Base64PdfSource:`

                        - `data: String`

                        - `mediaType: JsonValue; "application/pdf"constant`

                          - `APPLICATION_PDF("application/pdf")`

                        - `type: JsonValue; "base64"constant`

                          - `BASE64("base64")`

                      - `class PlainTextSource:`

                        - `data: String`

                        - `mediaType: JsonValue; "text/plain"constant`

                          - `TEXT_PLAIN("text/plain")`

                        - `type: JsonValue; "text"constant`

                          - `TEXT("text")`

                      - `class ContentBlockSource:`

                        - `content: Content`

                          - `String`

                          - `List<ContentBlockSourceContent>`

                            - `class TextBlockParam:`

                              - `text: String`

                              - `type: JsonValue; "text"constant`

                                - `TEXT("text")`

                              - `cacheControl: Optional<CacheControlEphemeral>`

                                Create a cache control breakpoint at this content block.

                                - `type: JsonValue; "ephemeral"constant`

                                  - `EPHEMERAL("ephemeral")`

                                - `ttl: Optional<Ttl>`

                                  The time-to-live for the cache control breakpoint.

                                  This may be one the following values:

                                  - `5m`: 5 minutes
                                  - `1h`: 1 hour

                                  Defaults to `5m`.

                                  - `TTL_5M("5m")`

                                  - `TTL_1H("1h")`

                              - `citations: Optional<List<TextCitationParam>>`

                                - `class CitationCharLocationParam:`

                                  - `citedText: String`

                                  - `documentIndex: Long`

                                  - `documentTitle: Optional<String>`

                                  - `endCharIndex: Long`

                                  - `startCharIndex: Long`

                                  - `type: JsonValue; "char_location"constant`

                                    - `CHAR_LOCATION("char_location")`

                                - `class CitationPageLocationParam:`

                                  - `citedText: String`

                                  - `documentIndex: Long`

                                  - `documentTitle: Optional<String>`

                                  - `endPageNumber: Long`

                                  - `startPageNumber: Long`

                                  - `type: JsonValue; "page_location"constant`

                                    - `PAGE_LOCATION("page_location")`

                                - `class CitationContentBlockLocationParam:`

                                  - `citedText: String`

                                  - `documentIndex: Long`

                                  - `documentTitle: Optional<String>`

                                  - `endBlockIndex: Long`

                                  - `startBlockIndex: Long`

                                  - `type: JsonValue; "content_block_location"constant`

                                    - `CONTENT_BLOCK_LOCATION("content_block_location")`

                                - `class CitationWebSearchResultLocationParam:`

                                  - `citedText: String`

                                  - `encryptedIndex: String`

                                  - `title: Optional<String>`

                                  - `type: JsonValue; "web_search_result_location"constant`

                                    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                                  - `url: String`

                                - `class CitationSearchResultLocationParam:`

                                  - `citedText: String`

                                  - `endBlockIndex: Long`

                                  - `searchResultIndex: Long`

                                  - `source: String`

                                  - `startBlockIndex: Long`

                                  - `title: Optional<String>`

                                  - `type: JsonValue; "search_result_location"constant`

                                    - `SEARCH_RESULT_LOCATION("search_result_location")`

                            - `class ImageBlockParam:`

                              - `source: Source`

                                - `class Base64ImageSource:`

                                  - `data: String`

                                  - `mediaType: MediaType`

                                    - `IMAGE_JPEG("image/jpeg")`

                                    - `IMAGE_PNG("image/png")`

                                    - `IMAGE_GIF("image/gif")`

                                    - `IMAGE_WEBP("image/webp")`

                                  - `type: JsonValue; "base64"constant`

                                    - `BASE64("base64")`

                                - `class UrlImageSource:`

                                  - `type: JsonValue; "url"constant`

                                    - `URL("url")`

                                  - `url: String`

                              - `type: JsonValue; "image"constant`

                                - `IMAGE("image")`

                              - `cacheControl: Optional<CacheControlEphemeral>`

                                Create a cache control breakpoint at this content block.

                                - `type: JsonValue; "ephemeral"constant`

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

                      - `class UrlPdfSource:`

                        - `type: JsonValue; "url"constant`

                          - `URL("url")`

                        - `url: String`

                    - `type: JsonValue; "document"constant`

                      - `DOCUMENT("document")`

                    - `cacheControl: Optional<CacheControlEphemeral>`

                      Create a cache control breakpoint at this content block.

                      - `type: JsonValue; "ephemeral"constant`

                        - `EPHEMERAL("ephemeral")`

                      - `ttl: Optional<Ttl>`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `TTL_5M("5m")`

                        - `TTL_1H("1h")`

                    - `citations: Optional<CitationsConfigParam>`

                      - `enabled: Optional<Boolean>`

                    - `context: Optional<String>`

                    - `title: Optional<String>`

              - `isError: Optional<Boolean>`

            - `class ServerToolUseBlockParam:`

              - `id: String`

              - `input: Input`

              - `name: JsonValue; "web_search"constant`

                - `WEB_SEARCH("web_search")`

              - `type: JsonValue; "server_tool_use"constant`

                - `SERVER_TOOL_USE("server_tool_use")`

              - `cacheControl: Optional<CacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

                  - `EPHEMERAL("ephemeral")`

                - `ttl: Optional<Ttl>`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `TTL_5M("5m")`

                  - `TTL_1H("1h")`

            - `class WebSearchToolResultBlockParam:`

              - `content: WebSearchToolResultBlockParamContent`

                - `List<WebSearchResultBlockParam>`

                  - `encryptedContent: String`

                  - `title: String`

                  - `type: JsonValue; "web_search_result"constant`

                    - `WEB_SEARCH_RESULT("web_search_result")`

                  - `url: String`

                  - `pageAge: Optional<String>`

                - `class WebSearchToolRequestError:`

                  - `errorCode: ErrorCode`

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

              - `cacheControl: Optional<CacheControlEphemeral>`

                Create a cache control breakpoint at this content block.

                - `type: JsonValue; "ephemeral"constant`

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

      - `metadata: Optional<Metadata>`

        An object describing metadata about the request.

        - `userId: Optional<String>`

          An external identifier for the user who is associated with the request.

          This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

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

        - `List<TextBlockParam>`

          - `text: String`

          - `type: JsonValue; "text"constant`

            - `TEXT("text")`

          - `cacheControl: Optional<CacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `citations: Optional<List<TextCitationParam>>`

            - `class CitationCharLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class CitationPageLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class CitationContentBlockLocationParam:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class CitationWebSearchResultLocationParam:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class CitationSearchResultLocationParam:`

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

      - `thinking: Optional<ThinkingConfigParam>`

        Configuration for enabling Claude's extended thinking.

        When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

        See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

        - `class ThinkingConfigEnabled:`

          - `budgetTokens: Long`

            Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

            Must be ≥1024 and less than `max_tokens`.

            See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

          - `type: JsonValue; "enabled"constant`

            - `ENABLED("enabled")`

        - `class ThinkingConfigDisabled:`

          - `type: JsonValue; "disabled"constant`

            - `DISABLED("disabled")`

      - `toolChoice: Optional<ToolChoice>`

        How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

        - `class ToolChoiceAuto:`

          The model will automatically decide whether to use tools.

          - `type: JsonValue; "auto"constant`

            - `AUTO("auto")`

          - `disableParallelToolUse: Optional<Boolean>`

            Whether to disable parallel tool use.

            Defaults to `false`. If set to `true`, the model will output at most one tool use.

        - `class ToolChoiceAny:`

          The model will use any available tools.

          - `type: JsonValue; "any"constant`

            - `ANY("any")`

          - `disableParallelToolUse: Optional<Boolean>`

            Whether to disable parallel tool use.

            Defaults to `false`. If set to `true`, the model will output exactly one tool use.

        - `class ToolChoiceTool:`

          The model will use the specified tool with `tool_choice.name`.

          - `name: String`

            The name of the tool to use.

          - `type: JsonValue; "tool"constant`

            - `TOOL("tool")`

          - `disableParallelToolUse: Optional<Boolean>`

            Whether to disable parallel tool use.

            Defaults to `false`. If set to `true`, the model will output exactly one tool use.

        - `class ToolChoiceNone:`

          The model will not be allowed to use tools.

          - `type: JsonValue; "none"constant`

            - `NONE("none")`

      - `tools: Optional<List<ToolUnion>>`

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

        - `class Tool:`

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

          - `cacheControl: Optional<CacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `description: Optional<String>`

            Description of what this tool does.

            Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

          - `type: Optional<Type>`

            - `CUSTOM("custom")`

        - `class ToolBash20250124:`

          - `name: JsonValue; "bash"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `BASH("bash")`

          - `type: JsonValue; "bash_20250124"constant`

            - `BASH_20250124("bash_20250124")`

          - `cacheControl: Optional<CacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class ToolTextEditor20250124:`

          - `name: JsonValue; "str_replace_editor"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `STR_REPLACE_EDITOR("str_replace_editor")`

          - `type: JsonValue; "text_editor_20250124"constant`

            - `TEXT_EDITOR_20250124("text_editor_20250124")`

          - `cacheControl: Optional<CacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class ToolTextEditor20250429:`

          - `name: JsonValue; "str_replace_based_edit_tool"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

          - `type: JsonValue; "text_editor_20250429"constant`

            - `TEXT_EDITOR_20250429("text_editor_20250429")`

          - `cacheControl: Optional<CacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

        - `class ToolTextEditor20250728:`

          - `name: JsonValue; "str_replace_based_edit_tool"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

          - `type: JsonValue; "text_editor_20250728"constant`

            - `TEXT_EDITOR_20250728("text_editor_20250728")`

          - `cacheControl: Optional<CacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `maxCharacters: Optional<Long>`

            Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

        - `class WebSearchTool20250305:`

          - `name: JsonValue; "web_search"constant`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `WEB_SEARCH("web_search")`

          - `type: JsonValue; "web_search_20250305"constant`

            - `WEB_SEARCH_20250305("web_search_20250305")`

          - `allowedDomains: Optional<List<String>>`

            If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

          - `blockedDomains: Optional<List<String>>`

            If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

          - `cacheControl: Optional<CacheControlEphemeral>`

            Create a cache control breakpoint at this content block.

            - `type: JsonValue; "ephemeral"constant`

              - `EPHEMERAL("ephemeral")`

            - `ttl: Optional<Ttl>`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `TTL_5M("5m")`

              - `TTL_1H("1h")`

          - `maxUses: Optional<Long>`

            Maximum number of times the tool can be used in the API request.

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

      - `topK: Optional<Long>`

        Only sample from the top K options for each subsequent token.

        Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

        Recommended for advanced use cases only. You usually only need to use `temperature`.

      - `topP: Optional<Double>`

        Use nucleus sampling.

        In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

        Recommended for advanced use cases only. You usually only need to use `temperature`.

### Returns

- `class MessageBatch:`

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

  - `requestCounts: MessageBatchRequestCounts`

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
import com.anthropic.models.messages.Model
import com.anthropic.models.messages.batches.BatchCreateParams
import com.anthropic.models.messages.batches.MessageBatch

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
    val messageBatch: MessageBatch = client.messages().batches().create(params)
}
```
