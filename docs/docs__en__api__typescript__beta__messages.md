# Messages

## Create

`client.beta.messages.create(MessageCreateParamsparams, RequestOptionsoptions?): BetaMessage | Stream<BetaRawMessageStreamEvent>`

**post** `/v1/messages`

Send a structured list of input messages with text and/or image content, and the model will generate the next message in the conversation.

The Messages API can be used for either single queries or stateless multi-turn conversations.

Learn more about the Messages API in our [user guide](https://docs.claude.com/en/docs/initial-setup)

### Parameters

- `MessageCreateParams = MessageCreateParamsNonStreaming | MessageCreateParamsStreaming`

  - `MessageCreateParamsBase`

    - `max_tokens: number`

      Body param: The maximum number of tokens to generate before stopping.

      Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

      Different models have different maximum values for this parameter.  See [models](https://docs.claude.com/en/docs/models-overview) for details.

    - `messages: Array<BetaMessageParam>`

      Body param: Input messages.

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

      - `content: string | Array<BetaContentBlockParam>`

        - `string`

        - `Array<BetaContentBlockParam>`

          - `BetaTextBlockParam`

            - `text: string`

            - `type: "text"`

              - `"text"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `citations?: Array<BetaTextCitationParam> | null`

              - `BetaCitationCharLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_char_index: number`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `BetaCitationPageLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_page_number: number`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `BetaCitationContentBlockLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_block_index: number`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `BetaCitationWebSearchResultLocationParam`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string | null`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `BetaCitationSearchResultLocationParam`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string | null`

                - `type: "search_result_location"`

                  - `"search_result_location"`

          - `BetaImageBlockParam`

            - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

              - `BetaBase64ImageSource`

                - `data: string`

                - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                  - `"image/jpeg"`

                  - `"image/png"`

                  - `"image/gif"`

                  - `"image/webp"`

                - `type: "base64"`

                  - `"base64"`

              - `BetaURLImageSource`

                - `type: "url"`

                  - `"url"`

                - `url: string`

              - `BetaFileImageSource`

                - `file_id: string`

                - `type: "file"`

                  - `"file"`

            - `type: "image"`

              - `"image"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `BetaRequestDocumentBlock`

            - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

              - `BetaBase64PDFSource`

                - `data: string`

                - `media_type: "application/pdf"`

                  - `"application/pdf"`

                - `type: "base64"`

                  - `"base64"`

              - `BetaPlainTextSource`

                - `data: string`

                - `media_type: "text/plain"`

                  - `"text/plain"`

                - `type: "text"`

                  - `"text"`

              - `BetaContentBlockSource`

                - `content: string | Array<BetaContentBlockSourceContent>`

                  - `string`

                  - `Array<BetaContentBlockSourceContent>`

                    - `BetaTextBlockParam`

                      - `text: string`

                      - `type: "text"`

                        - `"text"`

                      - `cache_control?: BetaCacheControlEphemeral | null`

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

                      - `citations?: Array<BetaTextCitationParam> | null`

                        - `BetaCitationCharLocationParam`

                          - `cited_text: string`

                          - `document_index: number`

                          - `document_title: string | null`

                          - `end_char_index: number`

                          - `start_char_index: number`

                          - `type: "char_location"`

                            - `"char_location"`

                        - `BetaCitationPageLocationParam`

                          - `cited_text: string`

                          - `document_index: number`

                          - `document_title: string | null`

                          - `end_page_number: number`

                          - `start_page_number: number`

                          - `type: "page_location"`

                            - `"page_location"`

                        - `BetaCitationContentBlockLocationParam`

                          - `cited_text: string`

                          - `document_index: number`

                          - `document_title: string | null`

                          - `end_block_index: number`

                          - `start_block_index: number`

                          - `type: "content_block_location"`

                            - `"content_block_location"`

                        - `BetaCitationWebSearchResultLocationParam`

                          - `cited_text: string`

                          - `encrypted_index: string`

                          - `title: string | null`

                          - `type: "web_search_result_location"`

                            - `"web_search_result_location"`

                          - `url: string`

                        - `BetaCitationSearchResultLocationParam`

                          - `cited_text: string`

                          - `end_block_index: number`

                          - `search_result_index: number`

                          - `source: string`

                          - `start_block_index: number`

                          - `title: string | null`

                          - `type: "search_result_location"`

                            - `"search_result_location"`

                    - `BetaImageBlockParam`

                      - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                        - `BetaBase64ImageSource`

                          - `data: string`

                          - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                            - `"image/jpeg"`

                            - `"image/png"`

                            - `"image/gif"`

                            - `"image/webp"`

                          - `type: "base64"`

                            - `"base64"`

                        - `BetaURLImageSource`

                          - `type: "url"`

                            - `"url"`

                          - `url: string`

                        - `BetaFileImageSource`

                          - `file_id: string`

                          - `type: "file"`

                            - `"file"`

                      - `type: "image"`

                        - `"image"`

                      - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `BetaURLPDFSource`

                - `type: "url"`

                  - `"url"`

                - `url: string`

              - `BetaFileDocumentSource`

                - `file_id: string`

                - `type: "file"`

                  - `"file"`

            - `type: "document"`

              - `"document"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `citations?: BetaCitationsConfigParam | null`

              - `enabled?: boolean`

            - `context?: string | null`

            - `title?: string | null`

          - `BetaSearchResultBlockParam`

            - `content: Array<BetaTextBlockParam>`

              - `text: string`

              - `type: "text"`

                - `"text"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `citations?: Array<BetaTextCitationParam> | null`

                - `BetaCitationCharLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_char_index: number`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `BetaCitationPageLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_page_number: number`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `BetaCitationContentBlockLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_block_index: number`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `BetaCitationWebSearchResultLocationParam`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string | null`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `BetaCitationSearchResultLocationParam`

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

            - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `citations?: BetaCitationsConfigParam`

              - `enabled?: boolean`

          - `BetaThinkingBlockParam`

            - `signature: string`

            - `thinking: string`

            - `type: "thinking"`

              - `"thinking"`

          - `BetaRedactedThinkingBlockParam`

            - `data: string`

            - `type: "redacted_thinking"`

              - `"redacted_thinking"`

          - `BetaToolUseBlockParam`

            - `id: string`

            - `input: Record<string, unknown>`

            - `name: string`

            - `type: "tool_use"`

              - `"tool_use"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `caller?: BetaDirectCaller | BetaServerToolCaller`

              Tool invocation directly from the model.

              - `BetaDirectCaller`

                Tool invocation directly from the model.

                - `type: "direct"`

                  - `"direct"`

              - `BetaServerToolCaller`

                Tool invocation generated by a server-side tool.

                - `tool_id: string`

                - `type: "code_execution_20250825"`

                  - `"code_execution_20250825"`

          - `BetaToolResultBlockParam`

            - `tool_use_id: string`

            - `type: "tool_result"`

              - `"tool_result"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `content?: string | Array<BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more>`

              - `string`

              - `Array<BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more>`

                - `BetaTextBlockParam`

                  - `text: string`

                  - `type: "text"`

                    - `"text"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

                  - `citations?: Array<BetaTextCitationParam> | null`

                    - `BetaCitationCharLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_char_index: number`

                      - `start_char_index: number`

                      - `type: "char_location"`

                        - `"char_location"`

                    - `BetaCitationPageLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_page_number: number`

                      - `start_page_number: number`

                      - `type: "page_location"`

                        - `"page_location"`

                    - `BetaCitationContentBlockLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_block_index: number`

                      - `start_block_index: number`

                      - `type: "content_block_location"`

                        - `"content_block_location"`

                    - `BetaCitationWebSearchResultLocationParam`

                      - `cited_text: string`

                      - `encrypted_index: string`

                      - `title: string | null`

                      - `type: "web_search_result_location"`

                        - `"web_search_result_location"`

                      - `url: string`

                    - `BetaCitationSearchResultLocationParam`

                      - `cited_text: string`

                      - `end_block_index: number`

                      - `search_result_index: number`

                      - `source: string`

                      - `start_block_index: number`

                      - `title: string | null`

                      - `type: "search_result_location"`

                        - `"search_result_location"`

                - `BetaImageBlockParam`

                  - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                    - `BetaBase64ImageSource`

                      - `data: string`

                      - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                        - `"image/jpeg"`

                        - `"image/png"`

                        - `"image/gif"`

                        - `"image/webp"`

                      - `type: "base64"`

                        - `"base64"`

                    - `BetaURLImageSource`

                      - `type: "url"`

                        - `"url"`

                      - `url: string`

                    - `BetaFileImageSource`

                      - `file_id: string`

                      - `type: "file"`

                        - `"file"`

                  - `type: "image"`

                    - `"image"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

                - `BetaSearchResultBlockParam`

                  - `content: Array<BetaTextBlockParam>`

                    - `text: string`

                    - `type: "text"`

                      - `"text"`

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

                    - `citations?: Array<BetaTextCitationParam> | null`

                      - `BetaCitationCharLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_char_index: number`

                        - `start_char_index: number`

                        - `type: "char_location"`

                          - `"char_location"`

                      - `BetaCitationPageLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_page_number: number`

                        - `start_page_number: number`

                        - `type: "page_location"`

                          - `"page_location"`

                      - `BetaCitationContentBlockLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_block_index: number`

                        - `start_block_index: number`

                        - `type: "content_block_location"`

                          - `"content_block_location"`

                      - `BetaCitationWebSearchResultLocationParam`

                        - `cited_text: string`

                        - `encrypted_index: string`

                        - `title: string | null`

                        - `type: "web_search_result_location"`

                          - `"web_search_result_location"`

                        - `url: string`

                      - `BetaCitationSearchResultLocationParam`

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

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

                  - `citations?: BetaCitationsConfigParam`

                    - `enabled?: boolean`

                - `BetaRequestDocumentBlock`

                  - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

                    - `BetaBase64PDFSource`

                      - `data: string`

                      - `media_type: "application/pdf"`

                        - `"application/pdf"`

                      - `type: "base64"`

                        - `"base64"`

                    - `BetaPlainTextSource`

                      - `data: string`

                      - `media_type: "text/plain"`

                        - `"text/plain"`

                      - `type: "text"`

                        - `"text"`

                    - `BetaContentBlockSource`

                      - `content: string | Array<BetaContentBlockSourceContent>`

                        - `string`

                        - `Array<BetaContentBlockSourceContent>`

                          - `BetaTextBlockParam`

                            - `text: string`

                            - `type: "text"`

                              - `"text"`

                            - `cache_control?: BetaCacheControlEphemeral | null`

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

                            - `citations?: Array<BetaTextCitationParam> | null`

                              - `BetaCitationCharLocationParam`

                                - `cited_text: string`

                                - `document_index: number`

                                - `document_title: string | null`

                                - `end_char_index: number`

                                - `start_char_index: number`

                                - `type: "char_location"`

                                  - `"char_location"`

                              - `BetaCitationPageLocationParam`

                                - `cited_text: string`

                                - `document_index: number`

                                - `document_title: string | null`

                                - `end_page_number: number`

                                - `start_page_number: number`

                                - `type: "page_location"`

                                  - `"page_location"`

                              - `BetaCitationContentBlockLocationParam`

                                - `cited_text: string`

                                - `document_index: number`

                                - `document_title: string | null`

                                - `end_block_index: number`

                                - `start_block_index: number`

                                - `type: "content_block_location"`

                                  - `"content_block_location"`

                              - `BetaCitationWebSearchResultLocationParam`

                                - `cited_text: string`

                                - `encrypted_index: string`

                                - `title: string | null`

                                - `type: "web_search_result_location"`

                                  - `"web_search_result_location"`

                                - `url: string`

                              - `BetaCitationSearchResultLocationParam`

                                - `cited_text: string`

                                - `end_block_index: number`

                                - `search_result_index: number`

                                - `source: string`

                                - `start_block_index: number`

                                - `title: string | null`

                                - `type: "search_result_location"`

                                  - `"search_result_location"`

                          - `BetaImageBlockParam`

                            - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                              - `BetaBase64ImageSource`

                                - `data: string`

                                - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                                  - `"image/jpeg"`

                                  - `"image/png"`

                                  - `"image/gif"`

                                  - `"image/webp"`

                                - `type: "base64"`

                                  - `"base64"`

                              - `BetaURLImageSource`

                                - `type: "url"`

                                  - `"url"`

                                - `url: string`

                              - `BetaFileImageSource`

                                - `file_id: string`

                                - `type: "file"`

                                  - `"file"`

                            - `type: "image"`

                              - `"image"`

                            - `cache_control?: BetaCacheControlEphemeral | null`

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

                    - `BetaURLPDFSource`

                      - `type: "url"`

                        - `"url"`

                      - `url: string`

                    - `BetaFileDocumentSource`

                      - `file_id: string`

                      - `type: "file"`

                        - `"file"`

                  - `type: "document"`

                    - `"document"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

                  - `citations?: BetaCitationsConfigParam | null`

                    - `enabled?: boolean`

                  - `context?: string | null`

                  - `title?: string | null`

                - `BetaToolReferenceBlockParam`

                  Tool reference block that can be included in tool_result content.

                  - `tool_name: string`

                  - `type: "tool_reference"`

                    - `"tool_reference"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `is_error?: boolean`

          - `BetaServerToolUseBlockParam`

            - `id: string`

            - `input: Record<string, unknown>`

            - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

              - `"web_search"`

              - `"web_fetch"`

              - `"code_execution"`

              - `"bash_code_execution"`

              - `"text_editor_code_execution"`

              - `"tool_search_tool_regex"`

              - `"tool_search_tool_bm25"`

            - `type: "server_tool_use"`

              - `"server_tool_use"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `caller?: BetaDirectCaller | BetaServerToolCaller`

              Tool invocation directly from the model.

              - `BetaDirectCaller`

                Tool invocation directly from the model.

                - `type: "direct"`

                  - `"direct"`

              - `BetaServerToolCaller`

                Tool invocation generated by a server-side tool.

                - `tool_id: string`

                - `type: "code_execution_20250825"`

                  - `"code_execution_20250825"`

          - `BetaWebSearchToolResultBlockParam`

            - `content: BetaWebSearchToolResultBlockParamContent`

              - `Array<BetaWebSearchResultBlockParam>`

                - `encrypted_content: string`

                - `title: string`

                - `type: "web_search_result"`

                  - `"web_search_result"`

                - `url: string`

                - `page_age?: string | null`

              - `BetaWebSearchToolRequestError`

                - `error_code: BetaWebSearchToolResultErrorCode`

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

            - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `BetaWebFetchToolResultBlockParam`

            - `content: BetaWebFetchToolResultErrorBlockParam | BetaWebFetchBlockParam`

              - `BetaWebFetchToolResultErrorBlockParam`

                - `error_code: BetaWebFetchToolResultErrorCode`

                  - `"invalid_tool_input"`

                  - `"url_too_long"`

                  - `"url_not_allowed"`

                  - `"url_not_accessible"`

                  - `"unsupported_content_type"`

                  - `"too_many_requests"`

                  - `"max_uses_exceeded"`

                  - `"unavailable"`

                - `type: "web_fetch_tool_result_error"`

                  - `"web_fetch_tool_result_error"`

              - `BetaWebFetchBlockParam`

                - `content: BetaRequestDocumentBlock`

                  - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

                    - `BetaBase64PDFSource`

                      - `data: string`

                      - `media_type: "application/pdf"`

                        - `"application/pdf"`

                      - `type: "base64"`

                        - `"base64"`

                    - `BetaPlainTextSource`

                      - `data: string`

                      - `media_type: "text/plain"`

                        - `"text/plain"`

                      - `type: "text"`

                        - `"text"`

                    - `BetaContentBlockSource`

                      - `content: string | Array<BetaContentBlockSourceContent>`

                        - `string`

                        - `Array<BetaContentBlockSourceContent>`

                          - `BetaTextBlockParam`

                            - `text: string`

                            - `type: "text"`

                              - `"text"`

                            - `cache_control?: BetaCacheControlEphemeral | null`

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

                            - `citations?: Array<BetaTextCitationParam> | null`

                              - `BetaCitationCharLocationParam`

                                - `cited_text: string`

                                - `document_index: number`

                                - `document_title: string | null`

                                - `end_char_index: number`

                                - `start_char_index: number`

                                - `type: "char_location"`

                                  - `"char_location"`

                              - `BetaCitationPageLocationParam`

                                - `cited_text: string`

                                - `document_index: number`

                                - `document_title: string | null`

                                - `end_page_number: number`

                                - `start_page_number: number`

                                - `type: "page_location"`

                                  - `"page_location"`

                              - `BetaCitationContentBlockLocationParam`

                                - `cited_text: string`

                                - `document_index: number`

                                - `document_title: string | null`

                                - `end_block_index: number`

                                - `start_block_index: number`

                                - `type: "content_block_location"`

                                  - `"content_block_location"`

                              - `BetaCitationWebSearchResultLocationParam`

                                - `cited_text: string`

                                - `encrypted_index: string`

                                - `title: string | null`

                                - `type: "web_search_result_location"`

                                  - `"web_search_result_location"`

                                - `url: string`

                              - `BetaCitationSearchResultLocationParam`

                                - `cited_text: string`

                                - `end_block_index: number`

                                - `search_result_index: number`

                                - `source: string`

                                - `start_block_index: number`

                                - `title: string | null`

                                - `type: "search_result_location"`

                                  - `"search_result_location"`

                          - `BetaImageBlockParam`

                            - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                              - `BetaBase64ImageSource`

                                - `data: string`

                                - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                                  - `"image/jpeg"`

                                  - `"image/png"`

                                  - `"image/gif"`

                                  - `"image/webp"`

                                - `type: "base64"`

                                  - `"base64"`

                              - `BetaURLImageSource`

                                - `type: "url"`

                                  - `"url"`

                                - `url: string`

                              - `BetaFileImageSource`

                                - `file_id: string`

                                - `type: "file"`

                                  - `"file"`

                            - `type: "image"`

                              - `"image"`

                            - `cache_control?: BetaCacheControlEphemeral | null`

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

                    - `BetaURLPDFSource`

                      - `type: "url"`

                        - `"url"`

                      - `url: string`

                    - `BetaFileDocumentSource`

                      - `file_id: string`

                      - `type: "file"`

                        - `"file"`

                  - `type: "document"`

                    - `"document"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

                  - `citations?: BetaCitationsConfigParam | null`

                    - `enabled?: boolean`

                  - `context?: string | null`

                  - `title?: string | null`

                - `type: "web_fetch_result"`

                  - `"web_fetch_result"`

                - `url: string`

                  Fetched content URL

                - `retrieved_at?: string | null`

                  ISO 8601 timestamp when the content was retrieved

            - `tool_use_id: string`

            - `type: "web_fetch_tool_result"`

              - `"web_fetch_tool_result"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `BetaCodeExecutionToolResultBlockParam`

            - `content: BetaCodeExecutionToolResultBlockParamContent`

              - `BetaCodeExecutionToolResultErrorParam`

                - `error_code: BetaCodeExecutionToolResultErrorCode`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"too_many_requests"`

                  - `"execution_time_exceeded"`

                - `type: "code_execution_tool_result_error"`

                  - `"code_execution_tool_result_error"`

              - `BetaCodeExecutionResultBlockParam`

                - `content: Array<BetaCodeExecutionOutputBlockParam>`

                  - `file_id: string`

                  - `type: "code_execution_output"`

                    - `"code_execution_output"`

                - `return_code: number`

                - `stderr: string`

                - `stdout: string`

                - `type: "code_execution_result"`

                  - `"code_execution_result"`

            - `tool_use_id: string`

            - `type: "code_execution_tool_result"`

              - `"code_execution_tool_result"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `BetaBashCodeExecutionToolResultBlockParam`

            - `content: BetaBashCodeExecutionToolResultErrorParam | BetaBashCodeExecutionResultBlockParam`

              - `BetaBashCodeExecutionToolResultErrorParam`

                - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"too_many_requests"`

                  - `"execution_time_exceeded"`

                  - `"output_file_too_large"`

                - `type: "bash_code_execution_tool_result_error"`

                  - `"bash_code_execution_tool_result_error"`

              - `BetaBashCodeExecutionResultBlockParam`

                - `content: Array<BetaBashCodeExecutionOutputBlockParam>`

                  - `file_id: string`

                  - `type: "bash_code_execution_output"`

                    - `"bash_code_execution_output"`

                - `return_code: number`

                - `stderr: string`

                - `stdout: string`

                - `type: "bash_code_execution_result"`

                  - `"bash_code_execution_result"`

            - `tool_use_id: string`

            - `type: "bash_code_execution_tool_result"`

              - `"bash_code_execution_tool_result"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `BetaTextEditorCodeExecutionToolResultBlockParam`

            - `content: BetaTextEditorCodeExecutionToolResultErrorParam | BetaTextEditorCodeExecutionViewResultBlockParam | BetaTextEditorCodeExecutionCreateResultBlockParam | BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

              - `BetaTextEditorCodeExecutionToolResultErrorParam`

                - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"too_many_requests"`

                  - `"execution_time_exceeded"`

                  - `"file_not_found"`

                - `type: "text_editor_code_execution_tool_result_error"`

                  - `"text_editor_code_execution_tool_result_error"`

                - `error_message?: string | null`

              - `BetaTextEditorCodeExecutionViewResultBlockParam`

                - `content: string`

                - `file_type: "text" | "image" | "pdf"`

                  - `"text"`

                  - `"image"`

                  - `"pdf"`

                - `type: "text_editor_code_execution_view_result"`

                  - `"text_editor_code_execution_view_result"`

                - `num_lines?: number | null`

                - `start_line?: number | null`

                - `total_lines?: number | null`

              - `BetaTextEditorCodeExecutionCreateResultBlockParam`

                - `is_file_update: boolean`

                - `type: "text_editor_code_execution_create_result"`

                  - `"text_editor_code_execution_create_result"`

              - `BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

                - `type: "text_editor_code_execution_str_replace_result"`

                  - `"text_editor_code_execution_str_replace_result"`

                - `lines?: Array<string> | null`

                - `new_lines?: number | null`

                - `new_start?: number | null`

                - `old_lines?: number | null`

                - `old_start?: number | null`

            - `tool_use_id: string`

            - `type: "text_editor_code_execution_tool_result"`

              - `"text_editor_code_execution_tool_result"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `BetaToolSearchToolResultBlockParam`

            - `content: BetaToolSearchToolResultErrorParam | BetaToolSearchToolSearchResultBlockParam`

              - `BetaToolSearchToolResultErrorParam`

                - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"too_many_requests"`

                  - `"execution_time_exceeded"`

                - `type: "tool_search_tool_result_error"`

                  - `"tool_search_tool_result_error"`

              - `BetaToolSearchToolSearchResultBlockParam`

                - `tool_references: Array<BetaToolReferenceBlockParam>`

                  - `tool_name: string`

                  - `type: "tool_reference"`

                    - `"tool_reference"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

                - `type: "tool_search_tool_search_result"`

                  - `"tool_search_tool_search_result"`

            - `tool_use_id: string`

            - `type: "tool_search_tool_result"`

              - `"tool_search_tool_result"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `BetaMCPToolUseBlockParam`

            - `id: string`

            - `input: Record<string, unknown>`

            - `name: string`

            - `server_name: string`

              The name of the MCP server

            - `type: "mcp_tool_use"`

              - `"mcp_tool_use"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `BetaRequestMCPToolResultBlockParam`

            - `tool_use_id: string`

            - `type: "mcp_tool_result"`

              - `"mcp_tool_result"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `content?: string | Array<BetaTextBlockParam>`

              - `string`

              - `Array<BetaTextBlockParam>`

                - `text: string`

                - `type: "text"`

                  - `"text"`

                - `cache_control?: BetaCacheControlEphemeral | null`

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

                - `citations?: Array<BetaTextCitationParam> | null`

                  - `BetaCitationCharLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_char_index: number`

                    - `start_char_index: number`

                    - `type: "char_location"`

                      - `"char_location"`

                  - `BetaCitationPageLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_page_number: number`

                    - `start_page_number: number`

                    - `type: "page_location"`

                      - `"page_location"`

                  - `BetaCitationContentBlockLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_block_index: number`

                    - `start_block_index: number`

                    - `type: "content_block_location"`

                      - `"content_block_location"`

                  - `BetaCitationWebSearchResultLocationParam`

                    - `cited_text: string`

                    - `encrypted_index: string`

                    - `title: string | null`

                    - `type: "web_search_result_location"`

                      - `"web_search_result_location"`

                    - `url: string`

                  - `BetaCitationSearchResultLocationParam`

                    - `cited_text: string`

                    - `end_block_index: number`

                    - `search_result_index: number`

                    - `source: string`

                    - `start_block_index: number`

                    - `title: string | null`

                    - `type: "search_result_location"`

                      - `"search_result_location"`

            - `is_error?: boolean`

          - `BetaContainerUploadBlockParam`

            A content block that represents a file to be uploaded to the container
            Files uploaded via this block will be available in the container's input directory.

            - `file_id: string`

            - `type: "container_upload"`

              - `"container_upload"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

      Body param: The model that will complete your prompt.

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

    - `container?: BetaContainerParams | string | null`

      Body param: Container identifier for reuse across requests.

      - `BetaContainerParams`

        Container parameters with skills to be loaded.

        - `id?: string | null`

          Container id

        - `skills?: Array<BetaSkillParams> | null`

          List of skills to load in the container

          - `skill_id: string`

            Skill ID

          - `type: "anthropic" | "custom"`

            Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

            - `"anthropic"`

            - `"custom"`

          - `version?: string`

            Skill version or 'latest' for most recent version

      - `string`

    - `context_management?: BetaContextManagementConfig | null`

      Body param: Context management configuration.

      This allows you to control how Claude manages context across multiple requests, such as whether to clear function results or not.

      - `edits?: Array<BetaClearToolUses20250919Edit | BetaClearThinking20251015Edit>`

        List of context management edits to apply

        - `BetaClearToolUses20250919Edit`

          - `type: "clear_tool_uses_20250919"`

            - `"clear_tool_uses_20250919"`

          - `clear_at_least?: BetaInputTokensClearAtLeast | null`

            Minimum number of tokens that must be cleared when triggered. Context will only be modified if at least this many tokens can be removed.

            - `type: "input_tokens"`

              - `"input_tokens"`

            - `value: number`

          - `clear_tool_inputs?: boolean | Array<string> | null`

            Whether to clear all tool inputs (bool) or specific tool inputs to clear (list)

            - `boolean`

            - `Array<string>`

          - `exclude_tools?: Array<string> | null`

            Tool names whose uses are preserved from clearing

          - `keep?: BetaToolUsesKeep`

            Number of tool uses to retain in the conversation

            - `type: "tool_uses"`

              - `"tool_uses"`

            - `value: number`

          - `trigger?: BetaInputTokensTrigger | BetaToolUsesTrigger`

            Condition that triggers the context management strategy

            - `BetaInputTokensTrigger`

              - `type: "input_tokens"`

                - `"input_tokens"`

              - `value: number`

            - `BetaToolUsesTrigger`

              - `type: "tool_uses"`

                - `"tool_uses"`

              - `value: number`

        - `BetaClearThinking20251015Edit`

          - `type: "clear_thinking_20251015"`

            - `"clear_thinking_20251015"`

          - `keep?: BetaThinkingTurns | BetaAllThinkingTurns | "all"`

            Number of most recent assistant turns to keep thinking blocks for. Older turns will have their thinking blocks removed.

            - `BetaThinkingTurns`

              - `type: "thinking_turns"`

                - `"thinking_turns"`

              - `value: number`

            - `BetaAllThinkingTurns`

              - `type: "all"`

                - `"all"`

            - `"all"`

              - `"all"`

    - `mcp_servers?: Array<BetaRequestMCPServerURLDefinition>`

      Body param: MCP servers to be utilized in this request

      - `name: string`

      - `type: "url"`

        - `"url"`

      - `url: string`

      - `authorization_token?: string | null`

      - `tool_configuration?: BetaRequestMCPServerToolConfiguration | null`

        - `allowed_tools?: Array<string> | null`

        - `enabled?: boolean | null`

    - `metadata?: BetaMetadata`

      Body param: An object describing metadata about the request.

      - `user_id?: string | null`

        An external identifier for the user who is associated with the request.

        This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

    - `output_config?: BetaOutputConfig`

      Body param: Configuration options for the model's output. Controls aspects like how much effort the model puts into its response.

      - `effort?: "low" | "medium" | "high" | null`

        All possible effort levels.

        - `"low"`

        - `"medium"`

        - `"high"`

    - `output_format?: BetaJSONOutputFormat | null`

      Body param:
      A schema to specify Claude's output format in responses.

      - `schema: Record<string, unknown>`

        The JSON schema of the format

      - `type: "json_schema"`

        - `"json_schema"`

    - `service_tier?: "auto" | "standard_only"`

      Body param: Determines whether to use priority capacity (if available) or standard capacity for this request.

      Anthropic offers different levels of service for your API requests. See [service-tiers](https://docs.claude.com/en/api/service-tiers) for details.

      - `"auto"`

      - `"standard_only"`

    - `stop_sequences?: Array<string>`

      Body param: Custom text sequences that will cause the model to stop generating.

      Our models will normally stop when they have naturally completed their turn, which will result in a response `stop_reason` of `"end_turn"`.

      If you want the model to stop generating when it encounters custom strings of text, you can use the `stop_sequences` parameter. If the model encounters one of the custom sequences, the response `stop_reason` value will be `"stop_sequence"` and the response `stop_sequence` value will contain the matched stop sequence.

    - `stream?: false`

      Body param: Whether to incrementally stream the response using server-sent events.

      See [streaming](https://docs.claude.com/en/api/messages-streaming) for details.

      - `false`

    - `system?: string | Array<BetaTextBlockParam>`

      Body param: System prompt.

      A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

      - `string`

      - `Array<BetaTextBlockParam>`

        - `text: string`

        - `type: "text"`

          - `"text"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `citations?: Array<BetaTextCitationParam> | null`

          - `BetaCitationCharLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_char_index: number`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `BetaCitationPageLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_page_number: number`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `BetaCitationContentBlockLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_block_index: number`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `BetaCitationWebSearchResultLocationParam`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string | null`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `BetaCitationSearchResultLocationParam`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string | null`

            - `type: "search_result_location"`

              - `"search_result_location"`

    - `temperature?: number`

      Body param: Amount of randomness injected into the response.

      Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.

      Note that even with `temperature` of `0.0`, the results will not be fully deterministic.

    - `thinking?: BetaThinkingConfigParam`

      Body param: Configuration for enabling Claude's extended thinking.

      When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

      See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

      - `BetaThinkingConfigEnabled`

        - `budget_tokens: number`

          Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

          Must be ≥1024 and less than `max_tokens`.

          See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

        - `type: "enabled"`

          - `"enabled"`

      - `BetaThinkingConfigDisabled`

        - `type: "disabled"`

          - `"disabled"`

    - `tool_choice?: BetaToolChoice`

      Body param: How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

      - `BetaToolChoiceAuto`

        The model will automatically decide whether to use tools.

        - `type: "auto"`

          - `"auto"`

        - `disable_parallel_tool_use?: boolean`

          Whether to disable parallel tool use.

          Defaults to `false`. If set to `true`, the model will output at most one tool use.

      - `BetaToolChoiceAny`

        The model will use any available tools.

        - `type: "any"`

          - `"any"`

        - `disable_parallel_tool_use?: boolean`

          Whether to disable parallel tool use.

          Defaults to `false`. If set to `true`, the model will output exactly one tool use.

      - `BetaToolChoiceTool`

        The model will use the specified tool with `tool_choice.name`.

        - `name: string`

          The name of the tool to use.

        - `type: "tool"`

          - `"tool"`

        - `disable_parallel_tool_use?: boolean`

          Whether to disable parallel tool use.

          Defaults to `false`. If set to `true`, the model will output exactly one tool use.

      - `BetaToolChoiceNone`

        The model will not be allowed to use tools.

        - `type: "none"`

          - `"none"`

    - `tools?: Array<BetaToolUnion>`

      Body param: Definitions of tools that the model may use.

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

      - `BetaTool`

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

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `description?: string`

          Description of what this tool does.

          Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

        - `input_examples?: Array<Record<string, unknown>>`

        - `strict?: boolean`

        - `type?: "custom" | null`

          - `"custom"`

      - `BetaToolBash20241022`

        - `name: "bash"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"bash"`

        - `type: "bash_20241022"`

          - `"bash_20241022"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples?: Array<Record<string, unknown>>`

        - `strict?: boolean`

      - `BetaToolBash20250124`

        - `name: "bash"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"bash"`

        - `type: "bash_20250124"`

          - `"bash_20250124"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples?: Array<Record<string, unknown>>`

        - `strict?: boolean`

      - `BetaCodeExecutionTool20250522`

        - `name: "code_execution"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"code_execution"`

        - `type: "code_execution_20250522"`

          - `"code_execution_20250522"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `strict?: boolean`

      - `BetaCodeExecutionTool20250825`

        - `name: "code_execution"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"code_execution"`

        - `type: "code_execution_20250825"`

          - `"code_execution_20250825"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `strict?: boolean`

      - `BetaToolComputerUse20241022`

        - `display_height_px: number`

          The height of the display in pixels.

        - `display_width_px: number`

          The width of the display in pixels.

        - `name: "computer"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"computer"`

        - `type: "computer_20241022"`

          - `"computer_20241022"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `display_number?: number | null`

          The X11 display number (e.g. 0, 1) for the display.

        - `input_examples?: Array<Record<string, unknown>>`

        - `strict?: boolean`

      - `BetaMemoryTool20250818`

        - `name: "memory"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"memory"`

        - `type: "memory_20250818"`

          - `"memory_20250818"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples?: Array<Record<string, unknown>>`

        - `strict?: boolean`

      - `BetaToolComputerUse20250124`

        - `display_height_px: number`

          The height of the display in pixels.

        - `display_width_px: number`

          The width of the display in pixels.

        - `name: "computer"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"computer"`

        - `type: "computer_20250124"`

          - `"computer_20250124"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `display_number?: number | null`

          The X11 display number (e.g. 0, 1) for the display.

        - `input_examples?: Array<Record<string, unknown>>`

        - `strict?: boolean`

      - `BetaToolTextEditor20241022`

        - `name: "str_replace_editor"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"str_replace_editor"`

        - `type: "text_editor_20241022"`

          - `"text_editor_20241022"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples?: Array<Record<string, unknown>>`

        - `strict?: boolean`

      - `BetaToolComputerUse20251124`

        - `display_height_px: number`

          The height of the display in pixels.

        - `display_width_px: number`

          The width of the display in pixels.

        - `name: "computer"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"computer"`

        - `type: "computer_20251124"`

          - `"computer_20251124"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `display_number?: number | null`

          The X11 display number (e.g. 0, 1) for the display.

        - `enable_zoom?: boolean`

          Whether to enable an action to take a zoomed-in screenshot of the screen.

        - `input_examples?: Array<Record<string, unknown>>`

        - `strict?: boolean`

      - `BetaToolTextEditor20250124`

        - `name: "str_replace_editor"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"str_replace_editor"`

        - `type: "text_editor_20250124"`

          - `"text_editor_20250124"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples?: Array<Record<string, unknown>>`

        - `strict?: boolean`

      - `BetaToolTextEditor20250429`

        - `name: "str_replace_based_edit_tool"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"str_replace_based_edit_tool"`

        - `type: "text_editor_20250429"`

          - `"text_editor_20250429"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples?: Array<Record<string, unknown>>`

        - `strict?: boolean`

      - `BetaToolTextEditor20250728`

        - `name: "str_replace_based_edit_tool"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"str_replace_based_edit_tool"`

        - `type: "text_editor_20250728"`

          - `"text_editor_20250728"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples?: Array<Record<string, unknown>>`

        - `max_characters?: number | null`

          Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

        - `strict?: boolean`

      - `BetaWebSearchTool20250305`

        - `name: "web_search"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"web_search"`

        - `type: "web_search_20250305"`

          - `"web_search_20250305"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `allowed_domains?: Array<string> | null`

          If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

        - `blocked_domains?: Array<string> | null`

          If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `max_uses?: number | null`

          Maximum number of times the tool can be used in the API request.

        - `strict?: boolean`

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

      - `BetaWebFetchTool20250910`

        - `name: "web_fetch"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"web_fetch"`

        - `type: "web_fetch_20250910"`

          - `"web_fetch_20250910"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `allowed_domains?: Array<string> | null`

          List of domains to allow fetching from

        - `blocked_domains?: Array<string> | null`

          List of domains to block fetching from

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `citations?: BetaCitationsConfigParam | null`

          Citations configuration for fetched documents. Citations are disabled by default.

          - `enabled?: boolean`

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `max_content_tokens?: number | null`

          Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

        - `max_uses?: number | null`

          Maximum number of times the tool can be used in the API request.

        - `strict?: boolean`

      - `BetaToolSearchToolBm25_20251119`

        - `name: "tool_search_tool_bm25"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"tool_search_tool_bm25"`

        - `type: "tool_search_tool_bm25_20251119" | "tool_search_tool_bm25"`

          - `"tool_search_tool_bm25_20251119"`

          - `"tool_search_tool_bm25"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `strict?: boolean`

      - `BetaToolSearchToolRegex20251119`

        - `name: "tool_search_tool_regex"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"tool_search_tool_regex"`

        - `type: "tool_search_tool_regex_20251119" | "tool_search_tool_regex"`

          - `"tool_search_tool_regex_20251119"`

          - `"tool_search_tool_regex"`

        - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

          - `"direct"`

          - `"code_execution_20250825"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `defer_loading?: boolean`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `strict?: boolean`

      - `BetaMCPToolset`

        Configuration for a group of tools from an MCP server.

        Allows configuring enabled status and defer_loading for all tools
        from an MCP server, with optional per-tool overrides.

        - `mcp_server_name: string`

          Name of the MCP server to configure tools for

        - `type: "mcp_toolset"`

          - `"mcp_toolset"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `configs?: Record<string, BetaMCPToolConfig> | null`

          Configuration overrides for specific tools, keyed by tool name

          - `defer_loading?: boolean`

          - `enabled?: boolean`

        - `default_config?: BetaMCPToolDefaultConfig`

          Default configuration applied to all tools from this server

          - `defer_loading?: boolean`

          - `enabled?: boolean`

    - `top_k?: number`

      Body param: Only sample from the top K options for each subsequent token.

      Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

      Recommended for advanced use cases only. You usually only need to use `temperature`.

    - `top_p?: number`

      Body param: Use nucleus sampling.

      In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

      Recommended for advanced use cases only. You usually only need to use `temperature`.

    - `betas?: Array<AnthropicBeta>`

      Header param: Optional header to specify the beta version(s) you want to use.

      - `(string & {})`

      - `"message-batches-2024-09-24" | "prompt-caching-2024-07-31" | "computer-use-2024-10-22" | 16 more`

        - `"message-batches-2024-09-24"`

        - `"prompt-caching-2024-07-31"`

        - `"computer-use-2024-10-22"`

        - `"computer-use-2025-01-24"`

        - `"pdfs-2024-09-25"`

        - `"token-counting-2024-11-01"`

        - `"token-efficient-tools-2025-02-19"`

        - `"output-128k-2025-02-19"`

        - `"files-api-2025-04-14"`

        - `"mcp-client-2025-04-04"`

        - `"mcp-client-2025-11-20"`

        - `"dev-full-thinking-2025-05-14"`

        - `"interleaved-thinking-2025-05-14"`

        - `"code-execution-2025-05-22"`

        - `"extended-cache-ttl-2025-04-11"`

        - `"context-1m-2025-08-07"`

        - `"context-management-2025-06-27"`

        - `"model-context-window-exceeded-2025-08-26"`

        - `"skills-2025-10-02"`

  - `MessageCreateParamsNonStreaming extends MessageCreateParamsBase`

    - `stream?: false`

      Body param: Whether to incrementally stream the response using server-sent events.

      See [streaming](https://docs.claude.com/en/api/messages-streaming) for details.

      - `false`

  - `MessageCreateParamsNonStreaming extends MessageCreateParamsBase`

    - `stream?: false`

      Body param: Whether to incrementally stream the response using server-sent events.

      See [streaming](https://docs.claude.com/en/api/messages-streaming) for details.

      - `false`

### Returns

- `BetaMessage`

  - `id: string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `container: BetaContainer | null`

    Information about the container used in the request (for the code execution tool)

    - `id: string`

      Identifier for the container used in this request

    - `expires_at: string`

      The time at which the container will expire.

    - `skills: Array<BetaSkill> | null`

      Skills loaded in the container

      - `skill_id: string`

        Skill ID

      - `type: "anthropic" | "custom"`

        Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

        - `"anthropic"`

        - `"custom"`

      - `version: string`

        Skill version or 'latest' for most recent version

  - `content: Array<BetaContentBlock>`

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

    - `BetaTextBlock`

      - `citations: Array<BetaTextCitation> | null`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `BetaCitationCharLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_char_index: number`

          - `file_id: string | null`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `BetaCitationPageLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_page_number: number`

          - `file_id: string | null`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `BetaCitationContentBlockLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_block_index: number`

          - `file_id: string | null`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `BetaCitationsWebSearchResultLocation`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string | null`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `BetaCitationSearchResultLocation`

          - `cited_text: string`

          - `end_block_index: number`

          - `search_result_index: number`

          - `source: string`

          - `start_block_index: number`

          - `title: string | null`

          - `type: "search_result_location"`

            - `"search_result_location"`

      - `text: string`

      - `type: "text"`

        - `"text"`

    - `BetaThinkingBlock`

      - `signature: string`

      - `thinking: string`

      - `type: "thinking"`

        - `"thinking"`

    - `BetaRedactedThinkingBlock`

      - `data: string`

      - `type: "redacted_thinking"`

        - `"redacted_thinking"`

    - `BetaToolUseBlock`

      - `id: string`

      - `input: Record<string, unknown>`

      - `name: string`

      - `type: "tool_use"`

        - `"tool_use"`

      - `caller?: BetaDirectCaller | BetaServerToolCaller`

        Tool invocation directly from the model.

        - `BetaDirectCaller`

          Tool invocation directly from the model.

          - `type: "direct"`

            - `"direct"`

        - `BetaServerToolCaller`

          Tool invocation generated by a server-side tool.

          - `tool_id: string`

          - `type: "code_execution_20250825"`

            - `"code_execution_20250825"`

    - `BetaServerToolUseBlock`

      - `id: string`

      - `caller: BetaDirectCaller | BetaServerToolCaller`

        Tool invocation directly from the model.

        - `BetaDirectCaller`

          Tool invocation directly from the model.

          - `type: "direct"`

            - `"direct"`

        - `BetaServerToolCaller`

          Tool invocation generated by a server-side tool.

          - `tool_id: string`

          - `type: "code_execution_20250825"`

            - `"code_execution_20250825"`

      - `input: Record<string, unknown>`

      - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

        - `"web_search"`

        - `"web_fetch"`

        - `"code_execution"`

        - `"bash_code_execution"`

        - `"text_editor_code_execution"`

        - `"tool_search_tool_regex"`

        - `"tool_search_tool_bm25"`

      - `type: "server_tool_use"`

        - `"server_tool_use"`

    - `BetaWebSearchToolResultBlock`

      - `content: BetaWebSearchToolResultBlockContent`

        - `BetaWebSearchToolResultError`

          - `error_code: BetaWebSearchToolResultErrorCode`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"max_uses_exceeded"`

            - `"too_many_requests"`

            - `"query_too_long"`

          - `type: "web_search_tool_result_error"`

            - `"web_search_tool_result_error"`

        - `Array<BetaWebSearchResultBlock>`

          - `encrypted_content: string`

          - `page_age: string | null`

          - `title: string`

          - `type: "web_search_result"`

            - `"web_search_result"`

          - `url: string`

      - `tool_use_id: string`

      - `type: "web_search_tool_result"`

        - `"web_search_tool_result"`

    - `BetaWebFetchToolResultBlock`

      - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

        - `BetaWebFetchToolResultErrorBlock`

          - `error_code: BetaWebFetchToolResultErrorCode`

            - `"invalid_tool_input"`

            - `"url_too_long"`

            - `"url_not_allowed"`

            - `"url_not_accessible"`

            - `"unsupported_content_type"`

            - `"too_many_requests"`

            - `"max_uses_exceeded"`

            - `"unavailable"`

          - `type: "web_fetch_tool_result_error"`

            - `"web_fetch_tool_result_error"`

        - `BetaWebFetchBlock`

          - `content: BetaDocumentBlock`

            - `citations: BetaCitationConfig | null`

              Citation configuration for the document

              - `enabled: boolean`

            - `source: BetaBase64PDFSource | BetaPlainTextSource`

              - `BetaBase64PDFSource`

                - `data: string`

                - `media_type: "application/pdf"`

                  - `"application/pdf"`

                - `type: "base64"`

                  - `"base64"`

              - `BetaPlainTextSource`

                - `data: string`

                - `media_type: "text/plain"`

                  - `"text/plain"`

                - `type: "text"`

                  - `"text"`

            - `title: string | null`

              The title of the document

            - `type: "document"`

              - `"document"`

          - `retrieved_at: string | null`

            ISO 8601 timestamp when the content was retrieved

          - `type: "web_fetch_result"`

            - `"web_fetch_result"`

          - `url: string`

            Fetched content URL

      - `tool_use_id: string`

      - `type: "web_fetch_tool_result"`

        - `"web_fetch_tool_result"`

    - `BetaCodeExecutionToolResultBlock`

      - `content: BetaCodeExecutionToolResultBlockContent`

        - `BetaCodeExecutionToolResultError`

          - `error_code: BetaCodeExecutionToolResultErrorCode`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

          - `type: "code_execution_tool_result_error"`

            - `"code_execution_tool_result_error"`

        - `BetaCodeExecutionResultBlock`

          - `content: Array<BetaCodeExecutionOutputBlock>`

            - `file_id: string`

            - `type: "code_execution_output"`

              - `"code_execution_output"`

          - `return_code: number`

          - `stderr: string`

          - `stdout: string`

          - `type: "code_execution_result"`

            - `"code_execution_result"`

      - `tool_use_id: string`

      - `type: "code_execution_tool_result"`

        - `"code_execution_tool_result"`

    - `BetaBashCodeExecutionToolResultBlock`

      - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

        - `BetaBashCodeExecutionToolResultError`

          - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

            - `"output_file_too_large"`

          - `type: "bash_code_execution_tool_result_error"`

            - `"bash_code_execution_tool_result_error"`

        - `BetaBashCodeExecutionResultBlock`

          - `content: Array<BetaBashCodeExecutionOutputBlock>`

            - `file_id: string`

            - `type: "bash_code_execution_output"`

              - `"bash_code_execution_output"`

          - `return_code: number`

          - `stderr: string`

          - `stdout: string`

          - `type: "bash_code_execution_result"`

            - `"bash_code_execution_result"`

      - `tool_use_id: string`

      - `type: "bash_code_execution_tool_result"`

        - `"bash_code_execution_tool_result"`

    - `BetaTextEditorCodeExecutionToolResultBlock`

      - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

        - `BetaTextEditorCodeExecutionToolResultError`

          - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

            - `"file_not_found"`

          - `error_message: string | null`

          - `type: "text_editor_code_execution_tool_result_error"`

            - `"text_editor_code_execution_tool_result_error"`

        - `BetaTextEditorCodeExecutionViewResultBlock`

          - `content: string`

          - `file_type: "text" | "image" | "pdf"`

            - `"text"`

            - `"image"`

            - `"pdf"`

          - `num_lines: number | null`

          - `start_line: number | null`

          - `total_lines: number | null`

          - `type: "text_editor_code_execution_view_result"`

            - `"text_editor_code_execution_view_result"`

        - `BetaTextEditorCodeExecutionCreateResultBlock`

          - `is_file_update: boolean`

          - `type: "text_editor_code_execution_create_result"`

            - `"text_editor_code_execution_create_result"`

        - `BetaTextEditorCodeExecutionStrReplaceResultBlock`

          - `lines: Array<string> | null`

          - `new_lines: number | null`

          - `new_start: number | null`

          - `old_lines: number | null`

          - `old_start: number | null`

          - `type: "text_editor_code_execution_str_replace_result"`

            - `"text_editor_code_execution_str_replace_result"`

      - `tool_use_id: string`

      - `type: "text_editor_code_execution_tool_result"`

        - `"text_editor_code_execution_tool_result"`

    - `BetaToolSearchToolResultBlock`

      - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

        - `BetaToolSearchToolResultError`

          - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

          - `error_message: string | null`

          - `type: "tool_search_tool_result_error"`

            - `"tool_search_tool_result_error"`

        - `BetaToolSearchToolSearchResultBlock`

          - `tool_references: Array<BetaToolReferenceBlock>`

            - `tool_name: string`

            - `type: "tool_reference"`

              - `"tool_reference"`

          - `type: "tool_search_tool_search_result"`

            - `"tool_search_tool_search_result"`

      - `tool_use_id: string`

      - `type: "tool_search_tool_result"`

        - `"tool_search_tool_result"`

    - `BetaMCPToolUseBlock`

      - `id: string`

      - `input: Record<string, unknown>`

      - `name: string`

        The name of the MCP tool

      - `server_name: string`

        The name of the MCP server

      - `type: "mcp_tool_use"`

        - `"mcp_tool_use"`

    - `BetaMCPToolResultBlock`

      - `content: string | Array<BetaTextBlock>`

        - `string`

        - `Array<BetaTextBlock>`

          - `citations: Array<BetaTextCitation> | null`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `BetaCitationCharLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_char_index: number`

              - `file_id: string | null`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `BetaCitationPageLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_page_number: number`

              - `file_id: string | null`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `BetaCitationContentBlockLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_block_index: number`

              - `file_id: string | null`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `BetaCitationsWebSearchResultLocation`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string | null`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `BetaCitationSearchResultLocation`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string | null`

              - `type: "search_result_location"`

                - `"search_result_location"`

          - `text: string`

          - `type: "text"`

            - `"text"`

      - `is_error: boolean`

      - `tool_use_id: string`

      - `type: "mcp_tool_result"`

        - `"mcp_tool_result"`

    - `BetaContainerUploadBlock`

      Response model for a file uploaded to the container.

      - `file_id: string`

      - `type: "container_upload"`

        - `"container_upload"`

  - `context_management: BetaContextManagementResponse | null`

    Context management response.

    Information about context management strategies applied during the request.

    - `applied_edits: Array<BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse>`

      List of context management edits that were applied.

      - `BetaClearToolUses20250919EditResponse`

        - `cleared_input_tokens: number`

          Number of input tokens cleared by this edit.

        - `cleared_tool_uses: number`

          Number of tool uses that were cleared.

        - `type: "clear_tool_uses_20250919"`

          The type of context management edit applied.

          - `"clear_tool_uses_20250919"`

      - `BetaClearThinking20251015EditResponse`

        - `cleared_input_tokens: number`

          Number of input tokens cleared by this edit.

        - `cleared_thinking_turns: number`

          Number of thinking turns that were cleared.

        - `type: "clear_thinking_20251015"`

          The type of context management edit applied.

          - `"clear_thinking_20251015"`

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

  - `role: "assistant"`

    Conversational role of the generated message.

    This will always be `"assistant"`.

    - `"assistant"`

  - `stop_reason: BetaStopReason | null`

    The reason that we stopped.

    This may be one the following values:

    * `"end_turn"`: the model reached a natural stopping point
    * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
    * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
    * `"tool_use"`: the model invoked one or more tools
    * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
    * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

    In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

    - `"end_turn"`

    - `"max_tokens"`

    - `"stop_sequence"`

    - `"tool_use"`

    - `"pause_turn"`

    - `"refusal"`

    - `"model_context_window_exceeded"`

  - `stop_sequence: string | null`

    Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was generated.

  - `type: "message"`

    Object type.

    For Messages, this is always `"message"`.

    - `"message"`

  - `usage: BetaUsage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cache_creation: BetaCacheCreation | null`

      Breakdown of cached tokens by TTL

      - `ephemeral_1h_input_tokens: number`

        The number of input tokens used to create the 1 hour cache entry.

      - `ephemeral_5m_input_tokens: number`

        The number of input tokens used to create the 5 minute cache entry.

    - `cache_creation_input_tokens: number | null`

      The number of input tokens used to create the cache entry.

    - `cache_read_input_tokens: number | null`

      The number of input tokens read from the cache.

    - `input_tokens: number`

      The number of input tokens which were used.

    - `output_tokens: number`

      The number of output tokens which were used.

    - `server_tool_use: BetaServerToolUsage | null`

      The number of server tool requests.

      - `web_fetch_requests: number`

        The number of web fetch tool requests.

      - `web_search_requests: number`

        The number of web search tool requests.

    - `service_tier: "standard" | "priority" | "batch" | null`

      If the request used the priority, standard, or batch tier.

      - `"standard"`

      - `"priority"`

      - `"batch"`

### Example

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: 'my-anthropic-api-key',
});

const betaMessage = await client.beta.messages.create({
  max_tokens: 1024,
  messages: [{ content: 'Hello, world', role: 'user' }],
  model: 'claude-sonnet-4-5-20250929',
});

console.log(betaMessage.id);
```

## Count Tokens

`client.beta.messages.countTokens(MessageCountTokensParamsparams, RequestOptionsoptions?): BetaMessageTokensCount`

**post** `/v1/messages/count_tokens`

Count the number of tokens in a Message.

The Token Count API can be used to count the number of tokens in a Message, including tools, images, and documents, without creating it.

Learn more about token counting in our [user guide](https://docs.claude.com/en/docs/build-with-claude/token-counting)

### Parameters

- `params: MessageCountTokensParams`

  - `messages: Array<BetaMessageParam>`

    Body param: Input messages.

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

    - `content: string | Array<BetaContentBlockParam>`

      - `string`

      - `Array<BetaContentBlockParam>`

        - `BetaTextBlockParam`

          - `text: string`

          - `type: "text"`

            - `"text"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `citations?: Array<BetaTextCitationParam> | null`

            - `BetaCitationCharLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_char_index: number`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `BetaCitationPageLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_page_number: number`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `BetaCitationContentBlockLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_block_index: number`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `BetaCitationWebSearchResultLocationParam`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string | null`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `BetaCitationSearchResultLocationParam`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string | null`

              - `type: "search_result_location"`

                - `"search_result_location"`

        - `BetaImageBlockParam`

          - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

            - `BetaBase64ImageSource`

              - `data: string`

              - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                - `"image/jpeg"`

                - `"image/png"`

                - `"image/gif"`

                - `"image/webp"`

              - `type: "base64"`

                - `"base64"`

            - `BetaURLImageSource`

              - `type: "url"`

                - `"url"`

              - `url: string`

            - `BetaFileImageSource`

              - `file_id: string`

              - `type: "file"`

                - `"file"`

          - `type: "image"`

            - `"image"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `BetaRequestDocumentBlock`

          - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

            - `BetaBase64PDFSource`

              - `data: string`

              - `media_type: "application/pdf"`

                - `"application/pdf"`

              - `type: "base64"`

                - `"base64"`

            - `BetaPlainTextSource`

              - `data: string`

              - `media_type: "text/plain"`

                - `"text/plain"`

              - `type: "text"`

                - `"text"`

            - `BetaContentBlockSource`

              - `content: string | Array<BetaContentBlockSourceContent>`

                - `string`

                - `Array<BetaContentBlockSourceContent>`

                  - `BetaTextBlockParam`

                    - `text: string`

                    - `type: "text"`

                      - `"text"`

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

                    - `citations?: Array<BetaTextCitationParam> | null`

                      - `BetaCitationCharLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_char_index: number`

                        - `start_char_index: number`

                        - `type: "char_location"`

                          - `"char_location"`

                      - `BetaCitationPageLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_page_number: number`

                        - `start_page_number: number`

                        - `type: "page_location"`

                          - `"page_location"`

                      - `BetaCitationContentBlockLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_block_index: number`

                        - `start_block_index: number`

                        - `type: "content_block_location"`

                          - `"content_block_location"`

                      - `BetaCitationWebSearchResultLocationParam`

                        - `cited_text: string`

                        - `encrypted_index: string`

                        - `title: string | null`

                        - `type: "web_search_result_location"`

                          - `"web_search_result_location"`

                        - `url: string`

                      - `BetaCitationSearchResultLocationParam`

                        - `cited_text: string`

                        - `end_block_index: number`

                        - `search_result_index: number`

                        - `source: string`

                        - `start_block_index: number`

                        - `title: string | null`

                        - `type: "search_result_location"`

                          - `"search_result_location"`

                  - `BetaImageBlockParam`

                    - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                      - `BetaBase64ImageSource`

                        - `data: string`

                        - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                          - `"image/jpeg"`

                          - `"image/png"`

                          - `"image/gif"`

                          - `"image/webp"`

                        - `type: "base64"`

                          - `"base64"`

                      - `BetaURLImageSource`

                        - `type: "url"`

                          - `"url"`

                        - `url: string`

                      - `BetaFileImageSource`

                        - `file_id: string`

                        - `type: "file"`

                          - `"file"`

                    - `type: "image"`

                      - `"image"`

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `BetaURLPDFSource`

              - `type: "url"`

                - `"url"`

              - `url: string`

            - `BetaFileDocumentSource`

              - `file_id: string`

              - `type: "file"`

                - `"file"`

          - `type: "document"`

            - `"document"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `citations?: BetaCitationsConfigParam | null`

            - `enabled?: boolean`

          - `context?: string | null`

          - `title?: string | null`

        - `BetaSearchResultBlockParam`

          - `content: Array<BetaTextBlockParam>`

            - `text: string`

            - `type: "text"`

              - `"text"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `citations?: Array<BetaTextCitationParam> | null`

              - `BetaCitationCharLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_char_index: number`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `BetaCitationPageLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_page_number: number`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `BetaCitationContentBlockLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_block_index: number`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `BetaCitationWebSearchResultLocationParam`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string | null`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `BetaCitationSearchResultLocationParam`

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

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `citations?: BetaCitationsConfigParam`

            - `enabled?: boolean`

        - `BetaThinkingBlockParam`

          - `signature: string`

          - `thinking: string`

          - `type: "thinking"`

            - `"thinking"`

        - `BetaRedactedThinkingBlockParam`

          - `data: string`

          - `type: "redacted_thinking"`

            - `"redacted_thinking"`

        - `BetaToolUseBlockParam`

          - `id: string`

          - `input: Record<string, unknown>`

          - `name: string`

          - `type: "tool_use"`

            - `"tool_use"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `caller?: BetaDirectCaller | BetaServerToolCaller`

            Tool invocation directly from the model.

            - `BetaDirectCaller`

              Tool invocation directly from the model.

              - `type: "direct"`

                - `"direct"`

            - `BetaServerToolCaller`

              Tool invocation generated by a server-side tool.

              - `tool_id: string`

              - `type: "code_execution_20250825"`

                - `"code_execution_20250825"`

        - `BetaToolResultBlockParam`

          - `tool_use_id: string`

          - `type: "tool_result"`

            - `"tool_result"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `content?: string | Array<BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more>`

            - `string`

            - `Array<BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more>`

              - `BetaTextBlockParam`

                - `text: string`

                - `type: "text"`

                  - `"text"`

                - `cache_control?: BetaCacheControlEphemeral | null`

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

                - `citations?: Array<BetaTextCitationParam> | null`

                  - `BetaCitationCharLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_char_index: number`

                    - `start_char_index: number`

                    - `type: "char_location"`

                      - `"char_location"`

                  - `BetaCitationPageLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_page_number: number`

                    - `start_page_number: number`

                    - `type: "page_location"`

                      - `"page_location"`

                  - `BetaCitationContentBlockLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_block_index: number`

                    - `start_block_index: number`

                    - `type: "content_block_location"`

                      - `"content_block_location"`

                  - `BetaCitationWebSearchResultLocationParam`

                    - `cited_text: string`

                    - `encrypted_index: string`

                    - `title: string | null`

                    - `type: "web_search_result_location"`

                      - `"web_search_result_location"`

                    - `url: string`

                  - `BetaCitationSearchResultLocationParam`

                    - `cited_text: string`

                    - `end_block_index: number`

                    - `search_result_index: number`

                    - `source: string`

                    - `start_block_index: number`

                    - `title: string | null`

                    - `type: "search_result_location"`

                      - `"search_result_location"`

              - `BetaImageBlockParam`

                - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                  - `BetaBase64ImageSource`

                    - `data: string`

                    - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                      - `"image/jpeg"`

                      - `"image/png"`

                      - `"image/gif"`

                      - `"image/webp"`

                    - `type: "base64"`

                      - `"base64"`

                  - `BetaURLImageSource`

                    - `type: "url"`

                      - `"url"`

                    - `url: string`

                  - `BetaFileImageSource`

                    - `file_id: string`

                    - `type: "file"`

                      - `"file"`

                - `type: "image"`

                  - `"image"`

                - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `BetaSearchResultBlockParam`

                - `content: Array<BetaTextBlockParam>`

                  - `text: string`

                  - `type: "text"`

                    - `"text"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

                  - `citations?: Array<BetaTextCitationParam> | null`

                    - `BetaCitationCharLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_char_index: number`

                      - `start_char_index: number`

                      - `type: "char_location"`

                        - `"char_location"`

                    - `BetaCitationPageLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_page_number: number`

                      - `start_page_number: number`

                      - `type: "page_location"`

                        - `"page_location"`

                    - `BetaCitationContentBlockLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_block_index: number`

                      - `start_block_index: number`

                      - `type: "content_block_location"`

                        - `"content_block_location"`

                    - `BetaCitationWebSearchResultLocationParam`

                      - `cited_text: string`

                      - `encrypted_index: string`

                      - `title: string | null`

                      - `type: "web_search_result_location"`

                        - `"web_search_result_location"`

                      - `url: string`

                    - `BetaCitationSearchResultLocationParam`

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

                - `cache_control?: BetaCacheControlEphemeral | null`

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

                - `citations?: BetaCitationsConfigParam`

                  - `enabled?: boolean`

              - `BetaRequestDocumentBlock`

                - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

                  - `BetaBase64PDFSource`

                    - `data: string`

                    - `media_type: "application/pdf"`

                      - `"application/pdf"`

                    - `type: "base64"`

                      - `"base64"`

                  - `BetaPlainTextSource`

                    - `data: string`

                    - `media_type: "text/plain"`

                      - `"text/plain"`

                    - `type: "text"`

                      - `"text"`

                  - `BetaContentBlockSource`

                    - `content: string | Array<BetaContentBlockSourceContent>`

                      - `string`

                      - `Array<BetaContentBlockSourceContent>`

                        - `BetaTextBlockParam`

                          - `text: string`

                          - `type: "text"`

                            - `"text"`

                          - `cache_control?: BetaCacheControlEphemeral | null`

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

                          - `citations?: Array<BetaTextCitationParam> | null`

                            - `BetaCitationCharLocationParam`

                              - `cited_text: string`

                              - `document_index: number`

                              - `document_title: string | null`

                              - `end_char_index: number`

                              - `start_char_index: number`

                              - `type: "char_location"`

                                - `"char_location"`

                            - `BetaCitationPageLocationParam`

                              - `cited_text: string`

                              - `document_index: number`

                              - `document_title: string | null`

                              - `end_page_number: number`

                              - `start_page_number: number`

                              - `type: "page_location"`

                                - `"page_location"`

                            - `BetaCitationContentBlockLocationParam`

                              - `cited_text: string`

                              - `document_index: number`

                              - `document_title: string | null`

                              - `end_block_index: number`

                              - `start_block_index: number`

                              - `type: "content_block_location"`

                                - `"content_block_location"`

                            - `BetaCitationWebSearchResultLocationParam`

                              - `cited_text: string`

                              - `encrypted_index: string`

                              - `title: string | null`

                              - `type: "web_search_result_location"`

                                - `"web_search_result_location"`

                              - `url: string`

                            - `BetaCitationSearchResultLocationParam`

                              - `cited_text: string`

                              - `end_block_index: number`

                              - `search_result_index: number`

                              - `source: string`

                              - `start_block_index: number`

                              - `title: string | null`

                              - `type: "search_result_location"`

                                - `"search_result_location"`

                        - `BetaImageBlockParam`

                          - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                            - `BetaBase64ImageSource`

                              - `data: string`

                              - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                                - `"image/jpeg"`

                                - `"image/png"`

                                - `"image/gif"`

                                - `"image/webp"`

                              - `type: "base64"`

                                - `"base64"`

                            - `BetaURLImageSource`

                              - `type: "url"`

                                - `"url"`

                              - `url: string`

                            - `BetaFileImageSource`

                              - `file_id: string`

                              - `type: "file"`

                                - `"file"`

                          - `type: "image"`

                            - `"image"`

                          - `cache_control?: BetaCacheControlEphemeral | null`

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

                  - `BetaURLPDFSource`

                    - `type: "url"`

                      - `"url"`

                    - `url: string`

                  - `BetaFileDocumentSource`

                    - `file_id: string`

                    - `type: "file"`

                      - `"file"`

                - `type: "document"`

                  - `"document"`

                - `cache_control?: BetaCacheControlEphemeral | null`

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

                - `citations?: BetaCitationsConfigParam | null`

                  - `enabled?: boolean`

                - `context?: string | null`

                - `title?: string | null`

              - `BetaToolReferenceBlockParam`

                Tool reference block that can be included in tool_result content.

                - `tool_name: string`

                - `type: "tool_reference"`

                  - `"tool_reference"`

                - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `is_error?: boolean`

        - `BetaServerToolUseBlockParam`

          - `id: string`

          - `input: Record<string, unknown>`

          - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

            - `"web_search"`

            - `"web_fetch"`

            - `"code_execution"`

            - `"bash_code_execution"`

            - `"text_editor_code_execution"`

            - `"tool_search_tool_regex"`

            - `"tool_search_tool_bm25"`

          - `type: "server_tool_use"`

            - `"server_tool_use"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `caller?: BetaDirectCaller | BetaServerToolCaller`

            Tool invocation directly from the model.

            - `BetaDirectCaller`

              Tool invocation directly from the model.

              - `type: "direct"`

                - `"direct"`

            - `BetaServerToolCaller`

              Tool invocation generated by a server-side tool.

              - `tool_id: string`

              - `type: "code_execution_20250825"`

                - `"code_execution_20250825"`

        - `BetaWebSearchToolResultBlockParam`

          - `content: BetaWebSearchToolResultBlockParamContent`

            - `Array<BetaWebSearchResultBlockParam>`

              - `encrypted_content: string`

              - `title: string`

              - `type: "web_search_result"`

                - `"web_search_result"`

              - `url: string`

              - `page_age?: string | null`

            - `BetaWebSearchToolRequestError`

              - `error_code: BetaWebSearchToolResultErrorCode`

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

          - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `BetaWebFetchToolResultBlockParam`

          - `content: BetaWebFetchToolResultErrorBlockParam | BetaWebFetchBlockParam`

            - `BetaWebFetchToolResultErrorBlockParam`

              - `error_code: BetaWebFetchToolResultErrorCode`

                - `"invalid_tool_input"`

                - `"url_too_long"`

                - `"url_not_allowed"`

                - `"url_not_accessible"`

                - `"unsupported_content_type"`

                - `"too_many_requests"`

                - `"max_uses_exceeded"`

                - `"unavailable"`

              - `type: "web_fetch_tool_result_error"`

                - `"web_fetch_tool_result_error"`

            - `BetaWebFetchBlockParam`

              - `content: BetaRequestDocumentBlock`

                - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

                  - `BetaBase64PDFSource`

                    - `data: string`

                    - `media_type: "application/pdf"`

                      - `"application/pdf"`

                    - `type: "base64"`

                      - `"base64"`

                  - `BetaPlainTextSource`

                    - `data: string`

                    - `media_type: "text/plain"`

                      - `"text/plain"`

                    - `type: "text"`

                      - `"text"`

                  - `BetaContentBlockSource`

                    - `content: string | Array<BetaContentBlockSourceContent>`

                      - `string`

                      - `Array<BetaContentBlockSourceContent>`

                        - `BetaTextBlockParam`

                          - `text: string`

                          - `type: "text"`

                            - `"text"`

                          - `cache_control?: BetaCacheControlEphemeral | null`

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

                          - `citations?: Array<BetaTextCitationParam> | null`

                            - `BetaCitationCharLocationParam`

                              - `cited_text: string`

                              - `document_index: number`

                              - `document_title: string | null`

                              - `end_char_index: number`

                              - `start_char_index: number`

                              - `type: "char_location"`

                                - `"char_location"`

                            - `BetaCitationPageLocationParam`

                              - `cited_text: string`

                              - `document_index: number`

                              - `document_title: string | null`

                              - `end_page_number: number`

                              - `start_page_number: number`

                              - `type: "page_location"`

                                - `"page_location"`

                            - `BetaCitationContentBlockLocationParam`

                              - `cited_text: string`

                              - `document_index: number`

                              - `document_title: string | null`

                              - `end_block_index: number`

                              - `start_block_index: number`

                              - `type: "content_block_location"`

                                - `"content_block_location"`

                            - `BetaCitationWebSearchResultLocationParam`

                              - `cited_text: string`

                              - `encrypted_index: string`

                              - `title: string | null`

                              - `type: "web_search_result_location"`

                                - `"web_search_result_location"`

                              - `url: string`

                            - `BetaCitationSearchResultLocationParam`

                              - `cited_text: string`

                              - `end_block_index: number`

                              - `search_result_index: number`

                              - `source: string`

                              - `start_block_index: number`

                              - `title: string | null`

                              - `type: "search_result_location"`

                                - `"search_result_location"`

                        - `BetaImageBlockParam`

                          - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                            - `BetaBase64ImageSource`

                              - `data: string`

                              - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                                - `"image/jpeg"`

                                - `"image/png"`

                                - `"image/gif"`

                                - `"image/webp"`

                              - `type: "base64"`

                                - `"base64"`

                            - `BetaURLImageSource`

                              - `type: "url"`

                                - `"url"`

                              - `url: string`

                            - `BetaFileImageSource`

                              - `file_id: string`

                              - `type: "file"`

                                - `"file"`

                          - `type: "image"`

                            - `"image"`

                          - `cache_control?: BetaCacheControlEphemeral | null`

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

                  - `BetaURLPDFSource`

                    - `type: "url"`

                      - `"url"`

                    - `url: string`

                  - `BetaFileDocumentSource`

                    - `file_id: string`

                    - `type: "file"`

                      - `"file"`

                - `type: "document"`

                  - `"document"`

                - `cache_control?: BetaCacheControlEphemeral | null`

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

                - `citations?: BetaCitationsConfigParam | null`

                  - `enabled?: boolean`

                - `context?: string | null`

                - `title?: string | null`

              - `type: "web_fetch_result"`

                - `"web_fetch_result"`

              - `url: string`

                Fetched content URL

              - `retrieved_at?: string | null`

                ISO 8601 timestamp when the content was retrieved

          - `tool_use_id: string`

          - `type: "web_fetch_tool_result"`

            - `"web_fetch_tool_result"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `BetaCodeExecutionToolResultBlockParam`

          - `content: BetaCodeExecutionToolResultBlockParamContent`

            - `BetaCodeExecutionToolResultErrorParam`

              - `error_code: BetaCodeExecutionToolResultErrorCode`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"too_many_requests"`

                - `"execution_time_exceeded"`

              - `type: "code_execution_tool_result_error"`

                - `"code_execution_tool_result_error"`

            - `BetaCodeExecutionResultBlockParam`

              - `content: Array<BetaCodeExecutionOutputBlockParam>`

                - `file_id: string`

                - `type: "code_execution_output"`

                  - `"code_execution_output"`

              - `return_code: number`

              - `stderr: string`

              - `stdout: string`

              - `type: "code_execution_result"`

                - `"code_execution_result"`

          - `tool_use_id: string`

          - `type: "code_execution_tool_result"`

            - `"code_execution_tool_result"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `BetaBashCodeExecutionToolResultBlockParam`

          - `content: BetaBashCodeExecutionToolResultErrorParam | BetaBashCodeExecutionResultBlockParam`

            - `BetaBashCodeExecutionToolResultErrorParam`

              - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"too_many_requests"`

                - `"execution_time_exceeded"`

                - `"output_file_too_large"`

              - `type: "bash_code_execution_tool_result_error"`

                - `"bash_code_execution_tool_result_error"`

            - `BetaBashCodeExecutionResultBlockParam`

              - `content: Array<BetaBashCodeExecutionOutputBlockParam>`

                - `file_id: string`

                - `type: "bash_code_execution_output"`

                  - `"bash_code_execution_output"`

              - `return_code: number`

              - `stderr: string`

              - `stdout: string`

              - `type: "bash_code_execution_result"`

                - `"bash_code_execution_result"`

          - `tool_use_id: string`

          - `type: "bash_code_execution_tool_result"`

            - `"bash_code_execution_tool_result"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `BetaTextEditorCodeExecutionToolResultBlockParam`

          - `content: BetaTextEditorCodeExecutionToolResultErrorParam | BetaTextEditorCodeExecutionViewResultBlockParam | BetaTextEditorCodeExecutionCreateResultBlockParam | BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

            - `BetaTextEditorCodeExecutionToolResultErrorParam`

              - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"too_many_requests"`

                - `"execution_time_exceeded"`

                - `"file_not_found"`

              - `type: "text_editor_code_execution_tool_result_error"`

                - `"text_editor_code_execution_tool_result_error"`

              - `error_message?: string | null`

            - `BetaTextEditorCodeExecutionViewResultBlockParam`

              - `content: string`

              - `file_type: "text" | "image" | "pdf"`

                - `"text"`

                - `"image"`

                - `"pdf"`

              - `type: "text_editor_code_execution_view_result"`

                - `"text_editor_code_execution_view_result"`

              - `num_lines?: number | null`

              - `start_line?: number | null`

              - `total_lines?: number | null`

            - `BetaTextEditorCodeExecutionCreateResultBlockParam`

              - `is_file_update: boolean`

              - `type: "text_editor_code_execution_create_result"`

                - `"text_editor_code_execution_create_result"`

            - `BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

              - `type: "text_editor_code_execution_str_replace_result"`

                - `"text_editor_code_execution_str_replace_result"`

              - `lines?: Array<string> | null`

              - `new_lines?: number | null`

              - `new_start?: number | null`

              - `old_lines?: number | null`

              - `old_start?: number | null`

          - `tool_use_id: string`

          - `type: "text_editor_code_execution_tool_result"`

            - `"text_editor_code_execution_tool_result"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `BetaToolSearchToolResultBlockParam`

          - `content: BetaToolSearchToolResultErrorParam | BetaToolSearchToolSearchResultBlockParam`

            - `BetaToolSearchToolResultErrorParam`

              - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"too_many_requests"`

                - `"execution_time_exceeded"`

              - `type: "tool_search_tool_result_error"`

                - `"tool_search_tool_result_error"`

            - `BetaToolSearchToolSearchResultBlockParam`

              - `tool_references: Array<BetaToolReferenceBlockParam>`

                - `tool_name: string`

                - `type: "tool_reference"`

                  - `"tool_reference"`

                - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `type: "tool_search_tool_search_result"`

                - `"tool_search_tool_search_result"`

          - `tool_use_id: string`

          - `type: "tool_search_tool_result"`

            - `"tool_search_tool_result"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `BetaMCPToolUseBlockParam`

          - `id: string`

          - `input: Record<string, unknown>`

          - `name: string`

          - `server_name: string`

            The name of the MCP server

          - `type: "mcp_tool_use"`

            - `"mcp_tool_use"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `BetaRequestMCPToolResultBlockParam`

          - `tool_use_id: string`

          - `type: "mcp_tool_result"`

            - `"mcp_tool_result"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `content?: string | Array<BetaTextBlockParam>`

            - `string`

            - `Array<BetaTextBlockParam>`

              - `text: string`

              - `type: "text"`

                - `"text"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `citations?: Array<BetaTextCitationParam> | null`

                - `BetaCitationCharLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_char_index: number`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `BetaCitationPageLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_page_number: number`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `BetaCitationContentBlockLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_block_index: number`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `BetaCitationWebSearchResultLocationParam`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string | null`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `BetaCitationSearchResultLocationParam`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string | null`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

          - `is_error?: boolean`

        - `BetaContainerUploadBlockParam`

          A content block that represents a file to be uploaded to the container
          Files uploaded via this block will be available in the container's input directory.

          - `file_id: string`

          - `type: "container_upload"`

            - `"container_upload"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

    Body param: The model that will complete your prompt.

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

  - `context_management?: BetaContextManagementConfig | null`

    Body param: Context management configuration.

    This allows you to control how Claude manages context across multiple requests, such as whether to clear function results or not.

    - `edits?: Array<BetaClearToolUses20250919Edit | BetaClearThinking20251015Edit>`

      List of context management edits to apply

      - `BetaClearToolUses20250919Edit`

        - `type: "clear_tool_uses_20250919"`

          - `"clear_tool_uses_20250919"`

        - `clear_at_least?: BetaInputTokensClearAtLeast | null`

          Minimum number of tokens that must be cleared when triggered. Context will only be modified if at least this many tokens can be removed.

          - `type: "input_tokens"`

            - `"input_tokens"`

          - `value: number`

        - `clear_tool_inputs?: boolean | Array<string> | null`

          Whether to clear all tool inputs (bool) or specific tool inputs to clear (list)

          - `boolean`

          - `Array<string>`

        - `exclude_tools?: Array<string> | null`

          Tool names whose uses are preserved from clearing

        - `keep?: BetaToolUsesKeep`

          Number of tool uses to retain in the conversation

          - `type: "tool_uses"`

            - `"tool_uses"`

          - `value: number`

        - `trigger?: BetaInputTokensTrigger | BetaToolUsesTrigger`

          Condition that triggers the context management strategy

          - `BetaInputTokensTrigger`

            - `type: "input_tokens"`

              - `"input_tokens"`

            - `value: number`

          - `BetaToolUsesTrigger`

            - `type: "tool_uses"`

              - `"tool_uses"`

            - `value: number`

      - `BetaClearThinking20251015Edit`

        - `type: "clear_thinking_20251015"`

          - `"clear_thinking_20251015"`

        - `keep?: BetaThinkingTurns | BetaAllThinkingTurns | "all"`

          Number of most recent assistant turns to keep thinking blocks for. Older turns will have their thinking blocks removed.

          - `BetaThinkingTurns`

            - `type: "thinking_turns"`

              - `"thinking_turns"`

            - `value: number`

          - `BetaAllThinkingTurns`

            - `type: "all"`

              - `"all"`

          - `"all"`

            - `"all"`

  - `mcp_servers?: Array<BetaRequestMCPServerURLDefinition>`

    Body param: MCP servers to be utilized in this request

    - `name: string`

    - `type: "url"`

      - `"url"`

    - `url: string`

    - `authorization_token?: string | null`

    - `tool_configuration?: BetaRequestMCPServerToolConfiguration | null`

      - `allowed_tools?: Array<string> | null`

      - `enabled?: boolean | null`

  - `output_config?: BetaOutputConfig`

    Body param: Configuration options for the model's output. Controls aspects like how much effort the model puts into its response.

    - `effort?: "low" | "medium" | "high" | null`

      All possible effort levels.

      - `"low"`

      - `"medium"`

      - `"high"`

  - `output_format?: BetaJSONOutputFormat | null`

    Body param:
    A schema to specify Claude's output format in responses.

    - `schema: Record<string, unknown>`

      The JSON schema of the format

    - `type: "json_schema"`

      - `"json_schema"`

  - `system?: string | Array<BetaTextBlockParam>`

    Body param: System prompt.

    A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

    - `string`

    - `Array<BetaTextBlockParam>`

      - `text: string`

      - `type: "text"`

        - `"text"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `citations?: Array<BetaTextCitationParam> | null`

        - `BetaCitationCharLocationParam`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_char_index: number`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `BetaCitationPageLocationParam`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_page_number: number`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `BetaCitationContentBlockLocationParam`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_block_index: number`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `BetaCitationWebSearchResultLocationParam`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string | null`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `BetaCitationSearchResultLocationParam`

          - `cited_text: string`

          - `end_block_index: number`

          - `search_result_index: number`

          - `source: string`

          - `start_block_index: number`

          - `title: string | null`

          - `type: "search_result_location"`

            - `"search_result_location"`

  - `thinking?: BetaThinkingConfigParam`

    Body param: Configuration for enabling Claude's extended thinking.

    When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

    - `BetaThinkingConfigEnabled`

      - `budget_tokens: number`

        Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

        Must be ≥1024 and less than `max_tokens`.

        See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

      - `type: "enabled"`

        - `"enabled"`

    - `BetaThinkingConfigDisabled`

      - `type: "disabled"`

        - `"disabled"`

  - `tool_choice?: BetaToolChoice`

    Body param: How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

    - `BetaToolChoiceAuto`

      The model will automatically decide whether to use tools.

      - `type: "auto"`

        - `"auto"`

      - `disable_parallel_tool_use?: boolean`

        Whether to disable parallel tool use.

        Defaults to `false`. If set to `true`, the model will output at most one tool use.

    - `BetaToolChoiceAny`

      The model will use any available tools.

      - `type: "any"`

        - `"any"`

      - `disable_parallel_tool_use?: boolean`

        Whether to disable parallel tool use.

        Defaults to `false`. If set to `true`, the model will output exactly one tool use.

    - `BetaToolChoiceTool`

      The model will use the specified tool with `tool_choice.name`.

      - `name: string`

        The name of the tool to use.

      - `type: "tool"`

        - `"tool"`

      - `disable_parallel_tool_use?: boolean`

        Whether to disable parallel tool use.

        Defaults to `false`. If set to `true`, the model will output exactly one tool use.

    - `BetaToolChoiceNone`

      The model will not be allowed to use tools.

      - `type: "none"`

        - `"none"`

  - `tools?: Array<BetaTool | BetaToolBash20241022 | BetaToolBash20250124 | 15 more>`

    Body param: Definitions of tools that the model may use.

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

    - `BetaTool`

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

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `description?: string`

        Description of what this tool does.

        Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

      - `input_examples?: Array<Record<string, unknown>>`

      - `strict?: boolean`

      - `type?: "custom" | null`

        - `"custom"`

    - `BetaToolBash20241022`

      - `name: "bash"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"bash"`

      - `type: "bash_20241022"`

        - `"bash_20241022"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `input_examples?: Array<Record<string, unknown>>`

      - `strict?: boolean`

    - `BetaToolBash20250124`

      - `name: "bash"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"bash"`

      - `type: "bash_20250124"`

        - `"bash_20250124"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `input_examples?: Array<Record<string, unknown>>`

      - `strict?: boolean`

    - `BetaCodeExecutionTool20250522`

      - `name: "code_execution"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"code_execution"`

      - `type: "code_execution_20250522"`

        - `"code_execution_20250522"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `strict?: boolean`

    - `BetaCodeExecutionTool20250825`

      - `name: "code_execution"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"code_execution"`

      - `type: "code_execution_20250825"`

        - `"code_execution_20250825"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `strict?: boolean`

    - `BetaToolComputerUse20241022`

      - `display_height_px: number`

        The height of the display in pixels.

      - `display_width_px: number`

        The width of the display in pixels.

      - `name: "computer"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"computer"`

      - `type: "computer_20241022"`

        - `"computer_20241022"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `display_number?: number | null`

        The X11 display number (e.g. 0, 1) for the display.

      - `input_examples?: Array<Record<string, unknown>>`

      - `strict?: boolean`

    - `BetaMemoryTool20250818`

      - `name: "memory"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"memory"`

      - `type: "memory_20250818"`

        - `"memory_20250818"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `input_examples?: Array<Record<string, unknown>>`

      - `strict?: boolean`

    - `BetaToolComputerUse20250124`

      - `display_height_px: number`

        The height of the display in pixels.

      - `display_width_px: number`

        The width of the display in pixels.

      - `name: "computer"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"computer"`

      - `type: "computer_20250124"`

        - `"computer_20250124"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `display_number?: number | null`

        The X11 display number (e.g. 0, 1) for the display.

      - `input_examples?: Array<Record<string, unknown>>`

      - `strict?: boolean`

    - `BetaToolTextEditor20241022`

      - `name: "str_replace_editor"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"str_replace_editor"`

      - `type: "text_editor_20241022"`

        - `"text_editor_20241022"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `input_examples?: Array<Record<string, unknown>>`

      - `strict?: boolean`

    - `BetaToolComputerUse20251124`

      - `display_height_px: number`

        The height of the display in pixels.

      - `display_width_px: number`

        The width of the display in pixels.

      - `name: "computer"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"computer"`

      - `type: "computer_20251124"`

        - `"computer_20251124"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `display_number?: number | null`

        The X11 display number (e.g. 0, 1) for the display.

      - `enable_zoom?: boolean`

        Whether to enable an action to take a zoomed-in screenshot of the screen.

      - `input_examples?: Array<Record<string, unknown>>`

      - `strict?: boolean`

    - `BetaToolTextEditor20250124`

      - `name: "str_replace_editor"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"str_replace_editor"`

      - `type: "text_editor_20250124"`

        - `"text_editor_20250124"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `input_examples?: Array<Record<string, unknown>>`

      - `strict?: boolean`

    - `BetaToolTextEditor20250429`

      - `name: "str_replace_based_edit_tool"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"str_replace_based_edit_tool"`

      - `type: "text_editor_20250429"`

        - `"text_editor_20250429"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `input_examples?: Array<Record<string, unknown>>`

      - `strict?: boolean`

    - `BetaToolTextEditor20250728`

      - `name: "str_replace_based_edit_tool"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"str_replace_based_edit_tool"`

      - `type: "text_editor_20250728"`

        - `"text_editor_20250728"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `input_examples?: Array<Record<string, unknown>>`

      - `max_characters?: number | null`

        Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

      - `strict?: boolean`

    - `BetaWebSearchTool20250305`

      - `name: "web_search"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"web_search"`

      - `type: "web_search_20250305"`

        - `"web_search_20250305"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `allowed_domains?: Array<string> | null`

        If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

      - `blocked_domains?: Array<string> | null`

        If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `max_uses?: number | null`

        Maximum number of times the tool can be used in the API request.

      - `strict?: boolean`

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

    - `BetaWebFetchTool20250910`

      - `name: "web_fetch"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"web_fetch"`

      - `type: "web_fetch_20250910"`

        - `"web_fetch_20250910"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `allowed_domains?: Array<string> | null`

        List of domains to allow fetching from

      - `blocked_domains?: Array<string> | null`

        List of domains to block fetching from

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `citations?: BetaCitationsConfigParam | null`

        Citations configuration for fetched documents. Citations are disabled by default.

        - `enabled?: boolean`

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `max_content_tokens?: number | null`

        Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

      - `max_uses?: number | null`

        Maximum number of times the tool can be used in the API request.

      - `strict?: boolean`

    - `BetaToolSearchToolBm25_20251119`

      - `name: "tool_search_tool_bm25"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"tool_search_tool_bm25"`

      - `type: "tool_search_tool_bm25_20251119" | "tool_search_tool_bm25"`

        - `"tool_search_tool_bm25_20251119"`

        - `"tool_search_tool_bm25"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `strict?: boolean`

    - `BetaToolSearchToolRegex20251119`

      - `name: "tool_search_tool_regex"`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `"tool_search_tool_regex"`

      - `type: "tool_search_tool_regex_20251119" | "tool_search_tool_regex"`

        - `"tool_search_tool_regex_20251119"`

        - `"tool_search_tool_regex"`

      - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

        - `"direct"`

        - `"code_execution_20250825"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `defer_loading?: boolean`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `strict?: boolean`

    - `BetaMCPToolset`

      Configuration for a group of tools from an MCP server.

      Allows configuring enabled status and defer_loading for all tools
      from an MCP server, with optional per-tool overrides.

      - `mcp_server_name: string`

        Name of the MCP server to configure tools for

      - `type: "mcp_toolset"`

        - `"mcp_toolset"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `configs?: Record<string, BetaMCPToolConfig> | null`

        Configuration overrides for specific tools, keyed by tool name

        - `defer_loading?: boolean`

        - `enabled?: boolean`

      - `default_config?: BetaMCPToolDefaultConfig`

        Default configuration applied to all tools from this server

        - `defer_loading?: boolean`

        - `enabled?: boolean`

  - `betas?: Array<AnthropicBeta>`

    Header param: Optional header to specify the beta version(s) you want to use.

    - `(string & {})`

    - `"message-batches-2024-09-24" | "prompt-caching-2024-07-31" | "computer-use-2024-10-22" | 16 more`

      - `"message-batches-2024-09-24"`

      - `"prompt-caching-2024-07-31"`

      - `"computer-use-2024-10-22"`

      - `"computer-use-2025-01-24"`

      - `"pdfs-2024-09-25"`

      - `"token-counting-2024-11-01"`

      - `"token-efficient-tools-2025-02-19"`

      - `"output-128k-2025-02-19"`

      - `"files-api-2025-04-14"`

      - `"mcp-client-2025-04-04"`

      - `"mcp-client-2025-11-20"`

      - `"dev-full-thinking-2025-05-14"`

      - `"interleaved-thinking-2025-05-14"`

      - `"code-execution-2025-05-22"`

      - `"extended-cache-ttl-2025-04-11"`

      - `"context-1m-2025-08-07"`

      - `"context-management-2025-06-27"`

      - `"model-context-window-exceeded-2025-08-26"`

      - `"skills-2025-10-02"`

### Returns

- `BetaMessageTokensCount`

  - `context_management: BetaCountTokensContextManagementResponse | null`

    Information about context management applied to the message.

    - `original_input_tokens: number`

      The original token count before context management was applied

  - `input_tokens: number`

    The total number of tokens across the provided list of messages, system prompt, and tools.

### Example

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: 'my-anthropic-api-key',
});

const betaMessageTokensCount = await client.beta.messages.countTokens({
  messages: [{ content: 'string', role: 'user' }],
  model: 'claude-opus-4-5-20251101',
});

console.log(betaMessageTokensCount.context_management);
```

## Domain Types

### Beta All Thinking Turns

- `BetaAllThinkingTurns`

  - `type: "all"`

    - `"all"`

### Beta Base64 Image Source

- `BetaBase64ImageSource`

  - `data: string`

  - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

    - `"image/jpeg"`

    - `"image/png"`

    - `"image/gif"`

    - `"image/webp"`

  - `type: "base64"`

    - `"base64"`

### Beta Base64 PDF Source

- `BetaBase64PDFSource`

  - `data: string`

  - `media_type: "application/pdf"`

    - `"application/pdf"`

  - `type: "base64"`

    - `"base64"`

### Beta Bash Code Execution Output Block

- `BetaBashCodeExecutionOutputBlock`

  - `file_id: string`

  - `type: "bash_code_execution_output"`

    - `"bash_code_execution_output"`

### Beta Bash Code Execution Output Block Param

- `BetaBashCodeExecutionOutputBlockParam`

  - `file_id: string`

  - `type: "bash_code_execution_output"`

    - `"bash_code_execution_output"`

### Beta Bash Code Execution Result Block

- `BetaBashCodeExecutionResultBlock`

  - `content: Array<BetaBashCodeExecutionOutputBlock>`

    - `file_id: string`

    - `type: "bash_code_execution_output"`

      - `"bash_code_execution_output"`

  - `return_code: number`

  - `stderr: string`

  - `stdout: string`

  - `type: "bash_code_execution_result"`

    - `"bash_code_execution_result"`

### Beta Bash Code Execution Result Block Param

- `BetaBashCodeExecutionResultBlockParam`

  - `content: Array<BetaBashCodeExecutionOutputBlockParam>`

    - `file_id: string`

    - `type: "bash_code_execution_output"`

      - `"bash_code_execution_output"`

  - `return_code: number`

  - `stderr: string`

  - `stdout: string`

  - `type: "bash_code_execution_result"`

    - `"bash_code_execution_result"`

### Beta Bash Code Execution Tool Result Block

- `BetaBashCodeExecutionToolResultBlock`

  - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

    - `BetaBashCodeExecutionToolResultError`

      - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

        - `"invalid_tool_input"`

        - `"unavailable"`

        - `"too_many_requests"`

        - `"execution_time_exceeded"`

        - `"output_file_too_large"`

      - `type: "bash_code_execution_tool_result_error"`

        - `"bash_code_execution_tool_result_error"`

    - `BetaBashCodeExecutionResultBlock`

      - `content: Array<BetaBashCodeExecutionOutputBlock>`

        - `file_id: string`

        - `type: "bash_code_execution_output"`

          - `"bash_code_execution_output"`

      - `return_code: number`

      - `stderr: string`

      - `stdout: string`

      - `type: "bash_code_execution_result"`

        - `"bash_code_execution_result"`

  - `tool_use_id: string`

  - `type: "bash_code_execution_tool_result"`

    - `"bash_code_execution_tool_result"`

### Beta Bash Code Execution Tool Result Block Param

- `BetaBashCodeExecutionToolResultBlockParam`

  - `content: BetaBashCodeExecutionToolResultErrorParam | BetaBashCodeExecutionResultBlockParam`

    - `BetaBashCodeExecutionToolResultErrorParam`

      - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

        - `"invalid_tool_input"`

        - `"unavailable"`

        - `"too_many_requests"`

        - `"execution_time_exceeded"`

        - `"output_file_too_large"`

      - `type: "bash_code_execution_tool_result_error"`

        - `"bash_code_execution_tool_result_error"`

    - `BetaBashCodeExecutionResultBlockParam`

      - `content: Array<BetaBashCodeExecutionOutputBlockParam>`

        - `file_id: string`

        - `type: "bash_code_execution_output"`

          - `"bash_code_execution_output"`

      - `return_code: number`

      - `stderr: string`

      - `stdout: string`

      - `type: "bash_code_execution_result"`

        - `"bash_code_execution_result"`

  - `tool_use_id: string`

  - `type: "bash_code_execution_tool_result"`

    - `"bash_code_execution_tool_result"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta Bash Code Execution Tool Result Error

- `BetaBashCodeExecutionToolResultError`

  - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

    - `"output_file_too_large"`

  - `type: "bash_code_execution_tool_result_error"`

    - `"bash_code_execution_tool_result_error"`

### Beta Bash Code Execution Tool Result Error Param

- `BetaBashCodeExecutionToolResultErrorParam`

  - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

    - `"output_file_too_large"`

  - `type: "bash_code_execution_tool_result_error"`

    - `"bash_code_execution_tool_result_error"`

### Beta Cache Control Ephemeral

- `BetaCacheControlEphemeral`

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

### Beta Cache Creation

- `BetaCacheCreation`

  - `ephemeral_1h_input_tokens: number`

    The number of input tokens used to create the 1 hour cache entry.

  - `ephemeral_5m_input_tokens: number`

    The number of input tokens used to create the 5 minute cache entry.

### Beta Citation Char Location

- `BetaCitationCharLocation`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string | null`

  - `end_char_index: number`

  - `file_id: string | null`

  - `start_char_index: number`

  - `type: "char_location"`

    - `"char_location"`

### Beta Citation Char Location Param

- `BetaCitationCharLocationParam`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string | null`

  - `end_char_index: number`

  - `start_char_index: number`

  - `type: "char_location"`

    - `"char_location"`

### Beta Citation Config

- `BetaCitationConfig`

  - `enabled: boolean`

### Beta Citation Content Block Location

- `BetaCitationContentBlockLocation`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string | null`

  - `end_block_index: number`

  - `file_id: string | null`

  - `start_block_index: number`

  - `type: "content_block_location"`

    - `"content_block_location"`

### Beta Citation Content Block Location Param

- `BetaCitationContentBlockLocationParam`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string | null`

  - `end_block_index: number`

  - `start_block_index: number`

  - `type: "content_block_location"`

    - `"content_block_location"`

### Beta Citation Page Location

- `BetaCitationPageLocation`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string | null`

  - `end_page_number: number`

  - `file_id: string | null`

  - `start_page_number: number`

  - `type: "page_location"`

    - `"page_location"`

### Beta Citation Page Location Param

- `BetaCitationPageLocationParam`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string | null`

  - `end_page_number: number`

  - `start_page_number: number`

  - `type: "page_location"`

    - `"page_location"`

### Beta Citation Search Result Location

- `BetaCitationSearchResultLocation`

  - `cited_text: string`

  - `end_block_index: number`

  - `search_result_index: number`

  - `source: string`

  - `start_block_index: number`

  - `title: string | null`

  - `type: "search_result_location"`

    - `"search_result_location"`

### Beta Citation Search Result Location Param

- `BetaCitationSearchResultLocationParam`

  - `cited_text: string`

  - `end_block_index: number`

  - `search_result_index: number`

  - `source: string`

  - `start_block_index: number`

  - `title: string | null`

  - `type: "search_result_location"`

    - `"search_result_location"`

### Beta Citation Web Search Result Location Param

- `BetaCitationWebSearchResultLocationParam`

  - `cited_text: string`

  - `encrypted_index: string`

  - `title: string | null`

  - `type: "web_search_result_location"`

    - `"web_search_result_location"`

  - `url: string`

### Beta Citations Config Param

- `BetaCitationsConfigParam`

  - `enabled?: boolean`

### Beta Citations Delta

- `BetaCitationsDelta`

  - `citation: BetaCitationCharLocation | BetaCitationPageLocation | BetaCitationContentBlockLocation | 2 more`

    - `BetaCitationCharLocation`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string | null`

      - `end_char_index: number`

      - `file_id: string | null`

      - `start_char_index: number`

      - `type: "char_location"`

        - `"char_location"`

    - `BetaCitationPageLocation`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string | null`

      - `end_page_number: number`

      - `file_id: string | null`

      - `start_page_number: number`

      - `type: "page_location"`

        - `"page_location"`

    - `BetaCitationContentBlockLocation`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string | null`

      - `end_block_index: number`

      - `file_id: string | null`

      - `start_block_index: number`

      - `type: "content_block_location"`

        - `"content_block_location"`

    - `BetaCitationsWebSearchResultLocation`

      - `cited_text: string`

      - `encrypted_index: string`

      - `title: string | null`

      - `type: "web_search_result_location"`

        - `"web_search_result_location"`

      - `url: string`

    - `BetaCitationSearchResultLocation`

      - `cited_text: string`

      - `end_block_index: number`

      - `search_result_index: number`

      - `source: string`

      - `start_block_index: number`

      - `title: string | null`

      - `type: "search_result_location"`

        - `"search_result_location"`

  - `type: "citations_delta"`

    - `"citations_delta"`

### Beta Citations Web Search Result Location

- `BetaCitationsWebSearchResultLocation`

  - `cited_text: string`

  - `encrypted_index: string`

  - `title: string | null`

  - `type: "web_search_result_location"`

    - `"web_search_result_location"`

  - `url: string`

### Beta Clear Thinking 20251015 Edit

- `BetaClearThinking20251015Edit`

  - `type: "clear_thinking_20251015"`

    - `"clear_thinking_20251015"`

  - `keep?: BetaThinkingTurns | BetaAllThinkingTurns | "all"`

    Number of most recent assistant turns to keep thinking blocks for. Older turns will have their thinking blocks removed.

    - `BetaThinkingTurns`

      - `type: "thinking_turns"`

        - `"thinking_turns"`

      - `value: number`

    - `BetaAllThinkingTurns`

      - `type: "all"`

        - `"all"`

    - `"all"`

      - `"all"`

### Beta Clear Thinking 20251015 Edit Response

- `BetaClearThinking20251015EditResponse`

  - `cleared_input_tokens: number`

    Number of input tokens cleared by this edit.

  - `cleared_thinking_turns: number`

    Number of thinking turns that were cleared.

  - `type: "clear_thinking_20251015"`

    The type of context management edit applied.

    - `"clear_thinking_20251015"`

### Beta Clear Tool Uses 20250919 Edit

- `BetaClearToolUses20250919Edit`

  - `type: "clear_tool_uses_20250919"`

    - `"clear_tool_uses_20250919"`

  - `clear_at_least?: BetaInputTokensClearAtLeast | null`

    Minimum number of tokens that must be cleared when triggered. Context will only be modified if at least this many tokens can be removed.

    - `type: "input_tokens"`

      - `"input_tokens"`

    - `value: number`

  - `clear_tool_inputs?: boolean | Array<string> | null`

    Whether to clear all tool inputs (bool) or specific tool inputs to clear (list)

    - `boolean`

    - `Array<string>`

  - `exclude_tools?: Array<string> | null`

    Tool names whose uses are preserved from clearing

  - `keep?: BetaToolUsesKeep`

    Number of tool uses to retain in the conversation

    - `type: "tool_uses"`

      - `"tool_uses"`

    - `value: number`

  - `trigger?: BetaInputTokensTrigger | BetaToolUsesTrigger`

    Condition that triggers the context management strategy

    - `BetaInputTokensTrigger`

      - `type: "input_tokens"`

        - `"input_tokens"`

      - `value: number`

    - `BetaToolUsesTrigger`

      - `type: "tool_uses"`

        - `"tool_uses"`

      - `value: number`

### Beta Clear Tool Uses 20250919 Edit Response

- `BetaClearToolUses20250919EditResponse`

  - `cleared_input_tokens: number`

    Number of input tokens cleared by this edit.

  - `cleared_tool_uses: number`

    Number of tool uses that were cleared.

  - `type: "clear_tool_uses_20250919"`

    The type of context management edit applied.

    - `"clear_tool_uses_20250919"`

### Beta Code Execution Output Block

- `BetaCodeExecutionOutputBlock`

  - `file_id: string`

  - `type: "code_execution_output"`

    - `"code_execution_output"`

### Beta Code Execution Output Block Param

- `BetaCodeExecutionOutputBlockParam`

  - `file_id: string`

  - `type: "code_execution_output"`

    - `"code_execution_output"`

### Beta Code Execution Result Block

- `BetaCodeExecutionResultBlock`

  - `content: Array<BetaCodeExecutionOutputBlock>`

    - `file_id: string`

    - `type: "code_execution_output"`

      - `"code_execution_output"`

  - `return_code: number`

  - `stderr: string`

  - `stdout: string`

  - `type: "code_execution_result"`

    - `"code_execution_result"`

### Beta Code Execution Result Block Param

- `BetaCodeExecutionResultBlockParam`

  - `content: Array<BetaCodeExecutionOutputBlockParam>`

    - `file_id: string`

    - `type: "code_execution_output"`

      - `"code_execution_output"`

  - `return_code: number`

  - `stderr: string`

  - `stdout: string`

  - `type: "code_execution_result"`

    - `"code_execution_result"`

### Beta Code Execution Tool 20250522

- `BetaCodeExecutionTool20250522`

  - `name: "code_execution"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"code_execution"`

  - `type: "code_execution_20250522"`

    - `"code_execution_20250522"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `strict?: boolean`

### Beta Code Execution Tool 20250825

- `BetaCodeExecutionTool20250825`

  - `name: "code_execution"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"code_execution"`

  - `type: "code_execution_20250825"`

    - `"code_execution_20250825"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `strict?: boolean`

### Beta Code Execution Tool Result Block

- `BetaCodeExecutionToolResultBlock`

  - `content: BetaCodeExecutionToolResultBlockContent`

    - `BetaCodeExecutionToolResultError`

      - `error_code: BetaCodeExecutionToolResultErrorCode`

        - `"invalid_tool_input"`

        - `"unavailable"`

        - `"too_many_requests"`

        - `"execution_time_exceeded"`

      - `type: "code_execution_tool_result_error"`

        - `"code_execution_tool_result_error"`

    - `BetaCodeExecutionResultBlock`

      - `content: Array<BetaCodeExecutionOutputBlock>`

        - `file_id: string`

        - `type: "code_execution_output"`

          - `"code_execution_output"`

      - `return_code: number`

      - `stderr: string`

      - `stdout: string`

      - `type: "code_execution_result"`

        - `"code_execution_result"`

  - `tool_use_id: string`

  - `type: "code_execution_tool_result"`

    - `"code_execution_tool_result"`

### Beta Code Execution Tool Result Block Content

- `BetaCodeExecutionToolResultBlockContent = BetaCodeExecutionToolResultError | BetaCodeExecutionResultBlock`

  - `BetaCodeExecutionToolResultError`

    - `error_code: BetaCodeExecutionToolResultErrorCode`

      - `"invalid_tool_input"`

      - `"unavailable"`

      - `"too_many_requests"`

      - `"execution_time_exceeded"`

    - `type: "code_execution_tool_result_error"`

      - `"code_execution_tool_result_error"`

  - `BetaCodeExecutionResultBlock`

    - `content: Array<BetaCodeExecutionOutputBlock>`

      - `file_id: string`

      - `type: "code_execution_output"`

        - `"code_execution_output"`

    - `return_code: number`

    - `stderr: string`

    - `stdout: string`

    - `type: "code_execution_result"`

      - `"code_execution_result"`

### Beta Code Execution Tool Result Block Param

- `BetaCodeExecutionToolResultBlockParam`

  - `content: BetaCodeExecutionToolResultBlockParamContent`

    - `BetaCodeExecutionToolResultErrorParam`

      - `error_code: BetaCodeExecutionToolResultErrorCode`

        - `"invalid_tool_input"`

        - `"unavailable"`

        - `"too_many_requests"`

        - `"execution_time_exceeded"`

      - `type: "code_execution_tool_result_error"`

        - `"code_execution_tool_result_error"`

    - `BetaCodeExecutionResultBlockParam`

      - `content: Array<BetaCodeExecutionOutputBlockParam>`

        - `file_id: string`

        - `type: "code_execution_output"`

          - `"code_execution_output"`

      - `return_code: number`

      - `stderr: string`

      - `stdout: string`

      - `type: "code_execution_result"`

        - `"code_execution_result"`

  - `tool_use_id: string`

  - `type: "code_execution_tool_result"`

    - `"code_execution_tool_result"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta Code Execution Tool Result Block Param Content

- `BetaCodeExecutionToolResultBlockParamContent = BetaCodeExecutionToolResultErrorParam | BetaCodeExecutionResultBlockParam`

  - `BetaCodeExecutionToolResultErrorParam`

    - `error_code: BetaCodeExecutionToolResultErrorCode`

      - `"invalid_tool_input"`

      - `"unavailable"`

      - `"too_many_requests"`

      - `"execution_time_exceeded"`

    - `type: "code_execution_tool_result_error"`

      - `"code_execution_tool_result_error"`

  - `BetaCodeExecutionResultBlockParam`

    - `content: Array<BetaCodeExecutionOutputBlockParam>`

      - `file_id: string`

      - `type: "code_execution_output"`

        - `"code_execution_output"`

    - `return_code: number`

    - `stderr: string`

    - `stdout: string`

    - `type: "code_execution_result"`

      - `"code_execution_result"`

### Beta Code Execution Tool Result Error

- `BetaCodeExecutionToolResultError`

  - `error_code: BetaCodeExecutionToolResultErrorCode`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

  - `type: "code_execution_tool_result_error"`

    - `"code_execution_tool_result_error"`

### Beta Code Execution Tool Result Error Code

- `BetaCodeExecutionToolResultErrorCode = "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

  - `"invalid_tool_input"`

  - `"unavailable"`

  - `"too_many_requests"`

  - `"execution_time_exceeded"`

### Beta Code Execution Tool Result Error Param

- `BetaCodeExecutionToolResultErrorParam`

  - `error_code: BetaCodeExecutionToolResultErrorCode`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

  - `type: "code_execution_tool_result_error"`

    - `"code_execution_tool_result_error"`

### Beta Container

- `BetaContainer`

  Information about the container used in the request (for the code execution tool)

  - `id: string`

    Identifier for the container used in this request

  - `expires_at: string`

    The time at which the container will expire.

  - `skills: Array<BetaSkill> | null`

    Skills loaded in the container

    - `skill_id: string`

      Skill ID

    - `type: "anthropic" | "custom"`

      Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

      - `"anthropic"`

      - `"custom"`

    - `version: string`

      Skill version or 'latest' for most recent version

### Beta Container Params

- `BetaContainerParams`

  Container parameters with skills to be loaded.

  - `id?: string | null`

    Container id

  - `skills?: Array<BetaSkillParams> | null`

    List of skills to load in the container

    - `skill_id: string`

      Skill ID

    - `type: "anthropic" | "custom"`

      Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

      - `"anthropic"`

      - `"custom"`

    - `version?: string`

      Skill version or 'latest' for most recent version

### Beta Container Upload Block

- `BetaContainerUploadBlock`

  Response model for a file uploaded to the container.

  - `file_id: string`

  - `type: "container_upload"`

    - `"container_upload"`

### Beta Container Upload Block Param

- `BetaContainerUploadBlockParam`

  A content block that represents a file to be uploaded to the container
  Files uploaded via this block will be available in the container's input directory.

  - `file_id: string`

  - `type: "container_upload"`

    - `"container_upload"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta Content Block

- `BetaContentBlock = BetaTextBlock | BetaThinkingBlock | BetaRedactedThinkingBlock | 11 more`

  Response model for a file uploaded to the container.

  - `BetaTextBlock`

    - `citations: Array<BetaTextCitation> | null`

      Citations supporting the text block.

      The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

      - `BetaCitationCharLocation`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_char_index: number`

        - `file_id: string | null`

        - `start_char_index: number`

        - `type: "char_location"`

          - `"char_location"`

      - `BetaCitationPageLocation`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_page_number: number`

        - `file_id: string | null`

        - `start_page_number: number`

        - `type: "page_location"`

          - `"page_location"`

      - `BetaCitationContentBlockLocation`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_block_index: number`

        - `file_id: string | null`

        - `start_block_index: number`

        - `type: "content_block_location"`

          - `"content_block_location"`

      - `BetaCitationsWebSearchResultLocation`

        - `cited_text: string`

        - `encrypted_index: string`

        - `title: string | null`

        - `type: "web_search_result_location"`

          - `"web_search_result_location"`

        - `url: string`

      - `BetaCitationSearchResultLocation`

        - `cited_text: string`

        - `end_block_index: number`

        - `search_result_index: number`

        - `source: string`

        - `start_block_index: number`

        - `title: string | null`

        - `type: "search_result_location"`

          - `"search_result_location"`

    - `text: string`

    - `type: "text"`

      - `"text"`

  - `BetaThinkingBlock`

    - `signature: string`

    - `thinking: string`

    - `type: "thinking"`

      - `"thinking"`

  - `BetaRedactedThinkingBlock`

    - `data: string`

    - `type: "redacted_thinking"`

      - `"redacted_thinking"`

  - `BetaToolUseBlock`

    - `id: string`

    - `input: Record<string, unknown>`

    - `name: string`

    - `type: "tool_use"`

      - `"tool_use"`

    - `caller?: BetaDirectCaller | BetaServerToolCaller`

      Tool invocation directly from the model.

      - `BetaDirectCaller`

        Tool invocation directly from the model.

        - `type: "direct"`

          - `"direct"`

      - `BetaServerToolCaller`

        Tool invocation generated by a server-side tool.

        - `tool_id: string`

        - `type: "code_execution_20250825"`

          - `"code_execution_20250825"`

  - `BetaServerToolUseBlock`

    - `id: string`

    - `caller: BetaDirectCaller | BetaServerToolCaller`

      Tool invocation directly from the model.

      - `BetaDirectCaller`

        Tool invocation directly from the model.

        - `type: "direct"`

          - `"direct"`

      - `BetaServerToolCaller`

        Tool invocation generated by a server-side tool.

        - `tool_id: string`

        - `type: "code_execution_20250825"`

          - `"code_execution_20250825"`

    - `input: Record<string, unknown>`

    - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

      - `"web_search"`

      - `"web_fetch"`

      - `"code_execution"`

      - `"bash_code_execution"`

      - `"text_editor_code_execution"`

      - `"tool_search_tool_regex"`

      - `"tool_search_tool_bm25"`

    - `type: "server_tool_use"`

      - `"server_tool_use"`

  - `BetaWebSearchToolResultBlock`

    - `content: BetaWebSearchToolResultBlockContent`

      - `BetaWebSearchToolResultError`

        - `error_code: BetaWebSearchToolResultErrorCode`

          - `"invalid_tool_input"`

          - `"unavailable"`

          - `"max_uses_exceeded"`

          - `"too_many_requests"`

          - `"query_too_long"`

        - `type: "web_search_tool_result_error"`

          - `"web_search_tool_result_error"`

      - `Array<BetaWebSearchResultBlock>`

        - `encrypted_content: string`

        - `page_age: string | null`

        - `title: string`

        - `type: "web_search_result"`

          - `"web_search_result"`

        - `url: string`

    - `tool_use_id: string`

    - `type: "web_search_tool_result"`

      - `"web_search_tool_result"`

  - `BetaWebFetchToolResultBlock`

    - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

      - `BetaWebFetchToolResultErrorBlock`

        - `error_code: BetaWebFetchToolResultErrorCode`

          - `"invalid_tool_input"`

          - `"url_too_long"`

          - `"url_not_allowed"`

          - `"url_not_accessible"`

          - `"unsupported_content_type"`

          - `"too_many_requests"`

          - `"max_uses_exceeded"`

          - `"unavailable"`

        - `type: "web_fetch_tool_result_error"`

          - `"web_fetch_tool_result_error"`

      - `BetaWebFetchBlock`

        - `content: BetaDocumentBlock`

          - `citations: BetaCitationConfig | null`

            Citation configuration for the document

            - `enabled: boolean`

          - `source: BetaBase64PDFSource | BetaPlainTextSource`

            - `BetaBase64PDFSource`

              - `data: string`

              - `media_type: "application/pdf"`

                - `"application/pdf"`

              - `type: "base64"`

                - `"base64"`

            - `BetaPlainTextSource`

              - `data: string`

              - `media_type: "text/plain"`

                - `"text/plain"`

              - `type: "text"`

                - `"text"`

          - `title: string | null`

            The title of the document

          - `type: "document"`

            - `"document"`

        - `retrieved_at: string | null`

          ISO 8601 timestamp when the content was retrieved

        - `type: "web_fetch_result"`

          - `"web_fetch_result"`

        - `url: string`

          Fetched content URL

    - `tool_use_id: string`

    - `type: "web_fetch_tool_result"`

      - `"web_fetch_tool_result"`

  - `BetaCodeExecutionToolResultBlock`

    - `content: BetaCodeExecutionToolResultBlockContent`

      - `BetaCodeExecutionToolResultError`

        - `error_code: BetaCodeExecutionToolResultErrorCode`

          - `"invalid_tool_input"`

          - `"unavailable"`

          - `"too_many_requests"`

          - `"execution_time_exceeded"`

        - `type: "code_execution_tool_result_error"`

          - `"code_execution_tool_result_error"`

      - `BetaCodeExecutionResultBlock`

        - `content: Array<BetaCodeExecutionOutputBlock>`

          - `file_id: string`

          - `type: "code_execution_output"`

            - `"code_execution_output"`

        - `return_code: number`

        - `stderr: string`

        - `stdout: string`

        - `type: "code_execution_result"`

          - `"code_execution_result"`

    - `tool_use_id: string`

    - `type: "code_execution_tool_result"`

      - `"code_execution_tool_result"`

  - `BetaBashCodeExecutionToolResultBlock`

    - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

      - `BetaBashCodeExecutionToolResultError`

        - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

          - `"invalid_tool_input"`

          - `"unavailable"`

          - `"too_many_requests"`

          - `"execution_time_exceeded"`

          - `"output_file_too_large"`

        - `type: "bash_code_execution_tool_result_error"`

          - `"bash_code_execution_tool_result_error"`

      - `BetaBashCodeExecutionResultBlock`

        - `content: Array<BetaBashCodeExecutionOutputBlock>`

          - `file_id: string`

          - `type: "bash_code_execution_output"`

            - `"bash_code_execution_output"`

        - `return_code: number`

        - `stderr: string`

        - `stdout: string`

        - `type: "bash_code_execution_result"`

          - `"bash_code_execution_result"`

    - `tool_use_id: string`

    - `type: "bash_code_execution_tool_result"`

      - `"bash_code_execution_tool_result"`

  - `BetaTextEditorCodeExecutionToolResultBlock`

    - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

      - `BetaTextEditorCodeExecutionToolResultError`

        - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

          - `"invalid_tool_input"`

          - `"unavailable"`

          - `"too_many_requests"`

          - `"execution_time_exceeded"`

          - `"file_not_found"`

        - `error_message: string | null`

        - `type: "text_editor_code_execution_tool_result_error"`

          - `"text_editor_code_execution_tool_result_error"`

      - `BetaTextEditorCodeExecutionViewResultBlock`

        - `content: string`

        - `file_type: "text" | "image" | "pdf"`

          - `"text"`

          - `"image"`

          - `"pdf"`

        - `num_lines: number | null`

        - `start_line: number | null`

        - `total_lines: number | null`

        - `type: "text_editor_code_execution_view_result"`

          - `"text_editor_code_execution_view_result"`

      - `BetaTextEditorCodeExecutionCreateResultBlock`

        - `is_file_update: boolean`

        - `type: "text_editor_code_execution_create_result"`

          - `"text_editor_code_execution_create_result"`

      - `BetaTextEditorCodeExecutionStrReplaceResultBlock`

        - `lines: Array<string> | null`

        - `new_lines: number | null`

        - `new_start: number | null`

        - `old_lines: number | null`

        - `old_start: number | null`

        - `type: "text_editor_code_execution_str_replace_result"`

          - `"text_editor_code_execution_str_replace_result"`

    - `tool_use_id: string`

    - `type: "text_editor_code_execution_tool_result"`

      - `"text_editor_code_execution_tool_result"`

  - `BetaToolSearchToolResultBlock`

    - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

      - `BetaToolSearchToolResultError`

        - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

          - `"invalid_tool_input"`

          - `"unavailable"`

          - `"too_many_requests"`

          - `"execution_time_exceeded"`

        - `error_message: string | null`

        - `type: "tool_search_tool_result_error"`

          - `"tool_search_tool_result_error"`

      - `BetaToolSearchToolSearchResultBlock`

        - `tool_references: Array<BetaToolReferenceBlock>`

          - `tool_name: string`

          - `type: "tool_reference"`

            - `"tool_reference"`

        - `type: "tool_search_tool_search_result"`

          - `"tool_search_tool_search_result"`

    - `tool_use_id: string`

    - `type: "tool_search_tool_result"`

      - `"tool_search_tool_result"`

  - `BetaMCPToolUseBlock`

    - `id: string`

    - `input: Record<string, unknown>`

    - `name: string`

      The name of the MCP tool

    - `server_name: string`

      The name of the MCP server

    - `type: "mcp_tool_use"`

      - `"mcp_tool_use"`

  - `BetaMCPToolResultBlock`

    - `content: string | Array<BetaTextBlock>`

      - `string`

      - `Array<BetaTextBlock>`

        - `citations: Array<BetaTextCitation> | null`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `BetaCitationCharLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_char_index: number`

            - `file_id: string | null`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `BetaCitationPageLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_page_number: number`

            - `file_id: string | null`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `BetaCitationContentBlockLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_block_index: number`

            - `file_id: string | null`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `BetaCitationsWebSearchResultLocation`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string | null`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `BetaCitationSearchResultLocation`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string | null`

            - `type: "search_result_location"`

              - `"search_result_location"`

        - `text: string`

        - `type: "text"`

          - `"text"`

    - `is_error: boolean`

    - `tool_use_id: string`

    - `type: "mcp_tool_result"`

      - `"mcp_tool_result"`

  - `BetaContainerUploadBlock`

    Response model for a file uploaded to the container.

    - `file_id: string`

    - `type: "container_upload"`

      - `"container_upload"`

### Beta Content Block Param

- `BetaContentBlockParam = BetaTextBlockParam | BetaImageBlockParam | BetaRequestDocumentBlock | 15 more`

  Regular text content.

  - `BetaTextBlockParam`

    - `text: string`

    - `type: "text"`

      - `"text"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `citations?: Array<BetaTextCitationParam> | null`

      - `BetaCitationCharLocationParam`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_char_index: number`

        - `start_char_index: number`

        - `type: "char_location"`

          - `"char_location"`

      - `BetaCitationPageLocationParam`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_page_number: number`

        - `start_page_number: number`

        - `type: "page_location"`

          - `"page_location"`

      - `BetaCitationContentBlockLocationParam`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_block_index: number`

        - `start_block_index: number`

        - `type: "content_block_location"`

          - `"content_block_location"`

      - `BetaCitationWebSearchResultLocationParam`

        - `cited_text: string`

        - `encrypted_index: string`

        - `title: string | null`

        - `type: "web_search_result_location"`

          - `"web_search_result_location"`

        - `url: string`

      - `BetaCitationSearchResultLocationParam`

        - `cited_text: string`

        - `end_block_index: number`

        - `search_result_index: number`

        - `source: string`

        - `start_block_index: number`

        - `title: string | null`

        - `type: "search_result_location"`

          - `"search_result_location"`

  - `BetaImageBlockParam`

    - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

      - `BetaBase64ImageSource`

        - `data: string`

        - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

          - `"image/jpeg"`

          - `"image/png"`

          - `"image/gif"`

          - `"image/webp"`

        - `type: "base64"`

          - `"base64"`

      - `BetaURLImageSource`

        - `type: "url"`

          - `"url"`

        - `url: string`

      - `BetaFileImageSource`

        - `file_id: string`

        - `type: "file"`

          - `"file"`

    - `type: "image"`

      - `"image"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `BetaRequestDocumentBlock`

    - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

      - `BetaBase64PDFSource`

        - `data: string`

        - `media_type: "application/pdf"`

          - `"application/pdf"`

        - `type: "base64"`

          - `"base64"`

      - `BetaPlainTextSource`

        - `data: string`

        - `media_type: "text/plain"`

          - `"text/plain"`

        - `type: "text"`

          - `"text"`

      - `BetaContentBlockSource`

        - `content: string | Array<BetaContentBlockSourceContent>`

          - `string`

          - `Array<BetaContentBlockSourceContent>`

            - `BetaTextBlockParam`

              - `text: string`

              - `type: "text"`

                - `"text"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `citations?: Array<BetaTextCitationParam> | null`

                - `BetaCitationCharLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_char_index: number`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `BetaCitationPageLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_page_number: number`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `BetaCitationContentBlockLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_block_index: number`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `BetaCitationWebSearchResultLocationParam`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string | null`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `BetaCitationSearchResultLocationParam`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string | null`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

            - `BetaImageBlockParam`

              - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                - `BetaBase64ImageSource`

                  - `data: string`

                  - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                    - `"image/jpeg"`

                    - `"image/png"`

                    - `"image/gif"`

                    - `"image/webp"`

                  - `type: "base64"`

                    - `"base64"`

                - `BetaURLImageSource`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

                - `BetaFileImageSource`

                  - `file_id: string`

                  - `type: "file"`

                    - `"file"`

              - `type: "image"`

                - `"image"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `BetaURLPDFSource`

        - `type: "url"`

          - `"url"`

        - `url: string`

      - `BetaFileDocumentSource`

        - `file_id: string`

        - `type: "file"`

          - `"file"`

    - `type: "document"`

      - `"document"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `citations?: BetaCitationsConfigParam | null`

      - `enabled?: boolean`

    - `context?: string | null`

    - `title?: string | null`

  - `BetaSearchResultBlockParam`

    - `content: Array<BetaTextBlockParam>`

      - `text: string`

      - `type: "text"`

        - `"text"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `citations?: Array<BetaTextCitationParam> | null`

        - `BetaCitationCharLocationParam`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_char_index: number`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `BetaCitationPageLocationParam`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_page_number: number`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `BetaCitationContentBlockLocationParam`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_block_index: number`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `BetaCitationWebSearchResultLocationParam`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string | null`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `BetaCitationSearchResultLocationParam`

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

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `citations?: BetaCitationsConfigParam`

      - `enabled?: boolean`

  - `BetaThinkingBlockParam`

    - `signature: string`

    - `thinking: string`

    - `type: "thinking"`

      - `"thinking"`

  - `BetaRedactedThinkingBlockParam`

    - `data: string`

    - `type: "redacted_thinking"`

      - `"redacted_thinking"`

  - `BetaToolUseBlockParam`

    - `id: string`

    - `input: Record<string, unknown>`

    - `name: string`

    - `type: "tool_use"`

      - `"tool_use"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `caller?: BetaDirectCaller | BetaServerToolCaller`

      Tool invocation directly from the model.

      - `BetaDirectCaller`

        Tool invocation directly from the model.

        - `type: "direct"`

          - `"direct"`

      - `BetaServerToolCaller`

        Tool invocation generated by a server-side tool.

        - `tool_id: string`

        - `type: "code_execution_20250825"`

          - `"code_execution_20250825"`

  - `BetaToolResultBlockParam`

    - `tool_use_id: string`

    - `type: "tool_result"`

      - `"tool_result"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `content?: string | Array<BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more>`

      - `string`

      - `Array<BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more>`

        - `BetaTextBlockParam`

          - `text: string`

          - `type: "text"`

            - `"text"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `citations?: Array<BetaTextCitationParam> | null`

            - `BetaCitationCharLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_char_index: number`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `BetaCitationPageLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_page_number: number`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `BetaCitationContentBlockLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_block_index: number`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `BetaCitationWebSearchResultLocationParam`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string | null`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `BetaCitationSearchResultLocationParam`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string | null`

              - `type: "search_result_location"`

                - `"search_result_location"`

        - `BetaImageBlockParam`

          - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

            - `BetaBase64ImageSource`

              - `data: string`

              - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                - `"image/jpeg"`

                - `"image/png"`

                - `"image/gif"`

                - `"image/webp"`

              - `type: "base64"`

                - `"base64"`

            - `BetaURLImageSource`

              - `type: "url"`

                - `"url"`

              - `url: string`

            - `BetaFileImageSource`

              - `file_id: string`

              - `type: "file"`

                - `"file"`

          - `type: "image"`

            - `"image"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `BetaSearchResultBlockParam`

          - `content: Array<BetaTextBlockParam>`

            - `text: string`

            - `type: "text"`

              - `"text"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `citations?: Array<BetaTextCitationParam> | null`

              - `BetaCitationCharLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_char_index: number`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `BetaCitationPageLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_page_number: number`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `BetaCitationContentBlockLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_block_index: number`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `BetaCitationWebSearchResultLocationParam`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string | null`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `BetaCitationSearchResultLocationParam`

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

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `citations?: BetaCitationsConfigParam`

            - `enabled?: boolean`

        - `BetaRequestDocumentBlock`

          - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

            - `BetaBase64PDFSource`

              - `data: string`

              - `media_type: "application/pdf"`

                - `"application/pdf"`

              - `type: "base64"`

                - `"base64"`

            - `BetaPlainTextSource`

              - `data: string`

              - `media_type: "text/plain"`

                - `"text/plain"`

              - `type: "text"`

                - `"text"`

            - `BetaContentBlockSource`

              - `content: string | Array<BetaContentBlockSourceContent>`

                - `string`

                - `Array<BetaContentBlockSourceContent>`

                  - `BetaTextBlockParam`

                    - `text: string`

                    - `type: "text"`

                      - `"text"`

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

                    - `citations?: Array<BetaTextCitationParam> | null`

                      - `BetaCitationCharLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_char_index: number`

                        - `start_char_index: number`

                        - `type: "char_location"`

                          - `"char_location"`

                      - `BetaCitationPageLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_page_number: number`

                        - `start_page_number: number`

                        - `type: "page_location"`

                          - `"page_location"`

                      - `BetaCitationContentBlockLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_block_index: number`

                        - `start_block_index: number`

                        - `type: "content_block_location"`

                          - `"content_block_location"`

                      - `BetaCitationWebSearchResultLocationParam`

                        - `cited_text: string`

                        - `encrypted_index: string`

                        - `title: string | null`

                        - `type: "web_search_result_location"`

                          - `"web_search_result_location"`

                        - `url: string`

                      - `BetaCitationSearchResultLocationParam`

                        - `cited_text: string`

                        - `end_block_index: number`

                        - `search_result_index: number`

                        - `source: string`

                        - `start_block_index: number`

                        - `title: string | null`

                        - `type: "search_result_location"`

                          - `"search_result_location"`

                  - `BetaImageBlockParam`

                    - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                      - `BetaBase64ImageSource`

                        - `data: string`

                        - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                          - `"image/jpeg"`

                          - `"image/png"`

                          - `"image/gif"`

                          - `"image/webp"`

                        - `type: "base64"`

                          - `"base64"`

                      - `BetaURLImageSource`

                        - `type: "url"`

                          - `"url"`

                        - `url: string`

                      - `BetaFileImageSource`

                        - `file_id: string`

                        - `type: "file"`

                          - `"file"`

                    - `type: "image"`

                      - `"image"`

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `BetaURLPDFSource`

              - `type: "url"`

                - `"url"`

              - `url: string`

            - `BetaFileDocumentSource`

              - `file_id: string`

              - `type: "file"`

                - `"file"`

          - `type: "document"`

            - `"document"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `citations?: BetaCitationsConfigParam | null`

            - `enabled?: boolean`

          - `context?: string | null`

          - `title?: string | null`

        - `BetaToolReferenceBlockParam`

          Tool reference block that can be included in tool_result content.

          - `tool_name: string`

          - `type: "tool_reference"`

            - `"tool_reference"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `is_error?: boolean`

  - `BetaServerToolUseBlockParam`

    - `id: string`

    - `input: Record<string, unknown>`

    - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

      - `"web_search"`

      - `"web_fetch"`

      - `"code_execution"`

      - `"bash_code_execution"`

      - `"text_editor_code_execution"`

      - `"tool_search_tool_regex"`

      - `"tool_search_tool_bm25"`

    - `type: "server_tool_use"`

      - `"server_tool_use"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `caller?: BetaDirectCaller | BetaServerToolCaller`

      Tool invocation directly from the model.

      - `BetaDirectCaller`

        Tool invocation directly from the model.

        - `type: "direct"`

          - `"direct"`

      - `BetaServerToolCaller`

        Tool invocation generated by a server-side tool.

        - `tool_id: string`

        - `type: "code_execution_20250825"`

          - `"code_execution_20250825"`

  - `BetaWebSearchToolResultBlockParam`

    - `content: BetaWebSearchToolResultBlockParamContent`

      - `Array<BetaWebSearchResultBlockParam>`

        - `encrypted_content: string`

        - `title: string`

        - `type: "web_search_result"`

          - `"web_search_result"`

        - `url: string`

        - `page_age?: string | null`

      - `BetaWebSearchToolRequestError`

        - `error_code: BetaWebSearchToolResultErrorCode`

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

    - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `BetaWebFetchToolResultBlockParam`

    - `content: BetaWebFetchToolResultErrorBlockParam | BetaWebFetchBlockParam`

      - `BetaWebFetchToolResultErrorBlockParam`

        - `error_code: BetaWebFetchToolResultErrorCode`

          - `"invalid_tool_input"`

          - `"url_too_long"`

          - `"url_not_allowed"`

          - `"url_not_accessible"`

          - `"unsupported_content_type"`

          - `"too_many_requests"`

          - `"max_uses_exceeded"`

          - `"unavailable"`

        - `type: "web_fetch_tool_result_error"`

          - `"web_fetch_tool_result_error"`

      - `BetaWebFetchBlockParam`

        - `content: BetaRequestDocumentBlock`

          - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

            - `BetaBase64PDFSource`

              - `data: string`

              - `media_type: "application/pdf"`

                - `"application/pdf"`

              - `type: "base64"`

                - `"base64"`

            - `BetaPlainTextSource`

              - `data: string`

              - `media_type: "text/plain"`

                - `"text/plain"`

              - `type: "text"`

                - `"text"`

            - `BetaContentBlockSource`

              - `content: string | Array<BetaContentBlockSourceContent>`

                - `string`

                - `Array<BetaContentBlockSourceContent>`

                  - `BetaTextBlockParam`

                    - `text: string`

                    - `type: "text"`

                      - `"text"`

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

                    - `citations?: Array<BetaTextCitationParam> | null`

                      - `BetaCitationCharLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_char_index: number`

                        - `start_char_index: number`

                        - `type: "char_location"`

                          - `"char_location"`

                      - `BetaCitationPageLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_page_number: number`

                        - `start_page_number: number`

                        - `type: "page_location"`

                          - `"page_location"`

                      - `BetaCitationContentBlockLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_block_index: number`

                        - `start_block_index: number`

                        - `type: "content_block_location"`

                          - `"content_block_location"`

                      - `BetaCitationWebSearchResultLocationParam`

                        - `cited_text: string`

                        - `encrypted_index: string`

                        - `title: string | null`

                        - `type: "web_search_result_location"`

                          - `"web_search_result_location"`

                        - `url: string`

                      - `BetaCitationSearchResultLocationParam`

                        - `cited_text: string`

                        - `end_block_index: number`

                        - `search_result_index: number`

                        - `source: string`

                        - `start_block_index: number`

                        - `title: string | null`

                        - `type: "search_result_location"`

                          - `"search_result_location"`

                  - `BetaImageBlockParam`

                    - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                      - `BetaBase64ImageSource`

                        - `data: string`

                        - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                          - `"image/jpeg"`

                          - `"image/png"`

                          - `"image/gif"`

                          - `"image/webp"`

                        - `type: "base64"`

                          - `"base64"`

                      - `BetaURLImageSource`

                        - `type: "url"`

                          - `"url"`

                        - `url: string`

                      - `BetaFileImageSource`

                        - `file_id: string`

                        - `type: "file"`

                          - `"file"`

                    - `type: "image"`

                      - `"image"`

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `BetaURLPDFSource`

              - `type: "url"`

                - `"url"`

              - `url: string`

            - `BetaFileDocumentSource`

              - `file_id: string`

              - `type: "file"`

                - `"file"`

          - `type: "document"`

            - `"document"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `citations?: BetaCitationsConfigParam | null`

            - `enabled?: boolean`

          - `context?: string | null`

          - `title?: string | null`

        - `type: "web_fetch_result"`

          - `"web_fetch_result"`

        - `url: string`

          Fetched content URL

        - `retrieved_at?: string | null`

          ISO 8601 timestamp when the content was retrieved

    - `tool_use_id: string`

    - `type: "web_fetch_tool_result"`

      - `"web_fetch_tool_result"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `BetaCodeExecutionToolResultBlockParam`

    - `content: BetaCodeExecutionToolResultBlockParamContent`

      - `BetaCodeExecutionToolResultErrorParam`

        - `error_code: BetaCodeExecutionToolResultErrorCode`

          - `"invalid_tool_input"`

          - `"unavailable"`

          - `"too_many_requests"`

          - `"execution_time_exceeded"`

        - `type: "code_execution_tool_result_error"`

          - `"code_execution_tool_result_error"`

      - `BetaCodeExecutionResultBlockParam`

        - `content: Array<BetaCodeExecutionOutputBlockParam>`

          - `file_id: string`

          - `type: "code_execution_output"`

            - `"code_execution_output"`

        - `return_code: number`

        - `stderr: string`

        - `stdout: string`

        - `type: "code_execution_result"`

          - `"code_execution_result"`

    - `tool_use_id: string`

    - `type: "code_execution_tool_result"`

      - `"code_execution_tool_result"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `BetaBashCodeExecutionToolResultBlockParam`

    - `content: BetaBashCodeExecutionToolResultErrorParam | BetaBashCodeExecutionResultBlockParam`

      - `BetaBashCodeExecutionToolResultErrorParam`

        - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

          - `"invalid_tool_input"`

          - `"unavailable"`

          - `"too_many_requests"`

          - `"execution_time_exceeded"`

          - `"output_file_too_large"`

        - `type: "bash_code_execution_tool_result_error"`

          - `"bash_code_execution_tool_result_error"`

      - `BetaBashCodeExecutionResultBlockParam`

        - `content: Array<BetaBashCodeExecutionOutputBlockParam>`

          - `file_id: string`

          - `type: "bash_code_execution_output"`

            - `"bash_code_execution_output"`

        - `return_code: number`

        - `stderr: string`

        - `stdout: string`

        - `type: "bash_code_execution_result"`

          - `"bash_code_execution_result"`

    - `tool_use_id: string`

    - `type: "bash_code_execution_tool_result"`

      - `"bash_code_execution_tool_result"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `BetaTextEditorCodeExecutionToolResultBlockParam`

    - `content: BetaTextEditorCodeExecutionToolResultErrorParam | BetaTextEditorCodeExecutionViewResultBlockParam | BetaTextEditorCodeExecutionCreateResultBlockParam | BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

      - `BetaTextEditorCodeExecutionToolResultErrorParam`

        - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

          - `"invalid_tool_input"`

          - `"unavailable"`

          - `"too_many_requests"`

          - `"execution_time_exceeded"`

          - `"file_not_found"`

        - `type: "text_editor_code_execution_tool_result_error"`

          - `"text_editor_code_execution_tool_result_error"`

        - `error_message?: string | null`

      - `BetaTextEditorCodeExecutionViewResultBlockParam`

        - `content: string`

        - `file_type: "text" | "image" | "pdf"`

          - `"text"`

          - `"image"`

          - `"pdf"`

        - `type: "text_editor_code_execution_view_result"`

          - `"text_editor_code_execution_view_result"`

        - `num_lines?: number | null`

        - `start_line?: number | null`

        - `total_lines?: number | null`

      - `BetaTextEditorCodeExecutionCreateResultBlockParam`

        - `is_file_update: boolean`

        - `type: "text_editor_code_execution_create_result"`

          - `"text_editor_code_execution_create_result"`

      - `BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

        - `type: "text_editor_code_execution_str_replace_result"`

          - `"text_editor_code_execution_str_replace_result"`

        - `lines?: Array<string> | null`

        - `new_lines?: number | null`

        - `new_start?: number | null`

        - `old_lines?: number | null`

        - `old_start?: number | null`

    - `tool_use_id: string`

    - `type: "text_editor_code_execution_tool_result"`

      - `"text_editor_code_execution_tool_result"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `BetaToolSearchToolResultBlockParam`

    - `content: BetaToolSearchToolResultErrorParam | BetaToolSearchToolSearchResultBlockParam`

      - `BetaToolSearchToolResultErrorParam`

        - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

          - `"invalid_tool_input"`

          - `"unavailable"`

          - `"too_many_requests"`

          - `"execution_time_exceeded"`

        - `type: "tool_search_tool_result_error"`

          - `"tool_search_tool_result_error"`

      - `BetaToolSearchToolSearchResultBlockParam`

        - `tool_references: Array<BetaToolReferenceBlockParam>`

          - `tool_name: string`

          - `type: "tool_reference"`

            - `"tool_reference"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `type: "tool_search_tool_search_result"`

          - `"tool_search_tool_search_result"`

    - `tool_use_id: string`

    - `type: "tool_search_tool_result"`

      - `"tool_search_tool_result"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `BetaMCPToolUseBlockParam`

    - `id: string`

    - `input: Record<string, unknown>`

    - `name: string`

    - `server_name: string`

      The name of the MCP server

    - `type: "mcp_tool_use"`

      - `"mcp_tool_use"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `BetaRequestMCPToolResultBlockParam`

    - `tool_use_id: string`

    - `type: "mcp_tool_result"`

      - `"mcp_tool_result"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `content?: string | Array<BetaTextBlockParam>`

      - `string`

      - `Array<BetaTextBlockParam>`

        - `text: string`

        - `type: "text"`

          - `"text"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `citations?: Array<BetaTextCitationParam> | null`

          - `BetaCitationCharLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_char_index: number`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `BetaCitationPageLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_page_number: number`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `BetaCitationContentBlockLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_block_index: number`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `BetaCitationWebSearchResultLocationParam`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string | null`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `BetaCitationSearchResultLocationParam`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string | null`

            - `type: "search_result_location"`

              - `"search_result_location"`

    - `is_error?: boolean`

  - `BetaContainerUploadBlockParam`

    A content block that represents a file to be uploaded to the container
    Files uploaded via this block will be available in the container's input directory.

    - `file_id: string`

    - `type: "container_upload"`

      - `"container_upload"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta Content Block Source

- `BetaContentBlockSource`

  - `content: string | Array<BetaContentBlockSourceContent>`

    - `string`

    - `Array<BetaContentBlockSourceContent>`

      - `BetaTextBlockParam`

        - `text: string`

        - `type: "text"`

          - `"text"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `citations?: Array<BetaTextCitationParam> | null`

          - `BetaCitationCharLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_char_index: number`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `BetaCitationPageLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_page_number: number`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `BetaCitationContentBlockLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_block_index: number`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `BetaCitationWebSearchResultLocationParam`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string | null`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `BetaCitationSearchResultLocationParam`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string | null`

            - `type: "search_result_location"`

              - `"search_result_location"`

      - `BetaImageBlockParam`

        - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

          - `BetaBase64ImageSource`

            - `data: string`

            - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

              - `"image/jpeg"`

              - `"image/png"`

              - `"image/gif"`

              - `"image/webp"`

            - `type: "base64"`

              - `"base64"`

          - `BetaURLImageSource`

            - `type: "url"`

              - `"url"`

            - `url: string`

          - `BetaFileImageSource`

            - `file_id: string`

            - `type: "file"`

              - `"file"`

        - `type: "image"`

          - `"image"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta Content Block Source Content

- `BetaContentBlockSourceContent = BetaTextBlockParam | BetaImageBlockParam`

  - `BetaTextBlockParam`

    - `text: string`

    - `type: "text"`

      - `"text"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `citations?: Array<BetaTextCitationParam> | null`

      - `BetaCitationCharLocationParam`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_char_index: number`

        - `start_char_index: number`

        - `type: "char_location"`

          - `"char_location"`

      - `BetaCitationPageLocationParam`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_page_number: number`

        - `start_page_number: number`

        - `type: "page_location"`

          - `"page_location"`

      - `BetaCitationContentBlockLocationParam`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_block_index: number`

        - `start_block_index: number`

        - `type: "content_block_location"`

          - `"content_block_location"`

      - `BetaCitationWebSearchResultLocationParam`

        - `cited_text: string`

        - `encrypted_index: string`

        - `title: string | null`

        - `type: "web_search_result_location"`

          - `"web_search_result_location"`

        - `url: string`

      - `BetaCitationSearchResultLocationParam`

        - `cited_text: string`

        - `end_block_index: number`

        - `search_result_index: number`

        - `source: string`

        - `start_block_index: number`

        - `title: string | null`

        - `type: "search_result_location"`

          - `"search_result_location"`

  - `BetaImageBlockParam`

    - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

      - `BetaBase64ImageSource`

        - `data: string`

        - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

          - `"image/jpeg"`

          - `"image/png"`

          - `"image/gif"`

          - `"image/webp"`

        - `type: "base64"`

          - `"base64"`

      - `BetaURLImageSource`

        - `type: "url"`

          - `"url"`

        - `url: string`

      - `BetaFileImageSource`

        - `file_id: string`

        - `type: "file"`

          - `"file"`

    - `type: "image"`

      - `"image"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta Context Management Config

- `BetaContextManagementConfig`

  - `edits?: Array<BetaClearToolUses20250919Edit | BetaClearThinking20251015Edit>`

    List of context management edits to apply

    - `BetaClearToolUses20250919Edit`

      - `type: "clear_tool_uses_20250919"`

        - `"clear_tool_uses_20250919"`

      - `clear_at_least?: BetaInputTokensClearAtLeast | null`

        Minimum number of tokens that must be cleared when triggered. Context will only be modified if at least this many tokens can be removed.

        - `type: "input_tokens"`

          - `"input_tokens"`

        - `value: number`

      - `clear_tool_inputs?: boolean | Array<string> | null`

        Whether to clear all tool inputs (bool) or specific tool inputs to clear (list)

        - `boolean`

        - `Array<string>`

      - `exclude_tools?: Array<string> | null`

        Tool names whose uses are preserved from clearing

      - `keep?: BetaToolUsesKeep`

        Number of tool uses to retain in the conversation

        - `type: "tool_uses"`

          - `"tool_uses"`

        - `value: number`

      - `trigger?: BetaInputTokensTrigger | BetaToolUsesTrigger`

        Condition that triggers the context management strategy

        - `BetaInputTokensTrigger`

          - `type: "input_tokens"`

            - `"input_tokens"`

          - `value: number`

        - `BetaToolUsesTrigger`

          - `type: "tool_uses"`

            - `"tool_uses"`

          - `value: number`

    - `BetaClearThinking20251015Edit`

      - `type: "clear_thinking_20251015"`

        - `"clear_thinking_20251015"`

      - `keep?: BetaThinkingTurns | BetaAllThinkingTurns | "all"`

        Number of most recent assistant turns to keep thinking blocks for. Older turns will have their thinking blocks removed.

        - `BetaThinkingTurns`

          - `type: "thinking_turns"`

            - `"thinking_turns"`

          - `value: number`

        - `BetaAllThinkingTurns`

          - `type: "all"`

            - `"all"`

        - `"all"`

          - `"all"`

### Beta Context Management Response

- `BetaContextManagementResponse`

  - `applied_edits: Array<BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse>`

    List of context management edits that were applied.

    - `BetaClearToolUses20250919EditResponse`

      - `cleared_input_tokens: number`

        Number of input tokens cleared by this edit.

      - `cleared_tool_uses: number`

        Number of tool uses that were cleared.

      - `type: "clear_tool_uses_20250919"`

        The type of context management edit applied.

        - `"clear_tool_uses_20250919"`

    - `BetaClearThinking20251015EditResponse`

      - `cleared_input_tokens: number`

        Number of input tokens cleared by this edit.

      - `cleared_thinking_turns: number`

        Number of thinking turns that were cleared.

      - `type: "clear_thinking_20251015"`

        The type of context management edit applied.

        - `"clear_thinking_20251015"`

### Beta Count Tokens Context Management Response

- `BetaCountTokensContextManagementResponse`

  - `original_input_tokens: number`

    The original token count before context management was applied

### Beta Direct Caller

- `BetaDirectCaller`

  Tool invocation directly from the model.

  - `type: "direct"`

    - `"direct"`

### Beta Document Block

- `BetaDocumentBlock`

  - `citations: BetaCitationConfig | null`

    Citation configuration for the document

    - `enabled: boolean`

  - `source: BetaBase64PDFSource | BetaPlainTextSource`

    - `BetaBase64PDFSource`

      - `data: string`

      - `media_type: "application/pdf"`

        - `"application/pdf"`

      - `type: "base64"`

        - `"base64"`

    - `BetaPlainTextSource`

      - `data: string`

      - `media_type: "text/plain"`

        - `"text/plain"`

      - `type: "text"`

        - `"text"`

  - `title: string | null`

    The title of the document

  - `type: "document"`

    - `"document"`

### Beta File Document Source

- `BetaFileDocumentSource`

  - `file_id: string`

  - `type: "file"`

    - `"file"`

### Beta File Image Source

- `BetaFileImageSource`

  - `file_id: string`

  - `type: "file"`

    - `"file"`

### Beta Image Block Param

- `BetaImageBlockParam`

  - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

    - `BetaBase64ImageSource`

      - `data: string`

      - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

        - `"image/jpeg"`

        - `"image/png"`

        - `"image/gif"`

        - `"image/webp"`

      - `type: "base64"`

        - `"base64"`

    - `BetaURLImageSource`

      - `type: "url"`

        - `"url"`

      - `url: string`

    - `BetaFileImageSource`

      - `file_id: string`

      - `type: "file"`

        - `"file"`

  - `type: "image"`

    - `"image"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta Input JSON Delta

- `BetaInputJSONDelta`

  - `partial_json: string`

  - `type: "input_json_delta"`

    - `"input_json_delta"`

### Beta Input Tokens Clear At Least

- `BetaInputTokensClearAtLeast`

  - `type: "input_tokens"`

    - `"input_tokens"`

  - `value: number`

### Beta Input Tokens Trigger

- `BetaInputTokensTrigger`

  - `type: "input_tokens"`

    - `"input_tokens"`

  - `value: number`

### Beta JSON Output Format

- `BetaJSONOutputFormat`

  - `schema: Record<string, unknown>`

    The JSON schema of the format

  - `type: "json_schema"`

    - `"json_schema"`

### Beta MCP Tool Config

- `BetaMCPToolConfig`

  Configuration for a specific tool in an MCP toolset.

  - `defer_loading?: boolean`

  - `enabled?: boolean`

### Beta MCP Tool Default Config

- `BetaMCPToolDefaultConfig`

  Default configuration for tools in an MCP toolset.

  - `defer_loading?: boolean`

  - `enabled?: boolean`

### Beta MCP Tool Result Block

- `BetaMCPToolResultBlock`

  - `content: string | Array<BetaTextBlock>`

    - `string`

    - `Array<BetaTextBlock>`

      - `citations: Array<BetaTextCitation> | null`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `BetaCitationCharLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_char_index: number`

          - `file_id: string | null`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `BetaCitationPageLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_page_number: number`

          - `file_id: string | null`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `BetaCitationContentBlockLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_block_index: number`

          - `file_id: string | null`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `BetaCitationsWebSearchResultLocation`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string | null`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `BetaCitationSearchResultLocation`

          - `cited_text: string`

          - `end_block_index: number`

          - `search_result_index: number`

          - `source: string`

          - `start_block_index: number`

          - `title: string | null`

          - `type: "search_result_location"`

            - `"search_result_location"`

      - `text: string`

      - `type: "text"`

        - `"text"`

  - `is_error: boolean`

  - `tool_use_id: string`

  - `type: "mcp_tool_result"`

    - `"mcp_tool_result"`

### Beta MCP Tool Use Block

- `BetaMCPToolUseBlock`

  - `id: string`

  - `input: Record<string, unknown>`

  - `name: string`

    The name of the MCP tool

  - `server_name: string`

    The name of the MCP server

  - `type: "mcp_tool_use"`

    - `"mcp_tool_use"`

### Beta MCP Tool Use Block Param

- `BetaMCPToolUseBlockParam`

  - `id: string`

  - `input: Record<string, unknown>`

  - `name: string`

  - `server_name: string`

    The name of the MCP server

  - `type: "mcp_tool_use"`

    - `"mcp_tool_use"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta MCP Toolset

- `BetaMCPToolset`

  Configuration for a group of tools from an MCP server.

  Allows configuring enabled status and defer_loading for all tools
  from an MCP server, with optional per-tool overrides.

  - `mcp_server_name: string`

    Name of the MCP server to configure tools for

  - `type: "mcp_toolset"`

    - `"mcp_toolset"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `configs?: Record<string, BetaMCPToolConfig> | null`

    Configuration overrides for specific tools, keyed by tool name

    - `defer_loading?: boolean`

    - `enabled?: boolean`

  - `default_config?: BetaMCPToolDefaultConfig`

    Default configuration applied to all tools from this server

    - `defer_loading?: boolean`

    - `enabled?: boolean`

### Beta Memory Tool 20250818

- `BetaMemoryTool20250818`

  - `name: "memory"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"memory"`

  - `type: "memory_20250818"`

    - `"memory_20250818"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `input_examples?: Array<Record<string, unknown>>`

  - `strict?: boolean`

### Beta Memory Tool 20250818 Command

- `BetaMemoryTool20250818Command = BetaMemoryTool20250818ViewCommand | BetaMemoryTool20250818CreateCommand | BetaMemoryTool20250818StrReplaceCommand | 3 more`

  - `BetaMemoryTool20250818ViewCommand`

    - `command: "view"`

      Command type identifier

      - `"view"`

    - `path: string`

      Path to directory or file to view

    - `view_range?: Array<number>`

      Optional line range for viewing specific lines

  - `BetaMemoryTool20250818CreateCommand`

    - `command: "create"`

      Command type identifier

      - `"create"`

    - `file_text: string`

      Content to write to the file

    - `path: string`

      Path where the file should be created

  - `BetaMemoryTool20250818StrReplaceCommand`

    - `command: "str_replace"`

      Command type identifier

      - `"str_replace"`

    - `new_str: string`

      Text to replace with

    - `old_str: string`

      Text to search for and replace

    - `path: string`

      Path to the file where text should be replaced

  - `BetaMemoryTool20250818InsertCommand`

    - `command: "insert"`

      Command type identifier

      - `"insert"`

    - `insert_line: number`

      Line number where text should be inserted

    - `insert_text: string`

      Text to insert at the specified line

    - `path: string`

      Path to the file where text should be inserted

  - `BetaMemoryTool20250818DeleteCommand`

    - `command: "delete"`

      Command type identifier

      - `"delete"`

    - `path: string`

      Path to the file or directory to delete

  - `BetaMemoryTool20250818RenameCommand`

    - `command: "rename"`

      Command type identifier

      - `"rename"`

    - `new_path: string`

      New path for the file or directory

    - `old_path: string`

      Current path of the file or directory

### Beta Memory Tool 20250818 Create Command

- `BetaMemoryTool20250818CreateCommand`

  - `command: "create"`

    Command type identifier

    - `"create"`

  - `file_text: string`

    Content to write to the file

  - `path: string`

    Path where the file should be created

### Beta Memory Tool 20250818 Delete Command

- `BetaMemoryTool20250818DeleteCommand`

  - `command: "delete"`

    Command type identifier

    - `"delete"`

  - `path: string`

    Path to the file or directory to delete

### Beta Memory Tool 20250818 Insert Command

- `BetaMemoryTool20250818InsertCommand`

  - `command: "insert"`

    Command type identifier

    - `"insert"`

  - `insert_line: number`

    Line number where text should be inserted

  - `insert_text: string`

    Text to insert at the specified line

  - `path: string`

    Path to the file where text should be inserted

### Beta Memory Tool 20250818 Rename Command

- `BetaMemoryTool20250818RenameCommand`

  - `command: "rename"`

    Command type identifier

    - `"rename"`

  - `new_path: string`

    New path for the file or directory

  - `old_path: string`

    Current path of the file or directory

### Beta Memory Tool 20250818 Str Replace Command

- `BetaMemoryTool20250818StrReplaceCommand`

  - `command: "str_replace"`

    Command type identifier

    - `"str_replace"`

  - `new_str: string`

    Text to replace with

  - `old_str: string`

    Text to search for and replace

  - `path: string`

    Path to the file where text should be replaced

### Beta Memory Tool 20250818 View Command

- `BetaMemoryTool20250818ViewCommand`

  - `command: "view"`

    Command type identifier

    - `"view"`

  - `path: string`

    Path to directory or file to view

  - `view_range?: Array<number>`

    Optional line range for viewing specific lines

### Beta Message

- `BetaMessage`

  - `id: string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `container: BetaContainer | null`

    Information about the container used in the request (for the code execution tool)

    - `id: string`

      Identifier for the container used in this request

    - `expires_at: string`

      The time at which the container will expire.

    - `skills: Array<BetaSkill> | null`

      Skills loaded in the container

      - `skill_id: string`

        Skill ID

      - `type: "anthropic" | "custom"`

        Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

        - `"anthropic"`

        - `"custom"`

      - `version: string`

        Skill version or 'latest' for most recent version

  - `content: Array<BetaContentBlock>`

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

    - `BetaTextBlock`

      - `citations: Array<BetaTextCitation> | null`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `BetaCitationCharLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_char_index: number`

          - `file_id: string | null`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `BetaCitationPageLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_page_number: number`

          - `file_id: string | null`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `BetaCitationContentBlockLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_block_index: number`

          - `file_id: string | null`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `BetaCitationsWebSearchResultLocation`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string | null`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `BetaCitationSearchResultLocation`

          - `cited_text: string`

          - `end_block_index: number`

          - `search_result_index: number`

          - `source: string`

          - `start_block_index: number`

          - `title: string | null`

          - `type: "search_result_location"`

            - `"search_result_location"`

      - `text: string`

      - `type: "text"`

        - `"text"`

    - `BetaThinkingBlock`

      - `signature: string`

      - `thinking: string`

      - `type: "thinking"`

        - `"thinking"`

    - `BetaRedactedThinkingBlock`

      - `data: string`

      - `type: "redacted_thinking"`

        - `"redacted_thinking"`

    - `BetaToolUseBlock`

      - `id: string`

      - `input: Record<string, unknown>`

      - `name: string`

      - `type: "tool_use"`

        - `"tool_use"`

      - `caller?: BetaDirectCaller | BetaServerToolCaller`

        Tool invocation directly from the model.

        - `BetaDirectCaller`

          Tool invocation directly from the model.

          - `type: "direct"`

            - `"direct"`

        - `BetaServerToolCaller`

          Tool invocation generated by a server-side tool.

          - `tool_id: string`

          - `type: "code_execution_20250825"`

            - `"code_execution_20250825"`

    - `BetaServerToolUseBlock`

      - `id: string`

      - `caller: BetaDirectCaller | BetaServerToolCaller`

        Tool invocation directly from the model.

        - `BetaDirectCaller`

          Tool invocation directly from the model.

          - `type: "direct"`

            - `"direct"`

        - `BetaServerToolCaller`

          Tool invocation generated by a server-side tool.

          - `tool_id: string`

          - `type: "code_execution_20250825"`

            - `"code_execution_20250825"`

      - `input: Record<string, unknown>`

      - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

        - `"web_search"`

        - `"web_fetch"`

        - `"code_execution"`

        - `"bash_code_execution"`

        - `"text_editor_code_execution"`

        - `"tool_search_tool_regex"`

        - `"tool_search_tool_bm25"`

      - `type: "server_tool_use"`

        - `"server_tool_use"`

    - `BetaWebSearchToolResultBlock`

      - `content: BetaWebSearchToolResultBlockContent`

        - `BetaWebSearchToolResultError`

          - `error_code: BetaWebSearchToolResultErrorCode`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"max_uses_exceeded"`

            - `"too_many_requests"`

            - `"query_too_long"`

          - `type: "web_search_tool_result_error"`

            - `"web_search_tool_result_error"`

        - `Array<BetaWebSearchResultBlock>`

          - `encrypted_content: string`

          - `page_age: string | null`

          - `title: string`

          - `type: "web_search_result"`

            - `"web_search_result"`

          - `url: string`

      - `tool_use_id: string`

      - `type: "web_search_tool_result"`

        - `"web_search_tool_result"`

    - `BetaWebFetchToolResultBlock`

      - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

        - `BetaWebFetchToolResultErrorBlock`

          - `error_code: BetaWebFetchToolResultErrorCode`

            - `"invalid_tool_input"`

            - `"url_too_long"`

            - `"url_not_allowed"`

            - `"url_not_accessible"`

            - `"unsupported_content_type"`

            - `"too_many_requests"`

            - `"max_uses_exceeded"`

            - `"unavailable"`

          - `type: "web_fetch_tool_result_error"`

            - `"web_fetch_tool_result_error"`

        - `BetaWebFetchBlock`

          - `content: BetaDocumentBlock`

            - `citations: BetaCitationConfig | null`

              Citation configuration for the document

              - `enabled: boolean`

            - `source: BetaBase64PDFSource | BetaPlainTextSource`

              - `BetaBase64PDFSource`

                - `data: string`

                - `media_type: "application/pdf"`

                  - `"application/pdf"`

                - `type: "base64"`

                  - `"base64"`

              - `BetaPlainTextSource`

                - `data: string`

                - `media_type: "text/plain"`

                  - `"text/plain"`

                - `type: "text"`

                  - `"text"`

            - `title: string | null`

              The title of the document

            - `type: "document"`

              - `"document"`

          - `retrieved_at: string | null`

            ISO 8601 timestamp when the content was retrieved

          - `type: "web_fetch_result"`

            - `"web_fetch_result"`

          - `url: string`

            Fetched content URL

      - `tool_use_id: string`

      - `type: "web_fetch_tool_result"`

        - `"web_fetch_tool_result"`

    - `BetaCodeExecutionToolResultBlock`

      - `content: BetaCodeExecutionToolResultBlockContent`

        - `BetaCodeExecutionToolResultError`

          - `error_code: BetaCodeExecutionToolResultErrorCode`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

          - `type: "code_execution_tool_result_error"`

            - `"code_execution_tool_result_error"`

        - `BetaCodeExecutionResultBlock`

          - `content: Array<BetaCodeExecutionOutputBlock>`

            - `file_id: string`

            - `type: "code_execution_output"`

              - `"code_execution_output"`

          - `return_code: number`

          - `stderr: string`

          - `stdout: string`

          - `type: "code_execution_result"`

            - `"code_execution_result"`

      - `tool_use_id: string`

      - `type: "code_execution_tool_result"`

        - `"code_execution_tool_result"`

    - `BetaBashCodeExecutionToolResultBlock`

      - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

        - `BetaBashCodeExecutionToolResultError`

          - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

            - `"output_file_too_large"`

          - `type: "bash_code_execution_tool_result_error"`

            - `"bash_code_execution_tool_result_error"`

        - `BetaBashCodeExecutionResultBlock`

          - `content: Array<BetaBashCodeExecutionOutputBlock>`

            - `file_id: string`

            - `type: "bash_code_execution_output"`

              - `"bash_code_execution_output"`

          - `return_code: number`

          - `stderr: string`

          - `stdout: string`

          - `type: "bash_code_execution_result"`

            - `"bash_code_execution_result"`

      - `tool_use_id: string`

      - `type: "bash_code_execution_tool_result"`

        - `"bash_code_execution_tool_result"`

    - `BetaTextEditorCodeExecutionToolResultBlock`

      - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

        - `BetaTextEditorCodeExecutionToolResultError`

          - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

            - `"file_not_found"`

          - `error_message: string | null`

          - `type: "text_editor_code_execution_tool_result_error"`

            - `"text_editor_code_execution_tool_result_error"`

        - `BetaTextEditorCodeExecutionViewResultBlock`

          - `content: string`

          - `file_type: "text" | "image" | "pdf"`

            - `"text"`

            - `"image"`

            - `"pdf"`

          - `num_lines: number | null`

          - `start_line: number | null`

          - `total_lines: number | null`

          - `type: "text_editor_code_execution_view_result"`

            - `"text_editor_code_execution_view_result"`

        - `BetaTextEditorCodeExecutionCreateResultBlock`

          - `is_file_update: boolean`

          - `type: "text_editor_code_execution_create_result"`

            - `"text_editor_code_execution_create_result"`

        - `BetaTextEditorCodeExecutionStrReplaceResultBlock`

          - `lines: Array<string> | null`

          - `new_lines: number | null`

          - `new_start: number | null`

          - `old_lines: number | null`

          - `old_start: number | null`

          - `type: "text_editor_code_execution_str_replace_result"`

            - `"text_editor_code_execution_str_replace_result"`

      - `tool_use_id: string`

      - `type: "text_editor_code_execution_tool_result"`

        - `"text_editor_code_execution_tool_result"`

    - `BetaToolSearchToolResultBlock`

      - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

        - `BetaToolSearchToolResultError`

          - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

          - `error_message: string | null`

          - `type: "tool_search_tool_result_error"`

            - `"tool_search_tool_result_error"`

        - `BetaToolSearchToolSearchResultBlock`

          - `tool_references: Array<BetaToolReferenceBlock>`

            - `tool_name: string`

            - `type: "tool_reference"`

              - `"tool_reference"`

          - `type: "tool_search_tool_search_result"`

            - `"tool_search_tool_search_result"`

      - `tool_use_id: string`

      - `type: "tool_search_tool_result"`

        - `"tool_search_tool_result"`

    - `BetaMCPToolUseBlock`

      - `id: string`

      - `input: Record<string, unknown>`

      - `name: string`

        The name of the MCP tool

      - `server_name: string`

        The name of the MCP server

      - `type: "mcp_tool_use"`

        - `"mcp_tool_use"`

    - `BetaMCPToolResultBlock`

      - `content: string | Array<BetaTextBlock>`

        - `string`

        - `Array<BetaTextBlock>`

          - `citations: Array<BetaTextCitation> | null`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `BetaCitationCharLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_char_index: number`

              - `file_id: string | null`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `BetaCitationPageLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_page_number: number`

              - `file_id: string | null`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `BetaCitationContentBlockLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_block_index: number`

              - `file_id: string | null`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `BetaCitationsWebSearchResultLocation`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string | null`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `BetaCitationSearchResultLocation`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string | null`

              - `type: "search_result_location"`

                - `"search_result_location"`

          - `text: string`

          - `type: "text"`

            - `"text"`

      - `is_error: boolean`

      - `tool_use_id: string`

      - `type: "mcp_tool_result"`

        - `"mcp_tool_result"`

    - `BetaContainerUploadBlock`

      Response model for a file uploaded to the container.

      - `file_id: string`

      - `type: "container_upload"`

        - `"container_upload"`

  - `context_management: BetaContextManagementResponse | null`

    Context management response.

    Information about context management strategies applied during the request.

    - `applied_edits: Array<BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse>`

      List of context management edits that were applied.

      - `BetaClearToolUses20250919EditResponse`

        - `cleared_input_tokens: number`

          Number of input tokens cleared by this edit.

        - `cleared_tool_uses: number`

          Number of tool uses that were cleared.

        - `type: "clear_tool_uses_20250919"`

          The type of context management edit applied.

          - `"clear_tool_uses_20250919"`

      - `BetaClearThinking20251015EditResponse`

        - `cleared_input_tokens: number`

          Number of input tokens cleared by this edit.

        - `cleared_thinking_turns: number`

          Number of thinking turns that were cleared.

        - `type: "clear_thinking_20251015"`

          The type of context management edit applied.

          - `"clear_thinking_20251015"`

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

  - `role: "assistant"`

    Conversational role of the generated message.

    This will always be `"assistant"`.

    - `"assistant"`

  - `stop_reason: BetaStopReason | null`

    The reason that we stopped.

    This may be one the following values:

    * `"end_turn"`: the model reached a natural stopping point
    * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
    * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
    * `"tool_use"`: the model invoked one or more tools
    * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
    * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

    In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

    - `"end_turn"`

    - `"max_tokens"`

    - `"stop_sequence"`

    - `"tool_use"`

    - `"pause_turn"`

    - `"refusal"`

    - `"model_context_window_exceeded"`

  - `stop_sequence: string | null`

    Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was generated.

  - `type: "message"`

    Object type.

    For Messages, this is always `"message"`.

    - `"message"`

  - `usage: BetaUsage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cache_creation: BetaCacheCreation | null`

      Breakdown of cached tokens by TTL

      - `ephemeral_1h_input_tokens: number`

        The number of input tokens used to create the 1 hour cache entry.

      - `ephemeral_5m_input_tokens: number`

        The number of input tokens used to create the 5 minute cache entry.

    - `cache_creation_input_tokens: number | null`

      The number of input tokens used to create the cache entry.

    - `cache_read_input_tokens: number | null`

      The number of input tokens read from the cache.

    - `input_tokens: number`

      The number of input tokens which were used.

    - `output_tokens: number`

      The number of output tokens which were used.

    - `server_tool_use: BetaServerToolUsage | null`

      The number of server tool requests.

      - `web_fetch_requests: number`

        The number of web fetch tool requests.

      - `web_search_requests: number`

        The number of web search tool requests.

    - `service_tier: "standard" | "priority" | "batch" | null`

      If the request used the priority, standard, or batch tier.

      - `"standard"`

      - `"priority"`

      - `"batch"`

### Beta Message Delta Usage

- `BetaMessageDeltaUsage`

  - `cache_creation_input_tokens: number | null`

    The cumulative number of input tokens used to create the cache entry.

  - `cache_read_input_tokens: number | null`

    The cumulative number of input tokens read from the cache.

  - `input_tokens: number | null`

    The cumulative number of input tokens which were used.

  - `output_tokens: number`

    The cumulative number of output tokens which were used.

  - `server_tool_use: BetaServerToolUsage | null`

    The number of server tool requests.

    - `web_fetch_requests: number`

      The number of web fetch tool requests.

    - `web_search_requests: number`

      The number of web search tool requests.

### Beta Message Param

- `BetaMessageParam`

  - `content: string | Array<BetaContentBlockParam>`

    - `string`

    - `Array<BetaContentBlockParam>`

      - `BetaTextBlockParam`

        - `text: string`

        - `type: "text"`

          - `"text"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `citations?: Array<BetaTextCitationParam> | null`

          - `BetaCitationCharLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_char_index: number`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `BetaCitationPageLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_page_number: number`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `BetaCitationContentBlockLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_block_index: number`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `BetaCitationWebSearchResultLocationParam`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string | null`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `BetaCitationSearchResultLocationParam`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string | null`

            - `type: "search_result_location"`

              - `"search_result_location"`

      - `BetaImageBlockParam`

        - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

          - `BetaBase64ImageSource`

            - `data: string`

            - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

              - `"image/jpeg"`

              - `"image/png"`

              - `"image/gif"`

              - `"image/webp"`

            - `type: "base64"`

              - `"base64"`

          - `BetaURLImageSource`

            - `type: "url"`

              - `"url"`

            - `url: string`

          - `BetaFileImageSource`

            - `file_id: string`

            - `type: "file"`

              - `"file"`

        - `type: "image"`

          - `"image"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `BetaRequestDocumentBlock`

        - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

          - `BetaBase64PDFSource`

            - `data: string`

            - `media_type: "application/pdf"`

              - `"application/pdf"`

            - `type: "base64"`

              - `"base64"`

          - `BetaPlainTextSource`

            - `data: string`

            - `media_type: "text/plain"`

              - `"text/plain"`

            - `type: "text"`

              - `"text"`

          - `BetaContentBlockSource`

            - `content: string | Array<BetaContentBlockSourceContent>`

              - `string`

              - `Array<BetaContentBlockSourceContent>`

                - `BetaTextBlockParam`

                  - `text: string`

                  - `type: "text"`

                    - `"text"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

                  - `citations?: Array<BetaTextCitationParam> | null`

                    - `BetaCitationCharLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_char_index: number`

                      - `start_char_index: number`

                      - `type: "char_location"`

                        - `"char_location"`

                    - `BetaCitationPageLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_page_number: number`

                      - `start_page_number: number`

                      - `type: "page_location"`

                        - `"page_location"`

                    - `BetaCitationContentBlockLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_block_index: number`

                      - `start_block_index: number`

                      - `type: "content_block_location"`

                        - `"content_block_location"`

                    - `BetaCitationWebSearchResultLocationParam`

                      - `cited_text: string`

                      - `encrypted_index: string`

                      - `title: string | null`

                      - `type: "web_search_result_location"`

                        - `"web_search_result_location"`

                      - `url: string`

                    - `BetaCitationSearchResultLocationParam`

                      - `cited_text: string`

                      - `end_block_index: number`

                      - `search_result_index: number`

                      - `source: string`

                      - `start_block_index: number`

                      - `title: string | null`

                      - `type: "search_result_location"`

                        - `"search_result_location"`

                - `BetaImageBlockParam`

                  - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                    - `BetaBase64ImageSource`

                      - `data: string`

                      - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                        - `"image/jpeg"`

                        - `"image/png"`

                        - `"image/gif"`

                        - `"image/webp"`

                      - `type: "base64"`

                        - `"base64"`

                    - `BetaURLImageSource`

                      - `type: "url"`

                        - `"url"`

                      - `url: string`

                    - `BetaFileImageSource`

                      - `file_id: string`

                      - `type: "file"`

                        - `"file"`

                  - `type: "image"`

                    - `"image"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `BetaURLPDFSource`

            - `type: "url"`

              - `"url"`

            - `url: string`

          - `BetaFileDocumentSource`

            - `file_id: string`

            - `type: "file"`

              - `"file"`

        - `type: "document"`

          - `"document"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `citations?: BetaCitationsConfigParam | null`

          - `enabled?: boolean`

        - `context?: string | null`

        - `title?: string | null`

      - `BetaSearchResultBlockParam`

        - `content: Array<BetaTextBlockParam>`

          - `text: string`

          - `type: "text"`

            - `"text"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `citations?: Array<BetaTextCitationParam> | null`

            - `BetaCitationCharLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_char_index: number`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `BetaCitationPageLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_page_number: number`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `BetaCitationContentBlockLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_block_index: number`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `BetaCitationWebSearchResultLocationParam`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string | null`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `BetaCitationSearchResultLocationParam`

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

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `citations?: BetaCitationsConfigParam`

          - `enabled?: boolean`

      - `BetaThinkingBlockParam`

        - `signature: string`

        - `thinking: string`

        - `type: "thinking"`

          - `"thinking"`

      - `BetaRedactedThinkingBlockParam`

        - `data: string`

        - `type: "redacted_thinking"`

          - `"redacted_thinking"`

      - `BetaToolUseBlockParam`

        - `id: string`

        - `input: Record<string, unknown>`

        - `name: string`

        - `type: "tool_use"`

          - `"tool_use"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `caller?: BetaDirectCaller | BetaServerToolCaller`

          Tool invocation directly from the model.

          - `BetaDirectCaller`

            Tool invocation directly from the model.

            - `type: "direct"`

              - `"direct"`

          - `BetaServerToolCaller`

            Tool invocation generated by a server-side tool.

            - `tool_id: string`

            - `type: "code_execution_20250825"`

              - `"code_execution_20250825"`

      - `BetaToolResultBlockParam`

        - `tool_use_id: string`

        - `type: "tool_result"`

          - `"tool_result"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `content?: string | Array<BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more>`

          - `string`

          - `Array<BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more>`

            - `BetaTextBlockParam`

              - `text: string`

              - `type: "text"`

                - `"text"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `citations?: Array<BetaTextCitationParam> | null`

                - `BetaCitationCharLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_char_index: number`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `BetaCitationPageLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_page_number: number`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `BetaCitationContentBlockLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_block_index: number`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `BetaCitationWebSearchResultLocationParam`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string | null`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `BetaCitationSearchResultLocationParam`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string | null`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

            - `BetaImageBlockParam`

              - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                - `BetaBase64ImageSource`

                  - `data: string`

                  - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                    - `"image/jpeg"`

                    - `"image/png"`

                    - `"image/gif"`

                    - `"image/webp"`

                  - `type: "base64"`

                    - `"base64"`

                - `BetaURLImageSource`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

                - `BetaFileImageSource`

                  - `file_id: string`

                  - `type: "file"`

                    - `"file"`

              - `type: "image"`

                - `"image"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `BetaSearchResultBlockParam`

              - `content: Array<BetaTextBlockParam>`

                - `text: string`

                - `type: "text"`

                  - `"text"`

                - `cache_control?: BetaCacheControlEphemeral | null`

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

                - `citations?: Array<BetaTextCitationParam> | null`

                  - `BetaCitationCharLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_char_index: number`

                    - `start_char_index: number`

                    - `type: "char_location"`

                      - `"char_location"`

                  - `BetaCitationPageLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_page_number: number`

                    - `start_page_number: number`

                    - `type: "page_location"`

                      - `"page_location"`

                  - `BetaCitationContentBlockLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_block_index: number`

                    - `start_block_index: number`

                    - `type: "content_block_location"`

                      - `"content_block_location"`

                  - `BetaCitationWebSearchResultLocationParam`

                    - `cited_text: string`

                    - `encrypted_index: string`

                    - `title: string | null`

                    - `type: "web_search_result_location"`

                      - `"web_search_result_location"`

                    - `url: string`

                  - `BetaCitationSearchResultLocationParam`

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

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `citations?: BetaCitationsConfigParam`

                - `enabled?: boolean`

            - `BetaRequestDocumentBlock`

              - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

                - `BetaBase64PDFSource`

                  - `data: string`

                  - `media_type: "application/pdf"`

                    - `"application/pdf"`

                  - `type: "base64"`

                    - `"base64"`

                - `BetaPlainTextSource`

                  - `data: string`

                  - `media_type: "text/plain"`

                    - `"text/plain"`

                  - `type: "text"`

                    - `"text"`

                - `BetaContentBlockSource`

                  - `content: string | Array<BetaContentBlockSourceContent>`

                    - `string`

                    - `Array<BetaContentBlockSourceContent>`

                      - `BetaTextBlockParam`

                        - `text: string`

                        - `type: "text"`

                          - `"text"`

                        - `cache_control?: BetaCacheControlEphemeral | null`

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

                        - `citations?: Array<BetaTextCitationParam> | null`

                          - `BetaCitationCharLocationParam`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string | null`

                            - `end_char_index: number`

                            - `start_char_index: number`

                            - `type: "char_location"`

                              - `"char_location"`

                          - `BetaCitationPageLocationParam`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string | null`

                            - `end_page_number: number`

                            - `start_page_number: number`

                            - `type: "page_location"`

                              - `"page_location"`

                          - `BetaCitationContentBlockLocationParam`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string | null`

                            - `end_block_index: number`

                            - `start_block_index: number`

                            - `type: "content_block_location"`

                              - `"content_block_location"`

                          - `BetaCitationWebSearchResultLocationParam`

                            - `cited_text: string`

                            - `encrypted_index: string`

                            - `title: string | null`

                            - `type: "web_search_result_location"`

                              - `"web_search_result_location"`

                            - `url: string`

                          - `BetaCitationSearchResultLocationParam`

                            - `cited_text: string`

                            - `end_block_index: number`

                            - `search_result_index: number`

                            - `source: string`

                            - `start_block_index: number`

                            - `title: string | null`

                            - `type: "search_result_location"`

                              - `"search_result_location"`

                      - `BetaImageBlockParam`

                        - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                          - `BetaBase64ImageSource`

                            - `data: string`

                            - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                              - `"image/jpeg"`

                              - `"image/png"`

                              - `"image/gif"`

                              - `"image/webp"`

                            - `type: "base64"`

                              - `"base64"`

                          - `BetaURLImageSource`

                            - `type: "url"`

                              - `"url"`

                            - `url: string`

                          - `BetaFileImageSource`

                            - `file_id: string`

                            - `type: "file"`

                              - `"file"`

                        - `type: "image"`

                          - `"image"`

                        - `cache_control?: BetaCacheControlEphemeral | null`

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

                - `BetaURLPDFSource`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

                - `BetaFileDocumentSource`

                  - `file_id: string`

                  - `type: "file"`

                    - `"file"`

              - `type: "document"`

                - `"document"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `citations?: BetaCitationsConfigParam | null`

                - `enabled?: boolean`

              - `context?: string | null`

              - `title?: string | null`

            - `BetaToolReferenceBlockParam`

              Tool reference block that can be included in tool_result content.

              - `tool_name: string`

              - `type: "tool_reference"`

                - `"tool_reference"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `is_error?: boolean`

      - `BetaServerToolUseBlockParam`

        - `id: string`

        - `input: Record<string, unknown>`

        - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

          - `"web_search"`

          - `"web_fetch"`

          - `"code_execution"`

          - `"bash_code_execution"`

          - `"text_editor_code_execution"`

          - `"tool_search_tool_regex"`

          - `"tool_search_tool_bm25"`

        - `type: "server_tool_use"`

          - `"server_tool_use"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `caller?: BetaDirectCaller | BetaServerToolCaller`

          Tool invocation directly from the model.

          - `BetaDirectCaller`

            Tool invocation directly from the model.

            - `type: "direct"`

              - `"direct"`

          - `BetaServerToolCaller`

            Tool invocation generated by a server-side tool.

            - `tool_id: string`

            - `type: "code_execution_20250825"`

              - `"code_execution_20250825"`

      - `BetaWebSearchToolResultBlockParam`

        - `content: BetaWebSearchToolResultBlockParamContent`

          - `Array<BetaWebSearchResultBlockParam>`

            - `encrypted_content: string`

            - `title: string`

            - `type: "web_search_result"`

              - `"web_search_result"`

            - `url: string`

            - `page_age?: string | null`

          - `BetaWebSearchToolRequestError`

            - `error_code: BetaWebSearchToolResultErrorCode`

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

        - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `BetaWebFetchToolResultBlockParam`

        - `content: BetaWebFetchToolResultErrorBlockParam | BetaWebFetchBlockParam`

          - `BetaWebFetchToolResultErrorBlockParam`

            - `error_code: BetaWebFetchToolResultErrorCode`

              - `"invalid_tool_input"`

              - `"url_too_long"`

              - `"url_not_allowed"`

              - `"url_not_accessible"`

              - `"unsupported_content_type"`

              - `"too_many_requests"`

              - `"max_uses_exceeded"`

              - `"unavailable"`

            - `type: "web_fetch_tool_result_error"`

              - `"web_fetch_tool_result_error"`

          - `BetaWebFetchBlockParam`

            - `content: BetaRequestDocumentBlock`

              - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

                - `BetaBase64PDFSource`

                  - `data: string`

                  - `media_type: "application/pdf"`

                    - `"application/pdf"`

                  - `type: "base64"`

                    - `"base64"`

                - `BetaPlainTextSource`

                  - `data: string`

                  - `media_type: "text/plain"`

                    - `"text/plain"`

                  - `type: "text"`

                    - `"text"`

                - `BetaContentBlockSource`

                  - `content: string | Array<BetaContentBlockSourceContent>`

                    - `string`

                    - `Array<BetaContentBlockSourceContent>`

                      - `BetaTextBlockParam`

                        - `text: string`

                        - `type: "text"`

                          - `"text"`

                        - `cache_control?: BetaCacheControlEphemeral | null`

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

                        - `citations?: Array<BetaTextCitationParam> | null`

                          - `BetaCitationCharLocationParam`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string | null`

                            - `end_char_index: number`

                            - `start_char_index: number`

                            - `type: "char_location"`

                              - `"char_location"`

                          - `BetaCitationPageLocationParam`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string | null`

                            - `end_page_number: number`

                            - `start_page_number: number`

                            - `type: "page_location"`

                              - `"page_location"`

                          - `BetaCitationContentBlockLocationParam`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string | null`

                            - `end_block_index: number`

                            - `start_block_index: number`

                            - `type: "content_block_location"`

                              - `"content_block_location"`

                          - `BetaCitationWebSearchResultLocationParam`

                            - `cited_text: string`

                            - `encrypted_index: string`

                            - `title: string | null`

                            - `type: "web_search_result_location"`

                              - `"web_search_result_location"`

                            - `url: string`

                          - `BetaCitationSearchResultLocationParam`

                            - `cited_text: string`

                            - `end_block_index: number`

                            - `search_result_index: number`

                            - `source: string`

                            - `start_block_index: number`

                            - `title: string | null`

                            - `type: "search_result_location"`

                              - `"search_result_location"`

                      - `BetaImageBlockParam`

                        - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                          - `BetaBase64ImageSource`

                            - `data: string`

                            - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                              - `"image/jpeg"`

                              - `"image/png"`

                              - `"image/gif"`

                              - `"image/webp"`

                            - `type: "base64"`

                              - `"base64"`

                          - `BetaURLImageSource`

                            - `type: "url"`

                              - `"url"`

                            - `url: string`

                          - `BetaFileImageSource`

                            - `file_id: string`

                            - `type: "file"`

                              - `"file"`

                        - `type: "image"`

                          - `"image"`

                        - `cache_control?: BetaCacheControlEphemeral | null`

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

                - `BetaURLPDFSource`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

                - `BetaFileDocumentSource`

                  - `file_id: string`

                  - `type: "file"`

                    - `"file"`

              - `type: "document"`

                - `"document"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `citations?: BetaCitationsConfigParam | null`

                - `enabled?: boolean`

              - `context?: string | null`

              - `title?: string | null`

            - `type: "web_fetch_result"`

              - `"web_fetch_result"`

            - `url: string`

              Fetched content URL

            - `retrieved_at?: string | null`

              ISO 8601 timestamp when the content was retrieved

        - `tool_use_id: string`

        - `type: "web_fetch_tool_result"`

          - `"web_fetch_tool_result"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `BetaCodeExecutionToolResultBlockParam`

        - `content: BetaCodeExecutionToolResultBlockParamContent`

          - `BetaCodeExecutionToolResultErrorParam`

            - `error_code: BetaCodeExecutionToolResultErrorCode`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

            - `type: "code_execution_tool_result_error"`

              - `"code_execution_tool_result_error"`

          - `BetaCodeExecutionResultBlockParam`

            - `content: Array<BetaCodeExecutionOutputBlockParam>`

              - `file_id: string`

              - `type: "code_execution_output"`

                - `"code_execution_output"`

            - `return_code: number`

            - `stderr: string`

            - `stdout: string`

            - `type: "code_execution_result"`

              - `"code_execution_result"`

        - `tool_use_id: string`

        - `type: "code_execution_tool_result"`

          - `"code_execution_tool_result"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `BetaBashCodeExecutionToolResultBlockParam`

        - `content: BetaBashCodeExecutionToolResultErrorParam | BetaBashCodeExecutionResultBlockParam`

          - `BetaBashCodeExecutionToolResultErrorParam`

            - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

              - `"output_file_too_large"`

            - `type: "bash_code_execution_tool_result_error"`

              - `"bash_code_execution_tool_result_error"`

          - `BetaBashCodeExecutionResultBlockParam`

            - `content: Array<BetaBashCodeExecutionOutputBlockParam>`

              - `file_id: string`

              - `type: "bash_code_execution_output"`

                - `"bash_code_execution_output"`

            - `return_code: number`

            - `stderr: string`

            - `stdout: string`

            - `type: "bash_code_execution_result"`

              - `"bash_code_execution_result"`

        - `tool_use_id: string`

        - `type: "bash_code_execution_tool_result"`

          - `"bash_code_execution_tool_result"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `BetaTextEditorCodeExecutionToolResultBlockParam`

        - `content: BetaTextEditorCodeExecutionToolResultErrorParam | BetaTextEditorCodeExecutionViewResultBlockParam | BetaTextEditorCodeExecutionCreateResultBlockParam | BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

          - `BetaTextEditorCodeExecutionToolResultErrorParam`

            - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

              - `"file_not_found"`

            - `type: "text_editor_code_execution_tool_result_error"`

              - `"text_editor_code_execution_tool_result_error"`

            - `error_message?: string | null`

          - `BetaTextEditorCodeExecutionViewResultBlockParam`

            - `content: string`

            - `file_type: "text" | "image" | "pdf"`

              - `"text"`

              - `"image"`

              - `"pdf"`

            - `type: "text_editor_code_execution_view_result"`

              - `"text_editor_code_execution_view_result"`

            - `num_lines?: number | null`

            - `start_line?: number | null`

            - `total_lines?: number | null`

          - `BetaTextEditorCodeExecutionCreateResultBlockParam`

            - `is_file_update: boolean`

            - `type: "text_editor_code_execution_create_result"`

              - `"text_editor_code_execution_create_result"`

          - `BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

            - `type: "text_editor_code_execution_str_replace_result"`

              - `"text_editor_code_execution_str_replace_result"`

            - `lines?: Array<string> | null`

            - `new_lines?: number | null`

            - `new_start?: number | null`

            - `old_lines?: number | null`

            - `old_start?: number | null`

        - `tool_use_id: string`

        - `type: "text_editor_code_execution_tool_result"`

          - `"text_editor_code_execution_tool_result"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `BetaToolSearchToolResultBlockParam`

        - `content: BetaToolSearchToolResultErrorParam | BetaToolSearchToolSearchResultBlockParam`

          - `BetaToolSearchToolResultErrorParam`

            - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

            - `type: "tool_search_tool_result_error"`

              - `"tool_search_tool_result_error"`

          - `BetaToolSearchToolSearchResultBlockParam`

            - `tool_references: Array<BetaToolReferenceBlockParam>`

              - `tool_name: string`

              - `type: "tool_reference"`

                - `"tool_reference"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `type: "tool_search_tool_search_result"`

              - `"tool_search_tool_search_result"`

        - `tool_use_id: string`

        - `type: "tool_search_tool_result"`

          - `"tool_search_tool_result"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `BetaMCPToolUseBlockParam`

        - `id: string`

        - `input: Record<string, unknown>`

        - `name: string`

        - `server_name: string`

          The name of the MCP server

        - `type: "mcp_tool_use"`

          - `"mcp_tool_use"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `BetaRequestMCPToolResultBlockParam`

        - `tool_use_id: string`

        - `type: "mcp_tool_result"`

          - `"mcp_tool_result"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `content?: string | Array<BetaTextBlockParam>`

          - `string`

          - `Array<BetaTextBlockParam>`

            - `text: string`

            - `type: "text"`

              - `"text"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `citations?: Array<BetaTextCitationParam> | null`

              - `BetaCitationCharLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_char_index: number`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `BetaCitationPageLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_page_number: number`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `BetaCitationContentBlockLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_block_index: number`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `BetaCitationWebSearchResultLocationParam`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string | null`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `BetaCitationSearchResultLocationParam`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string | null`

                - `type: "search_result_location"`

                  - `"search_result_location"`

        - `is_error?: boolean`

      - `BetaContainerUploadBlockParam`

        A content block that represents a file to be uploaded to the container
        Files uploaded via this block will be available in the container's input directory.

        - `file_id: string`

        - `type: "container_upload"`

          - `"container_upload"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta Message Tokens Count

- `BetaMessageTokensCount`

  - `context_management: BetaCountTokensContextManagementResponse | null`

    Information about context management applied to the message.

    - `original_input_tokens: number`

      The original token count before context management was applied

  - `input_tokens: number`

    The total number of tokens across the provided list of messages, system prompt, and tools.

### Beta Metadata

- `BetaMetadata`

  - `user_id?: string | null`

    An external identifier for the user who is associated with the request.

    This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

### Beta Output Config

- `BetaOutputConfig`

  - `effort?: "low" | "medium" | "high" | null`

    All possible effort levels.

    - `"low"`

    - `"medium"`

    - `"high"`

### Beta Plain Text Source

- `BetaPlainTextSource`

  - `data: string`

  - `media_type: "text/plain"`

    - `"text/plain"`

  - `type: "text"`

    - `"text"`

### Beta Raw Content Block Delta

- `BetaRawContentBlockDelta = BetaTextDelta | BetaInputJSONDelta | BetaCitationsDelta | 2 more`

  - `BetaTextDelta`

    - `text: string`

    - `type: "text_delta"`

      - `"text_delta"`

  - `BetaInputJSONDelta`

    - `partial_json: string`

    - `type: "input_json_delta"`

      - `"input_json_delta"`

  - `BetaCitationsDelta`

    - `citation: BetaCitationCharLocation | BetaCitationPageLocation | BetaCitationContentBlockLocation | 2 more`

      - `BetaCitationCharLocation`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_char_index: number`

        - `file_id: string | null`

        - `start_char_index: number`

        - `type: "char_location"`

          - `"char_location"`

      - `BetaCitationPageLocation`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_page_number: number`

        - `file_id: string | null`

        - `start_page_number: number`

        - `type: "page_location"`

          - `"page_location"`

      - `BetaCitationContentBlockLocation`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_block_index: number`

        - `file_id: string | null`

        - `start_block_index: number`

        - `type: "content_block_location"`

          - `"content_block_location"`

      - `BetaCitationsWebSearchResultLocation`

        - `cited_text: string`

        - `encrypted_index: string`

        - `title: string | null`

        - `type: "web_search_result_location"`

          - `"web_search_result_location"`

        - `url: string`

      - `BetaCitationSearchResultLocation`

        - `cited_text: string`

        - `end_block_index: number`

        - `search_result_index: number`

        - `source: string`

        - `start_block_index: number`

        - `title: string | null`

        - `type: "search_result_location"`

          - `"search_result_location"`

    - `type: "citations_delta"`

      - `"citations_delta"`

  - `BetaThinkingDelta`

    - `thinking: string`

    - `type: "thinking_delta"`

      - `"thinking_delta"`

  - `BetaSignatureDelta`

    - `signature: string`

    - `type: "signature_delta"`

      - `"signature_delta"`

### Beta Raw Content Block Delta Event

- `BetaRawContentBlockDeltaEvent`

  - `delta: BetaRawContentBlockDelta`

    - `BetaTextDelta`

      - `text: string`

      - `type: "text_delta"`

        - `"text_delta"`

    - `BetaInputJSONDelta`

      - `partial_json: string`

      - `type: "input_json_delta"`

        - `"input_json_delta"`

    - `BetaCitationsDelta`

      - `citation: BetaCitationCharLocation | BetaCitationPageLocation | BetaCitationContentBlockLocation | 2 more`

        - `BetaCitationCharLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_char_index: number`

          - `file_id: string | null`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `BetaCitationPageLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_page_number: number`

          - `file_id: string | null`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `BetaCitationContentBlockLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_block_index: number`

          - `file_id: string | null`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `BetaCitationsWebSearchResultLocation`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string | null`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `BetaCitationSearchResultLocation`

          - `cited_text: string`

          - `end_block_index: number`

          - `search_result_index: number`

          - `source: string`

          - `start_block_index: number`

          - `title: string | null`

          - `type: "search_result_location"`

            - `"search_result_location"`

      - `type: "citations_delta"`

        - `"citations_delta"`

    - `BetaThinkingDelta`

      - `thinking: string`

      - `type: "thinking_delta"`

        - `"thinking_delta"`

    - `BetaSignatureDelta`

      - `signature: string`

      - `type: "signature_delta"`

        - `"signature_delta"`

  - `index: number`

  - `type: "content_block_delta"`

    - `"content_block_delta"`

### Beta Raw Content Block Start Event

- `BetaRawContentBlockStartEvent`

  - `content_block: BetaTextBlock | BetaThinkingBlock | BetaRedactedThinkingBlock | 11 more`

    Response model for a file uploaded to the container.

    - `BetaTextBlock`

      - `citations: Array<BetaTextCitation> | null`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `BetaCitationCharLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_char_index: number`

          - `file_id: string | null`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `BetaCitationPageLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_page_number: number`

          - `file_id: string | null`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `BetaCitationContentBlockLocation`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_block_index: number`

          - `file_id: string | null`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `BetaCitationsWebSearchResultLocation`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string | null`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `BetaCitationSearchResultLocation`

          - `cited_text: string`

          - `end_block_index: number`

          - `search_result_index: number`

          - `source: string`

          - `start_block_index: number`

          - `title: string | null`

          - `type: "search_result_location"`

            - `"search_result_location"`

      - `text: string`

      - `type: "text"`

        - `"text"`

    - `BetaThinkingBlock`

      - `signature: string`

      - `thinking: string`

      - `type: "thinking"`

        - `"thinking"`

    - `BetaRedactedThinkingBlock`

      - `data: string`

      - `type: "redacted_thinking"`

        - `"redacted_thinking"`

    - `BetaToolUseBlock`

      - `id: string`

      - `input: Record<string, unknown>`

      - `name: string`

      - `type: "tool_use"`

        - `"tool_use"`

      - `caller?: BetaDirectCaller | BetaServerToolCaller`

        Tool invocation directly from the model.

        - `BetaDirectCaller`

          Tool invocation directly from the model.

          - `type: "direct"`

            - `"direct"`

        - `BetaServerToolCaller`

          Tool invocation generated by a server-side tool.

          - `tool_id: string`

          - `type: "code_execution_20250825"`

            - `"code_execution_20250825"`

    - `BetaServerToolUseBlock`

      - `id: string`

      - `caller: BetaDirectCaller | BetaServerToolCaller`

        Tool invocation directly from the model.

        - `BetaDirectCaller`

          Tool invocation directly from the model.

          - `type: "direct"`

            - `"direct"`

        - `BetaServerToolCaller`

          Tool invocation generated by a server-side tool.

          - `tool_id: string`

          - `type: "code_execution_20250825"`

            - `"code_execution_20250825"`

      - `input: Record<string, unknown>`

      - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

        - `"web_search"`

        - `"web_fetch"`

        - `"code_execution"`

        - `"bash_code_execution"`

        - `"text_editor_code_execution"`

        - `"tool_search_tool_regex"`

        - `"tool_search_tool_bm25"`

      - `type: "server_tool_use"`

        - `"server_tool_use"`

    - `BetaWebSearchToolResultBlock`

      - `content: BetaWebSearchToolResultBlockContent`

        - `BetaWebSearchToolResultError`

          - `error_code: BetaWebSearchToolResultErrorCode`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"max_uses_exceeded"`

            - `"too_many_requests"`

            - `"query_too_long"`

          - `type: "web_search_tool_result_error"`

            - `"web_search_tool_result_error"`

        - `Array<BetaWebSearchResultBlock>`

          - `encrypted_content: string`

          - `page_age: string | null`

          - `title: string`

          - `type: "web_search_result"`

            - `"web_search_result"`

          - `url: string`

      - `tool_use_id: string`

      - `type: "web_search_tool_result"`

        - `"web_search_tool_result"`

    - `BetaWebFetchToolResultBlock`

      - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

        - `BetaWebFetchToolResultErrorBlock`

          - `error_code: BetaWebFetchToolResultErrorCode`

            - `"invalid_tool_input"`

            - `"url_too_long"`

            - `"url_not_allowed"`

            - `"url_not_accessible"`

            - `"unsupported_content_type"`

            - `"too_many_requests"`

            - `"max_uses_exceeded"`

            - `"unavailable"`

          - `type: "web_fetch_tool_result_error"`

            - `"web_fetch_tool_result_error"`

        - `BetaWebFetchBlock`

          - `content: BetaDocumentBlock`

            - `citations: BetaCitationConfig | null`

              Citation configuration for the document

              - `enabled: boolean`

            - `source: BetaBase64PDFSource | BetaPlainTextSource`

              - `BetaBase64PDFSource`

                - `data: string`

                - `media_type: "application/pdf"`

                  - `"application/pdf"`

                - `type: "base64"`

                  - `"base64"`

              - `BetaPlainTextSource`

                - `data: string`

                - `media_type: "text/plain"`

                  - `"text/plain"`

                - `type: "text"`

                  - `"text"`

            - `title: string | null`

              The title of the document

            - `type: "document"`

              - `"document"`

          - `retrieved_at: string | null`

            ISO 8601 timestamp when the content was retrieved

          - `type: "web_fetch_result"`

            - `"web_fetch_result"`

          - `url: string`

            Fetched content URL

      - `tool_use_id: string`

      - `type: "web_fetch_tool_result"`

        - `"web_fetch_tool_result"`

    - `BetaCodeExecutionToolResultBlock`

      - `content: BetaCodeExecutionToolResultBlockContent`

        - `BetaCodeExecutionToolResultError`

          - `error_code: BetaCodeExecutionToolResultErrorCode`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

          - `type: "code_execution_tool_result_error"`

            - `"code_execution_tool_result_error"`

        - `BetaCodeExecutionResultBlock`

          - `content: Array<BetaCodeExecutionOutputBlock>`

            - `file_id: string`

            - `type: "code_execution_output"`

              - `"code_execution_output"`

          - `return_code: number`

          - `stderr: string`

          - `stdout: string`

          - `type: "code_execution_result"`

            - `"code_execution_result"`

      - `tool_use_id: string`

      - `type: "code_execution_tool_result"`

        - `"code_execution_tool_result"`

    - `BetaBashCodeExecutionToolResultBlock`

      - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

        - `BetaBashCodeExecutionToolResultError`

          - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

            - `"output_file_too_large"`

          - `type: "bash_code_execution_tool_result_error"`

            - `"bash_code_execution_tool_result_error"`

        - `BetaBashCodeExecutionResultBlock`

          - `content: Array<BetaBashCodeExecutionOutputBlock>`

            - `file_id: string`

            - `type: "bash_code_execution_output"`

              - `"bash_code_execution_output"`

          - `return_code: number`

          - `stderr: string`

          - `stdout: string`

          - `type: "bash_code_execution_result"`

            - `"bash_code_execution_result"`

      - `tool_use_id: string`

      - `type: "bash_code_execution_tool_result"`

        - `"bash_code_execution_tool_result"`

    - `BetaTextEditorCodeExecutionToolResultBlock`

      - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

        - `BetaTextEditorCodeExecutionToolResultError`

          - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

            - `"file_not_found"`

          - `error_message: string | null`

          - `type: "text_editor_code_execution_tool_result_error"`

            - `"text_editor_code_execution_tool_result_error"`

        - `BetaTextEditorCodeExecutionViewResultBlock`

          - `content: string`

          - `file_type: "text" | "image" | "pdf"`

            - `"text"`

            - `"image"`

            - `"pdf"`

          - `num_lines: number | null`

          - `start_line: number | null`

          - `total_lines: number | null`

          - `type: "text_editor_code_execution_view_result"`

            - `"text_editor_code_execution_view_result"`

        - `BetaTextEditorCodeExecutionCreateResultBlock`

          - `is_file_update: boolean`

          - `type: "text_editor_code_execution_create_result"`

            - `"text_editor_code_execution_create_result"`

        - `BetaTextEditorCodeExecutionStrReplaceResultBlock`

          - `lines: Array<string> | null`

          - `new_lines: number | null`

          - `new_start: number | null`

          - `old_lines: number | null`

          - `old_start: number | null`

          - `type: "text_editor_code_execution_str_replace_result"`

            - `"text_editor_code_execution_str_replace_result"`

      - `tool_use_id: string`

      - `type: "text_editor_code_execution_tool_result"`

        - `"text_editor_code_execution_tool_result"`

    - `BetaToolSearchToolResultBlock`

      - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

        - `BetaToolSearchToolResultError`

          - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

          - `error_message: string | null`

          - `type: "tool_search_tool_result_error"`

            - `"tool_search_tool_result_error"`

        - `BetaToolSearchToolSearchResultBlock`

          - `tool_references: Array<BetaToolReferenceBlock>`

            - `tool_name: string`

            - `type: "tool_reference"`

              - `"tool_reference"`

          - `type: "tool_search_tool_search_result"`

            - `"tool_search_tool_search_result"`

      - `tool_use_id: string`

      - `type: "tool_search_tool_result"`

        - `"tool_search_tool_result"`

    - `BetaMCPToolUseBlock`

      - `id: string`

      - `input: Record<string, unknown>`

      - `name: string`

        The name of the MCP tool

      - `server_name: string`

        The name of the MCP server

      - `type: "mcp_tool_use"`

        - `"mcp_tool_use"`

    - `BetaMCPToolResultBlock`

      - `content: string | Array<BetaTextBlock>`

        - `string`

        - `Array<BetaTextBlock>`

          - `citations: Array<BetaTextCitation> | null`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `BetaCitationCharLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_char_index: number`

              - `file_id: string | null`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `BetaCitationPageLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_page_number: number`

              - `file_id: string | null`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `BetaCitationContentBlockLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_block_index: number`

              - `file_id: string | null`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `BetaCitationsWebSearchResultLocation`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string | null`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `BetaCitationSearchResultLocation`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string | null`

              - `type: "search_result_location"`

                - `"search_result_location"`

          - `text: string`

          - `type: "text"`

            - `"text"`

      - `is_error: boolean`

      - `tool_use_id: string`

      - `type: "mcp_tool_result"`

        - `"mcp_tool_result"`

    - `BetaContainerUploadBlock`

      Response model for a file uploaded to the container.

      - `file_id: string`

      - `type: "container_upload"`

        - `"container_upload"`

  - `index: number`

  - `type: "content_block_start"`

    - `"content_block_start"`

### Beta Raw Content Block Stop Event

- `BetaRawContentBlockStopEvent`

  - `index: number`

  - `type: "content_block_stop"`

    - `"content_block_stop"`

### Beta Raw Message Delta Event

- `BetaRawMessageDeltaEvent`

  - `context_management: BetaContextManagementResponse | null`

    Information about context management strategies applied during the request

    - `applied_edits: Array<BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse>`

      List of context management edits that were applied.

      - `BetaClearToolUses20250919EditResponse`

        - `cleared_input_tokens: number`

          Number of input tokens cleared by this edit.

        - `cleared_tool_uses: number`

          Number of tool uses that were cleared.

        - `type: "clear_tool_uses_20250919"`

          The type of context management edit applied.

          - `"clear_tool_uses_20250919"`

      - `BetaClearThinking20251015EditResponse`

        - `cleared_input_tokens: number`

          Number of input tokens cleared by this edit.

        - `cleared_thinking_turns: number`

          Number of thinking turns that were cleared.

        - `type: "clear_thinking_20251015"`

          The type of context management edit applied.

          - `"clear_thinking_20251015"`

  - `delta: Delta`

    - `container: BetaContainer | null`

      Information about the container used in the request (for the code execution tool)

      - `id: string`

        Identifier for the container used in this request

      - `expires_at: string`

        The time at which the container will expire.

      - `skills: Array<BetaSkill> | null`

        Skills loaded in the container

        - `skill_id: string`

          Skill ID

        - `type: "anthropic" | "custom"`

          Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

          - `"anthropic"`

          - `"custom"`

        - `version: string`

          Skill version or 'latest' for most recent version

    - `stop_reason: BetaStopReason | null`

      - `"end_turn"`

      - `"max_tokens"`

      - `"stop_sequence"`

      - `"tool_use"`

      - `"pause_turn"`

      - `"refusal"`

      - `"model_context_window_exceeded"`

    - `stop_sequence: string | null`

  - `type: "message_delta"`

    - `"message_delta"`

  - `usage: BetaMessageDeltaUsage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cache_creation_input_tokens: number | null`

      The cumulative number of input tokens used to create the cache entry.

    - `cache_read_input_tokens: number | null`

      The cumulative number of input tokens read from the cache.

    - `input_tokens: number | null`

      The cumulative number of input tokens which were used.

    - `output_tokens: number`

      The cumulative number of output tokens which were used.

    - `server_tool_use: BetaServerToolUsage | null`

      The number of server tool requests.

      - `web_fetch_requests: number`

        The number of web fetch tool requests.

      - `web_search_requests: number`

        The number of web search tool requests.

### Beta Raw Message Start Event

- `BetaRawMessageStartEvent`

  - `message: BetaMessage`

    - `id: string`

      Unique object identifier.

      The format and length of IDs may change over time.

    - `container: BetaContainer | null`

      Information about the container used in the request (for the code execution tool)

      - `id: string`

        Identifier for the container used in this request

      - `expires_at: string`

        The time at which the container will expire.

      - `skills: Array<BetaSkill> | null`

        Skills loaded in the container

        - `skill_id: string`

          Skill ID

        - `type: "anthropic" | "custom"`

          Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

          - `"anthropic"`

          - `"custom"`

        - `version: string`

          Skill version or 'latest' for most recent version

    - `content: Array<BetaContentBlock>`

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

      - `BetaTextBlock`

        - `citations: Array<BetaTextCitation> | null`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `BetaCitationCharLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_char_index: number`

            - `file_id: string | null`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `BetaCitationPageLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_page_number: number`

            - `file_id: string | null`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `BetaCitationContentBlockLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_block_index: number`

            - `file_id: string | null`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `BetaCitationsWebSearchResultLocation`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string | null`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `BetaCitationSearchResultLocation`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string | null`

            - `type: "search_result_location"`

              - `"search_result_location"`

        - `text: string`

        - `type: "text"`

          - `"text"`

      - `BetaThinkingBlock`

        - `signature: string`

        - `thinking: string`

        - `type: "thinking"`

          - `"thinking"`

      - `BetaRedactedThinkingBlock`

        - `data: string`

        - `type: "redacted_thinking"`

          - `"redacted_thinking"`

      - `BetaToolUseBlock`

        - `id: string`

        - `input: Record<string, unknown>`

        - `name: string`

        - `type: "tool_use"`

          - `"tool_use"`

        - `caller?: BetaDirectCaller | BetaServerToolCaller`

          Tool invocation directly from the model.

          - `BetaDirectCaller`

            Tool invocation directly from the model.

            - `type: "direct"`

              - `"direct"`

          - `BetaServerToolCaller`

            Tool invocation generated by a server-side tool.

            - `tool_id: string`

            - `type: "code_execution_20250825"`

              - `"code_execution_20250825"`

      - `BetaServerToolUseBlock`

        - `id: string`

        - `caller: BetaDirectCaller | BetaServerToolCaller`

          Tool invocation directly from the model.

          - `BetaDirectCaller`

            Tool invocation directly from the model.

            - `type: "direct"`

              - `"direct"`

          - `BetaServerToolCaller`

            Tool invocation generated by a server-side tool.

            - `tool_id: string`

            - `type: "code_execution_20250825"`

              - `"code_execution_20250825"`

        - `input: Record<string, unknown>`

        - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

          - `"web_search"`

          - `"web_fetch"`

          - `"code_execution"`

          - `"bash_code_execution"`

          - `"text_editor_code_execution"`

          - `"tool_search_tool_regex"`

          - `"tool_search_tool_bm25"`

        - `type: "server_tool_use"`

          - `"server_tool_use"`

      - `BetaWebSearchToolResultBlock`

        - `content: BetaWebSearchToolResultBlockContent`

          - `BetaWebSearchToolResultError`

            - `error_code: BetaWebSearchToolResultErrorCode`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"max_uses_exceeded"`

              - `"too_many_requests"`

              - `"query_too_long"`

            - `type: "web_search_tool_result_error"`

              - `"web_search_tool_result_error"`

          - `Array<BetaWebSearchResultBlock>`

            - `encrypted_content: string`

            - `page_age: string | null`

            - `title: string`

            - `type: "web_search_result"`

              - `"web_search_result"`

            - `url: string`

        - `tool_use_id: string`

        - `type: "web_search_tool_result"`

          - `"web_search_tool_result"`

      - `BetaWebFetchToolResultBlock`

        - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

          - `BetaWebFetchToolResultErrorBlock`

            - `error_code: BetaWebFetchToolResultErrorCode`

              - `"invalid_tool_input"`

              - `"url_too_long"`

              - `"url_not_allowed"`

              - `"url_not_accessible"`

              - `"unsupported_content_type"`

              - `"too_many_requests"`

              - `"max_uses_exceeded"`

              - `"unavailable"`

            - `type: "web_fetch_tool_result_error"`

              - `"web_fetch_tool_result_error"`

          - `BetaWebFetchBlock`

            - `content: BetaDocumentBlock`

              - `citations: BetaCitationConfig | null`

                Citation configuration for the document

                - `enabled: boolean`

              - `source: BetaBase64PDFSource | BetaPlainTextSource`

                - `BetaBase64PDFSource`

                  - `data: string`

                  - `media_type: "application/pdf"`

                    - `"application/pdf"`

                  - `type: "base64"`

                    - `"base64"`

                - `BetaPlainTextSource`

                  - `data: string`

                  - `media_type: "text/plain"`

                    - `"text/plain"`

                  - `type: "text"`

                    - `"text"`

              - `title: string | null`

                The title of the document

              - `type: "document"`

                - `"document"`

            - `retrieved_at: string | null`

              ISO 8601 timestamp when the content was retrieved

            - `type: "web_fetch_result"`

              - `"web_fetch_result"`

            - `url: string`

              Fetched content URL

        - `tool_use_id: string`

        - `type: "web_fetch_tool_result"`

          - `"web_fetch_tool_result"`

      - `BetaCodeExecutionToolResultBlock`

        - `content: BetaCodeExecutionToolResultBlockContent`

          - `BetaCodeExecutionToolResultError`

            - `error_code: BetaCodeExecutionToolResultErrorCode`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

            - `type: "code_execution_tool_result_error"`

              - `"code_execution_tool_result_error"`

          - `BetaCodeExecutionResultBlock`

            - `content: Array<BetaCodeExecutionOutputBlock>`

              - `file_id: string`

              - `type: "code_execution_output"`

                - `"code_execution_output"`

            - `return_code: number`

            - `stderr: string`

            - `stdout: string`

            - `type: "code_execution_result"`

              - `"code_execution_result"`

        - `tool_use_id: string`

        - `type: "code_execution_tool_result"`

          - `"code_execution_tool_result"`

      - `BetaBashCodeExecutionToolResultBlock`

        - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

          - `BetaBashCodeExecutionToolResultError`

            - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

              - `"output_file_too_large"`

            - `type: "bash_code_execution_tool_result_error"`

              - `"bash_code_execution_tool_result_error"`

          - `BetaBashCodeExecutionResultBlock`

            - `content: Array<BetaBashCodeExecutionOutputBlock>`

              - `file_id: string`

              - `type: "bash_code_execution_output"`

                - `"bash_code_execution_output"`

            - `return_code: number`

            - `stderr: string`

            - `stdout: string`

            - `type: "bash_code_execution_result"`

              - `"bash_code_execution_result"`

        - `tool_use_id: string`

        - `type: "bash_code_execution_tool_result"`

          - `"bash_code_execution_tool_result"`

      - `BetaTextEditorCodeExecutionToolResultBlock`

        - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

          - `BetaTextEditorCodeExecutionToolResultError`

            - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

              - `"file_not_found"`

            - `error_message: string | null`

            - `type: "text_editor_code_execution_tool_result_error"`

              - `"text_editor_code_execution_tool_result_error"`

          - `BetaTextEditorCodeExecutionViewResultBlock`

            - `content: string`

            - `file_type: "text" | "image" | "pdf"`

              - `"text"`

              - `"image"`

              - `"pdf"`

            - `num_lines: number | null`

            - `start_line: number | null`

            - `total_lines: number | null`

            - `type: "text_editor_code_execution_view_result"`

              - `"text_editor_code_execution_view_result"`

          - `BetaTextEditorCodeExecutionCreateResultBlock`

            - `is_file_update: boolean`

            - `type: "text_editor_code_execution_create_result"`

              - `"text_editor_code_execution_create_result"`

          - `BetaTextEditorCodeExecutionStrReplaceResultBlock`

            - `lines: Array<string> | null`

            - `new_lines: number | null`

            - `new_start: number | null`

            - `old_lines: number | null`

            - `old_start: number | null`

            - `type: "text_editor_code_execution_str_replace_result"`

              - `"text_editor_code_execution_str_replace_result"`

        - `tool_use_id: string`

        - `type: "text_editor_code_execution_tool_result"`

          - `"text_editor_code_execution_tool_result"`

      - `BetaToolSearchToolResultBlock`

        - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

          - `BetaToolSearchToolResultError`

            - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

            - `error_message: string | null`

            - `type: "tool_search_tool_result_error"`

              - `"tool_search_tool_result_error"`

          - `BetaToolSearchToolSearchResultBlock`

            - `tool_references: Array<BetaToolReferenceBlock>`

              - `tool_name: string`

              - `type: "tool_reference"`

                - `"tool_reference"`

            - `type: "tool_search_tool_search_result"`

              - `"tool_search_tool_search_result"`

        - `tool_use_id: string`

        - `type: "tool_search_tool_result"`

          - `"tool_search_tool_result"`

      - `BetaMCPToolUseBlock`

        - `id: string`

        - `input: Record<string, unknown>`

        - `name: string`

          The name of the MCP tool

        - `server_name: string`

          The name of the MCP server

        - `type: "mcp_tool_use"`

          - `"mcp_tool_use"`

      - `BetaMCPToolResultBlock`

        - `content: string | Array<BetaTextBlock>`

          - `string`

          - `Array<BetaTextBlock>`

            - `citations: Array<BetaTextCitation> | null`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `BetaCitationCharLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_char_index: number`

                - `file_id: string | null`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `BetaCitationPageLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_page_number: number`

                - `file_id: string | null`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `BetaCitationContentBlockLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_block_index: number`

                - `file_id: string | null`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `BetaCitationsWebSearchResultLocation`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string | null`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `BetaCitationSearchResultLocation`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string | null`

                - `type: "search_result_location"`

                  - `"search_result_location"`

            - `text: string`

            - `type: "text"`

              - `"text"`

        - `is_error: boolean`

        - `tool_use_id: string`

        - `type: "mcp_tool_result"`

          - `"mcp_tool_result"`

      - `BetaContainerUploadBlock`

        Response model for a file uploaded to the container.

        - `file_id: string`

        - `type: "container_upload"`

          - `"container_upload"`

    - `context_management: BetaContextManagementResponse | null`

      Context management response.

      Information about context management strategies applied during the request.

      - `applied_edits: Array<BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse>`

        List of context management edits that were applied.

        - `BetaClearToolUses20250919EditResponse`

          - `cleared_input_tokens: number`

            Number of input tokens cleared by this edit.

          - `cleared_tool_uses: number`

            Number of tool uses that were cleared.

          - `type: "clear_tool_uses_20250919"`

            The type of context management edit applied.

            - `"clear_tool_uses_20250919"`

        - `BetaClearThinking20251015EditResponse`

          - `cleared_input_tokens: number`

            Number of input tokens cleared by this edit.

          - `cleared_thinking_turns: number`

            Number of thinking turns that were cleared.

          - `type: "clear_thinking_20251015"`

            The type of context management edit applied.

            - `"clear_thinking_20251015"`

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

    - `role: "assistant"`

      Conversational role of the generated message.

      This will always be `"assistant"`.

      - `"assistant"`

    - `stop_reason: BetaStopReason | null`

      The reason that we stopped.

      This may be one the following values:

      * `"end_turn"`: the model reached a natural stopping point
      * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
      * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
      * `"tool_use"`: the model invoked one or more tools
      * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
      * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

      In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

      - `"end_turn"`

      - `"max_tokens"`

      - `"stop_sequence"`

      - `"tool_use"`

      - `"pause_turn"`

      - `"refusal"`

      - `"model_context_window_exceeded"`

    - `stop_sequence: string | null`

      Which custom stop sequence was generated, if any.

      This value will be a non-null string if one of your custom stop sequences was generated.

    - `type: "message"`

      Object type.

      For Messages, this is always `"message"`.

      - `"message"`

    - `usage: BetaUsage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cache_creation: BetaCacheCreation | null`

        Breakdown of cached tokens by TTL

        - `ephemeral_1h_input_tokens: number`

          The number of input tokens used to create the 1 hour cache entry.

        - `ephemeral_5m_input_tokens: number`

          The number of input tokens used to create the 5 minute cache entry.

      - `cache_creation_input_tokens: number | null`

        The number of input tokens used to create the cache entry.

      - `cache_read_input_tokens: number | null`

        The number of input tokens read from the cache.

      - `input_tokens: number`

        The number of input tokens which were used.

      - `output_tokens: number`

        The number of output tokens which were used.

      - `server_tool_use: BetaServerToolUsage | null`

        The number of server tool requests.

        - `web_fetch_requests: number`

          The number of web fetch tool requests.

        - `web_search_requests: number`

          The number of web search tool requests.

      - `service_tier: "standard" | "priority" | "batch" | null`

        If the request used the priority, standard, or batch tier.

        - `"standard"`

        - `"priority"`

        - `"batch"`

  - `type: "message_start"`

    - `"message_start"`

### Beta Raw Message Stop Event

- `BetaRawMessageStopEvent`

  - `type: "message_stop"`

    - `"message_stop"`

### Beta Raw Message Stream Event

- `BetaRawMessageStreamEvent = BetaRawMessageStartEvent | BetaRawMessageDeltaEvent | BetaRawMessageStopEvent | 3 more`

  - `BetaRawMessageStartEvent`

    - `message: BetaMessage`

      - `id: string`

        Unique object identifier.

        The format and length of IDs may change over time.

      - `container: BetaContainer | null`

        Information about the container used in the request (for the code execution tool)

        - `id: string`

          Identifier for the container used in this request

        - `expires_at: string`

          The time at which the container will expire.

        - `skills: Array<BetaSkill> | null`

          Skills loaded in the container

          - `skill_id: string`

            Skill ID

          - `type: "anthropic" | "custom"`

            Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

            - `"anthropic"`

            - `"custom"`

          - `version: string`

            Skill version or 'latest' for most recent version

      - `content: Array<BetaContentBlock>`

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

        - `BetaTextBlock`

          - `citations: Array<BetaTextCitation> | null`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `BetaCitationCharLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_char_index: number`

              - `file_id: string | null`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `BetaCitationPageLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_page_number: number`

              - `file_id: string | null`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `BetaCitationContentBlockLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_block_index: number`

              - `file_id: string | null`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `BetaCitationsWebSearchResultLocation`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string | null`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `BetaCitationSearchResultLocation`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string | null`

              - `type: "search_result_location"`

                - `"search_result_location"`

          - `text: string`

          - `type: "text"`

            - `"text"`

        - `BetaThinkingBlock`

          - `signature: string`

          - `thinking: string`

          - `type: "thinking"`

            - `"thinking"`

        - `BetaRedactedThinkingBlock`

          - `data: string`

          - `type: "redacted_thinking"`

            - `"redacted_thinking"`

        - `BetaToolUseBlock`

          - `id: string`

          - `input: Record<string, unknown>`

          - `name: string`

          - `type: "tool_use"`

            - `"tool_use"`

          - `caller?: BetaDirectCaller | BetaServerToolCaller`

            Tool invocation directly from the model.

            - `BetaDirectCaller`

              Tool invocation directly from the model.

              - `type: "direct"`

                - `"direct"`

            - `BetaServerToolCaller`

              Tool invocation generated by a server-side tool.

              - `tool_id: string`

              - `type: "code_execution_20250825"`

                - `"code_execution_20250825"`

        - `BetaServerToolUseBlock`

          - `id: string`

          - `caller: BetaDirectCaller | BetaServerToolCaller`

            Tool invocation directly from the model.

            - `BetaDirectCaller`

              Tool invocation directly from the model.

              - `type: "direct"`

                - `"direct"`

            - `BetaServerToolCaller`

              Tool invocation generated by a server-side tool.

              - `tool_id: string`

              - `type: "code_execution_20250825"`

                - `"code_execution_20250825"`

          - `input: Record<string, unknown>`

          - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

            - `"web_search"`

            - `"web_fetch"`

            - `"code_execution"`

            - `"bash_code_execution"`

            - `"text_editor_code_execution"`

            - `"tool_search_tool_regex"`

            - `"tool_search_tool_bm25"`

          - `type: "server_tool_use"`

            - `"server_tool_use"`

        - `BetaWebSearchToolResultBlock`

          - `content: BetaWebSearchToolResultBlockContent`

            - `BetaWebSearchToolResultError`

              - `error_code: BetaWebSearchToolResultErrorCode`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"max_uses_exceeded"`

                - `"too_many_requests"`

                - `"query_too_long"`

              - `type: "web_search_tool_result_error"`

                - `"web_search_tool_result_error"`

            - `Array<BetaWebSearchResultBlock>`

              - `encrypted_content: string`

              - `page_age: string | null`

              - `title: string`

              - `type: "web_search_result"`

                - `"web_search_result"`

              - `url: string`

          - `tool_use_id: string`

          - `type: "web_search_tool_result"`

            - `"web_search_tool_result"`

        - `BetaWebFetchToolResultBlock`

          - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

            - `BetaWebFetchToolResultErrorBlock`

              - `error_code: BetaWebFetchToolResultErrorCode`

                - `"invalid_tool_input"`

                - `"url_too_long"`

                - `"url_not_allowed"`

                - `"url_not_accessible"`

                - `"unsupported_content_type"`

                - `"too_many_requests"`

                - `"max_uses_exceeded"`

                - `"unavailable"`

              - `type: "web_fetch_tool_result_error"`

                - `"web_fetch_tool_result_error"`

            - `BetaWebFetchBlock`

              - `content: BetaDocumentBlock`

                - `citations: BetaCitationConfig | null`

                  Citation configuration for the document

                  - `enabled: boolean`

                - `source: BetaBase64PDFSource | BetaPlainTextSource`

                  - `BetaBase64PDFSource`

                    - `data: string`

                    - `media_type: "application/pdf"`

                      - `"application/pdf"`

                    - `type: "base64"`

                      - `"base64"`

                  - `BetaPlainTextSource`

                    - `data: string`

                    - `media_type: "text/plain"`

                      - `"text/plain"`

                    - `type: "text"`

                      - `"text"`

                - `title: string | null`

                  The title of the document

                - `type: "document"`

                  - `"document"`

              - `retrieved_at: string | null`

                ISO 8601 timestamp when the content was retrieved

              - `type: "web_fetch_result"`

                - `"web_fetch_result"`

              - `url: string`

                Fetched content URL

          - `tool_use_id: string`

          - `type: "web_fetch_tool_result"`

            - `"web_fetch_tool_result"`

        - `BetaCodeExecutionToolResultBlock`

          - `content: BetaCodeExecutionToolResultBlockContent`

            - `BetaCodeExecutionToolResultError`

              - `error_code: BetaCodeExecutionToolResultErrorCode`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"too_many_requests"`

                - `"execution_time_exceeded"`

              - `type: "code_execution_tool_result_error"`

                - `"code_execution_tool_result_error"`

            - `BetaCodeExecutionResultBlock`

              - `content: Array<BetaCodeExecutionOutputBlock>`

                - `file_id: string`

                - `type: "code_execution_output"`

                  - `"code_execution_output"`

              - `return_code: number`

              - `stderr: string`

              - `stdout: string`

              - `type: "code_execution_result"`

                - `"code_execution_result"`

          - `tool_use_id: string`

          - `type: "code_execution_tool_result"`

            - `"code_execution_tool_result"`

        - `BetaBashCodeExecutionToolResultBlock`

          - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

            - `BetaBashCodeExecutionToolResultError`

              - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"too_many_requests"`

                - `"execution_time_exceeded"`

                - `"output_file_too_large"`

              - `type: "bash_code_execution_tool_result_error"`

                - `"bash_code_execution_tool_result_error"`

            - `BetaBashCodeExecutionResultBlock`

              - `content: Array<BetaBashCodeExecutionOutputBlock>`

                - `file_id: string`

                - `type: "bash_code_execution_output"`

                  - `"bash_code_execution_output"`

              - `return_code: number`

              - `stderr: string`

              - `stdout: string`

              - `type: "bash_code_execution_result"`

                - `"bash_code_execution_result"`

          - `tool_use_id: string`

          - `type: "bash_code_execution_tool_result"`

            - `"bash_code_execution_tool_result"`

        - `BetaTextEditorCodeExecutionToolResultBlock`

          - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

            - `BetaTextEditorCodeExecutionToolResultError`

              - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"too_many_requests"`

                - `"execution_time_exceeded"`

                - `"file_not_found"`

              - `error_message: string | null`

              - `type: "text_editor_code_execution_tool_result_error"`

                - `"text_editor_code_execution_tool_result_error"`

            - `BetaTextEditorCodeExecutionViewResultBlock`

              - `content: string`

              - `file_type: "text" | "image" | "pdf"`

                - `"text"`

                - `"image"`

                - `"pdf"`

              - `num_lines: number | null`

              - `start_line: number | null`

              - `total_lines: number | null`

              - `type: "text_editor_code_execution_view_result"`

                - `"text_editor_code_execution_view_result"`

            - `BetaTextEditorCodeExecutionCreateResultBlock`

              - `is_file_update: boolean`

              - `type: "text_editor_code_execution_create_result"`

                - `"text_editor_code_execution_create_result"`

            - `BetaTextEditorCodeExecutionStrReplaceResultBlock`

              - `lines: Array<string> | null`

              - `new_lines: number | null`

              - `new_start: number | null`

              - `old_lines: number | null`

              - `old_start: number | null`

              - `type: "text_editor_code_execution_str_replace_result"`

                - `"text_editor_code_execution_str_replace_result"`

          - `tool_use_id: string`

          - `type: "text_editor_code_execution_tool_result"`

            - `"text_editor_code_execution_tool_result"`

        - `BetaToolSearchToolResultBlock`

          - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

            - `BetaToolSearchToolResultError`

              - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"too_many_requests"`

                - `"execution_time_exceeded"`

              - `error_message: string | null`

              - `type: "tool_search_tool_result_error"`

                - `"tool_search_tool_result_error"`

            - `BetaToolSearchToolSearchResultBlock`

              - `tool_references: Array<BetaToolReferenceBlock>`

                - `tool_name: string`

                - `type: "tool_reference"`

                  - `"tool_reference"`

              - `type: "tool_search_tool_search_result"`

                - `"tool_search_tool_search_result"`

          - `tool_use_id: string`

          - `type: "tool_search_tool_result"`

            - `"tool_search_tool_result"`

        - `BetaMCPToolUseBlock`

          - `id: string`

          - `input: Record<string, unknown>`

          - `name: string`

            The name of the MCP tool

          - `server_name: string`

            The name of the MCP server

          - `type: "mcp_tool_use"`

            - `"mcp_tool_use"`

        - `BetaMCPToolResultBlock`

          - `content: string | Array<BetaTextBlock>`

            - `string`

            - `Array<BetaTextBlock>`

              - `citations: Array<BetaTextCitation> | null`

                Citations supporting the text block.

                The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

                - `BetaCitationCharLocation`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_char_index: number`

                  - `file_id: string | null`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `BetaCitationPageLocation`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_page_number: number`

                  - `file_id: string | null`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `BetaCitationContentBlockLocation`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_block_index: number`

                  - `file_id: string | null`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `BetaCitationsWebSearchResultLocation`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string | null`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `BetaCitationSearchResultLocation`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string | null`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

              - `text: string`

              - `type: "text"`

                - `"text"`

          - `is_error: boolean`

          - `tool_use_id: string`

          - `type: "mcp_tool_result"`

            - `"mcp_tool_result"`

        - `BetaContainerUploadBlock`

          Response model for a file uploaded to the container.

          - `file_id: string`

          - `type: "container_upload"`

            - `"container_upload"`

      - `context_management: BetaContextManagementResponse | null`

        Context management response.

        Information about context management strategies applied during the request.

        - `applied_edits: Array<BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse>`

          List of context management edits that were applied.

          - `BetaClearToolUses20250919EditResponse`

            - `cleared_input_tokens: number`

              Number of input tokens cleared by this edit.

            - `cleared_tool_uses: number`

              Number of tool uses that were cleared.

            - `type: "clear_tool_uses_20250919"`

              The type of context management edit applied.

              - `"clear_tool_uses_20250919"`

          - `BetaClearThinking20251015EditResponse`

            - `cleared_input_tokens: number`

              Number of input tokens cleared by this edit.

            - `cleared_thinking_turns: number`

              Number of thinking turns that were cleared.

            - `type: "clear_thinking_20251015"`

              The type of context management edit applied.

              - `"clear_thinking_20251015"`

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

      - `role: "assistant"`

        Conversational role of the generated message.

        This will always be `"assistant"`.

        - `"assistant"`

      - `stop_reason: BetaStopReason | null`

        The reason that we stopped.

        This may be one the following values:

        * `"end_turn"`: the model reached a natural stopping point
        * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
        * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
        * `"tool_use"`: the model invoked one or more tools
        * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
        * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

        In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

        - `"end_turn"`

        - `"max_tokens"`

        - `"stop_sequence"`

        - `"tool_use"`

        - `"pause_turn"`

        - `"refusal"`

        - `"model_context_window_exceeded"`

      - `stop_sequence: string | null`

        Which custom stop sequence was generated, if any.

        This value will be a non-null string if one of your custom stop sequences was generated.

      - `type: "message"`

        Object type.

        For Messages, this is always `"message"`.

        - `"message"`

      - `usage: BetaUsage`

        Billing and rate-limit usage.

        Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

        Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

        For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

        Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

        - `cache_creation: BetaCacheCreation | null`

          Breakdown of cached tokens by TTL

          - `ephemeral_1h_input_tokens: number`

            The number of input tokens used to create the 1 hour cache entry.

          - `ephemeral_5m_input_tokens: number`

            The number of input tokens used to create the 5 minute cache entry.

        - `cache_creation_input_tokens: number | null`

          The number of input tokens used to create the cache entry.

        - `cache_read_input_tokens: number | null`

          The number of input tokens read from the cache.

        - `input_tokens: number`

          The number of input tokens which were used.

        - `output_tokens: number`

          The number of output tokens which were used.

        - `server_tool_use: BetaServerToolUsage | null`

          The number of server tool requests.

          - `web_fetch_requests: number`

            The number of web fetch tool requests.

          - `web_search_requests: number`

            The number of web search tool requests.

        - `service_tier: "standard" | "priority" | "batch" | null`

          If the request used the priority, standard, or batch tier.

          - `"standard"`

          - `"priority"`

          - `"batch"`

    - `type: "message_start"`

      - `"message_start"`

  - `BetaRawMessageDeltaEvent`

    - `context_management: BetaContextManagementResponse | null`

      Information about context management strategies applied during the request

      - `applied_edits: Array<BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse>`

        List of context management edits that were applied.

        - `BetaClearToolUses20250919EditResponse`

          - `cleared_input_tokens: number`

            Number of input tokens cleared by this edit.

          - `cleared_tool_uses: number`

            Number of tool uses that were cleared.

          - `type: "clear_tool_uses_20250919"`

            The type of context management edit applied.

            - `"clear_tool_uses_20250919"`

        - `BetaClearThinking20251015EditResponse`

          - `cleared_input_tokens: number`

            Number of input tokens cleared by this edit.

          - `cleared_thinking_turns: number`

            Number of thinking turns that were cleared.

          - `type: "clear_thinking_20251015"`

            The type of context management edit applied.

            - `"clear_thinking_20251015"`

    - `delta: Delta`

      - `container: BetaContainer | null`

        Information about the container used in the request (for the code execution tool)

        - `id: string`

          Identifier for the container used in this request

        - `expires_at: string`

          The time at which the container will expire.

        - `skills: Array<BetaSkill> | null`

          Skills loaded in the container

          - `skill_id: string`

            Skill ID

          - `type: "anthropic" | "custom"`

            Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

            - `"anthropic"`

            - `"custom"`

          - `version: string`

            Skill version or 'latest' for most recent version

      - `stop_reason: BetaStopReason | null`

        - `"end_turn"`

        - `"max_tokens"`

        - `"stop_sequence"`

        - `"tool_use"`

        - `"pause_turn"`

        - `"refusal"`

        - `"model_context_window_exceeded"`

      - `stop_sequence: string | null`

    - `type: "message_delta"`

      - `"message_delta"`

    - `usage: BetaMessageDeltaUsage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cache_creation_input_tokens: number | null`

        The cumulative number of input tokens used to create the cache entry.

      - `cache_read_input_tokens: number | null`

        The cumulative number of input tokens read from the cache.

      - `input_tokens: number | null`

        The cumulative number of input tokens which were used.

      - `output_tokens: number`

        The cumulative number of output tokens which were used.

      - `server_tool_use: BetaServerToolUsage | null`

        The number of server tool requests.

        - `web_fetch_requests: number`

          The number of web fetch tool requests.

        - `web_search_requests: number`

          The number of web search tool requests.

  - `BetaRawMessageStopEvent`

    - `type: "message_stop"`

      - `"message_stop"`

  - `BetaRawContentBlockStartEvent`

    - `content_block: BetaTextBlock | BetaThinkingBlock | BetaRedactedThinkingBlock | 11 more`

      Response model for a file uploaded to the container.

      - `BetaTextBlock`

        - `citations: Array<BetaTextCitation> | null`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `BetaCitationCharLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_char_index: number`

            - `file_id: string | null`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `BetaCitationPageLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_page_number: number`

            - `file_id: string | null`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `BetaCitationContentBlockLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_block_index: number`

            - `file_id: string | null`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `BetaCitationsWebSearchResultLocation`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string | null`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `BetaCitationSearchResultLocation`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string | null`

            - `type: "search_result_location"`

              - `"search_result_location"`

        - `text: string`

        - `type: "text"`

          - `"text"`

      - `BetaThinkingBlock`

        - `signature: string`

        - `thinking: string`

        - `type: "thinking"`

          - `"thinking"`

      - `BetaRedactedThinkingBlock`

        - `data: string`

        - `type: "redacted_thinking"`

          - `"redacted_thinking"`

      - `BetaToolUseBlock`

        - `id: string`

        - `input: Record<string, unknown>`

        - `name: string`

        - `type: "tool_use"`

          - `"tool_use"`

        - `caller?: BetaDirectCaller | BetaServerToolCaller`

          Tool invocation directly from the model.

          - `BetaDirectCaller`

            Tool invocation directly from the model.

            - `type: "direct"`

              - `"direct"`

          - `BetaServerToolCaller`

            Tool invocation generated by a server-side tool.

            - `tool_id: string`

            - `type: "code_execution_20250825"`

              - `"code_execution_20250825"`

      - `BetaServerToolUseBlock`

        - `id: string`

        - `caller: BetaDirectCaller | BetaServerToolCaller`

          Tool invocation directly from the model.

          - `BetaDirectCaller`

            Tool invocation directly from the model.

            - `type: "direct"`

              - `"direct"`

          - `BetaServerToolCaller`

            Tool invocation generated by a server-side tool.

            - `tool_id: string`

            - `type: "code_execution_20250825"`

              - `"code_execution_20250825"`

        - `input: Record<string, unknown>`

        - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

          - `"web_search"`

          - `"web_fetch"`

          - `"code_execution"`

          - `"bash_code_execution"`

          - `"text_editor_code_execution"`

          - `"tool_search_tool_regex"`

          - `"tool_search_tool_bm25"`

        - `type: "server_tool_use"`

          - `"server_tool_use"`

      - `BetaWebSearchToolResultBlock`

        - `content: BetaWebSearchToolResultBlockContent`

          - `BetaWebSearchToolResultError`

            - `error_code: BetaWebSearchToolResultErrorCode`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"max_uses_exceeded"`

              - `"too_many_requests"`

              - `"query_too_long"`

            - `type: "web_search_tool_result_error"`

              - `"web_search_tool_result_error"`

          - `Array<BetaWebSearchResultBlock>`

            - `encrypted_content: string`

            - `page_age: string | null`

            - `title: string`

            - `type: "web_search_result"`

              - `"web_search_result"`

            - `url: string`

        - `tool_use_id: string`

        - `type: "web_search_tool_result"`

          - `"web_search_tool_result"`

      - `BetaWebFetchToolResultBlock`

        - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

          - `BetaWebFetchToolResultErrorBlock`

            - `error_code: BetaWebFetchToolResultErrorCode`

              - `"invalid_tool_input"`

              - `"url_too_long"`

              - `"url_not_allowed"`

              - `"url_not_accessible"`

              - `"unsupported_content_type"`

              - `"too_many_requests"`

              - `"max_uses_exceeded"`

              - `"unavailable"`

            - `type: "web_fetch_tool_result_error"`

              - `"web_fetch_tool_result_error"`

          - `BetaWebFetchBlock`

            - `content: BetaDocumentBlock`

              - `citations: BetaCitationConfig | null`

                Citation configuration for the document

                - `enabled: boolean`

              - `source: BetaBase64PDFSource | BetaPlainTextSource`

                - `BetaBase64PDFSource`

                  - `data: string`

                  - `media_type: "application/pdf"`

                    - `"application/pdf"`

                  - `type: "base64"`

                    - `"base64"`

                - `BetaPlainTextSource`

                  - `data: string`

                  - `media_type: "text/plain"`

                    - `"text/plain"`

                  - `type: "text"`

                    - `"text"`

              - `title: string | null`

                The title of the document

              - `type: "document"`

                - `"document"`

            - `retrieved_at: string | null`

              ISO 8601 timestamp when the content was retrieved

            - `type: "web_fetch_result"`

              - `"web_fetch_result"`

            - `url: string`

              Fetched content URL

        - `tool_use_id: string`

        - `type: "web_fetch_tool_result"`

          - `"web_fetch_tool_result"`

      - `BetaCodeExecutionToolResultBlock`

        - `content: BetaCodeExecutionToolResultBlockContent`

          - `BetaCodeExecutionToolResultError`

            - `error_code: BetaCodeExecutionToolResultErrorCode`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

            - `type: "code_execution_tool_result_error"`

              - `"code_execution_tool_result_error"`

          - `BetaCodeExecutionResultBlock`

            - `content: Array<BetaCodeExecutionOutputBlock>`

              - `file_id: string`

              - `type: "code_execution_output"`

                - `"code_execution_output"`

            - `return_code: number`

            - `stderr: string`

            - `stdout: string`

            - `type: "code_execution_result"`

              - `"code_execution_result"`

        - `tool_use_id: string`

        - `type: "code_execution_tool_result"`

          - `"code_execution_tool_result"`

      - `BetaBashCodeExecutionToolResultBlock`

        - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

          - `BetaBashCodeExecutionToolResultError`

            - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

              - `"output_file_too_large"`

            - `type: "bash_code_execution_tool_result_error"`

              - `"bash_code_execution_tool_result_error"`

          - `BetaBashCodeExecutionResultBlock`

            - `content: Array<BetaBashCodeExecutionOutputBlock>`

              - `file_id: string`

              - `type: "bash_code_execution_output"`

                - `"bash_code_execution_output"`

            - `return_code: number`

            - `stderr: string`

            - `stdout: string`

            - `type: "bash_code_execution_result"`

              - `"bash_code_execution_result"`

        - `tool_use_id: string`

        - `type: "bash_code_execution_tool_result"`

          - `"bash_code_execution_tool_result"`

      - `BetaTextEditorCodeExecutionToolResultBlock`

        - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

          - `BetaTextEditorCodeExecutionToolResultError`

            - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

              - `"file_not_found"`

            - `error_message: string | null`

            - `type: "text_editor_code_execution_tool_result_error"`

              - `"text_editor_code_execution_tool_result_error"`

          - `BetaTextEditorCodeExecutionViewResultBlock`

            - `content: string`

            - `file_type: "text" | "image" | "pdf"`

              - `"text"`

              - `"image"`

              - `"pdf"`

            - `num_lines: number | null`

            - `start_line: number | null`

            - `total_lines: number | null`

            - `type: "text_editor_code_execution_view_result"`

              - `"text_editor_code_execution_view_result"`

          - `BetaTextEditorCodeExecutionCreateResultBlock`

            - `is_file_update: boolean`

            - `type: "text_editor_code_execution_create_result"`

              - `"text_editor_code_execution_create_result"`

          - `BetaTextEditorCodeExecutionStrReplaceResultBlock`

            - `lines: Array<string> | null`

            - `new_lines: number | null`

            - `new_start: number | null`

            - `old_lines: number | null`

            - `old_start: number | null`

            - `type: "text_editor_code_execution_str_replace_result"`

              - `"text_editor_code_execution_str_replace_result"`

        - `tool_use_id: string`

        - `type: "text_editor_code_execution_tool_result"`

          - `"text_editor_code_execution_tool_result"`

      - `BetaToolSearchToolResultBlock`

        - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

          - `BetaToolSearchToolResultError`

            - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

            - `error_message: string | null`

            - `type: "tool_search_tool_result_error"`

              - `"tool_search_tool_result_error"`

          - `BetaToolSearchToolSearchResultBlock`

            - `tool_references: Array<BetaToolReferenceBlock>`

              - `tool_name: string`

              - `type: "tool_reference"`

                - `"tool_reference"`

            - `type: "tool_search_tool_search_result"`

              - `"tool_search_tool_search_result"`

        - `tool_use_id: string`

        - `type: "tool_search_tool_result"`

          - `"tool_search_tool_result"`

      - `BetaMCPToolUseBlock`

        - `id: string`

        - `input: Record<string, unknown>`

        - `name: string`

          The name of the MCP tool

        - `server_name: string`

          The name of the MCP server

        - `type: "mcp_tool_use"`

          - `"mcp_tool_use"`

      - `BetaMCPToolResultBlock`

        - `content: string | Array<BetaTextBlock>`

          - `string`

          - `Array<BetaTextBlock>`

            - `citations: Array<BetaTextCitation> | null`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `BetaCitationCharLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_char_index: number`

                - `file_id: string | null`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `BetaCitationPageLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_page_number: number`

                - `file_id: string | null`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `BetaCitationContentBlockLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_block_index: number`

                - `file_id: string | null`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `BetaCitationsWebSearchResultLocation`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string | null`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `BetaCitationSearchResultLocation`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string | null`

                - `type: "search_result_location"`

                  - `"search_result_location"`

            - `text: string`

            - `type: "text"`

              - `"text"`

        - `is_error: boolean`

        - `tool_use_id: string`

        - `type: "mcp_tool_result"`

          - `"mcp_tool_result"`

      - `BetaContainerUploadBlock`

        Response model for a file uploaded to the container.

        - `file_id: string`

        - `type: "container_upload"`

          - `"container_upload"`

    - `index: number`

    - `type: "content_block_start"`

      - `"content_block_start"`

  - `BetaRawContentBlockDeltaEvent`

    - `delta: BetaRawContentBlockDelta`

      - `BetaTextDelta`

        - `text: string`

        - `type: "text_delta"`

          - `"text_delta"`

      - `BetaInputJSONDelta`

        - `partial_json: string`

        - `type: "input_json_delta"`

          - `"input_json_delta"`

      - `BetaCitationsDelta`

        - `citation: BetaCitationCharLocation | BetaCitationPageLocation | BetaCitationContentBlockLocation | 2 more`

          - `BetaCitationCharLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_char_index: number`

            - `file_id: string | null`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `BetaCitationPageLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_page_number: number`

            - `file_id: string | null`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `BetaCitationContentBlockLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_block_index: number`

            - `file_id: string | null`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `BetaCitationsWebSearchResultLocation`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string | null`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `BetaCitationSearchResultLocation`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string | null`

            - `type: "search_result_location"`

              - `"search_result_location"`

        - `type: "citations_delta"`

          - `"citations_delta"`

      - `BetaThinkingDelta`

        - `thinking: string`

        - `type: "thinking_delta"`

          - `"thinking_delta"`

      - `BetaSignatureDelta`

        - `signature: string`

        - `type: "signature_delta"`

          - `"signature_delta"`

    - `index: number`

    - `type: "content_block_delta"`

      - `"content_block_delta"`

  - `BetaRawContentBlockStopEvent`

    - `index: number`

    - `type: "content_block_stop"`

      - `"content_block_stop"`

### Beta Redacted Thinking Block

- `BetaRedactedThinkingBlock`

  - `data: string`

  - `type: "redacted_thinking"`

    - `"redacted_thinking"`

### Beta Redacted Thinking Block Param

- `BetaRedactedThinkingBlockParam`

  - `data: string`

  - `type: "redacted_thinking"`

    - `"redacted_thinking"`

### Beta Request Document Block

- `BetaRequestDocumentBlock`

  - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

    - `BetaBase64PDFSource`

      - `data: string`

      - `media_type: "application/pdf"`

        - `"application/pdf"`

      - `type: "base64"`

        - `"base64"`

    - `BetaPlainTextSource`

      - `data: string`

      - `media_type: "text/plain"`

        - `"text/plain"`

      - `type: "text"`

        - `"text"`

    - `BetaContentBlockSource`

      - `content: string | Array<BetaContentBlockSourceContent>`

        - `string`

        - `Array<BetaContentBlockSourceContent>`

          - `BetaTextBlockParam`

            - `text: string`

            - `type: "text"`

              - `"text"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `citations?: Array<BetaTextCitationParam> | null`

              - `BetaCitationCharLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_char_index: number`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `BetaCitationPageLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_page_number: number`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `BetaCitationContentBlockLocationParam`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_block_index: number`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `BetaCitationWebSearchResultLocationParam`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string | null`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `BetaCitationSearchResultLocationParam`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string | null`

                - `type: "search_result_location"`

                  - `"search_result_location"`

          - `BetaImageBlockParam`

            - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

              - `BetaBase64ImageSource`

                - `data: string`

                - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                  - `"image/jpeg"`

                  - `"image/png"`

                  - `"image/gif"`

                  - `"image/webp"`

                - `type: "base64"`

                  - `"base64"`

              - `BetaURLImageSource`

                - `type: "url"`

                  - `"url"`

                - `url: string`

              - `BetaFileImageSource`

                - `file_id: string`

                - `type: "file"`

                  - `"file"`

            - `type: "image"`

              - `"image"`

            - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `BetaURLPDFSource`

      - `type: "url"`

        - `"url"`

      - `url: string`

    - `BetaFileDocumentSource`

      - `file_id: string`

      - `type: "file"`

        - `"file"`

  - `type: "document"`

    - `"document"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `citations?: BetaCitationsConfigParam | null`

    - `enabled?: boolean`

  - `context?: string | null`

  - `title?: string | null`

### Beta Request MCP Server Tool Configuration

- `BetaRequestMCPServerToolConfiguration`

  - `allowed_tools?: Array<string> | null`

  - `enabled?: boolean | null`

### Beta Request MCP Server URL Definition

- `BetaRequestMCPServerURLDefinition`

  - `name: string`

  - `type: "url"`

    - `"url"`

  - `url: string`

  - `authorization_token?: string | null`

  - `tool_configuration?: BetaRequestMCPServerToolConfiguration | null`

    - `allowed_tools?: Array<string> | null`

    - `enabled?: boolean | null`

### Beta Request MCP Tool Result Block Param

- `BetaRequestMCPToolResultBlockParam`

  - `tool_use_id: string`

  - `type: "mcp_tool_result"`

    - `"mcp_tool_result"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `content?: string | Array<BetaTextBlockParam>`

    - `string`

    - `Array<BetaTextBlockParam>`

      - `text: string`

      - `type: "text"`

        - `"text"`

      - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `citations?: Array<BetaTextCitationParam> | null`

        - `BetaCitationCharLocationParam`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_char_index: number`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `BetaCitationPageLocationParam`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_page_number: number`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `BetaCitationContentBlockLocationParam`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string | null`

          - `end_block_index: number`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `BetaCitationWebSearchResultLocationParam`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string | null`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `BetaCitationSearchResultLocationParam`

          - `cited_text: string`

          - `end_block_index: number`

          - `search_result_index: number`

          - `source: string`

          - `start_block_index: number`

          - `title: string | null`

          - `type: "search_result_location"`

            - `"search_result_location"`

  - `is_error?: boolean`

### Beta Search Result Block Param

- `BetaSearchResultBlockParam`

  - `content: Array<BetaTextBlockParam>`

    - `text: string`

    - `type: "text"`

      - `"text"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `citations?: Array<BetaTextCitationParam> | null`

      - `BetaCitationCharLocationParam`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_char_index: number`

        - `start_char_index: number`

        - `type: "char_location"`

          - `"char_location"`

      - `BetaCitationPageLocationParam`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_page_number: number`

        - `start_page_number: number`

        - `type: "page_location"`

          - `"page_location"`

      - `BetaCitationContentBlockLocationParam`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string | null`

        - `end_block_index: number`

        - `start_block_index: number`

        - `type: "content_block_location"`

          - `"content_block_location"`

      - `BetaCitationWebSearchResultLocationParam`

        - `cited_text: string`

        - `encrypted_index: string`

        - `title: string | null`

        - `type: "web_search_result_location"`

          - `"web_search_result_location"`

        - `url: string`

      - `BetaCitationSearchResultLocationParam`

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

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `citations?: BetaCitationsConfigParam`

    - `enabled?: boolean`

### Beta Server Tool Caller

- `BetaServerToolCaller`

  Tool invocation generated by a server-side tool.

  - `tool_id: string`

  - `type: "code_execution_20250825"`

    - `"code_execution_20250825"`

### Beta Server Tool Usage

- `BetaServerToolUsage`

  - `web_fetch_requests: number`

    The number of web fetch tool requests.

  - `web_search_requests: number`

    The number of web search tool requests.

### Beta Server Tool Use Block

- `BetaServerToolUseBlock`

  - `id: string`

  - `caller: BetaDirectCaller | BetaServerToolCaller`

    Tool invocation directly from the model.

    - `BetaDirectCaller`

      Tool invocation directly from the model.

      - `type: "direct"`

        - `"direct"`

    - `BetaServerToolCaller`

      Tool invocation generated by a server-side tool.

      - `tool_id: string`

      - `type: "code_execution_20250825"`

        - `"code_execution_20250825"`

  - `input: Record<string, unknown>`

  - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

    - `"web_search"`

    - `"web_fetch"`

    - `"code_execution"`

    - `"bash_code_execution"`

    - `"text_editor_code_execution"`

    - `"tool_search_tool_regex"`

    - `"tool_search_tool_bm25"`

  - `type: "server_tool_use"`

    - `"server_tool_use"`

### Beta Server Tool Use Block Param

- `BetaServerToolUseBlockParam`

  - `id: string`

  - `input: Record<string, unknown>`

  - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

    - `"web_search"`

    - `"web_fetch"`

    - `"code_execution"`

    - `"bash_code_execution"`

    - `"text_editor_code_execution"`

    - `"tool_search_tool_regex"`

    - `"tool_search_tool_bm25"`

  - `type: "server_tool_use"`

    - `"server_tool_use"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `caller?: BetaDirectCaller | BetaServerToolCaller`

    Tool invocation directly from the model.

    - `BetaDirectCaller`

      Tool invocation directly from the model.

      - `type: "direct"`

        - `"direct"`

    - `BetaServerToolCaller`

      Tool invocation generated by a server-side tool.

      - `tool_id: string`

      - `type: "code_execution_20250825"`

        - `"code_execution_20250825"`

### Beta Signature Delta

- `BetaSignatureDelta`

  - `signature: string`

  - `type: "signature_delta"`

    - `"signature_delta"`

### Beta Skill

- `BetaSkill`

  A skill that was loaded in a container (response model).

  - `skill_id: string`

    Skill ID

  - `type: "anthropic" | "custom"`

    Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

    - `"anthropic"`

    - `"custom"`

  - `version: string`

    Skill version or 'latest' for most recent version

### Beta Skill Params

- `BetaSkillParams`

  Specification for a skill to be loaded in a container (request model).

  - `skill_id: string`

    Skill ID

  - `type: "anthropic" | "custom"`

    Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

    - `"anthropic"`

    - `"custom"`

  - `version?: string`

    Skill version or 'latest' for most recent version

### Beta Stop Reason

- `BetaStopReason = "end_turn" | "max_tokens" | "stop_sequence" | 4 more`

  - `"end_turn"`

  - `"max_tokens"`

  - `"stop_sequence"`

  - `"tool_use"`

  - `"pause_turn"`

  - `"refusal"`

  - `"model_context_window_exceeded"`

### Beta Text Block

- `BetaTextBlock`

  - `citations: Array<BetaTextCitation> | null`

    Citations supporting the text block.

    The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

    - `BetaCitationCharLocation`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string | null`

      - `end_char_index: number`

      - `file_id: string | null`

      - `start_char_index: number`

      - `type: "char_location"`

        - `"char_location"`

    - `BetaCitationPageLocation`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string | null`

      - `end_page_number: number`

      - `file_id: string | null`

      - `start_page_number: number`

      - `type: "page_location"`

        - `"page_location"`

    - `BetaCitationContentBlockLocation`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string | null`

      - `end_block_index: number`

      - `file_id: string | null`

      - `start_block_index: number`

      - `type: "content_block_location"`

        - `"content_block_location"`

    - `BetaCitationsWebSearchResultLocation`

      - `cited_text: string`

      - `encrypted_index: string`

      - `title: string | null`

      - `type: "web_search_result_location"`

        - `"web_search_result_location"`

      - `url: string`

    - `BetaCitationSearchResultLocation`

      - `cited_text: string`

      - `end_block_index: number`

      - `search_result_index: number`

      - `source: string`

      - `start_block_index: number`

      - `title: string | null`

      - `type: "search_result_location"`

        - `"search_result_location"`

  - `text: string`

  - `type: "text"`

    - `"text"`

### Beta Text Block Param

- `BetaTextBlockParam`

  - `text: string`

  - `type: "text"`

    - `"text"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `citations?: Array<BetaTextCitationParam> | null`

    - `BetaCitationCharLocationParam`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string | null`

      - `end_char_index: number`

      - `start_char_index: number`

      - `type: "char_location"`

        - `"char_location"`

    - `BetaCitationPageLocationParam`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string | null`

      - `end_page_number: number`

      - `start_page_number: number`

      - `type: "page_location"`

        - `"page_location"`

    - `BetaCitationContentBlockLocationParam`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string | null`

      - `end_block_index: number`

      - `start_block_index: number`

      - `type: "content_block_location"`

        - `"content_block_location"`

    - `BetaCitationWebSearchResultLocationParam`

      - `cited_text: string`

      - `encrypted_index: string`

      - `title: string | null`

      - `type: "web_search_result_location"`

        - `"web_search_result_location"`

      - `url: string`

    - `BetaCitationSearchResultLocationParam`

      - `cited_text: string`

      - `end_block_index: number`

      - `search_result_index: number`

      - `source: string`

      - `start_block_index: number`

      - `title: string | null`

      - `type: "search_result_location"`

        - `"search_result_location"`

### Beta Text Citation

- `BetaTextCitation = BetaCitationCharLocation | BetaCitationPageLocation | BetaCitationContentBlockLocation | 2 more`

  - `BetaCitationCharLocation`

    - `cited_text: string`

    - `document_index: number`

    - `document_title: string | null`

    - `end_char_index: number`

    - `file_id: string | null`

    - `start_char_index: number`

    - `type: "char_location"`

      - `"char_location"`

  - `BetaCitationPageLocation`

    - `cited_text: string`

    - `document_index: number`

    - `document_title: string | null`

    - `end_page_number: number`

    - `file_id: string | null`

    - `start_page_number: number`

    - `type: "page_location"`

      - `"page_location"`

  - `BetaCitationContentBlockLocation`

    - `cited_text: string`

    - `document_index: number`

    - `document_title: string | null`

    - `end_block_index: number`

    - `file_id: string | null`

    - `start_block_index: number`

    - `type: "content_block_location"`

      - `"content_block_location"`

  - `BetaCitationsWebSearchResultLocation`

    - `cited_text: string`

    - `encrypted_index: string`

    - `title: string | null`

    - `type: "web_search_result_location"`

      - `"web_search_result_location"`

    - `url: string`

  - `BetaCitationSearchResultLocation`

    - `cited_text: string`

    - `end_block_index: number`

    - `search_result_index: number`

    - `source: string`

    - `start_block_index: number`

    - `title: string | null`

    - `type: "search_result_location"`

      - `"search_result_location"`

### Beta Text Citation Param

- `BetaTextCitationParam = BetaCitationCharLocationParam | BetaCitationPageLocationParam | BetaCitationContentBlockLocationParam | 2 more`

  - `BetaCitationCharLocationParam`

    - `cited_text: string`

    - `document_index: number`

    - `document_title: string | null`

    - `end_char_index: number`

    - `start_char_index: number`

    - `type: "char_location"`

      - `"char_location"`

  - `BetaCitationPageLocationParam`

    - `cited_text: string`

    - `document_index: number`

    - `document_title: string | null`

    - `end_page_number: number`

    - `start_page_number: number`

    - `type: "page_location"`

      - `"page_location"`

  - `BetaCitationContentBlockLocationParam`

    - `cited_text: string`

    - `document_index: number`

    - `document_title: string | null`

    - `end_block_index: number`

    - `start_block_index: number`

    - `type: "content_block_location"`

      - `"content_block_location"`

  - `BetaCitationWebSearchResultLocationParam`

    - `cited_text: string`

    - `encrypted_index: string`

    - `title: string | null`

    - `type: "web_search_result_location"`

      - `"web_search_result_location"`

    - `url: string`

  - `BetaCitationSearchResultLocationParam`

    - `cited_text: string`

    - `end_block_index: number`

    - `search_result_index: number`

    - `source: string`

    - `start_block_index: number`

    - `title: string | null`

    - `type: "search_result_location"`

      - `"search_result_location"`

### Beta Text Delta

- `BetaTextDelta`

  - `text: string`

  - `type: "text_delta"`

    - `"text_delta"`

### Beta Text Editor Code Execution Create Result Block

- `BetaTextEditorCodeExecutionCreateResultBlock`

  - `is_file_update: boolean`

  - `type: "text_editor_code_execution_create_result"`

    - `"text_editor_code_execution_create_result"`

### Beta Text Editor Code Execution Create Result Block Param

- `BetaTextEditorCodeExecutionCreateResultBlockParam`

  - `is_file_update: boolean`

  - `type: "text_editor_code_execution_create_result"`

    - `"text_editor_code_execution_create_result"`

### Beta Text Editor Code Execution Str Replace Result Block

- `BetaTextEditorCodeExecutionStrReplaceResultBlock`

  - `lines: Array<string> | null`

  - `new_lines: number | null`

  - `new_start: number | null`

  - `old_lines: number | null`

  - `old_start: number | null`

  - `type: "text_editor_code_execution_str_replace_result"`

    - `"text_editor_code_execution_str_replace_result"`

### Beta Text Editor Code Execution Str Replace Result Block Param

- `BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

  - `type: "text_editor_code_execution_str_replace_result"`

    - `"text_editor_code_execution_str_replace_result"`

  - `lines?: Array<string> | null`

  - `new_lines?: number | null`

  - `new_start?: number | null`

  - `old_lines?: number | null`

  - `old_start?: number | null`

### Beta Text Editor Code Execution Tool Result Block

- `BetaTextEditorCodeExecutionToolResultBlock`

  - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

    - `BetaTextEditorCodeExecutionToolResultError`

      - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

        - `"invalid_tool_input"`

        - `"unavailable"`

        - `"too_many_requests"`

        - `"execution_time_exceeded"`

        - `"file_not_found"`

      - `error_message: string | null`

      - `type: "text_editor_code_execution_tool_result_error"`

        - `"text_editor_code_execution_tool_result_error"`

    - `BetaTextEditorCodeExecutionViewResultBlock`

      - `content: string`

      - `file_type: "text" | "image" | "pdf"`

        - `"text"`

        - `"image"`

        - `"pdf"`

      - `num_lines: number | null`

      - `start_line: number | null`

      - `total_lines: number | null`

      - `type: "text_editor_code_execution_view_result"`

        - `"text_editor_code_execution_view_result"`

    - `BetaTextEditorCodeExecutionCreateResultBlock`

      - `is_file_update: boolean`

      - `type: "text_editor_code_execution_create_result"`

        - `"text_editor_code_execution_create_result"`

    - `BetaTextEditorCodeExecutionStrReplaceResultBlock`

      - `lines: Array<string> | null`

      - `new_lines: number | null`

      - `new_start: number | null`

      - `old_lines: number | null`

      - `old_start: number | null`

      - `type: "text_editor_code_execution_str_replace_result"`

        - `"text_editor_code_execution_str_replace_result"`

  - `tool_use_id: string`

  - `type: "text_editor_code_execution_tool_result"`

    - `"text_editor_code_execution_tool_result"`

### Beta Text Editor Code Execution Tool Result Block Param

- `BetaTextEditorCodeExecutionToolResultBlockParam`

  - `content: BetaTextEditorCodeExecutionToolResultErrorParam | BetaTextEditorCodeExecutionViewResultBlockParam | BetaTextEditorCodeExecutionCreateResultBlockParam | BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

    - `BetaTextEditorCodeExecutionToolResultErrorParam`

      - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

        - `"invalid_tool_input"`

        - `"unavailable"`

        - `"too_many_requests"`

        - `"execution_time_exceeded"`

        - `"file_not_found"`

      - `type: "text_editor_code_execution_tool_result_error"`

        - `"text_editor_code_execution_tool_result_error"`

      - `error_message?: string | null`

    - `BetaTextEditorCodeExecutionViewResultBlockParam`

      - `content: string`

      - `file_type: "text" | "image" | "pdf"`

        - `"text"`

        - `"image"`

        - `"pdf"`

      - `type: "text_editor_code_execution_view_result"`

        - `"text_editor_code_execution_view_result"`

      - `num_lines?: number | null`

      - `start_line?: number | null`

      - `total_lines?: number | null`

    - `BetaTextEditorCodeExecutionCreateResultBlockParam`

      - `is_file_update: boolean`

      - `type: "text_editor_code_execution_create_result"`

        - `"text_editor_code_execution_create_result"`

    - `BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

      - `type: "text_editor_code_execution_str_replace_result"`

        - `"text_editor_code_execution_str_replace_result"`

      - `lines?: Array<string> | null`

      - `new_lines?: number | null`

      - `new_start?: number | null`

      - `old_lines?: number | null`

      - `old_start?: number | null`

  - `tool_use_id: string`

  - `type: "text_editor_code_execution_tool_result"`

    - `"text_editor_code_execution_tool_result"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta Text Editor Code Execution Tool Result Error

- `BetaTextEditorCodeExecutionToolResultError`

  - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

    - `"file_not_found"`

  - `error_message: string | null`

  - `type: "text_editor_code_execution_tool_result_error"`

    - `"text_editor_code_execution_tool_result_error"`

### Beta Text Editor Code Execution Tool Result Error Param

- `BetaTextEditorCodeExecutionToolResultErrorParam`

  - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

    - `"file_not_found"`

  - `type: "text_editor_code_execution_tool_result_error"`

    - `"text_editor_code_execution_tool_result_error"`

  - `error_message?: string | null`

### Beta Text Editor Code Execution View Result Block

- `BetaTextEditorCodeExecutionViewResultBlock`

  - `content: string`

  - `file_type: "text" | "image" | "pdf"`

    - `"text"`

    - `"image"`

    - `"pdf"`

  - `num_lines: number | null`

  - `start_line: number | null`

  - `total_lines: number | null`

  - `type: "text_editor_code_execution_view_result"`

    - `"text_editor_code_execution_view_result"`

### Beta Text Editor Code Execution View Result Block Param

- `BetaTextEditorCodeExecutionViewResultBlockParam`

  - `content: string`

  - `file_type: "text" | "image" | "pdf"`

    - `"text"`

    - `"image"`

    - `"pdf"`

  - `type: "text_editor_code_execution_view_result"`

    - `"text_editor_code_execution_view_result"`

  - `num_lines?: number | null`

  - `start_line?: number | null`

  - `total_lines?: number | null`

### Beta Thinking Block

- `BetaThinkingBlock`

  - `signature: string`

  - `thinking: string`

  - `type: "thinking"`

    - `"thinking"`

### Beta Thinking Block Param

- `BetaThinkingBlockParam`

  - `signature: string`

  - `thinking: string`

  - `type: "thinking"`

    - `"thinking"`

### Beta Thinking Config Disabled

- `BetaThinkingConfigDisabled`

  - `type: "disabled"`

    - `"disabled"`

### Beta Thinking Config Enabled

- `BetaThinkingConfigEnabled`

  - `budget_tokens: number`

    Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

    Must be ≥1024 and less than `max_tokens`.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `type: "enabled"`

    - `"enabled"`

### Beta Thinking Config Param

- `BetaThinkingConfigParam = BetaThinkingConfigEnabled | BetaThinkingConfigDisabled`

  Configuration for enabling Claude's extended thinking.

  When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

  See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `BetaThinkingConfigEnabled`

    - `budget_tokens: number`

      Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

      Must be ≥1024 and less than `max_tokens`.

      See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

    - `type: "enabled"`

      - `"enabled"`

  - `BetaThinkingConfigDisabled`

    - `type: "disabled"`

      - `"disabled"`

### Beta Thinking Delta

- `BetaThinkingDelta`

  - `thinking: string`

  - `type: "thinking_delta"`

    - `"thinking_delta"`

### Beta Thinking Turns

- `BetaThinkingTurns`

  - `type: "thinking_turns"`

    - `"thinking_turns"`

  - `value: number`

### Beta Tool

- `BetaTool`

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

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `description?: string`

    Description of what this tool does.

    Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

  - `input_examples?: Array<Record<string, unknown>>`

  - `strict?: boolean`

  - `type?: "custom" | null`

    - `"custom"`

### Beta Tool Bash 20241022

- `BetaToolBash20241022`

  - `name: "bash"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"bash"`

  - `type: "bash_20241022"`

    - `"bash_20241022"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `input_examples?: Array<Record<string, unknown>>`

  - `strict?: boolean`

### Beta Tool Bash 20250124

- `BetaToolBash20250124`

  - `name: "bash"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"bash"`

  - `type: "bash_20250124"`

    - `"bash_20250124"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `input_examples?: Array<Record<string, unknown>>`

  - `strict?: boolean`

### Beta Tool Choice

- `BetaToolChoice = BetaToolChoiceAuto | BetaToolChoiceAny | BetaToolChoiceTool | BetaToolChoiceNone`

  How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `BetaToolChoiceAuto`

    The model will automatically decide whether to use tools.

    - `type: "auto"`

      - `"auto"`

    - `disable_parallel_tool_use?: boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output at most one tool use.

  - `BetaToolChoiceAny`

    The model will use any available tools.

    - `type: "any"`

      - `"any"`

    - `disable_parallel_tool_use?: boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output exactly one tool use.

  - `BetaToolChoiceTool`

    The model will use the specified tool with `tool_choice.name`.

    - `name: string`

      The name of the tool to use.

    - `type: "tool"`

      - `"tool"`

    - `disable_parallel_tool_use?: boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output exactly one tool use.

  - `BetaToolChoiceNone`

    The model will not be allowed to use tools.

    - `type: "none"`

      - `"none"`

### Beta Tool Choice Any

- `BetaToolChoiceAny`

  The model will use any available tools.

  - `type: "any"`

    - `"any"`

  - `disable_parallel_tool_use?: boolean`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output exactly one tool use.

### Beta Tool Choice Auto

- `BetaToolChoiceAuto`

  The model will automatically decide whether to use tools.

  - `type: "auto"`

    - `"auto"`

  - `disable_parallel_tool_use?: boolean`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output at most one tool use.

### Beta Tool Choice None

- `BetaToolChoiceNone`

  The model will not be allowed to use tools.

  - `type: "none"`

    - `"none"`

### Beta Tool Choice Tool

- `BetaToolChoiceTool`

  The model will use the specified tool with `tool_choice.name`.

  - `name: string`

    The name of the tool to use.

  - `type: "tool"`

    - `"tool"`

  - `disable_parallel_tool_use?: boolean`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output exactly one tool use.

### Beta Tool Computer Use 20241022

- `BetaToolComputerUse20241022`

  - `display_height_px: number`

    The height of the display in pixels.

  - `display_width_px: number`

    The width of the display in pixels.

  - `name: "computer"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"computer"`

  - `type: "computer_20241022"`

    - `"computer_20241022"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `display_number?: number | null`

    The X11 display number (e.g. 0, 1) for the display.

  - `input_examples?: Array<Record<string, unknown>>`

  - `strict?: boolean`

### Beta Tool Computer Use 20250124

- `BetaToolComputerUse20250124`

  - `display_height_px: number`

    The height of the display in pixels.

  - `display_width_px: number`

    The width of the display in pixels.

  - `name: "computer"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"computer"`

  - `type: "computer_20250124"`

    - `"computer_20250124"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `display_number?: number | null`

    The X11 display number (e.g. 0, 1) for the display.

  - `input_examples?: Array<Record<string, unknown>>`

  - `strict?: boolean`

### Beta Tool Computer Use 20251124

- `BetaToolComputerUse20251124`

  - `display_height_px: number`

    The height of the display in pixels.

  - `display_width_px: number`

    The width of the display in pixels.

  - `name: "computer"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"computer"`

  - `type: "computer_20251124"`

    - `"computer_20251124"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `display_number?: number | null`

    The X11 display number (e.g. 0, 1) for the display.

  - `enable_zoom?: boolean`

    Whether to enable an action to take a zoomed-in screenshot of the screen.

  - `input_examples?: Array<Record<string, unknown>>`

  - `strict?: boolean`

### Beta Tool Reference Block

- `BetaToolReferenceBlock`

  - `tool_name: string`

  - `type: "tool_reference"`

    - `"tool_reference"`

### Beta Tool Reference Block Param

- `BetaToolReferenceBlockParam`

  Tool reference block that can be included in tool_result content.

  - `tool_name: string`

  - `type: "tool_reference"`

    - `"tool_reference"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta Tool Result Block Param

- `BetaToolResultBlockParam`

  - `tool_use_id: string`

  - `type: "tool_result"`

    - `"tool_result"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `content?: string | Array<BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more>`

    - `string`

    - `Array<BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more>`

      - `BetaTextBlockParam`

        - `text: string`

        - `type: "text"`

          - `"text"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `citations?: Array<BetaTextCitationParam> | null`

          - `BetaCitationCharLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_char_index: number`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `BetaCitationPageLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_page_number: number`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `BetaCitationContentBlockLocationParam`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_block_index: number`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `BetaCitationWebSearchResultLocationParam`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string | null`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `BetaCitationSearchResultLocationParam`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string | null`

            - `type: "search_result_location"`

              - `"search_result_location"`

      - `BetaImageBlockParam`

        - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

          - `BetaBase64ImageSource`

            - `data: string`

            - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

              - `"image/jpeg"`

              - `"image/png"`

              - `"image/gif"`

              - `"image/webp"`

            - `type: "base64"`

              - `"base64"`

          - `BetaURLImageSource`

            - `type: "url"`

              - `"url"`

            - `url: string`

          - `BetaFileImageSource`

            - `file_id: string`

            - `type: "file"`

              - `"file"`

        - `type: "image"`

          - `"image"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `BetaSearchResultBlockParam`

        - `content: Array<BetaTextBlockParam>`

          - `text: string`

          - `type: "text"`

            - `"text"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `citations?: Array<BetaTextCitationParam> | null`

            - `BetaCitationCharLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_char_index: number`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `BetaCitationPageLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_page_number: number`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `BetaCitationContentBlockLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_block_index: number`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `BetaCitationWebSearchResultLocationParam`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string | null`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `BetaCitationSearchResultLocationParam`

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

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `citations?: BetaCitationsConfigParam`

          - `enabled?: boolean`

      - `BetaRequestDocumentBlock`

        - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

          - `BetaBase64PDFSource`

            - `data: string`

            - `media_type: "application/pdf"`

              - `"application/pdf"`

            - `type: "base64"`

              - `"base64"`

          - `BetaPlainTextSource`

            - `data: string`

            - `media_type: "text/plain"`

              - `"text/plain"`

            - `type: "text"`

              - `"text"`

          - `BetaContentBlockSource`

            - `content: string | Array<BetaContentBlockSourceContent>`

              - `string`

              - `Array<BetaContentBlockSourceContent>`

                - `BetaTextBlockParam`

                  - `text: string`

                  - `type: "text"`

                    - `"text"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

                  - `citations?: Array<BetaTextCitationParam> | null`

                    - `BetaCitationCharLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_char_index: number`

                      - `start_char_index: number`

                      - `type: "char_location"`

                        - `"char_location"`

                    - `BetaCitationPageLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_page_number: number`

                      - `start_page_number: number`

                      - `type: "page_location"`

                        - `"page_location"`

                    - `BetaCitationContentBlockLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_block_index: number`

                      - `start_block_index: number`

                      - `type: "content_block_location"`

                        - `"content_block_location"`

                    - `BetaCitationWebSearchResultLocationParam`

                      - `cited_text: string`

                      - `encrypted_index: string`

                      - `title: string | null`

                      - `type: "web_search_result_location"`

                        - `"web_search_result_location"`

                      - `url: string`

                    - `BetaCitationSearchResultLocationParam`

                      - `cited_text: string`

                      - `end_block_index: number`

                      - `search_result_index: number`

                      - `source: string`

                      - `start_block_index: number`

                      - `title: string | null`

                      - `type: "search_result_location"`

                        - `"search_result_location"`

                - `BetaImageBlockParam`

                  - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                    - `BetaBase64ImageSource`

                      - `data: string`

                      - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                        - `"image/jpeg"`

                        - `"image/png"`

                        - `"image/gif"`

                        - `"image/webp"`

                      - `type: "base64"`

                        - `"base64"`

                    - `BetaURLImageSource`

                      - `type: "url"`

                        - `"url"`

                      - `url: string`

                    - `BetaFileImageSource`

                      - `file_id: string`

                      - `type: "file"`

                        - `"file"`

                  - `type: "image"`

                    - `"image"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `BetaURLPDFSource`

            - `type: "url"`

              - `"url"`

            - `url: string`

          - `BetaFileDocumentSource`

            - `file_id: string`

            - `type: "file"`

              - `"file"`

        - `type: "document"`

          - `"document"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `citations?: BetaCitationsConfigParam | null`

          - `enabled?: boolean`

        - `context?: string | null`

        - `title?: string | null`

      - `BetaToolReferenceBlockParam`

        Tool reference block that can be included in tool_result content.

        - `tool_name: string`

        - `type: "tool_reference"`

          - `"tool_reference"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `is_error?: boolean`

### Beta Tool Search Tool Bm25 20251119

- `BetaToolSearchToolBm25_20251119`

  - `name: "tool_search_tool_bm25"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"tool_search_tool_bm25"`

  - `type: "tool_search_tool_bm25_20251119" | "tool_search_tool_bm25"`

    - `"tool_search_tool_bm25_20251119"`

    - `"tool_search_tool_bm25"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `strict?: boolean`

### Beta Tool Search Tool Regex 20251119

- `BetaToolSearchToolRegex20251119`

  - `name: "tool_search_tool_regex"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"tool_search_tool_regex"`

  - `type: "tool_search_tool_regex_20251119" | "tool_search_tool_regex"`

    - `"tool_search_tool_regex_20251119"`

    - `"tool_search_tool_regex"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `strict?: boolean`

### Beta Tool Search Tool Result Block

- `BetaToolSearchToolResultBlock`

  - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

    - `BetaToolSearchToolResultError`

      - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

        - `"invalid_tool_input"`

        - `"unavailable"`

        - `"too_many_requests"`

        - `"execution_time_exceeded"`

      - `error_message: string | null`

      - `type: "tool_search_tool_result_error"`

        - `"tool_search_tool_result_error"`

    - `BetaToolSearchToolSearchResultBlock`

      - `tool_references: Array<BetaToolReferenceBlock>`

        - `tool_name: string`

        - `type: "tool_reference"`

          - `"tool_reference"`

      - `type: "tool_search_tool_search_result"`

        - `"tool_search_tool_search_result"`

  - `tool_use_id: string`

  - `type: "tool_search_tool_result"`

    - `"tool_search_tool_result"`

### Beta Tool Search Tool Result Block Param

- `BetaToolSearchToolResultBlockParam`

  - `content: BetaToolSearchToolResultErrorParam | BetaToolSearchToolSearchResultBlockParam`

    - `BetaToolSearchToolResultErrorParam`

      - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

        - `"invalid_tool_input"`

        - `"unavailable"`

        - `"too_many_requests"`

        - `"execution_time_exceeded"`

      - `type: "tool_search_tool_result_error"`

        - `"tool_search_tool_result_error"`

    - `BetaToolSearchToolSearchResultBlockParam`

      - `tool_references: Array<BetaToolReferenceBlockParam>`

        - `tool_name: string`

        - `type: "tool_reference"`

          - `"tool_reference"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `type: "tool_search_tool_search_result"`

        - `"tool_search_tool_search_result"`

  - `tool_use_id: string`

  - `type: "tool_search_tool_result"`

    - `"tool_search_tool_result"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta Tool Search Tool Result Error

- `BetaToolSearchToolResultError`

  - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

  - `error_message: string | null`

  - `type: "tool_search_tool_result_error"`

    - `"tool_search_tool_result_error"`

### Beta Tool Search Tool Result Error Param

- `BetaToolSearchToolResultErrorParam`

  - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

  - `type: "tool_search_tool_result_error"`

    - `"tool_search_tool_result_error"`

### Beta Tool Search Tool Search Result Block

- `BetaToolSearchToolSearchResultBlock`

  - `tool_references: Array<BetaToolReferenceBlock>`

    - `tool_name: string`

    - `type: "tool_reference"`

      - `"tool_reference"`

  - `type: "tool_search_tool_search_result"`

    - `"tool_search_tool_search_result"`

### Beta Tool Search Tool Search Result Block Param

- `BetaToolSearchToolSearchResultBlockParam`

  - `tool_references: Array<BetaToolReferenceBlockParam>`

    - `tool_name: string`

    - `type: "tool_reference"`

      - `"tool_reference"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `type: "tool_search_tool_search_result"`

    - `"tool_search_tool_search_result"`

### Beta Tool Text Editor 20241022

- `BetaToolTextEditor20241022`

  - `name: "str_replace_editor"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"str_replace_editor"`

  - `type: "text_editor_20241022"`

    - `"text_editor_20241022"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `input_examples?: Array<Record<string, unknown>>`

  - `strict?: boolean`

### Beta Tool Text Editor 20250124

- `BetaToolTextEditor20250124`

  - `name: "str_replace_editor"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"str_replace_editor"`

  - `type: "text_editor_20250124"`

    - `"text_editor_20250124"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `input_examples?: Array<Record<string, unknown>>`

  - `strict?: boolean`

### Beta Tool Text Editor 20250429

- `BetaToolTextEditor20250429`

  - `name: "str_replace_based_edit_tool"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"str_replace_based_edit_tool"`

  - `type: "text_editor_20250429"`

    - `"text_editor_20250429"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `input_examples?: Array<Record<string, unknown>>`

  - `strict?: boolean`

### Beta Tool Text Editor 20250728

- `BetaToolTextEditor20250728`

  - `name: "str_replace_based_edit_tool"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"str_replace_based_edit_tool"`

  - `type: "text_editor_20250728"`

    - `"text_editor_20250728"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `input_examples?: Array<Record<string, unknown>>`

  - `max_characters?: number | null`

    Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

  - `strict?: boolean`

### Beta Tool Union

- `BetaToolUnion = BetaTool | BetaToolBash20241022 | BetaToolBash20250124 | 15 more`

  Configuration for a group of tools from an MCP server.

  Allows configuring enabled status and defer_loading for all tools
  from an MCP server, with optional per-tool overrides.

  - `BetaTool`

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

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `description?: string`

      Description of what this tool does.

      Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

    - `input_examples?: Array<Record<string, unknown>>`

    - `strict?: boolean`

    - `type?: "custom" | null`

      - `"custom"`

  - `BetaToolBash20241022`

    - `name: "bash"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"bash"`

    - `type: "bash_20241022"`

      - `"bash_20241022"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples?: Array<Record<string, unknown>>`

    - `strict?: boolean`

  - `BetaToolBash20250124`

    - `name: "bash"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"bash"`

    - `type: "bash_20250124"`

      - `"bash_20250124"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples?: Array<Record<string, unknown>>`

    - `strict?: boolean`

  - `BetaCodeExecutionTool20250522`

    - `name: "code_execution"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"code_execution"`

    - `type: "code_execution_20250522"`

      - `"code_execution_20250522"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `strict?: boolean`

  - `BetaCodeExecutionTool20250825`

    - `name: "code_execution"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"code_execution"`

    - `type: "code_execution_20250825"`

      - `"code_execution_20250825"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `strict?: boolean`

  - `BetaToolComputerUse20241022`

    - `display_height_px: number`

      The height of the display in pixels.

    - `display_width_px: number`

      The width of the display in pixels.

    - `name: "computer"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"computer"`

    - `type: "computer_20241022"`

      - `"computer_20241022"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `display_number?: number | null`

      The X11 display number (e.g. 0, 1) for the display.

    - `input_examples?: Array<Record<string, unknown>>`

    - `strict?: boolean`

  - `BetaMemoryTool20250818`

    - `name: "memory"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"memory"`

    - `type: "memory_20250818"`

      - `"memory_20250818"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples?: Array<Record<string, unknown>>`

    - `strict?: boolean`

  - `BetaToolComputerUse20250124`

    - `display_height_px: number`

      The height of the display in pixels.

    - `display_width_px: number`

      The width of the display in pixels.

    - `name: "computer"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"computer"`

    - `type: "computer_20250124"`

      - `"computer_20250124"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `display_number?: number | null`

      The X11 display number (e.g. 0, 1) for the display.

    - `input_examples?: Array<Record<string, unknown>>`

    - `strict?: boolean`

  - `BetaToolTextEditor20241022`

    - `name: "str_replace_editor"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_editor"`

    - `type: "text_editor_20241022"`

      - `"text_editor_20241022"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples?: Array<Record<string, unknown>>`

    - `strict?: boolean`

  - `BetaToolComputerUse20251124`

    - `display_height_px: number`

      The height of the display in pixels.

    - `display_width_px: number`

      The width of the display in pixels.

    - `name: "computer"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"computer"`

    - `type: "computer_20251124"`

      - `"computer_20251124"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `display_number?: number | null`

      The X11 display number (e.g. 0, 1) for the display.

    - `enable_zoom?: boolean`

      Whether to enable an action to take a zoomed-in screenshot of the screen.

    - `input_examples?: Array<Record<string, unknown>>`

    - `strict?: boolean`

  - `BetaToolTextEditor20250124`

    - `name: "str_replace_editor"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_editor"`

    - `type: "text_editor_20250124"`

      - `"text_editor_20250124"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples?: Array<Record<string, unknown>>`

    - `strict?: boolean`

  - `BetaToolTextEditor20250429`

    - `name: "str_replace_based_edit_tool"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_based_edit_tool"`

    - `type: "text_editor_20250429"`

      - `"text_editor_20250429"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples?: Array<Record<string, unknown>>`

    - `strict?: boolean`

  - `BetaToolTextEditor20250728`

    - `name: "str_replace_based_edit_tool"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_based_edit_tool"`

    - `type: "text_editor_20250728"`

      - `"text_editor_20250728"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples?: Array<Record<string, unknown>>`

    - `max_characters?: number | null`

      Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

    - `strict?: boolean`

  - `BetaWebSearchTool20250305`

    - `name: "web_search"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"web_search"`

    - `type: "web_search_20250305"`

      - `"web_search_20250305"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `allowed_domains?: Array<string> | null`

      If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

    - `blocked_domains?: Array<string> | null`

      If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `max_uses?: number | null`

      Maximum number of times the tool can be used in the API request.

    - `strict?: boolean`

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

  - `BetaWebFetchTool20250910`

    - `name: "web_fetch"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"web_fetch"`

    - `type: "web_fetch_20250910"`

      - `"web_fetch_20250910"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `allowed_domains?: Array<string> | null`

      List of domains to allow fetching from

    - `blocked_domains?: Array<string> | null`

      List of domains to block fetching from

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `citations?: BetaCitationsConfigParam | null`

      Citations configuration for fetched documents. Citations are disabled by default.

      - `enabled?: boolean`

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `max_content_tokens?: number | null`

      Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

    - `max_uses?: number | null`

      Maximum number of times the tool can be used in the API request.

    - `strict?: boolean`

  - `BetaToolSearchToolBm25_20251119`

    - `name: "tool_search_tool_bm25"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"tool_search_tool_bm25"`

    - `type: "tool_search_tool_bm25_20251119" | "tool_search_tool_bm25"`

      - `"tool_search_tool_bm25_20251119"`

      - `"tool_search_tool_bm25"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `strict?: boolean`

  - `BetaToolSearchToolRegex20251119`

    - `name: "tool_search_tool_regex"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"tool_search_tool_regex"`

    - `type: "tool_search_tool_regex_20251119" | "tool_search_tool_regex"`

      - `"tool_search_tool_regex_20251119"`

      - `"tool_search_tool_regex"`

    - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `defer_loading?: boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `strict?: boolean`

  - `BetaMCPToolset`

    Configuration for a group of tools from an MCP server.

    Allows configuring enabled status and defer_loading for all tools
    from an MCP server, with optional per-tool overrides.

    - `mcp_server_name: string`

      Name of the MCP server to configure tools for

    - `type: "mcp_toolset"`

      - `"mcp_toolset"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `configs?: Record<string, BetaMCPToolConfig> | null`

      Configuration overrides for specific tools, keyed by tool name

      - `defer_loading?: boolean`

      - `enabled?: boolean`

    - `default_config?: BetaMCPToolDefaultConfig`

      Default configuration applied to all tools from this server

      - `defer_loading?: boolean`

      - `enabled?: boolean`

### Beta Tool Use Block

- `BetaToolUseBlock`

  - `id: string`

  - `input: Record<string, unknown>`

  - `name: string`

  - `type: "tool_use"`

    - `"tool_use"`

  - `caller?: BetaDirectCaller | BetaServerToolCaller`

    Tool invocation directly from the model.

    - `BetaDirectCaller`

      Tool invocation directly from the model.

      - `type: "direct"`

        - `"direct"`

    - `BetaServerToolCaller`

      Tool invocation generated by a server-side tool.

      - `tool_id: string`

      - `type: "code_execution_20250825"`

        - `"code_execution_20250825"`

### Beta Tool Use Block Param

- `BetaToolUseBlockParam`

  - `id: string`

  - `input: Record<string, unknown>`

  - `name: string`

  - `type: "tool_use"`

    - `"tool_use"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `caller?: BetaDirectCaller | BetaServerToolCaller`

    Tool invocation directly from the model.

    - `BetaDirectCaller`

      Tool invocation directly from the model.

      - `type: "direct"`

        - `"direct"`

    - `BetaServerToolCaller`

      Tool invocation generated by a server-side tool.

      - `tool_id: string`

      - `type: "code_execution_20250825"`

        - `"code_execution_20250825"`

### Beta Tool Uses Keep

- `BetaToolUsesKeep`

  - `type: "tool_uses"`

    - `"tool_uses"`

  - `value: number`

### Beta Tool Uses Trigger

- `BetaToolUsesTrigger`

  - `type: "tool_uses"`

    - `"tool_uses"`

  - `value: number`

### Beta URL Image Source

- `BetaURLImageSource`

  - `type: "url"`

    - `"url"`

  - `url: string`

### Beta URL PDF Source

- `BetaURLPDFSource`

  - `type: "url"`

    - `"url"`

  - `url: string`

### Beta Usage

- `BetaUsage`

  - `cache_creation: BetaCacheCreation | null`

    Breakdown of cached tokens by TTL

    - `ephemeral_1h_input_tokens: number`

      The number of input tokens used to create the 1 hour cache entry.

    - `ephemeral_5m_input_tokens: number`

      The number of input tokens used to create the 5 minute cache entry.

  - `cache_creation_input_tokens: number | null`

    The number of input tokens used to create the cache entry.

  - `cache_read_input_tokens: number | null`

    The number of input tokens read from the cache.

  - `input_tokens: number`

    The number of input tokens which were used.

  - `output_tokens: number`

    The number of output tokens which were used.

  - `server_tool_use: BetaServerToolUsage | null`

    The number of server tool requests.

    - `web_fetch_requests: number`

      The number of web fetch tool requests.

    - `web_search_requests: number`

      The number of web search tool requests.

  - `service_tier: "standard" | "priority" | "batch" | null`

    If the request used the priority, standard, or batch tier.

    - `"standard"`

    - `"priority"`

    - `"batch"`

### Beta Web Fetch Block

- `BetaWebFetchBlock`

  - `content: BetaDocumentBlock`

    - `citations: BetaCitationConfig | null`

      Citation configuration for the document

      - `enabled: boolean`

    - `source: BetaBase64PDFSource | BetaPlainTextSource`

      - `BetaBase64PDFSource`

        - `data: string`

        - `media_type: "application/pdf"`

          - `"application/pdf"`

        - `type: "base64"`

          - `"base64"`

      - `BetaPlainTextSource`

        - `data: string`

        - `media_type: "text/plain"`

          - `"text/plain"`

        - `type: "text"`

          - `"text"`

    - `title: string | null`

      The title of the document

    - `type: "document"`

      - `"document"`

  - `retrieved_at: string | null`

    ISO 8601 timestamp when the content was retrieved

  - `type: "web_fetch_result"`

    - `"web_fetch_result"`

  - `url: string`

    Fetched content URL

### Beta Web Fetch Block Param

- `BetaWebFetchBlockParam`

  - `content: BetaRequestDocumentBlock`

    - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

      - `BetaBase64PDFSource`

        - `data: string`

        - `media_type: "application/pdf"`

          - `"application/pdf"`

        - `type: "base64"`

          - `"base64"`

      - `BetaPlainTextSource`

        - `data: string`

        - `media_type: "text/plain"`

          - `"text/plain"`

        - `type: "text"`

          - `"text"`

      - `BetaContentBlockSource`

        - `content: string | Array<BetaContentBlockSourceContent>`

          - `string`

          - `Array<BetaContentBlockSourceContent>`

            - `BetaTextBlockParam`

              - `text: string`

              - `type: "text"`

                - `"text"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `citations?: Array<BetaTextCitationParam> | null`

                - `BetaCitationCharLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_char_index: number`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `BetaCitationPageLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_page_number: number`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `BetaCitationContentBlockLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_block_index: number`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `BetaCitationWebSearchResultLocationParam`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string | null`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `BetaCitationSearchResultLocationParam`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string | null`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

            - `BetaImageBlockParam`

              - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                - `BetaBase64ImageSource`

                  - `data: string`

                  - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                    - `"image/jpeg"`

                    - `"image/png"`

                    - `"image/gif"`

                    - `"image/webp"`

                  - `type: "base64"`

                    - `"base64"`

                - `BetaURLImageSource`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

                - `BetaFileImageSource`

                  - `file_id: string`

                  - `type: "file"`

                    - `"file"`

              - `type: "image"`

                - `"image"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `BetaURLPDFSource`

        - `type: "url"`

          - `"url"`

        - `url: string`

      - `BetaFileDocumentSource`

        - `file_id: string`

        - `type: "file"`

          - `"file"`

    - `type: "document"`

      - `"document"`

    - `cache_control?: BetaCacheControlEphemeral | null`

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

    - `citations?: BetaCitationsConfigParam | null`

      - `enabled?: boolean`

    - `context?: string | null`

    - `title?: string | null`

  - `type: "web_fetch_result"`

    - `"web_fetch_result"`

  - `url: string`

    Fetched content URL

  - `retrieved_at?: string | null`

    ISO 8601 timestamp when the content was retrieved

### Beta Web Fetch Tool 20250910

- `BetaWebFetchTool20250910`

  - `name: "web_fetch"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"web_fetch"`

  - `type: "web_fetch_20250910"`

    - `"web_fetch_20250910"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `allowed_domains?: Array<string> | null`

    List of domains to allow fetching from

  - `blocked_domains?: Array<string> | null`

    List of domains to block fetching from

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `citations?: BetaCitationsConfigParam | null`

    Citations configuration for fetched documents. Citations are disabled by default.

    - `enabled?: boolean`

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `max_content_tokens?: number | null`

    Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

  - `max_uses?: number | null`

    Maximum number of times the tool can be used in the API request.

  - `strict?: boolean`

### Beta Web Fetch Tool Result Block

- `BetaWebFetchToolResultBlock`

  - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

    - `BetaWebFetchToolResultErrorBlock`

      - `error_code: BetaWebFetchToolResultErrorCode`

        - `"invalid_tool_input"`

        - `"url_too_long"`

        - `"url_not_allowed"`

        - `"url_not_accessible"`

        - `"unsupported_content_type"`

        - `"too_many_requests"`

        - `"max_uses_exceeded"`

        - `"unavailable"`

      - `type: "web_fetch_tool_result_error"`

        - `"web_fetch_tool_result_error"`

    - `BetaWebFetchBlock`

      - `content: BetaDocumentBlock`

        - `citations: BetaCitationConfig | null`

          Citation configuration for the document

          - `enabled: boolean`

        - `source: BetaBase64PDFSource | BetaPlainTextSource`

          - `BetaBase64PDFSource`

            - `data: string`

            - `media_type: "application/pdf"`

              - `"application/pdf"`

            - `type: "base64"`

              - `"base64"`

          - `BetaPlainTextSource`

            - `data: string`

            - `media_type: "text/plain"`

              - `"text/plain"`

            - `type: "text"`

              - `"text"`

        - `title: string | null`

          The title of the document

        - `type: "document"`

          - `"document"`

      - `retrieved_at: string | null`

        ISO 8601 timestamp when the content was retrieved

      - `type: "web_fetch_result"`

        - `"web_fetch_result"`

      - `url: string`

        Fetched content URL

  - `tool_use_id: string`

  - `type: "web_fetch_tool_result"`

    - `"web_fetch_tool_result"`

### Beta Web Fetch Tool Result Block Param

- `BetaWebFetchToolResultBlockParam`

  - `content: BetaWebFetchToolResultErrorBlockParam | BetaWebFetchBlockParam`

    - `BetaWebFetchToolResultErrorBlockParam`

      - `error_code: BetaWebFetchToolResultErrorCode`

        - `"invalid_tool_input"`

        - `"url_too_long"`

        - `"url_not_allowed"`

        - `"url_not_accessible"`

        - `"unsupported_content_type"`

        - `"too_many_requests"`

        - `"max_uses_exceeded"`

        - `"unavailable"`

      - `type: "web_fetch_tool_result_error"`

        - `"web_fetch_tool_result_error"`

    - `BetaWebFetchBlockParam`

      - `content: BetaRequestDocumentBlock`

        - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

          - `BetaBase64PDFSource`

            - `data: string`

            - `media_type: "application/pdf"`

              - `"application/pdf"`

            - `type: "base64"`

              - `"base64"`

          - `BetaPlainTextSource`

            - `data: string`

            - `media_type: "text/plain"`

              - `"text/plain"`

            - `type: "text"`

              - `"text"`

          - `BetaContentBlockSource`

            - `content: string | Array<BetaContentBlockSourceContent>`

              - `string`

              - `Array<BetaContentBlockSourceContent>`

                - `BetaTextBlockParam`

                  - `text: string`

                  - `type: "text"`

                    - `"text"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

                  - `citations?: Array<BetaTextCitationParam> | null`

                    - `BetaCitationCharLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_char_index: number`

                      - `start_char_index: number`

                      - `type: "char_location"`

                        - `"char_location"`

                    - `BetaCitationPageLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_page_number: number`

                      - `start_page_number: number`

                      - `type: "page_location"`

                        - `"page_location"`

                    - `BetaCitationContentBlockLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_block_index: number`

                      - `start_block_index: number`

                      - `type: "content_block_location"`

                        - `"content_block_location"`

                    - `BetaCitationWebSearchResultLocationParam`

                      - `cited_text: string`

                      - `encrypted_index: string`

                      - `title: string | null`

                      - `type: "web_search_result_location"`

                        - `"web_search_result_location"`

                      - `url: string`

                    - `BetaCitationSearchResultLocationParam`

                      - `cited_text: string`

                      - `end_block_index: number`

                      - `search_result_index: number`

                      - `source: string`

                      - `start_block_index: number`

                      - `title: string | null`

                      - `type: "search_result_location"`

                        - `"search_result_location"`

                - `BetaImageBlockParam`

                  - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                    - `BetaBase64ImageSource`

                      - `data: string`

                      - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                        - `"image/jpeg"`

                        - `"image/png"`

                        - `"image/gif"`

                        - `"image/webp"`

                      - `type: "base64"`

                        - `"base64"`

                    - `BetaURLImageSource`

                      - `type: "url"`

                        - `"url"`

                      - `url: string`

                    - `BetaFileImageSource`

                      - `file_id: string`

                      - `type: "file"`

                        - `"file"`

                  - `type: "image"`

                    - `"image"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `BetaURLPDFSource`

            - `type: "url"`

              - `"url"`

            - `url: string`

          - `BetaFileDocumentSource`

            - `file_id: string`

            - `type: "file"`

              - `"file"`

        - `type: "document"`

          - `"document"`

        - `cache_control?: BetaCacheControlEphemeral | null`

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

        - `citations?: BetaCitationsConfigParam | null`

          - `enabled?: boolean`

        - `context?: string | null`

        - `title?: string | null`

      - `type: "web_fetch_result"`

        - `"web_fetch_result"`

      - `url: string`

        Fetched content URL

      - `retrieved_at?: string | null`

        ISO 8601 timestamp when the content was retrieved

  - `tool_use_id: string`

  - `type: "web_fetch_tool_result"`

    - `"web_fetch_tool_result"`

  - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta Web Fetch Tool Result Error Block

- `BetaWebFetchToolResultErrorBlock`

  - `error_code: BetaWebFetchToolResultErrorCode`

    - `"invalid_tool_input"`

    - `"url_too_long"`

    - `"url_not_allowed"`

    - `"url_not_accessible"`

    - `"unsupported_content_type"`

    - `"too_many_requests"`

    - `"max_uses_exceeded"`

    - `"unavailable"`

  - `type: "web_fetch_tool_result_error"`

    - `"web_fetch_tool_result_error"`

### Beta Web Fetch Tool Result Error Block Param

- `BetaWebFetchToolResultErrorBlockParam`

  - `error_code: BetaWebFetchToolResultErrorCode`

    - `"invalid_tool_input"`

    - `"url_too_long"`

    - `"url_not_allowed"`

    - `"url_not_accessible"`

    - `"unsupported_content_type"`

    - `"too_many_requests"`

    - `"max_uses_exceeded"`

    - `"unavailable"`

  - `type: "web_fetch_tool_result_error"`

    - `"web_fetch_tool_result_error"`

### Beta Web Fetch Tool Result Error Code

- `BetaWebFetchToolResultErrorCode = "invalid_tool_input" | "url_too_long" | "url_not_allowed" | 5 more`

  - `"invalid_tool_input"`

  - `"url_too_long"`

  - `"url_not_allowed"`

  - `"url_not_accessible"`

  - `"unsupported_content_type"`

  - `"too_many_requests"`

  - `"max_uses_exceeded"`

  - `"unavailable"`

### Beta Web Search Result Block

- `BetaWebSearchResultBlock`

  - `encrypted_content: string`

  - `page_age: string | null`

  - `title: string`

  - `type: "web_search_result"`

    - `"web_search_result"`

  - `url: string`

### Beta Web Search Result Block Param

- `BetaWebSearchResultBlockParam`

  - `encrypted_content: string`

  - `title: string`

  - `type: "web_search_result"`

    - `"web_search_result"`

  - `url: string`

  - `page_age?: string | null`

### Beta Web Search Tool 20250305

- `BetaWebSearchTool20250305`

  - `name: "web_search"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"web_search"`

  - `type: "web_search_20250305"`

    - `"web_search_20250305"`

  - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

    - `"direct"`

    - `"code_execution_20250825"`

  - `allowed_domains?: Array<string> | null`

    If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

  - `blocked_domains?: Array<string> | null`

    If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

  - `cache_control?: BetaCacheControlEphemeral | null`

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

  - `defer_loading?: boolean`

    If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

  - `max_uses?: number | null`

    Maximum number of times the tool can be used in the API request.

  - `strict?: boolean`

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

### Beta Web Search Tool Request Error

- `BetaWebSearchToolRequestError`

  - `error_code: BetaWebSearchToolResultErrorCode`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"max_uses_exceeded"`

    - `"too_many_requests"`

    - `"query_too_long"`

  - `type: "web_search_tool_result_error"`

    - `"web_search_tool_result_error"`

### Beta Web Search Tool Result Block

- `BetaWebSearchToolResultBlock`

  - `content: BetaWebSearchToolResultBlockContent`

    - `BetaWebSearchToolResultError`

      - `error_code: BetaWebSearchToolResultErrorCode`

        - `"invalid_tool_input"`

        - `"unavailable"`

        - `"max_uses_exceeded"`

        - `"too_many_requests"`

        - `"query_too_long"`

      - `type: "web_search_tool_result_error"`

        - `"web_search_tool_result_error"`

    - `Array<BetaWebSearchResultBlock>`

      - `encrypted_content: string`

      - `page_age: string | null`

      - `title: string`

      - `type: "web_search_result"`

        - `"web_search_result"`

      - `url: string`

  - `tool_use_id: string`

  - `type: "web_search_tool_result"`

    - `"web_search_tool_result"`

### Beta Web Search Tool Result Block Content

- `BetaWebSearchToolResultBlockContent = BetaWebSearchToolResultError | Array<BetaWebSearchResultBlock>`

  - `BetaWebSearchToolResultError`

    - `error_code: BetaWebSearchToolResultErrorCode`

      - `"invalid_tool_input"`

      - `"unavailable"`

      - `"max_uses_exceeded"`

      - `"too_many_requests"`

      - `"query_too_long"`

    - `type: "web_search_tool_result_error"`

      - `"web_search_tool_result_error"`

  - `Array<BetaWebSearchResultBlock>`

    - `encrypted_content: string`

    - `page_age: string | null`

    - `title: string`

    - `type: "web_search_result"`

      - `"web_search_result"`

    - `url: string`

### Beta Web Search Tool Result Block Param

- `BetaWebSearchToolResultBlockParam`

  - `content: BetaWebSearchToolResultBlockParamContent`

    - `Array<BetaWebSearchResultBlockParam>`

      - `encrypted_content: string`

      - `title: string`

      - `type: "web_search_result"`

        - `"web_search_result"`

      - `url: string`

      - `page_age?: string | null`

    - `BetaWebSearchToolRequestError`

      - `error_code: BetaWebSearchToolResultErrorCode`

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

  - `cache_control?: BetaCacheControlEphemeral | null`

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

### Beta Web Search Tool Result Block Param Content

- `BetaWebSearchToolResultBlockParamContent = Array<BetaWebSearchResultBlockParam> | BetaWebSearchToolRequestError`

  - `Array<BetaWebSearchResultBlockParam>`

    - `encrypted_content: string`

    - `title: string`

    - `type: "web_search_result"`

      - `"web_search_result"`

    - `url: string`

    - `page_age?: string | null`

  - `BetaWebSearchToolRequestError`

    - `error_code: BetaWebSearchToolResultErrorCode`

      - `"invalid_tool_input"`

      - `"unavailable"`

      - `"max_uses_exceeded"`

      - `"too_many_requests"`

      - `"query_too_long"`

    - `type: "web_search_tool_result_error"`

      - `"web_search_tool_result_error"`

### Beta Web Search Tool Result Error

- `BetaWebSearchToolResultError`

  - `error_code: BetaWebSearchToolResultErrorCode`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"max_uses_exceeded"`

    - `"too_many_requests"`

    - `"query_too_long"`

  - `type: "web_search_tool_result_error"`

    - `"web_search_tool_result_error"`

### Beta Web Search Tool Result Error Code

- `BetaWebSearchToolResultErrorCode = "invalid_tool_input" | "unavailable" | "max_uses_exceeded" | 2 more`

  - `"invalid_tool_input"`

  - `"unavailable"`

  - `"max_uses_exceeded"`

  - `"too_many_requests"`

  - `"query_too_long"`

# Batches

## Create

`client.beta.messages.batches.create(BatchCreateParamsparams, RequestOptionsoptions?): BetaMessageBatch`

**post** `/v1/messages/batches`

Send a batch of Message creation requests.

The Message Batches API can be used to process multiple Messages API requests at once. Once a Message Batch is created, it begins processing immediately. Batches can take up to 24 hours to complete.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchCreateParams`

  - `requests: Array<Request>`

    Body param: List of requests for prompt completion. Each is an individual request to create a Message.

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

      - `messages: Array<BetaMessageParam>`

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

        - `content: string | Array<BetaContentBlockParam>`

          - `string`

          - `Array<BetaContentBlockParam>`

            - `BetaTextBlockParam`

              - `text: string`

              - `type: "text"`

                - `"text"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `citations?: Array<BetaTextCitationParam> | null`

                - `BetaCitationCharLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_char_index: number`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `BetaCitationPageLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_page_number: number`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `BetaCitationContentBlockLocationParam`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_block_index: number`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `BetaCitationWebSearchResultLocationParam`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string | null`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `BetaCitationSearchResultLocationParam`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string | null`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

            - `BetaImageBlockParam`

              - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                - `BetaBase64ImageSource`

                  - `data: string`

                  - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                    - `"image/jpeg"`

                    - `"image/png"`

                    - `"image/gif"`

                    - `"image/webp"`

                  - `type: "base64"`

                    - `"base64"`

                - `BetaURLImageSource`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

                - `BetaFileImageSource`

                  - `file_id: string`

                  - `type: "file"`

                    - `"file"`

              - `type: "image"`

                - `"image"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `BetaRequestDocumentBlock`

              - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

                - `BetaBase64PDFSource`

                  - `data: string`

                  - `media_type: "application/pdf"`

                    - `"application/pdf"`

                  - `type: "base64"`

                    - `"base64"`

                - `BetaPlainTextSource`

                  - `data: string`

                  - `media_type: "text/plain"`

                    - `"text/plain"`

                  - `type: "text"`

                    - `"text"`

                - `BetaContentBlockSource`

                  - `content: string | Array<BetaContentBlockSourceContent>`

                    - `string`

                    - `Array<BetaContentBlockSourceContent>`

                      - `BetaTextBlockParam`

                        - `text: string`

                        - `type: "text"`

                          - `"text"`

                        - `cache_control?: BetaCacheControlEphemeral | null`

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

                        - `citations?: Array<BetaTextCitationParam> | null`

                          - `BetaCitationCharLocationParam`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string | null`

                            - `end_char_index: number`

                            - `start_char_index: number`

                            - `type: "char_location"`

                              - `"char_location"`

                          - `BetaCitationPageLocationParam`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string | null`

                            - `end_page_number: number`

                            - `start_page_number: number`

                            - `type: "page_location"`

                              - `"page_location"`

                          - `BetaCitationContentBlockLocationParam`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string | null`

                            - `end_block_index: number`

                            - `start_block_index: number`

                            - `type: "content_block_location"`

                              - `"content_block_location"`

                          - `BetaCitationWebSearchResultLocationParam`

                            - `cited_text: string`

                            - `encrypted_index: string`

                            - `title: string | null`

                            - `type: "web_search_result_location"`

                              - `"web_search_result_location"`

                            - `url: string`

                          - `BetaCitationSearchResultLocationParam`

                            - `cited_text: string`

                            - `end_block_index: number`

                            - `search_result_index: number`

                            - `source: string`

                            - `start_block_index: number`

                            - `title: string | null`

                            - `type: "search_result_location"`

                              - `"search_result_location"`

                      - `BetaImageBlockParam`

                        - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                          - `BetaBase64ImageSource`

                            - `data: string`

                            - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                              - `"image/jpeg"`

                              - `"image/png"`

                              - `"image/gif"`

                              - `"image/webp"`

                            - `type: "base64"`

                              - `"base64"`

                          - `BetaURLImageSource`

                            - `type: "url"`

                              - `"url"`

                            - `url: string`

                          - `BetaFileImageSource`

                            - `file_id: string`

                            - `type: "file"`

                              - `"file"`

                        - `type: "image"`

                          - `"image"`

                        - `cache_control?: BetaCacheControlEphemeral | null`

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

                - `BetaURLPDFSource`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

                - `BetaFileDocumentSource`

                  - `file_id: string`

                  - `type: "file"`

                    - `"file"`

              - `type: "document"`

                - `"document"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `citations?: BetaCitationsConfigParam | null`

                - `enabled?: boolean`

              - `context?: string | null`

              - `title?: string | null`

            - `BetaSearchResultBlockParam`

              - `content: Array<BetaTextBlockParam>`

                - `text: string`

                - `type: "text"`

                  - `"text"`

                - `cache_control?: BetaCacheControlEphemeral | null`

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

                - `citations?: Array<BetaTextCitationParam> | null`

                  - `BetaCitationCharLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_char_index: number`

                    - `start_char_index: number`

                    - `type: "char_location"`

                      - `"char_location"`

                  - `BetaCitationPageLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_page_number: number`

                    - `start_page_number: number`

                    - `type: "page_location"`

                      - `"page_location"`

                  - `BetaCitationContentBlockLocationParam`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_block_index: number`

                    - `start_block_index: number`

                    - `type: "content_block_location"`

                      - `"content_block_location"`

                  - `BetaCitationWebSearchResultLocationParam`

                    - `cited_text: string`

                    - `encrypted_index: string`

                    - `title: string | null`

                    - `type: "web_search_result_location"`

                      - `"web_search_result_location"`

                    - `url: string`

                  - `BetaCitationSearchResultLocationParam`

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

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `citations?: BetaCitationsConfigParam`

                - `enabled?: boolean`

            - `BetaThinkingBlockParam`

              - `signature: string`

              - `thinking: string`

              - `type: "thinking"`

                - `"thinking"`

            - `BetaRedactedThinkingBlockParam`

              - `data: string`

              - `type: "redacted_thinking"`

                - `"redacted_thinking"`

            - `BetaToolUseBlockParam`

              - `id: string`

              - `input: Record<string, unknown>`

              - `name: string`

              - `type: "tool_use"`

                - `"tool_use"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `caller?: BetaDirectCaller | BetaServerToolCaller`

                Tool invocation directly from the model.

                - `BetaDirectCaller`

                  Tool invocation directly from the model.

                  - `type: "direct"`

                    - `"direct"`

                - `BetaServerToolCaller`

                  Tool invocation generated by a server-side tool.

                  - `tool_id: string`

                  - `type: "code_execution_20250825"`

                    - `"code_execution_20250825"`

            - `BetaToolResultBlockParam`

              - `tool_use_id: string`

              - `type: "tool_result"`

                - `"tool_result"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `content?: string | Array<BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more>`

                - `string`

                - `Array<BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more>`

                  - `BetaTextBlockParam`

                    - `text: string`

                    - `type: "text"`

                      - `"text"`

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

                    - `citations?: Array<BetaTextCitationParam> | null`

                      - `BetaCitationCharLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_char_index: number`

                        - `start_char_index: number`

                        - `type: "char_location"`

                          - `"char_location"`

                      - `BetaCitationPageLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_page_number: number`

                        - `start_page_number: number`

                        - `type: "page_location"`

                          - `"page_location"`

                      - `BetaCitationContentBlockLocationParam`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string | null`

                        - `end_block_index: number`

                        - `start_block_index: number`

                        - `type: "content_block_location"`

                          - `"content_block_location"`

                      - `BetaCitationWebSearchResultLocationParam`

                        - `cited_text: string`

                        - `encrypted_index: string`

                        - `title: string | null`

                        - `type: "web_search_result_location"`

                          - `"web_search_result_location"`

                        - `url: string`

                      - `BetaCitationSearchResultLocationParam`

                        - `cited_text: string`

                        - `end_block_index: number`

                        - `search_result_index: number`

                        - `source: string`

                        - `start_block_index: number`

                        - `title: string | null`

                        - `type: "search_result_location"`

                          - `"search_result_location"`

                  - `BetaImageBlockParam`

                    - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                      - `BetaBase64ImageSource`

                        - `data: string`

                        - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                          - `"image/jpeg"`

                          - `"image/png"`

                          - `"image/gif"`

                          - `"image/webp"`

                        - `type: "base64"`

                          - `"base64"`

                      - `BetaURLImageSource`

                        - `type: "url"`

                          - `"url"`

                        - `url: string`

                      - `BetaFileImageSource`

                        - `file_id: string`

                        - `type: "file"`

                          - `"file"`

                    - `type: "image"`

                      - `"image"`

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

                  - `BetaSearchResultBlockParam`

                    - `content: Array<BetaTextBlockParam>`

                      - `text: string`

                      - `type: "text"`

                        - `"text"`

                      - `cache_control?: BetaCacheControlEphemeral | null`

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

                      - `citations?: Array<BetaTextCitationParam> | null`

                        - `BetaCitationCharLocationParam`

                          - `cited_text: string`

                          - `document_index: number`

                          - `document_title: string | null`

                          - `end_char_index: number`

                          - `start_char_index: number`

                          - `type: "char_location"`

                            - `"char_location"`

                        - `BetaCitationPageLocationParam`

                          - `cited_text: string`

                          - `document_index: number`

                          - `document_title: string | null`

                          - `end_page_number: number`

                          - `start_page_number: number`

                          - `type: "page_location"`

                            - `"page_location"`

                        - `BetaCitationContentBlockLocationParam`

                          - `cited_text: string`

                          - `document_index: number`

                          - `document_title: string | null`

                          - `end_block_index: number`

                          - `start_block_index: number`

                          - `type: "content_block_location"`

                            - `"content_block_location"`

                        - `BetaCitationWebSearchResultLocationParam`

                          - `cited_text: string`

                          - `encrypted_index: string`

                          - `title: string | null`

                          - `type: "web_search_result_location"`

                            - `"web_search_result_location"`

                          - `url: string`

                        - `BetaCitationSearchResultLocationParam`

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

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

                    - `citations?: BetaCitationsConfigParam`

                      - `enabled?: boolean`

                  - `BetaRequestDocumentBlock`

                    - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

                      - `BetaBase64PDFSource`

                        - `data: string`

                        - `media_type: "application/pdf"`

                          - `"application/pdf"`

                        - `type: "base64"`

                          - `"base64"`

                      - `BetaPlainTextSource`

                        - `data: string`

                        - `media_type: "text/plain"`

                          - `"text/plain"`

                        - `type: "text"`

                          - `"text"`

                      - `BetaContentBlockSource`

                        - `content: string | Array<BetaContentBlockSourceContent>`

                          - `string`

                          - `Array<BetaContentBlockSourceContent>`

                            - `BetaTextBlockParam`

                              - `text: string`

                              - `type: "text"`

                                - `"text"`

                              - `cache_control?: BetaCacheControlEphemeral | null`

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

                              - `citations?: Array<BetaTextCitationParam> | null`

                                - `BetaCitationCharLocationParam`

                                  - `cited_text: string`

                                  - `document_index: number`

                                  - `document_title: string | null`

                                  - `end_char_index: number`

                                  - `start_char_index: number`

                                  - `type: "char_location"`

                                    - `"char_location"`

                                - `BetaCitationPageLocationParam`

                                  - `cited_text: string`

                                  - `document_index: number`

                                  - `document_title: string | null`

                                  - `end_page_number: number`

                                  - `start_page_number: number`

                                  - `type: "page_location"`

                                    - `"page_location"`

                                - `BetaCitationContentBlockLocationParam`

                                  - `cited_text: string`

                                  - `document_index: number`

                                  - `document_title: string | null`

                                  - `end_block_index: number`

                                  - `start_block_index: number`

                                  - `type: "content_block_location"`

                                    - `"content_block_location"`

                                - `BetaCitationWebSearchResultLocationParam`

                                  - `cited_text: string`

                                  - `encrypted_index: string`

                                  - `title: string | null`

                                  - `type: "web_search_result_location"`

                                    - `"web_search_result_location"`

                                  - `url: string`

                                - `BetaCitationSearchResultLocationParam`

                                  - `cited_text: string`

                                  - `end_block_index: number`

                                  - `search_result_index: number`

                                  - `source: string`

                                  - `start_block_index: number`

                                  - `title: string | null`

                                  - `type: "search_result_location"`

                                    - `"search_result_location"`

                            - `BetaImageBlockParam`

                              - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                                - `BetaBase64ImageSource`

                                  - `data: string`

                                  - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                                    - `"image/jpeg"`

                                    - `"image/png"`

                                    - `"image/gif"`

                                    - `"image/webp"`

                                  - `type: "base64"`

                                    - `"base64"`

                                - `BetaURLImageSource`

                                  - `type: "url"`

                                    - `"url"`

                                  - `url: string`

                                - `BetaFileImageSource`

                                  - `file_id: string`

                                  - `type: "file"`

                                    - `"file"`

                              - `type: "image"`

                                - `"image"`

                              - `cache_control?: BetaCacheControlEphemeral | null`

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

                      - `BetaURLPDFSource`

                        - `type: "url"`

                          - `"url"`

                        - `url: string`

                      - `BetaFileDocumentSource`

                        - `file_id: string`

                        - `type: "file"`

                          - `"file"`

                    - `type: "document"`

                      - `"document"`

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

                    - `citations?: BetaCitationsConfigParam | null`

                      - `enabled?: boolean`

                    - `context?: string | null`

                    - `title?: string | null`

                  - `BetaToolReferenceBlockParam`

                    Tool reference block that can be included in tool_result content.

                    - `tool_name: string`

                    - `type: "tool_reference"`

                      - `"tool_reference"`

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `is_error?: boolean`

            - `BetaServerToolUseBlockParam`

              - `id: string`

              - `input: Record<string, unknown>`

              - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

                - `"web_search"`

                - `"web_fetch"`

                - `"code_execution"`

                - `"bash_code_execution"`

                - `"text_editor_code_execution"`

                - `"tool_search_tool_regex"`

                - `"tool_search_tool_bm25"`

              - `type: "server_tool_use"`

                - `"server_tool_use"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `caller?: BetaDirectCaller | BetaServerToolCaller`

                Tool invocation directly from the model.

                - `BetaDirectCaller`

                  Tool invocation directly from the model.

                  - `type: "direct"`

                    - `"direct"`

                - `BetaServerToolCaller`

                  Tool invocation generated by a server-side tool.

                  - `tool_id: string`

                  - `type: "code_execution_20250825"`

                    - `"code_execution_20250825"`

            - `BetaWebSearchToolResultBlockParam`

              - `content: BetaWebSearchToolResultBlockParamContent`

                - `Array<BetaWebSearchResultBlockParam>`

                  - `encrypted_content: string`

                  - `title: string`

                  - `type: "web_search_result"`

                    - `"web_search_result"`

                  - `url: string`

                  - `page_age?: string | null`

                - `BetaWebSearchToolRequestError`

                  - `error_code: BetaWebSearchToolResultErrorCode`

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

              - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `BetaWebFetchToolResultBlockParam`

              - `content: BetaWebFetchToolResultErrorBlockParam | BetaWebFetchBlockParam`

                - `BetaWebFetchToolResultErrorBlockParam`

                  - `error_code: BetaWebFetchToolResultErrorCode`

                    - `"invalid_tool_input"`

                    - `"url_too_long"`

                    - `"url_not_allowed"`

                    - `"url_not_accessible"`

                    - `"unsupported_content_type"`

                    - `"too_many_requests"`

                    - `"max_uses_exceeded"`

                    - `"unavailable"`

                  - `type: "web_fetch_tool_result_error"`

                    - `"web_fetch_tool_result_error"`

                - `BetaWebFetchBlockParam`

                  - `content: BetaRequestDocumentBlock`

                    - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

                      - `BetaBase64PDFSource`

                        - `data: string`

                        - `media_type: "application/pdf"`

                          - `"application/pdf"`

                        - `type: "base64"`

                          - `"base64"`

                      - `BetaPlainTextSource`

                        - `data: string`

                        - `media_type: "text/plain"`

                          - `"text/plain"`

                        - `type: "text"`

                          - `"text"`

                      - `BetaContentBlockSource`

                        - `content: string | Array<BetaContentBlockSourceContent>`

                          - `string`

                          - `Array<BetaContentBlockSourceContent>`

                            - `BetaTextBlockParam`

                              - `text: string`

                              - `type: "text"`

                                - `"text"`

                              - `cache_control?: BetaCacheControlEphemeral | null`

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

                              - `citations?: Array<BetaTextCitationParam> | null`

                                - `BetaCitationCharLocationParam`

                                  - `cited_text: string`

                                  - `document_index: number`

                                  - `document_title: string | null`

                                  - `end_char_index: number`

                                  - `start_char_index: number`

                                  - `type: "char_location"`

                                    - `"char_location"`

                                - `BetaCitationPageLocationParam`

                                  - `cited_text: string`

                                  - `document_index: number`

                                  - `document_title: string | null`

                                  - `end_page_number: number`

                                  - `start_page_number: number`

                                  - `type: "page_location"`

                                    - `"page_location"`

                                - `BetaCitationContentBlockLocationParam`

                                  - `cited_text: string`

                                  - `document_index: number`

                                  - `document_title: string | null`

                                  - `end_block_index: number`

                                  - `start_block_index: number`

                                  - `type: "content_block_location"`

                                    - `"content_block_location"`

                                - `BetaCitationWebSearchResultLocationParam`

                                  - `cited_text: string`

                                  - `encrypted_index: string`

                                  - `title: string | null`

                                  - `type: "web_search_result_location"`

                                    - `"web_search_result_location"`

                                  - `url: string`

                                - `BetaCitationSearchResultLocationParam`

                                  - `cited_text: string`

                                  - `end_block_index: number`

                                  - `search_result_index: number`

                                  - `source: string`

                                  - `start_block_index: number`

                                  - `title: string | null`

                                  - `type: "search_result_location"`

                                    - `"search_result_location"`

                            - `BetaImageBlockParam`

                              - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                                - `BetaBase64ImageSource`

                                  - `data: string`

                                  - `media_type: "image/jpeg" | "image/png" | "image/gif" | "image/webp"`

                                    - `"image/jpeg"`

                                    - `"image/png"`

                                    - `"image/gif"`

                                    - `"image/webp"`

                                  - `type: "base64"`

                                    - `"base64"`

                                - `BetaURLImageSource`

                                  - `type: "url"`

                                    - `"url"`

                                  - `url: string`

                                - `BetaFileImageSource`

                                  - `file_id: string`

                                  - `type: "file"`

                                    - `"file"`

                              - `type: "image"`

                                - `"image"`

                              - `cache_control?: BetaCacheControlEphemeral | null`

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

                      - `BetaURLPDFSource`

                        - `type: "url"`

                          - `"url"`

                        - `url: string`

                      - `BetaFileDocumentSource`

                        - `file_id: string`

                        - `type: "file"`

                          - `"file"`

                    - `type: "document"`

                      - `"document"`

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

                    - `citations?: BetaCitationsConfigParam | null`

                      - `enabled?: boolean`

                    - `context?: string | null`

                    - `title?: string | null`

                  - `type: "web_fetch_result"`

                    - `"web_fetch_result"`

                  - `url: string`

                    Fetched content URL

                  - `retrieved_at?: string | null`

                    ISO 8601 timestamp when the content was retrieved

              - `tool_use_id: string`

              - `type: "web_fetch_tool_result"`

                - `"web_fetch_tool_result"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `BetaCodeExecutionToolResultBlockParam`

              - `content: BetaCodeExecutionToolResultBlockParamContent`

                - `BetaCodeExecutionToolResultErrorParam`

                  - `error_code: BetaCodeExecutionToolResultErrorCode`

                    - `"invalid_tool_input"`

                    - `"unavailable"`

                    - `"too_many_requests"`

                    - `"execution_time_exceeded"`

                  - `type: "code_execution_tool_result_error"`

                    - `"code_execution_tool_result_error"`

                - `BetaCodeExecutionResultBlockParam`

                  - `content: Array<BetaCodeExecutionOutputBlockParam>`

                    - `file_id: string`

                    - `type: "code_execution_output"`

                      - `"code_execution_output"`

                  - `return_code: number`

                  - `stderr: string`

                  - `stdout: string`

                  - `type: "code_execution_result"`

                    - `"code_execution_result"`

              - `tool_use_id: string`

              - `type: "code_execution_tool_result"`

                - `"code_execution_tool_result"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `BetaBashCodeExecutionToolResultBlockParam`

              - `content: BetaBashCodeExecutionToolResultErrorParam | BetaBashCodeExecutionResultBlockParam`

                - `BetaBashCodeExecutionToolResultErrorParam`

                  - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                    - `"invalid_tool_input"`

                    - `"unavailable"`

                    - `"too_many_requests"`

                    - `"execution_time_exceeded"`

                    - `"output_file_too_large"`

                  - `type: "bash_code_execution_tool_result_error"`

                    - `"bash_code_execution_tool_result_error"`

                - `BetaBashCodeExecutionResultBlockParam`

                  - `content: Array<BetaBashCodeExecutionOutputBlockParam>`

                    - `file_id: string`

                    - `type: "bash_code_execution_output"`

                      - `"bash_code_execution_output"`

                  - `return_code: number`

                  - `stderr: string`

                  - `stdout: string`

                  - `type: "bash_code_execution_result"`

                    - `"bash_code_execution_result"`

              - `tool_use_id: string`

              - `type: "bash_code_execution_tool_result"`

                - `"bash_code_execution_tool_result"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `BetaTextEditorCodeExecutionToolResultBlockParam`

              - `content: BetaTextEditorCodeExecutionToolResultErrorParam | BetaTextEditorCodeExecutionViewResultBlockParam | BetaTextEditorCodeExecutionCreateResultBlockParam | BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

                - `BetaTextEditorCodeExecutionToolResultErrorParam`

                  - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                    - `"invalid_tool_input"`

                    - `"unavailable"`

                    - `"too_many_requests"`

                    - `"execution_time_exceeded"`

                    - `"file_not_found"`

                  - `type: "text_editor_code_execution_tool_result_error"`

                    - `"text_editor_code_execution_tool_result_error"`

                  - `error_message?: string | null`

                - `BetaTextEditorCodeExecutionViewResultBlockParam`

                  - `content: string`

                  - `file_type: "text" | "image" | "pdf"`

                    - `"text"`

                    - `"image"`

                    - `"pdf"`

                  - `type: "text_editor_code_execution_view_result"`

                    - `"text_editor_code_execution_view_result"`

                  - `num_lines?: number | null`

                  - `start_line?: number | null`

                  - `total_lines?: number | null`

                - `BetaTextEditorCodeExecutionCreateResultBlockParam`

                  - `is_file_update: boolean`

                  - `type: "text_editor_code_execution_create_result"`

                    - `"text_editor_code_execution_create_result"`

                - `BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

                  - `type: "text_editor_code_execution_str_replace_result"`

                    - `"text_editor_code_execution_str_replace_result"`

                  - `lines?: Array<string> | null`

                  - `new_lines?: number | null`

                  - `new_start?: number | null`

                  - `old_lines?: number | null`

                  - `old_start?: number | null`

              - `tool_use_id: string`

              - `type: "text_editor_code_execution_tool_result"`

                - `"text_editor_code_execution_tool_result"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `BetaToolSearchToolResultBlockParam`

              - `content: BetaToolSearchToolResultErrorParam | BetaToolSearchToolSearchResultBlockParam`

                - `BetaToolSearchToolResultErrorParam`

                  - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

                    - `"invalid_tool_input"`

                    - `"unavailable"`

                    - `"too_many_requests"`

                    - `"execution_time_exceeded"`

                  - `type: "tool_search_tool_result_error"`

                    - `"tool_search_tool_result_error"`

                - `BetaToolSearchToolSearchResultBlockParam`

                  - `tool_references: Array<BetaToolReferenceBlockParam>`

                    - `tool_name: string`

                    - `type: "tool_reference"`

                      - `"tool_reference"`

                    - `cache_control?: BetaCacheControlEphemeral | null`

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

                  - `type: "tool_search_tool_search_result"`

                    - `"tool_search_tool_search_result"`

              - `tool_use_id: string`

              - `type: "tool_search_tool_result"`

                - `"tool_search_tool_result"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `BetaMCPToolUseBlockParam`

              - `id: string`

              - `input: Record<string, unknown>`

              - `name: string`

              - `server_name: string`

                The name of the MCP server

              - `type: "mcp_tool_use"`

                - `"mcp_tool_use"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

            - `BetaRequestMCPToolResultBlockParam`

              - `tool_use_id: string`

              - `type: "mcp_tool_result"`

                - `"mcp_tool_result"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

              - `content?: string | Array<BetaTextBlockParam>`

                - `string`

                - `Array<BetaTextBlockParam>`

                  - `text: string`

                  - `type: "text"`

                    - `"text"`

                  - `cache_control?: BetaCacheControlEphemeral | null`

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

                  - `citations?: Array<BetaTextCitationParam> | null`

                    - `BetaCitationCharLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_char_index: number`

                      - `start_char_index: number`

                      - `type: "char_location"`

                        - `"char_location"`

                    - `BetaCitationPageLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_page_number: number`

                      - `start_page_number: number`

                      - `type: "page_location"`

                        - `"page_location"`

                    - `BetaCitationContentBlockLocationParam`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string | null`

                      - `end_block_index: number`

                      - `start_block_index: number`

                      - `type: "content_block_location"`

                        - `"content_block_location"`

                    - `BetaCitationWebSearchResultLocationParam`

                      - `cited_text: string`

                      - `encrypted_index: string`

                      - `title: string | null`

                      - `type: "web_search_result_location"`

                        - `"web_search_result_location"`

                      - `url: string`

                    - `BetaCitationSearchResultLocationParam`

                      - `cited_text: string`

                      - `end_block_index: number`

                      - `search_result_index: number`

                      - `source: string`

                      - `start_block_index: number`

                      - `title: string | null`

                      - `type: "search_result_location"`

                        - `"search_result_location"`

              - `is_error?: boolean`

            - `BetaContainerUploadBlockParam`

              A content block that represents a file to be uploaded to the container
              Files uploaded via this block will be available in the container's input directory.

              - `file_id: string`

              - `type: "container_upload"`

                - `"container_upload"`

              - `cache_control?: BetaCacheControlEphemeral | null`

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

      - `container?: BetaContainerParams | string | null`

        Container identifier for reuse across requests.

        - `BetaContainerParams`

          Container parameters with skills to be loaded.

          - `id?: string | null`

            Container id

          - `skills?: Array<BetaSkillParams> | null`

            List of skills to load in the container

            - `skill_id: string`

              Skill ID

            - `type: "anthropic" | "custom"`

              Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

              - `"anthropic"`

              - `"custom"`

            - `version?: string`

              Skill version or 'latest' for most recent version

        - `string`

      - `context_management?: BetaContextManagementConfig | null`

        Context management configuration.

        This allows you to control how Claude manages context across multiple requests, such as whether to clear function results or not.

        - `edits?: Array<BetaClearToolUses20250919Edit | BetaClearThinking20251015Edit>`

          List of context management edits to apply

          - `BetaClearToolUses20250919Edit`

            - `type: "clear_tool_uses_20250919"`

              - `"clear_tool_uses_20250919"`

            - `clear_at_least?: BetaInputTokensClearAtLeast | null`

              Minimum number of tokens that must be cleared when triggered. Context will only be modified if at least this many tokens can be removed.

              - `type: "input_tokens"`

                - `"input_tokens"`

              - `value: number`

            - `clear_tool_inputs?: boolean | Array<string> | null`

              Whether to clear all tool inputs (bool) or specific tool inputs to clear (list)

              - `boolean`

              - `Array<string>`

            - `exclude_tools?: Array<string> | null`

              Tool names whose uses are preserved from clearing

            - `keep?: BetaToolUsesKeep`

              Number of tool uses to retain in the conversation

              - `type: "tool_uses"`

                - `"tool_uses"`

              - `value: number`

            - `trigger?: BetaInputTokensTrigger | BetaToolUsesTrigger`

              Condition that triggers the context management strategy

              - `BetaInputTokensTrigger`

                - `type: "input_tokens"`

                  - `"input_tokens"`

                - `value: number`

              - `BetaToolUsesTrigger`

                - `type: "tool_uses"`

                  - `"tool_uses"`

                - `value: number`

          - `BetaClearThinking20251015Edit`

            - `type: "clear_thinking_20251015"`

              - `"clear_thinking_20251015"`

            - `keep?: BetaThinkingTurns | BetaAllThinkingTurns | "all"`

              Number of most recent assistant turns to keep thinking blocks for. Older turns will have their thinking blocks removed.

              - `BetaThinkingTurns`

                - `type: "thinking_turns"`

                  - `"thinking_turns"`

                - `value: number`

              - `BetaAllThinkingTurns`

                - `type: "all"`

                  - `"all"`

              - `"all"`

                - `"all"`

      - `mcp_servers?: Array<BetaRequestMCPServerURLDefinition>`

        MCP servers to be utilized in this request

        - `name: string`

        - `type: "url"`

          - `"url"`

        - `url: string`

        - `authorization_token?: string | null`

        - `tool_configuration?: BetaRequestMCPServerToolConfiguration | null`

          - `allowed_tools?: Array<string> | null`

          - `enabled?: boolean | null`

      - `metadata?: BetaMetadata`

        An object describing metadata about the request.

        - `user_id?: string | null`

          An external identifier for the user who is associated with the request.

          This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

      - `output_config?: BetaOutputConfig`

        Configuration options for the model's output. Controls aspects like how much effort the model puts into its response.

        - `effort?: "low" | "medium" | "high" | null`

          All possible effort levels.

          - `"low"`

          - `"medium"`

          - `"high"`

      - `output_format?: BetaJSONOutputFormat | null`

        A schema to specify Claude's output format in responses.

        - `schema: Record<string, unknown>`

          The JSON schema of the format

        - `type: "json_schema"`

          - `"json_schema"`

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

      - `system?: string | Array<BetaTextBlockParam>`

        System prompt.

        A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

        - `string`

        - `Array<BetaTextBlockParam>`

          - `text: string`

          - `type: "text"`

            - `"text"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `citations?: Array<BetaTextCitationParam> | null`

            - `BetaCitationCharLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_char_index: number`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `BetaCitationPageLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_page_number: number`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `BetaCitationContentBlockLocationParam`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_block_index: number`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `BetaCitationWebSearchResultLocationParam`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string | null`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `BetaCitationSearchResultLocationParam`

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

      - `thinking?: BetaThinkingConfigParam`

        Configuration for enabling Claude's extended thinking.

        When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

        See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

        - `BetaThinkingConfigEnabled`

          - `budget_tokens: number`

            Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

            Must be ≥1024 and less than `max_tokens`.

            See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

          - `type: "enabled"`

            - `"enabled"`

        - `BetaThinkingConfigDisabled`

          - `type: "disabled"`

            - `"disabled"`

      - `tool_choice?: BetaToolChoice`

        How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

        - `BetaToolChoiceAuto`

          The model will automatically decide whether to use tools.

          - `type: "auto"`

            - `"auto"`

          - `disable_parallel_tool_use?: boolean`

            Whether to disable parallel tool use.

            Defaults to `false`. If set to `true`, the model will output at most one tool use.

        - `BetaToolChoiceAny`

          The model will use any available tools.

          - `type: "any"`

            - `"any"`

          - `disable_parallel_tool_use?: boolean`

            Whether to disable parallel tool use.

            Defaults to `false`. If set to `true`, the model will output exactly one tool use.

        - `BetaToolChoiceTool`

          The model will use the specified tool with `tool_choice.name`.

          - `name: string`

            The name of the tool to use.

          - `type: "tool"`

            - `"tool"`

          - `disable_parallel_tool_use?: boolean`

            Whether to disable parallel tool use.

            Defaults to `false`. If set to `true`, the model will output exactly one tool use.

        - `BetaToolChoiceNone`

          The model will not be allowed to use tools.

          - `type: "none"`

            - `"none"`

      - `tools?: Array<BetaToolUnion>`

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

        - `BetaTool`

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

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `description?: string`

            Description of what this tool does.

            Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

          - `input_examples?: Array<Record<string, unknown>>`

          - `strict?: boolean`

          - `type?: "custom" | null`

            - `"custom"`

        - `BetaToolBash20241022`

          - `name: "bash"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"bash"`

          - `type: "bash_20241022"`

            - `"bash_20241022"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `input_examples?: Array<Record<string, unknown>>`

          - `strict?: boolean`

        - `BetaToolBash20250124`

          - `name: "bash"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"bash"`

          - `type: "bash_20250124"`

            - `"bash_20250124"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `input_examples?: Array<Record<string, unknown>>`

          - `strict?: boolean`

        - `BetaCodeExecutionTool20250522`

          - `name: "code_execution"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"code_execution"`

          - `type: "code_execution_20250522"`

            - `"code_execution_20250522"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `strict?: boolean`

        - `BetaCodeExecutionTool20250825`

          - `name: "code_execution"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"code_execution"`

          - `type: "code_execution_20250825"`

            - `"code_execution_20250825"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `strict?: boolean`

        - `BetaToolComputerUse20241022`

          - `display_height_px: number`

            The height of the display in pixels.

          - `display_width_px: number`

            The width of the display in pixels.

          - `name: "computer"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"computer"`

          - `type: "computer_20241022"`

            - `"computer_20241022"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `display_number?: number | null`

            The X11 display number (e.g. 0, 1) for the display.

          - `input_examples?: Array<Record<string, unknown>>`

          - `strict?: boolean`

        - `BetaMemoryTool20250818`

          - `name: "memory"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"memory"`

          - `type: "memory_20250818"`

            - `"memory_20250818"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `input_examples?: Array<Record<string, unknown>>`

          - `strict?: boolean`

        - `BetaToolComputerUse20250124`

          - `display_height_px: number`

            The height of the display in pixels.

          - `display_width_px: number`

            The width of the display in pixels.

          - `name: "computer"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"computer"`

          - `type: "computer_20250124"`

            - `"computer_20250124"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `display_number?: number | null`

            The X11 display number (e.g. 0, 1) for the display.

          - `input_examples?: Array<Record<string, unknown>>`

          - `strict?: boolean`

        - `BetaToolTextEditor20241022`

          - `name: "str_replace_editor"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"str_replace_editor"`

          - `type: "text_editor_20241022"`

            - `"text_editor_20241022"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `input_examples?: Array<Record<string, unknown>>`

          - `strict?: boolean`

        - `BetaToolComputerUse20251124`

          - `display_height_px: number`

            The height of the display in pixels.

          - `display_width_px: number`

            The width of the display in pixels.

          - `name: "computer"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"computer"`

          - `type: "computer_20251124"`

            - `"computer_20251124"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `display_number?: number | null`

            The X11 display number (e.g. 0, 1) for the display.

          - `enable_zoom?: boolean`

            Whether to enable an action to take a zoomed-in screenshot of the screen.

          - `input_examples?: Array<Record<string, unknown>>`

          - `strict?: boolean`

        - `BetaToolTextEditor20250124`

          - `name: "str_replace_editor"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"str_replace_editor"`

          - `type: "text_editor_20250124"`

            - `"text_editor_20250124"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `input_examples?: Array<Record<string, unknown>>`

          - `strict?: boolean`

        - `BetaToolTextEditor20250429`

          - `name: "str_replace_based_edit_tool"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"str_replace_based_edit_tool"`

          - `type: "text_editor_20250429"`

            - `"text_editor_20250429"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `input_examples?: Array<Record<string, unknown>>`

          - `strict?: boolean`

        - `BetaToolTextEditor20250728`

          - `name: "str_replace_based_edit_tool"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"str_replace_based_edit_tool"`

          - `type: "text_editor_20250728"`

            - `"text_editor_20250728"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `input_examples?: Array<Record<string, unknown>>`

          - `max_characters?: number | null`

            Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

          - `strict?: boolean`

        - `BetaWebSearchTool20250305`

          - `name: "web_search"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"web_search"`

          - `type: "web_search_20250305"`

            - `"web_search_20250305"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `allowed_domains?: Array<string> | null`

            If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

          - `blocked_domains?: Array<string> | null`

            If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `max_uses?: number | null`

            Maximum number of times the tool can be used in the API request.

          - `strict?: boolean`

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

        - `BetaWebFetchTool20250910`

          - `name: "web_fetch"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"web_fetch"`

          - `type: "web_fetch_20250910"`

            - `"web_fetch_20250910"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `allowed_domains?: Array<string> | null`

            List of domains to allow fetching from

          - `blocked_domains?: Array<string> | null`

            List of domains to block fetching from

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `citations?: BetaCitationsConfigParam | null`

            Citations configuration for fetched documents. Citations are disabled by default.

            - `enabled?: boolean`

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `max_content_tokens?: number | null`

            Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

          - `max_uses?: number | null`

            Maximum number of times the tool can be used in the API request.

          - `strict?: boolean`

        - `BetaToolSearchToolBm25_20251119`

          - `name: "tool_search_tool_bm25"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"tool_search_tool_bm25"`

          - `type: "tool_search_tool_bm25_20251119" | "tool_search_tool_bm25"`

            - `"tool_search_tool_bm25_20251119"`

            - `"tool_search_tool_bm25"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `strict?: boolean`

        - `BetaToolSearchToolRegex20251119`

          - `name: "tool_search_tool_regex"`

            Name of the tool.

            This is how the tool will be called by the model and in `tool_use` blocks.

            - `"tool_search_tool_regex"`

          - `type: "tool_search_tool_regex_20251119" | "tool_search_tool_regex"`

            - `"tool_search_tool_regex_20251119"`

            - `"tool_search_tool_regex"`

          - `allowed_callers?: Array<"direct" | "code_execution_20250825">`

            - `"direct"`

            - `"code_execution_20250825"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `defer_loading?: boolean`

            If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

          - `strict?: boolean`

        - `BetaMCPToolset`

          Configuration for a group of tools from an MCP server.

          Allows configuring enabled status and defer_loading for all tools
          from an MCP server, with optional per-tool overrides.

          - `mcp_server_name: string`

            Name of the MCP server to configure tools for

          - `type: "mcp_toolset"`

            - `"mcp_toolset"`

          - `cache_control?: BetaCacheControlEphemeral | null`

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

          - `configs?: Record<string, BetaMCPToolConfig> | null`

            Configuration overrides for specific tools, keyed by tool name

            - `defer_loading?: boolean`

            - `enabled?: boolean`

          - `default_config?: BetaMCPToolDefaultConfig`

            Default configuration applied to all tools from this server

            - `defer_loading?: boolean`

            - `enabled?: boolean`

      - `top_k?: number`

        Only sample from the top K options for each subsequent token.

        Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

        Recommended for advanced use cases only. You usually only need to use `temperature`.

      - `top_p?: number`

        Use nucleus sampling.

        In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

        Recommended for advanced use cases only. You usually only need to use `temperature`.

  - `betas?: Array<AnthropicBeta>`

    Header param: Optional header to specify the beta version(s) you want to use.

    - `(string & {})`

    - `"message-batches-2024-09-24" | "prompt-caching-2024-07-31" | "computer-use-2024-10-22" | 16 more`

      - `"message-batches-2024-09-24"`

      - `"prompt-caching-2024-07-31"`

      - `"computer-use-2024-10-22"`

      - `"computer-use-2025-01-24"`

      - `"pdfs-2024-09-25"`

      - `"token-counting-2024-11-01"`

      - `"token-efficient-tools-2025-02-19"`

      - `"output-128k-2025-02-19"`

      - `"files-api-2025-04-14"`

      - `"mcp-client-2025-04-04"`

      - `"mcp-client-2025-11-20"`

      - `"dev-full-thinking-2025-05-14"`

      - `"interleaved-thinking-2025-05-14"`

      - `"code-execution-2025-05-22"`

      - `"extended-cache-ttl-2025-04-11"`

      - `"context-1m-2025-08-07"`

      - `"context-management-2025-06-27"`

      - `"model-context-window-exceeded-2025-08-26"`

      - `"skills-2025-10-02"`

### Returns

- `BetaMessageBatch`

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

  - `request_counts: BetaMessageBatchRequestCounts`

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

const betaMessageBatch = await client.beta.messages.batches.create({
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

console.log(betaMessageBatch.id);
```

## Retrieve

`client.beta.messages.batches.retrieve(stringmessageBatchID, BatchRetrieveParamsparams?, RequestOptionsoptions?): BetaMessageBatch`

**get** `/v1/messages/batches/{message_batch_id}`

This endpoint is idempotent and can be used to poll for Message Batch completion. To access the results of a Message Batch, make a request to the `results_url` field in the response.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `messageBatchID: string`

  ID of the Message Batch.

- `params: BatchRetrieveParams`

  - `betas?: Array<AnthropicBeta>`

    Optional header to specify the beta version(s) you want to use.

    - `(string & {})`

    - `"message-batches-2024-09-24" | "prompt-caching-2024-07-31" | "computer-use-2024-10-22" | 16 more`

      - `"message-batches-2024-09-24"`

      - `"prompt-caching-2024-07-31"`

      - `"computer-use-2024-10-22"`

      - `"computer-use-2025-01-24"`

      - `"pdfs-2024-09-25"`

      - `"token-counting-2024-11-01"`

      - `"token-efficient-tools-2025-02-19"`

      - `"output-128k-2025-02-19"`

      - `"files-api-2025-04-14"`

      - `"mcp-client-2025-04-04"`

      - `"mcp-client-2025-11-20"`

      - `"dev-full-thinking-2025-05-14"`

      - `"interleaved-thinking-2025-05-14"`

      - `"code-execution-2025-05-22"`

      - `"extended-cache-ttl-2025-04-11"`

      - `"context-1m-2025-08-07"`

      - `"context-management-2025-06-27"`

      - `"model-context-window-exceeded-2025-08-26"`

      - `"skills-2025-10-02"`

### Returns

- `BetaMessageBatch`

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

  - `request_counts: BetaMessageBatchRequestCounts`

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

const betaMessageBatch = await client.beta.messages.batches.retrieve('message_batch_id');

console.log(betaMessageBatch.id);
```

## List

`client.beta.messages.batches.list(BatchListParamsparams?, RequestOptionsoptions?): Page<BetaMessageBatch>`

**get** `/v1/messages/batches`

List all Message Batches within a Workspace. Most recently created batches are returned first.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `params: BatchListParams`

  - `after_id?: string`

    Query param: ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

  - `before_id?: string`

    Query param: ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

  - `limit?: number`

    Query param: Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `1000`.

  - `betas?: Array<AnthropicBeta>`

    Header param: Optional header to specify the beta version(s) you want to use.

    - `(string & {})`

    - `"message-batches-2024-09-24" | "prompt-caching-2024-07-31" | "computer-use-2024-10-22" | 16 more`

      - `"message-batches-2024-09-24"`

      - `"prompt-caching-2024-07-31"`

      - `"computer-use-2024-10-22"`

      - `"computer-use-2025-01-24"`

      - `"pdfs-2024-09-25"`

      - `"token-counting-2024-11-01"`

      - `"token-efficient-tools-2025-02-19"`

      - `"output-128k-2025-02-19"`

      - `"files-api-2025-04-14"`

      - `"mcp-client-2025-04-04"`

      - `"mcp-client-2025-11-20"`

      - `"dev-full-thinking-2025-05-14"`

      - `"interleaved-thinking-2025-05-14"`

      - `"code-execution-2025-05-22"`

      - `"extended-cache-ttl-2025-04-11"`

      - `"context-1m-2025-08-07"`

      - `"context-management-2025-06-27"`

      - `"model-context-window-exceeded-2025-08-26"`

      - `"skills-2025-10-02"`

### Returns

- `BetaMessageBatch`

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

  - `request_counts: BetaMessageBatchRequestCounts`

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

// Automatically fetches more pages as needed.
for await (const betaMessageBatch of client.beta.messages.batches.list()) {
  console.log(betaMessageBatch.id);
}
```

## Cancel

`client.beta.messages.batches.cancel(stringmessageBatchID, BatchCancelParamsparams?, RequestOptionsoptions?): BetaMessageBatch`

**post** `/v1/messages/batches/{message_batch_id}/cancel`

Batches may be canceled any time before processing ends. Once cancellation is initiated, the batch enters a `canceling` state, at which time the system may complete any in-progress, non-interruptible requests before finalizing cancellation.

The number of canceled requests is specified in `request_counts`. To determine which requests were canceled, check the individual results within the batch. Note that cancellation may not result in any canceled requests if they were non-interruptible.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `messageBatchID: string`

  ID of the Message Batch.

- `params: BatchCancelParams`

  - `betas?: Array<AnthropicBeta>`

    Optional header to specify the beta version(s) you want to use.

    - `(string & {})`

    - `"message-batches-2024-09-24" | "prompt-caching-2024-07-31" | "computer-use-2024-10-22" | 16 more`

      - `"message-batches-2024-09-24"`

      - `"prompt-caching-2024-07-31"`

      - `"computer-use-2024-10-22"`

      - `"computer-use-2025-01-24"`

      - `"pdfs-2024-09-25"`

      - `"token-counting-2024-11-01"`

      - `"token-efficient-tools-2025-02-19"`

      - `"output-128k-2025-02-19"`

      - `"files-api-2025-04-14"`

      - `"mcp-client-2025-04-04"`

      - `"mcp-client-2025-11-20"`

      - `"dev-full-thinking-2025-05-14"`

      - `"interleaved-thinking-2025-05-14"`

      - `"code-execution-2025-05-22"`

      - `"extended-cache-ttl-2025-04-11"`

      - `"context-1m-2025-08-07"`

      - `"context-management-2025-06-27"`

      - `"model-context-window-exceeded-2025-08-26"`

      - `"skills-2025-10-02"`

### Returns

- `BetaMessageBatch`

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

  - `request_counts: BetaMessageBatchRequestCounts`

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

const betaMessageBatch = await client.beta.messages.batches.cancel('message_batch_id');

console.log(betaMessageBatch.id);
```

## Delete

`client.beta.messages.batches.delete(stringmessageBatchID, BatchDeleteParamsparams?, RequestOptionsoptions?): BetaDeletedMessageBatch`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `messageBatchID: string`

  ID of the Message Batch.

- `params: BatchDeleteParams`

  - `betas?: Array<AnthropicBeta>`

    Optional header to specify the beta version(s) you want to use.

    - `(string & {})`

    - `"message-batches-2024-09-24" | "prompt-caching-2024-07-31" | "computer-use-2024-10-22" | 16 more`

      - `"message-batches-2024-09-24"`

      - `"prompt-caching-2024-07-31"`

      - `"computer-use-2024-10-22"`

      - `"computer-use-2025-01-24"`

      - `"pdfs-2024-09-25"`

      - `"token-counting-2024-11-01"`

      - `"token-efficient-tools-2025-02-19"`

      - `"output-128k-2025-02-19"`

      - `"files-api-2025-04-14"`

      - `"mcp-client-2025-04-04"`

      - `"mcp-client-2025-11-20"`

      - `"dev-full-thinking-2025-05-14"`

      - `"interleaved-thinking-2025-05-14"`

      - `"code-execution-2025-05-22"`

      - `"extended-cache-ttl-2025-04-11"`

      - `"context-1m-2025-08-07"`

      - `"context-management-2025-06-27"`

      - `"model-context-window-exceeded-2025-08-26"`

      - `"skills-2025-10-02"`

### Returns

- `BetaDeletedMessageBatch`

  - `id: string`

    ID of the Message Batch.

  - `type: "message_batch_deleted"`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `"message_batch_deleted"`

### Example

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: 'my-anthropic-api-key',
});

const betaDeletedMessageBatch = await client.beta.messages.batches.delete('message_batch_id');

console.log(betaDeletedMessageBatch.id);
```

## Results

`client.beta.messages.batches.results(stringmessageBatchID, BatchResultsParamsparams?, RequestOptionsoptions?): BetaMessageBatchIndividualResponse | Stream<BetaMessageBatchIndividualResponse>`

**get** `/v1/messages/batches/{message_batch_id}/results`

Streams the results of a Message Batch as a `.jsonl` file.

Each line in the file is a JSON object containing the result of a single request in the Message Batch. Results are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `messageBatchID: string`

  ID of the Message Batch.

- `params: BatchResultsParams`

  - `betas?: Array<AnthropicBeta>`

    Optional header to specify the beta version(s) you want to use.

    - `(string & {})`

    - `"message-batches-2024-09-24" | "prompt-caching-2024-07-31" | "computer-use-2024-10-22" | 16 more`

      - `"message-batches-2024-09-24"`

      - `"prompt-caching-2024-07-31"`

      - `"computer-use-2024-10-22"`

      - `"computer-use-2025-01-24"`

      - `"pdfs-2024-09-25"`

      - `"token-counting-2024-11-01"`

      - `"token-efficient-tools-2025-02-19"`

      - `"output-128k-2025-02-19"`

      - `"files-api-2025-04-14"`

      - `"mcp-client-2025-04-04"`

      - `"mcp-client-2025-11-20"`

      - `"dev-full-thinking-2025-05-14"`

      - `"interleaved-thinking-2025-05-14"`

      - `"code-execution-2025-05-22"`

      - `"extended-cache-ttl-2025-04-11"`

      - `"context-1m-2025-08-07"`

      - `"context-management-2025-06-27"`

      - `"model-context-window-exceeded-2025-08-26"`

      - `"skills-2025-10-02"`

### Returns

- `BetaMessageBatchIndividualResponse`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `custom_id: string`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: BetaMessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `BetaMessageBatchSucceededResult`

      - `message: BetaMessage`

        - `id: string`

          Unique object identifier.

          The format and length of IDs may change over time.

        - `container: BetaContainer | null`

          Information about the container used in the request (for the code execution tool)

          - `id: string`

            Identifier for the container used in this request

          - `expires_at: string`

            The time at which the container will expire.

          - `skills: Array<BetaSkill> | null`

            Skills loaded in the container

            - `skill_id: string`

              Skill ID

            - `type: "anthropic" | "custom"`

              Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

              - `"anthropic"`

              - `"custom"`

            - `version: string`

              Skill version or 'latest' for most recent version

        - `content: Array<BetaContentBlock>`

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

          - `BetaTextBlock`

            - `citations: Array<BetaTextCitation> | null`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `BetaCitationCharLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_char_index: number`

                - `file_id: string | null`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `BetaCitationPageLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_page_number: number`

                - `file_id: string | null`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `BetaCitationContentBlockLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_block_index: number`

                - `file_id: string | null`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `BetaCitationsWebSearchResultLocation`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string | null`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `BetaCitationSearchResultLocation`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string | null`

                - `type: "search_result_location"`

                  - `"search_result_location"`

            - `text: string`

            - `type: "text"`

              - `"text"`

          - `BetaThinkingBlock`

            - `signature: string`

            - `thinking: string`

            - `type: "thinking"`

              - `"thinking"`

          - `BetaRedactedThinkingBlock`

            - `data: string`

            - `type: "redacted_thinking"`

              - `"redacted_thinking"`

          - `BetaToolUseBlock`

            - `id: string`

            - `input: Record<string, unknown>`

            - `name: string`

            - `type: "tool_use"`

              - `"tool_use"`

            - `caller?: BetaDirectCaller | BetaServerToolCaller`

              Tool invocation directly from the model.

              - `BetaDirectCaller`

                Tool invocation directly from the model.

                - `type: "direct"`

                  - `"direct"`

              - `BetaServerToolCaller`

                Tool invocation generated by a server-side tool.

                - `tool_id: string`

                - `type: "code_execution_20250825"`

                  - `"code_execution_20250825"`

          - `BetaServerToolUseBlock`

            - `id: string`

            - `caller: BetaDirectCaller | BetaServerToolCaller`

              Tool invocation directly from the model.

              - `BetaDirectCaller`

                Tool invocation directly from the model.

                - `type: "direct"`

                  - `"direct"`

              - `BetaServerToolCaller`

                Tool invocation generated by a server-side tool.

                - `tool_id: string`

                - `type: "code_execution_20250825"`

                  - `"code_execution_20250825"`

            - `input: Record<string, unknown>`

            - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

              - `"web_search"`

              - `"web_fetch"`

              - `"code_execution"`

              - `"bash_code_execution"`

              - `"text_editor_code_execution"`

              - `"tool_search_tool_regex"`

              - `"tool_search_tool_bm25"`

            - `type: "server_tool_use"`

              - `"server_tool_use"`

          - `BetaWebSearchToolResultBlock`

            - `content: BetaWebSearchToolResultBlockContent`

              - `BetaWebSearchToolResultError`

                - `error_code: BetaWebSearchToolResultErrorCode`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"max_uses_exceeded"`

                  - `"too_many_requests"`

                  - `"query_too_long"`

                - `type: "web_search_tool_result_error"`

                  - `"web_search_tool_result_error"`

              - `Array<BetaWebSearchResultBlock>`

                - `encrypted_content: string`

                - `page_age: string | null`

                - `title: string`

                - `type: "web_search_result"`

                  - `"web_search_result"`

                - `url: string`

            - `tool_use_id: string`

            - `type: "web_search_tool_result"`

              - `"web_search_tool_result"`

          - `BetaWebFetchToolResultBlock`

            - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

              - `BetaWebFetchToolResultErrorBlock`

                - `error_code: BetaWebFetchToolResultErrorCode`

                  - `"invalid_tool_input"`

                  - `"url_too_long"`

                  - `"url_not_allowed"`

                  - `"url_not_accessible"`

                  - `"unsupported_content_type"`

                  - `"too_many_requests"`

                  - `"max_uses_exceeded"`

                  - `"unavailable"`

                - `type: "web_fetch_tool_result_error"`

                  - `"web_fetch_tool_result_error"`

              - `BetaWebFetchBlock`

                - `content: BetaDocumentBlock`

                  - `citations: BetaCitationConfig | null`

                    Citation configuration for the document

                    - `enabled: boolean`

                  - `source: BetaBase64PDFSource | BetaPlainTextSource`

                    - `BetaBase64PDFSource`

                      - `data: string`

                      - `media_type: "application/pdf"`

                        - `"application/pdf"`

                      - `type: "base64"`

                        - `"base64"`

                    - `BetaPlainTextSource`

                      - `data: string`

                      - `media_type: "text/plain"`

                        - `"text/plain"`

                      - `type: "text"`

                        - `"text"`

                  - `title: string | null`

                    The title of the document

                  - `type: "document"`

                    - `"document"`

                - `retrieved_at: string | null`

                  ISO 8601 timestamp when the content was retrieved

                - `type: "web_fetch_result"`

                  - `"web_fetch_result"`

                - `url: string`

                  Fetched content URL

            - `tool_use_id: string`

            - `type: "web_fetch_tool_result"`

              - `"web_fetch_tool_result"`

          - `BetaCodeExecutionToolResultBlock`

            - `content: BetaCodeExecutionToolResultBlockContent`

              - `BetaCodeExecutionToolResultError`

                - `error_code: BetaCodeExecutionToolResultErrorCode`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"too_many_requests"`

                  - `"execution_time_exceeded"`

                - `type: "code_execution_tool_result_error"`

                  - `"code_execution_tool_result_error"`

              - `BetaCodeExecutionResultBlock`

                - `content: Array<BetaCodeExecutionOutputBlock>`

                  - `file_id: string`

                  - `type: "code_execution_output"`

                    - `"code_execution_output"`

                - `return_code: number`

                - `stderr: string`

                - `stdout: string`

                - `type: "code_execution_result"`

                  - `"code_execution_result"`

            - `tool_use_id: string`

            - `type: "code_execution_tool_result"`

              - `"code_execution_tool_result"`

          - `BetaBashCodeExecutionToolResultBlock`

            - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

              - `BetaBashCodeExecutionToolResultError`

                - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"too_many_requests"`

                  - `"execution_time_exceeded"`

                  - `"output_file_too_large"`

                - `type: "bash_code_execution_tool_result_error"`

                  - `"bash_code_execution_tool_result_error"`

              - `BetaBashCodeExecutionResultBlock`

                - `content: Array<BetaBashCodeExecutionOutputBlock>`

                  - `file_id: string`

                  - `type: "bash_code_execution_output"`

                    - `"bash_code_execution_output"`

                - `return_code: number`

                - `stderr: string`

                - `stdout: string`

                - `type: "bash_code_execution_result"`

                  - `"bash_code_execution_result"`

            - `tool_use_id: string`

            - `type: "bash_code_execution_tool_result"`

              - `"bash_code_execution_tool_result"`

          - `BetaTextEditorCodeExecutionToolResultBlock`

            - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

              - `BetaTextEditorCodeExecutionToolResultError`

                - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"too_many_requests"`

                  - `"execution_time_exceeded"`

                  - `"file_not_found"`

                - `error_message: string | null`

                - `type: "text_editor_code_execution_tool_result_error"`

                  - `"text_editor_code_execution_tool_result_error"`

              - `BetaTextEditorCodeExecutionViewResultBlock`

                - `content: string`

                - `file_type: "text" | "image" | "pdf"`

                  - `"text"`

                  - `"image"`

                  - `"pdf"`

                - `num_lines: number | null`

                - `start_line: number | null`

                - `total_lines: number | null`

                - `type: "text_editor_code_execution_view_result"`

                  - `"text_editor_code_execution_view_result"`

              - `BetaTextEditorCodeExecutionCreateResultBlock`

                - `is_file_update: boolean`

                - `type: "text_editor_code_execution_create_result"`

                  - `"text_editor_code_execution_create_result"`

              - `BetaTextEditorCodeExecutionStrReplaceResultBlock`

                - `lines: Array<string> | null`

                - `new_lines: number | null`

                - `new_start: number | null`

                - `old_lines: number | null`

                - `old_start: number | null`

                - `type: "text_editor_code_execution_str_replace_result"`

                  - `"text_editor_code_execution_str_replace_result"`

            - `tool_use_id: string`

            - `type: "text_editor_code_execution_tool_result"`

              - `"text_editor_code_execution_tool_result"`

          - `BetaToolSearchToolResultBlock`

            - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

              - `BetaToolSearchToolResultError`

                - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"too_many_requests"`

                  - `"execution_time_exceeded"`

                - `error_message: string | null`

                - `type: "tool_search_tool_result_error"`

                  - `"tool_search_tool_result_error"`

              - `BetaToolSearchToolSearchResultBlock`

                - `tool_references: Array<BetaToolReferenceBlock>`

                  - `tool_name: string`

                  - `type: "tool_reference"`

                    - `"tool_reference"`

                - `type: "tool_search_tool_search_result"`

                  - `"tool_search_tool_search_result"`

            - `tool_use_id: string`

            - `type: "tool_search_tool_result"`

              - `"tool_search_tool_result"`

          - `BetaMCPToolUseBlock`

            - `id: string`

            - `input: Record<string, unknown>`

            - `name: string`

              The name of the MCP tool

            - `server_name: string`

              The name of the MCP server

            - `type: "mcp_tool_use"`

              - `"mcp_tool_use"`

          - `BetaMCPToolResultBlock`

            - `content: string | Array<BetaTextBlock>`

              - `string`

              - `Array<BetaTextBlock>`

                - `citations: Array<BetaTextCitation> | null`

                  Citations supporting the text block.

                  The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

                  - `BetaCitationCharLocation`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_char_index: number`

                    - `file_id: string | null`

                    - `start_char_index: number`

                    - `type: "char_location"`

                      - `"char_location"`

                  - `BetaCitationPageLocation`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_page_number: number`

                    - `file_id: string | null`

                    - `start_page_number: number`

                    - `type: "page_location"`

                      - `"page_location"`

                  - `BetaCitationContentBlockLocation`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_block_index: number`

                    - `file_id: string | null`

                    - `start_block_index: number`

                    - `type: "content_block_location"`

                      - `"content_block_location"`

                  - `BetaCitationsWebSearchResultLocation`

                    - `cited_text: string`

                    - `encrypted_index: string`

                    - `title: string | null`

                    - `type: "web_search_result_location"`

                      - `"web_search_result_location"`

                    - `url: string`

                  - `BetaCitationSearchResultLocation`

                    - `cited_text: string`

                    - `end_block_index: number`

                    - `search_result_index: number`

                    - `source: string`

                    - `start_block_index: number`

                    - `title: string | null`

                    - `type: "search_result_location"`

                      - `"search_result_location"`

                - `text: string`

                - `type: "text"`

                  - `"text"`

            - `is_error: boolean`

            - `tool_use_id: string`

            - `type: "mcp_tool_result"`

              - `"mcp_tool_result"`

          - `BetaContainerUploadBlock`

            Response model for a file uploaded to the container.

            - `file_id: string`

            - `type: "container_upload"`

              - `"container_upload"`

        - `context_management: BetaContextManagementResponse | null`

          Context management response.

          Information about context management strategies applied during the request.

          - `applied_edits: Array<BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse>`

            List of context management edits that were applied.

            - `BetaClearToolUses20250919EditResponse`

              - `cleared_input_tokens: number`

                Number of input tokens cleared by this edit.

              - `cleared_tool_uses: number`

                Number of tool uses that were cleared.

              - `type: "clear_tool_uses_20250919"`

                The type of context management edit applied.

                - `"clear_tool_uses_20250919"`

            - `BetaClearThinking20251015EditResponse`

              - `cleared_input_tokens: number`

                Number of input tokens cleared by this edit.

              - `cleared_thinking_turns: number`

                Number of thinking turns that were cleared.

              - `type: "clear_thinking_20251015"`

                The type of context management edit applied.

                - `"clear_thinking_20251015"`

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

        - `role: "assistant"`

          Conversational role of the generated message.

          This will always be `"assistant"`.

          - `"assistant"`

        - `stop_reason: BetaStopReason | null`

          The reason that we stopped.

          This may be one the following values:

          * `"end_turn"`: the model reached a natural stopping point
          * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
          * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
          * `"tool_use"`: the model invoked one or more tools
          * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
          * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

          In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

          - `"end_turn"`

          - `"max_tokens"`

          - `"stop_sequence"`

          - `"tool_use"`

          - `"pause_turn"`

          - `"refusal"`

          - `"model_context_window_exceeded"`

        - `stop_sequence: string | null`

          Which custom stop sequence was generated, if any.

          This value will be a non-null string if one of your custom stop sequences was generated.

        - `type: "message"`

          Object type.

          For Messages, this is always `"message"`.

          - `"message"`

        - `usage: BetaUsage`

          Billing and rate-limit usage.

          Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

          Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

          For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

          Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

          - `cache_creation: BetaCacheCreation | null`

            Breakdown of cached tokens by TTL

            - `ephemeral_1h_input_tokens: number`

              The number of input tokens used to create the 1 hour cache entry.

            - `ephemeral_5m_input_tokens: number`

              The number of input tokens used to create the 5 minute cache entry.

          - `cache_creation_input_tokens: number | null`

            The number of input tokens used to create the cache entry.

          - `cache_read_input_tokens: number | null`

            The number of input tokens read from the cache.

          - `input_tokens: number`

            The number of input tokens which were used.

          - `output_tokens: number`

            The number of output tokens which were used.

          - `server_tool_use: BetaServerToolUsage | null`

            The number of server tool requests.

            - `web_fetch_requests: number`

              The number of web fetch tool requests.

            - `web_search_requests: number`

              The number of web search tool requests.

          - `service_tier: "standard" | "priority" | "batch" | null`

            If the request used the priority, standard, or batch tier.

            - `"standard"`

            - `"priority"`

            - `"batch"`

      - `type: "succeeded"`

        - `"succeeded"`

    - `BetaMessageBatchErroredResult`

      - `error: BetaErrorResponse`

        - `error: BetaError`

          - `BetaInvalidRequestError`

            - `message: string`

            - `type: "invalid_request_error"`

              - `"invalid_request_error"`

          - `BetaAuthenticationError`

            - `message: string`

            - `type: "authentication_error"`

              - `"authentication_error"`

          - `BetaBillingError`

            - `message: string`

            - `type: "billing_error"`

              - `"billing_error"`

          - `BetaPermissionError`

            - `message: string`

            - `type: "permission_error"`

              - `"permission_error"`

          - `BetaNotFoundError`

            - `message: string`

            - `type: "not_found_error"`

              - `"not_found_error"`

          - `BetaRateLimitError`

            - `message: string`

            - `type: "rate_limit_error"`

              - `"rate_limit_error"`

          - `BetaGatewayTimeoutError`

            - `message: string`

            - `type: "timeout_error"`

              - `"timeout_error"`

          - `BetaAPIError`

            - `message: string`

            - `type: "api_error"`

              - `"api_error"`

          - `BetaOverloadedError`

            - `message: string`

            - `type: "overloaded_error"`

              - `"overloaded_error"`

        - `request_id: string | null`

        - `type: "error"`

          - `"error"`

      - `type: "errored"`

        - `"errored"`

    - `BetaMessageBatchCanceledResult`

      - `type: "canceled"`

        - `"canceled"`

    - `BetaMessageBatchExpiredResult`

      - `type: "expired"`

        - `"expired"`

### Example

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: 'my-anthropic-api-key',
});

const betaMessageBatchIndividualResponse = await client.beta.messages.batches.results('message_batch_id');

console.log(betaMessageBatchIndividualResponse.custom_id);
```

## Domain Types

### Beta Deleted Message Batch

- `BetaDeletedMessageBatch`

  - `id: string`

    ID of the Message Batch.

  - `type: "message_batch_deleted"`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `"message_batch_deleted"`

### Beta Message Batch

- `BetaMessageBatch`

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

  - `request_counts: BetaMessageBatchRequestCounts`

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

### Beta Message Batch Canceled Result

- `BetaMessageBatchCanceledResult`

  - `type: "canceled"`

    - `"canceled"`

### Beta Message Batch Errored Result

- `BetaMessageBatchErroredResult`

  - `error: BetaErrorResponse`

    - `error: BetaError`

      - `BetaInvalidRequestError`

        - `message: string`

        - `type: "invalid_request_error"`

          - `"invalid_request_error"`

      - `BetaAuthenticationError`

        - `message: string`

        - `type: "authentication_error"`

          - `"authentication_error"`

      - `BetaBillingError`

        - `message: string`

        - `type: "billing_error"`

          - `"billing_error"`

      - `BetaPermissionError`

        - `message: string`

        - `type: "permission_error"`

          - `"permission_error"`

      - `BetaNotFoundError`

        - `message: string`

        - `type: "not_found_error"`

          - `"not_found_error"`

      - `BetaRateLimitError`

        - `message: string`

        - `type: "rate_limit_error"`

          - `"rate_limit_error"`

      - `BetaGatewayTimeoutError`

        - `message: string`

        - `type: "timeout_error"`

          - `"timeout_error"`

      - `BetaAPIError`

        - `message: string`

        - `type: "api_error"`

          - `"api_error"`

      - `BetaOverloadedError`

        - `message: string`

        - `type: "overloaded_error"`

          - `"overloaded_error"`

    - `request_id: string | null`

    - `type: "error"`

      - `"error"`

  - `type: "errored"`

    - `"errored"`

### Beta Message Batch Expired Result

- `BetaMessageBatchExpiredResult`

  - `type: "expired"`

    - `"expired"`

### Beta Message Batch Individual Response

- `BetaMessageBatchIndividualResponse`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `custom_id: string`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: BetaMessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `BetaMessageBatchSucceededResult`

      - `message: BetaMessage`

        - `id: string`

          Unique object identifier.

          The format and length of IDs may change over time.

        - `container: BetaContainer | null`

          Information about the container used in the request (for the code execution tool)

          - `id: string`

            Identifier for the container used in this request

          - `expires_at: string`

            The time at which the container will expire.

          - `skills: Array<BetaSkill> | null`

            Skills loaded in the container

            - `skill_id: string`

              Skill ID

            - `type: "anthropic" | "custom"`

              Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

              - `"anthropic"`

              - `"custom"`

            - `version: string`

              Skill version or 'latest' for most recent version

        - `content: Array<BetaContentBlock>`

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

          - `BetaTextBlock`

            - `citations: Array<BetaTextCitation> | null`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `BetaCitationCharLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_char_index: number`

                - `file_id: string | null`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `BetaCitationPageLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_page_number: number`

                - `file_id: string | null`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `BetaCitationContentBlockLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_block_index: number`

                - `file_id: string | null`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `BetaCitationsWebSearchResultLocation`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string | null`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `BetaCitationSearchResultLocation`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string | null`

                - `type: "search_result_location"`

                  - `"search_result_location"`

            - `text: string`

            - `type: "text"`

              - `"text"`

          - `BetaThinkingBlock`

            - `signature: string`

            - `thinking: string`

            - `type: "thinking"`

              - `"thinking"`

          - `BetaRedactedThinkingBlock`

            - `data: string`

            - `type: "redacted_thinking"`

              - `"redacted_thinking"`

          - `BetaToolUseBlock`

            - `id: string`

            - `input: Record<string, unknown>`

            - `name: string`

            - `type: "tool_use"`

              - `"tool_use"`

            - `caller?: BetaDirectCaller | BetaServerToolCaller`

              Tool invocation directly from the model.

              - `BetaDirectCaller`

                Tool invocation directly from the model.

                - `type: "direct"`

                  - `"direct"`

              - `BetaServerToolCaller`

                Tool invocation generated by a server-side tool.

                - `tool_id: string`

                - `type: "code_execution_20250825"`

                  - `"code_execution_20250825"`

          - `BetaServerToolUseBlock`

            - `id: string`

            - `caller: BetaDirectCaller | BetaServerToolCaller`

              Tool invocation directly from the model.

              - `BetaDirectCaller`

                Tool invocation directly from the model.

                - `type: "direct"`

                  - `"direct"`

              - `BetaServerToolCaller`

                Tool invocation generated by a server-side tool.

                - `tool_id: string`

                - `type: "code_execution_20250825"`

                  - `"code_execution_20250825"`

            - `input: Record<string, unknown>`

            - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

              - `"web_search"`

              - `"web_fetch"`

              - `"code_execution"`

              - `"bash_code_execution"`

              - `"text_editor_code_execution"`

              - `"tool_search_tool_regex"`

              - `"tool_search_tool_bm25"`

            - `type: "server_tool_use"`

              - `"server_tool_use"`

          - `BetaWebSearchToolResultBlock`

            - `content: BetaWebSearchToolResultBlockContent`

              - `BetaWebSearchToolResultError`

                - `error_code: BetaWebSearchToolResultErrorCode`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"max_uses_exceeded"`

                  - `"too_many_requests"`

                  - `"query_too_long"`

                - `type: "web_search_tool_result_error"`

                  - `"web_search_tool_result_error"`

              - `Array<BetaWebSearchResultBlock>`

                - `encrypted_content: string`

                - `page_age: string | null`

                - `title: string`

                - `type: "web_search_result"`

                  - `"web_search_result"`

                - `url: string`

            - `tool_use_id: string`

            - `type: "web_search_tool_result"`

              - `"web_search_tool_result"`

          - `BetaWebFetchToolResultBlock`

            - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

              - `BetaWebFetchToolResultErrorBlock`

                - `error_code: BetaWebFetchToolResultErrorCode`

                  - `"invalid_tool_input"`

                  - `"url_too_long"`

                  - `"url_not_allowed"`

                  - `"url_not_accessible"`

                  - `"unsupported_content_type"`

                  - `"too_many_requests"`

                  - `"max_uses_exceeded"`

                  - `"unavailable"`

                - `type: "web_fetch_tool_result_error"`

                  - `"web_fetch_tool_result_error"`

              - `BetaWebFetchBlock`

                - `content: BetaDocumentBlock`

                  - `citations: BetaCitationConfig | null`

                    Citation configuration for the document

                    - `enabled: boolean`

                  - `source: BetaBase64PDFSource | BetaPlainTextSource`

                    - `BetaBase64PDFSource`

                      - `data: string`

                      - `media_type: "application/pdf"`

                        - `"application/pdf"`

                      - `type: "base64"`

                        - `"base64"`

                    - `BetaPlainTextSource`

                      - `data: string`

                      - `media_type: "text/plain"`

                        - `"text/plain"`

                      - `type: "text"`

                        - `"text"`

                  - `title: string | null`

                    The title of the document

                  - `type: "document"`

                    - `"document"`

                - `retrieved_at: string | null`

                  ISO 8601 timestamp when the content was retrieved

                - `type: "web_fetch_result"`

                  - `"web_fetch_result"`

                - `url: string`

                  Fetched content URL

            - `tool_use_id: string`

            - `type: "web_fetch_tool_result"`

              - `"web_fetch_tool_result"`

          - `BetaCodeExecutionToolResultBlock`

            - `content: BetaCodeExecutionToolResultBlockContent`

              - `BetaCodeExecutionToolResultError`

                - `error_code: BetaCodeExecutionToolResultErrorCode`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"too_many_requests"`

                  - `"execution_time_exceeded"`

                - `type: "code_execution_tool_result_error"`

                  - `"code_execution_tool_result_error"`

              - `BetaCodeExecutionResultBlock`

                - `content: Array<BetaCodeExecutionOutputBlock>`

                  - `file_id: string`

                  - `type: "code_execution_output"`

                    - `"code_execution_output"`

                - `return_code: number`

                - `stderr: string`

                - `stdout: string`

                - `type: "code_execution_result"`

                  - `"code_execution_result"`

            - `tool_use_id: string`

            - `type: "code_execution_tool_result"`

              - `"code_execution_tool_result"`

          - `BetaBashCodeExecutionToolResultBlock`

            - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

              - `BetaBashCodeExecutionToolResultError`

                - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"too_many_requests"`

                  - `"execution_time_exceeded"`

                  - `"output_file_too_large"`

                - `type: "bash_code_execution_tool_result_error"`

                  - `"bash_code_execution_tool_result_error"`

              - `BetaBashCodeExecutionResultBlock`

                - `content: Array<BetaBashCodeExecutionOutputBlock>`

                  - `file_id: string`

                  - `type: "bash_code_execution_output"`

                    - `"bash_code_execution_output"`

                - `return_code: number`

                - `stderr: string`

                - `stdout: string`

                - `type: "bash_code_execution_result"`

                  - `"bash_code_execution_result"`

            - `tool_use_id: string`

            - `type: "bash_code_execution_tool_result"`

              - `"bash_code_execution_tool_result"`

          - `BetaTextEditorCodeExecutionToolResultBlock`

            - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

              - `BetaTextEditorCodeExecutionToolResultError`

                - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"too_many_requests"`

                  - `"execution_time_exceeded"`

                  - `"file_not_found"`

                - `error_message: string | null`

                - `type: "text_editor_code_execution_tool_result_error"`

                  - `"text_editor_code_execution_tool_result_error"`

              - `BetaTextEditorCodeExecutionViewResultBlock`

                - `content: string`

                - `file_type: "text" | "image" | "pdf"`

                  - `"text"`

                  - `"image"`

                  - `"pdf"`

                - `num_lines: number | null`

                - `start_line: number | null`

                - `total_lines: number | null`

                - `type: "text_editor_code_execution_view_result"`

                  - `"text_editor_code_execution_view_result"`

              - `BetaTextEditorCodeExecutionCreateResultBlock`

                - `is_file_update: boolean`

                - `type: "text_editor_code_execution_create_result"`

                  - `"text_editor_code_execution_create_result"`

              - `BetaTextEditorCodeExecutionStrReplaceResultBlock`

                - `lines: Array<string> | null`

                - `new_lines: number | null`

                - `new_start: number | null`

                - `old_lines: number | null`

                - `old_start: number | null`

                - `type: "text_editor_code_execution_str_replace_result"`

                  - `"text_editor_code_execution_str_replace_result"`

            - `tool_use_id: string`

            - `type: "text_editor_code_execution_tool_result"`

              - `"text_editor_code_execution_tool_result"`

          - `BetaToolSearchToolResultBlock`

            - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

              - `BetaToolSearchToolResultError`

                - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"too_many_requests"`

                  - `"execution_time_exceeded"`

                - `error_message: string | null`

                - `type: "tool_search_tool_result_error"`

                  - `"tool_search_tool_result_error"`

              - `BetaToolSearchToolSearchResultBlock`

                - `tool_references: Array<BetaToolReferenceBlock>`

                  - `tool_name: string`

                  - `type: "tool_reference"`

                    - `"tool_reference"`

                - `type: "tool_search_tool_search_result"`

                  - `"tool_search_tool_search_result"`

            - `tool_use_id: string`

            - `type: "tool_search_tool_result"`

              - `"tool_search_tool_result"`

          - `BetaMCPToolUseBlock`

            - `id: string`

            - `input: Record<string, unknown>`

            - `name: string`

              The name of the MCP tool

            - `server_name: string`

              The name of the MCP server

            - `type: "mcp_tool_use"`

              - `"mcp_tool_use"`

          - `BetaMCPToolResultBlock`

            - `content: string | Array<BetaTextBlock>`

              - `string`

              - `Array<BetaTextBlock>`

                - `citations: Array<BetaTextCitation> | null`

                  Citations supporting the text block.

                  The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

                  - `BetaCitationCharLocation`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_char_index: number`

                    - `file_id: string | null`

                    - `start_char_index: number`

                    - `type: "char_location"`

                      - `"char_location"`

                  - `BetaCitationPageLocation`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_page_number: number`

                    - `file_id: string | null`

                    - `start_page_number: number`

                    - `type: "page_location"`

                      - `"page_location"`

                  - `BetaCitationContentBlockLocation`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string | null`

                    - `end_block_index: number`

                    - `file_id: string | null`

                    - `start_block_index: number`

                    - `type: "content_block_location"`

                      - `"content_block_location"`

                  - `BetaCitationsWebSearchResultLocation`

                    - `cited_text: string`

                    - `encrypted_index: string`

                    - `title: string | null`

                    - `type: "web_search_result_location"`

                      - `"web_search_result_location"`

                    - `url: string`

                  - `BetaCitationSearchResultLocation`

                    - `cited_text: string`

                    - `end_block_index: number`

                    - `search_result_index: number`

                    - `source: string`

                    - `start_block_index: number`

                    - `title: string | null`

                    - `type: "search_result_location"`

                      - `"search_result_location"`

                - `text: string`

                - `type: "text"`

                  - `"text"`

            - `is_error: boolean`

            - `tool_use_id: string`

            - `type: "mcp_tool_result"`

              - `"mcp_tool_result"`

          - `BetaContainerUploadBlock`

            Response model for a file uploaded to the container.

            - `file_id: string`

            - `type: "container_upload"`

              - `"container_upload"`

        - `context_management: BetaContextManagementResponse | null`

          Context management response.

          Information about context management strategies applied during the request.

          - `applied_edits: Array<BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse>`

            List of context management edits that were applied.

            - `BetaClearToolUses20250919EditResponse`

              - `cleared_input_tokens: number`

                Number of input tokens cleared by this edit.

              - `cleared_tool_uses: number`

                Number of tool uses that were cleared.

              - `type: "clear_tool_uses_20250919"`

                The type of context management edit applied.

                - `"clear_tool_uses_20250919"`

            - `BetaClearThinking20251015EditResponse`

              - `cleared_input_tokens: number`

                Number of input tokens cleared by this edit.

              - `cleared_thinking_turns: number`

                Number of thinking turns that were cleared.

              - `type: "clear_thinking_20251015"`

                The type of context management edit applied.

                - `"clear_thinking_20251015"`

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

        - `role: "assistant"`

          Conversational role of the generated message.

          This will always be `"assistant"`.

          - `"assistant"`

        - `stop_reason: BetaStopReason | null`

          The reason that we stopped.

          This may be one the following values:

          * `"end_turn"`: the model reached a natural stopping point
          * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
          * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
          * `"tool_use"`: the model invoked one or more tools
          * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
          * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

          In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

          - `"end_turn"`

          - `"max_tokens"`

          - `"stop_sequence"`

          - `"tool_use"`

          - `"pause_turn"`

          - `"refusal"`

          - `"model_context_window_exceeded"`

        - `stop_sequence: string | null`

          Which custom stop sequence was generated, if any.

          This value will be a non-null string if one of your custom stop sequences was generated.

        - `type: "message"`

          Object type.

          For Messages, this is always `"message"`.

          - `"message"`

        - `usage: BetaUsage`

          Billing and rate-limit usage.

          Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

          Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

          For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

          Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

          - `cache_creation: BetaCacheCreation | null`

            Breakdown of cached tokens by TTL

            - `ephemeral_1h_input_tokens: number`

              The number of input tokens used to create the 1 hour cache entry.

            - `ephemeral_5m_input_tokens: number`

              The number of input tokens used to create the 5 minute cache entry.

          - `cache_creation_input_tokens: number | null`

            The number of input tokens used to create the cache entry.

          - `cache_read_input_tokens: number | null`

            The number of input tokens read from the cache.

          - `input_tokens: number`

            The number of input tokens which were used.

          - `output_tokens: number`

            The number of output tokens which were used.

          - `server_tool_use: BetaServerToolUsage | null`

            The number of server tool requests.

            - `web_fetch_requests: number`

              The number of web fetch tool requests.

            - `web_search_requests: number`

              The number of web search tool requests.

          - `service_tier: "standard" | "priority" | "batch" | null`

            If the request used the priority, standard, or batch tier.

            - `"standard"`

            - `"priority"`

            - `"batch"`

      - `type: "succeeded"`

        - `"succeeded"`

    - `BetaMessageBatchErroredResult`

      - `error: BetaErrorResponse`

        - `error: BetaError`

          - `BetaInvalidRequestError`

            - `message: string`

            - `type: "invalid_request_error"`

              - `"invalid_request_error"`

          - `BetaAuthenticationError`

            - `message: string`

            - `type: "authentication_error"`

              - `"authentication_error"`

          - `BetaBillingError`

            - `message: string`

            - `type: "billing_error"`

              - `"billing_error"`

          - `BetaPermissionError`

            - `message: string`

            - `type: "permission_error"`

              - `"permission_error"`

          - `BetaNotFoundError`

            - `message: string`

            - `type: "not_found_error"`

              - `"not_found_error"`

          - `BetaRateLimitError`

            - `message: string`

            - `type: "rate_limit_error"`

              - `"rate_limit_error"`

          - `BetaGatewayTimeoutError`

            - `message: string`

            - `type: "timeout_error"`

              - `"timeout_error"`

          - `BetaAPIError`

            - `message: string`

            - `type: "api_error"`

              - `"api_error"`

          - `BetaOverloadedError`

            - `message: string`

            - `type: "overloaded_error"`

              - `"overloaded_error"`

        - `request_id: string | null`

        - `type: "error"`

          - `"error"`

      - `type: "errored"`

        - `"errored"`

    - `BetaMessageBatchCanceledResult`

      - `type: "canceled"`

        - `"canceled"`

    - `BetaMessageBatchExpiredResult`

      - `type: "expired"`

        - `"expired"`

### Beta Message Batch Request Counts

- `BetaMessageBatchRequestCounts`

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

### Beta Message Batch Result

- `BetaMessageBatchResult = BetaMessageBatchSucceededResult | BetaMessageBatchErroredResult | BetaMessageBatchCanceledResult | BetaMessageBatchExpiredResult`

  Processing result for this request.

  Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

  - `BetaMessageBatchSucceededResult`

    - `message: BetaMessage`

      - `id: string`

        Unique object identifier.

        The format and length of IDs may change over time.

      - `container: BetaContainer | null`

        Information about the container used in the request (for the code execution tool)

        - `id: string`

          Identifier for the container used in this request

        - `expires_at: string`

          The time at which the container will expire.

        - `skills: Array<BetaSkill> | null`

          Skills loaded in the container

          - `skill_id: string`

            Skill ID

          - `type: "anthropic" | "custom"`

            Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

            - `"anthropic"`

            - `"custom"`

          - `version: string`

            Skill version or 'latest' for most recent version

      - `content: Array<BetaContentBlock>`

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

        - `BetaTextBlock`

          - `citations: Array<BetaTextCitation> | null`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `BetaCitationCharLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_char_index: number`

              - `file_id: string | null`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `BetaCitationPageLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_page_number: number`

              - `file_id: string | null`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `BetaCitationContentBlockLocation`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string | null`

              - `end_block_index: number`

              - `file_id: string | null`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `BetaCitationsWebSearchResultLocation`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string | null`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `BetaCitationSearchResultLocation`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string | null`

              - `type: "search_result_location"`

                - `"search_result_location"`

          - `text: string`

          - `type: "text"`

            - `"text"`

        - `BetaThinkingBlock`

          - `signature: string`

          - `thinking: string`

          - `type: "thinking"`

            - `"thinking"`

        - `BetaRedactedThinkingBlock`

          - `data: string`

          - `type: "redacted_thinking"`

            - `"redacted_thinking"`

        - `BetaToolUseBlock`

          - `id: string`

          - `input: Record<string, unknown>`

          - `name: string`

          - `type: "tool_use"`

            - `"tool_use"`

          - `caller?: BetaDirectCaller | BetaServerToolCaller`

            Tool invocation directly from the model.

            - `BetaDirectCaller`

              Tool invocation directly from the model.

              - `type: "direct"`

                - `"direct"`

            - `BetaServerToolCaller`

              Tool invocation generated by a server-side tool.

              - `tool_id: string`

              - `type: "code_execution_20250825"`

                - `"code_execution_20250825"`

        - `BetaServerToolUseBlock`

          - `id: string`

          - `caller: BetaDirectCaller | BetaServerToolCaller`

            Tool invocation directly from the model.

            - `BetaDirectCaller`

              Tool invocation directly from the model.

              - `type: "direct"`

                - `"direct"`

            - `BetaServerToolCaller`

              Tool invocation generated by a server-side tool.

              - `tool_id: string`

              - `type: "code_execution_20250825"`

                - `"code_execution_20250825"`

          - `input: Record<string, unknown>`

          - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

            - `"web_search"`

            - `"web_fetch"`

            - `"code_execution"`

            - `"bash_code_execution"`

            - `"text_editor_code_execution"`

            - `"tool_search_tool_regex"`

            - `"tool_search_tool_bm25"`

          - `type: "server_tool_use"`

            - `"server_tool_use"`

        - `BetaWebSearchToolResultBlock`

          - `content: BetaWebSearchToolResultBlockContent`

            - `BetaWebSearchToolResultError`

              - `error_code: BetaWebSearchToolResultErrorCode`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"max_uses_exceeded"`

                - `"too_many_requests"`

                - `"query_too_long"`

              - `type: "web_search_tool_result_error"`

                - `"web_search_tool_result_error"`

            - `Array<BetaWebSearchResultBlock>`

              - `encrypted_content: string`

              - `page_age: string | null`

              - `title: string`

              - `type: "web_search_result"`

                - `"web_search_result"`

              - `url: string`

          - `tool_use_id: string`

          - `type: "web_search_tool_result"`

            - `"web_search_tool_result"`

        - `BetaWebFetchToolResultBlock`

          - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

            - `BetaWebFetchToolResultErrorBlock`

              - `error_code: BetaWebFetchToolResultErrorCode`

                - `"invalid_tool_input"`

                - `"url_too_long"`

                - `"url_not_allowed"`

                - `"url_not_accessible"`

                - `"unsupported_content_type"`

                - `"too_many_requests"`

                - `"max_uses_exceeded"`

                - `"unavailable"`

              - `type: "web_fetch_tool_result_error"`

                - `"web_fetch_tool_result_error"`

            - `BetaWebFetchBlock`

              - `content: BetaDocumentBlock`

                - `citations: BetaCitationConfig | null`

                  Citation configuration for the document

                  - `enabled: boolean`

                - `source: BetaBase64PDFSource | BetaPlainTextSource`

                  - `BetaBase64PDFSource`

                    - `data: string`

                    - `media_type: "application/pdf"`

                      - `"application/pdf"`

                    - `type: "base64"`

                      - `"base64"`

                  - `BetaPlainTextSource`

                    - `data: string`

                    - `media_type: "text/plain"`

                      - `"text/plain"`

                    - `type: "text"`

                      - `"text"`

                - `title: string | null`

                  The title of the document

                - `type: "document"`

                  - `"document"`

              - `retrieved_at: string | null`

                ISO 8601 timestamp when the content was retrieved

              - `type: "web_fetch_result"`

                - `"web_fetch_result"`

              - `url: string`

                Fetched content URL

          - `tool_use_id: string`

          - `type: "web_fetch_tool_result"`

            - `"web_fetch_tool_result"`

        - `BetaCodeExecutionToolResultBlock`

          - `content: BetaCodeExecutionToolResultBlockContent`

            - `BetaCodeExecutionToolResultError`

              - `error_code: BetaCodeExecutionToolResultErrorCode`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"too_many_requests"`

                - `"execution_time_exceeded"`

              - `type: "code_execution_tool_result_error"`

                - `"code_execution_tool_result_error"`

            - `BetaCodeExecutionResultBlock`

              - `content: Array<BetaCodeExecutionOutputBlock>`

                - `file_id: string`

                - `type: "code_execution_output"`

                  - `"code_execution_output"`

              - `return_code: number`

              - `stderr: string`

              - `stdout: string`

              - `type: "code_execution_result"`

                - `"code_execution_result"`

          - `tool_use_id: string`

          - `type: "code_execution_tool_result"`

            - `"code_execution_tool_result"`

        - `BetaBashCodeExecutionToolResultBlock`

          - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

            - `BetaBashCodeExecutionToolResultError`

              - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"too_many_requests"`

                - `"execution_time_exceeded"`

                - `"output_file_too_large"`

              - `type: "bash_code_execution_tool_result_error"`

                - `"bash_code_execution_tool_result_error"`

            - `BetaBashCodeExecutionResultBlock`

              - `content: Array<BetaBashCodeExecutionOutputBlock>`

                - `file_id: string`

                - `type: "bash_code_execution_output"`

                  - `"bash_code_execution_output"`

              - `return_code: number`

              - `stderr: string`

              - `stdout: string`

              - `type: "bash_code_execution_result"`

                - `"bash_code_execution_result"`

          - `tool_use_id: string`

          - `type: "bash_code_execution_tool_result"`

            - `"bash_code_execution_tool_result"`

        - `BetaTextEditorCodeExecutionToolResultBlock`

          - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

            - `BetaTextEditorCodeExecutionToolResultError`

              - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"too_many_requests"`

                - `"execution_time_exceeded"`

                - `"file_not_found"`

              - `error_message: string | null`

              - `type: "text_editor_code_execution_tool_result_error"`

                - `"text_editor_code_execution_tool_result_error"`

            - `BetaTextEditorCodeExecutionViewResultBlock`

              - `content: string`

              - `file_type: "text" | "image" | "pdf"`

                - `"text"`

                - `"image"`

                - `"pdf"`

              - `num_lines: number | null`

              - `start_line: number | null`

              - `total_lines: number | null`

              - `type: "text_editor_code_execution_view_result"`

                - `"text_editor_code_execution_view_result"`

            - `BetaTextEditorCodeExecutionCreateResultBlock`

              - `is_file_update: boolean`

              - `type: "text_editor_code_execution_create_result"`

                - `"text_editor_code_execution_create_result"`

            - `BetaTextEditorCodeExecutionStrReplaceResultBlock`

              - `lines: Array<string> | null`

              - `new_lines: number | null`

              - `new_start: number | null`

              - `old_lines: number | null`

              - `old_start: number | null`

              - `type: "text_editor_code_execution_str_replace_result"`

                - `"text_editor_code_execution_str_replace_result"`

          - `tool_use_id: string`

          - `type: "text_editor_code_execution_tool_result"`

            - `"text_editor_code_execution_tool_result"`

        - `BetaToolSearchToolResultBlock`

          - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

            - `BetaToolSearchToolResultError`

              - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"too_many_requests"`

                - `"execution_time_exceeded"`

              - `error_message: string | null`

              - `type: "tool_search_tool_result_error"`

                - `"tool_search_tool_result_error"`

            - `BetaToolSearchToolSearchResultBlock`

              - `tool_references: Array<BetaToolReferenceBlock>`

                - `tool_name: string`

                - `type: "tool_reference"`

                  - `"tool_reference"`

              - `type: "tool_search_tool_search_result"`

                - `"tool_search_tool_search_result"`

          - `tool_use_id: string`

          - `type: "tool_search_tool_result"`

            - `"tool_search_tool_result"`

        - `BetaMCPToolUseBlock`

          - `id: string`

          - `input: Record<string, unknown>`

          - `name: string`

            The name of the MCP tool

          - `server_name: string`

            The name of the MCP server

          - `type: "mcp_tool_use"`

            - `"mcp_tool_use"`

        - `BetaMCPToolResultBlock`

          - `content: string | Array<BetaTextBlock>`

            - `string`

            - `Array<BetaTextBlock>`

              - `citations: Array<BetaTextCitation> | null`

                Citations supporting the text block.

                The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

                - `BetaCitationCharLocation`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_char_index: number`

                  - `file_id: string | null`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `BetaCitationPageLocation`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_page_number: number`

                  - `file_id: string | null`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `BetaCitationContentBlockLocation`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string | null`

                  - `end_block_index: number`

                  - `file_id: string | null`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `BetaCitationsWebSearchResultLocation`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string | null`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `BetaCitationSearchResultLocation`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string | null`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

              - `text: string`

              - `type: "text"`

                - `"text"`

          - `is_error: boolean`

          - `tool_use_id: string`

          - `type: "mcp_tool_result"`

            - `"mcp_tool_result"`

        - `BetaContainerUploadBlock`

          Response model for a file uploaded to the container.

          - `file_id: string`

          - `type: "container_upload"`

            - `"container_upload"`

      - `context_management: BetaContextManagementResponse | null`

        Context management response.

        Information about context management strategies applied during the request.

        - `applied_edits: Array<BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse>`

          List of context management edits that were applied.

          - `BetaClearToolUses20250919EditResponse`

            - `cleared_input_tokens: number`

              Number of input tokens cleared by this edit.

            - `cleared_tool_uses: number`

              Number of tool uses that were cleared.

            - `type: "clear_tool_uses_20250919"`

              The type of context management edit applied.

              - `"clear_tool_uses_20250919"`

          - `BetaClearThinking20251015EditResponse`

            - `cleared_input_tokens: number`

              Number of input tokens cleared by this edit.

            - `cleared_thinking_turns: number`

              Number of thinking turns that were cleared.

            - `type: "clear_thinking_20251015"`

              The type of context management edit applied.

              - `"clear_thinking_20251015"`

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

      - `role: "assistant"`

        Conversational role of the generated message.

        This will always be `"assistant"`.

        - `"assistant"`

      - `stop_reason: BetaStopReason | null`

        The reason that we stopped.

        This may be one the following values:

        * `"end_turn"`: the model reached a natural stopping point
        * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
        * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
        * `"tool_use"`: the model invoked one or more tools
        * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
        * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

        In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

        - `"end_turn"`

        - `"max_tokens"`

        - `"stop_sequence"`

        - `"tool_use"`

        - `"pause_turn"`

        - `"refusal"`

        - `"model_context_window_exceeded"`

      - `stop_sequence: string | null`

        Which custom stop sequence was generated, if any.

        This value will be a non-null string if one of your custom stop sequences was generated.

      - `type: "message"`

        Object type.

        For Messages, this is always `"message"`.

        - `"message"`

      - `usage: BetaUsage`

        Billing and rate-limit usage.

        Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

        Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

        For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

        Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

        - `cache_creation: BetaCacheCreation | null`

          Breakdown of cached tokens by TTL

          - `ephemeral_1h_input_tokens: number`

            The number of input tokens used to create the 1 hour cache entry.

          - `ephemeral_5m_input_tokens: number`

            The number of input tokens used to create the 5 minute cache entry.

        - `cache_creation_input_tokens: number | null`

          The number of input tokens used to create the cache entry.

        - `cache_read_input_tokens: number | null`

          The number of input tokens read from the cache.

        - `input_tokens: number`

          The number of input tokens which were used.

        - `output_tokens: number`

          The number of output tokens which were used.

        - `server_tool_use: BetaServerToolUsage | null`

          The number of server tool requests.

          - `web_fetch_requests: number`

            The number of web fetch tool requests.

          - `web_search_requests: number`

            The number of web search tool requests.

        - `service_tier: "standard" | "priority" | "batch" | null`

          If the request used the priority, standard, or batch tier.

          - `"standard"`

          - `"priority"`

          - `"batch"`

    - `type: "succeeded"`

      - `"succeeded"`

  - `BetaMessageBatchErroredResult`

    - `error: BetaErrorResponse`

      - `error: BetaError`

        - `BetaInvalidRequestError`

          - `message: string`

          - `type: "invalid_request_error"`

            - `"invalid_request_error"`

        - `BetaAuthenticationError`

          - `message: string`

          - `type: "authentication_error"`

            - `"authentication_error"`

        - `BetaBillingError`

          - `message: string`

          - `type: "billing_error"`

            - `"billing_error"`

        - `BetaPermissionError`

          - `message: string`

          - `type: "permission_error"`

            - `"permission_error"`

        - `BetaNotFoundError`

          - `message: string`

          - `type: "not_found_error"`

            - `"not_found_error"`

        - `BetaRateLimitError`

          - `message: string`

          - `type: "rate_limit_error"`

            - `"rate_limit_error"`

        - `BetaGatewayTimeoutError`

          - `message: string`

          - `type: "timeout_error"`

            - `"timeout_error"`

        - `BetaAPIError`

          - `message: string`

          - `type: "api_error"`

            - `"api_error"`

        - `BetaOverloadedError`

          - `message: string`

          - `type: "overloaded_error"`

            - `"overloaded_error"`

      - `request_id: string | null`

      - `type: "error"`

        - `"error"`

    - `type: "errored"`

      - `"errored"`

  - `BetaMessageBatchCanceledResult`

    - `type: "canceled"`

      - `"canceled"`

  - `BetaMessageBatchExpiredResult`

    - `type: "expired"`

      - `"expired"`

### Beta Message Batch Succeeded Result

- `BetaMessageBatchSucceededResult`

  - `message: BetaMessage`

    - `id: string`

      Unique object identifier.

      The format and length of IDs may change over time.

    - `container: BetaContainer | null`

      Information about the container used in the request (for the code execution tool)

      - `id: string`

        Identifier for the container used in this request

      - `expires_at: string`

        The time at which the container will expire.

      - `skills: Array<BetaSkill> | null`

        Skills loaded in the container

        - `skill_id: string`

          Skill ID

        - `type: "anthropic" | "custom"`

          Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

          - `"anthropic"`

          - `"custom"`

        - `version: string`

          Skill version or 'latest' for most recent version

    - `content: Array<BetaContentBlock>`

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

      - `BetaTextBlock`

        - `citations: Array<BetaTextCitation> | null`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `BetaCitationCharLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_char_index: number`

            - `file_id: string | null`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `BetaCitationPageLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_page_number: number`

            - `file_id: string | null`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `BetaCitationContentBlockLocation`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string | null`

            - `end_block_index: number`

            - `file_id: string | null`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `BetaCitationsWebSearchResultLocation`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string | null`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `BetaCitationSearchResultLocation`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string | null`

            - `type: "search_result_location"`

              - `"search_result_location"`

        - `text: string`

        - `type: "text"`

          - `"text"`

      - `BetaThinkingBlock`

        - `signature: string`

        - `thinking: string`

        - `type: "thinking"`

          - `"thinking"`

      - `BetaRedactedThinkingBlock`

        - `data: string`

        - `type: "redacted_thinking"`

          - `"redacted_thinking"`

      - `BetaToolUseBlock`

        - `id: string`

        - `input: Record<string, unknown>`

        - `name: string`

        - `type: "tool_use"`

          - `"tool_use"`

        - `caller?: BetaDirectCaller | BetaServerToolCaller`

          Tool invocation directly from the model.

          - `BetaDirectCaller`

            Tool invocation directly from the model.

            - `type: "direct"`

              - `"direct"`

          - `BetaServerToolCaller`

            Tool invocation generated by a server-side tool.

            - `tool_id: string`

            - `type: "code_execution_20250825"`

              - `"code_execution_20250825"`

      - `BetaServerToolUseBlock`

        - `id: string`

        - `caller: BetaDirectCaller | BetaServerToolCaller`

          Tool invocation directly from the model.

          - `BetaDirectCaller`

            Tool invocation directly from the model.

            - `type: "direct"`

              - `"direct"`

          - `BetaServerToolCaller`

            Tool invocation generated by a server-side tool.

            - `tool_id: string`

            - `type: "code_execution_20250825"`

              - `"code_execution_20250825"`

        - `input: Record<string, unknown>`

        - `name: "web_search" | "web_fetch" | "code_execution" | 4 more`

          - `"web_search"`

          - `"web_fetch"`

          - `"code_execution"`

          - `"bash_code_execution"`

          - `"text_editor_code_execution"`

          - `"tool_search_tool_regex"`

          - `"tool_search_tool_bm25"`

        - `type: "server_tool_use"`

          - `"server_tool_use"`

      - `BetaWebSearchToolResultBlock`

        - `content: BetaWebSearchToolResultBlockContent`

          - `BetaWebSearchToolResultError`

            - `error_code: BetaWebSearchToolResultErrorCode`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"max_uses_exceeded"`

              - `"too_many_requests"`

              - `"query_too_long"`

            - `type: "web_search_tool_result_error"`

              - `"web_search_tool_result_error"`

          - `Array<BetaWebSearchResultBlock>`

            - `encrypted_content: string`

            - `page_age: string | null`

            - `title: string`

            - `type: "web_search_result"`

              - `"web_search_result"`

            - `url: string`

        - `tool_use_id: string`

        - `type: "web_search_tool_result"`

          - `"web_search_tool_result"`

      - `BetaWebFetchToolResultBlock`

        - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

          - `BetaWebFetchToolResultErrorBlock`

            - `error_code: BetaWebFetchToolResultErrorCode`

              - `"invalid_tool_input"`

              - `"url_too_long"`

              - `"url_not_allowed"`

              - `"url_not_accessible"`

              - `"unsupported_content_type"`

              - `"too_many_requests"`

              - `"max_uses_exceeded"`

              - `"unavailable"`

            - `type: "web_fetch_tool_result_error"`

              - `"web_fetch_tool_result_error"`

          - `BetaWebFetchBlock`

            - `content: BetaDocumentBlock`

              - `citations: BetaCitationConfig | null`

                Citation configuration for the document

                - `enabled: boolean`

              - `source: BetaBase64PDFSource | BetaPlainTextSource`

                - `BetaBase64PDFSource`

                  - `data: string`

                  - `media_type: "application/pdf"`

                    - `"application/pdf"`

                  - `type: "base64"`

                    - `"base64"`

                - `BetaPlainTextSource`

                  - `data: string`

                  - `media_type: "text/plain"`

                    - `"text/plain"`

                  - `type: "text"`

                    - `"text"`

              - `title: string | null`

                The title of the document

              - `type: "document"`

                - `"document"`

            - `retrieved_at: string | null`

              ISO 8601 timestamp when the content was retrieved

            - `type: "web_fetch_result"`

              - `"web_fetch_result"`

            - `url: string`

              Fetched content URL

        - `tool_use_id: string`

        - `type: "web_fetch_tool_result"`

          - `"web_fetch_tool_result"`

      - `BetaCodeExecutionToolResultBlock`

        - `content: BetaCodeExecutionToolResultBlockContent`

          - `BetaCodeExecutionToolResultError`

            - `error_code: BetaCodeExecutionToolResultErrorCode`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

            - `type: "code_execution_tool_result_error"`

              - `"code_execution_tool_result_error"`

          - `BetaCodeExecutionResultBlock`

            - `content: Array<BetaCodeExecutionOutputBlock>`

              - `file_id: string`

              - `type: "code_execution_output"`

                - `"code_execution_output"`

            - `return_code: number`

            - `stderr: string`

            - `stdout: string`

            - `type: "code_execution_result"`

              - `"code_execution_result"`

        - `tool_use_id: string`

        - `type: "code_execution_tool_result"`

          - `"code_execution_tool_result"`

      - `BetaBashCodeExecutionToolResultBlock`

        - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

          - `BetaBashCodeExecutionToolResultError`

            - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

              - `"output_file_too_large"`

            - `type: "bash_code_execution_tool_result_error"`

              - `"bash_code_execution_tool_result_error"`

          - `BetaBashCodeExecutionResultBlock`

            - `content: Array<BetaBashCodeExecutionOutputBlock>`

              - `file_id: string`

              - `type: "bash_code_execution_output"`

                - `"bash_code_execution_output"`

            - `return_code: number`

            - `stderr: string`

            - `stdout: string`

            - `type: "bash_code_execution_result"`

              - `"bash_code_execution_result"`

        - `tool_use_id: string`

        - `type: "bash_code_execution_tool_result"`

          - `"bash_code_execution_tool_result"`

      - `BetaTextEditorCodeExecutionToolResultBlock`

        - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

          - `BetaTextEditorCodeExecutionToolResultError`

            - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | 2 more`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

              - `"file_not_found"`

            - `error_message: string | null`

            - `type: "text_editor_code_execution_tool_result_error"`

              - `"text_editor_code_execution_tool_result_error"`

          - `BetaTextEditorCodeExecutionViewResultBlock`

            - `content: string`

            - `file_type: "text" | "image" | "pdf"`

              - `"text"`

              - `"image"`

              - `"pdf"`

            - `num_lines: number | null`

            - `start_line: number | null`

            - `total_lines: number | null`

            - `type: "text_editor_code_execution_view_result"`

              - `"text_editor_code_execution_view_result"`

          - `BetaTextEditorCodeExecutionCreateResultBlock`

            - `is_file_update: boolean`

            - `type: "text_editor_code_execution_create_result"`

              - `"text_editor_code_execution_create_result"`

          - `BetaTextEditorCodeExecutionStrReplaceResultBlock`

            - `lines: Array<string> | null`

            - `new_lines: number | null`

            - `new_start: number | null`

            - `old_lines: number | null`

            - `old_start: number | null`

            - `type: "text_editor_code_execution_str_replace_result"`

              - `"text_editor_code_execution_str_replace_result"`

        - `tool_use_id: string`

        - `type: "text_editor_code_execution_tool_result"`

          - `"text_editor_code_execution_tool_result"`

      - `BetaToolSearchToolResultBlock`

        - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

          - `BetaToolSearchToolResultError`

            - `error_code: "invalid_tool_input" | "unavailable" | "too_many_requests" | "execution_time_exceeded"`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

            - `error_message: string | null`

            - `type: "tool_search_tool_result_error"`

              - `"tool_search_tool_result_error"`

          - `BetaToolSearchToolSearchResultBlock`

            - `tool_references: Array<BetaToolReferenceBlock>`

              - `tool_name: string`

              - `type: "tool_reference"`

                - `"tool_reference"`

            - `type: "tool_search_tool_search_result"`

              - `"tool_search_tool_search_result"`

        - `tool_use_id: string`

        - `type: "tool_search_tool_result"`

          - `"tool_search_tool_result"`

      - `BetaMCPToolUseBlock`

        - `id: string`

        - `input: Record<string, unknown>`

        - `name: string`

          The name of the MCP tool

        - `server_name: string`

          The name of the MCP server

        - `type: "mcp_tool_use"`

          - `"mcp_tool_use"`

      - `BetaMCPToolResultBlock`

        - `content: string | Array<BetaTextBlock>`

          - `string`

          - `Array<BetaTextBlock>`

            - `citations: Array<BetaTextCitation> | null`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `BetaCitationCharLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_char_index: number`

                - `file_id: string | null`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `BetaCitationPageLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_page_number: number`

                - `file_id: string | null`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `BetaCitationContentBlockLocation`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string | null`

                - `end_block_index: number`

                - `file_id: string | null`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `BetaCitationsWebSearchResultLocation`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string | null`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `BetaCitationSearchResultLocation`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string | null`

                - `type: "search_result_location"`

                  - `"search_result_location"`

            - `text: string`

            - `type: "text"`

              - `"text"`

        - `is_error: boolean`

        - `tool_use_id: string`

        - `type: "mcp_tool_result"`

          - `"mcp_tool_result"`

      - `BetaContainerUploadBlock`

        Response model for a file uploaded to the container.

        - `file_id: string`

        - `type: "container_upload"`

          - `"container_upload"`

    - `context_management: BetaContextManagementResponse | null`

      Context management response.

      Information about context management strategies applied during the request.

      - `applied_edits: Array<BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse>`

        List of context management edits that were applied.

        - `BetaClearToolUses20250919EditResponse`

          - `cleared_input_tokens: number`

            Number of input tokens cleared by this edit.

          - `cleared_tool_uses: number`

            Number of tool uses that were cleared.

          - `type: "clear_tool_uses_20250919"`

            The type of context management edit applied.

            - `"clear_tool_uses_20250919"`

        - `BetaClearThinking20251015EditResponse`

          - `cleared_input_tokens: number`

            Number of input tokens cleared by this edit.

          - `cleared_thinking_turns: number`

            Number of thinking turns that were cleared.

          - `type: "clear_thinking_20251015"`

            The type of context management edit applied.

            - `"clear_thinking_20251015"`

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

    - `role: "assistant"`

      Conversational role of the generated message.

      This will always be `"assistant"`.

      - `"assistant"`

    - `stop_reason: BetaStopReason | null`

      The reason that we stopped.

      This may be one the following values:

      * `"end_turn"`: the model reached a natural stopping point
      * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
      * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
      * `"tool_use"`: the model invoked one or more tools
      * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
      * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

      In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

      - `"end_turn"`

      - `"max_tokens"`

      - `"stop_sequence"`

      - `"tool_use"`

      - `"pause_turn"`

      - `"refusal"`

      - `"model_context_window_exceeded"`

    - `stop_sequence: string | null`

      Which custom stop sequence was generated, if any.

      This value will be a non-null string if one of your custom stop sequences was generated.

    - `type: "message"`

      Object type.

      For Messages, this is always `"message"`.

      - `"message"`

    - `usage: BetaUsage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cache_creation: BetaCacheCreation | null`

        Breakdown of cached tokens by TTL

        - `ephemeral_1h_input_tokens: number`

          The number of input tokens used to create the 1 hour cache entry.

        - `ephemeral_5m_input_tokens: number`

          The number of input tokens used to create the 5 minute cache entry.

      - `cache_creation_input_tokens: number | null`

        The number of input tokens used to create the cache entry.

      - `cache_read_input_tokens: number | null`

        The number of input tokens read from the cache.

      - `input_tokens: number`

        The number of input tokens which were used.

      - `output_tokens: number`

        The number of output tokens which were used.

      - `server_tool_use: BetaServerToolUsage | null`

        The number of server tool requests.

        - `web_fetch_requests: number`

          The number of web fetch tool requests.

        - `web_search_requests: number`

          The number of web search tool requests.

      - `service_tier: "standard" | "priority" | "batch" | null`

        If the request used the priority, standard, or batch tier.

        - `"standard"`

        - `"priority"`

        - `"batch"`

  - `type: "succeeded"`

    - `"succeeded"`
