# Messages

## Create

`messages().create(MessageCreateParamsparams, RequestOptionsrequestOptions = RequestOptions.none()) : Message`

**post** `/v1/messages`

Send a structured list of input messages with text and/or image content, and the model will generate the next message in the conversation.

The Messages API can be used for either single queries or stateless multi-turn conversations.

Learn more about the Messages API in our [user guide](https://docs.claude.com/en/docs/initial-setup)

### Parameters

- `params: MessageCreateParams`

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

  - `metadata: Optional<Metadata>`

    An object describing metadata about the request.

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

  - `toolChoice: Optional<ToolChoice>`

    How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

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

- `class Message:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `content: List<ContentBlock>`

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

    - `class TextBlock:`

      - `citations: Optional<List<TextCitation>>`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `class CitationCharLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endCharIndex: Long`

          - `fileId: Optional<String>`

          - `startCharIndex: Long`

          - `type: JsonValue; "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class CitationPageLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endPageNumber: Long`

          - `fileId: Optional<String>`

          - `startPageNumber: Long`

          - `type: JsonValue; "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class CitationContentBlockLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endBlockIndex: Long`

          - `fileId: Optional<String>`

          - `startBlockIndex: Long`

          - `type: JsonValue; "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class CitationsWebSearchResultLocation:`

          - `citedText: String`

          - `encryptedIndex: String`

          - `title: Optional<String>`

          - `type: JsonValue; "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `url: String`

        - `class CitationsSearchResultLocation:`

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

    - `class ThinkingBlock:`

      - `signature: String`

      - `thinking: String`

      - `type: JsonValue; "thinking"constant`

        - `THINKING("thinking")`

    - `class RedactedThinkingBlock:`

      - `data: String`

      - `type: JsonValue; "redacted_thinking"constant`

        - `REDACTED_THINKING("redacted_thinking")`

    - `class ToolUseBlock:`

      - `id: String`

      - `input: Input`

      - `name: String`

      - `type: JsonValue; "tool_use"constant`

        - `TOOL_USE("tool_use")`

    - `class ServerToolUseBlock:`

      - `id: String`

      - `input: Input`

      - `name: JsonValue; "web_search"constant`

        - `WEB_SEARCH("web_search")`

      - `type: JsonValue; "server_tool_use"constant`

        - `SERVER_TOOL_USE("server_tool_use")`

    - `class WebSearchToolResultBlock:`

      - `content: WebSearchToolResultBlockContent`

        - `class WebSearchToolResultError:`

          - `errorCode: ErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `MAX_USES_EXCEEDED("max_uses_exceeded")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `QUERY_TOO_LONG("query_too_long")`

          - `type: JsonValue; "web_search_tool_result_error"constant`

            - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

        - `List<WebSearchResultBlock>`

          - `encryptedContent: String`

          - `pageAge: Optional<String>`

          - `title: String`

          - `type: JsonValue; "web_search_result"constant`

            - `WEB_SEARCH_RESULT("web_search_result")`

          - `url: String`

      - `toolUseId: String`

      - `type: JsonValue; "web_search_tool_result"constant`

        - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

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

  - `stopReason: Optional<StopReason>`

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

  - `stopSequence: Optional<String>`

    Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was generated.

  - `type: JsonValue; "message"constant`

    Object type.

    For Messages, this is always `"message"`.

    - `MESSAGE("message")`

  - `usage: Usage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cacheCreation: Optional<CacheCreation>`

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

    - `serverToolUse: Optional<ServerToolUsage>`

      The number of server tool requests.

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
import com.anthropic.models.messages.Message
import com.anthropic.models.messages.MessageCreateParams
import com.anthropic.models.messages.Model

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val params: MessageCreateParams = MessageCreateParams.builder()
        .maxTokens(1024L)
        .addUserMessage("Hello, world")
        .model(Model.CLAUDE_OPUS_4_5_20251101)
        .build()
    val message: Message = client.messages().create(params)
}
```

## Count Tokens

`messages().countTokens(MessageCountTokensParamsparams, RequestOptionsrequestOptions = RequestOptions.none()) : MessageTokensCount`

**post** `/v1/messages/count_tokens`

Count the number of tokens in a Message.

The Token Count API can be used to count the number of tokens in a Message, including tools, images, and documents, without creating it.

Learn more about token counting in our [user guide](https://docs.claude.com/en/docs/build-with-claude/token-counting)

### Parameters

- `params: MessageCountTokensParams`

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

  - `thinking: Optional<ThinkingConfigParam>`

    Configuration for enabling Claude's extended thinking.

    When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `toolChoice: Optional<ToolChoice>`

    How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `tools: Optional<List<MessageCountTokensTool>>`

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

### Returns

- `class MessageTokensCount:`

  - `inputTokens: Long`

    The total number of tokens across the provided list of messages, system prompt, and tools.

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.messages.MessageCountTokensParams
import com.anthropic.models.messages.MessageTokensCount
import com.anthropic.models.messages.Model

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val params: MessageCountTokensParams = MessageCountTokensParams.builder()
        .addUserMessage("Hello, world")
        .model(Model.CLAUDE_OPUS_4_5_20251101)
        .build()
    val messageTokensCount: MessageTokensCount = client.messages().countTokens(params)
}
```

## Domain Types

### Base64 Image Source

- `class Base64ImageSource:`

  - `data: String`

  - `mediaType: MediaType`

    - `IMAGE_JPEG("image/jpeg")`

    - `IMAGE_PNG("image/png")`

    - `IMAGE_GIF("image/gif")`

    - `IMAGE_WEBP("image/webp")`

  - `type: JsonValue; "base64"constant`

    - `BASE64("base64")`

### Base64 PDF Source

- `class Base64PdfSource:`

  - `data: String`

  - `mediaType: JsonValue; "application/pdf"constant`

    - `APPLICATION_PDF("application/pdf")`

  - `type: JsonValue; "base64"constant`

    - `BASE64("base64")`

### Cache Control Ephemeral

- `class CacheControlEphemeral:`

  - `type: JsonValue; "ephemeral"constant`

    - `EPHEMERAL("ephemeral")`

  - `ttl: Optional<Ttl>`

    The time-to-live for the cache control breakpoint.

    This may be one the following values:

    - `5m`: 5 minutes
    - `1h`: 1 hour

    Defaults to `5m`.

    - `TTL_5M("5m")`

    - `TTL_1H("1h")`

### Cache Creation

- `class CacheCreation:`

  - `ephemeral1hInputTokens: Long`

    The number of input tokens used to create the 1 hour cache entry.

  - `ephemeral5mInputTokens: Long`

    The number of input tokens used to create the 5 minute cache entry.

### Citation Char Location

- `class CitationCharLocation:`

  - `citedText: String`

  - `documentIndex: Long`

  - `documentTitle: Optional<String>`

  - `endCharIndex: Long`

  - `fileId: Optional<String>`

  - `startCharIndex: Long`

  - `type: JsonValue; "char_location"constant`

    - `CHAR_LOCATION("char_location")`

### Citation Char Location Param

- `class CitationCharLocationParam:`

  - `citedText: String`

  - `documentIndex: Long`

  - `documentTitle: Optional<String>`

  - `endCharIndex: Long`

  - `startCharIndex: Long`

  - `type: JsonValue; "char_location"constant`

    - `CHAR_LOCATION("char_location")`

### Citation Content Block Location

- `class CitationContentBlockLocation:`

  - `citedText: String`

  - `documentIndex: Long`

  - `documentTitle: Optional<String>`

  - `endBlockIndex: Long`

  - `fileId: Optional<String>`

  - `startBlockIndex: Long`

  - `type: JsonValue; "content_block_location"constant`

    - `CONTENT_BLOCK_LOCATION("content_block_location")`

### Citation Content Block Location Param

- `class CitationContentBlockLocationParam:`

  - `citedText: String`

  - `documentIndex: Long`

  - `documentTitle: Optional<String>`

  - `endBlockIndex: Long`

  - `startBlockIndex: Long`

  - `type: JsonValue; "content_block_location"constant`

    - `CONTENT_BLOCK_LOCATION("content_block_location")`

### Citation Page Location

- `class CitationPageLocation:`

  - `citedText: String`

  - `documentIndex: Long`

  - `documentTitle: Optional<String>`

  - `endPageNumber: Long`

  - `fileId: Optional<String>`

  - `startPageNumber: Long`

  - `type: JsonValue; "page_location"constant`

    - `PAGE_LOCATION("page_location")`

### Citation Page Location Param

- `class CitationPageLocationParam:`

  - `citedText: String`

  - `documentIndex: Long`

  - `documentTitle: Optional<String>`

  - `endPageNumber: Long`

  - `startPageNumber: Long`

  - `type: JsonValue; "page_location"constant`

    - `PAGE_LOCATION("page_location")`

### Citation Search Result Location Param

- `class CitationSearchResultLocationParam:`

  - `citedText: String`

  - `endBlockIndex: Long`

  - `searchResultIndex: Long`

  - `source: String`

  - `startBlockIndex: Long`

  - `title: Optional<String>`

  - `type: JsonValue; "search_result_location"constant`

    - `SEARCH_RESULT_LOCATION("search_result_location")`

### Citation Web Search Result Location Param

- `class CitationWebSearchResultLocationParam:`

  - `citedText: String`

  - `encryptedIndex: String`

  - `title: Optional<String>`

  - `type: JsonValue; "web_search_result_location"constant`

    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

  - `url: String`

### Citations Config Param

- `class CitationsConfigParam:`

  - `enabled: Optional<Boolean>`

### Citations Delta

- `class CitationsDelta:`

  - `citation: Citation`

    - `class CitationCharLocation:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endCharIndex: Long`

      - `fileId: Optional<String>`

      - `startCharIndex: Long`

      - `type: JsonValue; "char_location"constant`

        - `CHAR_LOCATION("char_location")`

    - `class CitationPageLocation:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endPageNumber: Long`

      - `fileId: Optional<String>`

      - `startPageNumber: Long`

      - `type: JsonValue; "page_location"constant`

        - `PAGE_LOCATION("page_location")`

    - `class CitationContentBlockLocation:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endBlockIndex: Long`

      - `fileId: Optional<String>`

      - `startBlockIndex: Long`

      - `type: JsonValue; "content_block_location"constant`

        - `CONTENT_BLOCK_LOCATION("content_block_location")`

    - `class CitationsWebSearchResultLocation:`

      - `citedText: String`

      - `encryptedIndex: String`

      - `title: Optional<String>`

      - `type: JsonValue; "web_search_result_location"constant`

        - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

      - `url: String`

    - `class CitationsSearchResultLocation:`

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

### Citations Search Result Location

- `class CitationsSearchResultLocation:`

  - `citedText: String`

  - `endBlockIndex: Long`

  - `searchResultIndex: Long`

  - `source: String`

  - `startBlockIndex: Long`

  - `title: Optional<String>`

  - `type: JsonValue; "search_result_location"constant`

    - `SEARCH_RESULT_LOCATION("search_result_location")`

### Citations Web Search Result Location

- `class CitationsWebSearchResultLocation:`

  - `citedText: String`

  - `encryptedIndex: String`

  - `title: Optional<String>`

  - `type: JsonValue; "web_search_result_location"constant`

    - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

  - `url: String`

### Content Block

- `class ContentBlock: A class that can be one of several variants.union`

  - `class TextBlock:`

    - `citations: Optional<List<TextCitation>>`

      Citations supporting the text block.

      The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

      - `class CitationCharLocation:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endCharIndex: Long`

        - `fileId: Optional<String>`

        - `startCharIndex: Long`

        - `type: JsonValue; "char_location"constant`

          - `CHAR_LOCATION("char_location")`

      - `class CitationPageLocation:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endPageNumber: Long`

        - `fileId: Optional<String>`

        - `startPageNumber: Long`

        - `type: JsonValue; "page_location"constant`

          - `PAGE_LOCATION("page_location")`

      - `class CitationContentBlockLocation:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endBlockIndex: Long`

        - `fileId: Optional<String>`

        - `startBlockIndex: Long`

        - `type: JsonValue; "content_block_location"constant`

          - `CONTENT_BLOCK_LOCATION("content_block_location")`

      - `class CitationsWebSearchResultLocation:`

        - `citedText: String`

        - `encryptedIndex: String`

        - `title: Optional<String>`

        - `type: JsonValue; "web_search_result_location"constant`

          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

        - `url: String`

      - `class CitationsSearchResultLocation:`

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

  - `class ThinkingBlock:`

    - `signature: String`

    - `thinking: String`

    - `type: JsonValue; "thinking"constant`

      - `THINKING("thinking")`

  - `class RedactedThinkingBlock:`

    - `data: String`

    - `type: JsonValue; "redacted_thinking"constant`

      - `REDACTED_THINKING("redacted_thinking")`

  - `class ToolUseBlock:`

    - `id: String`

    - `input: Input`

    - `name: String`

    - `type: JsonValue; "tool_use"constant`

      - `TOOL_USE("tool_use")`

  - `class ServerToolUseBlock:`

    - `id: String`

    - `input: Input`

    - `name: JsonValue; "web_search"constant`

      - `WEB_SEARCH("web_search")`

    - `type: JsonValue; "server_tool_use"constant`

      - `SERVER_TOOL_USE("server_tool_use")`

  - `class WebSearchToolResultBlock:`

    - `content: WebSearchToolResultBlockContent`

      - `class WebSearchToolResultError:`

        - `errorCode: ErrorCode`

          - `INVALID_TOOL_INPUT("invalid_tool_input")`

          - `UNAVAILABLE("unavailable")`

          - `MAX_USES_EXCEEDED("max_uses_exceeded")`

          - `TOO_MANY_REQUESTS("too_many_requests")`

          - `QUERY_TOO_LONG("query_too_long")`

        - `type: JsonValue; "web_search_tool_result_error"constant`

          - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

      - `List<WebSearchResultBlock>`

        - `encryptedContent: String`

        - `pageAge: Optional<String>`

        - `title: String`

        - `type: JsonValue; "web_search_result"constant`

          - `WEB_SEARCH_RESULT("web_search_result")`

        - `url: String`

    - `toolUseId: String`

    - `type: JsonValue; "web_search_tool_result"constant`

      - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

### Content Block Param

- `class ContentBlockParam: A class that can be one of several variants.union`

  Regular text content.

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

### Content Block Source

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

### Content Block Source Content

- `class ContentBlockSourceContent: A class that can be one of several variants.union`

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

### Document Block Param

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

### Image Block Param

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

### Input JSON Delta

- `class InputJsonDelta:`

  - `partialJson: String`

  - `type: JsonValue; "input_json_delta"constant`

    - `INPUT_JSON_DELTA("input_json_delta")`

### Message

- `class Message:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `content: List<ContentBlock>`

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

    - `class TextBlock:`

      - `citations: Optional<List<TextCitation>>`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `class CitationCharLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endCharIndex: Long`

          - `fileId: Optional<String>`

          - `startCharIndex: Long`

          - `type: JsonValue; "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class CitationPageLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endPageNumber: Long`

          - `fileId: Optional<String>`

          - `startPageNumber: Long`

          - `type: JsonValue; "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class CitationContentBlockLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endBlockIndex: Long`

          - `fileId: Optional<String>`

          - `startBlockIndex: Long`

          - `type: JsonValue; "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class CitationsWebSearchResultLocation:`

          - `citedText: String`

          - `encryptedIndex: String`

          - `title: Optional<String>`

          - `type: JsonValue; "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `url: String`

        - `class CitationsSearchResultLocation:`

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

    - `class ThinkingBlock:`

      - `signature: String`

      - `thinking: String`

      - `type: JsonValue; "thinking"constant`

        - `THINKING("thinking")`

    - `class RedactedThinkingBlock:`

      - `data: String`

      - `type: JsonValue; "redacted_thinking"constant`

        - `REDACTED_THINKING("redacted_thinking")`

    - `class ToolUseBlock:`

      - `id: String`

      - `input: Input`

      - `name: String`

      - `type: JsonValue; "tool_use"constant`

        - `TOOL_USE("tool_use")`

    - `class ServerToolUseBlock:`

      - `id: String`

      - `input: Input`

      - `name: JsonValue; "web_search"constant`

        - `WEB_SEARCH("web_search")`

      - `type: JsonValue; "server_tool_use"constant`

        - `SERVER_TOOL_USE("server_tool_use")`

    - `class WebSearchToolResultBlock:`

      - `content: WebSearchToolResultBlockContent`

        - `class WebSearchToolResultError:`

          - `errorCode: ErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `MAX_USES_EXCEEDED("max_uses_exceeded")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `QUERY_TOO_LONG("query_too_long")`

          - `type: JsonValue; "web_search_tool_result_error"constant`

            - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

        - `List<WebSearchResultBlock>`

          - `encryptedContent: String`

          - `pageAge: Optional<String>`

          - `title: String`

          - `type: JsonValue; "web_search_result"constant`

            - `WEB_SEARCH_RESULT("web_search_result")`

          - `url: String`

      - `toolUseId: String`

      - `type: JsonValue; "web_search_tool_result"constant`

        - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

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

  - `stopReason: Optional<StopReason>`

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

  - `stopSequence: Optional<String>`

    Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was generated.

  - `type: JsonValue; "message"constant`

    Object type.

    For Messages, this is always `"message"`.

    - `MESSAGE("message")`

  - `usage: Usage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cacheCreation: Optional<CacheCreation>`

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

    - `serverToolUse: Optional<ServerToolUsage>`

      The number of server tool requests.

      - `webSearchRequests: Long`

        The number of web search tool requests.

    - `serviceTier: Optional<ServiceTier>`

      If the request used the priority, standard, or batch tier.

      - `STANDARD("standard")`

      - `PRIORITY("priority")`

      - `BATCH("batch")`

### Message Count Tokens Tool

- `class MessageCountTokensTool: A class that can be one of several variants.union`

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

### Message Delta Usage

- `class MessageDeltaUsage:`

  - `cacheCreationInputTokens: Optional<Long>`

    The cumulative number of input tokens used to create the cache entry.

  - `cacheReadInputTokens: Optional<Long>`

    The cumulative number of input tokens read from the cache.

  - `inputTokens: Optional<Long>`

    The cumulative number of input tokens which were used.

  - `outputTokens: Long`

    The cumulative number of output tokens which were used.

  - `serverToolUse: Optional<ServerToolUsage>`

    The number of server tool requests.

    - `webSearchRequests: Long`

      The number of web search tool requests.

### Message Param

- `class MessageParam:`

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

### Message Tokens Count

- `class MessageTokensCount:`

  - `inputTokens: Long`

    The total number of tokens across the provided list of messages, system prompt, and tools.

### Metadata

- `class Metadata:`

  - `userId: Optional<String>`

    An external identifier for the user who is associated with the request.

    This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

### Plain Text Source

- `class PlainTextSource:`

  - `data: String`

  - `mediaType: JsonValue; "text/plain"constant`

    - `TEXT_PLAIN("text/plain")`

  - `type: JsonValue; "text"constant`

    - `TEXT("text")`

### Raw Content Block Delta

- `class RawContentBlockDelta: A class that can be one of several variants.union`

  - `class TextDelta:`

    - `text: String`

    - `type: JsonValue; "text_delta"constant`

      - `TEXT_DELTA("text_delta")`

  - `class InputJsonDelta:`

    - `partialJson: String`

    - `type: JsonValue; "input_json_delta"constant`

      - `INPUT_JSON_DELTA("input_json_delta")`

  - `class CitationsDelta:`

    - `citation: Citation`

      - `class CitationCharLocation:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endCharIndex: Long`

        - `fileId: Optional<String>`

        - `startCharIndex: Long`

        - `type: JsonValue; "char_location"constant`

          - `CHAR_LOCATION("char_location")`

      - `class CitationPageLocation:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endPageNumber: Long`

        - `fileId: Optional<String>`

        - `startPageNumber: Long`

        - `type: JsonValue; "page_location"constant`

          - `PAGE_LOCATION("page_location")`

      - `class CitationContentBlockLocation:`

        - `citedText: String`

        - `documentIndex: Long`

        - `documentTitle: Optional<String>`

        - `endBlockIndex: Long`

        - `fileId: Optional<String>`

        - `startBlockIndex: Long`

        - `type: JsonValue; "content_block_location"constant`

          - `CONTENT_BLOCK_LOCATION("content_block_location")`

      - `class CitationsWebSearchResultLocation:`

        - `citedText: String`

        - `encryptedIndex: String`

        - `title: Optional<String>`

        - `type: JsonValue; "web_search_result_location"constant`

          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

        - `url: String`

      - `class CitationsSearchResultLocation:`

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

  - `class ThinkingDelta:`

    - `thinking: String`

    - `type: JsonValue; "thinking_delta"constant`

      - `THINKING_DELTA("thinking_delta")`

  - `class SignatureDelta:`

    - `signature: String`

    - `type: JsonValue; "signature_delta"constant`

      - `SIGNATURE_DELTA("signature_delta")`

### Raw Content Block Delta Event

- `class RawContentBlockDeltaEvent:`

  - `delta: RawContentBlockDelta`

    - `class TextDelta:`

      - `text: String`

      - `type: JsonValue; "text_delta"constant`

        - `TEXT_DELTA("text_delta")`

    - `class InputJsonDelta:`

      - `partialJson: String`

      - `type: JsonValue; "input_json_delta"constant`

        - `INPUT_JSON_DELTA("input_json_delta")`

    - `class CitationsDelta:`

      - `citation: Citation`

        - `class CitationCharLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endCharIndex: Long`

          - `fileId: Optional<String>`

          - `startCharIndex: Long`

          - `type: JsonValue; "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class CitationPageLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endPageNumber: Long`

          - `fileId: Optional<String>`

          - `startPageNumber: Long`

          - `type: JsonValue; "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class CitationContentBlockLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endBlockIndex: Long`

          - `fileId: Optional<String>`

          - `startBlockIndex: Long`

          - `type: JsonValue; "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class CitationsWebSearchResultLocation:`

          - `citedText: String`

          - `encryptedIndex: String`

          - `title: Optional<String>`

          - `type: JsonValue; "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `url: String`

        - `class CitationsSearchResultLocation:`

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

    - `class ThinkingDelta:`

      - `thinking: String`

      - `type: JsonValue; "thinking_delta"constant`

        - `THINKING_DELTA("thinking_delta")`

    - `class SignatureDelta:`

      - `signature: String`

      - `type: JsonValue; "signature_delta"constant`

        - `SIGNATURE_DELTA("signature_delta")`

  - `index: Long`

  - `type: JsonValue; "content_block_delta"constant`

    - `CONTENT_BLOCK_DELTA("content_block_delta")`

### Raw Content Block Start Event

- `class RawContentBlockStartEvent:`

  - `contentBlock: ContentBlock`

    - `class TextBlock:`

      - `citations: Optional<List<TextCitation>>`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `class CitationCharLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endCharIndex: Long`

          - `fileId: Optional<String>`

          - `startCharIndex: Long`

          - `type: JsonValue; "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class CitationPageLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endPageNumber: Long`

          - `fileId: Optional<String>`

          - `startPageNumber: Long`

          - `type: JsonValue; "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class CitationContentBlockLocation:`

          - `citedText: String`

          - `documentIndex: Long`

          - `documentTitle: Optional<String>`

          - `endBlockIndex: Long`

          - `fileId: Optional<String>`

          - `startBlockIndex: Long`

          - `type: JsonValue; "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class CitationsWebSearchResultLocation:`

          - `citedText: String`

          - `encryptedIndex: String`

          - `title: Optional<String>`

          - `type: JsonValue; "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `url: String`

        - `class CitationsSearchResultLocation:`

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

    - `class ThinkingBlock:`

      - `signature: String`

      - `thinking: String`

      - `type: JsonValue; "thinking"constant`

        - `THINKING("thinking")`

    - `class RedactedThinkingBlock:`

      - `data: String`

      - `type: JsonValue; "redacted_thinking"constant`

        - `REDACTED_THINKING("redacted_thinking")`

    - `class ToolUseBlock:`

      - `id: String`

      - `input: Input`

      - `name: String`

      - `type: JsonValue; "tool_use"constant`

        - `TOOL_USE("tool_use")`

    - `class ServerToolUseBlock:`

      - `id: String`

      - `input: Input`

      - `name: JsonValue; "web_search"constant`

        - `WEB_SEARCH("web_search")`

      - `type: JsonValue; "server_tool_use"constant`

        - `SERVER_TOOL_USE("server_tool_use")`

    - `class WebSearchToolResultBlock:`

      - `content: WebSearchToolResultBlockContent`

        - `class WebSearchToolResultError:`

          - `errorCode: ErrorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `MAX_USES_EXCEEDED("max_uses_exceeded")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `QUERY_TOO_LONG("query_too_long")`

          - `type: JsonValue; "web_search_tool_result_error"constant`

            - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

        - `List<WebSearchResultBlock>`

          - `encryptedContent: String`

          - `pageAge: Optional<String>`

          - `title: String`

          - `type: JsonValue; "web_search_result"constant`

            - `WEB_SEARCH_RESULT("web_search_result")`

          - `url: String`

      - `toolUseId: String`

      - `type: JsonValue; "web_search_tool_result"constant`

        - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

  - `index: Long`

  - `type: JsonValue; "content_block_start"constant`

    - `CONTENT_BLOCK_START("content_block_start")`

### Raw Content Block Stop Event

- `class RawContentBlockStopEvent:`

  - `index: Long`

  - `type: JsonValue; "content_block_stop"constant`

    - `CONTENT_BLOCK_STOP("content_block_stop")`

### Raw Message Delta Event

- `class RawMessageDeltaEvent:`

  - `delta: Delta`

    - `stopReason: Optional<StopReason>`

      - `END_TURN("end_turn")`

      - `MAX_TOKENS("max_tokens")`

      - `STOP_SEQUENCE("stop_sequence")`

      - `TOOL_USE("tool_use")`

      - `PAUSE_TURN("pause_turn")`

      - `REFUSAL("refusal")`

    - `stopSequence: Optional<String>`

  - `type: JsonValue; "message_delta"constant`

    - `MESSAGE_DELTA("message_delta")`

  - `usage: MessageDeltaUsage`

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

    - `serverToolUse: Optional<ServerToolUsage>`

      The number of server tool requests.

      - `webSearchRequests: Long`

        The number of web search tool requests.

### Raw Message Start Event

- `class RawMessageStartEvent:`

  - `message: Message`

    - `id: String`

      Unique object identifier.

      The format and length of IDs may change over time.

    - `content: List<ContentBlock>`

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

      - `class TextBlock:`

        - `citations: Optional<List<TextCitation>>`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `class CitationCharLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endCharIndex: Long`

            - `fileId: Optional<String>`

            - `startCharIndex: Long`

            - `type: JsonValue; "char_location"constant`

              - `CHAR_LOCATION("char_location")`

          - `class CitationPageLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endPageNumber: Long`

            - `fileId: Optional<String>`

            - `startPageNumber: Long`

            - `type: JsonValue; "page_location"constant`

              - `PAGE_LOCATION("page_location")`

          - `class CitationContentBlockLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endBlockIndex: Long`

            - `fileId: Optional<String>`

            - `startBlockIndex: Long`

            - `type: JsonValue; "content_block_location"constant`

              - `CONTENT_BLOCK_LOCATION("content_block_location")`

          - `class CitationsWebSearchResultLocation:`

            - `citedText: String`

            - `encryptedIndex: String`

            - `title: Optional<String>`

            - `type: JsonValue; "web_search_result_location"constant`

              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

            - `url: String`

          - `class CitationsSearchResultLocation:`

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

      - `class ThinkingBlock:`

        - `signature: String`

        - `thinking: String`

        - `type: JsonValue; "thinking"constant`

          - `THINKING("thinking")`

      - `class RedactedThinkingBlock:`

        - `data: String`

        - `type: JsonValue; "redacted_thinking"constant`

          - `REDACTED_THINKING("redacted_thinking")`

      - `class ToolUseBlock:`

        - `id: String`

        - `input: Input`

        - `name: String`

        - `type: JsonValue; "tool_use"constant`

          - `TOOL_USE("tool_use")`

      - `class ServerToolUseBlock:`

        - `id: String`

        - `input: Input`

        - `name: JsonValue; "web_search"constant`

          - `WEB_SEARCH("web_search")`

        - `type: JsonValue; "server_tool_use"constant`

          - `SERVER_TOOL_USE("server_tool_use")`

      - `class WebSearchToolResultBlock:`

        - `content: WebSearchToolResultBlockContent`

          - `class WebSearchToolResultError:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `MAX_USES_EXCEEDED("max_uses_exceeded")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `QUERY_TOO_LONG("query_too_long")`

            - `type: JsonValue; "web_search_tool_result_error"constant`

              - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

          - `List<WebSearchResultBlock>`

            - `encryptedContent: String`

            - `pageAge: Optional<String>`

            - `title: String`

            - `type: JsonValue; "web_search_result"constant`

              - `WEB_SEARCH_RESULT("web_search_result")`

            - `url: String`

        - `toolUseId: String`

        - `type: JsonValue; "web_search_tool_result"constant`

          - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

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

    - `stopReason: Optional<StopReason>`

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

    - `stopSequence: Optional<String>`

      Which custom stop sequence was generated, if any.

      This value will be a non-null string if one of your custom stop sequences was generated.

    - `type: JsonValue; "message"constant`

      Object type.

      For Messages, this is always `"message"`.

      - `MESSAGE("message")`

    - `usage: Usage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cacheCreation: Optional<CacheCreation>`

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

      - `serverToolUse: Optional<ServerToolUsage>`

        The number of server tool requests.

        - `webSearchRequests: Long`

          The number of web search tool requests.

      - `serviceTier: Optional<ServiceTier>`

        If the request used the priority, standard, or batch tier.

        - `STANDARD("standard")`

        - `PRIORITY("priority")`

        - `BATCH("batch")`

  - `type: JsonValue; "message_start"constant`

    - `MESSAGE_START("message_start")`

### Raw Message Stop Event

- `class RawMessageStopEvent:`

  - `type: JsonValue; "message_stop"constant`

    - `MESSAGE_STOP("message_stop")`

### Raw Message Stream Event

- `class RawMessageStreamEvent: A class that can be one of several variants.union`

  - `class RawMessageStartEvent:`

    - `message: Message`

      - `id: String`

        Unique object identifier.

        The format and length of IDs may change over time.

      - `content: List<ContentBlock>`

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

        - `class TextBlock:`

          - `citations: Optional<List<TextCitation>>`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `class CitationCharLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `fileId: Optional<String>`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class CitationPageLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `fileId: Optional<String>`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class CitationContentBlockLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `fileId: Optional<String>`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class CitationsWebSearchResultLocation:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class CitationsSearchResultLocation:`

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

        - `class ThinkingBlock:`

          - `signature: String`

          - `thinking: String`

          - `type: JsonValue; "thinking"constant`

            - `THINKING("thinking")`

        - `class RedactedThinkingBlock:`

          - `data: String`

          - `type: JsonValue; "redacted_thinking"constant`

            - `REDACTED_THINKING("redacted_thinking")`

        - `class ToolUseBlock:`

          - `id: String`

          - `input: Input`

          - `name: String`

          - `type: JsonValue; "tool_use"constant`

            - `TOOL_USE("tool_use")`

        - `class ServerToolUseBlock:`

          - `id: String`

          - `input: Input`

          - `name: JsonValue; "web_search"constant`

            - `WEB_SEARCH("web_search")`

          - `type: JsonValue; "server_tool_use"constant`

            - `SERVER_TOOL_USE("server_tool_use")`

        - `class WebSearchToolResultBlock:`

          - `content: WebSearchToolResultBlockContent`

            - `class WebSearchToolResultError:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `QUERY_TOO_LONG("query_too_long")`

              - `type: JsonValue; "web_search_tool_result_error"constant`

                - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

            - `List<WebSearchResultBlock>`

              - `encryptedContent: String`

              - `pageAge: Optional<String>`

              - `title: String`

              - `type: JsonValue; "web_search_result"constant`

                - `WEB_SEARCH_RESULT("web_search_result")`

              - `url: String`

          - `toolUseId: String`

          - `type: JsonValue; "web_search_tool_result"constant`

            - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

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

      - `stopReason: Optional<StopReason>`

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

      - `stopSequence: Optional<String>`

        Which custom stop sequence was generated, if any.

        This value will be a non-null string if one of your custom stop sequences was generated.

      - `type: JsonValue; "message"constant`

        Object type.

        For Messages, this is always `"message"`.

        - `MESSAGE("message")`

      - `usage: Usage`

        Billing and rate-limit usage.

        Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

        Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

        For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

        Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

        - `cacheCreation: Optional<CacheCreation>`

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

        - `serverToolUse: Optional<ServerToolUsage>`

          The number of server tool requests.

          - `webSearchRequests: Long`

            The number of web search tool requests.

        - `serviceTier: Optional<ServiceTier>`

          If the request used the priority, standard, or batch tier.

          - `STANDARD("standard")`

          - `PRIORITY("priority")`

          - `BATCH("batch")`

    - `type: JsonValue; "message_start"constant`

      - `MESSAGE_START("message_start")`

  - `class RawMessageDeltaEvent:`

    - `delta: Delta`

      - `stopReason: Optional<StopReason>`

        - `END_TURN("end_turn")`

        - `MAX_TOKENS("max_tokens")`

        - `STOP_SEQUENCE("stop_sequence")`

        - `TOOL_USE("tool_use")`

        - `PAUSE_TURN("pause_turn")`

        - `REFUSAL("refusal")`

      - `stopSequence: Optional<String>`

    - `type: JsonValue; "message_delta"constant`

      - `MESSAGE_DELTA("message_delta")`

    - `usage: MessageDeltaUsage`

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

      - `serverToolUse: Optional<ServerToolUsage>`

        The number of server tool requests.

        - `webSearchRequests: Long`

          The number of web search tool requests.

  - `class RawMessageStopEvent:`

    - `type: JsonValue; "message_stop"constant`

      - `MESSAGE_STOP("message_stop")`

  - `class RawContentBlockStartEvent:`

    - `contentBlock: ContentBlock`

      - `class TextBlock:`

        - `citations: Optional<List<TextCitation>>`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `class CitationCharLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endCharIndex: Long`

            - `fileId: Optional<String>`

            - `startCharIndex: Long`

            - `type: JsonValue; "char_location"constant`

              - `CHAR_LOCATION("char_location")`

          - `class CitationPageLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endPageNumber: Long`

            - `fileId: Optional<String>`

            - `startPageNumber: Long`

            - `type: JsonValue; "page_location"constant`

              - `PAGE_LOCATION("page_location")`

          - `class CitationContentBlockLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endBlockIndex: Long`

            - `fileId: Optional<String>`

            - `startBlockIndex: Long`

            - `type: JsonValue; "content_block_location"constant`

              - `CONTENT_BLOCK_LOCATION("content_block_location")`

          - `class CitationsWebSearchResultLocation:`

            - `citedText: String`

            - `encryptedIndex: String`

            - `title: Optional<String>`

            - `type: JsonValue; "web_search_result_location"constant`

              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

            - `url: String`

          - `class CitationsSearchResultLocation:`

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

      - `class ThinkingBlock:`

        - `signature: String`

        - `thinking: String`

        - `type: JsonValue; "thinking"constant`

          - `THINKING("thinking")`

      - `class RedactedThinkingBlock:`

        - `data: String`

        - `type: JsonValue; "redacted_thinking"constant`

          - `REDACTED_THINKING("redacted_thinking")`

      - `class ToolUseBlock:`

        - `id: String`

        - `input: Input`

        - `name: String`

        - `type: JsonValue; "tool_use"constant`

          - `TOOL_USE("tool_use")`

      - `class ServerToolUseBlock:`

        - `id: String`

        - `input: Input`

        - `name: JsonValue; "web_search"constant`

          - `WEB_SEARCH("web_search")`

        - `type: JsonValue; "server_tool_use"constant`

          - `SERVER_TOOL_USE("server_tool_use")`

      - `class WebSearchToolResultBlock:`

        - `content: WebSearchToolResultBlockContent`

          - `class WebSearchToolResultError:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `MAX_USES_EXCEEDED("max_uses_exceeded")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `QUERY_TOO_LONG("query_too_long")`

            - `type: JsonValue; "web_search_tool_result_error"constant`

              - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

          - `List<WebSearchResultBlock>`

            - `encryptedContent: String`

            - `pageAge: Optional<String>`

            - `title: String`

            - `type: JsonValue; "web_search_result"constant`

              - `WEB_SEARCH_RESULT("web_search_result")`

            - `url: String`

        - `toolUseId: String`

        - `type: JsonValue; "web_search_tool_result"constant`

          - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

    - `index: Long`

    - `type: JsonValue; "content_block_start"constant`

      - `CONTENT_BLOCK_START("content_block_start")`

  - `class RawContentBlockDeltaEvent:`

    - `delta: RawContentBlockDelta`

      - `class TextDelta:`

        - `text: String`

        - `type: JsonValue; "text_delta"constant`

          - `TEXT_DELTA("text_delta")`

      - `class InputJsonDelta:`

        - `partialJson: String`

        - `type: JsonValue; "input_json_delta"constant`

          - `INPUT_JSON_DELTA("input_json_delta")`

      - `class CitationsDelta:`

        - `citation: Citation`

          - `class CitationCharLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endCharIndex: Long`

            - `fileId: Optional<String>`

            - `startCharIndex: Long`

            - `type: JsonValue; "char_location"constant`

              - `CHAR_LOCATION("char_location")`

          - `class CitationPageLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endPageNumber: Long`

            - `fileId: Optional<String>`

            - `startPageNumber: Long`

            - `type: JsonValue; "page_location"constant`

              - `PAGE_LOCATION("page_location")`

          - `class CitationContentBlockLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endBlockIndex: Long`

            - `fileId: Optional<String>`

            - `startBlockIndex: Long`

            - `type: JsonValue; "content_block_location"constant`

              - `CONTENT_BLOCK_LOCATION("content_block_location")`

          - `class CitationsWebSearchResultLocation:`

            - `citedText: String`

            - `encryptedIndex: String`

            - `title: Optional<String>`

            - `type: JsonValue; "web_search_result_location"constant`

              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

            - `url: String`

          - `class CitationsSearchResultLocation:`

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

      - `class ThinkingDelta:`

        - `thinking: String`

        - `type: JsonValue; "thinking_delta"constant`

          - `THINKING_DELTA("thinking_delta")`

      - `class SignatureDelta:`

        - `signature: String`

        - `type: JsonValue; "signature_delta"constant`

          - `SIGNATURE_DELTA("signature_delta")`

    - `index: Long`

    - `type: JsonValue; "content_block_delta"constant`

      - `CONTENT_BLOCK_DELTA("content_block_delta")`

  - `class RawContentBlockStopEvent:`

    - `index: Long`

    - `type: JsonValue; "content_block_stop"constant`

      - `CONTENT_BLOCK_STOP("content_block_stop")`

### Redacted Thinking Block

- `class RedactedThinkingBlock:`

  - `data: String`

  - `type: JsonValue; "redacted_thinking"constant`

    - `REDACTED_THINKING("redacted_thinking")`

### Redacted Thinking Block Param

- `class RedactedThinkingBlockParam:`

  - `data: String`

  - `type: JsonValue; "redacted_thinking"constant`

    - `REDACTED_THINKING("redacted_thinking")`

### Search Result Block Param

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

### Server Tool Usage

- `class ServerToolUsage:`

  - `webSearchRequests: Long`

    The number of web search tool requests.

### Server Tool Use Block

- `class ServerToolUseBlock:`

  - `id: String`

  - `input: Input`

  - `name: JsonValue; "web_search"constant`

    - `WEB_SEARCH("web_search")`

  - `type: JsonValue; "server_tool_use"constant`

    - `SERVER_TOOL_USE("server_tool_use")`

### Server Tool Use Block Param

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

### Signature Delta

- `class SignatureDelta:`

  - `signature: String`

  - `type: JsonValue; "signature_delta"constant`

    - `SIGNATURE_DELTA("signature_delta")`

### Stop Reason

- `enum class StopReason:`

  - `END_TURN("end_turn")`

  - `MAX_TOKENS("max_tokens")`

  - `STOP_SEQUENCE("stop_sequence")`

  - `TOOL_USE("tool_use")`

  - `PAUSE_TURN("pause_turn")`

  - `REFUSAL("refusal")`

### Text Block

- `class TextBlock:`

  - `citations: Optional<List<TextCitation>>`

    Citations supporting the text block.

    The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

    - `class CitationCharLocation:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endCharIndex: Long`

      - `fileId: Optional<String>`

      - `startCharIndex: Long`

      - `type: JsonValue; "char_location"constant`

        - `CHAR_LOCATION("char_location")`

    - `class CitationPageLocation:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endPageNumber: Long`

      - `fileId: Optional<String>`

      - `startPageNumber: Long`

      - `type: JsonValue; "page_location"constant`

        - `PAGE_LOCATION("page_location")`

    - `class CitationContentBlockLocation:`

      - `citedText: String`

      - `documentIndex: Long`

      - `documentTitle: Optional<String>`

      - `endBlockIndex: Long`

      - `fileId: Optional<String>`

      - `startBlockIndex: Long`

      - `type: JsonValue; "content_block_location"constant`

        - `CONTENT_BLOCK_LOCATION("content_block_location")`

    - `class CitationsWebSearchResultLocation:`

      - `citedText: String`

      - `encryptedIndex: String`

      - `title: Optional<String>`

      - `type: JsonValue; "web_search_result_location"constant`

        - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

      - `url: String`

    - `class CitationsSearchResultLocation:`

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

### Text Block Param

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

### Text Citation

- `class TextCitation: A class that can be one of several variants.union`

  - `class CitationCharLocation:`

    - `citedText: String`

    - `documentIndex: Long`

    - `documentTitle: Optional<String>`

    - `endCharIndex: Long`

    - `fileId: Optional<String>`

    - `startCharIndex: Long`

    - `type: JsonValue; "char_location"constant`

      - `CHAR_LOCATION("char_location")`

  - `class CitationPageLocation:`

    - `citedText: String`

    - `documentIndex: Long`

    - `documentTitle: Optional<String>`

    - `endPageNumber: Long`

    - `fileId: Optional<String>`

    - `startPageNumber: Long`

    - `type: JsonValue; "page_location"constant`

      - `PAGE_LOCATION("page_location")`

  - `class CitationContentBlockLocation:`

    - `citedText: String`

    - `documentIndex: Long`

    - `documentTitle: Optional<String>`

    - `endBlockIndex: Long`

    - `fileId: Optional<String>`

    - `startBlockIndex: Long`

    - `type: JsonValue; "content_block_location"constant`

      - `CONTENT_BLOCK_LOCATION("content_block_location")`

  - `class CitationsWebSearchResultLocation:`

    - `citedText: String`

    - `encryptedIndex: String`

    - `title: Optional<String>`

    - `type: JsonValue; "web_search_result_location"constant`

      - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

    - `url: String`

  - `class CitationsSearchResultLocation:`

    - `citedText: String`

    - `endBlockIndex: Long`

    - `searchResultIndex: Long`

    - `source: String`

    - `startBlockIndex: Long`

    - `title: Optional<String>`

    - `type: JsonValue; "search_result_location"constant`

      - `SEARCH_RESULT_LOCATION("search_result_location")`

### Text Citation Param

- `class TextCitationParam: A class that can be one of several variants.union`

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

### Text Delta

- `class TextDelta:`

  - `text: String`

  - `type: JsonValue; "text_delta"constant`

    - `TEXT_DELTA("text_delta")`

### Thinking Block

- `class ThinkingBlock:`

  - `signature: String`

  - `thinking: String`

  - `type: JsonValue; "thinking"constant`

    - `THINKING("thinking")`

### Thinking Block Param

- `class ThinkingBlockParam:`

  - `signature: String`

  - `thinking: String`

  - `type: JsonValue; "thinking"constant`

    - `THINKING("thinking")`

### Thinking Config Disabled

- `class ThinkingConfigDisabled:`

  - `type: JsonValue; "disabled"constant`

    - `DISABLED("disabled")`

### Thinking Config Enabled

- `class ThinkingConfigEnabled:`

  - `budgetTokens: Long`

    Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

    Must be ≥1024 and less than `max_tokens`.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `type: JsonValue; "enabled"constant`

    - `ENABLED("enabled")`

### Thinking Config Param

- `class ThinkingConfigParam: A class that can be one of several variants.union`

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

### Thinking Delta

- `class ThinkingDelta:`

  - `thinking: String`

  - `type: JsonValue; "thinking_delta"constant`

    - `THINKING_DELTA("thinking_delta")`

### Tool

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

### Tool Bash 20250124

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

### Tool Choice

- `class ToolChoice: A class that can be one of several variants.union`

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

### Tool Choice Any

- `class ToolChoiceAny:`

  The model will use any available tools.

  - `type: JsonValue; "any"constant`

    - `ANY("any")`

  - `disableParallelToolUse: Optional<Boolean>`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output exactly one tool use.

### Tool Choice Auto

- `class ToolChoiceAuto:`

  The model will automatically decide whether to use tools.

  - `type: JsonValue; "auto"constant`

    - `AUTO("auto")`

  - `disableParallelToolUse: Optional<Boolean>`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output at most one tool use.

### Tool Choice None

- `class ToolChoiceNone:`

  The model will not be allowed to use tools.

  - `type: JsonValue; "none"constant`

    - `NONE("none")`

### Tool Choice Tool

- `class ToolChoiceTool:`

  The model will use the specified tool with `tool_choice.name`.

  - `name: String`

    The name of the tool to use.

  - `type: JsonValue; "tool"constant`

    - `TOOL("tool")`

  - `disableParallelToolUse: Optional<Boolean>`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output exactly one tool use.

### Tool Result Block Param

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

### Tool Text Editor 20250124

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

### Tool Text Editor 20250429

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

### Tool Text Editor 20250728

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

### Tool Union

- `class ToolUnion: A class that can be one of several variants.union`

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

### Tool Use Block

- `class ToolUseBlock:`

  - `id: String`

  - `input: Input`

  - `name: String`

  - `type: JsonValue; "tool_use"constant`

    - `TOOL_USE("tool_use")`

### Tool Use Block Param

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

### URL Image Source

- `class UrlImageSource:`

  - `type: JsonValue; "url"constant`

    - `URL("url")`

  - `url: String`

### URL PDF Source

- `class UrlPdfSource:`

  - `type: JsonValue; "url"constant`

    - `URL("url")`

  - `url: String`

### Usage

- `class Usage:`

  - `cacheCreation: Optional<CacheCreation>`

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

  - `serverToolUse: Optional<ServerToolUsage>`

    The number of server tool requests.

    - `webSearchRequests: Long`

      The number of web search tool requests.

  - `serviceTier: Optional<ServiceTier>`

    If the request used the priority, standard, or batch tier.

    - `STANDARD("standard")`

    - `PRIORITY("priority")`

    - `BATCH("batch")`

### Web Search Result Block

- `class WebSearchResultBlock:`

  - `encryptedContent: String`

  - `pageAge: Optional<String>`

  - `title: String`

  - `type: JsonValue; "web_search_result"constant`

    - `WEB_SEARCH_RESULT("web_search_result")`

  - `url: String`

### Web Search Result Block Param

- `class WebSearchResultBlockParam:`

  - `encryptedContent: String`

  - `title: String`

  - `type: JsonValue; "web_search_result"constant`

    - `WEB_SEARCH_RESULT("web_search_result")`

  - `url: String`

  - `pageAge: Optional<String>`

### Web Search Tool 20250305

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

### Web Search Tool Request Error

- `class WebSearchToolRequestError:`

  - `errorCode: ErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `UNAVAILABLE("unavailable")`

    - `MAX_USES_EXCEEDED("max_uses_exceeded")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `QUERY_TOO_LONG("query_too_long")`

  - `type: JsonValue; "web_search_tool_result_error"constant`

    - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

### Web Search Tool Result Block

- `class WebSearchToolResultBlock:`

  - `content: WebSearchToolResultBlockContent`

    - `class WebSearchToolResultError:`

      - `errorCode: ErrorCode`

        - `INVALID_TOOL_INPUT("invalid_tool_input")`

        - `UNAVAILABLE("unavailable")`

        - `MAX_USES_EXCEEDED("max_uses_exceeded")`

        - `TOO_MANY_REQUESTS("too_many_requests")`

        - `QUERY_TOO_LONG("query_too_long")`

      - `type: JsonValue; "web_search_tool_result_error"constant`

        - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

    - `List<WebSearchResultBlock>`

      - `encryptedContent: String`

      - `pageAge: Optional<String>`

      - `title: String`

      - `type: JsonValue; "web_search_result"constant`

        - `WEB_SEARCH_RESULT("web_search_result")`

      - `url: String`

  - `toolUseId: String`

  - `type: JsonValue; "web_search_tool_result"constant`

    - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

### Web Search Tool Result Block Content

- `class WebSearchToolResultBlockContent: A class that can be one of several variants.union`

  - `class WebSearchToolResultError:`

    - `errorCode: ErrorCode`

      - `INVALID_TOOL_INPUT("invalid_tool_input")`

      - `UNAVAILABLE("unavailable")`

      - `MAX_USES_EXCEEDED("max_uses_exceeded")`

      - `TOO_MANY_REQUESTS("too_many_requests")`

      - `QUERY_TOO_LONG("query_too_long")`

    - `type: JsonValue; "web_search_tool_result_error"constant`

      - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

  - `List<WebSearchResultBlock>`

    - `encryptedContent: String`

    - `pageAge: Optional<String>`

    - `title: String`

    - `type: JsonValue; "web_search_result"constant`

      - `WEB_SEARCH_RESULT("web_search_result")`

    - `url: String`

### Web Search Tool Result Block Param

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

### Web Search Tool Result Block Param Content

- `class WebSearchToolResultBlockParamContent: A class that can be one of several variants.union`

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

### Web Search Tool Result Error

- `class WebSearchToolResultError:`

  - `errorCode: ErrorCode`

    - `INVALID_TOOL_INPUT("invalid_tool_input")`

    - `UNAVAILABLE("unavailable")`

    - `MAX_USES_EXCEEDED("max_uses_exceeded")`

    - `TOO_MANY_REQUESTS("too_many_requests")`

    - `QUERY_TOO_LONG("query_too_long")`

  - `type: JsonValue; "web_search_tool_result_error"constant`

    - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

# Batches

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

## Retrieve

`messages().batches().retrieve(BatchRetrieveParamsparams = BatchRetrieveParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : MessageBatch`

**get** `/v1/messages/batches/{message_batch_id}`

This endpoint is idempotent and can be used to poll for Message Batch completion. To access the results of a Message Batch, make a request to the `results_url` field in the response.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchRetrieveParams`

  - `messageBatchId: Optional<String>`

    ID of the Message Batch.

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
import com.anthropic.models.messages.batches.BatchRetrieveParams
import com.anthropic.models.messages.batches.MessageBatch

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val messageBatch: MessageBatch = client.messages().batches().retrieve("message_batch_id")
}
```

## List

`messages().batches().list(BatchListParamsparams = BatchListParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : BatchListPage`

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
import com.anthropic.models.messages.batches.BatchListPage
import com.anthropic.models.messages.batches.BatchListParams

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val page: BatchListPage = client.messages().batches().list()
}
```

## Cancel

`messages().batches().cancel(BatchCancelParamsparams = BatchCancelParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : MessageBatch`

**post** `/v1/messages/batches/{message_batch_id}/cancel`

Batches may be canceled any time before processing ends. Once cancellation is initiated, the batch enters a `canceling` state, at which time the system may complete any in-progress, non-interruptible requests before finalizing cancellation.

The number of canceled requests is specified in `request_counts`. To determine which requests were canceled, check the individual results within the batch. Note that cancellation may not result in any canceled requests if they were non-interruptible.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchCancelParams`

  - `messageBatchId: Optional<String>`

    ID of the Message Batch.

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
import com.anthropic.models.messages.batches.BatchCancelParams
import com.anthropic.models.messages.batches.MessageBatch

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val messageBatch: MessageBatch = client.messages().batches().cancel("message_batch_id")
}
```

## Delete

`messages().batches().delete(BatchDeleteParamsparams = BatchDeleteParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : DeletedMessageBatch`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchDeleteParams`

  - `messageBatchId: Optional<String>`

    ID of the Message Batch.

### Returns

- `class DeletedMessageBatch:`

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
import com.anthropic.models.messages.batches.BatchDeleteParams
import com.anthropic.models.messages.batches.DeletedMessageBatch

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val deletedMessageBatch: DeletedMessageBatch = client.messages().batches().delete("message_batch_id")
}
```

## Results

`messages().batches().resultsStreaming(BatchResultsParamsparams = BatchResultsParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : MessageBatchIndividualResponse`

**get** `/v1/messages/batches/{message_batch_id}/results`

Streams the results of a Message Batch as a `.jsonl` file.

Each line in the file is a JSON object containing the result of a single request in the Message Batch. Results are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchResultsParams`

  - `messageBatchId: Optional<String>`

    ID of the Message Batch.

### Returns

- `class MessageBatchIndividualResponse:`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `customId: String`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: MessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `class MessageBatchSucceededResult:`

      - `message: Message`

        - `id: String`

          Unique object identifier.

          The format and length of IDs may change over time.

        - `content: List<ContentBlock>`

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

          - `class TextBlock:`

            - `citations: Optional<List<TextCitation>>`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class CitationCharLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endCharIndex: Long`

                - `fileId: Optional<String>`

                - `startCharIndex: Long`

                - `type: JsonValue; "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class CitationPageLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endPageNumber: Long`

                - `fileId: Optional<String>`

                - `startPageNumber: Long`

                - `type: JsonValue; "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class CitationContentBlockLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endBlockIndex: Long`

                - `fileId: Optional<String>`

                - `startBlockIndex: Long`

                - `type: JsonValue; "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class CitationsWebSearchResultLocation:`

                - `citedText: String`

                - `encryptedIndex: String`

                - `title: Optional<String>`

                - `type: JsonValue; "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `url: String`

              - `class CitationsSearchResultLocation:`

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

          - `class ThinkingBlock:`

            - `signature: String`

            - `thinking: String`

            - `type: JsonValue; "thinking"constant`

              - `THINKING("thinking")`

          - `class RedactedThinkingBlock:`

            - `data: String`

            - `type: JsonValue; "redacted_thinking"constant`

              - `REDACTED_THINKING("redacted_thinking")`

          - `class ToolUseBlock:`

            - `id: String`

            - `input: Input`

            - `name: String`

            - `type: JsonValue; "tool_use"constant`

              - `TOOL_USE("tool_use")`

          - `class ServerToolUseBlock:`

            - `id: String`

            - `input: Input`

            - `name: JsonValue; "web_search"constant`

              - `WEB_SEARCH("web_search")`

            - `type: JsonValue; "server_tool_use"constant`

              - `SERVER_TOOL_USE("server_tool_use")`

          - `class WebSearchToolResultBlock:`

            - `content: WebSearchToolResultBlockContent`

              - `class WebSearchToolResultError:`

                - `errorCode: ErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `UNAVAILABLE("unavailable")`

                  - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `QUERY_TOO_LONG("query_too_long")`

                - `type: JsonValue; "web_search_tool_result_error"constant`

                  - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

              - `List<WebSearchResultBlock>`

                - `encryptedContent: String`

                - `pageAge: Optional<String>`

                - `title: String`

                - `type: JsonValue; "web_search_result"constant`

                  - `WEB_SEARCH_RESULT("web_search_result")`

                - `url: String`

            - `toolUseId: String`

            - `type: JsonValue; "web_search_tool_result"constant`

              - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

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

        - `stopReason: Optional<StopReason>`

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

        - `stopSequence: Optional<String>`

          Which custom stop sequence was generated, if any.

          This value will be a non-null string if one of your custom stop sequences was generated.

        - `type: JsonValue; "message"constant`

          Object type.

          For Messages, this is always `"message"`.

          - `MESSAGE("message")`

        - `usage: Usage`

          Billing and rate-limit usage.

          Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

          Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

          For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

          Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

          - `cacheCreation: Optional<CacheCreation>`

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

          - `serverToolUse: Optional<ServerToolUsage>`

            The number of server tool requests.

            - `webSearchRequests: Long`

              The number of web search tool requests.

          - `serviceTier: Optional<ServiceTier>`

            If the request used the priority, standard, or batch tier.

            - `STANDARD("standard")`

            - `PRIORITY("priority")`

            - `BATCH("batch")`

      - `type: JsonValue; "succeeded"constant`

        - `SUCCEEDED("succeeded")`

    - `class MessageBatchErroredResult:`

      - `error: ErrorResponse`

        - `error: ErrorObject`

          - `class InvalidRequestError:`

            - `message: String`

            - `type: JsonValue; "invalid_request_error"constant`

              - `INVALID_REQUEST_ERROR("invalid_request_error")`

          - `class AuthenticationError:`

            - `message: String`

            - `type: JsonValue; "authentication_error"constant`

              - `AUTHENTICATION_ERROR("authentication_error")`

          - `class BillingError:`

            - `message: String`

            - `type: JsonValue; "billing_error"constant`

              - `BILLING_ERROR("billing_error")`

          - `class PermissionError:`

            - `message: String`

            - `type: JsonValue; "permission_error"constant`

              - `PERMISSION_ERROR("permission_error")`

          - `class NotFoundError:`

            - `message: String`

            - `type: JsonValue; "not_found_error"constant`

              - `NOT_FOUND_ERROR("not_found_error")`

          - `class RateLimitError:`

            - `message: String`

            - `type: JsonValue; "rate_limit_error"constant`

              - `RATE_LIMIT_ERROR("rate_limit_error")`

          - `class GatewayTimeoutError:`

            - `message: String`

            - `type: JsonValue; "timeout_error"constant`

              - `TIMEOUT_ERROR("timeout_error")`

          - `class ApiErrorObject:`

            - `message: String`

            - `type: JsonValue; "api_error"constant`

              - `API_ERROR("api_error")`

          - `class OverloadedError:`

            - `message: String`

            - `type: JsonValue; "overloaded_error"constant`

              - `OVERLOADED_ERROR("overloaded_error")`

        - `requestId: Optional<String>`

        - `type: JsonValue; "error"constant`

          - `ERROR("error")`

      - `type: JsonValue; "errored"constant`

        - `ERRORED("errored")`

    - `class MessageBatchCanceledResult:`

      - `type: JsonValue; "canceled"constant`

        - `CANCELED("canceled")`

    - `class MessageBatchExpiredResult:`

      - `type: JsonValue; "expired"constant`

        - `EXPIRED("expired")`

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.core.http.StreamResponse
import com.anthropic.models.messages.batches.BatchResultsParams
import com.anthropic.models.messages.batches.MessageBatchIndividualResponse

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val messageBatchIndividualResponse: StreamResponse<MessageBatchIndividualResponse> = client.messages().batches().resultsStreaming("message_batch_id")
}
```

## Domain Types

### Deleted Message Batch

- `class DeletedMessageBatch:`

  - `id: String`

    ID of the Message Batch.

  - `type: JsonValue; "message_batch_deleted"constant`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `MESSAGE_BATCH_DELETED("message_batch_deleted")`

### Message Batch

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

### Message Batch Canceled Result

- `class MessageBatchCanceledResult:`

  - `type: JsonValue; "canceled"constant`

    - `CANCELED("canceled")`

### Message Batch Errored Result

- `class MessageBatchErroredResult:`

  - `error: ErrorResponse`

    - `error: ErrorObject`

      - `class InvalidRequestError:`

        - `message: String`

        - `type: JsonValue; "invalid_request_error"constant`

          - `INVALID_REQUEST_ERROR("invalid_request_error")`

      - `class AuthenticationError:`

        - `message: String`

        - `type: JsonValue; "authentication_error"constant`

          - `AUTHENTICATION_ERROR("authentication_error")`

      - `class BillingError:`

        - `message: String`

        - `type: JsonValue; "billing_error"constant`

          - `BILLING_ERROR("billing_error")`

      - `class PermissionError:`

        - `message: String`

        - `type: JsonValue; "permission_error"constant`

          - `PERMISSION_ERROR("permission_error")`

      - `class NotFoundError:`

        - `message: String`

        - `type: JsonValue; "not_found_error"constant`

          - `NOT_FOUND_ERROR("not_found_error")`

      - `class RateLimitError:`

        - `message: String`

        - `type: JsonValue; "rate_limit_error"constant`

          - `RATE_LIMIT_ERROR("rate_limit_error")`

      - `class GatewayTimeoutError:`

        - `message: String`

        - `type: JsonValue; "timeout_error"constant`

          - `TIMEOUT_ERROR("timeout_error")`

      - `class ApiErrorObject:`

        - `message: String`

        - `type: JsonValue; "api_error"constant`

          - `API_ERROR("api_error")`

      - `class OverloadedError:`

        - `message: String`

        - `type: JsonValue; "overloaded_error"constant`

          - `OVERLOADED_ERROR("overloaded_error")`

    - `requestId: Optional<String>`

    - `type: JsonValue; "error"constant`

      - `ERROR("error")`

  - `type: JsonValue; "errored"constant`

    - `ERRORED("errored")`

### Message Batch Expired Result

- `class MessageBatchExpiredResult:`

  - `type: JsonValue; "expired"constant`

    - `EXPIRED("expired")`

### Message Batch Individual Response

- `class MessageBatchIndividualResponse:`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `customId: String`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: MessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `class MessageBatchSucceededResult:`

      - `message: Message`

        - `id: String`

          Unique object identifier.

          The format and length of IDs may change over time.

        - `content: List<ContentBlock>`

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

          - `class TextBlock:`

            - `citations: Optional<List<TextCitation>>`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class CitationCharLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endCharIndex: Long`

                - `fileId: Optional<String>`

                - `startCharIndex: Long`

                - `type: JsonValue; "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class CitationPageLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endPageNumber: Long`

                - `fileId: Optional<String>`

                - `startPageNumber: Long`

                - `type: JsonValue; "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class CitationContentBlockLocation:`

                - `citedText: String`

                - `documentIndex: Long`

                - `documentTitle: Optional<String>`

                - `endBlockIndex: Long`

                - `fileId: Optional<String>`

                - `startBlockIndex: Long`

                - `type: JsonValue; "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class CitationsWebSearchResultLocation:`

                - `citedText: String`

                - `encryptedIndex: String`

                - `title: Optional<String>`

                - `type: JsonValue; "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `url: String`

              - `class CitationsSearchResultLocation:`

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

          - `class ThinkingBlock:`

            - `signature: String`

            - `thinking: String`

            - `type: JsonValue; "thinking"constant`

              - `THINKING("thinking")`

          - `class RedactedThinkingBlock:`

            - `data: String`

            - `type: JsonValue; "redacted_thinking"constant`

              - `REDACTED_THINKING("redacted_thinking")`

          - `class ToolUseBlock:`

            - `id: String`

            - `input: Input`

            - `name: String`

            - `type: JsonValue; "tool_use"constant`

              - `TOOL_USE("tool_use")`

          - `class ServerToolUseBlock:`

            - `id: String`

            - `input: Input`

            - `name: JsonValue; "web_search"constant`

              - `WEB_SEARCH("web_search")`

            - `type: JsonValue; "server_tool_use"constant`

              - `SERVER_TOOL_USE("server_tool_use")`

          - `class WebSearchToolResultBlock:`

            - `content: WebSearchToolResultBlockContent`

              - `class WebSearchToolResultError:`

                - `errorCode: ErrorCode`

                  - `INVALID_TOOL_INPUT("invalid_tool_input")`

                  - `UNAVAILABLE("unavailable")`

                  - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                  - `TOO_MANY_REQUESTS("too_many_requests")`

                  - `QUERY_TOO_LONG("query_too_long")`

                - `type: JsonValue; "web_search_tool_result_error"constant`

                  - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

              - `List<WebSearchResultBlock>`

                - `encryptedContent: String`

                - `pageAge: Optional<String>`

                - `title: String`

                - `type: JsonValue; "web_search_result"constant`

                  - `WEB_SEARCH_RESULT("web_search_result")`

                - `url: String`

            - `toolUseId: String`

            - `type: JsonValue; "web_search_tool_result"constant`

              - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

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

        - `stopReason: Optional<StopReason>`

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

        - `stopSequence: Optional<String>`

          Which custom stop sequence was generated, if any.

          This value will be a non-null string if one of your custom stop sequences was generated.

        - `type: JsonValue; "message"constant`

          Object type.

          For Messages, this is always `"message"`.

          - `MESSAGE("message")`

        - `usage: Usage`

          Billing and rate-limit usage.

          Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

          Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

          For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

          Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

          - `cacheCreation: Optional<CacheCreation>`

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

          - `serverToolUse: Optional<ServerToolUsage>`

            The number of server tool requests.

            - `webSearchRequests: Long`

              The number of web search tool requests.

          - `serviceTier: Optional<ServiceTier>`

            If the request used the priority, standard, or batch tier.

            - `STANDARD("standard")`

            - `PRIORITY("priority")`

            - `BATCH("batch")`

      - `type: JsonValue; "succeeded"constant`

        - `SUCCEEDED("succeeded")`

    - `class MessageBatchErroredResult:`

      - `error: ErrorResponse`

        - `error: ErrorObject`

          - `class InvalidRequestError:`

            - `message: String`

            - `type: JsonValue; "invalid_request_error"constant`

              - `INVALID_REQUEST_ERROR("invalid_request_error")`

          - `class AuthenticationError:`

            - `message: String`

            - `type: JsonValue; "authentication_error"constant`

              - `AUTHENTICATION_ERROR("authentication_error")`

          - `class BillingError:`

            - `message: String`

            - `type: JsonValue; "billing_error"constant`

              - `BILLING_ERROR("billing_error")`

          - `class PermissionError:`

            - `message: String`

            - `type: JsonValue; "permission_error"constant`

              - `PERMISSION_ERROR("permission_error")`

          - `class NotFoundError:`

            - `message: String`

            - `type: JsonValue; "not_found_error"constant`

              - `NOT_FOUND_ERROR("not_found_error")`

          - `class RateLimitError:`

            - `message: String`

            - `type: JsonValue; "rate_limit_error"constant`

              - `RATE_LIMIT_ERROR("rate_limit_error")`

          - `class GatewayTimeoutError:`

            - `message: String`

            - `type: JsonValue; "timeout_error"constant`

              - `TIMEOUT_ERROR("timeout_error")`

          - `class ApiErrorObject:`

            - `message: String`

            - `type: JsonValue; "api_error"constant`

              - `API_ERROR("api_error")`

          - `class OverloadedError:`

            - `message: String`

            - `type: JsonValue; "overloaded_error"constant`

              - `OVERLOADED_ERROR("overloaded_error")`

        - `requestId: Optional<String>`

        - `type: JsonValue; "error"constant`

          - `ERROR("error")`

      - `type: JsonValue; "errored"constant`

        - `ERRORED("errored")`

    - `class MessageBatchCanceledResult:`

      - `type: JsonValue; "canceled"constant`

        - `CANCELED("canceled")`

    - `class MessageBatchExpiredResult:`

      - `type: JsonValue; "expired"constant`

        - `EXPIRED("expired")`

### Message Batch Request Counts

- `class MessageBatchRequestCounts:`

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

### Message Batch Result

- `class MessageBatchResult: A class that can be one of several variants.union`

  Processing result for this request.

  Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

  - `class MessageBatchSucceededResult:`

    - `message: Message`

      - `id: String`

        Unique object identifier.

        The format and length of IDs may change over time.

      - `content: List<ContentBlock>`

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

        - `class TextBlock:`

          - `citations: Optional<List<TextCitation>>`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `class CitationCharLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endCharIndex: Long`

              - `fileId: Optional<String>`

              - `startCharIndex: Long`

              - `type: JsonValue; "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class CitationPageLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endPageNumber: Long`

              - `fileId: Optional<String>`

              - `startPageNumber: Long`

              - `type: JsonValue; "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class CitationContentBlockLocation:`

              - `citedText: String`

              - `documentIndex: Long`

              - `documentTitle: Optional<String>`

              - `endBlockIndex: Long`

              - `fileId: Optional<String>`

              - `startBlockIndex: Long`

              - `type: JsonValue; "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class CitationsWebSearchResultLocation:`

              - `citedText: String`

              - `encryptedIndex: String`

              - `title: Optional<String>`

              - `type: JsonValue; "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `url: String`

            - `class CitationsSearchResultLocation:`

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

        - `class ThinkingBlock:`

          - `signature: String`

          - `thinking: String`

          - `type: JsonValue; "thinking"constant`

            - `THINKING("thinking")`

        - `class RedactedThinkingBlock:`

          - `data: String`

          - `type: JsonValue; "redacted_thinking"constant`

            - `REDACTED_THINKING("redacted_thinking")`

        - `class ToolUseBlock:`

          - `id: String`

          - `input: Input`

          - `name: String`

          - `type: JsonValue; "tool_use"constant`

            - `TOOL_USE("tool_use")`

        - `class ServerToolUseBlock:`

          - `id: String`

          - `input: Input`

          - `name: JsonValue; "web_search"constant`

            - `WEB_SEARCH("web_search")`

          - `type: JsonValue; "server_tool_use"constant`

            - `SERVER_TOOL_USE("server_tool_use")`

        - `class WebSearchToolResultBlock:`

          - `content: WebSearchToolResultBlockContent`

            - `class WebSearchToolResultError:`

              - `errorCode: ErrorCode`

                - `INVALID_TOOL_INPUT("invalid_tool_input")`

                - `UNAVAILABLE("unavailable")`

                - `MAX_USES_EXCEEDED("max_uses_exceeded")`

                - `TOO_MANY_REQUESTS("too_many_requests")`

                - `QUERY_TOO_LONG("query_too_long")`

              - `type: JsonValue; "web_search_tool_result_error"constant`

                - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

            - `List<WebSearchResultBlock>`

              - `encryptedContent: String`

              - `pageAge: Optional<String>`

              - `title: String`

              - `type: JsonValue; "web_search_result"constant`

                - `WEB_SEARCH_RESULT("web_search_result")`

              - `url: String`

          - `toolUseId: String`

          - `type: JsonValue; "web_search_tool_result"constant`

            - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

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

      - `stopReason: Optional<StopReason>`

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

      - `stopSequence: Optional<String>`

        Which custom stop sequence was generated, if any.

        This value will be a non-null string if one of your custom stop sequences was generated.

      - `type: JsonValue; "message"constant`

        Object type.

        For Messages, this is always `"message"`.

        - `MESSAGE("message")`

      - `usage: Usage`

        Billing and rate-limit usage.

        Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

        Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

        For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

        Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

        - `cacheCreation: Optional<CacheCreation>`

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

        - `serverToolUse: Optional<ServerToolUsage>`

          The number of server tool requests.

          - `webSearchRequests: Long`

            The number of web search tool requests.

        - `serviceTier: Optional<ServiceTier>`

          If the request used the priority, standard, or batch tier.

          - `STANDARD("standard")`

          - `PRIORITY("priority")`

          - `BATCH("batch")`

    - `type: JsonValue; "succeeded"constant`

      - `SUCCEEDED("succeeded")`

  - `class MessageBatchErroredResult:`

    - `error: ErrorResponse`

      - `error: ErrorObject`

        - `class InvalidRequestError:`

          - `message: String`

          - `type: JsonValue; "invalid_request_error"constant`

            - `INVALID_REQUEST_ERROR("invalid_request_error")`

        - `class AuthenticationError:`

          - `message: String`

          - `type: JsonValue; "authentication_error"constant`

            - `AUTHENTICATION_ERROR("authentication_error")`

        - `class BillingError:`

          - `message: String`

          - `type: JsonValue; "billing_error"constant`

            - `BILLING_ERROR("billing_error")`

        - `class PermissionError:`

          - `message: String`

          - `type: JsonValue; "permission_error"constant`

            - `PERMISSION_ERROR("permission_error")`

        - `class NotFoundError:`

          - `message: String`

          - `type: JsonValue; "not_found_error"constant`

            - `NOT_FOUND_ERROR("not_found_error")`

        - `class RateLimitError:`

          - `message: String`

          - `type: JsonValue; "rate_limit_error"constant`

            - `RATE_LIMIT_ERROR("rate_limit_error")`

        - `class GatewayTimeoutError:`

          - `message: String`

          - `type: JsonValue; "timeout_error"constant`

            - `TIMEOUT_ERROR("timeout_error")`

        - `class ApiErrorObject:`

          - `message: String`

          - `type: JsonValue; "api_error"constant`

            - `API_ERROR("api_error")`

        - `class OverloadedError:`

          - `message: String`

          - `type: JsonValue; "overloaded_error"constant`

            - `OVERLOADED_ERROR("overloaded_error")`

      - `requestId: Optional<String>`

      - `type: JsonValue; "error"constant`

        - `ERROR("error")`

    - `type: JsonValue; "errored"constant`

      - `ERRORED("errored")`

  - `class MessageBatchCanceledResult:`

    - `type: JsonValue; "canceled"constant`

      - `CANCELED("canceled")`

  - `class MessageBatchExpiredResult:`

    - `type: JsonValue; "expired"constant`

      - `EXPIRED("expired")`

### Message Batch Succeeded Result

- `class MessageBatchSucceededResult:`

  - `message: Message`

    - `id: String`

      Unique object identifier.

      The format and length of IDs may change over time.

    - `content: List<ContentBlock>`

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

      - `class TextBlock:`

        - `citations: Optional<List<TextCitation>>`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `class CitationCharLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endCharIndex: Long`

            - `fileId: Optional<String>`

            - `startCharIndex: Long`

            - `type: JsonValue; "char_location"constant`

              - `CHAR_LOCATION("char_location")`

          - `class CitationPageLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endPageNumber: Long`

            - `fileId: Optional<String>`

            - `startPageNumber: Long`

            - `type: JsonValue; "page_location"constant`

              - `PAGE_LOCATION("page_location")`

          - `class CitationContentBlockLocation:`

            - `citedText: String`

            - `documentIndex: Long`

            - `documentTitle: Optional<String>`

            - `endBlockIndex: Long`

            - `fileId: Optional<String>`

            - `startBlockIndex: Long`

            - `type: JsonValue; "content_block_location"constant`

              - `CONTENT_BLOCK_LOCATION("content_block_location")`

          - `class CitationsWebSearchResultLocation:`

            - `citedText: String`

            - `encryptedIndex: String`

            - `title: Optional<String>`

            - `type: JsonValue; "web_search_result_location"constant`

              - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

            - `url: String`

          - `class CitationsSearchResultLocation:`

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

      - `class ThinkingBlock:`

        - `signature: String`

        - `thinking: String`

        - `type: JsonValue; "thinking"constant`

          - `THINKING("thinking")`

      - `class RedactedThinkingBlock:`

        - `data: String`

        - `type: JsonValue; "redacted_thinking"constant`

          - `REDACTED_THINKING("redacted_thinking")`

      - `class ToolUseBlock:`

        - `id: String`

        - `input: Input`

        - `name: String`

        - `type: JsonValue; "tool_use"constant`

          - `TOOL_USE("tool_use")`

      - `class ServerToolUseBlock:`

        - `id: String`

        - `input: Input`

        - `name: JsonValue; "web_search"constant`

          - `WEB_SEARCH("web_search")`

        - `type: JsonValue; "server_tool_use"constant`

          - `SERVER_TOOL_USE("server_tool_use")`

      - `class WebSearchToolResultBlock:`

        - `content: WebSearchToolResultBlockContent`

          - `class WebSearchToolResultError:`

            - `errorCode: ErrorCode`

              - `INVALID_TOOL_INPUT("invalid_tool_input")`

              - `UNAVAILABLE("unavailable")`

              - `MAX_USES_EXCEEDED("max_uses_exceeded")`

              - `TOO_MANY_REQUESTS("too_many_requests")`

              - `QUERY_TOO_LONG("query_too_long")`

            - `type: JsonValue; "web_search_tool_result_error"constant`

              - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

          - `List<WebSearchResultBlock>`

            - `encryptedContent: String`

            - `pageAge: Optional<String>`

            - `title: String`

            - `type: JsonValue; "web_search_result"constant`

              - `WEB_SEARCH_RESULT("web_search_result")`

            - `url: String`

        - `toolUseId: String`

        - `type: JsonValue; "web_search_tool_result"constant`

          - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

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

    - `stopReason: Optional<StopReason>`

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

    - `stopSequence: Optional<String>`

      Which custom stop sequence was generated, if any.

      This value will be a non-null string if one of your custom stop sequences was generated.

    - `type: JsonValue; "message"constant`

      Object type.

      For Messages, this is always `"message"`.

      - `MESSAGE("message")`

    - `usage: Usage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cacheCreation: Optional<CacheCreation>`

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

      - `serverToolUse: Optional<ServerToolUsage>`

        The number of server tool requests.

        - `webSearchRequests: Long`

          The number of web search tool requests.

      - `serviceTier: Optional<ServiceTier>`

        If the request used the priority, standard, or batch tier.

        - `STANDARD("standard")`

        - `PRIORITY("priority")`

        - `BATCH("batch")`

  - `type: JsonValue; "succeeded"constant`

    - `SUCCEEDED("succeeded")`
