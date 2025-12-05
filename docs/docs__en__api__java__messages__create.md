## Create

`Message messages().create(MessageCreateParamsparams, RequestOptionsrequestOptions = RequestOptions.none())`

**post** `/v1/messages`

Send a structured list of input messages with text and/or image content, and the model will generate the next message in the conversation.

The Messages API can be used for either single queries or stateless multi-turn conversations.

Learn more about the Messages API in our [user guide](https://docs.claude.com/en/docs/initial-setup)

### Parameters

- `MessageCreateParams params`

  - `long maxTokens`

    The maximum number of tokens to generate before stopping.

    Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

    Different models have different maximum values for this parameter.  See [models](https://docs.claude.com/en/docs/models-overview) for details.

  - `List<MessageParam> messages`

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

      - `List<ContentBlockParam>`

        - `class TextBlockParam:`

          - `String text`

          - `JsonValue; type "text"constant`

            - `TEXT("text")`

          - `Optional<CacheControlEphemeral> cacheControl`

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

          - `Optional<List<TextCitationParam>> citations`

            - `class CitationCharLocationParam:`

              - `String citedText`

              - `long documentIndex`

              - `Optional<String> documentTitle`

              - `long endCharIndex`

              - `long startCharIndex`

              - `JsonValue; type "char_location"constant`

                - `CHAR_LOCATION("char_location")`

            - `class CitationPageLocationParam:`

              - `String citedText`

              - `long documentIndex`

              - `Optional<String> documentTitle`

              - `long endPageNumber`

              - `long startPageNumber`

              - `JsonValue; type "page_location"constant`

                - `PAGE_LOCATION("page_location")`

            - `class CitationContentBlockLocationParam:`

              - `String citedText`

              - `long documentIndex`

              - `Optional<String> documentTitle`

              - `long endBlockIndex`

              - `long startBlockIndex`

              - `JsonValue; type "content_block_location"constant`

                - `CONTENT_BLOCK_LOCATION("content_block_location")`

            - `class CitationWebSearchResultLocationParam:`

              - `String citedText`

              - `String encryptedIndex`

              - `Optional<String> title`

              - `JsonValue; type "web_search_result_location"constant`

                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

              - `String url`

            - `class CitationSearchResultLocationParam:`

              - `String citedText`

              - `long endBlockIndex`

              - `long searchResultIndex`

              - `String source`

              - `long startBlockIndex`

              - `Optional<String> title`

              - `JsonValue; type "search_result_location"constant`

                - `SEARCH_RESULT_LOCATION("search_result_location")`

        - `class ImageBlockParam:`

          - `Source source`

            - `class Base64ImageSource:`

              - `String data`

              - `MediaType mediaType`

                - `IMAGE_JPEG("image/jpeg")`

                - `IMAGE_PNG("image/png")`

                - `IMAGE_GIF("image/gif")`

                - `IMAGE_WEBP("image/webp")`

              - `JsonValue; type "base64"constant`

                - `BASE64("base64")`

            - `class UrlImageSource:`

              - `JsonValue; type "url"constant`

                - `URL("url")`

              - `String url`

          - `JsonValue; type "image"constant`

            - `IMAGE("image")`

          - `Optional<CacheControlEphemeral> cacheControl`

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

        - `class DocumentBlockParam:`

          - `Source source`

            - `class Base64PdfSource:`

              - `String data`

              - `JsonValue; mediaType "application/pdf"constant`

                - `APPLICATION_PDF("application/pdf")`

              - `JsonValue; type "base64"constant`

                - `BASE64("base64")`

            - `class PlainTextSource:`

              - `String data`

              - `JsonValue; mediaType "text/plain"constant`

                - `TEXT_PLAIN("text/plain")`

              - `JsonValue; type "text"constant`

                - `TEXT("text")`

            - `class ContentBlockSource:`

              - `Content content`

                - `String`

                - `List<ContentBlockSourceContent>`

                  - `class TextBlockParam:`

                    - `String text`

                    - `JsonValue; type "text"constant`

                      - `TEXT("text")`

                    - `Optional<CacheControlEphemeral> cacheControl`

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

                    - `Optional<List<TextCitationParam>> citations`

                      - `class CitationCharLocationParam:`

                        - `String citedText`

                        - `long documentIndex`

                        - `Optional<String> documentTitle`

                        - `long endCharIndex`

                        - `long startCharIndex`

                        - `JsonValue; type "char_location"constant`

                          - `CHAR_LOCATION("char_location")`

                      - `class CitationPageLocationParam:`

                        - `String citedText`

                        - `long documentIndex`

                        - `Optional<String> documentTitle`

                        - `long endPageNumber`

                        - `long startPageNumber`

                        - `JsonValue; type "page_location"constant`

                          - `PAGE_LOCATION("page_location")`

                      - `class CitationContentBlockLocationParam:`

                        - `String citedText`

                        - `long documentIndex`

                        - `Optional<String> documentTitle`

                        - `long endBlockIndex`

                        - `long startBlockIndex`

                        - `JsonValue; type "content_block_location"constant`

                          - `CONTENT_BLOCK_LOCATION("content_block_location")`

                      - `class CitationWebSearchResultLocationParam:`

                        - `String citedText`

                        - `String encryptedIndex`

                        - `Optional<String> title`

                        - `JsonValue; type "web_search_result_location"constant`

                          - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                        - `String url`

                      - `class CitationSearchResultLocationParam:`

                        - `String citedText`

                        - `long endBlockIndex`

                        - `long searchResultIndex`

                        - `String source`

                        - `long startBlockIndex`

                        - `Optional<String> title`

                        - `JsonValue; type "search_result_location"constant`

                          - `SEARCH_RESULT_LOCATION("search_result_location")`

                  - `class ImageBlockParam:`

                    - `Source source`

                      - `class Base64ImageSource:`

                        - `String data`

                        - `MediaType mediaType`

                          - `IMAGE_JPEG("image/jpeg")`

                          - `IMAGE_PNG("image/png")`

                          - `IMAGE_GIF("image/gif")`

                          - `IMAGE_WEBP("image/webp")`

                        - `JsonValue; type "base64"constant`

                          - `BASE64("base64")`

                      - `class UrlImageSource:`

                        - `JsonValue; type "url"constant`

                          - `URL("url")`

                        - `String url`

                    - `JsonValue; type "image"constant`

                      - `IMAGE("image")`

                    - `Optional<CacheControlEphemeral> cacheControl`

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

            - `class UrlPdfSource:`

              - `JsonValue; type "url"constant`

                - `URL("url")`

              - `String url`

          - `JsonValue; type "document"constant`

            - `DOCUMENT("document")`

          - `Optional<CacheControlEphemeral> cacheControl`

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

          - `Optional<CitationsConfigParam> citations`

            - `Optional<Boolean> enabled`

          - `Optional<String> context`

          - `Optional<String> title`

        - `class SearchResultBlockParam:`

          - `List<TextBlockParam> content`

            - `String text`

            - `JsonValue; type "text"constant`

              - `TEXT("text")`

            - `Optional<CacheControlEphemeral> cacheControl`

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

            - `Optional<List<TextCitationParam>> citations`

              - `class CitationCharLocationParam:`

                - `String citedText`

                - `long documentIndex`

                - `Optional<String> documentTitle`

                - `long endCharIndex`

                - `long startCharIndex`

                - `JsonValue; type "char_location"constant`

                  - `CHAR_LOCATION("char_location")`

              - `class CitationPageLocationParam:`

                - `String citedText`

                - `long documentIndex`

                - `Optional<String> documentTitle`

                - `long endPageNumber`

                - `long startPageNumber`

                - `JsonValue; type "page_location"constant`

                  - `PAGE_LOCATION("page_location")`

              - `class CitationContentBlockLocationParam:`

                - `String citedText`

                - `long documentIndex`

                - `Optional<String> documentTitle`

                - `long endBlockIndex`

                - `long startBlockIndex`

                - `JsonValue; type "content_block_location"constant`

                  - `CONTENT_BLOCK_LOCATION("content_block_location")`

              - `class CitationWebSearchResultLocationParam:`

                - `String citedText`

                - `String encryptedIndex`

                - `Optional<String> title`

                - `JsonValue; type "web_search_result_location"constant`

                  - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                - `String url`

              - `class CitationSearchResultLocationParam:`

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

          - `Optional<CacheControlEphemeral> cacheControl`

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

          - `Optional<CitationsConfigParam> citations`

            - `Optional<Boolean> enabled`

        - `class ThinkingBlockParam:`

          - `String signature`

          - `String thinking`

          - `JsonValue; type "thinking"constant`

            - `THINKING("thinking")`

        - `class RedactedThinkingBlockParam:`

          - `String data`

          - `JsonValue; type "redacted_thinking"constant`

            - `REDACTED_THINKING("redacted_thinking")`

        - `class ToolUseBlockParam:`

          - `String id`

          - `Input input`

          - `String name`

          - `JsonValue; type "tool_use"constant`

            - `TOOL_USE("tool_use")`

          - `Optional<CacheControlEphemeral> cacheControl`

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

        - `class ToolResultBlockParam:`

          - `String toolUseId`

          - `JsonValue; type "tool_result"constant`

            - `TOOL_RESULT("tool_result")`

          - `Optional<CacheControlEphemeral> cacheControl`

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

              - `class TextBlockParam:`

                - `String text`

                - `JsonValue; type "text"constant`

                  - `TEXT("text")`

                - `Optional<CacheControlEphemeral> cacheControl`

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

                - `Optional<List<TextCitationParam>> citations`

                  - `class CitationCharLocationParam:`

                    - `String citedText`

                    - `long documentIndex`

                    - `Optional<String> documentTitle`

                    - `long endCharIndex`

                    - `long startCharIndex`

                    - `JsonValue; type "char_location"constant`

                      - `CHAR_LOCATION("char_location")`

                  - `class CitationPageLocationParam:`

                    - `String citedText`

                    - `long documentIndex`

                    - `Optional<String> documentTitle`

                    - `long endPageNumber`

                    - `long startPageNumber`

                    - `JsonValue; type "page_location"constant`

                      - `PAGE_LOCATION("page_location")`

                  - `class CitationContentBlockLocationParam:`

                    - `String citedText`

                    - `long documentIndex`

                    - `Optional<String> documentTitle`

                    - `long endBlockIndex`

                    - `long startBlockIndex`

                    - `JsonValue; type "content_block_location"constant`

                      - `CONTENT_BLOCK_LOCATION("content_block_location")`

                  - `class CitationWebSearchResultLocationParam:`

                    - `String citedText`

                    - `String encryptedIndex`

                    - `Optional<String> title`

                    - `JsonValue; type "web_search_result_location"constant`

                      - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                    - `String url`

                  - `class CitationSearchResultLocationParam:`

                    - `String citedText`

                    - `long endBlockIndex`

                    - `long searchResultIndex`

                    - `String source`

                    - `long startBlockIndex`

                    - `Optional<String> title`

                    - `JsonValue; type "search_result_location"constant`

                      - `SEARCH_RESULT_LOCATION("search_result_location")`

              - `class ImageBlockParam:`

                - `Source source`

                  - `class Base64ImageSource:`

                    - `String data`

                    - `MediaType mediaType`

                      - `IMAGE_JPEG("image/jpeg")`

                      - `IMAGE_PNG("image/png")`

                      - `IMAGE_GIF("image/gif")`

                      - `IMAGE_WEBP("image/webp")`

                    - `JsonValue; type "base64"constant`

                      - `BASE64("base64")`

                  - `class UrlImageSource:`

                    - `JsonValue; type "url"constant`

                      - `URL("url")`

                    - `String url`

                - `JsonValue; type "image"constant`

                  - `IMAGE("image")`

                - `Optional<CacheControlEphemeral> cacheControl`

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

              - `class SearchResultBlockParam:`

                - `List<TextBlockParam> content`

                  - `String text`

                  - `JsonValue; type "text"constant`

                    - `TEXT("text")`

                  - `Optional<CacheControlEphemeral> cacheControl`

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

                  - `Optional<List<TextCitationParam>> citations`

                    - `class CitationCharLocationParam:`

                      - `String citedText`

                      - `long documentIndex`

                      - `Optional<String> documentTitle`

                      - `long endCharIndex`

                      - `long startCharIndex`

                      - `JsonValue; type "char_location"constant`

                        - `CHAR_LOCATION("char_location")`

                    - `class CitationPageLocationParam:`

                      - `String citedText`

                      - `long documentIndex`

                      - `Optional<String> documentTitle`

                      - `long endPageNumber`

                      - `long startPageNumber`

                      - `JsonValue; type "page_location"constant`

                        - `PAGE_LOCATION("page_location")`

                    - `class CitationContentBlockLocationParam:`

                      - `String citedText`

                      - `long documentIndex`

                      - `Optional<String> documentTitle`

                      - `long endBlockIndex`

                      - `long startBlockIndex`

                      - `JsonValue; type "content_block_location"constant`

                        - `CONTENT_BLOCK_LOCATION("content_block_location")`

                    - `class CitationWebSearchResultLocationParam:`

                      - `String citedText`

                      - `String encryptedIndex`

                      - `Optional<String> title`

                      - `JsonValue; type "web_search_result_location"constant`

                        - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                      - `String url`

                    - `class CitationSearchResultLocationParam:`

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

                - `Optional<CacheControlEphemeral> cacheControl`

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

                - `Optional<CitationsConfigParam> citations`

                  - `Optional<Boolean> enabled`

              - `class DocumentBlockParam:`

                - `Source source`

                  - `class Base64PdfSource:`

                    - `String data`

                    - `JsonValue; mediaType "application/pdf"constant`

                      - `APPLICATION_PDF("application/pdf")`

                    - `JsonValue; type "base64"constant`

                      - `BASE64("base64")`

                  - `class PlainTextSource:`

                    - `String data`

                    - `JsonValue; mediaType "text/plain"constant`

                      - `TEXT_PLAIN("text/plain")`

                    - `JsonValue; type "text"constant`

                      - `TEXT("text")`

                  - `class ContentBlockSource:`

                    - `Content content`

                      - `String`

                      - `List<ContentBlockSourceContent>`

                        - `class TextBlockParam:`

                          - `String text`

                          - `JsonValue; type "text"constant`

                            - `TEXT("text")`

                          - `Optional<CacheControlEphemeral> cacheControl`

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

                          - `Optional<List<TextCitationParam>> citations`

                            - `class CitationCharLocationParam:`

                              - `String citedText`

                              - `long documentIndex`

                              - `Optional<String> documentTitle`

                              - `long endCharIndex`

                              - `long startCharIndex`

                              - `JsonValue; type "char_location"constant`

                                - `CHAR_LOCATION("char_location")`

                            - `class CitationPageLocationParam:`

                              - `String citedText`

                              - `long documentIndex`

                              - `Optional<String> documentTitle`

                              - `long endPageNumber`

                              - `long startPageNumber`

                              - `JsonValue; type "page_location"constant`

                                - `PAGE_LOCATION("page_location")`

                            - `class CitationContentBlockLocationParam:`

                              - `String citedText`

                              - `long documentIndex`

                              - `Optional<String> documentTitle`

                              - `long endBlockIndex`

                              - `long startBlockIndex`

                              - `JsonValue; type "content_block_location"constant`

                                - `CONTENT_BLOCK_LOCATION("content_block_location")`

                            - `class CitationWebSearchResultLocationParam:`

                              - `String citedText`

                              - `String encryptedIndex`

                              - `Optional<String> title`

                              - `JsonValue; type "web_search_result_location"constant`

                                - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

                              - `String url`

                            - `class CitationSearchResultLocationParam:`

                              - `String citedText`

                              - `long endBlockIndex`

                              - `long searchResultIndex`

                              - `String source`

                              - `long startBlockIndex`

                              - `Optional<String> title`

                              - `JsonValue; type "search_result_location"constant`

                                - `SEARCH_RESULT_LOCATION("search_result_location")`

                        - `class ImageBlockParam:`

                          - `Source source`

                            - `class Base64ImageSource:`

                              - `String data`

                              - `MediaType mediaType`

                                - `IMAGE_JPEG("image/jpeg")`

                                - `IMAGE_PNG("image/png")`

                                - `IMAGE_GIF("image/gif")`

                                - `IMAGE_WEBP("image/webp")`

                              - `JsonValue; type "base64"constant`

                                - `BASE64("base64")`

                            - `class UrlImageSource:`

                              - `JsonValue; type "url"constant`

                                - `URL("url")`

                              - `String url`

                          - `JsonValue; type "image"constant`

                            - `IMAGE("image")`

                          - `Optional<CacheControlEphemeral> cacheControl`

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

                  - `class UrlPdfSource:`

                    - `JsonValue; type "url"constant`

                      - `URL("url")`

                    - `String url`

                - `JsonValue; type "document"constant`

                  - `DOCUMENT("document")`

                - `Optional<CacheControlEphemeral> cacheControl`

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

                - `Optional<CitationsConfigParam> citations`

                  - `Optional<Boolean> enabled`

                - `Optional<String> context`

                - `Optional<String> title`

          - `Optional<Boolean> isError`

        - `class ServerToolUseBlockParam:`

          - `String id`

          - `Input input`

          - `JsonValue; name "web_search"constant`

            - `WEB_SEARCH("web_search")`

          - `JsonValue; type "server_tool_use"constant`

            - `SERVER_TOOL_USE("server_tool_use")`

          - `Optional<CacheControlEphemeral> cacheControl`

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

        - `class WebSearchToolResultBlockParam:`

          - `WebSearchToolResultBlockParamContent content`

            - `List<WebSearchResultBlockParam>`

              - `String encryptedContent`

              - `String title`

              - `JsonValue; type "web_search_result"constant`

                - `WEB_SEARCH_RESULT("web_search_result")`

              - `String url`

              - `Optional<String> pageAge`

            - `class WebSearchToolRequestError:`

              - `ErrorCode errorCode`

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

          - `Optional<CacheControlEphemeral> cacheControl`

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

  - `Optional<Metadata> metadata`

    An object describing metadata about the request.

  - `Optional<ServiceTier> serviceTier`

    Determines whether to use priority capacity (if available) or standard capacity for this request.

    Anthropic offers different levels of service for your API requests. See [service-tiers](https://docs.claude.com/en/api/service-tiers) for details.

    - `AUTO("auto")`

    - `STANDARD_ONLY("standard_only")`

  - `Optional<List<String>> stopSequences`

    Custom text sequences that will cause the model to stop generating.

    Our models will normally stop when they have naturally completed their turn, which will result in a response `stop_reason` of `"end_turn"`.

    If you want the model to stop generating when it encounters custom strings of text, you can use the `stop_sequences` parameter. If the model encounters one of the custom sequences, the response `stop_reason` value will be `"stop_sequence"` and the response `stop_sequence` value will contain the matched stop sequence.

  - `Optional<System> system`

    System prompt.

    A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

    - `String`

    - `List<TextBlockParam>`

      - `String text`

      - `JsonValue; type "text"constant`

        - `TEXT("text")`

      - `Optional<CacheControlEphemeral> cacheControl`

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

      - `Optional<List<TextCitationParam>> citations`

        - `class CitationCharLocationParam:`

          - `String citedText`

          - `long documentIndex`

          - `Optional<String> documentTitle`

          - `long endCharIndex`

          - `long startCharIndex`

          - `JsonValue; type "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class CitationPageLocationParam:`

          - `String citedText`

          - `long documentIndex`

          - `Optional<String> documentTitle`

          - `long endPageNumber`

          - `long startPageNumber`

          - `JsonValue; type "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class CitationContentBlockLocationParam:`

          - `String citedText`

          - `long documentIndex`

          - `Optional<String> documentTitle`

          - `long endBlockIndex`

          - `long startBlockIndex`

          - `JsonValue; type "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class CitationWebSearchResultLocationParam:`

          - `String citedText`

          - `String encryptedIndex`

          - `Optional<String> title`

          - `JsonValue; type "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `String url`

        - `class CitationSearchResultLocationParam:`

          - `String citedText`

          - `long endBlockIndex`

          - `long searchResultIndex`

          - `String source`

          - `long startBlockIndex`

          - `Optional<String> title`

          - `JsonValue; type "search_result_location"constant`

            - `SEARCH_RESULT_LOCATION("search_result_location")`

  - `Optional<Double> temperature`

    Amount of randomness injected into the response.

    Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.

    Note that even with `temperature` of `0.0`, the results will not be fully deterministic.

  - `Optional<ThinkingConfigParam> thinking`

    Configuration for enabling Claude's extended thinking.

    When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `Optional<ToolChoice> toolChoice`

    How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `Optional<List<ToolUnion>> tools`

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

      - `Optional<CacheControlEphemeral> cacheControl`

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

      - `Optional<String> description`

        Description of what this tool does.

        Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

      - `Optional<Type> type`

        - `CUSTOM("custom")`

    - `class ToolBash20250124:`

      - `JsonValue; name "bash"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `BASH("bash")`

      - `JsonValue; type "bash_20250124"constant`

        - `BASH_20250124("bash_20250124")`

      - `Optional<CacheControlEphemeral> cacheControl`

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

    - `class ToolTextEditor20250124:`

      - `JsonValue; name "str_replace_editor"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_EDITOR("str_replace_editor")`

      - `JsonValue; type "text_editor_20250124"constant`

        - `TEXT_EDITOR_20250124("text_editor_20250124")`

      - `Optional<CacheControlEphemeral> cacheControl`

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

    - `class ToolTextEditor20250429:`

      - `JsonValue; name "str_replace_based_edit_tool"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

      - `JsonValue; type "text_editor_20250429"constant`

        - `TEXT_EDITOR_20250429("text_editor_20250429")`

      - `Optional<CacheControlEphemeral> cacheControl`

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

    - `class ToolTextEditor20250728:`

      - `JsonValue; name "str_replace_based_edit_tool"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `STR_REPLACE_BASED_EDIT_TOOL("str_replace_based_edit_tool")`

      - `JsonValue; type "text_editor_20250728"constant`

        - `TEXT_EDITOR_20250728("text_editor_20250728")`

      - `Optional<CacheControlEphemeral> cacheControl`

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

      - `Optional<Long> maxCharacters`

        Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

    - `class WebSearchTool20250305:`

      - `JsonValue; name "web_search"constant`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `WEB_SEARCH("web_search")`

      - `JsonValue; type "web_search_20250305"constant`

        - `WEB_SEARCH_20250305("web_search_20250305")`

      - `Optional<List<String>> allowedDomains`

        If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

      - `Optional<List<String>> blockedDomains`

        If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

      - `Optional<CacheControlEphemeral> cacheControl`

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

      - `Optional<Long> maxUses`

        Maximum number of times the tool can be used in the API request.

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

  - `Optional<Long> topK`

    Only sample from the top K options for each subsequent token.

    Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

    Recommended for advanced use cases only. You usually only need to use `temperature`.

  - `Optional<Double> topP`

    Use nucleus sampling.

    In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

    Recommended for advanced use cases only. You usually only need to use `temperature`.

### Returns

- `class Message:`

  - `String id`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `List<ContentBlock> content`

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

      - `Optional<List<TextCitation>> citations`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `class CitationCharLocation:`

          - `String citedText`

          - `long documentIndex`

          - `Optional<String> documentTitle`

          - `long endCharIndex`

          - `Optional<String> fileId`

          - `long startCharIndex`

          - `JsonValue; type "char_location"constant`

            - `CHAR_LOCATION("char_location")`

        - `class CitationPageLocation:`

          - `String citedText`

          - `long documentIndex`

          - `Optional<String> documentTitle`

          - `long endPageNumber`

          - `Optional<String> fileId`

          - `long startPageNumber`

          - `JsonValue; type "page_location"constant`

            - `PAGE_LOCATION("page_location")`

        - `class CitationContentBlockLocation:`

          - `String citedText`

          - `long documentIndex`

          - `Optional<String> documentTitle`

          - `long endBlockIndex`

          - `Optional<String> fileId`

          - `long startBlockIndex`

          - `JsonValue; type "content_block_location"constant`

            - `CONTENT_BLOCK_LOCATION("content_block_location")`

        - `class CitationsWebSearchResultLocation:`

          - `String citedText`

          - `String encryptedIndex`

          - `Optional<String> title`

          - `JsonValue; type "web_search_result_location"constant`

            - `WEB_SEARCH_RESULT_LOCATION("web_search_result_location")`

          - `String url`

        - `class CitationsSearchResultLocation:`

          - `String citedText`

          - `long endBlockIndex`

          - `long searchResultIndex`

          - `String source`

          - `long startBlockIndex`

          - `Optional<String> title`

          - `JsonValue; type "search_result_location"constant`

            - `SEARCH_RESULT_LOCATION("search_result_location")`

      - `String text`

      - `JsonValue; type "text"constant`

        - `TEXT("text")`

    - `class ThinkingBlock:`

      - `String signature`

      - `String thinking`

      - `JsonValue; type "thinking"constant`

        - `THINKING("thinking")`

    - `class RedactedThinkingBlock:`

      - `String data`

      - `JsonValue; type "redacted_thinking"constant`

        - `REDACTED_THINKING("redacted_thinking")`

    - `class ToolUseBlock:`

      - `String id`

      - `Input input`

      - `String name`

      - `JsonValue; type "tool_use"constant`

        - `TOOL_USE("tool_use")`

    - `class ServerToolUseBlock:`

      - `String id`

      - `Input input`

      - `JsonValue; name "web_search"constant`

        - `WEB_SEARCH("web_search")`

      - `JsonValue; type "server_tool_use"constant`

        - `SERVER_TOOL_USE("server_tool_use")`

    - `class WebSearchToolResultBlock:`

      - `WebSearchToolResultBlockContent content`

        - `class WebSearchToolResultError:`

          - `ErrorCode errorCode`

            - `INVALID_TOOL_INPUT("invalid_tool_input")`

            - `UNAVAILABLE("unavailable")`

            - `MAX_USES_EXCEEDED("max_uses_exceeded")`

            - `TOO_MANY_REQUESTS("too_many_requests")`

            - `QUERY_TOO_LONG("query_too_long")`

          - `JsonValue; type "web_search_tool_result_error"constant`

            - `WEB_SEARCH_TOOL_RESULT_ERROR("web_search_tool_result_error")`

        - `List<WebSearchResultBlock>`

          - `String encryptedContent`

          - `Optional<String> pageAge`

          - `String title`

          - `JsonValue; type "web_search_result"constant`

            - `WEB_SEARCH_RESULT("web_search_result")`

          - `String url`

      - `String toolUseId`

      - `JsonValue; type "web_search_tool_result"constant`

        - `WEB_SEARCH_TOOL_RESULT("web_search_tool_result")`

  - `Model model`

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

  - `JsonValue; role "assistant"constant`

    Conversational role of the generated message.

    This will always be `"assistant"`.

    - `ASSISTANT("assistant")`

  - `Optional<StopReason> stopReason`

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

  - `Optional<String> stopSequence`

    Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was generated.

  - `JsonValue; type "message"constant`

    Object type.

    For Messages, this is always `"message"`.

    - `MESSAGE("message")`

  - `Usage usage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `Optional<CacheCreation> cacheCreation`

      Breakdown of cached tokens by TTL

      - `long ephemeral1hInputTokens`

        The number of input tokens used to create the 1 hour cache entry.

      - `long ephemeral5mInputTokens`

        The number of input tokens used to create the 5 minute cache entry.

    - `Optional<Long> cacheCreationInputTokens`

      The number of input tokens used to create the cache entry.

    - `Optional<Long> cacheReadInputTokens`

      The number of input tokens read from the cache.

    - `long inputTokens`

      The number of input tokens which were used.

    - `long outputTokens`

      The number of output tokens which were used.

    - `Optional<ServerToolUsage> serverToolUse`

      The number of server tool requests.

      - `long webSearchRequests`

        The number of web search tool requests.

    - `Optional<ServiceTier> serviceTier`

      If the request used the priority, standard, or batch tier.

      - `STANDARD("standard")`

      - `PRIORITY("priority")`

      - `BATCH("batch")`

### Example

```java
package com.anthropic.example;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .maxTokens(1024L)
            .addUserMessage("Hello, world")
            .model(Model.CLAUDE_OPUS_4_5_20251101)
            .build();
        Message message = client.messages().create(params);
    }
}
```
