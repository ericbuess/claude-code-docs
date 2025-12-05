# Messages

## Create

`beta.messages.create(**kwargs) -> BetaMessage`

**post** `/v1/messages`

Send a structured list of input messages with text and/or image content, and the model will generate the next message in the conversation.

The Messages API can be used for either single queries or stateless multi-turn conversations.

Learn more about the Messages API in our [user guide](https://docs.claude.com/en/docs/initial-setup)

### Parameters

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

- `stream: false`

  Whether to incrementally stream the response using server-sent events.

  See [streaming](https://docs.claude.com/en/api/messages-streaming) for details.

  - `false`

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

- `class BetaMessage`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `container: BetaContainer`

    Information about the container used in the request (for the code execution tool)

    - `id: String`

      Identifier for the container used in this request

    - `expires_at: Time`

      The time at which the container will expire.

    - `skills: Array[BetaSkill]`

      Skills loaded in the container

      - `skill_id: String`

        Skill ID

      - `type: :anthropic | :custom`

        Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

        - `:anthropic`

        - `:custom`

      - `version: String`

        Skill version or 'latest' for most recent version

  - `content: Array[BetaContentBlock]`

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

    - `class BetaTextBlock`

      - `citations: Array[BetaTextCitation]`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `class BetaCitationCharLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_char_index: Integer`

          - `file_id: String`

          - `start_char_index: Integer`

          - `type: :char_location`

            - `:char_location`

        - `class BetaCitationPageLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_page_number: Integer`

          - `file_id: String`

          - `start_page_number: Integer`

          - `type: :page_location`

            - `:page_location`

        - `class BetaCitationContentBlockLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_block_index: Integer`

          - `file_id: String`

          - `start_block_index: Integer`

          - `type: :content_block_location`

            - `:content_block_location`

        - `class BetaCitationsWebSearchResultLocation`

          - `cited_text: String`

          - `encrypted_index: String`

          - `title: String`

          - `type: :web_search_result_location`

            - `:web_search_result_location`

          - `url: String`

        - `class BetaCitationSearchResultLocation`

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

    - `class BetaThinkingBlock`

      - `signature: String`

      - `thinking: String`

      - `type: :thinking`

        - `:thinking`

    - `class BetaRedactedThinkingBlock`

      - `data: String`

      - `type: :redacted_thinking`

        - `:redacted_thinking`

    - `class BetaToolUseBlock`

      - `id: String`

      - `input: Hash[Symbol, untyped]`

      - `name: String`

      - `type: :tool_use`

        - `:tool_use`

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

    - `class BetaServerToolUseBlock`

      - `id: String`

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

    - `class BetaWebSearchToolResultBlock`

      - `content: BetaWebSearchToolResultBlockContent`

        - `class BetaWebSearchToolResultError`

          - `error_code: BetaWebSearchToolResultErrorCode`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:max_uses_exceeded`

            - `:too_many_requests`

            - `:query_too_long`

          - `type: :web_search_tool_result_error`

            - `:web_search_tool_result_error`

        - `Array[BetaWebSearchResultBlock]`

          - `encrypted_content: String`

          - `page_age: String`

          - `title: String`

          - `type: :web_search_result`

            - `:web_search_result`

          - `url: String`

      - `tool_use_id: String`

      - `type: :web_search_tool_result`

        - `:web_search_tool_result`

    - `class BetaWebFetchToolResultBlock`

      - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

        - `class BetaWebFetchToolResultErrorBlock`

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

        - `class BetaWebFetchBlock`

          - `content: BetaDocumentBlock`

            - `citations: BetaCitationConfig`

              Citation configuration for the document

              - `enabled: bool`

            - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

            - `title: String`

              The title of the document

            - `type: :document`

              - `:document`

          - `retrieved_at: String`

            ISO 8601 timestamp when the content was retrieved

          - `type: :web_fetch_result`

            - `:web_fetch_result`

          - `url: String`

            Fetched content URL

      - `tool_use_id: String`

      - `type: :web_fetch_tool_result`

        - `:web_fetch_tool_result`

    - `class BetaCodeExecutionToolResultBlock`

      - `content: BetaCodeExecutionToolResultBlockContent`

        - `class BetaCodeExecutionToolResultError`

          - `error_code: BetaCodeExecutionToolResultErrorCode`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:too_many_requests`

            - `:execution_time_exceeded`

          - `type: :code_execution_tool_result_error`

            - `:code_execution_tool_result_error`

        - `class BetaCodeExecutionResultBlock`

          - `content: Array[BetaCodeExecutionOutputBlock]`

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

    - `class BetaBashCodeExecutionToolResultBlock`

      - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

        - `class BetaBashCodeExecutionToolResultError`

          - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:too_many_requests`

            - `:execution_time_exceeded`

            - `:output_file_too_large`

          - `type: :bash_code_execution_tool_result_error`

            - `:bash_code_execution_tool_result_error`

        - `class BetaBashCodeExecutionResultBlock`

          - `content: Array[BetaBashCodeExecutionOutputBlock]`

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

    - `class BetaTextEditorCodeExecutionToolResultBlock`

      - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

        - `class BetaTextEditorCodeExecutionToolResultError`

          - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:too_many_requests`

            - `:execution_time_exceeded`

            - `:file_not_found`

          - `error_message: String`

          - `type: :text_editor_code_execution_tool_result_error`

            - `:text_editor_code_execution_tool_result_error`

        - `class BetaTextEditorCodeExecutionViewResultBlock`

          - `content: String`

          - `file_type: :text | :image | :pdf`

            - `:text`

            - `:image`

            - `:pdf`

          - `num_lines: Integer`

          - `start_line: Integer`

          - `total_lines: Integer`

          - `type: :text_editor_code_execution_view_result`

            - `:text_editor_code_execution_view_result`

        - `class BetaTextEditorCodeExecutionCreateResultBlock`

          - `is_file_update: bool`

          - `type: :text_editor_code_execution_create_result`

            - `:text_editor_code_execution_create_result`

        - `class BetaTextEditorCodeExecutionStrReplaceResultBlock`

          - `lines: Array[String]`

          - `new_lines: Integer`

          - `new_start: Integer`

          - `old_lines: Integer`

          - `old_start: Integer`

          - `type: :text_editor_code_execution_str_replace_result`

            - `:text_editor_code_execution_str_replace_result`

      - `tool_use_id: String`

      - `type: :text_editor_code_execution_tool_result`

        - `:text_editor_code_execution_tool_result`

    - `class BetaToolSearchToolResultBlock`

      - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

        - `class BetaToolSearchToolResultError`

          - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:too_many_requests`

            - `:execution_time_exceeded`

          - `error_message: String`

          - `type: :tool_search_tool_result_error`

            - `:tool_search_tool_result_error`

        - `class BetaToolSearchToolSearchResultBlock`

          - `tool_references: Array[BetaToolReferenceBlock]`

            - `tool_name: String`

            - `type: :tool_reference`

              - `:tool_reference`

          - `type: :tool_search_tool_search_result`

            - `:tool_search_tool_search_result`

      - `tool_use_id: String`

      - `type: :tool_search_tool_result`

        - `:tool_search_tool_result`

    - `class BetaMCPToolUseBlock`

      - `id: String`

      - `input: Hash[Symbol, untyped]`

      - `name: String`

        The name of the MCP tool

      - `server_name: String`

        The name of the MCP server

      - `type: :mcp_tool_use`

        - `:mcp_tool_use`

    - `class BetaMCPToolResultBlock`

      - `content: String | Array[BetaTextBlock]`

        - `String`

        - `Array[BetaTextBlock]`

          - `citations: Array[BetaTextCitation]`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `class BetaCitationCharLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_char_index: Integer`

              - `file_id: String`

              - `start_char_index: Integer`

              - `type: :char_location`

                - `:char_location`

            - `class BetaCitationPageLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_page_number: Integer`

              - `file_id: String`

              - `start_page_number: Integer`

              - `type: :page_location`

                - `:page_location`

            - `class BetaCitationContentBlockLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_block_index: Integer`

              - `file_id: String`

              - `start_block_index: Integer`

              - `type: :content_block_location`

                - `:content_block_location`

            - `class BetaCitationsWebSearchResultLocation`

              - `cited_text: String`

              - `encrypted_index: String`

              - `title: String`

              - `type: :web_search_result_location`

                - `:web_search_result_location`

              - `url: String`

            - `class BetaCitationSearchResultLocation`

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

      - `is_error: bool`

      - `tool_use_id: String`

      - `type: :mcp_tool_result`

        - `:mcp_tool_result`

    - `class BetaContainerUploadBlock`

      Response model for a file uploaded to the container.

      - `file_id: String`

      - `type: :container_upload`

        - `:container_upload`

  - `context_management: BetaContextManagementResponse`

    Context management response.

    Information about context management strategies applied during the request.

    - `applied_edits: Array[BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse]`

      List of context management edits that were applied.

      - `class BetaClearToolUses20250919EditResponse`

        - `cleared_input_tokens: Integer`

          Number of input tokens cleared by this edit.

        - `cleared_tool_uses: Integer`

          Number of tool uses that were cleared.

        - `type: :clear_tool_uses_20250919`

          The type of context management edit applied.

          - `:clear_tool_uses_20250919`

      - `class BetaClearThinking20251015EditResponse`

        - `cleared_input_tokens: Integer`

          Number of input tokens cleared by this edit.

        - `cleared_thinking_turns: Integer`

          Number of thinking turns that were cleared.

        - `type: :clear_thinking_20251015`

          The type of context management edit applied.

          - `:clear_thinking_20251015`

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

  - `stop_reason: BetaStopReason`

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

    - `:model_context_window_exceeded`

  - `stop_sequence: String`

    Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was generated.

  - `type: :message`

    Object type.

    For Messages, this is always `"message"`.

    - `:message`

  - `usage: BetaUsage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cache_creation: BetaCacheCreation`

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

    - `server_tool_use: BetaServerToolUsage`

      The number of server tool requests.

      - `web_fetch_requests: Integer`

        The number of web fetch tool requests.

      - `web_search_requests: Integer`

        The number of web search tool requests.

    - `service_tier: :standard | :priority | :batch`

      If the request used the priority, standard, or batch tier.

      - `:standard`

      - `:priority`

      - `:batch`

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

beta_message = anthropic.beta.messages.create(
  max_tokens: 1024,
  messages: [{content: "Hello, world", role: :user}],
  model: :"claude-opus-4-5-20251101"
)

puts(beta_message)
```

## Count Tokens

`beta.messages.count_tokens(**kwargs) -> BetaMessageTokensCount`

**post** `/v1/messages/count_tokens`

Count the number of tokens in a Message.

The Token Count API can be used to count the number of tokens in a Message, including tools, images, and documents, without creating it.

Learn more about token counting in our [user guide](https://docs.claude.com/en/docs/build-with-claude/token-counting)

### Parameters

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

- `tools: Array[BetaTool | BetaToolBash20241022 | BetaToolBash20250124 | 15 more]`

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

- `class BetaMessageTokensCount`

  - `context_management: BetaCountTokensContextManagementResponse`

    Information about context management applied to the message.

    - `original_input_tokens: Integer`

      The original token count before context management was applied

  - `input_tokens: Integer`

    The total number of tokens across the provided list of messages, system prompt, and tools.

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

beta_message_tokens_count = anthropic.beta.messages.count_tokens(
  messages: [{content: "string", role: :user}],
  model: :"claude-opus-4-5-20251101"
)

puts(beta_message_tokens_count)
```

## Domain Types

### Beta All Thinking Turns

- `class BetaAllThinkingTurns`

  - `type: :all`

    - `:all`

### Beta Base64 Image Source

- `class BetaBase64ImageSource`

  - `data: String`

  - `media_type: :"image/jpeg" | :"image/png" | :"image/gif" | :"image/webp"`

    - `:"image/jpeg"`

    - `:"image/png"`

    - `:"image/gif"`

    - `:"image/webp"`

  - `type: :base64`

    - `:base64`

### Beta Base64 PDF Source

- `class BetaBase64PDFSource`

  - `data: String`

  - `media_type: :"application/pdf"`

    - `:"application/pdf"`

  - `type: :base64`

    - `:base64`

### Beta Bash Code Execution Output Block

- `class BetaBashCodeExecutionOutputBlock`

  - `file_id: String`

  - `type: :bash_code_execution_output`

    - `:bash_code_execution_output`

### Beta Bash Code Execution Output Block Param

- `class BetaBashCodeExecutionOutputBlockParam`

  - `file_id: String`

  - `type: :bash_code_execution_output`

    - `:bash_code_execution_output`

### Beta Bash Code Execution Result Block

- `class BetaBashCodeExecutionResultBlock`

  - `content: Array[BetaBashCodeExecutionOutputBlock]`

    - `file_id: String`

    - `type: :bash_code_execution_output`

      - `:bash_code_execution_output`

  - `return_code: Integer`

  - `stderr: String`

  - `stdout: String`

  - `type: :bash_code_execution_result`

    - `:bash_code_execution_result`

### Beta Bash Code Execution Result Block Param

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

### Beta Bash Code Execution Tool Result Block

- `class BetaBashCodeExecutionToolResultBlock`

  - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

    - `class BetaBashCodeExecutionToolResultError`

      - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

        - `:invalid_tool_input`

        - `:unavailable`

        - `:too_many_requests`

        - `:execution_time_exceeded`

        - `:output_file_too_large`

      - `type: :bash_code_execution_tool_result_error`

        - `:bash_code_execution_tool_result_error`

    - `class BetaBashCodeExecutionResultBlock`

      - `content: Array[BetaBashCodeExecutionOutputBlock]`

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

### Beta Bash Code Execution Tool Result Block Param

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

### Beta Bash Code Execution Tool Result Error

- `class BetaBashCodeExecutionToolResultError`

  - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

    - `:invalid_tool_input`

    - `:unavailable`

    - `:too_many_requests`

    - `:execution_time_exceeded`

    - `:output_file_too_large`

  - `type: :bash_code_execution_tool_result_error`

    - `:bash_code_execution_tool_result_error`

### Beta Bash Code Execution Tool Result Error Param

- `class BetaBashCodeExecutionToolResultErrorParam`

  - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

    - `:invalid_tool_input`

    - `:unavailable`

    - `:too_many_requests`

    - `:execution_time_exceeded`

    - `:output_file_too_large`

  - `type: :bash_code_execution_tool_result_error`

    - `:bash_code_execution_tool_result_error`

### Beta Cache Control Ephemeral

- `class BetaCacheControlEphemeral`

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

### Beta Cache Creation

- `class BetaCacheCreation`

  - `ephemeral_1h_input_tokens: Integer`

    The number of input tokens used to create the 1 hour cache entry.

  - `ephemeral_5m_input_tokens: Integer`

    The number of input tokens used to create the 5 minute cache entry.

### Beta Citation Char Location

- `class BetaCitationCharLocation`

  - `cited_text: String`

  - `document_index: Integer`

  - `document_title: String`

  - `end_char_index: Integer`

  - `file_id: String`

  - `start_char_index: Integer`

  - `type: :char_location`

    - `:char_location`

### Beta Citation Char Location Param

- `class BetaCitationCharLocationParam`

  - `cited_text: String`

  - `document_index: Integer`

  - `document_title: String`

  - `end_char_index: Integer`

  - `start_char_index: Integer`

  - `type: :char_location`

    - `:char_location`

### Beta Citation Config

- `class BetaCitationConfig`

  - `enabled: bool`

### Beta Citation Content Block Location

- `class BetaCitationContentBlockLocation`

  - `cited_text: String`

  - `document_index: Integer`

  - `document_title: String`

  - `end_block_index: Integer`

  - `file_id: String`

  - `start_block_index: Integer`

  - `type: :content_block_location`

    - `:content_block_location`

### Beta Citation Content Block Location Param

- `class BetaCitationContentBlockLocationParam`

  - `cited_text: String`

  - `document_index: Integer`

  - `document_title: String`

  - `end_block_index: Integer`

  - `start_block_index: Integer`

  - `type: :content_block_location`

    - `:content_block_location`

### Beta Citation Page Location

- `class BetaCitationPageLocation`

  - `cited_text: String`

  - `document_index: Integer`

  - `document_title: String`

  - `end_page_number: Integer`

  - `file_id: String`

  - `start_page_number: Integer`

  - `type: :page_location`

    - `:page_location`

### Beta Citation Page Location Param

- `class BetaCitationPageLocationParam`

  - `cited_text: String`

  - `document_index: Integer`

  - `document_title: String`

  - `end_page_number: Integer`

  - `start_page_number: Integer`

  - `type: :page_location`

    - `:page_location`

### Beta Citation Search Result Location

- `class BetaCitationSearchResultLocation`

  - `cited_text: String`

  - `end_block_index: Integer`

  - `search_result_index: Integer`

  - `source: String`

  - `start_block_index: Integer`

  - `title: String`

  - `type: :search_result_location`

    - `:search_result_location`

### Beta Citation Search Result Location Param

- `class BetaCitationSearchResultLocationParam`

  - `cited_text: String`

  - `end_block_index: Integer`

  - `search_result_index: Integer`

  - `source: String`

  - `start_block_index: Integer`

  - `title: String`

  - `type: :search_result_location`

    - `:search_result_location`

### Beta Citation Web Search Result Location Param

- `class BetaCitationWebSearchResultLocationParam`

  - `cited_text: String`

  - `encrypted_index: String`

  - `title: String`

  - `type: :web_search_result_location`

    - `:web_search_result_location`

  - `url: String`

### Beta Citations Config Param

- `class BetaCitationsConfigParam`

  - `enabled: bool`

### Beta Citations Delta

- `class BetaCitationsDelta`

  - `citation: BetaCitationCharLocation | BetaCitationPageLocation | BetaCitationContentBlockLocation | 2 more`

    - `class BetaCitationCharLocation`

      - `cited_text: String`

      - `document_index: Integer`

      - `document_title: String`

      - `end_char_index: Integer`

      - `file_id: String`

      - `start_char_index: Integer`

      - `type: :char_location`

        - `:char_location`

    - `class BetaCitationPageLocation`

      - `cited_text: String`

      - `document_index: Integer`

      - `document_title: String`

      - `end_page_number: Integer`

      - `file_id: String`

      - `start_page_number: Integer`

      - `type: :page_location`

        - `:page_location`

    - `class BetaCitationContentBlockLocation`

      - `cited_text: String`

      - `document_index: Integer`

      - `document_title: String`

      - `end_block_index: Integer`

      - `file_id: String`

      - `start_block_index: Integer`

      - `type: :content_block_location`

        - `:content_block_location`

    - `class BetaCitationsWebSearchResultLocation`

      - `cited_text: String`

      - `encrypted_index: String`

      - `title: String`

      - `type: :web_search_result_location`

        - `:web_search_result_location`

      - `url: String`

    - `class BetaCitationSearchResultLocation`

      - `cited_text: String`

      - `end_block_index: Integer`

      - `search_result_index: Integer`

      - `source: String`

      - `start_block_index: Integer`

      - `title: String`

      - `type: :search_result_location`

        - `:search_result_location`

  - `type: :citations_delta`

    - `:citations_delta`

### Beta Citations Web Search Result Location

- `class BetaCitationsWebSearchResultLocation`

  - `cited_text: String`

  - `encrypted_index: String`

  - `title: String`

  - `type: :web_search_result_location`

    - `:web_search_result_location`

  - `url: String`

### Beta Clear Thinking 20251015 Edit

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

### Beta Clear Thinking 20251015 Edit Response

- `class BetaClearThinking20251015EditResponse`

  - `cleared_input_tokens: Integer`

    Number of input tokens cleared by this edit.

  - `cleared_thinking_turns: Integer`

    Number of thinking turns that were cleared.

  - `type: :clear_thinking_20251015`

    The type of context management edit applied.

    - `:clear_thinking_20251015`

### Beta Clear Tool Uses 20250919 Edit

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

### Beta Clear Tool Uses 20250919 Edit Response

- `class BetaClearToolUses20250919EditResponse`

  - `cleared_input_tokens: Integer`

    Number of input tokens cleared by this edit.

  - `cleared_tool_uses: Integer`

    Number of tool uses that were cleared.

  - `type: :clear_tool_uses_20250919`

    The type of context management edit applied.

    - `:clear_tool_uses_20250919`

### Beta Code Execution Output Block

- `class BetaCodeExecutionOutputBlock`

  - `file_id: String`

  - `type: :code_execution_output`

    - `:code_execution_output`

### Beta Code Execution Output Block Param

- `class BetaCodeExecutionOutputBlockParam`

  - `file_id: String`

  - `type: :code_execution_output`

    - `:code_execution_output`

### Beta Code Execution Result Block

- `class BetaCodeExecutionResultBlock`

  - `content: Array[BetaCodeExecutionOutputBlock]`

    - `file_id: String`

    - `type: :code_execution_output`

      - `:code_execution_output`

  - `return_code: Integer`

  - `stderr: String`

  - `stdout: String`

  - `type: :code_execution_result`

    - `:code_execution_result`

### Beta Code Execution Result Block Param

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

### Beta Code Execution Tool 20250522

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

### Beta Code Execution Tool 20250825

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

### Beta Code Execution Tool Result Block

- `class BetaCodeExecutionToolResultBlock`

  - `content: BetaCodeExecutionToolResultBlockContent`

    - `class BetaCodeExecutionToolResultError`

      - `error_code: BetaCodeExecutionToolResultErrorCode`

        - `:invalid_tool_input`

        - `:unavailable`

        - `:too_many_requests`

        - `:execution_time_exceeded`

      - `type: :code_execution_tool_result_error`

        - `:code_execution_tool_result_error`

    - `class BetaCodeExecutionResultBlock`

      - `content: Array[BetaCodeExecutionOutputBlock]`

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

### Beta Code Execution Tool Result Block Content

- `BetaCodeExecutionToolResultBlockContent = BetaCodeExecutionToolResultError | BetaCodeExecutionResultBlock`

  - `class BetaCodeExecutionToolResultError`

    - `error_code: BetaCodeExecutionToolResultErrorCode`

      - `:invalid_tool_input`

      - `:unavailable`

      - `:too_many_requests`

      - `:execution_time_exceeded`

    - `type: :code_execution_tool_result_error`

      - `:code_execution_tool_result_error`

  - `class BetaCodeExecutionResultBlock`

    - `content: Array[BetaCodeExecutionOutputBlock]`

      - `file_id: String`

      - `type: :code_execution_output`

        - `:code_execution_output`

    - `return_code: Integer`

    - `stderr: String`

    - `stdout: String`

    - `type: :code_execution_result`

      - `:code_execution_result`

### Beta Code Execution Tool Result Block Param

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

### Beta Code Execution Tool Result Block Param Content

- `BetaCodeExecutionToolResultBlockParamContent = BetaCodeExecutionToolResultErrorParam | BetaCodeExecutionResultBlockParam`

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

### Beta Code Execution Tool Result Error

- `class BetaCodeExecutionToolResultError`

  - `error_code: BetaCodeExecutionToolResultErrorCode`

    - `:invalid_tool_input`

    - `:unavailable`

    - `:too_many_requests`

    - `:execution_time_exceeded`

  - `type: :code_execution_tool_result_error`

    - `:code_execution_tool_result_error`

### Beta Code Execution Tool Result Error Code

- `BetaCodeExecutionToolResultErrorCode = :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

  - `:invalid_tool_input`

  - `:unavailable`

  - `:too_many_requests`

  - `:execution_time_exceeded`

### Beta Code Execution Tool Result Error Param

- `class BetaCodeExecutionToolResultErrorParam`

  - `error_code: BetaCodeExecutionToolResultErrorCode`

    - `:invalid_tool_input`

    - `:unavailable`

    - `:too_many_requests`

    - `:execution_time_exceeded`

  - `type: :code_execution_tool_result_error`

    - `:code_execution_tool_result_error`

### Beta Container

- `class BetaContainer`

  Information about the container used in the request (for the code execution tool)

  - `id: String`

    Identifier for the container used in this request

  - `expires_at: Time`

    The time at which the container will expire.

  - `skills: Array[BetaSkill]`

    Skills loaded in the container

    - `skill_id: String`

      Skill ID

    - `type: :anthropic | :custom`

      Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

      - `:anthropic`

      - `:custom`

    - `version: String`

      Skill version or 'latest' for most recent version

### Beta Container Params

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

### Beta Container Upload Block

- `class BetaContainerUploadBlock`

  Response model for a file uploaded to the container.

  - `file_id: String`

  - `type: :container_upload`

    - `:container_upload`

### Beta Container Upload Block Param

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

### Beta Content Block

- `BetaContentBlock = BetaTextBlock | BetaThinkingBlock | BetaRedactedThinkingBlock | 11 more`

  Response model for a file uploaded to the container.

  - `class BetaTextBlock`

    - `citations: Array[BetaTextCitation]`

      Citations supporting the text block.

      The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

      - `class BetaCitationCharLocation`

        - `cited_text: String`

        - `document_index: Integer`

        - `document_title: String`

        - `end_char_index: Integer`

        - `file_id: String`

        - `start_char_index: Integer`

        - `type: :char_location`

          - `:char_location`

      - `class BetaCitationPageLocation`

        - `cited_text: String`

        - `document_index: Integer`

        - `document_title: String`

        - `end_page_number: Integer`

        - `file_id: String`

        - `start_page_number: Integer`

        - `type: :page_location`

          - `:page_location`

      - `class BetaCitationContentBlockLocation`

        - `cited_text: String`

        - `document_index: Integer`

        - `document_title: String`

        - `end_block_index: Integer`

        - `file_id: String`

        - `start_block_index: Integer`

        - `type: :content_block_location`

          - `:content_block_location`

      - `class BetaCitationsWebSearchResultLocation`

        - `cited_text: String`

        - `encrypted_index: String`

        - `title: String`

        - `type: :web_search_result_location`

          - `:web_search_result_location`

        - `url: String`

      - `class BetaCitationSearchResultLocation`

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

  - `class BetaThinkingBlock`

    - `signature: String`

    - `thinking: String`

    - `type: :thinking`

      - `:thinking`

  - `class BetaRedactedThinkingBlock`

    - `data: String`

    - `type: :redacted_thinking`

      - `:redacted_thinking`

  - `class BetaToolUseBlock`

    - `id: String`

    - `input: Hash[Symbol, untyped]`

    - `name: String`

    - `type: :tool_use`

      - `:tool_use`

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

  - `class BetaServerToolUseBlock`

    - `id: String`

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

  - `class BetaWebSearchToolResultBlock`

    - `content: BetaWebSearchToolResultBlockContent`

      - `class BetaWebSearchToolResultError`

        - `error_code: BetaWebSearchToolResultErrorCode`

          - `:invalid_tool_input`

          - `:unavailable`

          - `:max_uses_exceeded`

          - `:too_many_requests`

          - `:query_too_long`

        - `type: :web_search_tool_result_error`

          - `:web_search_tool_result_error`

      - `Array[BetaWebSearchResultBlock]`

        - `encrypted_content: String`

        - `page_age: String`

        - `title: String`

        - `type: :web_search_result`

          - `:web_search_result`

        - `url: String`

    - `tool_use_id: String`

    - `type: :web_search_tool_result`

      - `:web_search_tool_result`

  - `class BetaWebFetchToolResultBlock`

    - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

      - `class BetaWebFetchToolResultErrorBlock`

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

      - `class BetaWebFetchBlock`

        - `content: BetaDocumentBlock`

          - `citations: BetaCitationConfig`

            Citation configuration for the document

            - `enabled: bool`

          - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

          - `title: String`

            The title of the document

          - `type: :document`

            - `:document`

        - `retrieved_at: String`

          ISO 8601 timestamp when the content was retrieved

        - `type: :web_fetch_result`

          - `:web_fetch_result`

        - `url: String`

          Fetched content URL

    - `tool_use_id: String`

    - `type: :web_fetch_tool_result`

      - `:web_fetch_tool_result`

  - `class BetaCodeExecutionToolResultBlock`

    - `content: BetaCodeExecutionToolResultBlockContent`

      - `class BetaCodeExecutionToolResultError`

        - `error_code: BetaCodeExecutionToolResultErrorCode`

          - `:invalid_tool_input`

          - `:unavailable`

          - `:too_many_requests`

          - `:execution_time_exceeded`

        - `type: :code_execution_tool_result_error`

          - `:code_execution_tool_result_error`

      - `class BetaCodeExecutionResultBlock`

        - `content: Array[BetaCodeExecutionOutputBlock]`

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

  - `class BetaBashCodeExecutionToolResultBlock`

    - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

      - `class BetaBashCodeExecutionToolResultError`

        - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

          - `:invalid_tool_input`

          - `:unavailable`

          - `:too_many_requests`

          - `:execution_time_exceeded`

          - `:output_file_too_large`

        - `type: :bash_code_execution_tool_result_error`

          - `:bash_code_execution_tool_result_error`

      - `class BetaBashCodeExecutionResultBlock`

        - `content: Array[BetaBashCodeExecutionOutputBlock]`

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

  - `class BetaTextEditorCodeExecutionToolResultBlock`

    - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

      - `class BetaTextEditorCodeExecutionToolResultError`

        - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

          - `:invalid_tool_input`

          - `:unavailable`

          - `:too_many_requests`

          - `:execution_time_exceeded`

          - `:file_not_found`

        - `error_message: String`

        - `type: :text_editor_code_execution_tool_result_error`

          - `:text_editor_code_execution_tool_result_error`

      - `class BetaTextEditorCodeExecutionViewResultBlock`

        - `content: String`

        - `file_type: :text | :image | :pdf`

          - `:text`

          - `:image`

          - `:pdf`

        - `num_lines: Integer`

        - `start_line: Integer`

        - `total_lines: Integer`

        - `type: :text_editor_code_execution_view_result`

          - `:text_editor_code_execution_view_result`

      - `class BetaTextEditorCodeExecutionCreateResultBlock`

        - `is_file_update: bool`

        - `type: :text_editor_code_execution_create_result`

          - `:text_editor_code_execution_create_result`

      - `class BetaTextEditorCodeExecutionStrReplaceResultBlock`

        - `lines: Array[String]`

        - `new_lines: Integer`

        - `new_start: Integer`

        - `old_lines: Integer`

        - `old_start: Integer`

        - `type: :text_editor_code_execution_str_replace_result`

          - `:text_editor_code_execution_str_replace_result`

    - `tool_use_id: String`

    - `type: :text_editor_code_execution_tool_result`

      - `:text_editor_code_execution_tool_result`

  - `class BetaToolSearchToolResultBlock`

    - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

      - `class BetaToolSearchToolResultError`

        - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

          - `:invalid_tool_input`

          - `:unavailable`

          - `:too_many_requests`

          - `:execution_time_exceeded`

        - `error_message: String`

        - `type: :tool_search_tool_result_error`

          - `:tool_search_tool_result_error`

      - `class BetaToolSearchToolSearchResultBlock`

        - `tool_references: Array[BetaToolReferenceBlock]`

          - `tool_name: String`

          - `type: :tool_reference`

            - `:tool_reference`

        - `type: :tool_search_tool_search_result`

          - `:tool_search_tool_search_result`

    - `tool_use_id: String`

    - `type: :tool_search_tool_result`

      - `:tool_search_tool_result`

  - `class BetaMCPToolUseBlock`

    - `id: String`

    - `input: Hash[Symbol, untyped]`

    - `name: String`

      The name of the MCP tool

    - `server_name: String`

      The name of the MCP server

    - `type: :mcp_tool_use`

      - `:mcp_tool_use`

  - `class BetaMCPToolResultBlock`

    - `content: String | Array[BetaTextBlock]`

      - `String`

      - `Array[BetaTextBlock]`

        - `citations: Array[BetaTextCitation]`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `class BetaCitationCharLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_char_index: Integer`

            - `file_id: String`

            - `start_char_index: Integer`

            - `type: :char_location`

              - `:char_location`

          - `class BetaCitationPageLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_page_number: Integer`

            - `file_id: String`

            - `start_page_number: Integer`

            - `type: :page_location`

              - `:page_location`

          - `class BetaCitationContentBlockLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_block_index: Integer`

            - `file_id: String`

            - `start_block_index: Integer`

            - `type: :content_block_location`

              - `:content_block_location`

          - `class BetaCitationsWebSearchResultLocation`

            - `cited_text: String`

            - `encrypted_index: String`

            - `title: String`

            - `type: :web_search_result_location`

              - `:web_search_result_location`

            - `url: String`

          - `class BetaCitationSearchResultLocation`

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

    - `is_error: bool`

    - `tool_use_id: String`

    - `type: :mcp_tool_result`

      - `:mcp_tool_result`

  - `class BetaContainerUploadBlock`

    Response model for a file uploaded to the container.

    - `file_id: String`

    - `type: :container_upload`

      - `:container_upload`

### Beta Content Block Param

- `BetaContentBlockParam = BetaTextBlockParam | BetaImageBlockParam | BetaRequestDocumentBlock | 15 more`

  Regular text content.

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

### Beta Content Block Source

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

### Beta Content Block Source Content

- `BetaContentBlockSourceContent = BetaTextBlockParam | BetaImageBlockParam`

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

### Beta Context Management Config

- `class BetaContextManagementConfig`

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

### Beta Context Management Response

- `class BetaContextManagementResponse`

  - `applied_edits: Array[BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse]`

    List of context management edits that were applied.

    - `class BetaClearToolUses20250919EditResponse`

      - `cleared_input_tokens: Integer`

        Number of input tokens cleared by this edit.

      - `cleared_tool_uses: Integer`

        Number of tool uses that were cleared.

      - `type: :clear_tool_uses_20250919`

        The type of context management edit applied.

        - `:clear_tool_uses_20250919`

    - `class BetaClearThinking20251015EditResponse`

      - `cleared_input_tokens: Integer`

        Number of input tokens cleared by this edit.

      - `cleared_thinking_turns: Integer`

        Number of thinking turns that were cleared.

      - `type: :clear_thinking_20251015`

        The type of context management edit applied.

        - `:clear_thinking_20251015`

### Beta Count Tokens Context Management Response

- `class BetaCountTokensContextManagementResponse`

  - `original_input_tokens: Integer`

    The original token count before context management was applied

### Beta Direct Caller

- `class BetaDirectCaller`

  Tool invocation directly from the model.

  - `type: :direct`

    - `:direct`

### Beta Document Block

- `class BetaDocumentBlock`

  - `citations: BetaCitationConfig`

    Citation configuration for the document

    - `enabled: bool`

  - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

  - `title: String`

    The title of the document

  - `type: :document`

    - `:document`

### Beta File Document Source

- `class BetaFileDocumentSource`

  - `file_id: String`

  - `type: :file`

    - `:file`

### Beta File Image Source

- `class BetaFileImageSource`

  - `file_id: String`

  - `type: :file`

    - `:file`

### Beta Image Block Param

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

### Beta Input JSON Delta

- `class BetaInputJSONDelta`

  - `partial_json: String`

  - `type: :input_json_delta`

    - `:input_json_delta`

### Beta Input Tokens Clear At Least

- `class BetaInputTokensClearAtLeast`

  - `type: :input_tokens`

    - `:input_tokens`

  - `value: Integer`

### Beta Input Tokens Trigger

- `class BetaInputTokensTrigger`

  - `type: :input_tokens`

    - `:input_tokens`

  - `value: Integer`

### Beta JSON Output Format

- `class BetaJSONOutputFormat`

  - `schema: Hash[Symbol, untyped]`

    The JSON schema of the format

  - `type: :json_schema`

    - `:json_schema`

### Beta MCP Tool Config

- `class BetaMCPToolConfig`

  Configuration for a specific tool in an MCP toolset.

  - `defer_loading: bool`

  - `enabled: bool`

### Beta MCP Tool Default Config

- `class BetaMCPToolDefaultConfig`

  Default configuration for tools in an MCP toolset.

  - `defer_loading: bool`

  - `enabled: bool`

### Beta MCP Tool Result Block

- `class BetaMCPToolResultBlock`

  - `content: String | Array[BetaTextBlock]`

    - `String`

    - `Array[BetaTextBlock]`

      - `citations: Array[BetaTextCitation]`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `class BetaCitationCharLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_char_index: Integer`

          - `file_id: String`

          - `start_char_index: Integer`

          - `type: :char_location`

            - `:char_location`

        - `class BetaCitationPageLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_page_number: Integer`

          - `file_id: String`

          - `start_page_number: Integer`

          - `type: :page_location`

            - `:page_location`

        - `class BetaCitationContentBlockLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_block_index: Integer`

          - `file_id: String`

          - `start_block_index: Integer`

          - `type: :content_block_location`

            - `:content_block_location`

        - `class BetaCitationsWebSearchResultLocation`

          - `cited_text: String`

          - `encrypted_index: String`

          - `title: String`

          - `type: :web_search_result_location`

            - `:web_search_result_location`

          - `url: String`

        - `class BetaCitationSearchResultLocation`

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

  - `is_error: bool`

  - `tool_use_id: String`

  - `type: :mcp_tool_result`

    - `:mcp_tool_result`

### Beta MCP Tool Use Block

- `class BetaMCPToolUseBlock`

  - `id: String`

  - `input: Hash[Symbol, untyped]`

  - `name: String`

    The name of the MCP tool

  - `server_name: String`

    The name of the MCP server

  - `type: :mcp_tool_use`

    - `:mcp_tool_use`

### Beta MCP Tool Use Block Param

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

### Beta MCP Toolset

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

### Beta Memory Tool 20250818

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

### Beta Memory Tool 20250818 Command

- `BetaMemoryTool20250818Command = BetaMemoryTool20250818ViewCommand | BetaMemoryTool20250818CreateCommand | BetaMemoryTool20250818StrReplaceCommand | 3 more`

  - `class BetaMemoryTool20250818ViewCommand`

    - `command: :view`

      Command type identifier

      - `:view`

    - `path: String`

      Path to directory or file to view

    - `view_range: Array[Integer]`

      Optional line range for viewing specific lines

  - `class BetaMemoryTool20250818CreateCommand`

    - `command: :create`

      Command type identifier

      - `:create`

    - `file_text: String`

      Content to write to the file

    - `path: String`

      Path where the file should be created

  - `class BetaMemoryTool20250818StrReplaceCommand`

    - `command: :str_replace`

      Command type identifier

      - `:str_replace`

    - `new_str: String`

      Text to replace with

    - `old_str: String`

      Text to search for and replace

    - `path: String`

      Path to the file where text should be replaced

  - `class BetaMemoryTool20250818InsertCommand`

    - `command: :insert`

      Command type identifier

      - `:insert`

    - `insert_line: Integer`

      Line number where text should be inserted

    - `insert_text: String`

      Text to insert at the specified line

    - `path: String`

      Path to the file where text should be inserted

  - `class BetaMemoryTool20250818DeleteCommand`

    - `command: :delete`

      Command type identifier

      - `:delete`

    - `path: String`

      Path to the file or directory to delete

  - `class BetaMemoryTool20250818RenameCommand`

    - `command: :rename`

      Command type identifier

      - `:rename`

    - `new_path: String`

      New path for the file or directory

    - `old_path: String`

      Current path of the file or directory

### Beta Memory Tool 20250818 Create Command

- `class BetaMemoryTool20250818CreateCommand`

  - `command: :create`

    Command type identifier

    - `:create`

  - `file_text: String`

    Content to write to the file

  - `path: String`

    Path where the file should be created

### Beta Memory Tool 20250818 Delete Command

- `class BetaMemoryTool20250818DeleteCommand`

  - `command: :delete`

    Command type identifier

    - `:delete`

  - `path: String`

    Path to the file or directory to delete

### Beta Memory Tool 20250818 Insert Command

- `class BetaMemoryTool20250818InsertCommand`

  - `command: :insert`

    Command type identifier

    - `:insert`

  - `insert_line: Integer`

    Line number where text should be inserted

  - `insert_text: String`

    Text to insert at the specified line

  - `path: String`

    Path to the file where text should be inserted

### Beta Memory Tool 20250818 Rename Command

- `class BetaMemoryTool20250818RenameCommand`

  - `command: :rename`

    Command type identifier

    - `:rename`

  - `new_path: String`

    New path for the file or directory

  - `old_path: String`

    Current path of the file or directory

### Beta Memory Tool 20250818 Str Replace Command

- `class BetaMemoryTool20250818StrReplaceCommand`

  - `command: :str_replace`

    Command type identifier

    - `:str_replace`

  - `new_str: String`

    Text to replace with

  - `old_str: String`

    Text to search for and replace

  - `path: String`

    Path to the file where text should be replaced

### Beta Memory Tool 20250818 View Command

- `class BetaMemoryTool20250818ViewCommand`

  - `command: :view`

    Command type identifier

    - `:view`

  - `path: String`

    Path to directory or file to view

  - `view_range: Array[Integer]`

    Optional line range for viewing specific lines

### Beta Message

- `class BetaMessage`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `container: BetaContainer`

    Information about the container used in the request (for the code execution tool)

    - `id: String`

      Identifier for the container used in this request

    - `expires_at: Time`

      The time at which the container will expire.

    - `skills: Array[BetaSkill]`

      Skills loaded in the container

      - `skill_id: String`

        Skill ID

      - `type: :anthropic | :custom`

        Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

        - `:anthropic`

        - `:custom`

      - `version: String`

        Skill version or 'latest' for most recent version

  - `content: Array[BetaContentBlock]`

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

    - `class BetaTextBlock`

      - `citations: Array[BetaTextCitation]`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `class BetaCitationCharLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_char_index: Integer`

          - `file_id: String`

          - `start_char_index: Integer`

          - `type: :char_location`

            - `:char_location`

        - `class BetaCitationPageLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_page_number: Integer`

          - `file_id: String`

          - `start_page_number: Integer`

          - `type: :page_location`

            - `:page_location`

        - `class BetaCitationContentBlockLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_block_index: Integer`

          - `file_id: String`

          - `start_block_index: Integer`

          - `type: :content_block_location`

            - `:content_block_location`

        - `class BetaCitationsWebSearchResultLocation`

          - `cited_text: String`

          - `encrypted_index: String`

          - `title: String`

          - `type: :web_search_result_location`

            - `:web_search_result_location`

          - `url: String`

        - `class BetaCitationSearchResultLocation`

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

    - `class BetaThinkingBlock`

      - `signature: String`

      - `thinking: String`

      - `type: :thinking`

        - `:thinking`

    - `class BetaRedactedThinkingBlock`

      - `data: String`

      - `type: :redacted_thinking`

        - `:redacted_thinking`

    - `class BetaToolUseBlock`

      - `id: String`

      - `input: Hash[Symbol, untyped]`

      - `name: String`

      - `type: :tool_use`

        - `:tool_use`

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

    - `class BetaServerToolUseBlock`

      - `id: String`

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

    - `class BetaWebSearchToolResultBlock`

      - `content: BetaWebSearchToolResultBlockContent`

        - `class BetaWebSearchToolResultError`

          - `error_code: BetaWebSearchToolResultErrorCode`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:max_uses_exceeded`

            - `:too_many_requests`

            - `:query_too_long`

          - `type: :web_search_tool_result_error`

            - `:web_search_tool_result_error`

        - `Array[BetaWebSearchResultBlock]`

          - `encrypted_content: String`

          - `page_age: String`

          - `title: String`

          - `type: :web_search_result`

            - `:web_search_result`

          - `url: String`

      - `tool_use_id: String`

      - `type: :web_search_tool_result`

        - `:web_search_tool_result`

    - `class BetaWebFetchToolResultBlock`

      - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

        - `class BetaWebFetchToolResultErrorBlock`

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

        - `class BetaWebFetchBlock`

          - `content: BetaDocumentBlock`

            - `citations: BetaCitationConfig`

              Citation configuration for the document

              - `enabled: bool`

            - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

            - `title: String`

              The title of the document

            - `type: :document`

              - `:document`

          - `retrieved_at: String`

            ISO 8601 timestamp when the content was retrieved

          - `type: :web_fetch_result`

            - `:web_fetch_result`

          - `url: String`

            Fetched content URL

      - `tool_use_id: String`

      - `type: :web_fetch_tool_result`

        - `:web_fetch_tool_result`

    - `class BetaCodeExecutionToolResultBlock`

      - `content: BetaCodeExecutionToolResultBlockContent`

        - `class BetaCodeExecutionToolResultError`

          - `error_code: BetaCodeExecutionToolResultErrorCode`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:too_many_requests`

            - `:execution_time_exceeded`

          - `type: :code_execution_tool_result_error`

            - `:code_execution_tool_result_error`

        - `class BetaCodeExecutionResultBlock`

          - `content: Array[BetaCodeExecutionOutputBlock]`

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

    - `class BetaBashCodeExecutionToolResultBlock`

      - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

        - `class BetaBashCodeExecutionToolResultError`

          - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:too_many_requests`

            - `:execution_time_exceeded`

            - `:output_file_too_large`

          - `type: :bash_code_execution_tool_result_error`

            - `:bash_code_execution_tool_result_error`

        - `class BetaBashCodeExecutionResultBlock`

          - `content: Array[BetaBashCodeExecutionOutputBlock]`

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

    - `class BetaTextEditorCodeExecutionToolResultBlock`

      - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

        - `class BetaTextEditorCodeExecutionToolResultError`

          - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:too_many_requests`

            - `:execution_time_exceeded`

            - `:file_not_found`

          - `error_message: String`

          - `type: :text_editor_code_execution_tool_result_error`

            - `:text_editor_code_execution_tool_result_error`

        - `class BetaTextEditorCodeExecutionViewResultBlock`

          - `content: String`

          - `file_type: :text | :image | :pdf`

            - `:text`

            - `:image`

            - `:pdf`

          - `num_lines: Integer`

          - `start_line: Integer`

          - `total_lines: Integer`

          - `type: :text_editor_code_execution_view_result`

            - `:text_editor_code_execution_view_result`

        - `class BetaTextEditorCodeExecutionCreateResultBlock`

          - `is_file_update: bool`

          - `type: :text_editor_code_execution_create_result`

            - `:text_editor_code_execution_create_result`

        - `class BetaTextEditorCodeExecutionStrReplaceResultBlock`

          - `lines: Array[String]`

          - `new_lines: Integer`

          - `new_start: Integer`

          - `old_lines: Integer`

          - `old_start: Integer`

          - `type: :text_editor_code_execution_str_replace_result`

            - `:text_editor_code_execution_str_replace_result`

      - `tool_use_id: String`

      - `type: :text_editor_code_execution_tool_result`

        - `:text_editor_code_execution_tool_result`

    - `class BetaToolSearchToolResultBlock`

      - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

        - `class BetaToolSearchToolResultError`

          - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:too_many_requests`

            - `:execution_time_exceeded`

          - `error_message: String`

          - `type: :tool_search_tool_result_error`

            - `:tool_search_tool_result_error`

        - `class BetaToolSearchToolSearchResultBlock`

          - `tool_references: Array[BetaToolReferenceBlock]`

            - `tool_name: String`

            - `type: :tool_reference`

              - `:tool_reference`

          - `type: :tool_search_tool_search_result`

            - `:tool_search_tool_search_result`

      - `tool_use_id: String`

      - `type: :tool_search_tool_result`

        - `:tool_search_tool_result`

    - `class BetaMCPToolUseBlock`

      - `id: String`

      - `input: Hash[Symbol, untyped]`

      - `name: String`

        The name of the MCP tool

      - `server_name: String`

        The name of the MCP server

      - `type: :mcp_tool_use`

        - `:mcp_tool_use`

    - `class BetaMCPToolResultBlock`

      - `content: String | Array[BetaTextBlock]`

        - `String`

        - `Array[BetaTextBlock]`

          - `citations: Array[BetaTextCitation]`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `class BetaCitationCharLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_char_index: Integer`

              - `file_id: String`

              - `start_char_index: Integer`

              - `type: :char_location`

                - `:char_location`

            - `class BetaCitationPageLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_page_number: Integer`

              - `file_id: String`

              - `start_page_number: Integer`

              - `type: :page_location`

                - `:page_location`

            - `class BetaCitationContentBlockLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_block_index: Integer`

              - `file_id: String`

              - `start_block_index: Integer`

              - `type: :content_block_location`

                - `:content_block_location`

            - `class BetaCitationsWebSearchResultLocation`

              - `cited_text: String`

              - `encrypted_index: String`

              - `title: String`

              - `type: :web_search_result_location`

                - `:web_search_result_location`

              - `url: String`

            - `class BetaCitationSearchResultLocation`

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

      - `is_error: bool`

      - `tool_use_id: String`

      - `type: :mcp_tool_result`

        - `:mcp_tool_result`

    - `class BetaContainerUploadBlock`

      Response model for a file uploaded to the container.

      - `file_id: String`

      - `type: :container_upload`

        - `:container_upload`

  - `context_management: BetaContextManagementResponse`

    Context management response.

    Information about context management strategies applied during the request.

    - `applied_edits: Array[BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse]`

      List of context management edits that were applied.

      - `class BetaClearToolUses20250919EditResponse`

        - `cleared_input_tokens: Integer`

          Number of input tokens cleared by this edit.

        - `cleared_tool_uses: Integer`

          Number of tool uses that were cleared.

        - `type: :clear_tool_uses_20250919`

          The type of context management edit applied.

          - `:clear_tool_uses_20250919`

      - `class BetaClearThinking20251015EditResponse`

        - `cleared_input_tokens: Integer`

          Number of input tokens cleared by this edit.

        - `cleared_thinking_turns: Integer`

          Number of thinking turns that were cleared.

        - `type: :clear_thinking_20251015`

          The type of context management edit applied.

          - `:clear_thinking_20251015`

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

  - `stop_reason: BetaStopReason`

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

    - `:model_context_window_exceeded`

  - `stop_sequence: String`

    Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was generated.

  - `type: :message`

    Object type.

    For Messages, this is always `"message"`.

    - `:message`

  - `usage: BetaUsage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cache_creation: BetaCacheCreation`

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

    - `server_tool_use: BetaServerToolUsage`

      The number of server tool requests.

      - `web_fetch_requests: Integer`

        The number of web fetch tool requests.

      - `web_search_requests: Integer`

        The number of web search tool requests.

    - `service_tier: :standard | :priority | :batch`

      If the request used the priority, standard, or batch tier.

      - `:standard`

      - `:priority`

      - `:batch`

### Beta Message Delta Usage

- `class BetaMessageDeltaUsage`

  - `cache_creation_input_tokens: Integer`

    The cumulative number of input tokens used to create the cache entry.

  - `cache_read_input_tokens: Integer`

    The cumulative number of input tokens read from the cache.

  - `input_tokens: Integer`

    The cumulative number of input tokens which were used.

  - `output_tokens: Integer`

    The cumulative number of output tokens which were used.

  - `server_tool_use: BetaServerToolUsage`

    The number of server tool requests.

    - `web_fetch_requests: Integer`

      The number of web fetch tool requests.

    - `web_search_requests: Integer`

      The number of web search tool requests.

### Beta Message Param

- `class BetaMessageParam`

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

### Beta Message Tokens Count

- `class BetaMessageTokensCount`

  - `context_management: BetaCountTokensContextManagementResponse`

    Information about context management applied to the message.

    - `original_input_tokens: Integer`

      The original token count before context management was applied

  - `input_tokens: Integer`

    The total number of tokens across the provided list of messages, system prompt, and tools.

### Beta Metadata

- `class BetaMetadata`

  - `user_id: String`

    An external identifier for the user who is associated with the request.

    This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

### Beta Output Config

- `class BetaOutputConfig`

  - `effort: :low | :medium | :high`

    All possible effort levels.

    - `:low`

    - `:medium`

    - `:high`

### Beta Plain Text Source

- `class BetaPlainTextSource`

  - `data: String`

  - `media_type: :"text/plain"`

    - `:"text/plain"`

  - `type: :text`

    - `:text`

### Beta Raw Content Block Delta

- `BetaRawContentBlockDelta = BetaTextDelta | BetaInputJSONDelta | BetaCitationsDelta | 2 more`

  - `class BetaTextDelta`

    - `text: String`

    - `type: :text_delta`

      - `:text_delta`

  - `class BetaInputJSONDelta`

    - `partial_json: String`

    - `type: :input_json_delta`

      - `:input_json_delta`

  - `class BetaCitationsDelta`

    - `citation: BetaCitationCharLocation | BetaCitationPageLocation | BetaCitationContentBlockLocation | 2 more`

      - `class BetaCitationCharLocation`

        - `cited_text: String`

        - `document_index: Integer`

        - `document_title: String`

        - `end_char_index: Integer`

        - `file_id: String`

        - `start_char_index: Integer`

        - `type: :char_location`

          - `:char_location`

      - `class BetaCitationPageLocation`

        - `cited_text: String`

        - `document_index: Integer`

        - `document_title: String`

        - `end_page_number: Integer`

        - `file_id: String`

        - `start_page_number: Integer`

        - `type: :page_location`

          - `:page_location`

      - `class BetaCitationContentBlockLocation`

        - `cited_text: String`

        - `document_index: Integer`

        - `document_title: String`

        - `end_block_index: Integer`

        - `file_id: String`

        - `start_block_index: Integer`

        - `type: :content_block_location`

          - `:content_block_location`

      - `class BetaCitationsWebSearchResultLocation`

        - `cited_text: String`

        - `encrypted_index: String`

        - `title: String`

        - `type: :web_search_result_location`

          - `:web_search_result_location`

        - `url: String`

      - `class BetaCitationSearchResultLocation`

        - `cited_text: String`

        - `end_block_index: Integer`

        - `search_result_index: Integer`

        - `source: String`

        - `start_block_index: Integer`

        - `title: String`

        - `type: :search_result_location`

          - `:search_result_location`

    - `type: :citations_delta`

      - `:citations_delta`

  - `class BetaThinkingDelta`

    - `thinking: String`

    - `type: :thinking_delta`

      - `:thinking_delta`

  - `class BetaSignatureDelta`

    - `signature: String`

    - `type: :signature_delta`

      - `:signature_delta`

### Beta Raw Content Block Delta Event

- `class BetaRawContentBlockDeltaEvent`

  - `delta: BetaRawContentBlockDelta`

    - `class BetaTextDelta`

      - `text: String`

      - `type: :text_delta`

        - `:text_delta`

    - `class BetaInputJSONDelta`

      - `partial_json: String`

      - `type: :input_json_delta`

        - `:input_json_delta`

    - `class BetaCitationsDelta`

      - `citation: BetaCitationCharLocation | BetaCitationPageLocation | BetaCitationContentBlockLocation | 2 more`

        - `class BetaCitationCharLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_char_index: Integer`

          - `file_id: String`

          - `start_char_index: Integer`

          - `type: :char_location`

            - `:char_location`

        - `class BetaCitationPageLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_page_number: Integer`

          - `file_id: String`

          - `start_page_number: Integer`

          - `type: :page_location`

            - `:page_location`

        - `class BetaCitationContentBlockLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_block_index: Integer`

          - `file_id: String`

          - `start_block_index: Integer`

          - `type: :content_block_location`

            - `:content_block_location`

        - `class BetaCitationsWebSearchResultLocation`

          - `cited_text: String`

          - `encrypted_index: String`

          - `title: String`

          - `type: :web_search_result_location`

            - `:web_search_result_location`

          - `url: String`

        - `class BetaCitationSearchResultLocation`

          - `cited_text: String`

          - `end_block_index: Integer`

          - `search_result_index: Integer`

          - `source: String`

          - `start_block_index: Integer`

          - `title: String`

          - `type: :search_result_location`

            - `:search_result_location`

      - `type: :citations_delta`

        - `:citations_delta`

    - `class BetaThinkingDelta`

      - `thinking: String`

      - `type: :thinking_delta`

        - `:thinking_delta`

    - `class BetaSignatureDelta`

      - `signature: String`

      - `type: :signature_delta`

        - `:signature_delta`

  - `index: Integer`

  - `type: :content_block_delta`

    - `:content_block_delta`

### Beta Raw Content Block Start Event

- `class BetaRawContentBlockStartEvent`

  - `content_block: BetaTextBlock | BetaThinkingBlock | BetaRedactedThinkingBlock | 11 more`

    Response model for a file uploaded to the container.

    - `class BetaTextBlock`

      - `citations: Array[BetaTextCitation]`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `class BetaCitationCharLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_char_index: Integer`

          - `file_id: String`

          - `start_char_index: Integer`

          - `type: :char_location`

            - `:char_location`

        - `class BetaCitationPageLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_page_number: Integer`

          - `file_id: String`

          - `start_page_number: Integer`

          - `type: :page_location`

            - `:page_location`

        - `class BetaCitationContentBlockLocation`

          - `cited_text: String`

          - `document_index: Integer`

          - `document_title: String`

          - `end_block_index: Integer`

          - `file_id: String`

          - `start_block_index: Integer`

          - `type: :content_block_location`

            - `:content_block_location`

        - `class BetaCitationsWebSearchResultLocation`

          - `cited_text: String`

          - `encrypted_index: String`

          - `title: String`

          - `type: :web_search_result_location`

            - `:web_search_result_location`

          - `url: String`

        - `class BetaCitationSearchResultLocation`

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

    - `class BetaThinkingBlock`

      - `signature: String`

      - `thinking: String`

      - `type: :thinking`

        - `:thinking`

    - `class BetaRedactedThinkingBlock`

      - `data: String`

      - `type: :redacted_thinking`

        - `:redacted_thinking`

    - `class BetaToolUseBlock`

      - `id: String`

      - `input: Hash[Symbol, untyped]`

      - `name: String`

      - `type: :tool_use`

        - `:tool_use`

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

    - `class BetaServerToolUseBlock`

      - `id: String`

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

    - `class BetaWebSearchToolResultBlock`

      - `content: BetaWebSearchToolResultBlockContent`

        - `class BetaWebSearchToolResultError`

          - `error_code: BetaWebSearchToolResultErrorCode`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:max_uses_exceeded`

            - `:too_many_requests`

            - `:query_too_long`

          - `type: :web_search_tool_result_error`

            - `:web_search_tool_result_error`

        - `Array[BetaWebSearchResultBlock]`

          - `encrypted_content: String`

          - `page_age: String`

          - `title: String`

          - `type: :web_search_result`

            - `:web_search_result`

          - `url: String`

      - `tool_use_id: String`

      - `type: :web_search_tool_result`

        - `:web_search_tool_result`

    - `class BetaWebFetchToolResultBlock`

      - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

        - `class BetaWebFetchToolResultErrorBlock`

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

        - `class BetaWebFetchBlock`

          - `content: BetaDocumentBlock`

            - `citations: BetaCitationConfig`

              Citation configuration for the document

              - `enabled: bool`

            - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

            - `title: String`

              The title of the document

            - `type: :document`

              - `:document`

          - `retrieved_at: String`

            ISO 8601 timestamp when the content was retrieved

          - `type: :web_fetch_result`

            - `:web_fetch_result`

          - `url: String`

            Fetched content URL

      - `tool_use_id: String`

      - `type: :web_fetch_tool_result`

        - `:web_fetch_tool_result`

    - `class BetaCodeExecutionToolResultBlock`

      - `content: BetaCodeExecutionToolResultBlockContent`

        - `class BetaCodeExecutionToolResultError`

          - `error_code: BetaCodeExecutionToolResultErrorCode`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:too_many_requests`

            - `:execution_time_exceeded`

          - `type: :code_execution_tool_result_error`

            - `:code_execution_tool_result_error`

        - `class BetaCodeExecutionResultBlock`

          - `content: Array[BetaCodeExecutionOutputBlock]`

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

    - `class BetaBashCodeExecutionToolResultBlock`

      - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

        - `class BetaBashCodeExecutionToolResultError`

          - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:too_many_requests`

            - `:execution_time_exceeded`

            - `:output_file_too_large`

          - `type: :bash_code_execution_tool_result_error`

            - `:bash_code_execution_tool_result_error`

        - `class BetaBashCodeExecutionResultBlock`

          - `content: Array[BetaBashCodeExecutionOutputBlock]`

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

    - `class BetaTextEditorCodeExecutionToolResultBlock`

      - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

        - `class BetaTextEditorCodeExecutionToolResultError`

          - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:too_many_requests`

            - `:execution_time_exceeded`

            - `:file_not_found`

          - `error_message: String`

          - `type: :text_editor_code_execution_tool_result_error`

            - `:text_editor_code_execution_tool_result_error`

        - `class BetaTextEditorCodeExecutionViewResultBlock`

          - `content: String`

          - `file_type: :text | :image | :pdf`

            - `:text`

            - `:image`

            - `:pdf`

          - `num_lines: Integer`

          - `start_line: Integer`

          - `total_lines: Integer`

          - `type: :text_editor_code_execution_view_result`

            - `:text_editor_code_execution_view_result`

        - `class BetaTextEditorCodeExecutionCreateResultBlock`

          - `is_file_update: bool`

          - `type: :text_editor_code_execution_create_result`

            - `:text_editor_code_execution_create_result`

        - `class BetaTextEditorCodeExecutionStrReplaceResultBlock`

          - `lines: Array[String]`

          - `new_lines: Integer`

          - `new_start: Integer`

          - `old_lines: Integer`

          - `old_start: Integer`

          - `type: :text_editor_code_execution_str_replace_result`

            - `:text_editor_code_execution_str_replace_result`

      - `tool_use_id: String`

      - `type: :text_editor_code_execution_tool_result`

        - `:text_editor_code_execution_tool_result`

    - `class BetaToolSearchToolResultBlock`

      - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

        - `class BetaToolSearchToolResultError`

          - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

            - `:invalid_tool_input`

            - `:unavailable`

            - `:too_many_requests`

            - `:execution_time_exceeded`

          - `error_message: String`

          - `type: :tool_search_tool_result_error`

            - `:tool_search_tool_result_error`

        - `class BetaToolSearchToolSearchResultBlock`

          - `tool_references: Array[BetaToolReferenceBlock]`

            - `tool_name: String`

            - `type: :tool_reference`

              - `:tool_reference`

          - `type: :tool_search_tool_search_result`

            - `:tool_search_tool_search_result`

      - `tool_use_id: String`

      - `type: :tool_search_tool_result`

        - `:tool_search_tool_result`

    - `class BetaMCPToolUseBlock`

      - `id: String`

      - `input: Hash[Symbol, untyped]`

      - `name: String`

        The name of the MCP tool

      - `server_name: String`

        The name of the MCP server

      - `type: :mcp_tool_use`

        - `:mcp_tool_use`

    - `class BetaMCPToolResultBlock`

      - `content: String | Array[BetaTextBlock]`

        - `String`

        - `Array[BetaTextBlock]`

          - `citations: Array[BetaTextCitation]`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `class BetaCitationCharLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_char_index: Integer`

              - `file_id: String`

              - `start_char_index: Integer`

              - `type: :char_location`

                - `:char_location`

            - `class BetaCitationPageLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_page_number: Integer`

              - `file_id: String`

              - `start_page_number: Integer`

              - `type: :page_location`

                - `:page_location`

            - `class BetaCitationContentBlockLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_block_index: Integer`

              - `file_id: String`

              - `start_block_index: Integer`

              - `type: :content_block_location`

                - `:content_block_location`

            - `class BetaCitationsWebSearchResultLocation`

              - `cited_text: String`

              - `encrypted_index: String`

              - `title: String`

              - `type: :web_search_result_location`

                - `:web_search_result_location`

              - `url: String`

            - `class BetaCitationSearchResultLocation`

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

      - `is_error: bool`

      - `tool_use_id: String`

      - `type: :mcp_tool_result`

        - `:mcp_tool_result`

    - `class BetaContainerUploadBlock`

      Response model for a file uploaded to the container.

      - `file_id: String`

      - `type: :container_upload`

        - `:container_upload`

  - `index: Integer`

  - `type: :content_block_start`

    - `:content_block_start`

### Beta Raw Content Block Stop Event

- `class BetaRawContentBlockStopEvent`

  - `index: Integer`

  - `type: :content_block_stop`

    - `:content_block_stop`

### Beta Raw Message Delta Event

- `class BetaRawMessageDeltaEvent`

  - `context_management: BetaContextManagementResponse`

    Information about context management strategies applied during the request

    - `applied_edits: Array[BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse]`

      List of context management edits that were applied.

      - `class BetaClearToolUses20250919EditResponse`

        - `cleared_input_tokens: Integer`

          Number of input tokens cleared by this edit.

        - `cleared_tool_uses: Integer`

          Number of tool uses that were cleared.

        - `type: :clear_tool_uses_20250919`

          The type of context management edit applied.

          - `:clear_tool_uses_20250919`

      - `class BetaClearThinking20251015EditResponse`

        - `cleared_input_tokens: Integer`

          Number of input tokens cleared by this edit.

        - `cleared_thinking_turns: Integer`

          Number of thinking turns that were cleared.

        - `type: :clear_thinking_20251015`

          The type of context management edit applied.

          - `:clear_thinking_20251015`

  - `delta: { container, stop_reason, stop_sequence}`

    - `container: BetaContainer`

      Information about the container used in the request (for the code execution tool)

      - `id: String`

        Identifier for the container used in this request

      - `expires_at: Time`

        The time at which the container will expire.

      - `skills: Array[BetaSkill]`

        Skills loaded in the container

        - `skill_id: String`

          Skill ID

        - `type: :anthropic | :custom`

          Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

          - `:anthropic`

          - `:custom`

        - `version: String`

          Skill version or 'latest' for most recent version

    - `stop_reason: BetaStopReason`

      - `:end_turn`

      - `:max_tokens`

      - `:stop_sequence`

      - `:tool_use`

      - `:pause_turn`

      - `:refusal`

      - `:model_context_window_exceeded`

    - `stop_sequence: String`

  - `type: :message_delta`

    - `:message_delta`

  - `usage: BetaMessageDeltaUsage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cache_creation_input_tokens: Integer`

      The cumulative number of input tokens used to create the cache entry.

    - `cache_read_input_tokens: Integer`

      The cumulative number of input tokens read from the cache.

    - `input_tokens: Integer`

      The cumulative number of input tokens which were used.

    - `output_tokens: Integer`

      The cumulative number of output tokens which were used.

    - `server_tool_use: BetaServerToolUsage`

      The number of server tool requests.

      - `web_fetch_requests: Integer`

        The number of web fetch tool requests.

      - `web_search_requests: Integer`

        The number of web search tool requests.

### Beta Raw Message Start Event

- `class BetaRawMessageStartEvent`

  - `message: BetaMessage`

    - `id: String`

      Unique object identifier.

      The format and length of IDs may change over time.

    - `container: BetaContainer`

      Information about the container used in the request (for the code execution tool)

      - `id: String`

        Identifier for the container used in this request

      - `expires_at: Time`

        The time at which the container will expire.

      - `skills: Array[BetaSkill]`

        Skills loaded in the container

        - `skill_id: String`

          Skill ID

        - `type: :anthropic | :custom`

          Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

          - `:anthropic`

          - `:custom`

        - `version: String`

          Skill version or 'latest' for most recent version

    - `content: Array[BetaContentBlock]`

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

      - `class BetaTextBlock`

        - `citations: Array[BetaTextCitation]`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `class BetaCitationCharLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_char_index: Integer`

            - `file_id: String`

            - `start_char_index: Integer`

            - `type: :char_location`

              - `:char_location`

          - `class BetaCitationPageLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_page_number: Integer`

            - `file_id: String`

            - `start_page_number: Integer`

            - `type: :page_location`

              - `:page_location`

          - `class BetaCitationContentBlockLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_block_index: Integer`

            - `file_id: String`

            - `start_block_index: Integer`

            - `type: :content_block_location`

              - `:content_block_location`

          - `class BetaCitationsWebSearchResultLocation`

            - `cited_text: String`

            - `encrypted_index: String`

            - `title: String`

            - `type: :web_search_result_location`

              - `:web_search_result_location`

            - `url: String`

          - `class BetaCitationSearchResultLocation`

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

      - `class BetaThinkingBlock`

        - `signature: String`

        - `thinking: String`

        - `type: :thinking`

          - `:thinking`

      - `class BetaRedactedThinkingBlock`

        - `data: String`

        - `type: :redacted_thinking`

          - `:redacted_thinking`

      - `class BetaToolUseBlock`

        - `id: String`

        - `input: Hash[Symbol, untyped]`

        - `name: String`

        - `type: :tool_use`

          - `:tool_use`

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

      - `class BetaServerToolUseBlock`

        - `id: String`

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

      - `class BetaWebSearchToolResultBlock`

        - `content: BetaWebSearchToolResultBlockContent`

          - `class BetaWebSearchToolResultError`

            - `error_code: BetaWebSearchToolResultErrorCode`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:max_uses_exceeded`

              - `:too_many_requests`

              - `:query_too_long`

            - `type: :web_search_tool_result_error`

              - `:web_search_tool_result_error`

          - `Array[BetaWebSearchResultBlock]`

            - `encrypted_content: String`

            - `page_age: String`

            - `title: String`

            - `type: :web_search_result`

              - `:web_search_result`

            - `url: String`

        - `tool_use_id: String`

        - `type: :web_search_tool_result`

          - `:web_search_tool_result`

      - `class BetaWebFetchToolResultBlock`

        - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

          - `class BetaWebFetchToolResultErrorBlock`

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

          - `class BetaWebFetchBlock`

            - `content: BetaDocumentBlock`

              - `citations: BetaCitationConfig`

                Citation configuration for the document

                - `enabled: bool`

              - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

              - `title: String`

                The title of the document

              - `type: :document`

                - `:document`

            - `retrieved_at: String`

              ISO 8601 timestamp when the content was retrieved

            - `type: :web_fetch_result`

              - `:web_fetch_result`

            - `url: String`

              Fetched content URL

        - `tool_use_id: String`

        - `type: :web_fetch_tool_result`

          - `:web_fetch_tool_result`

      - `class BetaCodeExecutionToolResultBlock`

        - `content: BetaCodeExecutionToolResultBlockContent`

          - `class BetaCodeExecutionToolResultError`

            - `error_code: BetaCodeExecutionToolResultErrorCode`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:too_many_requests`

              - `:execution_time_exceeded`

            - `type: :code_execution_tool_result_error`

              - `:code_execution_tool_result_error`

          - `class BetaCodeExecutionResultBlock`

            - `content: Array[BetaCodeExecutionOutputBlock]`

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

      - `class BetaBashCodeExecutionToolResultBlock`

        - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

          - `class BetaBashCodeExecutionToolResultError`

            - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:too_many_requests`

              - `:execution_time_exceeded`

              - `:output_file_too_large`

            - `type: :bash_code_execution_tool_result_error`

              - `:bash_code_execution_tool_result_error`

          - `class BetaBashCodeExecutionResultBlock`

            - `content: Array[BetaBashCodeExecutionOutputBlock]`

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

      - `class BetaTextEditorCodeExecutionToolResultBlock`

        - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

          - `class BetaTextEditorCodeExecutionToolResultError`

            - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:too_many_requests`

              - `:execution_time_exceeded`

              - `:file_not_found`

            - `error_message: String`

            - `type: :text_editor_code_execution_tool_result_error`

              - `:text_editor_code_execution_tool_result_error`

          - `class BetaTextEditorCodeExecutionViewResultBlock`

            - `content: String`

            - `file_type: :text | :image | :pdf`

              - `:text`

              - `:image`

              - `:pdf`

            - `num_lines: Integer`

            - `start_line: Integer`

            - `total_lines: Integer`

            - `type: :text_editor_code_execution_view_result`

              - `:text_editor_code_execution_view_result`

          - `class BetaTextEditorCodeExecutionCreateResultBlock`

            - `is_file_update: bool`

            - `type: :text_editor_code_execution_create_result`

              - `:text_editor_code_execution_create_result`

          - `class BetaTextEditorCodeExecutionStrReplaceResultBlock`

            - `lines: Array[String]`

            - `new_lines: Integer`

            - `new_start: Integer`

            - `old_lines: Integer`

            - `old_start: Integer`

            - `type: :text_editor_code_execution_str_replace_result`

              - `:text_editor_code_execution_str_replace_result`

        - `tool_use_id: String`

        - `type: :text_editor_code_execution_tool_result`

          - `:text_editor_code_execution_tool_result`

      - `class BetaToolSearchToolResultBlock`

        - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

          - `class BetaToolSearchToolResultError`

            - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:too_many_requests`

              - `:execution_time_exceeded`

            - `error_message: String`

            - `type: :tool_search_tool_result_error`

              - `:tool_search_tool_result_error`

          - `class BetaToolSearchToolSearchResultBlock`

            - `tool_references: Array[BetaToolReferenceBlock]`

              - `tool_name: String`

              - `type: :tool_reference`

                - `:tool_reference`

            - `type: :tool_search_tool_search_result`

              - `:tool_search_tool_search_result`

        - `tool_use_id: String`

        - `type: :tool_search_tool_result`

          - `:tool_search_tool_result`

      - `class BetaMCPToolUseBlock`

        - `id: String`

        - `input: Hash[Symbol, untyped]`

        - `name: String`

          The name of the MCP tool

        - `server_name: String`

          The name of the MCP server

        - `type: :mcp_tool_use`

          - `:mcp_tool_use`

      - `class BetaMCPToolResultBlock`

        - `content: String | Array[BetaTextBlock]`

          - `String`

          - `Array[BetaTextBlock]`

            - `citations: Array[BetaTextCitation]`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class BetaCitationCharLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_char_index: Integer`

                - `file_id: String`

                - `start_char_index: Integer`

                - `type: :char_location`

                  - `:char_location`

              - `class BetaCitationPageLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_page_number: Integer`

                - `file_id: String`

                - `start_page_number: Integer`

                - `type: :page_location`

                  - `:page_location`

              - `class BetaCitationContentBlockLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_block_index: Integer`

                - `file_id: String`

                - `start_block_index: Integer`

                - `type: :content_block_location`

                  - `:content_block_location`

              - `class BetaCitationsWebSearchResultLocation`

                - `cited_text: String`

                - `encrypted_index: String`

                - `title: String`

                - `type: :web_search_result_location`

                  - `:web_search_result_location`

                - `url: String`

              - `class BetaCitationSearchResultLocation`

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

        - `is_error: bool`

        - `tool_use_id: String`

        - `type: :mcp_tool_result`

          - `:mcp_tool_result`

      - `class BetaContainerUploadBlock`

        Response model for a file uploaded to the container.

        - `file_id: String`

        - `type: :container_upload`

          - `:container_upload`

    - `context_management: BetaContextManagementResponse`

      Context management response.

      Information about context management strategies applied during the request.

      - `applied_edits: Array[BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse]`

        List of context management edits that were applied.

        - `class BetaClearToolUses20250919EditResponse`

          - `cleared_input_tokens: Integer`

            Number of input tokens cleared by this edit.

          - `cleared_tool_uses: Integer`

            Number of tool uses that were cleared.

          - `type: :clear_tool_uses_20250919`

            The type of context management edit applied.

            - `:clear_tool_uses_20250919`

        - `class BetaClearThinking20251015EditResponse`

          - `cleared_input_tokens: Integer`

            Number of input tokens cleared by this edit.

          - `cleared_thinking_turns: Integer`

            Number of thinking turns that were cleared.

          - `type: :clear_thinking_20251015`

            The type of context management edit applied.

            - `:clear_thinking_20251015`

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

    - `stop_reason: BetaStopReason`

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

      - `:model_context_window_exceeded`

    - `stop_sequence: String`

      Which custom stop sequence was generated, if any.

      This value will be a non-null string if one of your custom stop sequences was generated.

    - `type: :message`

      Object type.

      For Messages, this is always `"message"`.

      - `:message`

    - `usage: BetaUsage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cache_creation: BetaCacheCreation`

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

      - `server_tool_use: BetaServerToolUsage`

        The number of server tool requests.

        - `web_fetch_requests: Integer`

          The number of web fetch tool requests.

        - `web_search_requests: Integer`

          The number of web search tool requests.

      - `service_tier: :standard | :priority | :batch`

        If the request used the priority, standard, or batch tier.

        - `:standard`

        - `:priority`

        - `:batch`

  - `type: :message_start`

    - `:message_start`

### Beta Raw Message Stop Event

- `class BetaRawMessageStopEvent`

  - `type: :message_stop`

    - `:message_stop`

### Beta Raw Message Stream Event

- `BetaRawMessageStreamEvent = BetaRawMessageStartEvent | BetaRawMessageDeltaEvent | BetaRawMessageStopEvent | 3 more`

  - `class BetaRawMessageStartEvent`

    - `message: BetaMessage`

      - `id: String`

        Unique object identifier.

        The format and length of IDs may change over time.

      - `container: BetaContainer`

        Information about the container used in the request (for the code execution tool)

        - `id: String`

          Identifier for the container used in this request

        - `expires_at: Time`

          The time at which the container will expire.

        - `skills: Array[BetaSkill]`

          Skills loaded in the container

          - `skill_id: String`

            Skill ID

          - `type: :anthropic | :custom`

            Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

            - `:anthropic`

            - `:custom`

          - `version: String`

            Skill version or 'latest' for most recent version

      - `content: Array[BetaContentBlock]`

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

        - `class BetaTextBlock`

          - `citations: Array[BetaTextCitation]`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `class BetaCitationCharLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_char_index: Integer`

              - `file_id: String`

              - `start_char_index: Integer`

              - `type: :char_location`

                - `:char_location`

            - `class BetaCitationPageLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_page_number: Integer`

              - `file_id: String`

              - `start_page_number: Integer`

              - `type: :page_location`

                - `:page_location`

            - `class BetaCitationContentBlockLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_block_index: Integer`

              - `file_id: String`

              - `start_block_index: Integer`

              - `type: :content_block_location`

                - `:content_block_location`

            - `class BetaCitationsWebSearchResultLocation`

              - `cited_text: String`

              - `encrypted_index: String`

              - `title: String`

              - `type: :web_search_result_location`

                - `:web_search_result_location`

              - `url: String`

            - `class BetaCitationSearchResultLocation`

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

        - `class BetaThinkingBlock`

          - `signature: String`

          - `thinking: String`

          - `type: :thinking`

            - `:thinking`

        - `class BetaRedactedThinkingBlock`

          - `data: String`

          - `type: :redacted_thinking`

            - `:redacted_thinking`

        - `class BetaToolUseBlock`

          - `id: String`

          - `input: Hash[Symbol, untyped]`

          - `name: String`

          - `type: :tool_use`

            - `:tool_use`

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

        - `class BetaServerToolUseBlock`

          - `id: String`

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

        - `class BetaWebSearchToolResultBlock`

          - `content: BetaWebSearchToolResultBlockContent`

            - `class BetaWebSearchToolResultError`

              - `error_code: BetaWebSearchToolResultErrorCode`

                - `:invalid_tool_input`

                - `:unavailable`

                - `:max_uses_exceeded`

                - `:too_many_requests`

                - `:query_too_long`

              - `type: :web_search_tool_result_error`

                - `:web_search_tool_result_error`

            - `Array[BetaWebSearchResultBlock]`

              - `encrypted_content: String`

              - `page_age: String`

              - `title: String`

              - `type: :web_search_result`

                - `:web_search_result`

              - `url: String`

          - `tool_use_id: String`

          - `type: :web_search_tool_result`

            - `:web_search_tool_result`

        - `class BetaWebFetchToolResultBlock`

          - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

            - `class BetaWebFetchToolResultErrorBlock`

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

            - `class BetaWebFetchBlock`

              - `content: BetaDocumentBlock`

                - `citations: BetaCitationConfig`

                  Citation configuration for the document

                  - `enabled: bool`

                - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

                - `title: String`

                  The title of the document

                - `type: :document`

                  - `:document`

              - `retrieved_at: String`

                ISO 8601 timestamp when the content was retrieved

              - `type: :web_fetch_result`

                - `:web_fetch_result`

              - `url: String`

                Fetched content URL

          - `tool_use_id: String`

          - `type: :web_fetch_tool_result`

            - `:web_fetch_tool_result`

        - `class BetaCodeExecutionToolResultBlock`

          - `content: BetaCodeExecutionToolResultBlockContent`

            - `class BetaCodeExecutionToolResultError`

              - `error_code: BetaCodeExecutionToolResultErrorCode`

                - `:invalid_tool_input`

                - `:unavailable`

                - `:too_many_requests`

                - `:execution_time_exceeded`

              - `type: :code_execution_tool_result_error`

                - `:code_execution_tool_result_error`

            - `class BetaCodeExecutionResultBlock`

              - `content: Array[BetaCodeExecutionOutputBlock]`

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

        - `class BetaBashCodeExecutionToolResultBlock`

          - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

            - `class BetaBashCodeExecutionToolResultError`

              - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

                - `:invalid_tool_input`

                - `:unavailable`

                - `:too_many_requests`

                - `:execution_time_exceeded`

                - `:output_file_too_large`

              - `type: :bash_code_execution_tool_result_error`

                - `:bash_code_execution_tool_result_error`

            - `class BetaBashCodeExecutionResultBlock`

              - `content: Array[BetaBashCodeExecutionOutputBlock]`

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

        - `class BetaTextEditorCodeExecutionToolResultBlock`

          - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

            - `class BetaTextEditorCodeExecutionToolResultError`

              - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

                - `:invalid_tool_input`

                - `:unavailable`

                - `:too_many_requests`

                - `:execution_time_exceeded`

                - `:file_not_found`

              - `error_message: String`

              - `type: :text_editor_code_execution_tool_result_error`

                - `:text_editor_code_execution_tool_result_error`

            - `class BetaTextEditorCodeExecutionViewResultBlock`

              - `content: String`

              - `file_type: :text | :image | :pdf`

                - `:text`

                - `:image`

                - `:pdf`

              - `num_lines: Integer`

              - `start_line: Integer`

              - `total_lines: Integer`

              - `type: :text_editor_code_execution_view_result`

                - `:text_editor_code_execution_view_result`

            - `class BetaTextEditorCodeExecutionCreateResultBlock`

              - `is_file_update: bool`

              - `type: :text_editor_code_execution_create_result`

                - `:text_editor_code_execution_create_result`

            - `class BetaTextEditorCodeExecutionStrReplaceResultBlock`

              - `lines: Array[String]`

              - `new_lines: Integer`

              - `new_start: Integer`

              - `old_lines: Integer`

              - `old_start: Integer`

              - `type: :text_editor_code_execution_str_replace_result`

                - `:text_editor_code_execution_str_replace_result`

          - `tool_use_id: String`

          - `type: :text_editor_code_execution_tool_result`

            - `:text_editor_code_execution_tool_result`

        - `class BetaToolSearchToolResultBlock`

          - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

            - `class BetaToolSearchToolResultError`

              - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

                - `:invalid_tool_input`

                - `:unavailable`

                - `:too_many_requests`

                - `:execution_time_exceeded`

              - `error_message: String`

              - `type: :tool_search_tool_result_error`

                - `:tool_search_tool_result_error`

            - `class BetaToolSearchToolSearchResultBlock`

              - `tool_references: Array[BetaToolReferenceBlock]`

                - `tool_name: String`

                - `type: :tool_reference`

                  - `:tool_reference`

              - `type: :tool_search_tool_search_result`

                - `:tool_search_tool_search_result`

          - `tool_use_id: String`

          - `type: :tool_search_tool_result`

            - `:tool_search_tool_result`

        - `class BetaMCPToolUseBlock`

          - `id: String`

          - `input: Hash[Symbol, untyped]`

          - `name: String`

            The name of the MCP tool

          - `server_name: String`

            The name of the MCP server

          - `type: :mcp_tool_use`

            - `:mcp_tool_use`

        - `class BetaMCPToolResultBlock`

          - `content: String | Array[BetaTextBlock]`

            - `String`

            - `Array[BetaTextBlock]`

              - `citations: Array[BetaTextCitation]`

                Citations supporting the text block.

                The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

                - `class BetaCitationCharLocation`

                  - `cited_text: String`

                  - `document_index: Integer`

                  - `document_title: String`

                  - `end_char_index: Integer`

                  - `file_id: String`

                  - `start_char_index: Integer`

                  - `type: :char_location`

                    - `:char_location`

                - `class BetaCitationPageLocation`

                  - `cited_text: String`

                  - `document_index: Integer`

                  - `document_title: String`

                  - `end_page_number: Integer`

                  - `file_id: String`

                  - `start_page_number: Integer`

                  - `type: :page_location`

                    - `:page_location`

                - `class BetaCitationContentBlockLocation`

                  - `cited_text: String`

                  - `document_index: Integer`

                  - `document_title: String`

                  - `end_block_index: Integer`

                  - `file_id: String`

                  - `start_block_index: Integer`

                  - `type: :content_block_location`

                    - `:content_block_location`

                - `class BetaCitationsWebSearchResultLocation`

                  - `cited_text: String`

                  - `encrypted_index: String`

                  - `title: String`

                  - `type: :web_search_result_location`

                    - `:web_search_result_location`

                  - `url: String`

                - `class BetaCitationSearchResultLocation`

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

          - `is_error: bool`

          - `tool_use_id: String`

          - `type: :mcp_tool_result`

            - `:mcp_tool_result`

        - `class BetaContainerUploadBlock`

          Response model for a file uploaded to the container.

          - `file_id: String`

          - `type: :container_upload`

            - `:container_upload`

      - `context_management: BetaContextManagementResponse`

        Context management response.

        Information about context management strategies applied during the request.

        - `applied_edits: Array[BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse]`

          List of context management edits that were applied.

          - `class BetaClearToolUses20250919EditResponse`

            - `cleared_input_tokens: Integer`

              Number of input tokens cleared by this edit.

            - `cleared_tool_uses: Integer`

              Number of tool uses that were cleared.

            - `type: :clear_tool_uses_20250919`

              The type of context management edit applied.

              - `:clear_tool_uses_20250919`

          - `class BetaClearThinking20251015EditResponse`

            - `cleared_input_tokens: Integer`

              Number of input tokens cleared by this edit.

            - `cleared_thinking_turns: Integer`

              Number of thinking turns that were cleared.

            - `type: :clear_thinking_20251015`

              The type of context management edit applied.

              - `:clear_thinking_20251015`

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

      - `stop_reason: BetaStopReason`

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

        - `:model_context_window_exceeded`

      - `stop_sequence: String`

        Which custom stop sequence was generated, if any.

        This value will be a non-null string if one of your custom stop sequences was generated.

      - `type: :message`

        Object type.

        For Messages, this is always `"message"`.

        - `:message`

      - `usage: BetaUsage`

        Billing and rate-limit usage.

        Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

        Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

        For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

        Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

        - `cache_creation: BetaCacheCreation`

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

        - `server_tool_use: BetaServerToolUsage`

          The number of server tool requests.

          - `web_fetch_requests: Integer`

            The number of web fetch tool requests.

          - `web_search_requests: Integer`

            The number of web search tool requests.

        - `service_tier: :standard | :priority | :batch`

          If the request used the priority, standard, or batch tier.

          - `:standard`

          - `:priority`

          - `:batch`

    - `type: :message_start`

      - `:message_start`

  - `class BetaRawMessageDeltaEvent`

    - `context_management: BetaContextManagementResponse`

      Information about context management strategies applied during the request

      - `applied_edits: Array[BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse]`

        List of context management edits that were applied.

        - `class BetaClearToolUses20250919EditResponse`

          - `cleared_input_tokens: Integer`

            Number of input tokens cleared by this edit.

          - `cleared_tool_uses: Integer`

            Number of tool uses that were cleared.

          - `type: :clear_tool_uses_20250919`

            The type of context management edit applied.

            - `:clear_tool_uses_20250919`

        - `class BetaClearThinking20251015EditResponse`

          - `cleared_input_tokens: Integer`

            Number of input tokens cleared by this edit.

          - `cleared_thinking_turns: Integer`

            Number of thinking turns that were cleared.

          - `type: :clear_thinking_20251015`

            The type of context management edit applied.

            - `:clear_thinking_20251015`

    - `delta: { container, stop_reason, stop_sequence}`

      - `container: BetaContainer`

        Information about the container used in the request (for the code execution tool)

        - `id: String`

          Identifier for the container used in this request

        - `expires_at: Time`

          The time at which the container will expire.

        - `skills: Array[BetaSkill]`

          Skills loaded in the container

          - `skill_id: String`

            Skill ID

          - `type: :anthropic | :custom`

            Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

            - `:anthropic`

            - `:custom`

          - `version: String`

            Skill version or 'latest' for most recent version

      - `stop_reason: BetaStopReason`

        - `:end_turn`

        - `:max_tokens`

        - `:stop_sequence`

        - `:tool_use`

        - `:pause_turn`

        - `:refusal`

        - `:model_context_window_exceeded`

      - `stop_sequence: String`

    - `type: :message_delta`

      - `:message_delta`

    - `usage: BetaMessageDeltaUsage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cache_creation_input_tokens: Integer`

        The cumulative number of input tokens used to create the cache entry.

      - `cache_read_input_tokens: Integer`

        The cumulative number of input tokens read from the cache.

      - `input_tokens: Integer`

        The cumulative number of input tokens which were used.

      - `output_tokens: Integer`

        The cumulative number of output tokens which were used.

      - `server_tool_use: BetaServerToolUsage`

        The number of server tool requests.

        - `web_fetch_requests: Integer`

          The number of web fetch tool requests.

        - `web_search_requests: Integer`

          The number of web search tool requests.

  - `class BetaRawMessageStopEvent`

    - `type: :message_stop`

      - `:message_stop`

  - `class BetaRawContentBlockStartEvent`

    - `content_block: BetaTextBlock | BetaThinkingBlock | BetaRedactedThinkingBlock | 11 more`

      Response model for a file uploaded to the container.

      - `class BetaTextBlock`

        - `citations: Array[BetaTextCitation]`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `class BetaCitationCharLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_char_index: Integer`

            - `file_id: String`

            - `start_char_index: Integer`

            - `type: :char_location`

              - `:char_location`

          - `class BetaCitationPageLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_page_number: Integer`

            - `file_id: String`

            - `start_page_number: Integer`

            - `type: :page_location`

              - `:page_location`

          - `class BetaCitationContentBlockLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_block_index: Integer`

            - `file_id: String`

            - `start_block_index: Integer`

            - `type: :content_block_location`

              - `:content_block_location`

          - `class BetaCitationsWebSearchResultLocation`

            - `cited_text: String`

            - `encrypted_index: String`

            - `title: String`

            - `type: :web_search_result_location`

              - `:web_search_result_location`

            - `url: String`

          - `class BetaCitationSearchResultLocation`

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

      - `class BetaThinkingBlock`

        - `signature: String`

        - `thinking: String`

        - `type: :thinking`

          - `:thinking`

      - `class BetaRedactedThinkingBlock`

        - `data: String`

        - `type: :redacted_thinking`

          - `:redacted_thinking`

      - `class BetaToolUseBlock`

        - `id: String`

        - `input: Hash[Symbol, untyped]`

        - `name: String`

        - `type: :tool_use`

          - `:tool_use`

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

      - `class BetaServerToolUseBlock`

        - `id: String`

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

      - `class BetaWebSearchToolResultBlock`

        - `content: BetaWebSearchToolResultBlockContent`

          - `class BetaWebSearchToolResultError`

            - `error_code: BetaWebSearchToolResultErrorCode`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:max_uses_exceeded`

              - `:too_many_requests`

              - `:query_too_long`

            - `type: :web_search_tool_result_error`

              - `:web_search_tool_result_error`

          - `Array[BetaWebSearchResultBlock]`

            - `encrypted_content: String`

            - `page_age: String`

            - `title: String`

            - `type: :web_search_result`

              - `:web_search_result`

            - `url: String`

        - `tool_use_id: String`

        - `type: :web_search_tool_result`

          - `:web_search_tool_result`

      - `class BetaWebFetchToolResultBlock`

        - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

          - `class BetaWebFetchToolResultErrorBlock`

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

          - `class BetaWebFetchBlock`

            - `content: BetaDocumentBlock`

              - `citations: BetaCitationConfig`

                Citation configuration for the document

                - `enabled: bool`

              - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

              - `title: String`

                The title of the document

              - `type: :document`

                - `:document`

            - `retrieved_at: String`

              ISO 8601 timestamp when the content was retrieved

            - `type: :web_fetch_result`

              - `:web_fetch_result`

            - `url: String`

              Fetched content URL

        - `tool_use_id: String`

        - `type: :web_fetch_tool_result`

          - `:web_fetch_tool_result`

      - `class BetaCodeExecutionToolResultBlock`

        - `content: BetaCodeExecutionToolResultBlockContent`

          - `class BetaCodeExecutionToolResultError`

            - `error_code: BetaCodeExecutionToolResultErrorCode`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:too_many_requests`

              - `:execution_time_exceeded`

            - `type: :code_execution_tool_result_error`

              - `:code_execution_tool_result_error`

          - `class BetaCodeExecutionResultBlock`

            - `content: Array[BetaCodeExecutionOutputBlock]`

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

      - `class BetaBashCodeExecutionToolResultBlock`

        - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

          - `class BetaBashCodeExecutionToolResultError`

            - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:too_many_requests`

              - `:execution_time_exceeded`

              - `:output_file_too_large`

            - `type: :bash_code_execution_tool_result_error`

              - `:bash_code_execution_tool_result_error`

          - `class BetaBashCodeExecutionResultBlock`

            - `content: Array[BetaBashCodeExecutionOutputBlock]`

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

      - `class BetaTextEditorCodeExecutionToolResultBlock`

        - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

          - `class BetaTextEditorCodeExecutionToolResultError`

            - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:too_many_requests`

              - `:execution_time_exceeded`

              - `:file_not_found`

            - `error_message: String`

            - `type: :text_editor_code_execution_tool_result_error`

              - `:text_editor_code_execution_tool_result_error`

          - `class BetaTextEditorCodeExecutionViewResultBlock`

            - `content: String`

            - `file_type: :text | :image | :pdf`

              - `:text`

              - `:image`

              - `:pdf`

            - `num_lines: Integer`

            - `start_line: Integer`

            - `total_lines: Integer`

            - `type: :text_editor_code_execution_view_result`

              - `:text_editor_code_execution_view_result`

          - `class BetaTextEditorCodeExecutionCreateResultBlock`

            - `is_file_update: bool`

            - `type: :text_editor_code_execution_create_result`

              - `:text_editor_code_execution_create_result`

          - `class BetaTextEditorCodeExecutionStrReplaceResultBlock`

            - `lines: Array[String]`

            - `new_lines: Integer`

            - `new_start: Integer`

            - `old_lines: Integer`

            - `old_start: Integer`

            - `type: :text_editor_code_execution_str_replace_result`

              - `:text_editor_code_execution_str_replace_result`

        - `tool_use_id: String`

        - `type: :text_editor_code_execution_tool_result`

          - `:text_editor_code_execution_tool_result`

      - `class BetaToolSearchToolResultBlock`

        - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

          - `class BetaToolSearchToolResultError`

            - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:too_many_requests`

              - `:execution_time_exceeded`

            - `error_message: String`

            - `type: :tool_search_tool_result_error`

              - `:tool_search_tool_result_error`

          - `class BetaToolSearchToolSearchResultBlock`

            - `tool_references: Array[BetaToolReferenceBlock]`

              - `tool_name: String`

              - `type: :tool_reference`

                - `:tool_reference`

            - `type: :tool_search_tool_search_result`

              - `:tool_search_tool_search_result`

        - `tool_use_id: String`

        - `type: :tool_search_tool_result`

          - `:tool_search_tool_result`

      - `class BetaMCPToolUseBlock`

        - `id: String`

        - `input: Hash[Symbol, untyped]`

        - `name: String`

          The name of the MCP tool

        - `server_name: String`

          The name of the MCP server

        - `type: :mcp_tool_use`

          - `:mcp_tool_use`

      - `class BetaMCPToolResultBlock`

        - `content: String | Array[BetaTextBlock]`

          - `String`

          - `Array[BetaTextBlock]`

            - `citations: Array[BetaTextCitation]`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class BetaCitationCharLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_char_index: Integer`

                - `file_id: String`

                - `start_char_index: Integer`

                - `type: :char_location`

                  - `:char_location`

              - `class BetaCitationPageLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_page_number: Integer`

                - `file_id: String`

                - `start_page_number: Integer`

                - `type: :page_location`

                  - `:page_location`

              - `class BetaCitationContentBlockLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_block_index: Integer`

                - `file_id: String`

                - `start_block_index: Integer`

                - `type: :content_block_location`

                  - `:content_block_location`

              - `class BetaCitationsWebSearchResultLocation`

                - `cited_text: String`

                - `encrypted_index: String`

                - `title: String`

                - `type: :web_search_result_location`

                  - `:web_search_result_location`

                - `url: String`

              - `class BetaCitationSearchResultLocation`

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

        - `is_error: bool`

        - `tool_use_id: String`

        - `type: :mcp_tool_result`

          - `:mcp_tool_result`

      - `class BetaContainerUploadBlock`

        Response model for a file uploaded to the container.

        - `file_id: String`

        - `type: :container_upload`

          - `:container_upload`

    - `index: Integer`

    - `type: :content_block_start`

      - `:content_block_start`

  - `class BetaRawContentBlockDeltaEvent`

    - `delta: BetaRawContentBlockDelta`

      - `class BetaTextDelta`

        - `text: String`

        - `type: :text_delta`

          - `:text_delta`

      - `class BetaInputJSONDelta`

        - `partial_json: String`

        - `type: :input_json_delta`

          - `:input_json_delta`

      - `class BetaCitationsDelta`

        - `citation: BetaCitationCharLocation | BetaCitationPageLocation | BetaCitationContentBlockLocation | 2 more`

          - `class BetaCitationCharLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_char_index: Integer`

            - `file_id: String`

            - `start_char_index: Integer`

            - `type: :char_location`

              - `:char_location`

          - `class BetaCitationPageLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_page_number: Integer`

            - `file_id: String`

            - `start_page_number: Integer`

            - `type: :page_location`

              - `:page_location`

          - `class BetaCitationContentBlockLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_block_index: Integer`

            - `file_id: String`

            - `start_block_index: Integer`

            - `type: :content_block_location`

              - `:content_block_location`

          - `class BetaCitationsWebSearchResultLocation`

            - `cited_text: String`

            - `encrypted_index: String`

            - `title: String`

            - `type: :web_search_result_location`

              - `:web_search_result_location`

            - `url: String`

          - `class BetaCitationSearchResultLocation`

            - `cited_text: String`

            - `end_block_index: Integer`

            - `search_result_index: Integer`

            - `source: String`

            - `start_block_index: Integer`

            - `title: String`

            - `type: :search_result_location`

              - `:search_result_location`

        - `type: :citations_delta`

          - `:citations_delta`

      - `class BetaThinkingDelta`

        - `thinking: String`

        - `type: :thinking_delta`

          - `:thinking_delta`

      - `class BetaSignatureDelta`

        - `signature: String`

        - `type: :signature_delta`

          - `:signature_delta`

    - `index: Integer`

    - `type: :content_block_delta`

      - `:content_block_delta`

  - `class BetaRawContentBlockStopEvent`

    - `index: Integer`

    - `type: :content_block_stop`

      - `:content_block_stop`

### Beta Redacted Thinking Block

- `class BetaRedactedThinkingBlock`

  - `data: String`

  - `type: :redacted_thinking`

    - `:redacted_thinking`

### Beta Redacted Thinking Block Param

- `class BetaRedactedThinkingBlockParam`

  - `data: String`

  - `type: :redacted_thinking`

    - `:redacted_thinking`

### Beta Request Document Block

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

### Beta Request MCP Server Tool Configuration

- `class BetaRequestMCPServerToolConfiguration`

  - `allowed_tools: Array[String]`

  - `enabled: bool`

### Beta Request MCP Server URL Definition

- `class BetaRequestMCPServerURLDefinition`

  - `name: String`

  - `type: :url`

    - `:url`

  - `url: String`

  - `authorization_token: String`

  - `tool_configuration: BetaRequestMCPServerToolConfiguration`

    - `allowed_tools: Array[String]`

    - `enabled: bool`

### Beta Request MCP Tool Result Block Param

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

### Beta Search Result Block Param

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

### Beta Server Tool Caller

- `class BetaServerToolCaller`

  Tool invocation generated by a server-side tool.

  - `tool_id: String`

  - `type: :code_execution_20250825`

    - `:code_execution_20250825`

### Beta Server Tool Usage

- `class BetaServerToolUsage`

  - `web_fetch_requests: Integer`

    The number of web fetch tool requests.

  - `web_search_requests: Integer`

    The number of web search tool requests.

### Beta Server Tool Use Block

- `class BetaServerToolUseBlock`

  - `id: String`

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

### Beta Server Tool Use Block Param

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

### Beta Signature Delta

- `class BetaSignatureDelta`

  - `signature: String`

  - `type: :signature_delta`

    - `:signature_delta`

### Beta Skill

- `class BetaSkill`

  A skill that was loaded in a container (response model).

  - `skill_id: String`

    Skill ID

  - `type: :anthropic | :custom`

    Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

    - `:anthropic`

    - `:custom`

  - `version: String`

    Skill version or 'latest' for most recent version

### Beta Skill Params

- `class BetaSkillParams`

  Specification for a skill to be loaded in a container (request model).

  - `skill_id: String`

    Skill ID

  - `type: :anthropic | :custom`

    Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

    - `:anthropic`

    - `:custom`

  - `version: String`

    Skill version or 'latest' for most recent version

### Beta Stop Reason

- `BetaStopReason = :end_turn | :max_tokens | :stop_sequence | 4 more`

  - `:end_turn`

  - `:max_tokens`

  - `:stop_sequence`

  - `:tool_use`

  - `:pause_turn`

  - `:refusal`

  - `:model_context_window_exceeded`

### Beta Text Block

- `class BetaTextBlock`

  - `citations: Array[BetaTextCitation]`

    Citations supporting the text block.

    The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

    - `class BetaCitationCharLocation`

      - `cited_text: String`

      - `document_index: Integer`

      - `document_title: String`

      - `end_char_index: Integer`

      - `file_id: String`

      - `start_char_index: Integer`

      - `type: :char_location`

        - `:char_location`

    - `class BetaCitationPageLocation`

      - `cited_text: String`

      - `document_index: Integer`

      - `document_title: String`

      - `end_page_number: Integer`

      - `file_id: String`

      - `start_page_number: Integer`

      - `type: :page_location`

        - `:page_location`

    - `class BetaCitationContentBlockLocation`

      - `cited_text: String`

      - `document_index: Integer`

      - `document_title: String`

      - `end_block_index: Integer`

      - `file_id: String`

      - `start_block_index: Integer`

      - `type: :content_block_location`

        - `:content_block_location`

    - `class BetaCitationsWebSearchResultLocation`

      - `cited_text: String`

      - `encrypted_index: String`

      - `title: String`

      - `type: :web_search_result_location`

        - `:web_search_result_location`

      - `url: String`

    - `class BetaCitationSearchResultLocation`

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

### Beta Text Block Param

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

### Beta Text Citation

- `BetaTextCitation = BetaCitationCharLocation | BetaCitationPageLocation | BetaCitationContentBlockLocation | 2 more`

  - `class BetaCitationCharLocation`

    - `cited_text: String`

    - `document_index: Integer`

    - `document_title: String`

    - `end_char_index: Integer`

    - `file_id: String`

    - `start_char_index: Integer`

    - `type: :char_location`

      - `:char_location`

  - `class BetaCitationPageLocation`

    - `cited_text: String`

    - `document_index: Integer`

    - `document_title: String`

    - `end_page_number: Integer`

    - `file_id: String`

    - `start_page_number: Integer`

    - `type: :page_location`

      - `:page_location`

  - `class BetaCitationContentBlockLocation`

    - `cited_text: String`

    - `document_index: Integer`

    - `document_title: String`

    - `end_block_index: Integer`

    - `file_id: String`

    - `start_block_index: Integer`

    - `type: :content_block_location`

      - `:content_block_location`

  - `class BetaCitationsWebSearchResultLocation`

    - `cited_text: String`

    - `encrypted_index: String`

    - `title: String`

    - `type: :web_search_result_location`

      - `:web_search_result_location`

    - `url: String`

  - `class BetaCitationSearchResultLocation`

    - `cited_text: String`

    - `end_block_index: Integer`

    - `search_result_index: Integer`

    - `source: String`

    - `start_block_index: Integer`

    - `title: String`

    - `type: :search_result_location`

      - `:search_result_location`

### Beta Text Citation Param

- `BetaTextCitationParam = BetaCitationCharLocationParam | BetaCitationPageLocationParam | BetaCitationContentBlockLocationParam | 2 more`

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

### Beta Text Delta

- `class BetaTextDelta`

  - `text: String`

  - `type: :text_delta`

    - `:text_delta`

### Beta Text Editor Code Execution Create Result Block

- `class BetaTextEditorCodeExecutionCreateResultBlock`

  - `is_file_update: bool`

  - `type: :text_editor_code_execution_create_result`

    - `:text_editor_code_execution_create_result`

### Beta Text Editor Code Execution Create Result Block Param

- `class BetaTextEditorCodeExecutionCreateResultBlockParam`

  - `is_file_update: bool`

  - `type: :text_editor_code_execution_create_result`

    - `:text_editor_code_execution_create_result`

### Beta Text Editor Code Execution Str Replace Result Block

- `class BetaTextEditorCodeExecutionStrReplaceResultBlock`

  - `lines: Array[String]`

  - `new_lines: Integer`

  - `new_start: Integer`

  - `old_lines: Integer`

  - `old_start: Integer`

  - `type: :text_editor_code_execution_str_replace_result`

    - `:text_editor_code_execution_str_replace_result`

### Beta Text Editor Code Execution Str Replace Result Block Param

- `class BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

  - `type: :text_editor_code_execution_str_replace_result`

    - `:text_editor_code_execution_str_replace_result`

  - `lines: Array[String]`

  - `new_lines: Integer`

  - `new_start: Integer`

  - `old_lines: Integer`

  - `old_start: Integer`

### Beta Text Editor Code Execution Tool Result Block

- `class BetaTextEditorCodeExecutionToolResultBlock`

  - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

    - `class BetaTextEditorCodeExecutionToolResultError`

      - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

        - `:invalid_tool_input`

        - `:unavailable`

        - `:too_many_requests`

        - `:execution_time_exceeded`

        - `:file_not_found`

      - `error_message: String`

      - `type: :text_editor_code_execution_tool_result_error`

        - `:text_editor_code_execution_tool_result_error`

    - `class BetaTextEditorCodeExecutionViewResultBlock`

      - `content: String`

      - `file_type: :text | :image | :pdf`

        - `:text`

        - `:image`

        - `:pdf`

      - `num_lines: Integer`

      - `start_line: Integer`

      - `total_lines: Integer`

      - `type: :text_editor_code_execution_view_result`

        - `:text_editor_code_execution_view_result`

    - `class BetaTextEditorCodeExecutionCreateResultBlock`

      - `is_file_update: bool`

      - `type: :text_editor_code_execution_create_result`

        - `:text_editor_code_execution_create_result`

    - `class BetaTextEditorCodeExecutionStrReplaceResultBlock`

      - `lines: Array[String]`

      - `new_lines: Integer`

      - `new_start: Integer`

      - `old_lines: Integer`

      - `old_start: Integer`

      - `type: :text_editor_code_execution_str_replace_result`

        - `:text_editor_code_execution_str_replace_result`

  - `tool_use_id: String`

  - `type: :text_editor_code_execution_tool_result`

    - `:text_editor_code_execution_tool_result`

### Beta Text Editor Code Execution Tool Result Block Param

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

### Beta Text Editor Code Execution Tool Result Error

- `class BetaTextEditorCodeExecutionToolResultError`

  - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

    - `:invalid_tool_input`

    - `:unavailable`

    - `:too_many_requests`

    - `:execution_time_exceeded`

    - `:file_not_found`

  - `error_message: String`

  - `type: :text_editor_code_execution_tool_result_error`

    - `:text_editor_code_execution_tool_result_error`

### Beta Text Editor Code Execution Tool Result Error Param

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

### Beta Text Editor Code Execution View Result Block

- `class BetaTextEditorCodeExecutionViewResultBlock`

  - `content: String`

  - `file_type: :text | :image | :pdf`

    - `:text`

    - `:image`

    - `:pdf`

  - `num_lines: Integer`

  - `start_line: Integer`

  - `total_lines: Integer`

  - `type: :text_editor_code_execution_view_result`

    - `:text_editor_code_execution_view_result`

### Beta Text Editor Code Execution View Result Block Param

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

### Beta Thinking Block

- `class BetaThinkingBlock`

  - `signature: String`

  - `thinking: String`

  - `type: :thinking`

    - `:thinking`

### Beta Thinking Block Param

- `class BetaThinkingBlockParam`

  - `signature: String`

  - `thinking: String`

  - `type: :thinking`

    - `:thinking`

### Beta Thinking Config Disabled

- `class BetaThinkingConfigDisabled`

  - `type: :disabled`

    - `:disabled`

### Beta Thinking Config Enabled

- `class BetaThinkingConfigEnabled`

  - `budget_tokens: Integer`

    Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

    Must be ≥1024 and less than `max_tokens`.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `type: :enabled`

    - `:enabled`

### Beta Thinking Config Param

- `BetaThinkingConfigParam = BetaThinkingConfigEnabled | BetaThinkingConfigDisabled`

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

### Beta Thinking Delta

- `class BetaThinkingDelta`

  - `thinking: String`

  - `type: :thinking_delta`

    - `:thinking_delta`

### Beta Thinking Turns

- `class BetaThinkingTurns`

  - `type: :thinking_turns`

    - `:thinking_turns`

  - `value: Integer`

### Beta Tool

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

### Beta Tool Bash 20241022

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

### Beta Tool Bash 20250124

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

### Beta Tool Choice

- `BetaToolChoice = BetaToolChoiceAuto | BetaToolChoiceAny | BetaToolChoiceTool | BetaToolChoiceNone`

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

### Beta Tool Choice Any

- `class BetaToolChoiceAny`

  The model will use any available tools.

  - `type: :any`

    - `:any`

  - `disable_parallel_tool_use: bool`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output exactly one tool use.

### Beta Tool Choice Auto

- `class BetaToolChoiceAuto`

  The model will automatically decide whether to use tools.

  - `type: :auto`

    - `:auto`

  - `disable_parallel_tool_use: bool`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output at most one tool use.

### Beta Tool Choice None

- `class BetaToolChoiceNone`

  The model will not be allowed to use tools.

  - `type: :none`

    - `:none`

### Beta Tool Choice Tool

- `class BetaToolChoiceTool`

  The model will use the specified tool with `tool_choice.name`.

  - `name: String`

    The name of the tool to use.

  - `type: :tool`

    - `:tool`

  - `disable_parallel_tool_use: bool`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output exactly one tool use.

### Beta Tool Computer Use 20241022

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

### Beta Tool Computer Use 20250124

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

### Beta Tool Computer Use 20251124

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

### Beta Tool Reference Block

- `class BetaToolReferenceBlock`

  - `tool_name: String`

  - `type: :tool_reference`

    - `:tool_reference`

### Beta Tool Reference Block Param

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

### Beta Tool Result Block Param

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

### Beta Tool Search Tool Bm25 20251119

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

### Beta Tool Search Tool Regex 20251119

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

### Beta Tool Search Tool Result Block

- `class BetaToolSearchToolResultBlock`

  - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

    - `class BetaToolSearchToolResultError`

      - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

        - `:invalid_tool_input`

        - `:unavailable`

        - `:too_many_requests`

        - `:execution_time_exceeded`

      - `error_message: String`

      - `type: :tool_search_tool_result_error`

        - `:tool_search_tool_result_error`

    - `class BetaToolSearchToolSearchResultBlock`

      - `tool_references: Array[BetaToolReferenceBlock]`

        - `tool_name: String`

        - `type: :tool_reference`

          - `:tool_reference`

      - `type: :tool_search_tool_search_result`

        - `:tool_search_tool_search_result`

  - `tool_use_id: String`

  - `type: :tool_search_tool_result`

    - `:tool_search_tool_result`

### Beta Tool Search Tool Result Block Param

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

### Beta Tool Search Tool Result Error

- `class BetaToolSearchToolResultError`

  - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

    - `:invalid_tool_input`

    - `:unavailable`

    - `:too_many_requests`

    - `:execution_time_exceeded`

  - `error_message: String`

  - `type: :tool_search_tool_result_error`

    - `:tool_search_tool_result_error`

### Beta Tool Search Tool Result Error Param

- `class BetaToolSearchToolResultErrorParam`

  - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

    - `:invalid_tool_input`

    - `:unavailable`

    - `:too_many_requests`

    - `:execution_time_exceeded`

  - `type: :tool_search_tool_result_error`

    - `:tool_search_tool_result_error`

### Beta Tool Search Tool Search Result Block

- `class BetaToolSearchToolSearchResultBlock`

  - `tool_references: Array[BetaToolReferenceBlock]`

    - `tool_name: String`

    - `type: :tool_reference`

      - `:tool_reference`

  - `type: :tool_search_tool_search_result`

    - `:tool_search_tool_search_result`

### Beta Tool Search Tool Search Result Block Param

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

### Beta Tool Text Editor 20241022

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

### Beta Tool Text Editor 20250124

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

### Beta Tool Text Editor 20250429

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

### Beta Tool Text Editor 20250728

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

### Beta Tool Union

- `BetaToolUnion = BetaTool | BetaToolBash20241022 | BetaToolBash20250124 | 15 more`

  Configuration for a group of tools from an MCP server.

  Allows configuring enabled status and defer_loading for all tools
  from an MCP server, with optional per-tool overrides.

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

### Beta Tool Use Block

- `class BetaToolUseBlock`

  - `id: String`

  - `input: Hash[Symbol, untyped]`

  - `name: String`

  - `type: :tool_use`

    - `:tool_use`

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

### Beta Tool Use Block Param

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

### Beta Tool Uses Keep

- `class BetaToolUsesKeep`

  - `type: :tool_uses`

    - `:tool_uses`

  - `value: Integer`

### Beta Tool Uses Trigger

- `class BetaToolUsesTrigger`

  - `type: :tool_uses`

    - `:tool_uses`

  - `value: Integer`

### Beta URL Image Source

- `class BetaURLImageSource`

  - `type: :url`

    - `:url`

  - `url: String`

### Beta URL PDF Source

- `class BetaURLPDFSource`

  - `type: :url`

    - `:url`

  - `url: String`

### Beta Usage

- `class BetaUsage`

  - `cache_creation: BetaCacheCreation`

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

  - `server_tool_use: BetaServerToolUsage`

    The number of server tool requests.

    - `web_fetch_requests: Integer`

      The number of web fetch tool requests.

    - `web_search_requests: Integer`

      The number of web search tool requests.

  - `service_tier: :standard | :priority | :batch`

    If the request used the priority, standard, or batch tier.

    - `:standard`

    - `:priority`

    - `:batch`

### Beta Web Fetch Block

- `class BetaWebFetchBlock`

  - `content: BetaDocumentBlock`

    - `citations: BetaCitationConfig`

      Citation configuration for the document

      - `enabled: bool`

    - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

    - `title: String`

      The title of the document

    - `type: :document`

      - `:document`

  - `retrieved_at: String`

    ISO 8601 timestamp when the content was retrieved

  - `type: :web_fetch_result`

    - `:web_fetch_result`

  - `url: String`

    Fetched content URL

### Beta Web Fetch Block Param

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

### Beta Web Fetch Tool 20250910

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

### Beta Web Fetch Tool Result Block

- `class BetaWebFetchToolResultBlock`

  - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

    - `class BetaWebFetchToolResultErrorBlock`

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

    - `class BetaWebFetchBlock`

      - `content: BetaDocumentBlock`

        - `citations: BetaCitationConfig`

          Citation configuration for the document

          - `enabled: bool`

        - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

        - `title: String`

          The title of the document

        - `type: :document`

          - `:document`

      - `retrieved_at: String`

        ISO 8601 timestamp when the content was retrieved

      - `type: :web_fetch_result`

        - `:web_fetch_result`

      - `url: String`

        Fetched content URL

  - `tool_use_id: String`

  - `type: :web_fetch_tool_result`

    - `:web_fetch_tool_result`

### Beta Web Fetch Tool Result Block Param

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

### Beta Web Fetch Tool Result Error Block

- `class BetaWebFetchToolResultErrorBlock`

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

### Beta Web Fetch Tool Result Error Block Param

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

### Beta Web Fetch Tool Result Error Code

- `BetaWebFetchToolResultErrorCode = :invalid_tool_input | :url_too_long | :url_not_allowed | 5 more`

  - `:invalid_tool_input`

  - `:url_too_long`

  - `:url_not_allowed`

  - `:url_not_accessible`

  - `:unsupported_content_type`

  - `:too_many_requests`

  - `:max_uses_exceeded`

  - `:unavailable`

### Beta Web Search Result Block

- `class BetaWebSearchResultBlock`

  - `encrypted_content: String`

  - `page_age: String`

  - `title: String`

  - `type: :web_search_result`

    - `:web_search_result`

  - `url: String`

### Beta Web Search Result Block Param

- `class BetaWebSearchResultBlockParam`

  - `encrypted_content: String`

  - `title: String`

  - `type: :web_search_result`

    - `:web_search_result`

  - `url: String`

  - `page_age: String`

### Beta Web Search Tool 20250305

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

### Beta Web Search Tool Request Error

- `class BetaWebSearchToolRequestError`

  - `error_code: BetaWebSearchToolResultErrorCode`

    - `:invalid_tool_input`

    - `:unavailable`

    - `:max_uses_exceeded`

    - `:too_many_requests`

    - `:query_too_long`

  - `type: :web_search_tool_result_error`

    - `:web_search_tool_result_error`

### Beta Web Search Tool Result Block

- `class BetaWebSearchToolResultBlock`

  - `content: BetaWebSearchToolResultBlockContent`

    - `class BetaWebSearchToolResultError`

      - `error_code: BetaWebSearchToolResultErrorCode`

        - `:invalid_tool_input`

        - `:unavailable`

        - `:max_uses_exceeded`

        - `:too_many_requests`

        - `:query_too_long`

      - `type: :web_search_tool_result_error`

        - `:web_search_tool_result_error`

    - `Array[BetaWebSearchResultBlock]`

      - `encrypted_content: String`

      - `page_age: String`

      - `title: String`

      - `type: :web_search_result`

        - `:web_search_result`

      - `url: String`

  - `tool_use_id: String`

  - `type: :web_search_tool_result`

    - `:web_search_tool_result`

### Beta Web Search Tool Result Block Content

- `BetaWebSearchToolResultBlockContent = BetaWebSearchToolResultError | Array[BetaWebSearchResultBlock]`

  - `class BetaWebSearchToolResultError`

    - `error_code: BetaWebSearchToolResultErrorCode`

      - `:invalid_tool_input`

      - `:unavailable`

      - `:max_uses_exceeded`

      - `:too_many_requests`

      - `:query_too_long`

    - `type: :web_search_tool_result_error`

      - `:web_search_tool_result_error`

  - `Array[BetaWebSearchResultBlock]`

    - `encrypted_content: String`

    - `page_age: String`

    - `title: String`

    - `type: :web_search_result`

      - `:web_search_result`

    - `url: String`

### Beta Web Search Tool Result Block Param

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

### Beta Web Search Tool Result Block Param Content

- `BetaWebSearchToolResultBlockParamContent = Array[BetaWebSearchResultBlockParam] | BetaWebSearchToolRequestError`

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

### Beta Web Search Tool Result Error

- `class BetaWebSearchToolResultError`

  - `error_code: BetaWebSearchToolResultErrorCode`

    - `:invalid_tool_input`

    - `:unavailable`

    - `:max_uses_exceeded`

    - `:too_many_requests`

    - `:query_too_long`

  - `type: :web_search_tool_result_error`

    - `:web_search_tool_result_error`

### Beta Web Search Tool Result Error Code

- `BetaWebSearchToolResultErrorCode = :invalid_tool_input | :unavailable | :max_uses_exceeded | 2 more`

  - `:invalid_tool_input`

  - `:unavailable`

  - `:max_uses_exceeded`

  - `:too_many_requests`

  - `:query_too_long`

# Batches

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

## Retrieve

`beta.messages.batches.retrieve(message_batch_id, **kwargs) -> BetaMessageBatch`

**get** `/v1/messages/batches/{message_batch_id}`

This endpoint is idempotent and can be used to poll for Message Batch completion. To access the results of a Message Batch, make a request to the `results_url` field in the response.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `message_batch_id: String`

  ID of the Message Batch.

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

beta_message_batch = anthropic.beta.messages.batches.retrieve("message_batch_id")

puts(beta_message_batch)
```

## List

`beta.messages.batches.list(**kwargs) -> Page<BetaMessageBatch>`

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

page = anthropic.beta.messages.batches.list

puts(page)
```

## Cancel

`beta.messages.batches.cancel(message_batch_id, **kwargs) -> BetaMessageBatch`

**post** `/v1/messages/batches/{message_batch_id}/cancel`

Batches may be canceled any time before processing ends. Once cancellation is initiated, the batch enters a `canceling` state, at which time the system may complete any in-progress, non-interruptible requests before finalizing cancellation.

The number of canceled requests is specified in `request_counts`. To determine which requests were canceled, check the individual results within the batch. Note that cancellation may not result in any canceled requests if they were non-interruptible.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `message_batch_id: String`

  ID of the Message Batch.

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

beta_message_batch = anthropic.beta.messages.batches.cancel("message_batch_id")

puts(beta_message_batch)
```

## Delete

`beta.messages.batches.delete(message_batch_id, **kwargs) -> BetaDeletedMessageBatch`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `message_batch_id: String`

  ID of the Message Batch.

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

- `class BetaDeletedMessageBatch`

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

beta_deleted_message_batch = anthropic.beta.messages.batches.delete("message_batch_id")

puts(beta_deleted_message_batch)
```

## Results

`beta.messages.batches.results(message_batch_id, **kwargs) -> BetaMessageBatchIndividualResponse`

**get** `/v1/messages/batches/{message_batch_id}/results`

Streams the results of a Message Batch as a `.jsonl` file.

Each line in the file is a JSON object containing the result of a single request in the Message Batch. Results are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `message_batch_id: String`

  ID of the Message Batch.

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

- `class BetaMessageBatchIndividualResponse`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `custom_id: String`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: BetaMessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `class BetaMessageBatchSucceededResult`

      - `message: BetaMessage`

        - `id: String`

          Unique object identifier.

          The format and length of IDs may change over time.

        - `container: BetaContainer`

          Information about the container used in the request (for the code execution tool)

          - `id: String`

            Identifier for the container used in this request

          - `expires_at: Time`

            The time at which the container will expire.

          - `skills: Array[BetaSkill]`

            Skills loaded in the container

            - `skill_id: String`

              Skill ID

            - `type: :anthropic | :custom`

              Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

              - `:anthropic`

              - `:custom`

            - `version: String`

              Skill version or 'latest' for most recent version

        - `content: Array[BetaContentBlock]`

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

          - `class BetaTextBlock`

            - `citations: Array[BetaTextCitation]`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class BetaCitationCharLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_char_index: Integer`

                - `file_id: String`

                - `start_char_index: Integer`

                - `type: :char_location`

                  - `:char_location`

              - `class BetaCitationPageLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_page_number: Integer`

                - `file_id: String`

                - `start_page_number: Integer`

                - `type: :page_location`

                  - `:page_location`

              - `class BetaCitationContentBlockLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_block_index: Integer`

                - `file_id: String`

                - `start_block_index: Integer`

                - `type: :content_block_location`

                  - `:content_block_location`

              - `class BetaCitationsWebSearchResultLocation`

                - `cited_text: String`

                - `encrypted_index: String`

                - `title: String`

                - `type: :web_search_result_location`

                  - `:web_search_result_location`

                - `url: String`

              - `class BetaCitationSearchResultLocation`

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

          - `class BetaThinkingBlock`

            - `signature: String`

            - `thinking: String`

            - `type: :thinking`

              - `:thinking`

          - `class BetaRedactedThinkingBlock`

            - `data: String`

            - `type: :redacted_thinking`

              - `:redacted_thinking`

          - `class BetaToolUseBlock`

            - `id: String`

            - `input: Hash[Symbol, untyped]`

            - `name: String`

            - `type: :tool_use`

              - `:tool_use`

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

          - `class BetaServerToolUseBlock`

            - `id: String`

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

          - `class BetaWebSearchToolResultBlock`

            - `content: BetaWebSearchToolResultBlockContent`

              - `class BetaWebSearchToolResultError`

                - `error_code: BetaWebSearchToolResultErrorCode`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:max_uses_exceeded`

                  - `:too_many_requests`

                  - `:query_too_long`

                - `type: :web_search_tool_result_error`

                  - `:web_search_tool_result_error`

              - `Array[BetaWebSearchResultBlock]`

                - `encrypted_content: String`

                - `page_age: String`

                - `title: String`

                - `type: :web_search_result`

                  - `:web_search_result`

                - `url: String`

            - `tool_use_id: String`

            - `type: :web_search_tool_result`

              - `:web_search_tool_result`

          - `class BetaWebFetchToolResultBlock`

            - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

              - `class BetaWebFetchToolResultErrorBlock`

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

              - `class BetaWebFetchBlock`

                - `content: BetaDocumentBlock`

                  - `citations: BetaCitationConfig`

                    Citation configuration for the document

                    - `enabled: bool`

                  - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

                  - `title: String`

                    The title of the document

                  - `type: :document`

                    - `:document`

                - `retrieved_at: String`

                  ISO 8601 timestamp when the content was retrieved

                - `type: :web_fetch_result`

                  - `:web_fetch_result`

                - `url: String`

                  Fetched content URL

            - `tool_use_id: String`

            - `type: :web_fetch_tool_result`

              - `:web_fetch_tool_result`

          - `class BetaCodeExecutionToolResultBlock`

            - `content: BetaCodeExecutionToolResultBlockContent`

              - `class BetaCodeExecutionToolResultError`

                - `error_code: BetaCodeExecutionToolResultErrorCode`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:too_many_requests`

                  - `:execution_time_exceeded`

                - `type: :code_execution_tool_result_error`

                  - `:code_execution_tool_result_error`

              - `class BetaCodeExecutionResultBlock`

                - `content: Array[BetaCodeExecutionOutputBlock]`

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

          - `class BetaBashCodeExecutionToolResultBlock`

            - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

              - `class BetaBashCodeExecutionToolResultError`

                - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:too_many_requests`

                  - `:execution_time_exceeded`

                  - `:output_file_too_large`

                - `type: :bash_code_execution_tool_result_error`

                  - `:bash_code_execution_tool_result_error`

              - `class BetaBashCodeExecutionResultBlock`

                - `content: Array[BetaBashCodeExecutionOutputBlock]`

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

          - `class BetaTextEditorCodeExecutionToolResultBlock`

            - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

              - `class BetaTextEditorCodeExecutionToolResultError`

                - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:too_many_requests`

                  - `:execution_time_exceeded`

                  - `:file_not_found`

                - `error_message: String`

                - `type: :text_editor_code_execution_tool_result_error`

                  - `:text_editor_code_execution_tool_result_error`

              - `class BetaTextEditorCodeExecutionViewResultBlock`

                - `content: String`

                - `file_type: :text | :image | :pdf`

                  - `:text`

                  - `:image`

                  - `:pdf`

                - `num_lines: Integer`

                - `start_line: Integer`

                - `total_lines: Integer`

                - `type: :text_editor_code_execution_view_result`

                  - `:text_editor_code_execution_view_result`

              - `class BetaTextEditorCodeExecutionCreateResultBlock`

                - `is_file_update: bool`

                - `type: :text_editor_code_execution_create_result`

                  - `:text_editor_code_execution_create_result`

              - `class BetaTextEditorCodeExecutionStrReplaceResultBlock`

                - `lines: Array[String]`

                - `new_lines: Integer`

                - `new_start: Integer`

                - `old_lines: Integer`

                - `old_start: Integer`

                - `type: :text_editor_code_execution_str_replace_result`

                  - `:text_editor_code_execution_str_replace_result`

            - `tool_use_id: String`

            - `type: :text_editor_code_execution_tool_result`

              - `:text_editor_code_execution_tool_result`

          - `class BetaToolSearchToolResultBlock`

            - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

              - `class BetaToolSearchToolResultError`

                - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:too_many_requests`

                  - `:execution_time_exceeded`

                - `error_message: String`

                - `type: :tool_search_tool_result_error`

                  - `:tool_search_tool_result_error`

              - `class BetaToolSearchToolSearchResultBlock`

                - `tool_references: Array[BetaToolReferenceBlock]`

                  - `tool_name: String`

                  - `type: :tool_reference`

                    - `:tool_reference`

                - `type: :tool_search_tool_search_result`

                  - `:tool_search_tool_search_result`

            - `tool_use_id: String`

            - `type: :tool_search_tool_result`

              - `:tool_search_tool_result`

          - `class BetaMCPToolUseBlock`

            - `id: String`

            - `input: Hash[Symbol, untyped]`

            - `name: String`

              The name of the MCP tool

            - `server_name: String`

              The name of the MCP server

            - `type: :mcp_tool_use`

              - `:mcp_tool_use`

          - `class BetaMCPToolResultBlock`

            - `content: String | Array[BetaTextBlock]`

              - `String`

              - `Array[BetaTextBlock]`

                - `citations: Array[BetaTextCitation]`

                  Citations supporting the text block.

                  The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

                  - `class BetaCitationCharLocation`

                    - `cited_text: String`

                    - `document_index: Integer`

                    - `document_title: String`

                    - `end_char_index: Integer`

                    - `file_id: String`

                    - `start_char_index: Integer`

                    - `type: :char_location`

                      - `:char_location`

                  - `class BetaCitationPageLocation`

                    - `cited_text: String`

                    - `document_index: Integer`

                    - `document_title: String`

                    - `end_page_number: Integer`

                    - `file_id: String`

                    - `start_page_number: Integer`

                    - `type: :page_location`

                      - `:page_location`

                  - `class BetaCitationContentBlockLocation`

                    - `cited_text: String`

                    - `document_index: Integer`

                    - `document_title: String`

                    - `end_block_index: Integer`

                    - `file_id: String`

                    - `start_block_index: Integer`

                    - `type: :content_block_location`

                      - `:content_block_location`

                  - `class BetaCitationsWebSearchResultLocation`

                    - `cited_text: String`

                    - `encrypted_index: String`

                    - `title: String`

                    - `type: :web_search_result_location`

                      - `:web_search_result_location`

                    - `url: String`

                  - `class BetaCitationSearchResultLocation`

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

            - `is_error: bool`

            - `tool_use_id: String`

            - `type: :mcp_tool_result`

              - `:mcp_tool_result`

          - `class BetaContainerUploadBlock`

            Response model for a file uploaded to the container.

            - `file_id: String`

            - `type: :container_upload`

              - `:container_upload`

        - `context_management: BetaContextManagementResponse`

          Context management response.

          Information about context management strategies applied during the request.

          - `applied_edits: Array[BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse]`

            List of context management edits that were applied.

            - `class BetaClearToolUses20250919EditResponse`

              - `cleared_input_tokens: Integer`

                Number of input tokens cleared by this edit.

              - `cleared_tool_uses: Integer`

                Number of tool uses that were cleared.

              - `type: :clear_tool_uses_20250919`

                The type of context management edit applied.

                - `:clear_tool_uses_20250919`

            - `class BetaClearThinking20251015EditResponse`

              - `cleared_input_tokens: Integer`

                Number of input tokens cleared by this edit.

              - `cleared_thinking_turns: Integer`

                Number of thinking turns that were cleared.

              - `type: :clear_thinking_20251015`

                The type of context management edit applied.

                - `:clear_thinking_20251015`

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

        - `stop_reason: BetaStopReason`

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

          - `:model_context_window_exceeded`

        - `stop_sequence: String`

          Which custom stop sequence was generated, if any.

          This value will be a non-null string if one of your custom stop sequences was generated.

        - `type: :message`

          Object type.

          For Messages, this is always `"message"`.

          - `:message`

        - `usage: BetaUsage`

          Billing and rate-limit usage.

          Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

          Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

          For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

          Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

          - `cache_creation: BetaCacheCreation`

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

          - `server_tool_use: BetaServerToolUsage`

            The number of server tool requests.

            - `web_fetch_requests: Integer`

              The number of web fetch tool requests.

            - `web_search_requests: Integer`

              The number of web search tool requests.

          - `service_tier: :standard | :priority | :batch`

            If the request used the priority, standard, or batch tier.

            - `:standard`

            - `:priority`

            - `:batch`

      - `type: :succeeded`

        - `:succeeded`

    - `class BetaMessageBatchErroredResult`

      - `error: BetaErrorResponse`

        - `error: BetaError`

          - `class BetaInvalidRequestError`

            - `message: String`

            - `type: :invalid_request_error`

              - `:invalid_request_error`

          - `class BetaAuthenticationError`

            - `message: String`

            - `type: :authentication_error`

              - `:authentication_error`

          - `class BetaBillingError`

            - `message: String`

            - `type: :billing_error`

              - `:billing_error`

          - `class BetaPermissionError`

            - `message: String`

            - `type: :permission_error`

              - `:permission_error`

          - `class BetaNotFoundError`

            - `message: String`

            - `type: :not_found_error`

              - `:not_found_error`

          - `class BetaRateLimitError`

            - `message: String`

            - `type: :rate_limit_error`

              - `:rate_limit_error`

          - `class BetaGatewayTimeoutError`

            - `message: String`

            - `type: :timeout_error`

              - `:timeout_error`

          - `class BetaAPIError`

            - `message: String`

            - `type: :api_error`

              - `:api_error`

          - `class BetaOverloadedError`

            - `message: String`

            - `type: :overloaded_error`

              - `:overloaded_error`

        - `request_id: String`

        - `type: :error`

          - `:error`

      - `type: :errored`

        - `:errored`

    - `class BetaMessageBatchCanceledResult`

      - `type: :canceled`

        - `:canceled`

    - `class BetaMessageBatchExpiredResult`

      - `type: :expired`

        - `:expired`

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

beta_message_batch_individual_response = anthropic.beta.messages.batches.results("message_batch_id")

puts(beta_message_batch_individual_response)
```

## Domain Types

### Beta Deleted Message Batch

- `class BetaDeletedMessageBatch`

  - `id: String`

    ID of the Message Batch.

  - `type: :message_batch_deleted`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `:message_batch_deleted`

### Beta Message Batch

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

### Beta Message Batch Canceled Result

- `class BetaMessageBatchCanceledResult`

  - `type: :canceled`

    - `:canceled`

### Beta Message Batch Errored Result

- `class BetaMessageBatchErroredResult`

  - `error: BetaErrorResponse`

    - `error: BetaError`

      - `class BetaInvalidRequestError`

        - `message: String`

        - `type: :invalid_request_error`

          - `:invalid_request_error`

      - `class BetaAuthenticationError`

        - `message: String`

        - `type: :authentication_error`

          - `:authentication_error`

      - `class BetaBillingError`

        - `message: String`

        - `type: :billing_error`

          - `:billing_error`

      - `class BetaPermissionError`

        - `message: String`

        - `type: :permission_error`

          - `:permission_error`

      - `class BetaNotFoundError`

        - `message: String`

        - `type: :not_found_error`

          - `:not_found_error`

      - `class BetaRateLimitError`

        - `message: String`

        - `type: :rate_limit_error`

          - `:rate_limit_error`

      - `class BetaGatewayTimeoutError`

        - `message: String`

        - `type: :timeout_error`

          - `:timeout_error`

      - `class BetaAPIError`

        - `message: String`

        - `type: :api_error`

          - `:api_error`

      - `class BetaOverloadedError`

        - `message: String`

        - `type: :overloaded_error`

          - `:overloaded_error`

    - `request_id: String`

    - `type: :error`

      - `:error`

  - `type: :errored`

    - `:errored`

### Beta Message Batch Expired Result

- `class BetaMessageBatchExpiredResult`

  - `type: :expired`

    - `:expired`

### Beta Message Batch Individual Response

- `class BetaMessageBatchIndividualResponse`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `custom_id: String`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: BetaMessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `class BetaMessageBatchSucceededResult`

      - `message: BetaMessage`

        - `id: String`

          Unique object identifier.

          The format and length of IDs may change over time.

        - `container: BetaContainer`

          Information about the container used in the request (for the code execution tool)

          - `id: String`

            Identifier for the container used in this request

          - `expires_at: Time`

            The time at which the container will expire.

          - `skills: Array[BetaSkill]`

            Skills loaded in the container

            - `skill_id: String`

              Skill ID

            - `type: :anthropic | :custom`

              Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

              - `:anthropic`

              - `:custom`

            - `version: String`

              Skill version or 'latest' for most recent version

        - `content: Array[BetaContentBlock]`

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

          - `class BetaTextBlock`

            - `citations: Array[BetaTextCitation]`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class BetaCitationCharLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_char_index: Integer`

                - `file_id: String`

                - `start_char_index: Integer`

                - `type: :char_location`

                  - `:char_location`

              - `class BetaCitationPageLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_page_number: Integer`

                - `file_id: String`

                - `start_page_number: Integer`

                - `type: :page_location`

                  - `:page_location`

              - `class BetaCitationContentBlockLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_block_index: Integer`

                - `file_id: String`

                - `start_block_index: Integer`

                - `type: :content_block_location`

                  - `:content_block_location`

              - `class BetaCitationsWebSearchResultLocation`

                - `cited_text: String`

                - `encrypted_index: String`

                - `title: String`

                - `type: :web_search_result_location`

                  - `:web_search_result_location`

                - `url: String`

              - `class BetaCitationSearchResultLocation`

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

          - `class BetaThinkingBlock`

            - `signature: String`

            - `thinking: String`

            - `type: :thinking`

              - `:thinking`

          - `class BetaRedactedThinkingBlock`

            - `data: String`

            - `type: :redacted_thinking`

              - `:redacted_thinking`

          - `class BetaToolUseBlock`

            - `id: String`

            - `input: Hash[Symbol, untyped]`

            - `name: String`

            - `type: :tool_use`

              - `:tool_use`

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

          - `class BetaServerToolUseBlock`

            - `id: String`

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

          - `class BetaWebSearchToolResultBlock`

            - `content: BetaWebSearchToolResultBlockContent`

              - `class BetaWebSearchToolResultError`

                - `error_code: BetaWebSearchToolResultErrorCode`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:max_uses_exceeded`

                  - `:too_many_requests`

                  - `:query_too_long`

                - `type: :web_search_tool_result_error`

                  - `:web_search_tool_result_error`

              - `Array[BetaWebSearchResultBlock]`

                - `encrypted_content: String`

                - `page_age: String`

                - `title: String`

                - `type: :web_search_result`

                  - `:web_search_result`

                - `url: String`

            - `tool_use_id: String`

            - `type: :web_search_tool_result`

              - `:web_search_tool_result`

          - `class BetaWebFetchToolResultBlock`

            - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

              - `class BetaWebFetchToolResultErrorBlock`

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

              - `class BetaWebFetchBlock`

                - `content: BetaDocumentBlock`

                  - `citations: BetaCitationConfig`

                    Citation configuration for the document

                    - `enabled: bool`

                  - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

                  - `title: String`

                    The title of the document

                  - `type: :document`

                    - `:document`

                - `retrieved_at: String`

                  ISO 8601 timestamp when the content was retrieved

                - `type: :web_fetch_result`

                  - `:web_fetch_result`

                - `url: String`

                  Fetched content URL

            - `tool_use_id: String`

            - `type: :web_fetch_tool_result`

              - `:web_fetch_tool_result`

          - `class BetaCodeExecutionToolResultBlock`

            - `content: BetaCodeExecutionToolResultBlockContent`

              - `class BetaCodeExecutionToolResultError`

                - `error_code: BetaCodeExecutionToolResultErrorCode`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:too_many_requests`

                  - `:execution_time_exceeded`

                - `type: :code_execution_tool_result_error`

                  - `:code_execution_tool_result_error`

              - `class BetaCodeExecutionResultBlock`

                - `content: Array[BetaCodeExecutionOutputBlock]`

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

          - `class BetaBashCodeExecutionToolResultBlock`

            - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

              - `class BetaBashCodeExecutionToolResultError`

                - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:too_many_requests`

                  - `:execution_time_exceeded`

                  - `:output_file_too_large`

                - `type: :bash_code_execution_tool_result_error`

                  - `:bash_code_execution_tool_result_error`

              - `class BetaBashCodeExecutionResultBlock`

                - `content: Array[BetaBashCodeExecutionOutputBlock]`

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

          - `class BetaTextEditorCodeExecutionToolResultBlock`

            - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

              - `class BetaTextEditorCodeExecutionToolResultError`

                - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:too_many_requests`

                  - `:execution_time_exceeded`

                  - `:file_not_found`

                - `error_message: String`

                - `type: :text_editor_code_execution_tool_result_error`

                  - `:text_editor_code_execution_tool_result_error`

              - `class BetaTextEditorCodeExecutionViewResultBlock`

                - `content: String`

                - `file_type: :text | :image | :pdf`

                  - `:text`

                  - `:image`

                  - `:pdf`

                - `num_lines: Integer`

                - `start_line: Integer`

                - `total_lines: Integer`

                - `type: :text_editor_code_execution_view_result`

                  - `:text_editor_code_execution_view_result`

              - `class BetaTextEditorCodeExecutionCreateResultBlock`

                - `is_file_update: bool`

                - `type: :text_editor_code_execution_create_result`

                  - `:text_editor_code_execution_create_result`

              - `class BetaTextEditorCodeExecutionStrReplaceResultBlock`

                - `lines: Array[String]`

                - `new_lines: Integer`

                - `new_start: Integer`

                - `old_lines: Integer`

                - `old_start: Integer`

                - `type: :text_editor_code_execution_str_replace_result`

                  - `:text_editor_code_execution_str_replace_result`

            - `tool_use_id: String`

            - `type: :text_editor_code_execution_tool_result`

              - `:text_editor_code_execution_tool_result`

          - `class BetaToolSearchToolResultBlock`

            - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

              - `class BetaToolSearchToolResultError`

                - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

                  - `:invalid_tool_input`

                  - `:unavailable`

                  - `:too_many_requests`

                  - `:execution_time_exceeded`

                - `error_message: String`

                - `type: :tool_search_tool_result_error`

                  - `:tool_search_tool_result_error`

              - `class BetaToolSearchToolSearchResultBlock`

                - `tool_references: Array[BetaToolReferenceBlock]`

                  - `tool_name: String`

                  - `type: :tool_reference`

                    - `:tool_reference`

                - `type: :tool_search_tool_search_result`

                  - `:tool_search_tool_search_result`

            - `tool_use_id: String`

            - `type: :tool_search_tool_result`

              - `:tool_search_tool_result`

          - `class BetaMCPToolUseBlock`

            - `id: String`

            - `input: Hash[Symbol, untyped]`

            - `name: String`

              The name of the MCP tool

            - `server_name: String`

              The name of the MCP server

            - `type: :mcp_tool_use`

              - `:mcp_tool_use`

          - `class BetaMCPToolResultBlock`

            - `content: String | Array[BetaTextBlock]`

              - `String`

              - `Array[BetaTextBlock]`

                - `citations: Array[BetaTextCitation]`

                  Citations supporting the text block.

                  The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

                  - `class BetaCitationCharLocation`

                    - `cited_text: String`

                    - `document_index: Integer`

                    - `document_title: String`

                    - `end_char_index: Integer`

                    - `file_id: String`

                    - `start_char_index: Integer`

                    - `type: :char_location`

                      - `:char_location`

                  - `class BetaCitationPageLocation`

                    - `cited_text: String`

                    - `document_index: Integer`

                    - `document_title: String`

                    - `end_page_number: Integer`

                    - `file_id: String`

                    - `start_page_number: Integer`

                    - `type: :page_location`

                      - `:page_location`

                  - `class BetaCitationContentBlockLocation`

                    - `cited_text: String`

                    - `document_index: Integer`

                    - `document_title: String`

                    - `end_block_index: Integer`

                    - `file_id: String`

                    - `start_block_index: Integer`

                    - `type: :content_block_location`

                      - `:content_block_location`

                  - `class BetaCitationsWebSearchResultLocation`

                    - `cited_text: String`

                    - `encrypted_index: String`

                    - `title: String`

                    - `type: :web_search_result_location`

                      - `:web_search_result_location`

                    - `url: String`

                  - `class BetaCitationSearchResultLocation`

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

            - `is_error: bool`

            - `tool_use_id: String`

            - `type: :mcp_tool_result`

              - `:mcp_tool_result`

          - `class BetaContainerUploadBlock`

            Response model for a file uploaded to the container.

            - `file_id: String`

            - `type: :container_upload`

              - `:container_upload`

        - `context_management: BetaContextManagementResponse`

          Context management response.

          Information about context management strategies applied during the request.

          - `applied_edits: Array[BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse]`

            List of context management edits that were applied.

            - `class BetaClearToolUses20250919EditResponse`

              - `cleared_input_tokens: Integer`

                Number of input tokens cleared by this edit.

              - `cleared_tool_uses: Integer`

                Number of tool uses that were cleared.

              - `type: :clear_tool_uses_20250919`

                The type of context management edit applied.

                - `:clear_tool_uses_20250919`

            - `class BetaClearThinking20251015EditResponse`

              - `cleared_input_tokens: Integer`

                Number of input tokens cleared by this edit.

              - `cleared_thinking_turns: Integer`

                Number of thinking turns that were cleared.

              - `type: :clear_thinking_20251015`

                The type of context management edit applied.

                - `:clear_thinking_20251015`

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

        - `stop_reason: BetaStopReason`

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

          - `:model_context_window_exceeded`

        - `stop_sequence: String`

          Which custom stop sequence was generated, if any.

          This value will be a non-null string if one of your custom stop sequences was generated.

        - `type: :message`

          Object type.

          For Messages, this is always `"message"`.

          - `:message`

        - `usage: BetaUsage`

          Billing and rate-limit usage.

          Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

          Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

          For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

          Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

          - `cache_creation: BetaCacheCreation`

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

          - `server_tool_use: BetaServerToolUsage`

            The number of server tool requests.

            - `web_fetch_requests: Integer`

              The number of web fetch tool requests.

            - `web_search_requests: Integer`

              The number of web search tool requests.

          - `service_tier: :standard | :priority | :batch`

            If the request used the priority, standard, or batch tier.

            - `:standard`

            - `:priority`

            - `:batch`

      - `type: :succeeded`

        - `:succeeded`

    - `class BetaMessageBatchErroredResult`

      - `error: BetaErrorResponse`

        - `error: BetaError`

          - `class BetaInvalidRequestError`

            - `message: String`

            - `type: :invalid_request_error`

              - `:invalid_request_error`

          - `class BetaAuthenticationError`

            - `message: String`

            - `type: :authentication_error`

              - `:authentication_error`

          - `class BetaBillingError`

            - `message: String`

            - `type: :billing_error`

              - `:billing_error`

          - `class BetaPermissionError`

            - `message: String`

            - `type: :permission_error`

              - `:permission_error`

          - `class BetaNotFoundError`

            - `message: String`

            - `type: :not_found_error`

              - `:not_found_error`

          - `class BetaRateLimitError`

            - `message: String`

            - `type: :rate_limit_error`

              - `:rate_limit_error`

          - `class BetaGatewayTimeoutError`

            - `message: String`

            - `type: :timeout_error`

              - `:timeout_error`

          - `class BetaAPIError`

            - `message: String`

            - `type: :api_error`

              - `:api_error`

          - `class BetaOverloadedError`

            - `message: String`

            - `type: :overloaded_error`

              - `:overloaded_error`

        - `request_id: String`

        - `type: :error`

          - `:error`

      - `type: :errored`

        - `:errored`

    - `class BetaMessageBatchCanceledResult`

      - `type: :canceled`

        - `:canceled`

    - `class BetaMessageBatchExpiredResult`

      - `type: :expired`

        - `:expired`

### Beta Message Batch Request Counts

- `class BetaMessageBatchRequestCounts`

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

### Beta Message Batch Result

- `BetaMessageBatchResult = BetaMessageBatchSucceededResult | BetaMessageBatchErroredResult | BetaMessageBatchCanceledResult | BetaMessageBatchExpiredResult`

  Processing result for this request.

  Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

  - `class BetaMessageBatchSucceededResult`

    - `message: BetaMessage`

      - `id: String`

        Unique object identifier.

        The format and length of IDs may change over time.

      - `container: BetaContainer`

        Information about the container used in the request (for the code execution tool)

        - `id: String`

          Identifier for the container used in this request

        - `expires_at: Time`

          The time at which the container will expire.

        - `skills: Array[BetaSkill]`

          Skills loaded in the container

          - `skill_id: String`

            Skill ID

          - `type: :anthropic | :custom`

            Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

            - `:anthropic`

            - `:custom`

          - `version: String`

            Skill version or 'latest' for most recent version

      - `content: Array[BetaContentBlock]`

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

        - `class BetaTextBlock`

          - `citations: Array[BetaTextCitation]`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `class BetaCitationCharLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_char_index: Integer`

              - `file_id: String`

              - `start_char_index: Integer`

              - `type: :char_location`

                - `:char_location`

            - `class BetaCitationPageLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_page_number: Integer`

              - `file_id: String`

              - `start_page_number: Integer`

              - `type: :page_location`

                - `:page_location`

            - `class BetaCitationContentBlockLocation`

              - `cited_text: String`

              - `document_index: Integer`

              - `document_title: String`

              - `end_block_index: Integer`

              - `file_id: String`

              - `start_block_index: Integer`

              - `type: :content_block_location`

                - `:content_block_location`

            - `class BetaCitationsWebSearchResultLocation`

              - `cited_text: String`

              - `encrypted_index: String`

              - `title: String`

              - `type: :web_search_result_location`

                - `:web_search_result_location`

              - `url: String`

            - `class BetaCitationSearchResultLocation`

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

        - `class BetaThinkingBlock`

          - `signature: String`

          - `thinking: String`

          - `type: :thinking`

            - `:thinking`

        - `class BetaRedactedThinkingBlock`

          - `data: String`

          - `type: :redacted_thinking`

            - `:redacted_thinking`

        - `class BetaToolUseBlock`

          - `id: String`

          - `input: Hash[Symbol, untyped]`

          - `name: String`

          - `type: :tool_use`

            - `:tool_use`

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

        - `class BetaServerToolUseBlock`

          - `id: String`

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

        - `class BetaWebSearchToolResultBlock`

          - `content: BetaWebSearchToolResultBlockContent`

            - `class BetaWebSearchToolResultError`

              - `error_code: BetaWebSearchToolResultErrorCode`

                - `:invalid_tool_input`

                - `:unavailable`

                - `:max_uses_exceeded`

                - `:too_many_requests`

                - `:query_too_long`

              - `type: :web_search_tool_result_error`

                - `:web_search_tool_result_error`

            - `Array[BetaWebSearchResultBlock]`

              - `encrypted_content: String`

              - `page_age: String`

              - `title: String`

              - `type: :web_search_result`

                - `:web_search_result`

              - `url: String`

          - `tool_use_id: String`

          - `type: :web_search_tool_result`

            - `:web_search_tool_result`

        - `class BetaWebFetchToolResultBlock`

          - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

            - `class BetaWebFetchToolResultErrorBlock`

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

            - `class BetaWebFetchBlock`

              - `content: BetaDocumentBlock`

                - `citations: BetaCitationConfig`

                  Citation configuration for the document

                  - `enabled: bool`

                - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

                - `title: String`

                  The title of the document

                - `type: :document`

                  - `:document`

              - `retrieved_at: String`

                ISO 8601 timestamp when the content was retrieved

              - `type: :web_fetch_result`

                - `:web_fetch_result`

              - `url: String`

                Fetched content URL

          - `tool_use_id: String`

          - `type: :web_fetch_tool_result`

            - `:web_fetch_tool_result`

        - `class BetaCodeExecutionToolResultBlock`

          - `content: BetaCodeExecutionToolResultBlockContent`

            - `class BetaCodeExecutionToolResultError`

              - `error_code: BetaCodeExecutionToolResultErrorCode`

                - `:invalid_tool_input`

                - `:unavailable`

                - `:too_many_requests`

                - `:execution_time_exceeded`

              - `type: :code_execution_tool_result_error`

                - `:code_execution_tool_result_error`

            - `class BetaCodeExecutionResultBlock`

              - `content: Array[BetaCodeExecutionOutputBlock]`

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

        - `class BetaBashCodeExecutionToolResultBlock`

          - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

            - `class BetaBashCodeExecutionToolResultError`

              - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

                - `:invalid_tool_input`

                - `:unavailable`

                - `:too_many_requests`

                - `:execution_time_exceeded`

                - `:output_file_too_large`

              - `type: :bash_code_execution_tool_result_error`

                - `:bash_code_execution_tool_result_error`

            - `class BetaBashCodeExecutionResultBlock`

              - `content: Array[BetaBashCodeExecutionOutputBlock]`

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

        - `class BetaTextEditorCodeExecutionToolResultBlock`

          - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

            - `class BetaTextEditorCodeExecutionToolResultError`

              - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

                - `:invalid_tool_input`

                - `:unavailable`

                - `:too_many_requests`

                - `:execution_time_exceeded`

                - `:file_not_found`

              - `error_message: String`

              - `type: :text_editor_code_execution_tool_result_error`

                - `:text_editor_code_execution_tool_result_error`

            - `class BetaTextEditorCodeExecutionViewResultBlock`

              - `content: String`

              - `file_type: :text | :image | :pdf`

                - `:text`

                - `:image`

                - `:pdf`

              - `num_lines: Integer`

              - `start_line: Integer`

              - `total_lines: Integer`

              - `type: :text_editor_code_execution_view_result`

                - `:text_editor_code_execution_view_result`

            - `class BetaTextEditorCodeExecutionCreateResultBlock`

              - `is_file_update: bool`

              - `type: :text_editor_code_execution_create_result`

                - `:text_editor_code_execution_create_result`

            - `class BetaTextEditorCodeExecutionStrReplaceResultBlock`

              - `lines: Array[String]`

              - `new_lines: Integer`

              - `new_start: Integer`

              - `old_lines: Integer`

              - `old_start: Integer`

              - `type: :text_editor_code_execution_str_replace_result`

                - `:text_editor_code_execution_str_replace_result`

          - `tool_use_id: String`

          - `type: :text_editor_code_execution_tool_result`

            - `:text_editor_code_execution_tool_result`

        - `class BetaToolSearchToolResultBlock`

          - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

            - `class BetaToolSearchToolResultError`

              - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

                - `:invalid_tool_input`

                - `:unavailable`

                - `:too_many_requests`

                - `:execution_time_exceeded`

              - `error_message: String`

              - `type: :tool_search_tool_result_error`

                - `:tool_search_tool_result_error`

            - `class BetaToolSearchToolSearchResultBlock`

              - `tool_references: Array[BetaToolReferenceBlock]`

                - `tool_name: String`

                - `type: :tool_reference`

                  - `:tool_reference`

              - `type: :tool_search_tool_search_result`

                - `:tool_search_tool_search_result`

          - `tool_use_id: String`

          - `type: :tool_search_tool_result`

            - `:tool_search_tool_result`

        - `class BetaMCPToolUseBlock`

          - `id: String`

          - `input: Hash[Symbol, untyped]`

          - `name: String`

            The name of the MCP tool

          - `server_name: String`

            The name of the MCP server

          - `type: :mcp_tool_use`

            - `:mcp_tool_use`

        - `class BetaMCPToolResultBlock`

          - `content: String | Array[BetaTextBlock]`

            - `String`

            - `Array[BetaTextBlock]`

              - `citations: Array[BetaTextCitation]`

                Citations supporting the text block.

                The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

                - `class BetaCitationCharLocation`

                  - `cited_text: String`

                  - `document_index: Integer`

                  - `document_title: String`

                  - `end_char_index: Integer`

                  - `file_id: String`

                  - `start_char_index: Integer`

                  - `type: :char_location`

                    - `:char_location`

                - `class BetaCitationPageLocation`

                  - `cited_text: String`

                  - `document_index: Integer`

                  - `document_title: String`

                  - `end_page_number: Integer`

                  - `file_id: String`

                  - `start_page_number: Integer`

                  - `type: :page_location`

                    - `:page_location`

                - `class BetaCitationContentBlockLocation`

                  - `cited_text: String`

                  - `document_index: Integer`

                  - `document_title: String`

                  - `end_block_index: Integer`

                  - `file_id: String`

                  - `start_block_index: Integer`

                  - `type: :content_block_location`

                    - `:content_block_location`

                - `class BetaCitationsWebSearchResultLocation`

                  - `cited_text: String`

                  - `encrypted_index: String`

                  - `title: String`

                  - `type: :web_search_result_location`

                    - `:web_search_result_location`

                  - `url: String`

                - `class BetaCitationSearchResultLocation`

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

          - `is_error: bool`

          - `tool_use_id: String`

          - `type: :mcp_tool_result`

            - `:mcp_tool_result`

        - `class BetaContainerUploadBlock`

          Response model for a file uploaded to the container.

          - `file_id: String`

          - `type: :container_upload`

            - `:container_upload`

      - `context_management: BetaContextManagementResponse`

        Context management response.

        Information about context management strategies applied during the request.

        - `applied_edits: Array[BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse]`

          List of context management edits that were applied.

          - `class BetaClearToolUses20250919EditResponse`

            - `cleared_input_tokens: Integer`

              Number of input tokens cleared by this edit.

            - `cleared_tool_uses: Integer`

              Number of tool uses that were cleared.

            - `type: :clear_tool_uses_20250919`

              The type of context management edit applied.

              - `:clear_tool_uses_20250919`

          - `class BetaClearThinking20251015EditResponse`

            - `cleared_input_tokens: Integer`

              Number of input tokens cleared by this edit.

            - `cleared_thinking_turns: Integer`

              Number of thinking turns that were cleared.

            - `type: :clear_thinking_20251015`

              The type of context management edit applied.

              - `:clear_thinking_20251015`

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

      - `stop_reason: BetaStopReason`

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

        - `:model_context_window_exceeded`

      - `stop_sequence: String`

        Which custom stop sequence was generated, if any.

        This value will be a non-null string if one of your custom stop sequences was generated.

      - `type: :message`

        Object type.

        For Messages, this is always `"message"`.

        - `:message`

      - `usage: BetaUsage`

        Billing and rate-limit usage.

        Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

        Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

        For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

        Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

        - `cache_creation: BetaCacheCreation`

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

        - `server_tool_use: BetaServerToolUsage`

          The number of server tool requests.

          - `web_fetch_requests: Integer`

            The number of web fetch tool requests.

          - `web_search_requests: Integer`

            The number of web search tool requests.

        - `service_tier: :standard | :priority | :batch`

          If the request used the priority, standard, or batch tier.

          - `:standard`

          - `:priority`

          - `:batch`

    - `type: :succeeded`

      - `:succeeded`

  - `class BetaMessageBatchErroredResult`

    - `error: BetaErrorResponse`

      - `error: BetaError`

        - `class BetaInvalidRequestError`

          - `message: String`

          - `type: :invalid_request_error`

            - `:invalid_request_error`

        - `class BetaAuthenticationError`

          - `message: String`

          - `type: :authentication_error`

            - `:authentication_error`

        - `class BetaBillingError`

          - `message: String`

          - `type: :billing_error`

            - `:billing_error`

        - `class BetaPermissionError`

          - `message: String`

          - `type: :permission_error`

            - `:permission_error`

        - `class BetaNotFoundError`

          - `message: String`

          - `type: :not_found_error`

            - `:not_found_error`

        - `class BetaRateLimitError`

          - `message: String`

          - `type: :rate_limit_error`

            - `:rate_limit_error`

        - `class BetaGatewayTimeoutError`

          - `message: String`

          - `type: :timeout_error`

            - `:timeout_error`

        - `class BetaAPIError`

          - `message: String`

          - `type: :api_error`

            - `:api_error`

        - `class BetaOverloadedError`

          - `message: String`

          - `type: :overloaded_error`

            - `:overloaded_error`

      - `request_id: String`

      - `type: :error`

        - `:error`

    - `type: :errored`

      - `:errored`

  - `class BetaMessageBatchCanceledResult`

    - `type: :canceled`

      - `:canceled`

  - `class BetaMessageBatchExpiredResult`

    - `type: :expired`

      - `:expired`

### Beta Message Batch Succeeded Result

- `class BetaMessageBatchSucceededResult`

  - `message: BetaMessage`

    - `id: String`

      Unique object identifier.

      The format and length of IDs may change over time.

    - `container: BetaContainer`

      Information about the container used in the request (for the code execution tool)

      - `id: String`

        Identifier for the container used in this request

      - `expires_at: Time`

        The time at which the container will expire.

      - `skills: Array[BetaSkill]`

        Skills loaded in the container

        - `skill_id: String`

          Skill ID

        - `type: :anthropic | :custom`

          Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

          - `:anthropic`

          - `:custom`

        - `version: String`

          Skill version or 'latest' for most recent version

    - `content: Array[BetaContentBlock]`

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

      - `class BetaTextBlock`

        - `citations: Array[BetaTextCitation]`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `class BetaCitationCharLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_char_index: Integer`

            - `file_id: String`

            - `start_char_index: Integer`

            - `type: :char_location`

              - `:char_location`

          - `class BetaCitationPageLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_page_number: Integer`

            - `file_id: String`

            - `start_page_number: Integer`

            - `type: :page_location`

              - `:page_location`

          - `class BetaCitationContentBlockLocation`

            - `cited_text: String`

            - `document_index: Integer`

            - `document_title: String`

            - `end_block_index: Integer`

            - `file_id: String`

            - `start_block_index: Integer`

            - `type: :content_block_location`

              - `:content_block_location`

          - `class BetaCitationsWebSearchResultLocation`

            - `cited_text: String`

            - `encrypted_index: String`

            - `title: String`

            - `type: :web_search_result_location`

              - `:web_search_result_location`

            - `url: String`

          - `class BetaCitationSearchResultLocation`

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

      - `class BetaThinkingBlock`

        - `signature: String`

        - `thinking: String`

        - `type: :thinking`

          - `:thinking`

      - `class BetaRedactedThinkingBlock`

        - `data: String`

        - `type: :redacted_thinking`

          - `:redacted_thinking`

      - `class BetaToolUseBlock`

        - `id: String`

        - `input: Hash[Symbol, untyped]`

        - `name: String`

        - `type: :tool_use`

          - `:tool_use`

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

      - `class BetaServerToolUseBlock`

        - `id: String`

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

      - `class BetaWebSearchToolResultBlock`

        - `content: BetaWebSearchToolResultBlockContent`

          - `class BetaWebSearchToolResultError`

            - `error_code: BetaWebSearchToolResultErrorCode`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:max_uses_exceeded`

              - `:too_many_requests`

              - `:query_too_long`

            - `type: :web_search_tool_result_error`

              - `:web_search_tool_result_error`

          - `Array[BetaWebSearchResultBlock]`

            - `encrypted_content: String`

            - `page_age: String`

            - `title: String`

            - `type: :web_search_result`

              - `:web_search_result`

            - `url: String`

        - `tool_use_id: String`

        - `type: :web_search_tool_result`

          - `:web_search_tool_result`

      - `class BetaWebFetchToolResultBlock`

        - `content: BetaWebFetchToolResultErrorBlock | BetaWebFetchBlock`

          - `class BetaWebFetchToolResultErrorBlock`

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

          - `class BetaWebFetchBlock`

            - `content: BetaDocumentBlock`

              - `citations: BetaCitationConfig`

                Citation configuration for the document

                - `enabled: bool`

              - `source: BetaBase64PDFSource | BetaPlainTextSource`

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

              - `title: String`

                The title of the document

              - `type: :document`

                - `:document`

            - `retrieved_at: String`

              ISO 8601 timestamp when the content was retrieved

            - `type: :web_fetch_result`

              - `:web_fetch_result`

            - `url: String`

              Fetched content URL

        - `tool_use_id: String`

        - `type: :web_fetch_tool_result`

          - `:web_fetch_tool_result`

      - `class BetaCodeExecutionToolResultBlock`

        - `content: BetaCodeExecutionToolResultBlockContent`

          - `class BetaCodeExecutionToolResultError`

            - `error_code: BetaCodeExecutionToolResultErrorCode`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:too_many_requests`

              - `:execution_time_exceeded`

            - `type: :code_execution_tool_result_error`

              - `:code_execution_tool_result_error`

          - `class BetaCodeExecutionResultBlock`

            - `content: Array[BetaCodeExecutionOutputBlock]`

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

      - `class BetaBashCodeExecutionToolResultBlock`

        - `content: BetaBashCodeExecutionToolResultError | BetaBashCodeExecutionResultBlock`

          - `class BetaBashCodeExecutionToolResultError`

            - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:too_many_requests`

              - `:execution_time_exceeded`

              - `:output_file_too_large`

            - `type: :bash_code_execution_tool_result_error`

              - `:bash_code_execution_tool_result_error`

          - `class BetaBashCodeExecutionResultBlock`

            - `content: Array[BetaBashCodeExecutionOutputBlock]`

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

      - `class BetaTextEditorCodeExecutionToolResultBlock`

        - `content: BetaTextEditorCodeExecutionToolResultError | BetaTextEditorCodeExecutionViewResultBlock | BetaTextEditorCodeExecutionCreateResultBlock | BetaTextEditorCodeExecutionStrReplaceResultBlock`

          - `class BetaTextEditorCodeExecutionToolResultError`

            - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | 2 more`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:too_many_requests`

              - `:execution_time_exceeded`

              - `:file_not_found`

            - `error_message: String`

            - `type: :text_editor_code_execution_tool_result_error`

              - `:text_editor_code_execution_tool_result_error`

          - `class BetaTextEditorCodeExecutionViewResultBlock`

            - `content: String`

            - `file_type: :text | :image | :pdf`

              - `:text`

              - `:image`

              - `:pdf`

            - `num_lines: Integer`

            - `start_line: Integer`

            - `total_lines: Integer`

            - `type: :text_editor_code_execution_view_result`

              - `:text_editor_code_execution_view_result`

          - `class BetaTextEditorCodeExecutionCreateResultBlock`

            - `is_file_update: bool`

            - `type: :text_editor_code_execution_create_result`

              - `:text_editor_code_execution_create_result`

          - `class BetaTextEditorCodeExecutionStrReplaceResultBlock`

            - `lines: Array[String]`

            - `new_lines: Integer`

            - `new_start: Integer`

            - `old_lines: Integer`

            - `old_start: Integer`

            - `type: :text_editor_code_execution_str_replace_result`

              - `:text_editor_code_execution_str_replace_result`

        - `tool_use_id: String`

        - `type: :text_editor_code_execution_tool_result`

          - `:text_editor_code_execution_tool_result`

      - `class BetaToolSearchToolResultBlock`

        - `content: BetaToolSearchToolResultError | BetaToolSearchToolSearchResultBlock`

          - `class BetaToolSearchToolResultError`

            - `error_code: :invalid_tool_input | :unavailable | :too_many_requests | :execution_time_exceeded`

              - `:invalid_tool_input`

              - `:unavailable`

              - `:too_many_requests`

              - `:execution_time_exceeded`

            - `error_message: String`

            - `type: :tool_search_tool_result_error`

              - `:tool_search_tool_result_error`

          - `class BetaToolSearchToolSearchResultBlock`

            - `tool_references: Array[BetaToolReferenceBlock]`

              - `tool_name: String`

              - `type: :tool_reference`

                - `:tool_reference`

            - `type: :tool_search_tool_search_result`

              - `:tool_search_tool_search_result`

        - `tool_use_id: String`

        - `type: :tool_search_tool_result`

          - `:tool_search_tool_result`

      - `class BetaMCPToolUseBlock`

        - `id: String`

        - `input: Hash[Symbol, untyped]`

        - `name: String`

          The name of the MCP tool

        - `server_name: String`

          The name of the MCP server

        - `type: :mcp_tool_use`

          - `:mcp_tool_use`

      - `class BetaMCPToolResultBlock`

        - `content: String | Array[BetaTextBlock]`

          - `String`

          - `Array[BetaTextBlock]`

            - `citations: Array[BetaTextCitation]`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `class BetaCitationCharLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_char_index: Integer`

                - `file_id: String`

                - `start_char_index: Integer`

                - `type: :char_location`

                  - `:char_location`

              - `class BetaCitationPageLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_page_number: Integer`

                - `file_id: String`

                - `start_page_number: Integer`

                - `type: :page_location`

                  - `:page_location`

              - `class BetaCitationContentBlockLocation`

                - `cited_text: String`

                - `document_index: Integer`

                - `document_title: String`

                - `end_block_index: Integer`

                - `file_id: String`

                - `start_block_index: Integer`

                - `type: :content_block_location`

                  - `:content_block_location`

              - `class BetaCitationsWebSearchResultLocation`

                - `cited_text: String`

                - `encrypted_index: String`

                - `title: String`

                - `type: :web_search_result_location`

                  - `:web_search_result_location`

                - `url: String`

              - `class BetaCitationSearchResultLocation`

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

        - `is_error: bool`

        - `tool_use_id: String`

        - `type: :mcp_tool_result`

          - `:mcp_tool_result`

      - `class BetaContainerUploadBlock`

        Response model for a file uploaded to the container.

        - `file_id: String`

        - `type: :container_upload`

          - `:container_upload`

    - `context_management: BetaContextManagementResponse`

      Context management response.

      Information about context management strategies applied during the request.

      - `applied_edits: Array[BetaClearToolUses20250919EditResponse | BetaClearThinking20251015EditResponse]`

        List of context management edits that were applied.

        - `class BetaClearToolUses20250919EditResponse`

          - `cleared_input_tokens: Integer`

            Number of input tokens cleared by this edit.

          - `cleared_tool_uses: Integer`

            Number of tool uses that were cleared.

          - `type: :clear_tool_uses_20250919`

            The type of context management edit applied.

            - `:clear_tool_uses_20250919`

        - `class BetaClearThinking20251015EditResponse`

          - `cleared_input_tokens: Integer`

            Number of input tokens cleared by this edit.

          - `cleared_thinking_turns: Integer`

            Number of thinking turns that were cleared.

          - `type: :clear_thinking_20251015`

            The type of context management edit applied.

            - `:clear_thinking_20251015`

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

    - `stop_reason: BetaStopReason`

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

      - `:model_context_window_exceeded`

    - `stop_sequence: String`

      Which custom stop sequence was generated, if any.

      This value will be a non-null string if one of your custom stop sequences was generated.

    - `type: :message`

      Object type.

      For Messages, this is always `"message"`.

      - `:message`

    - `usage: BetaUsage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cache_creation: BetaCacheCreation`

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

      - `server_tool_use: BetaServerToolUsage`

        The number of server tool requests.

        - `web_fetch_requests: Integer`

          The number of web fetch tool requests.

        - `web_search_requests: Integer`

          The number of web search tool requests.

      - `service_tier: :standard | :priority | :batch`

        If the request used the priority, standard, or batch tier.

        - `:standard`

        - `:priority`

        - `:batch`

  - `type: :succeeded`

    - `:succeeded`
