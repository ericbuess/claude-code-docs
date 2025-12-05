## Create

`beta.messages.batches.create(**kwargs) -> BetaMessageBatch`

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

  - `params: { max_tokens, messages, model, 16 more}`

    Messages API creation parameters for the individual request.

    See the [Messages API reference](https://docs.claude.com/en/api/messages) for full documentation on available parameters.

    - `max_tokens: Integer`

      The maximum number of tokens to generate before stopping.

      Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

      Different models have different maximum values for this parameter.  See [models](https://docs.claude.com/en/docs/models-overview) for details.

    - `messages: Array[BetaMessageParam]`

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

      - `content: String | Array[BetaContentBlockParam]`

        - `String`

        - `Array[BetaContentBlockParam]`

          - `class BetaTextBlockParam`

            - `text: String`

            - `type: :text`

              - `:text`

            - `cache_control: BetaCacheControlEphemeral`

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

            - `citations: Array[BetaTextCitationParam]`

              - `class BetaCitationCharLocationParam`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_char_index: Integer`

                - `start_char_index: Integer`

                - `type: :char_location`

                  - `:char_location`

              - `class BetaCitationPageLocationParam`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_page_number: Integer`

                - `start_page_number: Integer`

                - `type: :page_location`

                  - `:page_location`

              - `class BetaCitationContentBlockLocationParam`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_block_index: Integer`

                - `start_block_index: Integer`

                - `type: :content_block_location`

                  - `:content_block_location`

              - `class BetaCitationWebSearchResultLocationParam`

                - `cited_text: String`

                - `encrypted_index: String`

                - `title: String`

                - `type: :web_search_result_location`

                  - `:web_search_result_location`

                - `url: String`

              - `class BetaCitationSearchResultLocationParam`

                - `cited_text: String`

                - `end_block_index: Integer`

                - `search_result_index: Integer`

                - `source: String`

                - `start_block_index: Integer`

                - `title: String`

                - `type: :search_result_location`

                  - `:search_result_location`

          - `class BetaImageBlockParam`

            - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

              - `class BetaBase64ImageSource`

                - `data: String`

                - `media_type: :"image/jpeg" | :"image/png" | :"image/gif" | :"image/webp"`

                  - `:"image/jpeg"`

                  - `:"image/png"`

                  - `:"image/gif"`

                  - `:"image/webp"`

                - `type: :base64`

                  - `:base64`

              - `class BetaURLImageSource`

                - `type: :url`

                  - `:url`

                - `url: String`

              - `class BetaFileImageSource`

                - `file_id: String`

                - `type: :file`

                  - `:file`

            - `type: :image`

              - `:image`

            - `cache_control: BetaCacheControlEphemeral`

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

          - `class BetaRequestDocumentBlock`

            - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

              - `class BetaBase64PDFSource`

                - `data: String`

                - `media_type: :"application/pdf"`

                  - `:"application/pdf"`

                - `type: :base64`

                  - `:base64`

              - `class BetaPlainTextSource`

                - `data: String`

                - `media_type: :"text/plain"`

                  - `:"text/plain"`

                - `type: :text`

                  - `:text`

              - `class BetaContentBlockSource`

                - `content: String | Array[BetaContentBlockSourceContent]`

                  - `String`

                  - `Array[BetaContentBlockSourceContent]`

                    - `class BetaTextBlockParam`

                      - `text: String`

                      - `type: :text`

                        - `:text`

                      - `cache_control: BetaCacheControlEphemeral`

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

                      - `citations: Array[BetaTextCitationParam]`

                        - `class BetaCitationCharLocationParam`

                          - `cited_text: String`

                          - `document_index: Integer`

                          - `document_title: String`

                          - `end_char_index: Integer`

                          - `start_char_index: Integer`

                          - `type: :char_location`

                            - `:char_location`

                        - `class BetaCitationPageLocationParam`

                          - `cited_text: String`

                          - `document_index: Integer`

                          - `document_title: String`

                          - `end_page_number: Integer`

                          - `start_page_number: Integer`

                          - `type: :page_location`

                            - `:page_location`

                        - `class BetaCitationContentBlockLocationParam`

                          - `cited_text: String`

                          - `document_index: Integer`

                          - `document_title: String`

                          - `end_block_index: Integer`

                          - `start_block_index: Integer`

                          - `type: :content_block_location`

                            - `:content_block_location`

                        - `class BetaCitationWebSearchResultLocationParam`

                          - `cited_text: String`

                          - `encrypted_index: String`

                          - `title: String`

                          - `type: :web_search_result_location`

                            - `:web_search_result_location`

                          - `url: String`

                        - `class BetaCitationSearchResultLocationParam`

                          - `cited_text: String`

                          - `end_block_index: Integer`

                          - `search_result_index: Integer`

                          - `source: String`

                          - `start_block_index: Integer`

                          - `title: String`

                          - `type: :search_result_location`

                            - `:search_result_location`

                    - `class BetaImageBlockParam`

                      - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                        - `class BetaBase64ImageSource`

                          - `data: String`

                          - `media_type: :"image/jpeg" | :"image/png" | :"image/gif" | :"image/webp"`

                            - `:"image/jpeg"`

                            - `:"image/png"`

                            - `:"image/gif"`

                            - `:"image/webp"`

                          - `type: :base64`

                            - `:base64`

                        - `class BetaURLImageSource`

                          - `type: :url`

                            - `:url`

                          - `url: String`

                        - `class BetaFileImageSource`

                          - `file_id: String`

                          - `type: :file`

                            - `:file`

                      - `type: :image`

                        - `:image`

                      - `cache_control: BetaCacheControlEphemeral`

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

              - `class BetaURLPDFSource`

                - `type: :url`

                  - `:url`

                - `url: String`

              - `class BetaFileDocumentSource`

                - `file_id: String`

                - `type: :file`

                  - `:file`

            - `type: :document`

              - `:document`

            - `cache_control: BetaCacheControlEphemeral`

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

            - `citations: BetaCitationsConfigParam`

              - `enabled: bool`

            - `context: String`

            - `title: String`

          - `class BetaSearchResultBlockParam`

            - `content: Array[BetaTextBlockParam]`

              - `text: String`

              - `type: :text`

                - `:text`

              - `cache_control: BetaCacheControlEphemeral`

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

              - `citations: Array[BetaTextCitationParam]`

                - `class BetaCitationCharLocationParam`

                  - `cited_text: String`

                  - `document_index: Integer`

                  - `document_title: String`

                  - `end_char_index: Integer`

                  - `start_char_index: Integer`

                  - `type: :char_location`

                    - `:char_location`

                - `class BetaCitationPageLocationParam`

                  - `cited_text: String`

                  - `document_index: Integer`

                  - `document_title: String`

                  - `end_page_number: Integer`

                  - `start_page_number: Integer`

                  - `type: :page_location`

                    - `:page_location`

                - `class BetaCitationContentBlockLocationParam`

                  - `cited_text: String`

                  - `document_index: Integer`

                  - `document_title: String`

                  - `end_block_index: Integer`

                  - `start_block_index: Integer`

                  - `type: :content_block_location`

                    - `:content_block_location`

                - `class BetaCitationWebSearchResultLocationParam`

                  - `cited_text: String`

                  - `encrypted_index: String`

                  - `title: String`

                  - `type: :web_search_result_location`

                    - `:web_search_result_location`

                  - `url: String`

                - `class BetaCitationSearchResultLocationParam`

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

            - `cache_control: BetaCacheControlEphemeral`

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

            - `citations: BetaCitationsConfigParam`

              - `enabled: bool`

          - `class BetaThinkingBlockParam`

            - `signature: String`

            - `thinking: String`

            - `type: :thinking`

              - `:thinking`

          - `class BetaRedactedThinkingBlockParam`

            - `data: String`

            - `type: :redacted_thinking`

              - `:redacted_thinking`

          - `class BetaToolUseBlockParam`

            - `id: String`

            - `input: Hash[Symbol, untyped]`

            - `name: String`

            - `type: :tool_use`

              - `:tool_use`

            - `cache_control: BetaCacheControlEphemeral`

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

            - `caller_: BetaDirectCaller | BetaServerToolCaller`

              Tool invocation directly from the model.

              - `class BetaDirectCaller`

                Tool invocation directly from the model.

                - `type: :direct`

                  - `:direct`

              - `class BetaServerToolCaller`

                Tool invocation generated by a server-side tool.

                - `tool_id: String`

                - `type: :code_execution_20250825`

                  - `:code_execution_20250825`

          - `class BetaToolResultBlockParam`

            - `tool_use_id: String`

            - `type: :tool_result`

              - `:tool_result`

            - `cache_control: BetaCacheControlEphemeral`

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

            - `content: String | Array[BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more]`

              - `String`

              - `Array[BetaTextBlockParam | BetaImageBlockParam | BetaSearchResultBlockParam | 2 more]`

                - `class BetaTextBlockParam`

                  - `text: String`

                  - `type: :text`

                    - `:text`

                  - `cache_control: BetaCacheControlEphemeral`

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

                  - `citations: Array[BetaTextCitationParam]`

                    - `class BetaCitationCharLocationParam`

                      - `cited_text: String`

                      - `document_index: Integer`

                      - `document_title: String`

                      - `end_char_index: Integer`

                      - `start_char_index: Integer`

                      - `type: :char_location`

                        - `:char_location`

                    - `class BetaCitationPageLocationParam`

                      - `cited_text: String`

                      - `document_index: Integer`

                      - `document_title: String`

                      - `end_page_number: Integer`

                      - `start_page_number: Integer`

                      - `type: :page_location`

                        - `:page_location`

                    - `class BetaCitationContentBlockLocationParam`

                      - `cited_text: String`

                      - `document_index: Integer`

                      - `document_title: String`

                      - `end_block_index: Integer`

                      - `start_block_index: Integer`

                      - `type: :content_block_location`

                        - `:content_block_location`

                    - `class BetaCitationWebSearchResultLocationParam`

                      - `cited_text: String`

                      - `encrypted_index: String`

                      - `title: String`

                      - `type: :web_search_result_location`

                        - `:web_search_result_location`

                      - `url: String`

                    - `class BetaCitationSearchResultLocationParam`

                      - `cited_text: String`

                      - `end_block_index: Integer`

                      - `search_result_index: Integer`

                      - `source: String`

                      - `start_block_index: Integer`

                      - `title: String`

                      - `type: :search_result_location`

                        - `:search_result_location`

                - `class BetaImageBlockParam`

                  - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                    - `class BetaBase64ImageSource`

                      - `data: String`

                      - `media_type: :"image/jpeg" | :"image/png" | :"image/gif" | :"image/webp"`

                        - `:"image/jpeg"`

                        - `:"image/png"`

                        - `:"image/gif"`

                        - `:"image/webp"`

                      - `type: :base64`

                        - `:base64`

                    - `class BetaURLImageSource`

                      - `type: :url`

                        - `:url`

                      - `url: String`

                    - `class BetaFileImageSource`

                      - `file_id: String`

                      - `type: :file`

                        - `:file`

                  - `type: :image`

                    - `:image`

                  - `cache_control: BetaCacheControlEphemeral`

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

                - `class BetaSearchResultBlockParam`

                  - `content: Array[BetaTextBlockParam]`

                    - `text: String`

                    - `type: :text`

                      - `:text`

                    - `cache_control: BetaCacheControlEphemeral`

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

                    - `citations: Array[BetaTextCitationParam]`

                      - `class BetaCitationCharLocationParam`

                        - `cited_text: String`

                        - `document_index: Integer`

                        - `document_title: String`

                        - `end_char_index: Integer`

                        - `start_char_index: Integer`

                        - `type: :char_location`

                          - `:char_location`

                      - `class BetaCitationPageLocationParam`

                        - `cited_text: String`

                        - `document_index: Integer`

                        - `document_title: String`

                        - `end_page_number: Integer`

                        - `start_page_number: Integer`

                        - `type: :page_location`

                          - `:page_location`

                      - `class BetaCitationContentBlockLocationParam`

                        - `cited_text: String`

                        - `document_index: Integer`

                        - `document_title: String`

                        - `end_block_index: Integer`

                        - `start_block_index: Integer`

                        - `type: :content_block_location`

                          - `:content_block_location`

                      - `class BetaCitationWebSearchResultLocationParam`

                        - `cited_text: String`

                        - `encrypted_index: String`

                        - `title: String`

                        - `type: :web_search_result_location`

                          - `:web_search_result_location`

                        - `url: String`

                      - `class BetaCitationSearchResultLocationParam`

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

                  - `cache_control: BetaCacheControlEphemeral`

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

                  - `citations: BetaCitationsConfigParam`

                    - `enabled: bool`

                - `class BetaRequestDocumentBlock`

                  - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

                    - `class BetaBase64PDFSource`

                      - `data: String`

                      - `media_type: :"application/pdf"`

                        - `:"application/pdf"`

                      - `type: :base64`

                        - `:base64`

                    - `class BetaPlainTextSource`

                      - `data: String`

                      - `media_type: :"text/plain"`

                        - `:"text/plain"`

                      - `type: :text`

                        - `:text`

                    - `class BetaContentBlockSource`

                      - `content: String | Array[BetaContentBlockSourceContent]`

                        - `String`

                        - `Array[BetaContentBlockSourceContent]`

                          - `class BetaTextBlockParam`

                            - `text: String`

                            - `type: :text`

                              - `:text`

                            - `cache_control: BetaCacheControlEphemeral`

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

                            - `citations: Array[BetaTextCitationParam]`

                              - `class BetaCitationCharLocationParam`

                                - `cited_text: String`

                                - `document_index: Integer`

                                - `document_title: String`

                                - `end_char_index: Integer`

                                - `start_char_index: Integer`

                                - `type: :char_location`

                                  - `:char_location`

                              - `class BetaCitationPageLocationParam`

                                - `cited_text: String`

                                - `document_index: Integer`

                                - `document_title: String`

                                - `end_page_number: Integer`

                                - `start_page_number: Integer`

                                - `type: :page_location`

                                  - `:page_location`

                              - `class BetaCitationContentBlockLocationParam`

                                - `cited_text: String`

                                - `document_index: Integer`

                                - `document_title: String`

                                - `end_block_index: Integer`

                                - `start_block_index: Integer`

                                - `type: :content_block_location`

                                  - `:content_block_location`

                              - `class BetaCitationWebSearchResultLocationParam`

                                - `cited_text: String`

                                - `encrypted_index: String`

                                - `title: String`

                                - `type: :web_search_result_location`

                                  - `:web_search_result_location`

                                - `url: String`

                              - `class BetaCitationSearchResultLocationParam`

                                - `cited_text: String`

                                - `end_block_index: Integer`

                                - `search_result_index: Integer`

                                - `source: String`

                                - `start_block_index: Integer`

                                - `title: String`

                                - `type: :search_result_location`

                                  - `:search_result_location`

                          - `class BetaImageBlockParam`

                            - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                              - `class BetaBase64ImageSource`

                                - `data: String`

                                - `media_type: :"image/jpeg" | :"image/png" | :"image/gif" | :"image/webp"`

                                  - `:"image/jpeg"`

                                  - `:"image/png"`

                                  - `:"image/gif"`

                                  - `:"image/webp"`

                                - `type: :base64`

                                  - `:base64`

                              - `class BetaURLImageSource`

                                - `type: :url`

                                  - `:url`

                                - `url: String`

                              - `class BetaFileImageSource`

                                - `file_id: String`

                                - `type: :file`

                                  - `:file`

                            - `type: :image`

                              - `:image`

                            - `cache_control: BetaCacheControlEphemeral`

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

                    - `class BetaURLPDFSource`

                      - `type: :url`

                        - `:url`

                      - `url: String`

                    - `class BetaFileDocumentSource`

                      - `file_id: String`

                      - `type: :file`

                        - `:file`

                  - `type: :document`

                    - `:document`

                  - `cache_control: BetaCacheControlEphemeral`

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

                  - `citations: BetaCitationsConfigParam`

                    - `enabled: bool`

                  - `context: String`

                  - `title: String`

                - `class BetaToolReferenceBlockParam`

                  Tool reference block that can be included in tool_result content.

                  - `tool_name: String`

                  - `type: :tool_reference`

                    - `:tool_reference`

                  - `cache_control: BetaCacheControlEphemeral`

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

            - `is_error: bool`

          - `class BetaServerToolUseBlockParam`

            - `id: String`

            - `input: Hash[Symbol, untyped]`

            - `name: :web_search | :web_fetch | :code_execution | 4 more`

              - `:web_search`

              - `:web_fetch`

              - `:code_execution`

              - `:bash_code_execution`

              - `:text_editor_code_execution`

              - `:tool_search_tool_regex`

              - `:tool_search_tool_bm25`

            - `type: :server_tool_use`

              - `:server_tool_use`

            - `cache_control: BetaCacheControlEphemeral`

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

            - `caller_: BetaDirectCaller | BetaServerToolCaller`

              Tool invocation directly from the model.

              - `class BetaDirectCaller`

                Tool invocation directly from the model.

                - `type: :direct`

                  - `:direct`

              - `class BetaServerToolCaller`

                Tool invocation generated by a server-side tool.

                - `tool_id: String`

                - `type: :code_execution_20250825`

                  - `:code_execution_20250825`

          - `class BetaWebSearchToolResultBlockParam`

            - `content: BetaWebSearchToolResultBlockParamContent`

              - `Array[BetaWebSearchResultBlockParam]`

                - `encrypted_content: String`

                - `title: String`

                - `type: :web_search_result`

                  - `:web_search_result`

                - `url: String`

                - `page_age: String`

              - `class BetaWebSearchToolRequestError`

                - `error_code: BetaWebSearchToolResultErrorCode`

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

            - `cache_control: BetaCacheControlEphemeral`

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

          - `class BetaWebFetchToolResultBlockParam`

            - `content: BetaWebFetchToolResultErrorBlockParam | BetaWebFetchBlockParam`

              - `class BetaWebFetchToolResultErrorBlockParam`

                - `error_code: BetaWebFetchToolResultErrorCode`

                  - `:invalid_tool_input`

                  - `:url_too_long`

                  - `:url_not_allowed`

                  - `:url_not_accessible`

                  - `:unsupported_content_type`

                  - `:too_many_requests`

                  - `:max_uses_exceeded`

                  - `:unavailable`

                - `type: :web_fetch_tool_result_error`

                  - `:web_fetch_tool_result_error`

              - `class BetaWebFetchBlockParam`

                - `content: BetaRequestDocumentBlock`

                  - `source: BetaBase64PDFSource | BetaPlainTextSource | BetaContentBlockSource | 2 more`

                    - `class BetaBase64PDFSource`

                      - `data: String`

                      - `media_type: :"application/pdf"`

                        - `:"application/pdf"`

                      - `type: :base64`

                        - `:base64`

                    - `class BetaPlainTextSource`

                      - `data: String`

                      - `media_type: :"text/plain"`

                        - `:"text/plain"`

                      - `type: :text`

                        - `:text`

                    - `class BetaContentBlockSource`

                      - `content: String | Array[BetaContentBlockSourceContent]`

                        - `String`

                        - `Array[BetaContentBlockSourceContent]`

                          - `class BetaTextBlockParam`

                            - `text: String`

                            - `type: :text`

                              - `:text`

                            - `cache_control: BetaCacheControlEphemeral`

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

                            - `citations: Array[BetaTextCitationParam]`

                              - `class BetaCitationCharLocationParam`

                                - `cited_text: String`

                                - `document_index: Integer`

                                - `document_title: String`

                                - `end_char_index: Integer`

                                - `start_char_index: Integer`

                                - `type: :char_location`

                                  - `:char_location`

                              - `class BetaCitationPageLocationParam`

                                - `cited_text: String`

                                - `document_index: Integer`

                                - `document_title: String`

                                - `end_page_number: Integer`

                                - `start_page_number: Integer`

                                - `type: :page_location`

                                  - `:page_location`

                              - `class BetaCitationContentBlockLocationParam`

                                - `cited_text: String`

                                - `document_index: Integer`

                                - `document_title: String`

                                - `end_block_index: Integer`

                                - `start_block_index: Integer`

                                - `type: :content_block_location`

                                  - `:content_block_location`

                              - `class BetaCitationWebSearchResultLocationParam`

                                - `cited_text: String`

                                - `encrypted_index: String`

                                - `title: String`

                                - `type: :web_search_result_location`

                                  - `:web_search_result_location`

                                - `url: String`

                              - `class BetaCitationSearchResultLocationParam`

                                - `cited_text: String`

                                - `end_block_index: Integer`

                                - `search_result_index: Integer`

                                - `source: String`

                                - `start_block_index: Integer`

                                - `title: String`

                                - `type: :search_result_location`

                                  - `:search_result_location`

                          - `class BetaImageBlockParam`

                            - `source: BetaBase64ImageSource | BetaURLImageSource | BetaFileImageSource`

                              - `class BetaBase64ImageSource`

                                - `data: String`

                                - `media_type: :"image/jpeg" | :"image/png" | :"image/gif" | :"image/webp"`

                                  - `:"image/jpeg"`

                                  - `:"image/png"`

                                  - `:"image/gif"`

                                  - `:"image/webp"`

                                - `type: :base64`

                                  - `:base64`

                              - `class BetaURLImageSource`

                                - `type: :url`

                                  - `:url`

                                - `url: String`

                              - `class BetaFileImageSource`

                                - `file_id: String`

                                - `type: :file`

                                  - `:file`

                            - `type: :image`

                              - `:image`

                            - `cache_control: BetaCacheControlEphemeral`

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

                    - `class BetaURLPDFSource`

                      - `type: :url`

                        - `:url`

                      - `url: String`

                    - `class BetaFileDocumentSource`

                      - `file_id: String`

                      - `type: :file`

                        - `:file`

                  - `type: :document`

                    - `:document`

                  - `cache_control: BetaCacheControlEphemeral`

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

                  - `citations: BetaCitationsConfigParam`

                    - `enabled: bool`

                  - `context: String`

                  - `title: String`

                - `type: :web_fetch_result`

                  - `:web_fetch_result`

                - `url: String`

                  Fetched content URL

                - `retrieved_at: String`

                  ISO 8601 timestamp when the content was retrieved

            - `tool_use_id: String`

            - `type: :web_fetch_tool_result`

              - `:web_fetch_tool_result`

            - `cache_control: BetaCacheControlEphemeral`

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

          - `class BetaCodeExecutionToolResultBlockParam`

            - `content: BetaCodeExecutionToolResultBlockParamContent`

              - `class BetaCodeExecutionToolResultErrorParam`

                - `error_code: BetaCodeExecutionToolResultErrorCode`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:too_many_requests`

                  - `:execution_time_exceeded`

                - `type: :code_execution_tool_result_error`

                  - `:code_execution_tool_result_error`

              - `class BetaCodeExecutionResultBlockParam`

                - `content: Array[BetaCodeExecutionOutputBlockParam]`

                  - `file_id: String`

                  - `type: :code_execution_output`

                    - `:code_execution_output`

                - `return_code: Integer`

                - `stderr: String`

                - `stdout: String`

                - `type: :code_execution_result`

                  - `:code_execution_result`

            - `tool_use_id: String`

            - `type: :code_execution_tool_result`

              - `:code_execution_tool_result`

            - `cache_control: BetaCacheControlEphemeral`

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

          - `class BetaBashCodeExecutionToolResultBlockParam`

            - `content: BetaBashCodeExecutionToolResultErrorParam | BetaBashCodeExecutionResultBlockParam`

              - `class BetaBashCodeExecutionToolResultErrorParam`

                - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:too_many_requests`

                  - `:execution_time_exceeded`

                  - `:output_file_too_large`

                - `type: :bash_code_execution_tool_result_error`

                  - `:bash_code_execution_tool_result_error`

              - `class BetaBashCodeExecutionResultBlockParam`

                - `content: Array[BetaBashCodeExecutionOutputBlockParam]`

                  - `file_id: String`

                  - `type: :bash_code_execution_output`

                    - `:bash_code_execution_output`

                - `return_code: Integer`

                - `stderr: String`

                - `stdout: String`

                - `type: :bash_code_execution_result`

                  - `:bash_code_execution_result`

            - `tool_use_id: String`

            - `type: :bash_code_execution_tool_result`

              - `:bash_code_execution_tool_result`

            - `cache_control: BetaCacheControlEphemeral`

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

          - `class BetaTextEditorCodeExecutionToolResultBlockParam`

            - `content: BetaTextEditorCodeExecutionToolResultErrorParam | BetaTextEditorCodeExecutionViewResultBlockParam | BetaTextEditorCodeExecutionCreateResultBlockParam | BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

              - `class BetaTextEditorCodeExecutionToolResultErrorParam`

                - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:too_many_requests`

                  - `:execution_time_exceeded`

                  - `:file_not_found`

                - `type: :text_editor_code_execution_tool_result_error`

                  - `:text_editor_code_execution_tool_result_error`

                - `error_message: String`

              - `class BetaTextEditorCodeExecutionViewResultBlockParam`

                - `content: String`

                - `file_type: :text | :image | :pdf`

                  - `:text`

                  - `:image`

                  - `:pdf`

                - `type: :text_editor_code_execution_view_result`

                  - `:text_editor_code_execution_view_result`

                - `num_lines: Integer`

                - `start_line: Integer`

                - `total_lines: Integer`

              - `class BetaTextEditorCodeExecutionCreateResultBlockParam`

                - `is_file_update: bool`

                - `type: :text_editor_code_execution_create_result`

                  - `:text_editor_code_execution_create_result`

              - `class BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

                - `type: :text_editor_code_execution_str_replace_result`

                  - `:text_editor_code_execution_str_replace_result`

                - `lines: Array[String]`

                - `new_lines: Integer`

                - `new_start: Integer`

                - `old_lines: Integer`

                - `old_start: Integer`

            - `tool_use_id: String`

            - `type: :text_editor_code_execution_tool_result`

              - `:text_editor_code_execution_tool_result`

            - `cache_control: BetaCacheControlEphemeral`

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

          - `class BetaToolSearchToolResultBlockParam`

            - `content: BetaToolSearchToolResultErrorParam | BetaToolSearchToolSearchResultBlockParam`

              - `class BetaToolSearchToolResultErrorParam`

                - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:too_many_requests`

                  - `:execution_time_exceeded`

                - `type: :tool_search_tool_result_error`

                  - `:tool_search_tool_result_error`

              - `class BetaToolSearchToolSearchResultBlockParam`

                - `tool_references: Array[BetaToolReferenceBlockParam]`

                  - `tool_name: String`

                  - `type: :tool_reference`

                    - `:tool_reference`

                  - `cache_control: BetaCacheControlEphemeral`

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

                - `type: :tool_search_tool_search_result`

                  - `:tool_search_tool_search_result`

            - `tool_use_id: String`

            - `type: :tool_search_tool_result`

              - `:tool_search_tool_result`

            - `cache_control: BetaCacheControlEphemeral`

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

          - `class BetaMCPToolUseBlockParam`

            - `id: String`

            - `input: Hash[Symbol, untyped]`

            - `name: String`

            - `server_name: String`

              The name of the MCP server

            - `type: :mcp_tool_use`

              - `:mcp_tool_use`

            - `cache_control: BetaCacheControlEphemeral`

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

          - `class BetaRequestMCPToolResultBlockParam`

            - `tool_use_id: String`

            - `type: :mcp_tool_result`

              - `:mcp_tool_result`

            - `cache_control: BetaCacheControlEphemeral`

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

            - `content: String | Array[BetaTextBlockParam]`

              - `String`

              - `Array[BetaTextBlockParam]`

                - `text: String`

                - `type: :text`

                  - `:text`

                - `cache_control: BetaCacheControlEphemeral`

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

                - `citations: Array[BetaTextCitationParam]`

                  - `class BetaCitationCharLocationParam`

                    - `cited_text: String`

                    - `document_index: Integer`

                    - `document_title: String`

                    - `end_char_index: Integer`

                    - `start_char_index: Integer`

                    - `type: :char_location`

                      - `:char_location`

                  - `class BetaCitationPageLocationParam`

                    - `cited_text: String`

                    - `document_index: Integer`

                    - `document_title: String`

                    - `end_page_number: Integer`

                    - `start_page_number: Integer`

                    - `type: :page_location`

                      - `:page_location`

                  - `class BetaCitationContentBlockLocationParam`

                    - `cited_text: String`

                    - `document_index: Integer`

                    - `document_title: String`

                    - `end_block_index: Integer`

                    - `start_block_index: Integer`

                    - `type: :content_block_location`

                      - `:content_block_location`

                  - `class BetaCitationWebSearchResultLocationParam`

                    - `cited_text: String`

                    - `encrypted_index: String`

                    - `title: String`

                    - `type: :web_search_result_location`

                      - `:web_search_result_location`

                    - `url: String`

                  - `class BetaCitationSearchResultLocationParam`

                    - `cited_text: String`

                    - `end_block_index: Integer`

                    - `search_result_index: Integer`

                    - `source: String`

                    - `start_block_index: Integer`

                    - `title: String`

                    - `type: :search_result_location`

                      - `:search_result_location`

            - `is_error: bool`

          - `class BetaContainerUploadBlockParam`

            A content block that represents a file to be uploaded to the container
            Files uploaded via this block will be available in the container's input directory.

            - `file_id: String`

            - `type: :container_upload`

              - `:container_upload`

            - `cache_control: BetaCacheControlEphemeral`

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

    - `container: BetaContainerParams | String`

      Container identifier for reuse across requests.

      - `class BetaContainerParams`

        Container parameters with skills to be loaded.

        - `id: String`

          Container id

        - `skills: Array[BetaSkillParams]`

          List of skills to load in the container

          - `skill_id: String`

            Skill ID

          - `type: :anthropic | :custom`

            Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

            - `:anthropic`

            - `:custom`

          - `version: String`

            Skill version or 'latest' for most recent version

      - `String`

    - `context_management: BetaContextManagementConfig`

      Context management configuration.

      This allows you to control how Claude manages context across multiple requests, such as whether to clear function results or not.

      - `edits: Array[BetaClearToolUses20250919Edit | BetaClearThinking20251015Edit]`

        List of context management edits to apply

        - `class BetaClearToolUses20250919Edit`

          - `type: :clear_tool_uses_20250919`

            - `:clear_tool_uses_20250919`

          - `clear_at_least: BetaInputTokensClearAtLeast`

            Minimum number of tokens that must be cleared when triggered. Context will only be modified if at least this many tokens can be removed.

            - `type: :input_tokens`

              - `:input_tokens`

            - `value: Integer`

          - `clear_tool_inputs: bool | Array[String]`

            Whether to clear all tool inputs (bool) or specific tool inputs to clear (list)

            - `bool`

            - `Array[String]`

          - `exclude_tools: Array[String]`

            Tool names whose uses are preserved from clearing

          - `keep: BetaToolUsesKeep`

            Number of tool uses to retain in the conversation

            - `type: :tool_uses`

              - `:tool_uses`

            - `value: Integer`

          - `trigger: BetaInputTokensTrigger | BetaToolUsesTrigger`

            Condition that triggers the context management strategy

            - `class BetaInputTokensTrigger`

              - `type: :input_tokens`

                - `:input_tokens`

              - `value: Integer`

            - `class BetaToolUsesTrigger`

              - `type: :tool_uses`

                - `:tool_uses`

              - `value: Integer`

        - `class BetaClearThinking20251015Edit`

          - `type: :clear_thinking_20251015`

            - `:clear_thinking_20251015`

          - `keep: BetaThinkingTurns | BetaAllThinkingTurns | :all`

            Number of most recent assistant turns to keep thinking blocks for. Older turns will have their thinking blocks removed.

            - `class BetaThinkingTurns`

              - `type: :thinking_turns`

                - `:thinking_turns`

              - `value: Integer`

            - `class BetaAllThinkingTurns`

              - `type: :all`

                - `:all`

            - `Keep = :all`

              - `:all`

    - `mcp_servers: Array[BetaRequestMCPServerURLDefinition]`

      MCP servers to be utilized in this request

      - `name: String`

      - `type: :url`

        - `:url`

      - `url: String`

      - `authorization_token: String`

      - `tool_configuration: BetaRequestMCPServerToolConfiguration`

        - `allowed_tools: Array[String]`

        - `enabled: bool`

    - `metadata: BetaMetadata`

      An object describing metadata about the request.

      - `user_id: String`

        An external identifier for the user who is associated with the request.

        This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

    - `output_config: BetaOutputConfig`

      Configuration options for the model's output. Controls aspects like how much effort the model puts into its response.

      - `effort: :low | :medium | :high`

        All possible effort levels.

        - `:low`

        - `:medium`

        - `:high`

    - `output_format: BetaJSONOutputFormat`

      A schema to specify Claude's output format in responses.

      - `schema: Hash[Symbol, untyped]`

        The JSON schema of the format

      - `type: :json_schema`

        - `:json_schema`

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

    - `system_: String | Array[BetaTextBlockParam]`

      System prompt.

      A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

      - `String`

      - `Array[BetaTextBlockParam]`

        - `text: String`

        - `type: :text`

          - `:text`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `citations: Array[BetaTextCitationParam]`

          - `class BetaCitationCharLocationParam`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_char_index: Integer`

            - `start_char_index: Integer`

            - `type: :char_location`

              - `:char_location`

          - `class BetaCitationPageLocationParam`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_page_number: Integer`

            - `start_page_number: Integer`

            - `type: :page_location`

              - `:page_location`

          - `class BetaCitationContentBlockLocationParam`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_block_index: Integer`

            - `start_block_index: Integer`

            - `type: :content_block_location`

              - `:content_block_location`

          - `class BetaCitationWebSearchResultLocationParam`

            - `cited_text: String`

            - `encrypted_index: String`

            - `title: String`

            - `type: :web_search_result_location`

              - `:web_search_result_location`

            - `url: String`

          - `class BetaCitationSearchResultLocationParam`

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

    - `thinking: BetaThinkingConfigParam`

      Configuration for enabling Claude's extended thinking.

      When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

      See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

      - `class BetaThinkingConfigEnabled`

        - `budget_tokens: Integer`

          Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

          Must be ≥1024 and less than `max_tokens`.

          See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

        - `type: :enabled`

          - `:enabled`

      - `class BetaThinkingConfigDisabled`

        - `type: :disabled`

          - `:disabled`

    - `tool_choice: BetaToolChoice`

      How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

      - `class BetaToolChoiceAuto`

        The model will automatically decide whether to use tools.

        - `type: :auto`

          - `:auto`

        - `disable_parallel_tool_use: bool`

          Whether to disable parallel tool use.

          Defaults to `false`. If set to `true`, the model will output at most one tool use.

      - `class BetaToolChoiceAny`

        The model will use any available tools.

        - `type: :any`

          - `:any`

        - `disable_parallel_tool_use: bool`

          Whether to disable parallel tool use.

          Defaults to `false`. If set to `true`, the model will output exactly one tool use.

      - `class BetaToolChoiceTool`

        The model will use the specified tool with `tool_choice.name`.

        - `name: String`

          The name of the tool to use.

        - `type: :tool`

          - `:tool`

        - `disable_parallel_tool_use: bool`

          Whether to disable parallel tool use.

          Defaults to `false`. If set to `true`, the model will output exactly one tool use.

      - `class BetaToolChoiceNone`

        The model will not be allowed to use tools.

        - `type: :none`

          - `:none`

    - `tools: Array[BetaToolUnion]`

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

      - `class BetaTool`

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

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `description: String`

          Description of what this tool does.

          Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

        - `input_examples: Array[Hash[Symbol, untyped]]`

        - `strict: bool`

        - `type: :custom`

          - `:custom`

      - `class BetaToolBash20241022`

        - `name: :bash`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:bash`

        - `type: :bash_20241022`

          - `:bash_20241022`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples: Array[Hash[Symbol, untyped]]`

        - `strict: bool`

      - `class BetaToolBash20250124`

        - `name: :bash`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:bash`

        - `type: :bash_20250124`

          - `:bash_20250124`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples: Array[Hash[Symbol, untyped]]`

        - `strict: bool`

      - `class BetaCodeExecutionTool20250522`

        - `name: :code_execution`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:code_execution`

        - `type: :code_execution_20250522`

          - `:code_execution_20250522`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `strict: bool`

      - `class BetaCodeExecutionTool20250825`

        - `name: :code_execution`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:code_execution`

        - `type: :code_execution_20250825`

          - `:code_execution_20250825`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `strict: bool`

      - `class BetaToolComputerUse20241022`

        - `display_height_px: Integer`

          The height of the display in pixels.

        - `display_width_px: Integer`

          The width of the display in pixels.

        - `name: :computer`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:computer`

        - `type: :computer_20241022`

          - `:computer_20241022`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `display_number: Integer`

          The X11 display number (e.g. 0, 1) for the display.

        - `input_examples: Array[Hash[Symbol, untyped]]`

        - `strict: bool`

      - `class BetaMemoryTool20250818`

        - `name: :memory`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:memory`

        - `type: :memory_20250818`

          - `:memory_20250818`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples: Array[Hash[Symbol, untyped]]`

        - `strict: bool`

      - `class BetaToolComputerUse20250124`

        - `display_height_px: Integer`

          The height of the display in pixels.

        - `display_width_px: Integer`

          The width of the display in pixels.

        - `name: :computer`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:computer`

        - `type: :computer_20250124`

          - `:computer_20250124`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `display_number: Integer`

          The X11 display number (e.g. 0, 1) for the display.

        - `input_examples: Array[Hash[Symbol, untyped]]`

        - `strict: bool`

      - `class BetaToolTextEditor20241022`

        - `name: :str_replace_editor`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:str_replace_editor`

        - `type: :text_editor_20241022`

          - `:text_editor_20241022`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples: Array[Hash[Symbol, untyped]]`

        - `strict: bool`

      - `class BetaToolComputerUse20251124`

        - `display_height_px: Integer`

          The height of the display in pixels.

        - `display_width_px: Integer`

          The width of the display in pixels.

        - `name: :computer`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:computer`

        - `type: :computer_20251124`

          - `:computer_20251124`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `display_number: Integer`

          The X11 display number (e.g. 0, 1) for the display.

        - `enable_zoom: bool`

          Whether to enable an action to take a zoomed-in screenshot of the screen.

        - `input_examples: Array[Hash[Symbol, untyped]]`

        - `strict: bool`

      - `class BetaToolTextEditor20250124`

        - `name: :str_replace_editor`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:str_replace_editor`

        - `type: :text_editor_20250124`

          - `:text_editor_20250124`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples: Array[Hash[Symbol, untyped]]`

        - `strict: bool`

      - `class BetaToolTextEditor20250429`

        - `name: :str_replace_based_edit_tool`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:str_replace_based_edit_tool`

        - `type: :text_editor_20250429`

          - `:text_editor_20250429`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples: Array[Hash[Symbol, untyped]]`

        - `strict: bool`

      - `class BetaToolTextEditor20250728`

        - `name: :str_replace_based_edit_tool`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:str_replace_based_edit_tool`

        - `type: :text_editor_20250728`

          - `:text_editor_20250728`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `input_examples: Array[Hash[Symbol, untyped]]`

        - `max_characters: Integer`

          Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

        - `strict: bool`

      - `class BetaWebSearchTool20250305`

        - `name: :web_search`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:web_search`

        - `type: :web_search_20250305`

          - `:web_search_20250305`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `allowed_domains: Array[String]`

          If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

        - `blocked_domains: Array[String]`

          If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `max_uses: Integer`

          Maximum number of times the tool can be used in the API request.

        - `strict: bool`

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

      - `class BetaWebFetchTool20250910`

        - `name: :web_fetch`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:web_fetch`

        - `type: :web_fetch_20250910`

          - `:web_fetch_20250910`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `allowed_domains: Array[String]`

          List of domains to allow fetching from

        - `blocked_domains: Array[String]`

          List of domains to block fetching from

        - `cache_control: BetaCacheControlEphemeral`

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

        - `citations: BetaCitationsConfigParam`

          Citations configuration for fetched documents. Citations are disabled by default.

          - `enabled: bool`

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `max_content_tokens: Integer`

          Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

        - `max_uses: Integer`

          Maximum number of times the tool can be used in the API request.

        - `strict: bool`

      - `class BetaToolSearchToolBm25_20251119`

        - `name: :tool_search_tool_bm25`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:tool_search_tool_bm25`

        - `type: :tool_search_tool_bm25_20251119 | :tool_search_tool_bm25`

          - `:tool_search_tool_bm25_20251119`

          - `:tool_search_tool_bm25`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `strict: bool`

      - `class BetaToolSearchToolRegex20251119`

        - `name: :tool_search_tool_regex`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `:tool_search_tool_regex`

        - `type: :tool_search_tool_regex_20251119 | :tool_search_tool_regex`

          - `:tool_search_tool_regex_20251119`

          - `:tool_search_tool_regex`

        - `allowed_callers: Array[:direct | :code_execution_20250825]`

          - `:direct`

          - `:code_execution_20250825`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `defer_loading: bool`

          If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

        - `strict: bool`

      - `class BetaMCPToolset`

        Configuration for a group of tools from an MCP server.

        Allows configuring enabled status and defer_loading for all tools
        from an MCP server, with optional per-tool overrides.

        - `mcp_server_name: String`

          Name of the MCP server to configure tools for

        - `type: :mcp_toolset`

          - `:mcp_toolset`

        - `cache_control: BetaCacheControlEphemeral`

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

        - `configs: Hash[Symbol, BetaMCPToolConfig]`

          Configuration overrides for specific tools, keyed by tool name

          - `defer_loading: bool`

          - `enabled: bool`

        - `default_config: BetaMCPToolDefaultConfig`

          Default configuration applied to all tools from this server

          - `defer_loading: bool`

          - `enabled: bool`

    - `top_k: Integer`

      Only sample from the top K options for each subsequent token.

      Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

      Recommended for advanced use cases only. You usually only need to use `temperature`.

    - `top_p: Float`

      Use nucleus sampling.

      In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

      Recommended for advanced use cases only. You usually only need to use `temperature`.

- `anthropic_beta: Array[AnthropicBeta]`

  Optional header to specify the beta version(s) you want to use.

  - `String`

  - `:"message-batches-2024-09-24" | :"prompt-caching-2024-07-31" | :"computer-use-2024-10-22" | 16 more`

    - `:"message-batches-2024-09-24"`

    - `:"prompt-caching-2024-07-31"`

    - `:"computer-use-2024-10-22"`

    - `:"computer-use-2025-01-24"`

    - `:"pdfs-2024-09-25"`

    - `:"token-counting-2024-11-01"`

    - `:"token-efficient-tools-2025-02-19"`

    - `:"output-128k-2025-02-19"`

    - `:"files-api-2025-04-14"`

    - `:"mcp-client-2025-04-04"`

    - `:"mcp-client-2025-11-20"`

    - `:"dev-full-thinking-2025-05-14"`

    - `:"interleaved-thinking-2025-05-14"`

    - `:"code-execution-2025-05-22"`

    - `:"extended-cache-ttl-2025-04-11"`

    - `:"context-1m-2025-08-07"`

    - `:"context-management-2025-06-27"`

    - `:"model-context-window-exceeded-2025-08-26"`

    - `:"skills-2025-10-02"`

### Returns

- `class BetaMessageBatch`

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

  - `request_counts: BetaMessageBatchRequestCounts`

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

beta_message_batch = anthropic.beta.messages.batches.create(
  requests: [
    {
      custom_id: "my-custom-id-1",
      params: {max_tokens: 1024, messages: [{content: "Hello, world", role: :user}], model: :"claude-opus-4-5-20251101"}
    }
  ]
)

puts(beta_message_batch)
```
