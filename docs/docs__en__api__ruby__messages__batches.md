# Batches

## Create

`messages.batches.create(**kwargs) -> MessageBatch`

**post** `/v1/messages/batches`

Send a batch of Message creation requests.

The Message Batches API can be used to process multiple Messages API requests at once. Once a Message Batch is created, it begins processing immediately. Batches can take up to 24 hours to complete.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `requests: Array[{ custom_id, params}]`

  List of requests for prompt completion. Each is an individual request to create a Message.

  - `custom_id: String`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `params: { max_tokens, messages, model, 11 more}`

    Messages API creation parameters for the individual request.

    See the [Messages API reference](https://docs.claude.com/en/api/messages) for full documentation on available parameters.

    - `max_tokens: Integer`

      The maximum number of tokens to generate before stopping.

      Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

      Different models have different maximum values for this parameter.  See [models](https://docs.claude.com/en/docs/models-overview) for details.

    - `messages: Array[MessageParam]`

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

      - `content: String | Array[ContentBlockParam]`

        - `String`

        - `Array[ContentBlockParam]`

          - `class TextBlockParam`

            - `text: String`

            - `type: :text`

              - `:text`

            - `cache_control: CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: :ephemeral`

                - `:ephemeral`

              - `ttl: :"5m" | :"1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `:"5m"`

                - `:"1h"`

            - `citations: Array[TextCitationParam]`

              - `class CitationCharLocationParam`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_char_index: Integer`

                - `start_char_index: Integer`

                - `type: :char_location`

                  - `:char_location`

              - `class CitationPageLocationParam`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_page_number: Integer`

                - `start_page_number: Integer`

                - `type: :page_location`

                  - `:page_location`

              - `class CitationContentBlockLocationParam`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_block_index: Integer`

                - `start_block_index: Integer`

                - `type: :content_block_location`

                  - `:content_block_location`

              - `class CitationWebSearchResultLocationParam`

                - `cited_text: String`

                - `encrypted_index: String`

                - `title: String`

                - `type: :web_search_result_location`

                  - `:web_search_result_location`

                - `url: String`

              - `class CitationSearchResultLocationParam`

                - `cited_text: String`

                - `end_block_index: Integer`

                - `search_result_index: Integer`

                - `source: String`

                - `start_block_index: Integer`

                - `title: String`

                - `type: :search_result_location`

                  - `:search_result_location`

          - `class ImageBlockParam`

            - `source: Base64ImageSource | URLImageSource`

              - `class Base64ImageSource`

                - `data: String`

                - `media_type: :"image/jpeg" | :"image/png" | :"image/gif" | :"image/webp"`

                  - `:"image/jpeg"`

                  - `:"image/png"`

                  - `:"image/gif"`

                  - `:"image/webp"`

                - `type: :base64`

                  - `:base64`

              - `class URLImageSource`

                - `type: :url`

                  - `:url`

                - `url: String`

            - `type: :image`

              - `:image`

            - `cache_control: CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: :ephemeral`

                - `:ephemeral`

              - `ttl: :"5m" | :"1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `:"5m"`

                - `:"1h"`

          - `class DocumentBlockParam`

            - `source: Base64PDFSource | PlainTextSource | ContentBlockSource | URLPDFSource`

              - `class Base64PDFSource`

                - `data: String`

                - `media_type: :"application/pdf"`

                  - `:"application/pdf"`

                - `type: :base64`

                  - `:base64`

              - `class PlainTextSource`

                - `data: String`

                - `media_type: :"text/plain"`

                  - `:"text/plain"`

                - `type: :text`

                  - `:text`

              - `class ContentBlockSource`

                - `content: String | Array[ContentBlockSourceContent]`

                  - `String`

                  - `Array[ContentBlockSourceContent]`

                    - `class TextBlockParam`

                      - `text: String`

                      - `type: :text`

                        - `:text`

                      - `cache_control: CacheControlEphemeral`

                        Create a cache control breakpoint at this content block.

                        - `type: :ephemeral`

                          - `:ephemeral`

                        - `ttl: :"5m" | :"1h"`

                          The time-to-live for the cache control breakpoint.

                          This may be one the following values:

                          - `5m`: 5 minutes
                          - `1h`: 1 hour

                          Defaults to `5m`.

                          - `:"5m"`

                          - `:"1h"`

                      - `citations: Array[TextCitationParam]`

                        - `class CitationCharLocationParam`

                          - `cited_text: String`

                          - `document_index: Integer`

                          - `document_title: String`

                          - `end_char_index: Integer`

                          - `start_char_index: Integer`

                          - `type: :char_location`

                            - `:char_location`

                        - `class CitationPageLocationParam`

                          - `cited_text: String`

                          - `document_index: Integer`

                          - `document_title: String`

                          - `end_page_number: Integer`

                          - `start_page_number: Integer`

                          - `type: :page_location`

                            - `:page_location`

                        - `class CitationContentBlockLocationParam`

                          - `cited_text: String`

                          - `document_index: Integer`

                          - `document_title: String`

                          - `end_block_index: Integer`

                          - `start_block_index: Integer`

                          - `type: :content_block_location`

                            - `:content_block_location`

                        - `class CitationWebSearchResultLocationParam`

                          - `cited_text: String`

                          - `encrypted_index: String`

                          - `title: String`

                          - `type: :web_search_result_location`

                            - `:web_search_result_location`

                          - `url: String`

                        - `class CitationSearchResultLocationParam`

                          - `cited_text: String`

                          - `end_block_index: Integer`

                          - `search_result_index: Integer`

                          - `source: String`

                          - `start_block_index: Integer`

                          - `title: String`

                          - `type: :search_result_location`

                            - `:search_result_location`

                    - `class ImageBlockParam`

                      - `source: Base64ImageSource | URLImageSource`

                        - `class Base64ImageSource`

                          - `data: String`

                          - `media_type: :"image/jpeg" | :"image/png" | :"image/gif" | :"image/webp"`

                            - `:"image/jpeg"`

                            - `:"image/png"`

                            - `:"image/gif"`

                            - `:"image/webp"`

                          - `type: :base64`

                            - `:base64`

                        - `class URLImageSource`

                          - `type: :url`

                            - `:url`

                          - `url: String`

                      - `type: :image`

                        - `:image`

                      - `cache_control: CacheControlEphemeral`

                        Create a cache control breakpoint at this content block.

                        - `type: :ephemeral`

                          - `:ephemeral`

                        - `ttl: :"5m" | :"1h"`

                          The time-to-live for the cache control breakpoint.

                          This may be one the following values:

                          - `5m`: 5 minutes
                          - `1h`: 1 hour

                          Defaults to `5m`.

                          - `:"5m"`

                          - `:"1h"`

                - `type: :content`

                  - `:content`

              - `class URLPDFSource`

                - `type: :url`

                  - `:url`

                - `url: String`

            - `type: :document`

              - `:document`

            - `cache_control: CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: :ephemeral`

                - `:ephemeral`

              - `ttl: :"5m" | :"1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `:"5m"`

                - `:"1h"`

            - `citations: CitationsConfigParam`

              - `enabled: bool`

            - `context: String`

            - `title: String`

          - `class SearchResultBlockParam`

            - `content: Array[TextBlockParam]`

              - `text: String`

              - `type: :text`

                - `:text`

              - `cache_control: CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: :ephemeral`

                  - `:ephemeral`

                - `ttl: :"5m" | :"1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `:"5m"`

                  - `:"1h"`

              - `citations: Array[TextCitationParam]`

                - `class CitationCharLocationParam`

                  - `cited_text: String`

                  - `document_index: Integer`

                  - `document_title: String`

                  - `end_char_index: Integer`

                  - `start_char_index: Integer`

                  - `type: :char_location`

                    - `:char_location`

                - `class CitationPageLocationParam`

                  - `cited_text: String`

                  - `document_index: Integer`

                  - `document_title: String`

                  - `end_page_number: Integer`

                  - `start_page_number: Integer`

                  - `type: :page_location`

                    - `:page_location`

                - `class CitationContentBlockLocationParam`

                  - `cited_text: String`

                  - `document_index: Integer`

                  - `document_title: String`

                  - `end_block_index: Integer`

                  - `start_block_index: Integer`

                  - `type: :content_block_location`

                    - `:content_block_location`

                - `class CitationWebSearchResultLocationParam`

                  - `cited_text: String`

                  - `encrypted_index: String`

                  - `title: String`

                  - `type: :web_search_result_location`

                    - `:web_search_result_location`

                  - `url: String`

                - `class CitationSearchResultLocationParam`

                  - `cited_text: String`

                  - `end_block_index: Integer`

                  - `search_result_index: Integer`

                  - `source: String`

                  - `start_block_index: Integer`

                  - `title: String`

                  - `type: :search_result_location`

                    - `:search_result_location`

            - `source: String`

            - `title: String`

            - `type: :search_result`

              - `:search_result`

            - `cache_control: CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: :ephemeral`

                - `:ephemeral`

              - `ttl: :"5m" | :"1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `:"5m"`

                - `:"1h"`

            - `citations: CitationsConfigParam`

              - `enabled: bool`

          - `class ThinkingBlockParam`

            - `signature: String`

            - `thinking: String`

            - `type: :thinking`

              - `:thinking`

          - `class RedactedThinkingBlockParam`

            - `data: String`

            - `type: :redacted_thinking`

              - `:redacted_thinking`

          - `class ToolUseBlockParam`

            - `id: String`

            - `input: Hash[Symbol, untyped]`

            - `name: String`

            - `type: :tool_use`

              - `:tool_use`

            - `cache_control: CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: :ephemeral`

                - `:ephemeral`

              - `ttl: :"5m" | :"1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `:"5m"`

                - `:"1h"`

          - `class ToolResultBlockParam`

            - `tool_use_id: String`

            - `type: :tool_result`

              - `:tool_result`

            - `cache_control: CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: :ephemeral`

                - `:ephemeral`

              - `ttl: :"5m" | :"1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `:"5m"`

                - `:"1h"`

            - `content: String | Array[TextBlockParam | ImageBlockParam | SearchResultBlockParam | DocumentBlockParam]`

              - `String`

              - `Array[TextBlockParam | ImageBlockParam | SearchResultBlockParam | DocumentBlockParam]`

                - `class TextBlockParam`

                  - `text: String`

                  - `type: :text`

                    - `:text`

                  - `cache_control: CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: :ephemeral`

                      - `:ephemeral`

                    - `ttl: :"5m" | :"1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `:"5m"`

                      - `:"1h"`

                  - `citations: Array[TextCitationParam]`

                    - `class CitationCharLocationParam`

                      - `cited_text: String`

                      - `document_index: Integer`

                      - `document_title: String`

                      - `end_char_index: Integer`

                      - `start_char_index: Integer`

                      - `type: :char_location`

                        - `:char_location`

                    - `class CitationPageLocationParam`

                      - `cited_text: String`

                      - `document_index: Integer`

                      - `document_title: String`

                      - `end_page_number: Integer`

                      - `start_page_number: Integer`

                      - `type: :page_location`

                        - `:page_location`

                    - `class CitationContentBlockLocationParam`

                      - `cited_text: String`

                      - `document_index: Integer`

                      - `document_title: String`

                      - `end_block_index: Integer`

                      - `start_block_index: Integer`

                      - `type: :content_block_location`

                        - `:content_block_location`

                    - `class CitationWebSearchResultLocationParam`

                      - `cited_text: String`

                      - `encrypted_index: String`

                      - `title: String`

                      - `type: :web_search_result_location`

                        - `:web_search_result_location`

                      - `url: String`

                    - `class CitationSearchResultLocationParam`

                      - `cited_text: String`

                      - `end_block_index: Integer`

                      - `search_result_index: Integer`

                      - `source: String`

                      - `start_block_index: Integer`

                      - `title: String`

                      - `type: :search_result_location`

                        - `:search_result_location`

                - `class ImageBlockParam`

                  - `source: Base64ImageSource | URLImageSource`

                    - `class Base64ImageSource`

                      - `data: String`

                      - `media_type: :"image/jpeg" | :"image/png" | :"image/gif" | :"image/webp"`

                        - `:"image/jpeg"`

                        - `:"image/png"`

                        - `:"image/gif"`

                        - `:"image/webp"`

                      - `type: :base64`

                        - `:base64`

                    - `class URLImageSource`

                      - `type: :url`

                        - `:url`

                      - `url: String`

                  - `type: :image`

                    - `:image`

                  - `cache_control: CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: :ephemeral`

                      - `:ephemeral`

                    - `ttl: :"5m" | :"1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `:"5m"`

                      - `:"1h"`

                - `class SearchResultBlockParam`

                  - `content: Array[TextBlockParam]`

                    - `text: String`

                    - `type: :text`

                      - `:text`

                    - `cache_control: CacheControlEphemeral`

                      Create a cache control breakpoint at this content block.

                      - `type: :ephemeral`

                        - `:ephemeral`

                      - `ttl: :"5m" | :"1h"`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `:"5m"`

                        - `:"1h"`

                    - `citations: Array[TextCitationParam]`

                      - `class CitationCharLocationParam`

                        - `cited_text: String`

                        - `document_index: Integer`

                        - `document_title: String`

                        - `end_char_index: Integer`

                        - `start_char_index: Integer`

                        - `type: :char_location`

                          - `:char_location`

                      - `class CitationPageLocationParam`

                        - `cited_text: String`

                        - `document_index: Integer`

                        - `document_title: String`

                        - `end_page_number: Integer`

                        - `start_page_number: Integer`

                        - `type: :page_location`

                          - `:page_location`

                      - `class CitationContentBlockLocationParam`

                        - `cited_text: String`

                        - `document_index: Integer`

                        - `document_title: String`

                        - `end_block_index: Integer`

                        - `start_block_index: Integer`

                        - `type: :content_block_location`

                          - `:content_block_location`

                      - `class CitationWebSearchResultLocationParam`

                        - `cited_text: String`

                        - `encrypted_index: String`

                        - `title: String`

                        - `type: :web_search_result_location`

                          - `:web_search_result_location`

                        - `url: String`

                      - `class CitationSearchResultLocationParam`

                        - `cited_text: String`

                        - `end_block_index: Integer`

                        - `search_result_index: Integer`

                        - `source: String`

                        - `start_block_index: Integer`

                        - `title: String`

                        - `type: :search_result_location`

                          - `:search_result_location`

                  - `source: String`

                  - `title: String`

                  - `type: :search_result`

                    - `:search_result`

                  - `cache_control: CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: :ephemeral`

                      - `:ephemeral`

                    - `ttl: :"5m" | :"1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `:"5m"`

                      - `:"1h"`

                  - `citations: CitationsConfigParam`

                    - `enabled: bool`

                - `class DocumentBlockParam`

                  - `source: Base64PDFSource | PlainTextSource | ContentBlockSource | URLPDFSource`

                    - `class Base64PDFSource`

                      - `data: String`

                      - `media_type: :"application/pdf"`

                        - `:"application/pdf"`

                      - `type: :base64`

                        - `:base64`

                    - `class PlainTextSource`

                      - `data: String`

                      - `media_type: :"text/plain"`

                        - `:"text/plain"`

                      - `type: :text`

                        - `:text`

                    - `class ContentBlockSource`

                      - `content: String | Array[ContentBlockSourceContent]`

                        - `String`

                        - `Array[ContentBlockSourceContent]`

                          - `class TextBlockParam`

                            - `text: String`

                            - `type: :text`

                              - `:text`

                            - `cache_control: CacheControlEphemeral`

                              Create a cache control breakpoint at this content block.

                              - `type: :ephemeral`

                                - `:ephemeral`

                              - `ttl: :"5m" | :"1h"`

                                The time-to-live for the cache control breakpoint.

                                This may be one the following values:

                                - `5m`: 5 minutes
                                - `1h`: 1 hour

                                Defaults to `5m`.

                                - `:"5m"`

                                - `:"1h"`

                            - `citations: Array[TextCitationParam]`

                              - `class CitationCharLocationParam`

                                - `cited_text: String`

                                - `document_index: Integer`

                                - `document_title: String`

                                - `end_char_index: Integer`

                                - `start_char_index: Integer`

                                - `type: :char_location`

                                  - `:char_location`

                              - `class CitationPageLocationParam`

                                - `cited_text: String`

                                - `document_index: Integer`

                                - `document_title: String`

                                - `end_page_number: Integer`

                                - `start_page_number: Integer`

                                - `type: :page_location`

                                  - `:page_location`

                              - `class CitationContentBlockLocationParam`

                                - `cited_text: String`

                                - `document_index: Integer`

                                - `document_title: String`

                                - `end_block_index: Integer`

                                - `start_block_index: Integer`

                                - `type: :content_block_location`

                                  - `:content_block_location`

                              - `class CitationWebSearchResultLocationParam`

                                - `cited_text: String`

                                - `encrypted_index: String`

                                - `title: String`

                                - `type: :web_search_result_location`

                                  - `:web_search_result_location`

                                - `url: String`

                              - `class CitationSearchResultLocationParam`

                                - `cited_text: String`

                                - `end_block_index: Integer`

                                - `search_result_index: Integer`

                                - `source: String`

                                - `start_block_index: Integer`

                                - `title: String`

                                - `type: :search_result_location`

                                  - `:search_result_location`

                          - `class ImageBlockParam`

                            - `source: Base64ImageSource | URLImageSource`

                              - `class Base64ImageSource`

                                - `data: String`

                                - `media_type: :"image/jpeg" | :"image/png" | :"image/gif" | :"image/webp"`

                                  - `:"image/jpeg"`

                                  - `:"image/png"`

                                  - `:"image/gif"`

                                  - `:"image/webp"`

                                - `type: :base64`

                                  - `:base64`

                              - `class URLImageSource`

                                - `type: :url`

                                  - `:url`

                                - `url: String`

                            - `type: :image`

                              - `:image`

                            - `cache_control: CacheControlEphemeral`

                              Create a cache control breakpoint at this content block.

                              - `type: :ephemeral`

                                - `:ephemeral`

                              - `ttl: :"5m" | :"1h"`

                                The time-to-live for the cache control breakpoint.

                                This may be one the following values:

                                - `5m`: 5 minutes
                                - `1h`: 1 hour

                                Defaults to `5m`.

                                - `:"5m"`

                                - `:"1h"`

                      - `type: :content`

                        - `:content`

                    - `class URLPDFSource`

                      - `type: :url`

                        - `:url`

                      - `url: String`

                  - `type: :document`

                    - `:document`

                  - `cache_control: CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: :ephemeral`

                      - `:ephemeral`

                    - `ttl: :"5m" | :"1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `:"5m"`

                      - `:"1h"`

                  - `citations: CitationsConfigParam`

                    - `enabled: bool`

                  - `context: String`

                  - `title: String`

            - `is_error: bool`

          - `class ServerToolUseBlockParam`

            - `id: String`

            - `input: Hash[Symbol, untyped]`

            - `name: :web_search`

              - `:web_search`

            - `type: :server_tool_use`

              - `:server_tool_use`

            - `cache_control: CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: :ephemeral`

                - `:ephemeral`

              - `ttl: :"5m" | :"1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `:"5m"`

                - `:"1h"`

          - `class WebSearchToolResultBlockParam`

            - `content: WebSearchToolResultBlockParamContent`

              - `Array[WebSearchResultBlockParam]`

                - `encrypted_content: String`

                - `title: String`

                - `type: :web_search_result`

                  - `:web_search_result`

                - `url: String`

                - `page_age: String`

              - `class WebSearchToolRequestError`

                - `error_code: :invalid_tool_input | :unavailable | :max_uses_exceeded | 2 more`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:max_uses_exceeded`

                  - `:too_many_requests`

                  - `:query_too_long`

                - `type: :web_search_tool_result_error`

                  - `:web_search_tool_result_error`

            - `tool_use_id: String`

            - `type: :web_search_tool_result`

              - `:web_search_tool_result`

            - `cache_control: CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: :ephemeral`

                - `:ephemeral`

              - `ttl: :"5m" | :"1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `:"5m"`

                - `:"1h"`

      - `role: :user | :assistant`

        - `:user`

        - `:assistant`

    - `model: Model`

      The model that will complete your prompt.

      See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

      - `:"claude-opus-4-5-20251101" | :"claude-opus-4-5" | :"claude-3-7-sonnet-latest" | 17 more`

        The model that will complete your prompt.

        See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

        - `:"claude-opus-4-5-20251101"`

          Premium model combining maximum intelligence with practical performance

        - `:"claude-opus-4-5"`

          Premium model combining maximum intelligence with practical performance

        - `:"claude-3-7-sonnet-latest"`

          High-performance model with early extended thinking

        - `:"claude-3-7-sonnet-20250219"`

          High-performance model with early extended thinking

        - `:"claude-3-5-haiku-latest"`

          Fastest and most compact model for near-instant responsiveness

        - `:"claude-3-5-haiku-20241022"`

          Our fastest model

        - `:"claude-haiku-4-5"`

          Hybrid model, capable of near-instant responses and extended thinking

        - `:"claude-haiku-4-5-20251001"`

          Hybrid model, capable of near-instant responses and extended thinking

        - `:"claude-sonnet-4-20250514"`

          High-performance model with extended thinking

        - `:"claude-sonnet-4-0"`

          High-performance model with extended thinking

        - `:"claude-4-sonnet-20250514"`

          High-performance model with extended thinking

        - `:"claude-sonnet-4-5"`

          Our best model for real-world agents and coding

        - `:"claude-sonnet-4-5-20250929"`

          Our best model for real-world agents and coding

        - `:"claude-opus-4-0"`

          Our most capable model

        - `:"claude-opus-4-20250514"`

          Our most capable model

        - `:"claude-4-opus-20250514"`

          Our most capable model

        - `:"claude-opus-4-1-20250805"`

          Our most capable model

        - `:"claude-3-opus-latest"`

          Excels at writing and complex tasks

        - `:"claude-3-opus-20240229"`

          Excels at writing and complex tasks

        - `:"claude-3-haiku-20240307"`

          Our previous most fast and cost-effective

      - `String`

    - `metadata: Metadata`

      An object describing metadata about the request.

      - `user_id: String`

        An external identifier for the user who is associated with the request.

        This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

    - `service_tier: :auto | :standard_only`

      Determines whether to use priority capacity (if available) or standard capacity for this request.

      Anthropic offers different levels of service for your API requests. See [service-tiers](https://docs.claude.com/en/api/service-tiers) for details.

      - `:auto`

      - `:standard_only`

    - `stop_sequences: Array[String]`

      Custom text sequences that will cause the model to stop generating.

      Our models will normally stop when they have naturally completed their turn, which will result in a response `stop_reason` of `"end_turn"`.

      If you want the model to stop generating when it encounters custom strings of text, you can use the `stop_sequences` parameter. If the model encounters one of the custom sequences, the response `stop_reason` value will be `"stop_sequence"` and the response `stop_sequence` value will contain the matched stop sequence.

    - `stream: bool`

      Whether to incrementally stream the response using server-sent events.

      See [streaming](https://docs.claude.com/en/api/messages-streaming) for details.

    - `system_: String | Array[TextBlockParam]`

      System prompt.

      A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

      - `String`

      - `Array[TextBlockParam]`

        - `text: String`

        - `type: :text`

          - `:text`

        - `cache_control: CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: :ephemeral`

            - `:ephemeral`

          - `ttl: :"5m" | :"1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `:"5m"`

            - `:"1h"`

        - `citations: Array[TextCitationParam]`

          - `class CitationCharLocationParam`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_char_index: Integer`

            - `start_char_index: Integer`

            - `type: :char_location`

              - `:char_location`

          - `class CitationPageLocationParam`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_page_number: Integer`

            - `start_page_number: Integer`

            - `type: :page_location`

              - `:page_location`

          - `class CitationContentBlockLocationParam`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_block_index: Integer`

            - `start_block_index: Integer`

            - `type: :content_block_location`

              - `:content_block_location`

          - `class CitationWebSearchResultLocationParam`

            - `cited_text: String`

            - `encrypted_index: String`

            - `title: String`

            - `type: :web_search_result_location`

              - `:web_search_result_location`

            - `url: String`

          - `class CitationSearchResultLocationParam`

            - `cited_text: String`

            - `end_block_index: Integer`

            - `search_result_index: Integer`

            - `source: String`

            - `start_block_index: Integer`

            - `title: String`

            - `type: :search_result_location`

              - `:search_result_location`

    - `temperature: Float`

      Amount of randomness injected into the response.

      Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.

      Note that even with `temperature` of `0.0`, the results will not be fully deterministic.

    - `thinking: ThinkingConfigParam`

      Configuration for enabling Claude's extended thinking.

      When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

      See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

      - `class ThinkingConfigEnabled`

        - `budget_tokens: Integer`

          Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

          Must be ≥1024 and less than `max_tokens`.

          See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

        - `type: :enabled`

          - `:enabled`

      - `class ThinkingConfigDisabled`

        - `type: :disabled`

          - `:disabled`

    - `tool_choice: ToolChoice`

      How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

      - `class ToolChoiceAuto`

        The model will automatically decide whether to use tools.

        - `type: :auto`

          - `:auto`

        - `disable_parallel_tool_use: bool`

          Whether to disable parallel tool use.

          Defaults to `false`. If set to `true`, the model will output at most one tool use.

      - `class ToolChoiceAny`

        The model will use any available tools.

        - `type: :any`

          - `:any`

        - `disable_parallel_tool_use: bool`

          Whether to disable parallel tool use.

          Defaults to `false`. If set to `true`, the model will output exactly one tool use.

      - `class ToolChoiceTool`

        The model will use the specified tool with `tool_choice.name`.

        - `name: String`

          The name of the tool to use.

        - `type: :tool`

          - `:tool`

        - `disable_parallel_tool_use: bool`

          Whether to disable parallel tool use.

          Defaults to `false`. If set to `true`, the model will output exactly one tool use.

      - `class ToolChoiceNone`

        The model will not be allowed to use tools.

        - `type: :none`

          - `:none`

    - `tools: Array[ToolUnion]`

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

      - `class Tool`

        - `input_schema: { type, properties, required}`

          [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

          This defines the shape of the `input` that your tool accepts and that the model will produce.

          - `type: :object`

            - `:object`

          - `properties: Hash[Symbol, untyped]`

          - `required: Array[String]`

        - `name: String`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

        - `cache_control: CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: :ephemeral`

            - `:ephemeral`

          - `ttl: :"5m" | :"1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `:"5m"`

            - `:"1h"`

        - `description: String`

          Description of what this tool does.

          Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

        - `type: :custom`

          - `:custom`

      - `class ToolBash20250124`

        - `name: :bash`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:bash`

        - `type: :bash_20250124`

          - `:bash_20250124`

        - `cache_control: CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: :ephemeral`

            - `:ephemeral`

          - `ttl: :"5m" | :"1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `:"5m"`

            - `:"1h"`

      - `class ToolTextEditor20250124`

        - `name: :str_replace_editor`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:str_replace_editor`

        - `type: :text_editor_20250124`

          - `:text_editor_20250124`

        - `cache_control: CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: :ephemeral`

            - `:ephemeral`

          - `ttl: :"5m" | :"1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `:"5m"`

            - `:"1h"`

      - `class ToolTextEditor20250429`

        - `name: :str_replace_based_edit_tool`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:str_replace_based_edit_tool`

        - `type: :text_editor_20250429`

          - `:text_editor_20250429`

        - `cache_control: CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: :ephemeral`

            - `:ephemeral`

          - `ttl: :"5m" | :"1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `:"5m"`

            - `:"1h"`

      - `class ToolTextEditor20250728`

        - `name: :str_replace_based_edit_tool`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:str_replace_based_edit_tool`

        - `type: :text_editor_20250728`

          - `:text_editor_20250728`

        - `cache_control: CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: :ephemeral`

            - `:ephemeral`

          - `ttl: :"5m" | :"1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `:"5m"`

            - `:"1h"`

        - `max_characters: Integer`

          Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

      - `class WebSearchTool20250305`

        - `name: :web_search`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:web_search`

        - `type: :web_search_20250305`

          - `:web_search_20250305`

        - `allowed_domains: Array[String]`

          If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

        - `blocked_domains: Array[String]`

          If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

        - `cache_control: CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: :ephemeral`

            - `:ephemeral`

          - `ttl: :"5m" | :"1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `:"5m"`

            - `:"1h"`

        - `max_uses: Integer`

          Maximum number of times the tool can be used in the API request.

        - `user_location: { type, city, country, 2 more}`

          Parameters for the user's location. Used to provide more relevant search results.

          - `type: :approximate`

            - `:approximate`

          - `city: String`

            The city of the user.

          - `country: String`

            The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

          - `region: String`

            The region of the user.

          - `timezone: String`

            The [IANA timezone](https://nodatime.org/TimeZones) of the user.

    - `top_k: Integer`

      Only sample from the top K options for each subsequent token.

      Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

      Recommended for advanced use cases only. You usually only need to use `temperature`.

    - `top_p: Float`

      Use nucleus sampling.

      In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

      Recommended for advanced use cases only. You usually only need to use `temperature`.

### Returns

- `class MessageBatch`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archived_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancel_initiated_at: Time`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `created_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `ended_at: Time`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expires_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processing_status: :in_progress | :canceling | :ended`

    Processing status of the Message Batch.

    - `:in_progress`

    - `:canceling`

    - `:ended`

  - `request_counts: MessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: Integer`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: Integer`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: Integer`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: Integer`

      Number of requests in the Message Batch that are processing.

    - `succeeded: Integer`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `results_url: String`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: :message_batch`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `:message_batch`

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

message_batch = anthropic.messages.batches.create(
  requests: [
    {
      custom_id: "my-custom-id-1",
      params: {max_tokens: 1024, messages: [{content: "Hello, world", role: :user}], model: :"claude-opus-4-5-20251101"}
    }
  ]
)

puts(message_batch)
```

## Retrieve

`messages.batches.retrieve(message_batch_id) -> MessageBatch`

**get** `/v1/messages/batches/{message_batch_id}`

This endpoint is idempotent and can be used to poll for Message Batch completion. To access the results of a Message Batch, make a request to the `results_url` field in the response.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `message_batch_id: String`

  ID of the Message Batch.

### Returns

- `class MessageBatch`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archived_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancel_initiated_at: Time`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `created_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `ended_at: Time`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expires_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processing_status: :in_progress | :canceling | :ended`

    Processing status of the Message Batch.

    - `:in_progress`

    - `:canceling`

    - `:ended`

  - `request_counts: MessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: Integer`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: Integer`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: Integer`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: Integer`

      Number of requests in the Message Batch that are processing.

    - `succeeded: Integer`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `results_url: String`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: :message_batch`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `:message_batch`

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

message_batch = anthropic.messages.batches.retrieve("message_batch_id")

puts(message_batch)
```

## List

`messages.batches.list(**kwargs) -> Page<MessageBatch>`

**get** `/v1/messages/batches`

List all Message Batches within a Workspace. Most recently created batches are returned first.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `after_id: String`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: String`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `limit: Integer`

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

### Returns

- `class MessageBatch`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archived_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancel_initiated_at: Time`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `created_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `ended_at: Time`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expires_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processing_status: :in_progress | :canceling | :ended`

    Processing status of the Message Batch.

    - `:in_progress`

    - `:canceling`

    - `:ended`

  - `request_counts: MessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: Integer`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: Integer`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: Integer`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: Integer`

      Number of requests in the Message Batch that are processing.

    - `succeeded: Integer`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `results_url: String`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: :message_batch`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `:message_batch`

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

page = anthropic.messages.batches.list

puts(page)
```

## Cancel

`messages.batches.cancel(message_batch_id) -> MessageBatch`

**post** `/v1/messages/batches/{message_batch_id}/cancel`

Batches may be canceled any time before processing ends. Once cancellation is initiated, the batch enters a `canceling` state, at which time the system may complete any in-progress, non-interruptible requests before finalizing cancellation.

The number of canceled requests is specified in `request_counts`. To determine which requests were canceled, check the individual results within the batch. Note that cancellation may not result in any canceled requests if they were non-interruptible.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `message_batch_id: String`

  ID of the Message Batch.

### Returns

- `class MessageBatch`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archived_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancel_initiated_at: Time`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `created_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `ended_at: Time`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expires_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processing_status: :in_progress | :canceling | :ended`

    Processing status of the Message Batch.

    - `:in_progress`

    - `:canceling`

    - `:ended`

  - `request_counts: MessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: Integer`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: Integer`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: Integer`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: Integer`

      Number of requests in the Message Batch that are processing.

    - `succeeded: Integer`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `results_url: String`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: :message_batch`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `:message_batch`

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

message_batch = anthropic.messages.batches.cancel("message_batch_id")

puts(message_batch)
```

## Delete

`messages.batches.delete(message_batch_id) -> DeletedMessageBatch`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `message_batch_id: String`

  ID of the Message Batch.

### Returns

- `class DeletedMessageBatch`

  - `id: String`

    ID of the Message Batch.

  - `type: :message_batch_deleted`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `:message_batch_deleted`

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

deleted_message_batch = anthropic.messages.batches.delete("message_batch_id")

puts(deleted_message_batch)
```

## Results

`messages.batches.results(message_batch_id) -> MessageBatchIndividualResponse`

**get** `/v1/messages/batches/{message_batch_id}/results`

Streams the results of a Message Batch as a `.jsonl` file.

Each line in the file is a JSON object containing the result of a single request in the Message Batch. Results are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `message_batch_id: String`

  ID of the Message Batch.

### Returns

- `class MessageBatchIndividualResponse`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `custom_id: String`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: MessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `class MessageBatchSucceededResult`

      - `message: Message`

        - `id: String`

          Unique object identifier.

          The format and length of IDs may change over time.

        - `content: Array[ContentBlock]`

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

          - `class TextBlock`

            - `citations: Array[TextCitation]`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class CitationCharLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_char_index: Integer`

                - `file_id: String`

                - `start_char_index: Integer`

                - `type: :char_location`

                  - `:char_location`

              - `class CitationPageLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_page_number: Integer`

                - `file_id: String`

                - `start_page_number: Integer`

                - `type: :page_location`

                  - `:page_location`

              - `class CitationContentBlockLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_block_index: Integer`

                - `file_id: String`

                - `start_block_index: Integer`

                - `type: :content_block_location`

                  - `:content_block_location`

              - `class CitationsWebSearchResultLocation`

                - `cited_text: String`

                - `encrypted_index: String`

                - `title: String`

                - `type: :web_search_result_location`

                  - `:web_search_result_location`

                - `url: String`

              - `class CitationsSearchResultLocation`

                - `cited_text: String`

                - `end_block_index: Integer`

                - `search_result_index: Integer`

                - `source: String`

                - `start_block_index: Integer`

                - `title: String`

                - `type: :search_result_location`

                  - `:search_result_location`

            - `text: String`

            - `type: :text`

              - `:text`

          - `class ThinkingBlock`

            - `signature: String`

            - `thinking: String`

            - `type: :thinking`

              - `:thinking`

          - `class RedactedThinkingBlock`

            - `data: String`

            - `type: :redacted_thinking`

              - `:redacted_thinking`

          - `class ToolUseBlock`

            - `id: String`

            - `input: Hash[Symbol, untyped]`

            - `name: String`

            - `type: :tool_use`

              - `:tool_use`

          - `class ServerToolUseBlock`

            - `id: String`

            - `input: Hash[Symbol, untyped]`

            - `name: :web_search`

              - `:web_search`

            - `type: :server_tool_use`

              - `:server_tool_use`

          - `class WebSearchToolResultBlock`

            - `content: WebSearchToolResultBlockContent`

              - `class WebSearchToolResultError`

                - `error_code: :invalid_tool_input | :unavailable | :max_uses_exceeded | 2 more`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:max_uses_exceeded`

                  - `:too_many_requests`

                  - `:query_too_long`

                - `type: :web_search_tool_result_error`

                  - `:web_search_tool_result_error`

              - `Array[WebSearchResultBlock]`

                - `encrypted_content: String`

                - `page_age: String`

                - `title: String`

                - `type: :web_search_result`

                  - `:web_search_result`

                - `url: String`

            - `tool_use_id: String`

            - `type: :web_search_tool_result`

              - `:web_search_tool_result`

        - `model: Model`

          The model that will complete your prompt.

          See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

          - `:"claude-opus-4-5-20251101" | :"claude-opus-4-5" | :"claude-3-7-sonnet-latest" | 17 more`

            The model that will complete your prompt.

            See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

            - `:"claude-opus-4-5-20251101"`

              Premium model combining maximum intelligence with practical performance

            - `:"claude-opus-4-5"`

              Premium model combining maximum intelligence with practical performance

            - `:"claude-3-7-sonnet-latest"`

              High-performance model with early extended thinking

            - `:"claude-3-7-sonnet-20250219"`

              High-performance model with early extended thinking

            - `:"claude-3-5-haiku-latest"`

              Fastest and most compact model for near-instant responsiveness

            - `:"claude-3-5-haiku-20241022"`

              Our fastest model

            - `:"claude-haiku-4-5"`

              Hybrid model, capable of near-instant responses and extended thinking

            - `:"claude-haiku-4-5-20251001"`

              Hybrid model, capable of near-instant responses and extended thinking

            - `:"claude-sonnet-4-20250514"`

              High-performance model with extended thinking

            - `:"claude-sonnet-4-0"`

              High-performance model with extended thinking

            - `:"claude-4-sonnet-20250514"`

              High-performance model with extended thinking

            - `:"claude-sonnet-4-5"`

              Our best model for real-world agents and coding

            - `:"claude-sonnet-4-5-20250929"`

              Our best model for real-world agents and coding

            - `:"claude-opus-4-0"`

              Our most capable model

            - `:"claude-opus-4-20250514"`

              Our most capable model

            - `:"claude-4-opus-20250514"`

              Our most capable model

            - `:"claude-opus-4-1-20250805"`

              Our most capable model

            - `:"claude-3-opus-latest"`

              Excels at writing and complex tasks

            - `:"claude-3-opus-20240229"`

              Excels at writing and complex tasks

            - `:"claude-3-haiku-20240307"`

              Our previous most fast and cost-effective

          - `String`

        - `role: :assistant`

          Conversational role of the generated message.

          This will always be `"assistant"`.

          - `:assistant`

        - `stop_reason: StopReason`

          The reason that we stopped.

          This may be one the following values:

          * `"end_turn"`: the model reached a natural stopping point
          * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
          * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
          * `"tool_use"`: the model invoked one or more tools
          * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
          * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

          In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

          - `:end_turn`

          - `:max_tokens`

          - `:stop_sequence`

          - `:tool_use`

          - `:pause_turn`

          - `:refusal`

        - `stop_sequence: String`

          Which custom stop sequence was generated, if any.

          This value will be a non-null string if one of your custom stop sequences was generated.

        - `type: :message`

          Object type.

          For Messages, this is always `"message"`.

          - `:message`

        - `usage: Usage`

          Billing and rate-limit usage.

          Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

          Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

          For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

          Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

          - `cache_creation: CacheCreation`

            Breakdown of cached tokens by TTL

            - `ephemeral_1h_input_tokens: Integer`

              The number of input tokens used to create the 1 hour cache entry.

            - `ephemeral_5m_input_tokens: Integer`

              The number of input tokens used to create the 5 minute cache entry.

          - `cache_creation_input_tokens: Integer`

            The number of input tokens used to create the cache entry.

          - `cache_read_input_tokens: Integer`

            The number of input tokens read from the cache.

          - `input_tokens: Integer`

            The number of input tokens which were used.

          - `output_tokens: Integer`

            The number of output tokens which were used.

          - `server_tool_use: ServerToolUsage`

            The number of server tool requests.

            - `web_search_requests: Integer`

              The number of web search tool requests.

          - `service_tier: :standard | :priority | :batch`

            If the request used the priority, standard, or batch tier.

            - `:standard`

            - `:priority`

            - `:batch`

      - `type: :succeeded`

        - `:succeeded`

    - `class MessageBatchErroredResult`

      - `error: ErrorResponse`

        - `error: ErrorObject`

          - `class InvalidRequestError`

            - `message: String`

            - `type: :invalid_request_error`

              - `:invalid_request_error`

          - `class AuthenticationError`

            - `message: String`

            - `type: :authentication_error`

              - `:authentication_error`

          - `class BillingError`

            - `message: String`

            - `type: :billing_error`

              - `:billing_error`

          - `class PermissionError`

            - `message: String`

            - `type: :permission_error`

              - `:permission_error`

          - `class NotFoundError`

            - `message: String`

            - `type: :not_found_error`

              - `:not_found_error`

          - `class RateLimitError`

            - `message: String`

            - `type: :rate_limit_error`

              - `:rate_limit_error`

          - `class GatewayTimeoutError`

            - `message: String`

            - `type: :timeout_error`

              - `:timeout_error`

          - `class APIErrorObject`

            - `message: String`

            - `type: :api_error`

              - `:api_error`

          - `class OverloadedError`

            - `message: String`

            - `type: :overloaded_error`

              - `:overloaded_error`

        - `request_id: String`

        - `type: :error`

          - `:error`

      - `type: :errored`

        - `:errored`

    - `class MessageBatchCanceledResult`

      - `type: :canceled`

        - `:canceled`

    - `class MessageBatchExpiredResult`

      - `type: :expired`

        - `:expired`

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

message_batch_individual_response = anthropic.messages.batches.results("message_batch_id")

puts(message_batch_individual_response)
```

## Domain Types

### Deleted Message Batch

- `class DeletedMessageBatch`

  - `id: String`

    ID of the Message Batch.

  - `type: :message_batch_deleted`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `:message_batch_deleted`

### Message Batch

- `class MessageBatch`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archived_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancel_initiated_at: Time`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `created_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `ended_at: Time`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expires_at: Time`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processing_status: :in_progress | :canceling | :ended`

    Processing status of the Message Batch.

    - `:in_progress`

    - `:canceling`

    - `:ended`

  - `request_counts: MessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: Integer`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: Integer`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: Integer`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: Integer`

      Number of requests in the Message Batch that are processing.

    - `succeeded: Integer`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `results_url: String`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: :message_batch`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `:message_batch`

### Message Batch Canceled Result

- `class MessageBatchCanceledResult`

  - `type: :canceled`

    - `:canceled`

### Message Batch Errored Result

- `class MessageBatchErroredResult`

  - `error: ErrorResponse`

    - `error: ErrorObject`

      - `class InvalidRequestError`

        - `message: String`

        - `type: :invalid_request_error`

          - `:invalid_request_error`

      - `class AuthenticationError`

        - `message: String`

        - `type: :authentication_error`

          - `:authentication_error`

      - `class BillingError`

        - `message: String`

        - `type: :billing_error`

          - `:billing_error`

      - `class PermissionError`

        - `message: String`

        - `type: :permission_error`

          - `:permission_error`

      - `class NotFoundError`

        - `message: String`

        - `type: :not_found_error`

          - `:not_found_error`

      - `class RateLimitError`

        - `message: String`

        - `type: :rate_limit_error`

          - `:rate_limit_error`

      - `class GatewayTimeoutError`

        - `message: String`

        - `type: :timeout_error`

          - `:timeout_error`

      - `class APIErrorObject`

        - `message: String`

        - `type: :api_error`

          - `:api_error`

      - `class OverloadedError`

        - `message: String`

        - `type: :overloaded_error`

          - `:overloaded_error`

    - `request_id: String`

    - `type: :error`

      - `:error`

  - `type: :errored`

    - `:errored`

### Message Batch Expired Result

- `class MessageBatchExpiredResult`

  - `type: :expired`

    - `:expired`

### Message Batch Individual Response

- `class MessageBatchIndividualResponse`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `custom_id: String`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: MessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `class MessageBatchSucceededResult`

      - `message: Message`

        - `id: String`

          Unique object identifier.

          The format and length of IDs may change over time.

        - `content: Array[ContentBlock]`

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

          - `class TextBlock`

            - `citations: Array[TextCitation]`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class CitationCharLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_char_index: Integer`

                - `file_id: String`

                - `start_char_index: Integer`

                - `type: :char_location`

                  - `:char_location`

              - `class CitationPageLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_page_number: Integer`

                - `file_id: String`

                - `start_page_number: Integer`

                - `type: :page_location`

                  - `:page_location`

              - `class CitationContentBlockLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_block_index: Integer`

                - `file_id: String`

                - `start_block_index: Integer`

                - `type: :content_block_location`

                  - `:content_block_location`

              - `class CitationsWebSearchResultLocation`

                - `cited_text: String`

                - `encrypted_index: String`

                - `title: String`

                - `type: :web_search_result_location`

                  - `:web_search_result_location`

                - `url: String`

              - `class CitationsSearchResultLocation`

                - `cited_text: String`

                - `end_block_index: Integer`

                - `search_result_index: Integer`

                - `source: String`

                - `start_block_index: Integer`

                - `title: String`

                - `type: :search_result_location`

                  - `:search_result_location`

            - `text: String`

            - `type: :text`

              - `:text`

          - `class ThinkingBlock`

            - `signature: String`

            - `thinking: String`

            - `type: :thinking`

              - `:thinking`

          - `class RedactedThinkingBlock`

            - `data: String`

            - `type: :redacted_thinking`

              - `:redacted_thinking`

          - `class ToolUseBlock`

            - `id: String`

            - `input: Hash[Symbol, untyped]`

            - `name: String`

            - `type: :tool_use`

              - `:tool_use`

          - `class ServerToolUseBlock`

            - `id: String`

            - `input: Hash[Symbol, untyped]`

            - `name: :web_search`

              - `:web_search`

            - `type: :server_tool_use`

              - `:server_tool_use`

          - `class WebSearchToolResultBlock`

            - `content: WebSearchToolResultBlockContent`

              - `class WebSearchToolResultError`

                - `error_code: :invalid_tool_input | :unavailable | :max_uses_exceeded | 2 more`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:max_uses_exceeded`

                  - `:too_many_requests`

                  - `:query_too_long`

                - `type: :web_search_tool_result_error`

                  - `:web_search_tool_result_error`

              - `Array[WebSearchResultBlock]`

                - `encrypted_content: String`

                - `page_age: String`

                - `title: String`

                - `type: :web_search_result`

                  - `:web_search_result`

                - `url: String`

            - `tool_use_id: String`

            - `type: :web_search_tool_result`

              - `:web_search_tool_result`

        - `model: Model`

          The model that will complete your prompt.

          See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

          - `:"claude-opus-4-5-20251101" | :"claude-opus-4-5" | :"claude-3-7-sonnet-latest" | 17 more`

            The model that will complete your prompt.

            See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

            - `:"claude-opus-4-5-20251101"`

              Premium model combining maximum intelligence with practical performance

            - `:"claude-opus-4-5"`

              Premium model combining maximum intelligence with practical performance

            - `:"claude-3-7-sonnet-latest"`

              High-performance model with early extended thinking

            - `:"claude-3-7-sonnet-20250219"`

              High-performance model with early extended thinking

            - `:"claude-3-5-haiku-latest"`

              Fastest and most compact model for near-instant responsiveness

            - `:"claude-3-5-haiku-20241022"`

              Our fastest model

            - `:"claude-haiku-4-5"`

              Hybrid model, capable of near-instant responses and extended thinking

            - `:"claude-haiku-4-5-20251001"`

              Hybrid model, capable of near-instant responses and extended thinking

            - `:"claude-sonnet-4-20250514"`

              High-performance model with extended thinking

            - `:"claude-sonnet-4-0"`

              High-performance model with extended thinking

            - `:"claude-4-sonnet-20250514"`

              High-performance model with extended thinking

            - `:"claude-sonnet-4-5"`

              Our best model for real-world agents and coding

            - `:"claude-sonnet-4-5-20250929"`

              Our best model for real-world agents and coding

            - `:"claude-opus-4-0"`

              Our most capable model

            - `:"claude-opus-4-20250514"`

              Our most capable model

            - `:"claude-4-opus-20250514"`

              Our most capable model

            - `:"claude-opus-4-1-20250805"`

              Our most capable model

            - `:"claude-3-opus-latest"`

              Excels at writing and complex tasks

            - `:"claude-3-opus-20240229"`

              Excels at writing and complex tasks

            - `:"claude-3-haiku-20240307"`

              Our previous most fast and cost-effective

          - `String`

        - `role: :assistant`

          Conversational role of the generated message.

          This will always be `"assistant"`.

          - `:assistant`

        - `stop_reason: StopReason`

          The reason that we stopped.

          This may be one the following values:

          * `"end_turn"`: the model reached a natural stopping point
          * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
          * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
          * `"tool_use"`: the model invoked one or more tools
          * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
          * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

          In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

          - `:end_turn`

          - `:max_tokens`

          - `:stop_sequence`

          - `:tool_use`

          - `:pause_turn`

          - `:refusal`

        - `stop_sequence: String`

          Which custom stop sequence was generated, if any.

          This value will be a non-null string if one of your custom stop sequences was generated.

        - `type: :message`

          Object type.

          For Messages, this is always `"message"`.

          - `:message`

        - `usage: Usage`

          Billing and rate-limit usage.

          Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

          Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

          For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

          Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

          - `cache_creation: CacheCreation`

            Breakdown of cached tokens by TTL

            - `ephemeral_1h_input_tokens: Integer`

              The number of input tokens used to create the 1 hour cache entry.

            - `ephemeral_5m_input_tokens: Integer`

              The number of input tokens used to create the 5 minute cache entry.

          - `cache_creation_input_tokens: Integer`

            The number of input tokens used to create the cache entry.

          - `cache_read_input_tokens: Integer`

            The number of input tokens read from the cache.

          - `input_tokens: Integer`

            The number of input tokens which were used.

          - `output_tokens: Integer`

            The number of output tokens which were used.

          - `server_tool_use: ServerToolUsage`

            The number of server tool requests.

            - `web_search_requests: Integer`

              The number of web search tool requests.

          - `service_tier: :standard | :priority | :batch`

            If the request used the priority, standard, or batch tier.

            - `:standard`

            - `:priority`

            - `:batch`

      - `type: :succeeded`

        - `:succeeded`

    - `class MessageBatchErroredResult`

      - `error: ErrorResponse`

        - `error: ErrorObject`

          - `class InvalidRequestError`

            - `message: String`

            - `type: :invalid_request_error`

              - `:invalid_request_error`

          - `class AuthenticationError`

            - `message: String`

            - `type: :authentication_error`

              - `:authentication_error`

          - `class BillingError`

            - `message: String`

            - `type: :billing_error`

              - `:billing_error`

          - `class PermissionError`

            - `message: String`

            - `type: :permission_error`

              - `:permission_error`

          - `class NotFoundError`

            - `message: String`

            - `type: :not_found_error`

              - `:not_found_error`

          - `class RateLimitError`

            - `message: String`

            - `type: :rate_limit_error`

              - `:rate_limit_error`

          - `class GatewayTimeoutError`

            - `message: String`

            - `type: :timeout_error`

              - `:timeout_error`

          - `class APIErrorObject`

            - `message: String`

            - `type: :api_error`

              - `:api_error`

          - `class OverloadedError`

            - `message: String`

            - `type: :overloaded_error`

              - `:overloaded_error`

        - `request_id: String`

        - `type: :error`

          - `:error`

      - `type: :errored`

        - `:errored`

    - `class MessageBatchCanceledResult`

      - `type: :canceled`

        - `:canceled`

    - `class MessageBatchExpiredResult`

      - `type: :expired`

        - `:expired`

### Message Batch Request Counts

- `class MessageBatchRequestCounts`

  - `canceled: Integer`

    Number of requests in the Message Batch that have been canceled.

    This is zero until processing of the entire Message Batch has ended.

  - `errored: Integer`

    Number of requests in the Message Batch that encountered an error.

    This is zero until processing of the entire Message Batch has ended.

  - `expired: Integer`

    Number of requests in the Message Batch that have expired.

    This is zero until processing of the entire Message Batch has ended.

  - `processing: Integer`

    Number of requests in the Message Batch that are processing.

  - `succeeded: Integer`

    Number of requests in the Message Batch that have completed successfully.

    This is zero until processing of the entire Message Batch has ended.

### Message Batch Result

- `MessageBatchResult = MessageBatchSucceededResult | MessageBatchErroredResult | MessageBatchCanceledResult | MessageBatchExpiredResult`

  Processing result for this request.

  Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

  - `class MessageBatchSucceededResult`

    - `message: Message`

      - `id: String`

        Unique object identifier.

        The format and length of IDs may change over time.

      - `content: Array[ContentBlock]`

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

        - `class TextBlock`

          - `citations: Array[TextCitation]`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `class CitationCharLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_char_index: Integer`

              - `file_id: String`

              - `start_char_index: Integer`

              - `type: :char_location`

                - `:char_location`

            - `class CitationPageLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_page_number: Integer`

              - `file_id: String`

              - `start_page_number: Integer`

              - `type: :page_location`

                - `:page_location`

            - `class CitationContentBlockLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_block_index: Integer`

              - `file_id: String`

              - `start_block_index: Integer`

              - `type: :content_block_location`

                - `:content_block_location`

            - `class CitationsWebSearchResultLocation`

              - `cited_text: String`

              - `encrypted_index: String`

              - `title: String`

              - `type: :web_search_result_location`

                - `:web_search_result_location`

              - `url: String`

            - `class CitationsSearchResultLocation`

              - `cited_text: String`

              - `end_block_index: Integer`

              - `search_result_index: Integer`

              - `source: String`

              - `start_block_index: Integer`

              - `title: String`

              - `type: :search_result_location`

                - `:search_result_location`

          - `text: String`

          - `type: :text`

            - `:text`

        - `class ThinkingBlock`

          - `signature: String`

          - `thinking: String`

          - `type: :thinking`

            - `:thinking`

        - `class RedactedThinkingBlock`

          - `data: String`

          - `type: :redacted_thinking`

            - `:redacted_thinking`

        - `class ToolUseBlock`

          - `id: String`

          - `input: Hash[Symbol, untyped]`

          - `name: String`

          - `type: :tool_use`

            - `:tool_use`

        - `class ServerToolUseBlock`

          - `id: String`

          - `input: Hash[Symbol, untyped]`

          - `name: :web_search`

            - `:web_search`

          - `type: :server_tool_use`

            - `:server_tool_use`

        - `class WebSearchToolResultBlock`

          - `content: WebSearchToolResultBlockContent`

            - `class WebSearchToolResultError`

              - `error_code: :invalid_tool_input | :unavailable | :max_uses_exceeded | 2 more`

                - `:invalid_tool_input`

                - `:unavailable`

                - `:max_uses_exceeded`

                - `:too_many_requests`

                - `:query_too_long`

              - `type: :web_search_tool_result_error`

                - `:web_search_tool_result_error`

            - `Array[WebSearchResultBlock]`

              - `encrypted_content: String`

              - `page_age: String`

              - `title: String`

              - `type: :web_search_result`

                - `:web_search_result`

              - `url: String`

          - `tool_use_id: String`

          - `type: :web_search_tool_result`

            - `:web_search_tool_result`

      - `model: Model`

        The model that will complete your prompt.

        See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

        - `:"claude-opus-4-5-20251101" | :"claude-opus-4-5" | :"claude-3-7-sonnet-latest" | 17 more`

          The model that will complete your prompt.

          See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

          - `:"claude-opus-4-5-20251101"`

            Premium model combining maximum intelligence with practical performance

          - `:"claude-opus-4-5"`

            Premium model combining maximum intelligence with practical performance

          - `:"claude-3-7-sonnet-latest"`

            High-performance model with early extended thinking

          - `:"claude-3-7-sonnet-20250219"`

            High-performance model with early extended thinking

          - `:"claude-3-5-haiku-latest"`

            Fastest and most compact model for near-instant responsiveness

          - `:"claude-3-5-haiku-20241022"`

            Our fastest model

          - `:"claude-haiku-4-5"`

            Hybrid model, capable of near-instant responses and extended thinking

          - `:"claude-haiku-4-5-20251001"`

            Hybrid model, capable of near-instant responses and extended thinking

          - `:"claude-sonnet-4-20250514"`

            High-performance model with extended thinking

          - `:"claude-sonnet-4-0"`

            High-performance model with extended thinking

          - `:"claude-4-sonnet-20250514"`

            High-performance model with extended thinking

          - `:"claude-sonnet-4-5"`

            Our best model for real-world agents and coding

          - `:"claude-sonnet-4-5-20250929"`

            Our best model for real-world agents and coding

          - `:"claude-opus-4-0"`

            Our most capable model

          - `:"claude-opus-4-20250514"`

            Our most capable model

          - `:"claude-4-opus-20250514"`

            Our most capable model

          - `:"claude-opus-4-1-20250805"`

            Our most capable model

          - `:"claude-3-opus-latest"`

            Excels at writing and complex tasks

          - `:"claude-3-opus-20240229"`

            Excels at writing and complex tasks

          - `:"claude-3-haiku-20240307"`

            Our previous most fast and cost-effective

        - `String`

      - `role: :assistant`

        Conversational role of the generated message.

        This will always be `"assistant"`.

        - `:assistant`

      - `stop_reason: StopReason`

        The reason that we stopped.

        This may be one the following values:

        * `"end_turn"`: the model reached a natural stopping point
        * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
        * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
        * `"tool_use"`: the model invoked one or more tools
        * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
        * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

        In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

        - `:end_turn`

        - `:max_tokens`

        - `:stop_sequence`

        - `:tool_use`

        - `:pause_turn`

        - `:refusal`

      - `stop_sequence: String`

        Which custom stop sequence was generated, if any.

        This value will be a non-null string if one of your custom stop sequences was generated.

      - `type: :message`

        Object type.

        For Messages, this is always `"message"`.

        - `:message`

      - `usage: Usage`

        Billing and rate-limit usage.

        Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

        Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

        For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

        Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

        - `cache_creation: CacheCreation`

          Breakdown of cached tokens by TTL

          - `ephemeral_1h_input_tokens: Integer`

            The number of input tokens used to create the 1 hour cache entry.

          - `ephemeral_5m_input_tokens: Integer`

            The number of input tokens used to create the 5 minute cache entry.

        - `cache_creation_input_tokens: Integer`

          The number of input tokens used to create the cache entry.

        - `cache_read_input_tokens: Integer`

          The number of input tokens read from the cache.

        - `input_tokens: Integer`

          The number of input tokens which were used.

        - `output_tokens: Integer`

          The number of output tokens which were used.

        - `server_tool_use: ServerToolUsage`

          The number of server tool requests.

          - `web_search_requests: Integer`

            The number of web search tool requests.

        - `service_tier: :standard | :priority | :batch`

          If the request used the priority, standard, or batch tier.

          - `:standard`

          - `:priority`

          - `:batch`

    - `type: :succeeded`

      - `:succeeded`

  - `class MessageBatchErroredResult`

    - `error: ErrorResponse`

      - `error: ErrorObject`

        - `class InvalidRequestError`

          - `message: String`

          - `type: :invalid_request_error`

            - `:invalid_request_error`

        - `class AuthenticationError`

          - `message: String`

          - `type: :authentication_error`

            - `:authentication_error`

        - `class BillingError`

          - `message: String`

          - `type: :billing_error`

            - `:billing_error`

        - `class PermissionError`

          - `message: String`

          - `type: :permission_error`

            - `:permission_error`

        - `class NotFoundError`

          - `message: String`

          - `type: :not_found_error`

            - `:not_found_error`

        - `class RateLimitError`

          - `message: String`

          - `type: :rate_limit_error`

            - `:rate_limit_error`

        - `class GatewayTimeoutError`

          - `message: String`

          - `type: :timeout_error`

            - `:timeout_error`

        - `class APIErrorObject`

          - `message: String`

          - `type: :api_error`

            - `:api_error`

        - `class OverloadedError`

          - `message: String`

          - `type: :overloaded_error`

            - `:overloaded_error`

      - `request_id: String`

      - `type: :error`

        - `:error`

    - `type: :errored`

      - `:errored`

  - `class MessageBatchCanceledResult`

    - `type: :canceled`

      - `:canceled`

  - `class MessageBatchExpiredResult`

    - `type: :expired`

      - `:expired`

### Message Batch Succeeded Result

- `class MessageBatchSucceededResult`

  - `message: Message`

    - `id: String`

      Unique object identifier.

      The format and length of IDs may change over time.

    - `content: Array[ContentBlock]`

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

      - `class TextBlock`

        - `citations: Array[TextCitation]`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `class CitationCharLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_char_index: Integer`

            - `file_id: String`

            - `start_char_index: Integer`

            - `type: :char_location`

              - `:char_location`

          - `class CitationPageLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_page_number: Integer`

            - `file_id: String`

            - `start_page_number: Integer`

            - `type: :page_location`

              - `:page_location`

          - `class CitationContentBlockLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_block_index: Integer`

            - `file_id: String`

            - `start_block_index: Integer`

            - `type: :content_block_location`

              - `:content_block_location`

          - `class CitationsWebSearchResultLocation`

            - `cited_text: String`

            - `encrypted_index: String`

            - `title: String`

            - `type: :web_search_result_location`

              - `:web_search_result_location`

            - `url: String`

          - `class CitationsSearchResultLocation`

            - `cited_text: String`

            - `end_block_index: Integer`

            - `search_result_index: Integer`

            - `source: String`

            - `start_block_index: Integer`

            - `title: String`

            - `type: :search_result_location`

              - `:search_result_location`

        - `text: String`

        - `type: :text`

          - `:text`

      - `class ThinkingBlock`

        - `signature: String`

        - `thinking: String`

        - `type: :thinking`

          - `:thinking`

      - `class RedactedThinkingBlock`

        - `data: String`

        - `type: :redacted_thinking`

          - `:redacted_thinking`

      - `class ToolUseBlock`

        - `id: String`

        - `input: Hash[Symbol, untyped]`

        - `name: String`

        - `type: :tool_use`

          - `:tool_use`

      - `class ServerToolUseBlock`

        - `id: String`

        - `input: Hash[Symbol, untyped]`

        - `name: :web_search`

          - `:web_search`

        - `type: :server_tool_use`

          - `:server_tool_use`

      - `class WebSearchToolResultBlock`

        - `content: WebSearchToolResultBlockContent`

          - `class WebSearchToolResultError`

            - `error_code: :invalid_tool_input | :unavailable | :max_uses_exceeded | 2 more`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:max_uses_exceeded`

              - `:too_many_requests`

              - `:query_too_long`

            - `type: :web_search_tool_result_error`

              - `:web_search_tool_result_error`

          - `Array[WebSearchResultBlock]`

            - `encrypted_content: String`

            - `page_age: String`

            - `title: String`

            - `type: :web_search_result`

              - `:web_search_result`

            - `url: String`

        - `tool_use_id: String`

        - `type: :web_search_tool_result`

          - `:web_search_tool_result`

    - `model: Model`

      The model that will complete your prompt.

      See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

      - `:"claude-opus-4-5-20251101" | :"claude-opus-4-5" | :"claude-3-7-sonnet-latest" | 17 more`

        The model that will complete your prompt.

        See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

        - `:"claude-opus-4-5-20251101"`

          Premium model combining maximum intelligence with practical performance

        - `:"claude-opus-4-5"`

          Premium model combining maximum intelligence with practical performance

        - `:"claude-3-7-sonnet-latest"`

          High-performance model with early extended thinking

        - `:"claude-3-7-sonnet-20250219"`

          High-performance model with early extended thinking

        - `:"claude-3-5-haiku-latest"`

          Fastest and most compact model for near-instant responsiveness

        - `:"claude-3-5-haiku-20241022"`

          Our fastest model

        - `:"claude-haiku-4-5"`

          Hybrid model, capable of near-instant responses and extended thinking

        - `:"claude-haiku-4-5-20251001"`

          Hybrid model, capable of near-instant responses and extended thinking

        - `:"claude-sonnet-4-20250514"`

          High-performance model with extended thinking

        - `:"claude-sonnet-4-0"`

          High-performance model with extended thinking

        - `:"claude-4-sonnet-20250514"`

          High-performance model with extended thinking

        - `:"claude-sonnet-4-5"`

          Our best model for real-world agents and coding

        - `:"claude-sonnet-4-5-20250929"`

          Our best model for real-world agents and coding

        - `:"claude-opus-4-0"`

          Our most capable model

        - `:"claude-opus-4-20250514"`

          Our most capable model

        - `:"claude-4-opus-20250514"`

          Our most capable model

        - `:"claude-opus-4-1-20250805"`

          Our most capable model

        - `:"claude-3-opus-latest"`

          Excels at writing and complex tasks

        - `:"claude-3-opus-20240229"`

          Excels at writing and complex tasks

        - `:"claude-3-haiku-20240307"`

          Our previous most fast and cost-effective

      - `String`

    - `role: :assistant`

      Conversational role of the generated message.

      This will always be `"assistant"`.

      - `:assistant`

    - `stop_reason: StopReason`

      The reason that we stopped.

      This may be one the following values:

      * `"end_turn"`: the model reached a natural stopping point
      * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
      * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
      * `"tool_use"`: the model invoked one or more tools
      * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
      * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

      In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

      - `:end_turn`

      - `:max_tokens`

      - `:stop_sequence`

      - `:tool_use`

      - `:pause_turn`

      - `:refusal`

    - `stop_sequence: String`

      Which custom stop sequence was generated, if any.

      This value will be a non-null string if one of your custom stop sequences was generated.

    - `type: :message`

      Object type.

      For Messages, this is always `"message"`.

      - `:message`

    - `usage: Usage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cache_creation: CacheCreation`

        Breakdown of cached tokens by TTL

        - `ephemeral_1h_input_tokens: Integer`

          The number of input tokens used to create the 1 hour cache entry.

        - `ephemeral_5m_input_tokens: Integer`

          The number of input tokens used to create the 5 minute cache entry.

      - `cache_creation_input_tokens: Integer`

        The number of input tokens used to create the cache entry.

      - `cache_read_input_tokens: Integer`

        The number of input tokens read from the cache.

      - `input_tokens: Integer`

        The number of input tokens which were used.

      - `output_tokens: Integer`

        The number of output tokens which were used.

      - `server_tool_use: ServerToolUsage`

        The number of server tool requests.

        - `web_search_requests: Integer`

          The number of web search tool requests.

      - `service_tier: :standard | :priority | :batch`

        If the request used the priority, standard, or batch tier.

        - `:standard`

        - `:priority`

        - `:batch`

  - `type: :succeeded`

    - `:succeeded`
