## Create

`client.messages.batches.create(BatchCreateParamsbody, RequestOptionsoptions?): MessageBatch`

**post** `/v1/messages/batches`

Send a batch of Message creation requests.

The Message Batches API can be used to process multiple Messages API requests at once. Once a Message Batch is created, it begins processing immediately. Batches can take up to 24 hours to complete.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `body: BatchCreateParams`

  - `requests: Array<Request>`

    List of requests for prompt completion. Each is an individual request to create a Message.

    - `custom_id: string`

      Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

      Must be unique for each request within the Message Batch.

    - `params: Params`

      Messages API creation parameters for the individual request.

      See the [Messages API reference](https://docs.claude.com/en/api/messages) for full documentation on available parameters.

      - `max_tokens: number`

        The maximum number of tokens to generate before stopping.

        Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

        Different models have different maximum values for this parameter.  See [models](https://docs.claude.com/en/docs/models-overview) for details.

      - `messages: Array<MessageParam>`

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

        - `content: string | Array<ContentBlockParam>`

          - `string`

          - `Array<ContentBlockParam>`

            - `TextBlockParam`

              - `text: string`

              - `type: "text"`

                - `"text"`

              - `cache_control?: CacheControlEphemeral | null`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl?: "5m" | "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations?: Array<TextCitationParam> | null`

                - `CitationCharLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_char_index: number`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `CitationPageLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_page_number: number`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `CitationContentBlockLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_block_index: number`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `CitationWebSearchResultLocationParam`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string | null`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `CitationSearchResultLocationParam`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string | null`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

            - `ImageBlockParam`

              - `source: Base64ImageSource | URLImageSource`

                - `Base64ImageSource`

                  - `data: string`

                  - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                    - `"image/jpeg"`

                    - `"image/png"`

                    - `"image/gif"`

                    - `"image/webp"`

                  - `type: "base64"`

                    - `"base64"`

                - `URLImageSource`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

              - `type: "image"`

                - `"image"`

              - `cache_control?: CacheControlEphemeral | null`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl?: "5m" | "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

            - `DocumentBlockParam`

              - `source: Base64PDFSource | PlainTextSource | ContentBlockSource | URLPDFSource`

                - `Base64PDFSource`

                  - `data: string`

                  - `media_type: "application/pdf"`

                    - `"application/pdf"`

                  - `type: "base64"`

                    - `"base64"`

                - `PlainTextSource`

                  - `data: string`

                  - `media_type: "text/plain"`

                    - `"text/plain"`

                  - `type: "text"`

                    - `"text"`

                - `ContentBlockSource`

                  - `content: string | Array<ContentBlockSourceContent>`

                    - `string`

                    - `Array<ContentBlockSourceContent>`

                      - `TextBlockParam`

                        - `text: string`

                        - `type: "text"`

                          - `"text"`

                        - `cache_control?: CacheControlEphemeral | null`

                          Create a cache control breakpoint at this content block.

                          - `type: "ephemeral"`

                            - `"ephemeral"`

                          - `ttl?: "5m" | "1h"`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `"5m"`

                            - `"1h"`

                        - `citations?: Array<TextCitationParam> | null`

                          - `CitationCharLocationParam`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string | null`

                            - `end_char_index: number`

                            - `start_char_index: number`

                            - `type: "char_location"`

                              - `"char_location"`

                          - `CitationPageLocationParam`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string | null`

                            - `end_page_number: number`

                            - `start_page_number: number`

                            - `type: "page_location"`

                              - `"page_location"`

                          - `CitationContentBlockLocationParam`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string | null`

                            - `end_block_index: number`

                            - `start_block_index: number`

                            - `type: "content_block_location"`

                              - `"content_block_location"`

                          - `CitationWebSearchResultLocationParam`

                            - `cited_text: string`

                            - `encrypted_index: string`

                            - `title: string | null`

                            - `type: "web_search_result_location"`

                              - `"web_search_result_location"`

                            - `url: string`

                          - `CitationSearchResultLocationParam`

                            - `cited_text: string`

                            - `end_block_index: number`

                            - `search_result_index: number`

                            - `source: string`

                            - `start_block_index: number`

                            - `title: string | null`

                            - `type: "search_result_location"`

                              - `"search_result_location"`

                      - `ImageBlockParam`

                        - `source: Base64ImageSource | URLImageSource`

                          - `Base64ImageSource`

                            - `data: string`

                            - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                              - `"image/jpeg"`

                              - `"image/png"`

                              - `"image/gif"`

                              - `"image/webp"`

                            - `type: "base64"`

                              - `"base64"`

                          - `URLImageSource`

                            - `type: "url"`

                              - `"url"`

                            - `url: string`

                        - `type: "image"`

                          - `"image"`

                        - `cache_control?: CacheControlEphemeral | null`

                          Create a cache control breakpoint at this content block.

                          - `type: "ephemeral"`

                            - `"ephemeral"`

                          - `ttl?: "5m" | "1h"`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `"5m"`

                            - `"1h"`

                  - `type: "content"`

                    - `"content"`

                - `URLPDFSource`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

              - `type: "document"`

                - `"document"`

              - `cache_control?: CacheControlEphemeral | null`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl?: "5m" | "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations?: CitationsConfigParam | null`

                - `enabled?: boolean`

              - `context?: string | null`

              - `title?: string | null`

            - `SearchResultBlockParam`

              - `content: Array<TextBlockParam>`

                - `text: string`

                - `type: "text"`

                  - `"text"`

                - `cache_control?: CacheControlEphemeral | null`

                  Create a cache control breakpoint at this content block.

                  - `type: "ephemeral"`

                    - `"ephemeral"`

                  - `ttl?: "5m" | "1h"`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `"5m"`

                    - `"1h"`

                - `citations?: Array<TextCitationParam> | null`

                  - `CitationCharLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_char_index: number`

                    - `start_char_index: number`

                    - `type: "char_location"`

                      - `"char_location"`

                  - `CitationPageLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_page_number: number`

                    - `start_page_number: number`

                    - `type: "page_location"`

                      - `"page_location"`

                  - `CitationContentBlockLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_block_index: number`

                    - `start_block_index: number`

                    - `type: "content_block_location"`

                      - `"content_block_location"`

                  - `CitationWebSearchResultLocationParam`

                    - `cited_text: string`

                    - `encrypted_index: string`

                    - `title: string | null`

                    - `type: "web_search_result_location"`

                      - `"web_search_result_location"`

                    - `url: string`

                  - `CitationSearchResultLocationParam`

                    - `cited_text: string`

                    - `end_block_index: number`

                    - `search_result_index: number`

                    - `source: string`

                    - `start_block_index: number`

                    - `title: string | null`

                    - `type: "search_result_location"`

                      - `"search_result_location"`

              - `source: string`

              - `title: string`

              - `type: "search_result"`

                - `"search_result"`

              - `cache_control?: CacheControlEphemeral | null`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl?: "5m" | "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations?: CitationsConfigParam`

                - `enabled?: boolean`

            - `ThinkingBlockParam`

              - `signature: string`

              - `thinking: string`

              - `type: "thinking"`

                - `"thinking"`

            - `RedactedThinkingBlockParam`

              - `data: string`

              - `type: "redacted_thinking"`

                - `"redacted_thinking"`

            - `ToolUseBlockParam`

              - `id: string`

              - `input: Record<string, unknown>`

              - `name: string`

              - `type: "tool_use"`

                - `"tool_use"`

              - `cache_control?: CacheControlEphemeral | null`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl?: "5m" | "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

            - `ToolResultBlockParam`

              - `tool_use_id: string`

              - `type: "tool_result"`

                - `"tool_result"`

              - `cache_control?: CacheControlEphemeral | null`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl?: "5m" | "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `content?: string | Array<TextBlockParam | ImageBlockParam | SearchResultBlockParam | DocumentBlockParam>`

                - `string`

                - `Array<TextBlockParam | ImageBlockParam | SearchResultBlockParam | DocumentBlockParam>`

                  - `TextBlockParam`

                    - `text: string`

                    - `type: "text"`

                      - `"text"`

                    - `cache_control?: CacheControlEphemeral | null`

                      Create a cache control breakpoint at this content block.

                      - `type: "ephemeral"`

                        - `"ephemeral"`

                      - `ttl?: "5m" | "1h"`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `"5m"`

                        - `"1h"`

                    - `citations?: Array<TextCitationParam> | null`

                      - `CitationCharLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_char_index: number`

                        - `start_char_index: number`

                        - `type: "char_location"`

                          - `"char_location"`

                      - `CitationPageLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_page_number: number`

                        - `start_page_number: number`

                        - `type: "page_location"`

                          - `"page_location"`

                      - `CitationContentBlockLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_block_index: number`

                        - `start_block_index: number`

                        - `type: "content_block_location"`

                          - `"content_block_location"`

                      - `CitationWebSearchResultLocationParam`

                        - `cited_text: string`

                        - `encrypted_index: string`

                        - `title: string | null`

                        - `type: "web_search_result_location"`

                          - `"web_search_result_location"`

                        - `url: string`

                      - `CitationSearchResultLocationParam`

                        - `cited_text: string`

                        - `end_block_index: number`

                        - `search_result_index: number`

                        - `source: string`

                        - `start_block_index: number`

                        - `title: string | null`

                        - `type: "search_result_location"`

                          - `"search_result_location"`

                  - `ImageBlockParam`

                    - `source: Base64ImageSource | URLImageSource`

                      - `Base64ImageSource`

                        - `data: string`

                        - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                          - `"image/jpeg"`

                          - `"image/png"`

                          - `"image/gif"`

                          - `"image/webp"`

                        - `type: "base64"`

                          - `"base64"`

                      - `URLImageSource`

                        - `type: "url"`

                          - `"url"`

                        - `url: string`

                    - `type: "image"`

                      - `"image"`

                    - `cache_control?: CacheControlEphemeral | null`

                      Create a cache control breakpoint at this content block.

                      - `type: "ephemeral"`

                        - `"ephemeral"`

                      - `ttl?: "5m" | "1h"`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `"5m"`

                        - `"1h"`

                  - `SearchResultBlockParam`

                    - `content: Array<TextBlockParam>`

                      - `text: string`

                      - `type: "text"`

                        - `"text"`

                      - `cache_control?: CacheControlEphemeral | null`

                        Create a cache control breakpoint at this content block.

                        - `type: "ephemeral"`

                          - `"ephemeral"`

                        - `ttl?: "5m" | "1h"`

                          The time-to-live for the cache control breakpoint.

                          This may be one the following values:

                          - `5m`: 5 minutes
                          - `1h`: 1 hour

                          Defaults to `5m`.

                          - `"5m"`

                          - `"1h"`

                      - `citations?: Array<TextCitationParam> | null`

                        - `CitationCharLocationParam`

                          - `cited_text: string`

                          - `document_index: number`

                          - `document_title: string | null`

                          - `end_char_index: number`

                          - `start_char_index: number`

                          - `type: "char_location"`

                            - `"char_location"`

                        - `CitationPageLocationParam`

                          - `cited_text: string`

                          - `document_index: number`

                          - `document_title: string | null`

                          - `end_page_number: number`

                          - `start_page_number: number`

                          - `type: "page_location"`

                            - `"page_location"`

                        - `CitationContentBlockLocationParam`

                          - `cited_text: string`

                          - `document_index: number`

                          - `document_title: string | null`

                          - `end_block_index: number`

                          - `start_block_index: number`

                          - `type: "content_block_location"`

                            - `"content_block_location"`

                        - `CitationWebSearchResultLocationParam`

                          - `cited_text: string`

                          - `encrypted_index: string`

                          - `title: string | null`

                          - `type: "web_search_result_location"`

                            - `"web_search_result_location"`

                          - `url: string`

                        - `CitationSearchResultLocationParam`

                          - `cited_text: string`

                          - `end_block_index: number`

                          - `search_result_index: number`

                          - `source: string`

                          - `start_block_index: number`

                          - `title: string | null`

                          - `type: "search_result_location"`

                            - `"search_result_location"`

                    - `source: string`

                    - `title: string`

                    - `type: "search_result"`

                      - `"search_result"`

                    - `cache_control?: CacheControlEphemeral | null`

                      Create a cache control breakpoint at this content block.

                      - `type: "ephemeral"`

                        - `"ephemeral"`

                      - `ttl?: "5m" | "1h"`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `"5m"`

                        - `"1h"`

                    - `citations?: CitationsConfigParam`

                      - `enabled?: boolean`

                  - `DocumentBlockParam`

                    - `source: Base64PDFSource | PlainTextSource | ContentBlockSource | URLPDFSource`

                      - `Base64PDFSource`

                        - `data: string`

                        - `media_type: "application/pdf"`

                          - `"application/pdf"`

                        - `type: "base64"`

                          - `"base64"`

                      - `PlainTextSource`

                        - `data: string`

                        - `media_type: "text/plain"`

                          - `"text/plain"`

                        - `type: "text"`

                          - `"text"`

                      - `ContentBlockSource`

                        - `content: string | Array<ContentBlockSourceContent>`

                          - `string`

                          - `Array<ContentBlockSourceContent>`

                            - `TextBlockParam`

                              - `text: string`

                              - `type: "text"`

                                - `"text"`

                              - `cache_control?: CacheControlEphemeral | null`

                                Create a cache control breakpoint at this content block.

                                - `type: "ephemeral"`

                                  - `"ephemeral"`

                                - `ttl?: "5m" | "1h"`

                                  The time-to-live for the cache control breakpoint.

                                  This may be one the following values:

                                  - `5m`: 5 minutes
                                  - `1h`: 1 hour

                                  Defaults to `5m`.

                                  - `"5m"`

                                  - `"1h"`

                              - `citations?: Array<TextCitationParam> | null`

                                - `CitationCharLocationParam`

                                  - `cited_text: string`

                                  - `document_index: number`

                                  - `document_title: string | null`

                                  - `end_char_index: number`

                                  - `start_char_index: number`

                                  - `type: "char_location"`

                                    - `"char_location"`

                                - `CitationPageLocationParam`

                                  - `cited_text: string`

                                  - `document_index: number`

                                  - `document_title: string | null`

                                  - `end_page_number: number`

                                  - `start_page_number: number`

                                  - `type: "page_location"`

                                    - `"page_location"`

                                - `CitationContentBlockLocationParam`

                                  - `cited_text: string`

                                  - `document_index: number`

                                  - `document_title: string | null`

                                  - `end_block_index: number`

                                  - `start_block_index: number`

                                  - `type: "content_block_location"`

                                    - `"content_block_location"`

                                - `CitationWebSearchResultLocationParam`

                                  - `cited_text: string`

                                  - `encrypted_index: string`

                                  - `title: string | null`

                                  - `type: "web_search_result_location"`

                                    - `"web_search_result_location"`

                                  - `url: string`

                                - `CitationSearchResultLocationParam`

                                  - `cited_text: string`

                                  - `end_block_index: number`

                                  - `search_result_index: number`

                                  - `source: string`

                                  - `start_block_index: number`

                                  - `title: string | null`

                                  - `type: "search_result_location"`

                                    - `"search_result_location"`

                            - `ImageBlockParam`

                              - `source: Base64ImageSource | URLImageSource`

                                - `Base64ImageSource`

                                  - `data: string`

                                  - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                                    - `"image/jpeg"`

                                    - `"image/png"`

                                    - `"image/gif"`

                                    - `"image/webp"`

                                  - `type: "base64"`

                                    - `"base64"`

                                - `URLImageSource`

                                  - `type: "url"`

                                    - `"url"`

                                  - `url: string`

                              - `type: "image"`

                                - `"image"`

                              - `cache_control?: CacheControlEphemeral | null`

                                Create a cache control breakpoint at this content block.

                                - `type: "ephemeral"`

                                  - `"ephemeral"`

                                - `ttl?: "5m" | "1h"`

                                  The time-to-live for the cache control breakpoint.

                                  This may be one the following values:

                                  - `5m`: 5 minutes
                                  - `1h`: 1 hour

                                  Defaults to `5m`.

                                  - `"5m"`

                                  - `"1h"`

                        - `type: "content"`

                          - `"content"`

                      - `URLPDFSource`

                        - `type: "url"`

                          - `"url"`

                        - `url: string`

                    - `type: "document"`

                      - `"document"`

                    - `cache_control?: CacheControlEphemeral | null`

                      Create a cache control breakpoint at this content block.

                      - `type: "ephemeral"`

                        - `"ephemeral"`

                      - `ttl?: "5m" | "1h"`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `"5m"`

                        - `"1h"`

                    - `citations?: CitationsConfigParam | null`

                      - `enabled?: boolean`

                    - `context?: string | null`

                    - `title?: string | null`

              - `is_error?: boolean`

            - `ServerToolUseBlockParam`

              - `id: string`

              - `input: Record<string, unknown>`

              - `name: "web_search"`

                - `"web_search"`

              - `type: "server_tool_use"`

                - `"server_tool_use"`

              - `cache_control?: CacheControlEphemeral | null`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl?: "5m" | "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

            - `WebSearchToolResultBlockParam`

              - `content: WebSearchToolResultBlockParamContent`

                - `Array<WebSearchResultBlockParam>`

                  - `encrypted_content: string`

                  - `title: string`

                  - `type: "web_search_result"`

                    - `"web_search_result"`

                  - `url: string`

                  - `page_age?: string | null`

                - `WebSearchToolRequestError`

                  - `error_code: "invalid_tool_input" | "unavailable" | "max_uses_exceeded" | 2 more`

                    - `"invalid_tool_input"`

                    - `"unavailable"`

                    - `"max_uses_exceeded"`

                    - `"too_many_requests"`

                    - `"query_too_long"`

                  - `type: "web_search_tool_result_error"`

                    - `"web_search_tool_result_error"`

              - `tool_use_id: string`

              - `type: "web_search_tool_result"`

                - `"web_search_tool_result"`

              - `cache_control?: CacheControlEphemeral | null`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl?: "5m" | "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

        - `role: "user" | "assistant"`

          - `"user"`

          - `"assistant"`

      - `model: Model`

        The model that will complete your prompt.

        See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

        - `"claude-opus-4-5-20251101" | "claude-opus-4-5" | "claude-3-7-sonnet-latest" | 17 more`

          - `"claude-opus-4-5-20251101"`

            Premium model combining maximum intelligence with practical performance

          - `"claude-opus-4-5"`

            Premium model combining maximum intelligence with practical performance

          - `"claude-3-7-sonnet-latest"`

            High-performance model with early extended thinking

          - `"claude-3-7-sonnet-20250219"`

            High-performance model with early extended thinking

          - `"claude-3-5-haiku-latest"`

            Fastest and most compact model for near-instant responsiveness

          - `"claude-3-5-haiku-20241022"`

            Our fastest model

          - `"claude-haiku-4-5"`

            Hybrid model, capable of near-instant responses and extended thinking

          - `"claude-haiku-4-5-20251001"`

            Hybrid model, capable of near-instant responses and extended thinking

          - `"claude-sonnet-4-20250514"`

            High-performance model with extended thinking

          - `"claude-sonnet-4-0"`

            High-performance model with extended thinking

          - `"claude-4-sonnet-20250514"`

            High-performance model with extended thinking

          - `"claude-sonnet-4-5"`

            Our best model for real-world agents and coding

          - `"claude-sonnet-4-5-20250929"`

            Our best model for real-world agents and coding

          - `"claude-opus-4-0"`

            Our most capable model

          - `"claude-opus-4-20250514"`

            Our most capable model

          - `"claude-4-opus-20250514"`

            Our most capable model

          - `"claude-opus-4-1-20250805"`

            Our most capable model

          - `"claude-3-opus-latest"`

            Excels at writing and complex tasks

          - `"claude-3-opus-20240229"`

            Excels at writing and complex tasks

          - `"claude-3-haiku-20240307"`

            Our previous most fast and cost-effective

        - `(string & {})`

      - `metadata?: Metadata`

        An object describing metadata about the request.

        - `user_id?: string | null`

          An external identifier for the user who is associated with the request.

          This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

      - `service_tier?: "auto" | "standard_only"`

        Determines whether to use priority capacity (if available) or standard capacity for this request.

        Anthropic offers different levels of service for your API requests. See [service-tiers](https://docs.claude.com/en/api/service-tiers) for details.

        - `"auto"`

        - `"standard_only"`

      - `stop_sequences?: Array<string>`

        Custom text sequences that will cause the model to stop generating.

        Our models will normally stop when they have naturally completed their turn, which will result in a response `stop_reason` of `"end_turn"`.

        If you want the model to stop generating when it encounters custom strings of text, you can use the `stop_sequences` parameter. If the model encounters one of the custom sequences, the response `stop_reason` value will be `"stop_sequence"` and the response `stop_sequence` value will contain the matched stop sequence.

      - `stream?: boolean`

        Whether to incrementally stream the response using server-sent events.

        See [streaming](https://docs.claude.com/en/api/messages-streaming) for details.

      - `system?: string | Array<TextBlockParam>`

        System prompt.

        A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

        - `string`

        - `Array<TextBlockParam>`

          - `text: string`

          - `type: "text"`

            - `"text"`

          - `cache_control?: CacheControlEphemeral | null`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl?: "5m" | "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

          - `citations?: Array<TextCitationParam> | null`

            - `CitationCharLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_char_index: number`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `CitationPageLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_page_number: number`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `CitationContentBlockLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_block_index: number`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `CitationWebSearchResultLocationParam`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string | null`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `CitationSearchResultLocationParam`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string | null`

              - `type: "search_result_location"`

                - `"search_result_location"`

      - `temperature?: number`

        Amount of randomness injected into the response.

        Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.

        Note that even with `temperature` of `0.0`, the results will not be fully deterministic.

      - `thinking?: ThinkingConfigParam`

        Configuration for enabling Claude's extended thinking.

        When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

        See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

        - `ThinkingConfigEnabled`

          - `budget_tokens: number`

            Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

            Must be ≥1024 and less than `max_tokens`.

            See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

          - `type: "enabled"`

            - `"enabled"`

        - `ThinkingConfigDisabled`

          - `type: "disabled"`

            - `"disabled"`

      - `tool_choice?: ToolChoice`

        How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

        - `ToolChoiceAuto`

          The model will automatically decide whether to use tools.

          - `type: "auto"`

            - `"auto"`

          - `disable_parallel_tool_use?: boolean`

            Whether to disable parallel tool use.

            Defaults to `false`. If set to `true`, the model will output at most one tool use.

        - `ToolChoiceAny`

          The model will use any available tools.

          - `type: "any"`

            - `"any"`

          - `disable_parallel_tool_use?: boolean`

            Whether to disable parallel tool use.

            Defaults to `false`. If set to `true`, the model will output exactly one tool use.

        - `ToolChoiceTool`

          The model will use the specified tool with `tool_choice.name`.

          - `name: string`

            The name of the tool to use.

          - `type: "tool"`

            - `"tool"`

          - `disable_parallel_tool_use?: boolean`

            Whether to disable parallel tool use.

            Defaults to `false`. If set to `true`, the model will output exactly one tool use.

        - `ToolChoiceNone`

          The model will not be allowed to use tools.

          - `type: "none"`

            - `"none"`

      - `tools?: Array<ToolUnion>`

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

        - `Tool`

          - `input_schema: InputSchema`

            [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

            This defines the shape of the `input` that your tool accepts and that the model will produce.

            - `type: "object"`

              - `"object"`

            - `properties?: Record<string, unknown> | null`

            - `required?: Array<string> | null`

          - `name: string`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

          - `cache_control?: CacheControlEphemeral | null`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl?: "5m" | "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

          - `description?: string`

            Description of what this tool does.

            Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

          - `type?: "custom" | null`

            - `"custom"`

        - `ToolBash20250124`

          - `name: "bash"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"bash"`

          - `type: "bash_20250124"`

            - `"bash_20250124"`

          - `cache_control?: CacheControlEphemeral | null`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl?: "5m" | "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

        - `ToolTextEditor20250124`

          - `name: "str_replace_editor"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"str_replace_editor"`

          - `type: "text_editor_20250124"`

            - `"text_editor_20250124"`

          - `cache_control?: CacheControlEphemeral | null`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl?: "5m" | "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

        - `ToolTextEditor20250429`

          - `name: "str_replace_based_edit_tool"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"str_replace_based_edit_tool"`

          - `type: "text_editor_20250429"`

            - `"text_editor_20250429"`

          - `cache_control?: CacheControlEphemeral | null`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl?: "5m" | "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

        - `ToolTextEditor20250728`

          - `name: "str_replace_based_edit_tool"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"str_replace_based_edit_tool"`

          - `type: "text_editor_20250728"`

            - `"text_editor_20250728"`

          - `cache_control?: CacheControlEphemeral | null`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl?: "5m" | "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

          - `max_characters?: number | null`

            Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

        - `WebSearchTool20250305`

          - `name: "web_search"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"web_search"`

          - `type: "web_search_20250305"`

            - `"web_search_20250305"`

          - `allowed_domains?: Array<string> | null`

            If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

          - `blocked_domains?: Array<string> | null`

            If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

          - `cache_control?: CacheControlEphemeral | null`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl?: "5m" | "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

          - `max_uses?: number | null`

            Maximum number of times the tool can be used in the API request.

          - `user_location?: UserLocation | null`

            Parameters for the user's location. Used to provide more relevant search results.

            - `type: "approximate"`

              - `"approximate"`

            - `city?: string | null`

              The city of the user.

            - `country?: string | null`

              The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

            - `region?: string | null`

              The region of the user.

            - `timezone?: string | null`

              The [IANA timezone](https://nodatime.org/TimeZones) of the user.

      - `top_k?: number`

        Only sample from the top K options for each subsequent token.

        Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

        Recommended for advanced use cases only. You usually only need to use `temperature`.

      - `top_p?: number`

        Use nucleus sampling.

        In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

        Recommended for advanced use cases only. You usually only need to use `temperature`.

### Returns

- `MessageBatch`

  - `id: string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archived_at: string | null`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancel_initiated_at: string | null`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `created_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `ended_at: string | null`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expires_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processing_status: "in_progress" | "canceling" | "ended"`

    Processing status of the Message Batch.

    - `"in_progress"`

    - `"canceling"`

    - `"ended"`

  - `request_counts: MessageBatchRequestCounts`

    Tallies requests within the Message Batch, categorized by their status.

    Requests start as `processing` and move to one of the other statuses only once processing of the entire batch ends. The sum of all values always matches the total number of requests in the batch.

    - `canceled: number`

      Number of requests in the Message Batch that have been canceled.

      This is zero until processing of the entire Message Batch has ended.

    - `errored: number`

      Number of requests in the Message Batch that encountered an error.

      This is zero until processing of the entire Message Batch has ended.

    - `expired: number`

      Number of requests in the Message Batch that have expired.

      This is zero until processing of the entire Message Batch has ended.

    - `processing: number`

      Number of requests in the Message Batch that are processing.

    - `succeeded: number`

      Number of requests in the Message Batch that have completed successfully.

      This is zero until processing of the entire Message Batch has ended.

  - `results_url: string | null`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: "message_batch"`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `"message_batch"`

### Example

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: 'my-anthropic-api-key',
});

const messageBatch = await client.messages.batches.create({
  requests: [
    {
      custom_id: 'my-custom-id-1',
      params: {
        max_tokens: 1024,
        messages: [{ content: 'Hello, world', role: 'user' }],
        model: 'claude-sonnet-4-5-20250929',
      },
    },
  ],
});

console.log(messageBatch.id);
```
