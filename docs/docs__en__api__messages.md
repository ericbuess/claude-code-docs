# Messages

## Create

**post** `/v1/messages`

Send a structured list of input messages with text and/or image content, and the model will generate the next message in the conversation.

The Messages API can be used for either single queries or stateless multi-turn conversations.

Learn more about the Messages API in our [user guide](https://docs.claude.com/en/docs/initial-setup)

### Body Parameters

- `max_tokens: number`

  The maximum number of tokens to generate before stopping.

  Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

  Different models have different maximum values for this parameter.  See [models](https://docs.claude.com/en/docs/models-overview) for details.

- `messages: array of MessageParam`

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

  - `content: string or array of ContentBlockParam`

    - `UnionMember0 = string`

    - `UnionMember1 = array of ContentBlockParam`

      - `TextBlockParam = object { text, type, cache_control, citations }`

        - `text: string`

        - `type: "text"`

          - `"text"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional array of TextCitationParam`

          - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_char_index: number`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_page_number: number`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_block_index: number`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string`

            - `type: "search_result_location"`

              - `"search_result_location"`

      - `ImageBlockParam = object { source, type, cache_control }`

        - `source: Base64ImageSource or URLImageSource`

          - `Base64ImageSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

              - `"image/jpeg"`

              - `"image/png"`

              - `"image/gif"`

              - `"image/webp"`

            - `type: "base64"`

              - `"base64"`

          - `URLImageSource = object { type, url }`

            - `type: "url"`

              - `"url"`

            - `url: string`

        - `type: "image"`

          - `"image"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

      - `DocumentBlockParam = object { source, type, cache_control, 3 more }`

        - `source: Base64PDFSource or PlainTextSource or ContentBlockSource or URLPDFSource`

          - `Base64PDFSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "application/pdf"`

              - `"application/pdf"`

            - `type: "base64"`

              - `"base64"`

          - `PlainTextSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "text/plain"`

              - `"text/plain"`

            - `type: "text"`

              - `"text"`

          - `ContentBlockSource = object { content, type }`

            - `content: string or array of ContentBlockSourceContent`

              - `UnionMember0 = string`

              - `ContentBlockSourceContent = array of ContentBlockSourceContent`

                - `TextBlockParam = object { text, type, cache_control, citations }`

                  - `text: string`

                  - `type: "text"`

                    - `"text"`

                  - `cache_control: optional CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: "ephemeral"`

                      - `"ephemeral"`

                    - `ttl: optional "5m" or "1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `"5m"`

                      - `"1h"`

                  - `citations: optional array of TextCitationParam`

                    - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_char_index: number`

                      - `start_char_index: number`

                      - `type: "char_location"`

                        - `"char_location"`

                    - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_page_number: number`

                      - `start_page_number: number`

                      - `type: "page_location"`

                        - `"page_location"`

                    - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_block_index: number`

                      - `start_block_index: number`

                      - `type: "content_block_location"`

                        - `"content_block_location"`

                    - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                      - `cited_text: string`

                      - `encrypted_index: string`

                      - `title: string`

                      - `type: "web_search_result_location"`

                        - `"web_search_result_location"`

                      - `url: string`

                    - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                      - `cited_text: string`

                      - `end_block_index: number`

                      - `search_result_index: number`

                      - `source: string`

                      - `start_block_index: number`

                      - `title: string`

                      - `type: "search_result_location"`

                        - `"search_result_location"`

                - `ImageBlockParam = object { source, type, cache_control }`

                  - `source: Base64ImageSource or URLImageSource`

                    - `Base64ImageSource = object { data, media_type, type }`

                      - `data: string`

                      - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                        - `"image/jpeg"`

                        - `"image/png"`

                        - `"image/gif"`

                        - `"image/webp"`

                      - `type: "base64"`

                        - `"base64"`

                    - `URLImageSource = object { type, url }`

                      - `type: "url"`

                        - `"url"`

                      - `url: string`

                  - `type: "image"`

                    - `"image"`

                  - `cache_control: optional CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: "ephemeral"`

                      - `"ephemeral"`

                    - `ttl: optional "5m" or "1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `"5m"`

                      - `"1h"`

            - `type: "content"`

              - `"content"`

          - `URLPDFSource = object { type, url }`

            - `type: "url"`

              - `"url"`

            - `url: string`

        - `type: "document"`

          - `"document"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional CitationsConfigParam`

          - `enabled: optional boolean`

        - `context: optional string`

        - `title: optional string`

      - `SearchResultBlockParam = object { content, source, title, 3 more }`

        - `content: array of TextBlockParam`

          - `text: string`

          - `type: "text"`

            - `"text"`

          - `cache_control: optional CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl: optional "5m" or "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

          - `citations: optional array of TextCitationParam`

            - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_char_index: number`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_page_number: number`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_block_index: number`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string`

              - `type: "search_result_location"`

                - `"search_result_location"`

        - `source: string`

        - `title: string`

        - `type: "search_result"`

          - `"search_result"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional CitationsConfigParam`

          - `enabled: optional boolean`

      - `ThinkingBlockParam = object { signature, thinking, type }`

        - `signature: string`

        - `thinking: string`

        - `type: "thinking"`

          - `"thinking"`

      - `RedactedThinkingBlockParam = object { data, type }`

        - `data: string`

        - `type: "redacted_thinking"`

          - `"redacted_thinking"`

      - `ToolUseBlockParam = object { id, input, name, 2 more }`

        - `id: string`

        - `input: map[unknown]`

        - `name: string`

        - `type: "tool_use"`

          - `"tool_use"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

      - `ToolResultBlockParam = object { tool_use_id, type, cache_control, 2 more }`

        - `tool_use_id: string`

        - `type: "tool_result"`

          - `"tool_result"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `content: optional string or array of TextBlockParam or ImageBlockParam or SearchResultBlockParam or DocumentBlockParam`

          - `UnionMember0 = string`

          - `UnionMember1 = array of TextBlockParam or ImageBlockParam or SearchResultBlockParam or DocumentBlockParam`

            - `TextBlockParam = object { text, type, cache_control, citations }`

              - `text: string`

              - `type: "text"`

                - `"text"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations: optional array of TextCitationParam`

                - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_char_index: number`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_page_number: number`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_block_index: number`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

            - `ImageBlockParam = object { source, type, cache_control }`

              - `source: Base64ImageSource or URLImageSource`

                - `Base64ImageSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                    - `"image/jpeg"`

                    - `"image/png"`

                    - `"image/gif"`

                    - `"image/webp"`

                  - `type: "base64"`

                    - `"base64"`

                - `URLImageSource = object { type, url }`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

              - `type: "image"`

                - `"image"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

            - `SearchResultBlockParam = object { content, source, title, 3 more }`

              - `content: array of TextBlockParam`

                - `text: string`

                - `type: "text"`

                  - `"text"`

                - `cache_control: optional CacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `type: "ephemeral"`

                    - `"ephemeral"`

                  - `ttl: optional "5m" or "1h"`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `"5m"`

                    - `"1h"`

                - `citations: optional array of TextCitationParam`

                  - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string`

                    - `end_char_index: number`

                    - `start_char_index: number`

                    - `type: "char_location"`

                      - `"char_location"`

                  - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string`

                    - `end_page_number: number`

                    - `start_page_number: number`

                    - `type: "page_location"`

                      - `"page_location"`

                  - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string`

                    - `end_block_index: number`

                    - `start_block_index: number`

                    - `type: "content_block_location"`

                      - `"content_block_location"`

                  - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                    - `cited_text: string`

                    - `encrypted_index: string`

                    - `title: string`

                    - `type: "web_search_result_location"`

                      - `"web_search_result_location"`

                    - `url: string`

                  - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                    - `cited_text: string`

                    - `end_block_index: number`

                    - `search_result_index: number`

                    - `source: string`

                    - `start_block_index: number`

                    - `title: string`

                    - `type: "search_result_location"`

                      - `"search_result_location"`

              - `source: string`

              - `title: string`

              - `type: "search_result"`

                - `"search_result"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations: optional CitationsConfigParam`

                - `enabled: optional boolean`

            - `DocumentBlockParam = object { source, type, cache_control, 3 more }`

              - `source: Base64PDFSource or PlainTextSource or ContentBlockSource or URLPDFSource`

                - `Base64PDFSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "application/pdf"`

                    - `"application/pdf"`

                  - `type: "base64"`

                    - `"base64"`

                - `PlainTextSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "text/plain"`

                    - `"text/plain"`

                  - `type: "text"`

                    - `"text"`

                - `ContentBlockSource = object { content, type }`

                  - `content: string or array of ContentBlockSourceContent`

                    - `UnionMember0 = string`

                    - `ContentBlockSourceContent = array of ContentBlockSourceContent`

                      - `TextBlockParam = object { text, type, cache_control, citations }`

                        - `text: string`

                        - `type: "text"`

                          - `"text"`

                        - `cache_control: optional CacheControlEphemeral`

                          Create a cache control breakpoint at this content block.

                          - `type: "ephemeral"`

                            - `"ephemeral"`

                          - `ttl: optional "5m" or "1h"`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `"5m"`

                            - `"1h"`

                        - `citations: optional array of TextCitationParam`

                          - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_char_index: number`

                            - `start_char_index: number`

                            - `type: "char_location"`

                              - `"char_location"`

                          - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_page_number: number`

                            - `start_page_number: number`

                            - `type: "page_location"`

                              - `"page_location"`

                          - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_block_index: number`

                            - `start_block_index: number`

                            - `type: "content_block_location"`

                              - `"content_block_location"`

                          - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                            - `cited_text: string`

                            - `encrypted_index: string`

                            - `title: string`

                            - `type: "web_search_result_location"`

                              - `"web_search_result_location"`

                            - `url: string`

                          - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                            - `cited_text: string`

                            - `end_block_index: number`

                            - `search_result_index: number`

                            - `source: string`

                            - `start_block_index: number`

                            - `title: string`

                            - `type: "search_result_location"`

                              - `"search_result_location"`

                      - `ImageBlockParam = object { source, type, cache_control }`

                        - `source: Base64ImageSource or URLImageSource`

                          - `Base64ImageSource = object { data, media_type, type }`

                            - `data: string`

                            - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                              - `"image/jpeg"`

                              - `"image/png"`

                              - `"image/gif"`

                              - `"image/webp"`

                            - `type: "base64"`

                              - `"base64"`

                          - `URLImageSource = object { type, url }`

                            - `type: "url"`

                              - `"url"`

                            - `url: string`

                        - `type: "image"`

                          - `"image"`

                        - `cache_control: optional CacheControlEphemeral`

                          Create a cache control breakpoint at this content block.

                          - `type: "ephemeral"`

                            - `"ephemeral"`

                          - `ttl: optional "5m" or "1h"`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `"5m"`

                            - `"1h"`

                  - `type: "content"`

                    - `"content"`

                - `URLPDFSource = object { type, url }`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

              - `type: "document"`

                - `"document"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations: optional CitationsConfigParam`

                - `enabled: optional boolean`

              - `context: optional string`

              - `title: optional string`

        - `is_error: optional boolean`

      - `ServerToolUseBlockParam = object { id, input, name, 2 more }`

        - `id: string`

        - `input: map[unknown]`

        - `name: "web_search"`

          - `"web_search"`

        - `type: "server_tool_use"`

          - `"server_tool_use"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

      - `WebSearchToolResultBlockParam = object { content, tool_use_id, type, cache_control }`

        - `content: WebSearchToolResultBlockParamContent`

          - `WebSearchToolResultBlockItem = array of WebSearchResultBlockParam`

            - `encrypted_content: string`

            - `title: string`

            - `type: "web_search_result"`

              - `"web_search_result"`

            - `url: string`

            - `page_age: optional string`

          - `WebSearchToolRequestError = object { error_code, type }`

            - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

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

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

  - `role: "user" or "assistant"`

    - `"user"`

    - `"assistant"`

- `model: Model`

  The model that will complete your prompt.

  See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

  - `UnionMember0 = "claude-opus-4-5-20251101" or "claude-opus-4-5" or "claude-3-7-sonnet-latest" or 17 more`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

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

  - `UnionMember1 = string`

- `metadata: optional Metadata`

  An object describing metadata about the request.

  - `user_id: optional string`

    An external identifier for the user who is associated with the request.

    This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

- `service_tier: optional "auto" or "standard_only"`

  Determines whether to use priority capacity (if available) or standard capacity for this request.

  Anthropic offers different levels of service for your API requests. See [service-tiers](https://docs.claude.com/en/api/service-tiers) for details.

  - `"auto"`

  - `"standard_only"`

- `stop_sequences: optional array of string`

  Custom text sequences that will cause the model to stop generating.

  Our models will normally stop when they have naturally completed their turn, which will result in a response `stop_reason` of `"end_turn"`.

  If you want the model to stop generating when it encounters custom strings of text, you can use the `stop_sequences` parameter. If the model encounters one of the custom sequences, the response `stop_reason` value will be `"stop_sequence"` and the response `stop_sequence` value will contain the matched stop sequence.

- `stream: optional boolean`

  Whether to incrementally stream the response using server-sent events.

  See [streaming](https://docs.claude.com/en/api/messages-streaming) for details.

- `system: optional string or array of TextBlockParam`

  System prompt.

  A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

  - `UnionMember0 = string`

  - `UnionMember1 = array of TextBlockParam`

    - `text: string`

    - `type: "text"`

      - `"text"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `citations: optional array of TextCitationParam`

      - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_char_index: number`

        - `start_char_index: number`

        - `type: "char_location"`

          - `"char_location"`

      - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_page_number: number`

        - `start_page_number: number`

        - `type: "page_location"`

          - `"page_location"`

      - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_block_index: number`

        - `start_block_index: number`

        - `type: "content_block_location"`

          - `"content_block_location"`

      - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

        - `cited_text: string`

        - `encrypted_index: string`

        - `title: string`

        - `type: "web_search_result_location"`

          - `"web_search_result_location"`

        - `url: string`

      - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

        - `cited_text: string`

        - `end_block_index: number`

        - `search_result_index: number`

        - `source: string`

        - `start_block_index: number`

        - `title: string`

        - `type: "search_result_location"`

          - `"search_result_location"`

- `temperature: optional number`

  Amount of randomness injected into the response.

  Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.

  Note that even with `temperature` of `0.0`, the results will not be fully deterministic.

- `thinking: optional ThinkingConfigParam`

  Configuration for enabling Claude's extended thinking.

  When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

  See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `ThinkingConfigEnabled = object { budget_tokens, type }`

    - `budget_tokens: number`

      Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

      Must be ≥1024 and less than `max_tokens`.

      See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

    - `type: "enabled"`

      - `"enabled"`

  - `ThinkingConfigDisabled = object { type }`

    - `type: "disabled"`

      - `"disabled"`

- `tool_choice: optional ToolChoice`

  How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `ToolChoiceAuto = object { type, disable_parallel_tool_use }`

    The model will automatically decide whether to use tools.

    - `type: "auto"`

      - `"auto"`

    - `disable_parallel_tool_use: optional boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output at most one tool use.

  - `ToolChoiceAny = object { type, disable_parallel_tool_use }`

    The model will use any available tools.

    - `type: "any"`

      - `"any"`

    - `disable_parallel_tool_use: optional boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output exactly one tool use.

  - `ToolChoiceTool = object { name, type, disable_parallel_tool_use }`

    The model will use the specified tool with `tool_choice.name`.

    - `name: string`

      The name of the tool to use.

    - `type: "tool"`

      - `"tool"`

    - `disable_parallel_tool_use: optional boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output exactly one tool use.

  - `ToolChoiceNone = object { type }`

    The model will not be allowed to use tools.

    - `type: "none"`

      - `"none"`

- `tools: optional array of ToolUnion`

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

  - `Tool = object { input_schema, name, cache_control, 2 more }`

    - `input_schema: object { type, properties, required }`

      [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

      This defines the shape of the `input` that your tool accepts and that the model will produce.

      - `type: "object"`

        - `"object"`

      - `properties: optional map[unknown]`

      - `required: optional array of string`

    - `name: string`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `description: optional string`

      Description of what this tool does.

      Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

    - `type: optional "custom"`

      - `"custom"`

  - `ToolBash20250124 = object { name, type, cache_control }`

    - `name: "bash"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"bash"`

    - `type: "bash_20250124"`

      - `"bash_20250124"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `ToolTextEditor20250124 = object { name, type, cache_control }`

    - `name: "str_replace_editor"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_editor"`

    - `type: "text_editor_20250124"`

      - `"text_editor_20250124"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `ToolTextEditor20250429 = object { name, type, cache_control }`

    - `name: "str_replace_based_edit_tool"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_based_edit_tool"`

    - `type: "text_editor_20250429"`

      - `"text_editor_20250429"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `ToolTextEditor20250728 = object { name, type, cache_control, max_characters }`

    - `name: "str_replace_based_edit_tool"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_based_edit_tool"`

    - `type: "text_editor_20250728"`

      - `"text_editor_20250728"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `max_characters: optional number`

      Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

  - `WebSearchTool20250305 = object { name, type, allowed_domains, 4 more }`

    - `name: "web_search"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"web_search"`

    - `type: "web_search_20250305"`

      - `"web_search_20250305"`

    - `allowed_domains: optional array of string`

      If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

    - `blocked_domains: optional array of string`

      If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `max_uses: optional number`

      Maximum number of times the tool can be used in the API request.

    - `user_location: optional object { type, city, country, 2 more }`

      Parameters for the user's location. Used to provide more relevant search results.

      - `type: "approximate"`

        - `"approximate"`

      - `city: optional string`

        The city of the user.

      - `country: optional string`

        The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

      - `region: optional string`

        The region of the user.

      - `timezone: optional string`

        The [IANA timezone](https://nodatime.org/TimeZones) of the user.

- `top_k: optional number`

  Only sample from the top K options for each subsequent token.

  Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

  Recommended for advanced use cases only. You usually only need to use `temperature`.

- `top_p: optional number`

  Use nucleus sampling.

  In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

  Recommended for advanced use cases only. You usually only need to use `temperature`.

### Returns

- `Message = object { id, content, model, 5 more }`

  - `id: string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `content: array of ContentBlock`

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

    - `TextBlock = object { citations, text, type }`

      - `citations: array of TextCitation`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_char_index: number`

          - `file_id: string`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_page_number: number`

          - `file_id: string`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_block_index: number`

          - `file_id: string`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

          - `cited_text: string`

          - `end_block_index: number`

          - `search_result_index: number`

          - `source: string`

          - `start_block_index: number`

          - `title: string`

          - `type: "search_result_location"`

            - `"search_result_location"`

      - `text: string`

      - `type: "text"`

        - `"text"`

    - `ThinkingBlock = object { signature, thinking, type }`

      - `signature: string`

      - `thinking: string`

      - `type: "thinking"`

        - `"thinking"`

    - `RedactedThinkingBlock = object { data, type }`

      - `data: string`

      - `type: "redacted_thinking"`

        - `"redacted_thinking"`

    - `ToolUseBlock = object { id, input, name, type }`

      - `id: string`

      - `input: map[unknown]`

      - `name: string`

      - `type: "tool_use"`

        - `"tool_use"`

    - `ServerToolUseBlock = object { id, input, name, type }`

      - `id: string`

      - `input: map[unknown]`

      - `name: "web_search"`

        - `"web_search"`

      - `type: "server_tool_use"`

        - `"server_tool_use"`

    - `WebSearchToolResultBlock = object { content, tool_use_id, type }`

      - `content: WebSearchToolResultBlockContent`

        - `WebSearchToolResultError = object { error_code, type }`

          - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"max_uses_exceeded"`

            - `"too_many_requests"`

            - `"query_too_long"`

          - `type: "web_search_tool_result_error"`

            - `"web_search_tool_result_error"`

        - `UnionMember1 = array of WebSearchResultBlock`

          - `encrypted_content: string`

          - `page_age: string`

          - `title: string`

          - `type: "web_search_result"`

            - `"web_search_result"`

          - `url: string`

      - `tool_use_id: string`

      - `type: "web_search_tool_result"`

        - `"web_search_tool_result"`

  - `model: Model`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

    - `UnionMember0 = "claude-opus-4-5-20251101" or "claude-opus-4-5" or "claude-3-7-sonnet-latest" or 17 more`

      The model that will complete your prompt.

      See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

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

    - `UnionMember1 = string`

  - `role: "assistant"`

    Conversational role of the generated message.

    This will always be `"assistant"`.

    - `"assistant"`

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

    - `"end_turn"`

    - `"max_tokens"`

    - `"stop_sequence"`

    - `"tool_use"`

    - `"pause_turn"`

    - `"refusal"`

  - `stop_sequence: string`

    Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was generated.

  - `type: "message"`

    Object type.

    For Messages, this is always `"message"`.

    - `"message"`

  - `usage: Usage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cache_creation: CacheCreation`

      Breakdown of cached tokens by TTL

      - `ephemeral_1h_input_tokens: number`

        The number of input tokens used to create the 1 hour cache entry.

      - `ephemeral_5m_input_tokens: number`

        The number of input tokens used to create the 5 minute cache entry.

    - `cache_creation_input_tokens: number`

      The number of input tokens used to create the cache entry.

    - `cache_read_input_tokens: number`

      The number of input tokens read from the cache.

    - `input_tokens: number`

      The number of input tokens which were used.

    - `output_tokens: number`

      The number of output tokens which were used.

    - `server_tool_use: ServerToolUsage`

      The number of server tool requests.

      - `web_search_requests: number`

        The number of web search tool requests.

    - `service_tier: "standard" or "priority" or "batch"`

      If the request used the priority, standard, or batch tier.

      - `"standard"`

      - `"priority"`

      - `"batch"`

### Example

```http
curl https://api.anthropic.com/v1/messages \
    -H 'Content-Type: application/json' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY" \
    -d '{
          "max_tokens": 1024,
          "messages": [
            {
              "content": "Hello, world",
              "role": "user"
            }
          ],
          "model": "claude-sonnet-4-5-20250929"
        }'
```

## Count Tokens

**post** `/v1/messages/count_tokens`

Count the number of tokens in a Message.

The Token Count API can be used to count the number of tokens in a Message, including tools, images, and documents, without creating it.

Learn more about token counting in our [user guide](https://docs.claude.com/en/docs/build-with-claude/token-counting)

### Body Parameters

- `messages: array of MessageParam`

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

  - `content: string or array of ContentBlockParam`

    - `UnionMember0 = string`

    - `UnionMember1 = array of ContentBlockParam`

      - `TextBlockParam = object { text, type, cache_control, citations }`

        - `text: string`

        - `type: "text"`

          - `"text"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional array of TextCitationParam`

          - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_char_index: number`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_page_number: number`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_block_index: number`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string`

            - `type: "search_result_location"`

              - `"search_result_location"`

      - `ImageBlockParam = object { source, type, cache_control }`

        - `source: Base64ImageSource or URLImageSource`

          - `Base64ImageSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

              - `"image/jpeg"`

              - `"image/png"`

              - `"image/gif"`

              - `"image/webp"`

            - `type: "base64"`

              - `"base64"`

          - `URLImageSource = object { type, url }`

            - `type: "url"`

              - `"url"`

            - `url: string`

        - `type: "image"`

          - `"image"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

      - `DocumentBlockParam = object { source, type, cache_control, 3 more }`

        - `source: Base64PDFSource or PlainTextSource or ContentBlockSource or URLPDFSource`

          - `Base64PDFSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "application/pdf"`

              - `"application/pdf"`

            - `type: "base64"`

              - `"base64"`

          - `PlainTextSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "text/plain"`

              - `"text/plain"`

            - `type: "text"`

              - `"text"`

          - `ContentBlockSource = object { content, type }`

            - `content: string or array of ContentBlockSourceContent`

              - `UnionMember0 = string`

              - `ContentBlockSourceContent = array of ContentBlockSourceContent`

                - `TextBlockParam = object { text, type, cache_control, citations }`

                  - `text: string`

                  - `type: "text"`

                    - `"text"`

                  - `cache_control: optional CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: "ephemeral"`

                      - `"ephemeral"`

                    - `ttl: optional "5m" or "1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `"5m"`

                      - `"1h"`

                  - `citations: optional array of TextCitationParam`

                    - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_char_index: number`

                      - `start_char_index: number`

                      - `type: "char_location"`

                        - `"char_location"`

                    - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_page_number: number`

                      - `start_page_number: number`

                      - `type: "page_location"`

                        - `"page_location"`

                    - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_block_index: number`

                      - `start_block_index: number`

                      - `type: "content_block_location"`

                        - `"content_block_location"`

                    - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                      - `cited_text: string`

                      - `encrypted_index: string`

                      - `title: string`

                      - `type: "web_search_result_location"`

                        - `"web_search_result_location"`

                      - `url: string`

                    - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                      - `cited_text: string`

                      - `end_block_index: number`

                      - `search_result_index: number`

                      - `source: string`

                      - `start_block_index: number`

                      - `title: string`

                      - `type: "search_result_location"`

                        - `"search_result_location"`

                - `ImageBlockParam = object { source, type, cache_control }`

                  - `source: Base64ImageSource or URLImageSource`

                    - `Base64ImageSource = object { data, media_type, type }`

                      - `data: string`

                      - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                        - `"image/jpeg"`

                        - `"image/png"`

                        - `"image/gif"`

                        - `"image/webp"`

                      - `type: "base64"`

                        - `"base64"`

                    - `URLImageSource = object { type, url }`

                      - `type: "url"`

                        - `"url"`

                      - `url: string`

                  - `type: "image"`

                    - `"image"`

                  - `cache_control: optional CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: "ephemeral"`

                      - `"ephemeral"`

                    - `ttl: optional "5m" or "1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `"5m"`

                      - `"1h"`

            - `type: "content"`

              - `"content"`

          - `URLPDFSource = object { type, url }`

            - `type: "url"`

              - `"url"`

            - `url: string`

        - `type: "document"`

          - `"document"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional CitationsConfigParam`

          - `enabled: optional boolean`

        - `context: optional string`

        - `title: optional string`

      - `SearchResultBlockParam = object { content, source, title, 3 more }`

        - `content: array of TextBlockParam`

          - `text: string`

          - `type: "text"`

            - `"text"`

          - `cache_control: optional CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl: optional "5m" or "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

          - `citations: optional array of TextCitationParam`

            - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_char_index: number`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_page_number: number`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_block_index: number`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string`

              - `type: "search_result_location"`

                - `"search_result_location"`

        - `source: string`

        - `title: string`

        - `type: "search_result"`

          - `"search_result"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional CitationsConfigParam`

          - `enabled: optional boolean`

      - `ThinkingBlockParam = object { signature, thinking, type }`

        - `signature: string`

        - `thinking: string`

        - `type: "thinking"`

          - `"thinking"`

      - `RedactedThinkingBlockParam = object { data, type }`

        - `data: string`

        - `type: "redacted_thinking"`

          - `"redacted_thinking"`

      - `ToolUseBlockParam = object { id, input, name, 2 more }`

        - `id: string`

        - `input: map[unknown]`

        - `name: string`

        - `type: "tool_use"`

          - `"tool_use"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

      - `ToolResultBlockParam = object { tool_use_id, type, cache_control, 2 more }`

        - `tool_use_id: string`

        - `type: "tool_result"`

          - `"tool_result"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `content: optional string or array of TextBlockParam or ImageBlockParam or SearchResultBlockParam or DocumentBlockParam`

          - `UnionMember0 = string`

          - `UnionMember1 = array of TextBlockParam or ImageBlockParam or SearchResultBlockParam or DocumentBlockParam`

            - `TextBlockParam = object { text, type, cache_control, citations }`

              - `text: string`

              - `type: "text"`

                - `"text"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations: optional array of TextCitationParam`

                - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_char_index: number`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_page_number: number`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_block_index: number`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

            - `ImageBlockParam = object { source, type, cache_control }`

              - `source: Base64ImageSource or URLImageSource`

                - `Base64ImageSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                    - `"image/jpeg"`

                    - `"image/png"`

                    - `"image/gif"`

                    - `"image/webp"`

                  - `type: "base64"`

                    - `"base64"`

                - `URLImageSource = object { type, url }`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

              - `type: "image"`

                - `"image"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

            - `SearchResultBlockParam = object { content, source, title, 3 more }`

              - `content: array of TextBlockParam`

                - `text: string`

                - `type: "text"`

                  - `"text"`

                - `cache_control: optional CacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `type: "ephemeral"`

                    - `"ephemeral"`

                  - `ttl: optional "5m" or "1h"`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `"5m"`

                    - `"1h"`

                - `citations: optional array of TextCitationParam`

                  - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string`

                    - `end_char_index: number`

                    - `start_char_index: number`

                    - `type: "char_location"`

                      - `"char_location"`

                  - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string`

                    - `end_page_number: number`

                    - `start_page_number: number`

                    - `type: "page_location"`

                      - `"page_location"`

                  - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string`

                    - `end_block_index: number`

                    - `start_block_index: number`

                    - `type: "content_block_location"`

                      - `"content_block_location"`

                  - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                    - `cited_text: string`

                    - `encrypted_index: string`

                    - `title: string`

                    - `type: "web_search_result_location"`

                      - `"web_search_result_location"`

                    - `url: string`

                  - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                    - `cited_text: string`

                    - `end_block_index: number`

                    - `search_result_index: number`

                    - `source: string`

                    - `start_block_index: number`

                    - `title: string`

                    - `type: "search_result_location"`

                      - `"search_result_location"`

              - `source: string`

              - `title: string`

              - `type: "search_result"`

                - `"search_result"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations: optional CitationsConfigParam`

                - `enabled: optional boolean`

            - `DocumentBlockParam = object { source, type, cache_control, 3 more }`

              - `source: Base64PDFSource or PlainTextSource or ContentBlockSource or URLPDFSource`

                - `Base64PDFSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "application/pdf"`

                    - `"application/pdf"`

                  - `type: "base64"`

                    - `"base64"`

                - `PlainTextSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "text/plain"`

                    - `"text/plain"`

                  - `type: "text"`

                    - `"text"`

                - `ContentBlockSource = object { content, type }`

                  - `content: string or array of ContentBlockSourceContent`

                    - `UnionMember0 = string`

                    - `ContentBlockSourceContent = array of ContentBlockSourceContent`

                      - `TextBlockParam = object { text, type, cache_control, citations }`

                        - `text: string`

                        - `type: "text"`

                          - `"text"`

                        - `cache_control: optional CacheControlEphemeral`

                          Create a cache control breakpoint at this content block.

                          - `type: "ephemeral"`

                            - `"ephemeral"`

                          - `ttl: optional "5m" or "1h"`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `"5m"`

                            - `"1h"`

                        - `citations: optional array of TextCitationParam`

                          - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_char_index: number`

                            - `start_char_index: number`

                            - `type: "char_location"`

                              - `"char_location"`

                          - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_page_number: number`

                            - `start_page_number: number`

                            - `type: "page_location"`

                              - `"page_location"`

                          - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_block_index: number`

                            - `start_block_index: number`

                            - `type: "content_block_location"`

                              - `"content_block_location"`

                          - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                            - `cited_text: string`

                            - `encrypted_index: string`

                            - `title: string`

                            - `type: "web_search_result_location"`

                              - `"web_search_result_location"`

                            - `url: string`

                          - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                            - `cited_text: string`

                            - `end_block_index: number`

                            - `search_result_index: number`

                            - `source: string`

                            - `start_block_index: number`

                            - `title: string`

                            - `type: "search_result_location"`

                              - `"search_result_location"`

                      - `ImageBlockParam = object { source, type, cache_control }`

                        - `source: Base64ImageSource or URLImageSource`

                          - `Base64ImageSource = object { data, media_type, type }`

                            - `data: string`

                            - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                              - `"image/jpeg"`

                              - `"image/png"`

                              - `"image/gif"`

                              - `"image/webp"`

                            - `type: "base64"`

                              - `"base64"`

                          - `URLImageSource = object { type, url }`

                            - `type: "url"`

                              - `"url"`

                            - `url: string`

                        - `type: "image"`

                          - `"image"`

                        - `cache_control: optional CacheControlEphemeral`

                          Create a cache control breakpoint at this content block.

                          - `type: "ephemeral"`

                            - `"ephemeral"`

                          - `ttl: optional "5m" or "1h"`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `"5m"`

                            - `"1h"`

                  - `type: "content"`

                    - `"content"`

                - `URLPDFSource = object { type, url }`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

              - `type: "document"`

                - `"document"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations: optional CitationsConfigParam`

                - `enabled: optional boolean`

              - `context: optional string`

              - `title: optional string`

        - `is_error: optional boolean`

      - `ServerToolUseBlockParam = object { id, input, name, 2 more }`

        - `id: string`

        - `input: map[unknown]`

        - `name: "web_search"`

          - `"web_search"`

        - `type: "server_tool_use"`

          - `"server_tool_use"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

      - `WebSearchToolResultBlockParam = object { content, tool_use_id, type, cache_control }`

        - `content: WebSearchToolResultBlockParamContent`

          - `WebSearchToolResultBlockItem = array of WebSearchResultBlockParam`

            - `encrypted_content: string`

            - `title: string`

            - `type: "web_search_result"`

              - `"web_search_result"`

            - `url: string`

            - `page_age: optional string`

          - `WebSearchToolRequestError = object { error_code, type }`

            - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

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

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

  - `role: "user" or "assistant"`

    - `"user"`

    - `"assistant"`

- `model: Model`

  The model that will complete your prompt.

  See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

  - `UnionMember0 = "claude-opus-4-5-20251101" or "claude-opus-4-5" or "claude-3-7-sonnet-latest" or 17 more`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

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

  - `UnionMember1 = string`

- `system: optional string or array of TextBlockParam`

  System prompt.

  A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

  - `UnionMember0 = string`

  - `UnionMember1 = array of TextBlockParam`

    - `text: string`

    - `type: "text"`

      - `"text"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `citations: optional array of TextCitationParam`

      - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_char_index: number`

        - `start_char_index: number`

        - `type: "char_location"`

          - `"char_location"`

      - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_page_number: number`

        - `start_page_number: number`

        - `type: "page_location"`

          - `"page_location"`

      - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_block_index: number`

        - `start_block_index: number`

        - `type: "content_block_location"`

          - `"content_block_location"`

      - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

        - `cited_text: string`

        - `encrypted_index: string`

        - `title: string`

        - `type: "web_search_result_location"`

          - `"web_search_result_location"`

        - `url: string`

      - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

        - `cited_text: string`

        - `end_block_index: number`

        - `search_result_index: number`

        - `source: string`

        - `start_block_index: number`

        - `title: string`

        - `type: "search_result_location"`

          - `"search_result_location"`

- `thinking: optional ThinkingConfigParam`

  Configuration for enabling Claude's extended thinking.

  When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

  See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `ThinkingConfigEnabled = object { budget_tokens, type }`

    - `budget_tokens: number`

      Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

      Must be ≥1024 and less than `max_tokens`.

      See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

    - `type: "enabled"`

      - `"enabled"`

  - `ThinkingConfigDisabled = object { type }`

    - `type: "disabled"`

      - `"disabled"`

- `tool_choice: optional ToolChoice`

  How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `ToolChoiceAuto = object { type, disable_parallel_tool_use }`

    The model will automatically decide whether to use tools.

    - `type: "auto"`

      - `"auto"`

    - `disable_parallel_tool_use: optional boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output at most one tool use.

  - `ToolChoiceAny = object { type, disable_parallel_tool_use }`

    The model will use any available tools.

    - `type: "any"`

      - `"any"`

    - `disable_parallel_tool_use: optional boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output exactly one tool use.

  - `ToolChoiceTool = object { name, type, disable_parallel_tool_use }`

    The model will use the specified tool with `tool_choice.name`.

    - `name: string`

      The name of the tool to use.

    - `type: "tool"`

      - `"tool"`

    - `disable_parallel_tool_use: optional boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output exactly one tool use.

  - `ToolChoiceNone = object { type }`

    The model will not be allowed to use tools.

    - `type: "none"`

      - `"none"`

- `tools: optional array of MessageCountTokensTool`

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

  - `Tool = object { input_schema, name, cache_control, 2 more }`

    - `input_schema: object { type, properties, required }`

      [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

      This defines the shape of the `input` that your tool accepts and that the model will produce.

      - `type: "object"`

        - `"object"`

      - `properties: optional map[unknown]`

      - `required: optional array of string`

    - `name: string`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `description: optional string`

      Description of what this tool does.

      Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

    - `type: optional "custom"`

      - `"custom"`

  - `ToolBash20250124 = object { name, type, cache_control }`

    - `name: "bash"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"bash"`

    - `type: "bash_20250124"`

      - `"bash_20250124"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `ToolTextEditor20250124 = object { name, type, cache_control }`

    - `name: "str_replace_editor"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_editor"`

    - `type: "text_editor_20250124"`

      - `"text_editor_20250124"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `ToolTextEditor20250429 = object { name, type, cache_control }`

    - `name: "str_replace_based_edit_tool"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_based_edit_tool"`

    - `type: "text_editor_20250429"`

      - `"text_editor_20250429"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `ToolTextEditor20250728 = object { name, type, cache_control, max_characters }`

    - `name: "str_replace_based_edit_tool"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_based_edit_tool"`

    - `type: "text_editor_20250728"`

      - `"text_editor_20250728"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `max_characters: optional number`

      Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

  - `WebSearchTool20250305 = object { name, type, allowed_domains, 4 more }`

    - `name: "web_search"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"web_search"`

    - `type: "web_search_20250305"`

      - `"web_search_20250305"`

    - `allowed_domains: optional array of string`

      If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

    - `blocked_domains: optional array of string`

      If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `max_uses: optional number`

      Maximum number of times the tool can be used in the API request.

    - `user_location: optional object { type, city, country, 2 more }`

      Parameters for the user's location. Used to provide more relevant search results.

      - `type: "approximate"`

        - `"approximate"`

      - `city: optional string`

        The city of the user.

      - `country: optional string`

        The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

      - `region: optional string`

        The region of the user.

      - `timezone: optional string`

        The [IANA timezone](https://nodatime.org/TimeZones) of the user.

### Returns

- `MessageTokensCount = object { input_tokens }`

  - `input_tokens: number`

    The total number of tokens across the provided list of messages, system prompt, and tools.

### Example

```http
curl https://api.anthropic.com/v1/messages/count_tokens \
    -H 'Content-Type: application/json' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY" \
    -d '{
          "messages": [
            {
              "content": "string",
              "role": "user"
            }
          ],
          "model": "claude-opus-4-5-20251101"
        }'
```

## Domain Types

### Base64 Image Source

- `Base64ImageSource = object { data, media_type, type }`

  - `data: string`

  - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

    - `"image/jpeg"`

    - `"image/png"`

    - `"image/gif"`

    - `"image/webp"`

  - `type: "base64"`

    - `"base64"`

### Base64 PDF Source

- `Base64PDFSource = object { data, media_type, type }`

  - `data: string`

  - `media_type: "application/pdf"`

    - `"application/pdf"`

  - `type: "base64"`

    - `"base64"`

### Cache Control Ephemeral

- `CacheControlEphemeral = object { type, ttl }`

  - `type: "ephemeral"`

    - `"ephemeral"`

  - `ttl: optional "5m" or "1h"`

    The time-to-live for the cache control breakpoint.

    This may be one the following values:

    - `5m`: 5 minutes
    - `1h`: 1 hour

    Defaults to `5m`.

    - `"5m"`

    - `"1h"`

### Cache Creation

- `CacheCreation = object { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens }`

  - `ephemeral_1h_input_tokens: number`

    The number of input tokens used to create the 1 hour cache entry.

  - `ephemeral_5m_input_tokens: number`

    The number of input tokens used to create the 5 minute cache entry.

### Citation Char Location

- `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string`

  - `end_char_index: number`

  - `file_id: string`

  - `start_char_index: number`

  - `type: "char_location"`

    - `"char_location"`

### Citation Char Location Param

- `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string`

  - `end_char_index: number`

  - `start_char_index: number`

  - `type: "char_location"`

    - `"char_location"`

### Citation Content Block Location

- `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string`

  - `end_block_index: number`

  - `file_id: string`

  - `start_block_index: number`

  - `type: "content_block_location"`

    - `"content_block_location"`

### Citation Content Block Location Param

- `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string`

  - `end_block_index: number`

  - `start_block_index: number`

  - `type: "content_block_location"`

    - `"content_block_location"`

### Citation Page Location

- `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string`

  - `end_page_number: number`

  - `file_id: string`

  - `start_page_number: number`

  - `type: "page_location"`

    - `"page_location"`

### Citation Page Location Param

- `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string`

  - `end_page_number: number`

  - `start_page_number: number`

  - `type: "page_location"`

    - `"page_location"`

### Citation Search Result Location Param

- `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

  - `cited_text: string`

  - `end_block_index: number`

  - `search_result_index: number`

  - `source: string`

  - `start_block_index: number`

  - `title: string`

  - `type: "search_result_location"`

    - `"search_result_location"`

### Citation Web Search Result Location Param

- `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

  - `cited_text: string`

  - `encrypted_index: string`

  - `title: string`

  - `type: "web_search_result_location"`

    - `"web_search_result_location"`

  - `url: string`

### Citations Config Param

- `CitationsConfigParam = object { enabled }`

  - `enabled: optional boolean`

### Citations Delta

- `CitationsDelta = object { citation, type }`

  - `citation: CitationCharLocation or CitationPageLocation or CitationContentBlockLocation or 2 more`

    - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string`

      - `end_char_index: number`

      - `file_id: string`

      - `start_char_index: number`

      - `type: "char_location"`

        - `"char_location"`

    - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string`

      - `end_page_number: number`

      - `file_id: string`

      - `start_page_number: number`

      - `type: "page_location"`

        - `"page_location"`

    - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string`

      - `end_block_index: number`

      - `file_id: string`

      - `start_block_index: number`

      - `type: "content_block_location"`

        - `"content_block_location"`

    - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

      - `cited_text: string`

      - `encrypted_index: string`

      - `title: string`

      - `type: "web_search_result_location"`

        - `"web_search_result_location"`

      - `url: string`

    - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

      - `cited_text: string`

      - `end_block_index: number`

      - `search_result_index: number`

      - `source: string`

      - `start_block_index: number`

      - `title: string`

      - `type: "search_result_location"`

        - `"search_result_location"`

  - `type: "citations_delta"`

    - `"citations_delta"`

### Citations Search Result Location

- `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

  - `cited_text: string`

  - `end_block_index: number`

  - `search_result_index: number`

  - `source: string`

  - `start_block_index: number`

  - `title: string`

  - `type: "search_result_location"`

    - `"search_result_location"`

### Citations Web Search Result Location

- `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

  - `cited_text: string`

  - `encrypted_index: string`

  - `title: string`

  - `type: "web_search_result_location"`

    - `"web_search_result_location"`

  - `url: string`

### Content Block

- `ContentBlock = TextBlock or ThinkingBlock or RedactedThinkingBlock or 3 more`

  - `TextBlock = object { citations, text, type }`

    - `citations: array of TextCitation`

      Citations supporting the text block.

      The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

      - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_char_index: number`

        - `file_id: string`

        - `start_char_index: number`

        - `type: "char_location"`

          - `"char_location"`

      - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_page_number: number`

        - `file_id: string`

        - `start_page_number: number`

        - `type: "page_location"`

          - `"page_location"`

      - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_block_index: number`

        - `file_id: string`

        - `start_block_index: number`

        - `type: "content_block_location"`

          - `"content_block_location"`

      - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

        - `cited_text: string`

        - `encrypted_index: string`

        - `title: string`

        - `type: "web_search_result_location"`

          - `"web_search_result_location"`

        - `url: string`

      - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

        - `cited_text: string`

        - `end_block_index: number`

        - `search_result_index: number`

        - `source: string`

        - `start_block_index: number`

        - `title: string`

        - `type: "search_result_location"`

          - `"search_result_location"`

    - `text: string`

    - `type: "text"`

      - `"text"`

  - `ThinkingBlock = object { signature, thinking, type }`

    - `signature: string`

    - `thinking: string`

    - `type: "thinking"`

      - `"thinking"`

  - `RedactedThinkingBlock = object { data, type }`

    - `data: string`

    - `type: "redacted_thinking"`

      - `"redacted_thinking"`

  - `ToolUseBlock = object { id, input, name, type }`

    - `id: string`

    - `input: map[unknown]`

    - `name: string`

    - `type: "tool_use"`

      - `"tool_use"`

  - `ServerToolUseBlock = object { id, input, name, type }`

    - `id: string`

    - `input: map[unknown]`

    - `name: "web_search"`

      - `"web_search"`

    - `type: "server_tool_use"`

      - `"server_tool_use"`

  - `WebSearchToolResultBlock = object { content, tool_use_id, type }`

    - `content: WebSearchToolResultBlockContent`

      - `WebSearchToolResultError = object { error_code, type }`

        - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

          - `"invalid_tool_input"`

          - `"unavailable"`

          - `"max_uses_exceeded"`

          - `"too_many_requests"`

          - `"query_too_long"`

        - `type: "web_search_tool_result_error"`

          - `"web_search_tool_result_error"`

      - `UnionMember1 = array of WebSearchResultBlock`

        - `encrypted_content: string`

        - `page_age: string`

        - `title: string`

        - `type: "web_search_result"`

          - `"web_search_result"`

        - `url: string`

    - `tool_use_id: string`

    - `type: "web_search_tool_result"`

      - `"web_search_tool_result"`

### Content Block Param

- `ContentBlockParam = TextBlockParam or ImageBlockParam or DocumentBlockParam or 7 more`

  Regular text content.

  - `TextBlockParam = object { text, type, cache_control, citations }`

    - `text: string`

    - `type: "text"`

      - `"text"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `citations: optional array of TextCitationParam`

      - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_char_index: number`

        - `start_char_index: number`

        - `type: "char_location"`

          - `"char_location"`

      - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_page_number: number`

        - `start_page_number: number`

        - `type: "page_location"`

          - `"page_location"`

      - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_block_index: number`

        - `start_block_index: number`

        - `type: "content_block_location"`

          - `"content_block_location"`

      - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

        - `cited_text: string`

        - `encrypted_index: string`

        - `title: string`

        - `type: "web_search_result_location"`

          - `"web_search_result_location"`

        - `url: string`

      - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

        - `cited_text: string`

        - `end_block_index: number`

        - `search_result_index: number`

        - `source: string`

        - `start_block_index: number`

        - `title: string`

        - `type: "search_result_location"`

          - `"search_result_location"`

  - `ImageBlockParam = object { source, type, cache_control }`

    - `source: Base64ImageSource or URLImageSource`

      - `Base64ImageSource = object { data, media_type, type }`

        - `data: string`

        - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

          - `"image/jpeg"`

          - `"image/png"`

          - `"image/gif"`

          - `"image/webp"`

        - `type: "base64"`

          - `"base64"`

      - `URLImageSource = object { type, url }`

        - `type: "url"`

          - `"url"`

        - `url: string`

    - `type: "image"`

      - `"image"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `DocumentBlockParam = object { source, type, cache_control, 3 more }`

    - `source: Base64PDFSource or PlainTextSource or ContentBlockSource or URLPDFSource`

      - `Base64PDFSource = object { data, media_type, type }`

        - `data: string`

        - `media_type: "application/pdf"`

          - `"application/pdf"`

        - `type: "base64"`

          - `"base64"`

      - `PlainTextSource = object { data, media_type, type }`

        - `data: string`

        - `media_type: "text/plain"`

          - `"text/plain"`

        - `type: "text"`

          - `"text"`

      - `ContentBlockSource = object { content, type }`

        - `content: string or array of ContentBlockSourceContent`

          - `UnionMember0 = string`

          - `ContentBlockSourceContent = array of ContentBlockSourceContent`

            - `TextBlockParam = object { text, type, cache_control, citations }`

              - `text: string`

              - `type: "text"`

                - `"text"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations: optional array of TextCitationParam`

                - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_char_index: number`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_page_number: number`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_block_index: number`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

            - `ImageBlockParam = object { source, type, cache_control }`

              - `source: Base64ImageSource or URLImageSource`

                - `Base64ImageSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                    - `"image/jpeg"`

                    - `"image/png"`

                    - `"image/gif"`

                    - `"image/webp"`

                  - `type: "base64"`

                    - `"base64"`

                - `URLImageSource = object { type, url }`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

              - `type: "image"`

                - `"image"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

        - `type: "content"`

          - `"content"`

      - `URLPDFSource = object { type, url }`

        - `type: "url"`

          - `"url"`

        - `url: string`

    - `type: "document"`

      - `"document"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `citations: optional CitationsConfigParam`

      - `enabled: optional boolean`

    - `context: optional string`

    - `title: optional string`

  - `SearchResultBlockParam = object { content, source, title, 3 more }`

    - `content: array of TextBlockParam`

      - `text: string`

      - `type: "text"`

        - `"text"`

      - `cache_control: optional CacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `type: "ephemeral"`

          - `"ephemeral"`

        - `ttl: optional "5m" or "1h"`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `"5m"`

          - `"1h"`

      - `citations: optional array of TextCitationParam`

        - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_char_index: number`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_page_number: number`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_block_index: number`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

          - `cited_text: string`

          - `end_block_index: number`

          - `search_result_index: number`

          - `source: string`

          - `start_block_index: number`

          - `title: string`

          - `type: "search_result_location"`

            - `"search_result_location"`

    - `source: string`

    - `title: string`

    - `type: "search_result"`

      - `"search_result"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `citations: optional CitationsConfigParam`

      - `enabled: optional boolean`

  - `ThinkingBlockParam = object { signature, thinking, type }`

    - `signature: string`

    - `thinking: string`

    - `type: "thinking"`

      - `"thinking"`

  - `RedactedThinkingBlockParam = object { data, type }`

    - `data: string`

    - `type: "redacted_thinking"`

      - `"redacted_thinking"`

  - `ToolUseBlockParam = object { id, input, name, 2 more }`

    - `id: string`

    - `input: map[unknown]`

    - `name: string`

    - `type: "tool_use"`

      - `"tool_use"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `ToolResultBlockParam = object { tool_use_id, type, cache_control, 2 more }`

    - `tool_use_id: string`

    - `type: "tool_result"`

      - `"tool_result"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `content: optional string or array of TextBlockParam or ImageBlockParam or SearchResultBlockParam or DocumentBlockParam`

      - `UnionMember0 = string`

      - `UnionMember1 = array of TextBlockParam or ImageBlockParam or SearchResultBlockParam or DocumentBlockParam`

        - `TextBlockParam = object { text, type, cache_control, citations }`

          - `text: string`

          - `type: "text"`

            - `"text"`

          - `cache_control: optional CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl: optional "5m" or "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

          - `citations: optional array of TextCitationParam`

            - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_char_index: number`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_page_number: number`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_block_index: number`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string`

              - `type: "search_result_location"`

                - `"search_result_location"`

        - `ImageBlockParam = object { source, type, cache_control }`

          - `source: Base64ImageSource or URLImageSource`

            - `Base64ImageSource = object { data, media_type, type }`

              - `data: string`

              - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                - `"image/jpeg"`

                - `"image/png"`

                - `"image/gif"`

                - `"image/webp"`

              - `type: "base64"`

                - `"base64"`

            - `URLImageSource = object { type, url }`

              - `type: "url"`

                - `"url"`

              - `url: string`

          - `type: "image"`

            - `"image"`

          - `cache_control: optional CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl: optional "5m" or "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

        - `SearchResultBlockParam = object { content, source, title, 3 more }`

          - `content: array of TextBlockParam`

            - `text: string`

            - `type: "text"`

              - `"text"`

            - `cache_control: optional CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: "ephemeral"`

                - `"ephemeral"`

              - `ttl: optional "5m" or "1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `"5m"`

                - `"1h"`

            - `citations: optional array of TextCitationParam`

              - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_char_index: number`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_page_number: number`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_block_index: number`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string`

                - `type: "search_result_location"`

                  - `"search_result_location"`

          - `source: string`

          - `title: string`

          - `type: "search_result"`

            - `"search_result"`

          - `cache_control: optional CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl: optional "5m" or "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

          - `citations: optional CitationsConfigParam`

            - `enabled: optional boolean`

        - `DocumentBlockParam = object { source, type, cache_control, 3 more }`

          - `source: Base64PDFSource or PlainTextSource or ContentBlockSource or URLPDFSource`

            - `Base64PDFSource = object { data, media_type, type }`

              - `data: string`

              - `media_type: "application/pdf"`

                - `"application/pdf"`

              - `type: "base64"`

                - `"base64"`

            - `PlainTextSource = object { data, media_type, type }`

              - `data: string`

              - `media_type: "text/plain"`

                - `"text/plain"`

              - `type: "text"`

                - `"text"`

            - `ContentBlockSource = object { content, type }`

              - `content: string or array of ContentBlockSourceContent`

                - `UnionMember0 = string`

                - `ContentBlockSourceContent = array of ContentBlockSourceContent`

                  - `TextBlockParam = object { text, type, cache_control, citations }`

                    - `text: string`

                    - `type: "text"`

                      - `"text"`

                    - `cache_control: optional CacheControlEphemeral`

                      Create a cache control breakpoint at this content block.

                      - `type: "ephemeral"`

                        - `"ephemeral"`

                      - `ttl: optional "5m" or "1h"`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `"5m"`

                        - `"1h"`

                    - `citations: optional array of TextCitationParam`

                      - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string`

                        - `end_char_index: number`

                        - `start_char_index: number`

                        - `type: "char_location"`

                          - `"char_location"`

                      - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string`

                        - `end_page_number: number`

                        - `start_page_number: number`

                        - `type: "page_location"`

                          - `"page_location"`

                      - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string`

                        - `end_block_index: number`

                        - `start_block_index: number`

                        - `type: "content_block_location"`

                          - `"content_block_location"`

                      - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                        - `cited_text: string`

                        - `encrypted_index: string`

                        - `title: string`

                        - `type: "web_search_result_location"`

                          - `"web_search_result_location"`

                        - `url: string`

                      - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                        - `cited_text: string`

                        - `end_block_index: number`

                        - `search_result_index: number`

                        - `source: string`

                        - `start_block_index: number`

                        - `title: string`

                        - `type: "search_result_location"`

                          - `"search_result_location"`

                  - `ImageBlockParam = object { source, type, cache_control }`

                    - `source: Base64ImageSource or URLImageSource`

                      - `Base64ImageSource = object { data, media_type, type }`

                        - `data: string`

                        - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                          - `"image/jpeg"`

                          - `"image/png"`

                          - `"image/gif"`

                          - `"image/webp"`

                        - `type: "base64"`

                          - `"base64"`

                      - `URLImageSource = object { type, url }`

                        - `type: "url"`

                          - `"url"`

                        - `url: string`

                    - `type: "image"`

                      - `"image"`

                    - `cache_control: optional CacheControlEphemeral`

                      Create a cache control breakpoint at this content block.

                      - `type: "ephemeral"`

                        - `"ephemeral"`

                      - `ttl: optional "5m" or "1h"`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `"5m"`

                        - `"1h"`

              - `type: "content"`

                - `"content"`

            - `URLPDFSource = object { type, url }`

              - `type: "url"`

                - `"url"`

              - `url: string`

          - `type: "document"`

            - `"document"`

          - `cache_control: optional CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl: optional "5m" or "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

          - `citations: optional CitationsConfigParam`

            - `enabled: optional boolean`

          - `context: optional string`

          - `title: optional string`

    - `is_error: optional boolean`

  - `ServerToolUseBlockParam = object { id, input, name, 2 more }`

    - `id: string`

    - `input: map[unknown]`

    - `name: "web_search"`

      - `"web_search"`

    - `type: "server_tool_use"`

      - `"server_tool_use"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `WebSearchToolResultBlockParam = object { content, tool_use_id, type, cache_control }`

    - `content: WebSearchToolResultBlockParamContent`

      - `WebSearchToolResultBlockItem = array of WebSearchResultBlockParam`

        - `encrypted_content: string`

        - `title: string`

        - `type: "web_search_result"`

          - `"web_search_result"`

        - `url: string`

        - `page_age: optional string`

      - `WebSearchToolRequestError = object { error_code, type }`

        - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

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

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

### Content Block Source

- `ContentBlockSource = object { content, type }`

  - `content: string or array of ContentBlockSourceContent`

    - `UnionMember0 = string`

    - `ContentBlockSourceContent = array of ContentBlockSourceContent`

      - `TextBlockParam = object { text, type, cache_control, citations }`

        - `text: string`

        - `type: "text"`

          - `"text"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional array of TextCitationParam`

          - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_char_index: number`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_page_number: number`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_block_index: number`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string`

            - `type: "search_result_location"`

              - `"search_result_location"`

      - `ImageBlockParam = object { source, type, cache_control }`

        - `source: Base64ImageSource or URLImageSource`

          - `Base64ImageSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

              - `"image/jpeg"`

              - `"image/png"`

              - `"image/gif"`

              - `"image/webp"`

            - `type: "base64"`

              - `"base64"`

          - `URLImageSource = object { type, url }`

            - `type: "url"`

              - `"url"`

            - `url: string`

        - `type: "image"`

          - `"image"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

  - `type: "content"`

    - `"content"`

### Content Block Source Content

- `ContentBlockSourceContent = TextBlockParam or ImageBlockParam`

  - `TextBlockParam = object { text, type, cache_control, citations }`

    - `text: string`

    - `type: "text"`

      - `"text"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `citations: optional array of TextCitationParam`

      - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_char_index: number`

        - `start_char_index: number`

        - `type: "char_location"`

          - `"char_location"`

      - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_page_number: number`

        - `start_page_number: number`

        - `type: "page_location"`

          - `"page_location"`

      - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_block_index: number`

        - `start_block_index: number`

        - `type: "content_block_location"`

          - `"content_block_location"`

      - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

        - `cited_text: string`

        - `encrypted_index: string`

        - `title: string`

        - `type: "web_search_result_location"`

          - `"web_search_result_location"`

        - `url: string`

      - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

        - `cited_text: string`

        - `end_block_index: number`

        - `search_result_index: number`

        - `source: string`

        - `start_block_index: number`

        - `title: string`

        - `type: "search_result_location"`

          - `"search_result_location"`

  - `ImageBlockParam = object { source, type, cache_control }`

    - `source: Base64ImageSource or URLImageSource`

      - `Base64ImageSource = object { data, media_type, type }`

        - `data: string`

        - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

          - `"image/jpeg"`

          - `"image/png"`

          - `"image/gif"`

          - `"image/webp"`

        - `type: "base64"`

          - `"base64"`

      - `URLImageSource = object { type, url }`

        - `type: "url"`

          - `"url"`

        - `url: string`

    - `type: "image"`

      - `"image"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

### Document Block Param

- `DocumentBlockParam = object { source, type, cache_control, 3 more }`

  - `source: Base64PDFSource or PlainTextSource or ContentBlockSource or URLPDFSource`

    - `Base64PDFSource = object { data, media_type, type }`

      - `data: string`

      - `media_type: "application/pdf"`

        - `"application/pdf"`

      - `type: "base64"`

        - `"base64"`

    - `PlainTextSource = object { data, media_type, type }`

      - `data: string`

      - `media_type: "text/plain"`

        - `"text/plain"`

      - `type: "text"`

        - `"text"`

    - `ContentBlockSource = object { content, type }`

      - `content: string or array of ContentBlockSourceContent`

        - `UnionMember0 = string`

        - `ContentBlockSourceContent = array of ContentBlockSourceContent`

          - `TextBlockParam = object { text, type, cache_control, citations }`

            - `text: string`

            - `type: "text"`

              - `"text"`

            - `cache_control: optional CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: "ephemeral"`

                - `"ephemeral"`

              - `ttl: optional "5m" or "1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `"5m"`

                - `"1h"`

            - `citations: optional array of TextCitationParam`

              - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_char_index: number`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_page_number: number`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_block_index: number`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string`

                - `type: "search_result_location"`

                  - `"search_result_location"`

          - `ImageBlockParam = object { source, type, cache_control }`

            - `source: Base64ImageSource or URLImageSource`

              - `Base64ImageSource = object { data, media_type, type }`

                - `data: string`

                - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                  - `"image/jpeg"`

                  - `"image/png"`

                  - `"image/gif"`

                  - `"image/webp"`

                - `type: "base64"`

                  - `"base64"`

              - `URLImageSource = object { type, url }`

                - `type: "url"`

                  - `"url"`

                - `url: string`

            - `type: "image"`

              - `"image"`

            - `cache_control: optional CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: "ephemeral"`

                - `"ephemeral"`

              - `ttl: optional "5m" or "1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `"5m"`

                - `"1h"`

      - `type: "content"`

        - `"content"`

    - `URLPDFSource = object { type, url }`

      - `type: "url"`

        - `"url"`

      - `url: string`

  - `type: "document"`

    - `"document"`

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

  - `citations: optional CitationsConfigParam`

    - `enabled: optional boolean`

  - `context: optional string`

  - `title: optional string`

### Image Block Param

- `ImageBlockParam = object { source, type, cache_control }`

  - `source: Base64ImageSource or URLImageSource`

    - `Base64ImageSource = object { data, media_type, type }`

      - `data: string`

      - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

        - `"image/jpeg"`

        - `"image/png"`

        - `"image/gif"`

        - `"image/webp"`

      - `type: "base64"`

        - `"base64"`

    - `URLImageSource = object { type, url }`

      - `type: "url"`

        - `"url"`

      - `url: string`

  - `type: "image"`

    - `"image"`

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

### Input JSON Delta

- `InputJSONDelta = object { partial_json, type }`

  - `partial_json: string`

  - `type: "input_json_delta"`

    - `"input_json_delta"`

### Message

- `Message = object { id, content, model, 5 more }`

  - `id: string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `content: array of ContentBlock`

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

    - `TextBlock = object { citations, text, type }`

      - `citations: array of TextCitation`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_char_index: number`

          - `file_id: string`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_page_number: number`

          - `file_id: string`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_block_index: number`

          - `file_id: string`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

          - `cited_text: string`

          - `end_block_index: number`

          - `search_result_index: number`

          - `source: string`

          - `start_block_index: number`

          - `title: string`

          - `type: "search_result_location"`

            - `"search_result_location"`

      - `text: string`

      - `type: "text"`

        - `"text"`

    - `ThinkingBlock = object { signature, thinking, type }`

      - `signature: string`

      - `thinking: string`

      - `type: "thinking"`

        - `"thinking"`

    - `RedactedThinkingBlock = object { data, type }`

      - `data: string`

      - `type: "redacted_thinking"`

        - `"redacted_thinking"`

    - `ToolUseBlock = object { id, input, name, type }`

      - `id: string`

      - `input: map[unknown]`

      - `name: string`

      - `type: "tool_use"`

        - `"tool_use"`

    - `ServerToolUseBlock = object { id, input, name, type }`

      - `id: string`

      - `input: map[unknown]`

      - `name: "web_search"`

        - `"web_search"`

      - `type: "server_tool_use"`

        - `"server_tool_use"`

    - `WebSearchToolResultBlock = object { content, tool_use_id, type }`

      - `content: WebSearchToolResultBlockContent`

        - `WebSearchToolResultError = object { error_code, type }`

          - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"max_uses_exceeded"`

            - `"too_many_requests"`

            - `"query_too_long"`

          - `type: "web_search_tool_result_error"`

            - `"web_search_tool_result_error"`

        - `UnionMember1 = array of WebSearchResultBlock`

          - `encrypted_content: string`

          - `page_age: string`

          - `title: string`

          - `type: "web_search_result"`

            - `"web_search_result"`

          - `url: string`

      - `tool_use_id: string`

      - `type: "web_search_tool_result"`

        - `"web_search_tool_result"`

  - `model: Model`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

    - `UnionMember0 = "claude-opus-4-5-20251101" or "claude-opus-4-5" or "claude-3-7-sonnet-latest" or 17 more`

      The model that will complete your prompt.

      See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

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

    - `UnionMember1 = string`

  - `role: "assistant"`

    Conversational role of the generated message.

    This will always be `"assistant"`.

    - `"assistant"`

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

    - `"end_turn"`

    - `"max_tokens"`

    - `"stop_sequence"`

    - `"tool_use"`

    - `"pause_turn"`

    - `"refusal"`

  - `stop_sequence: string`

    Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was generated.

  - `type: "message"`

    Object type.

    For Messages, this is always `"message"`.

    - `"message"`

  - `usage: Usage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cache_creation: CacheCreation`

      Breakdown of cached tokens by TTL

      - `ephemeral_1h_input_tokens: number`

        The number of input tokens used to create the 1 hour cache entry.

      - `ephemeral_5m_input_tokens: number`

        The number of input tokens used to create the 5 minute cache entry.

    - `cache_creation_input_tokens: number`

      The number of input tokens used to create the cache entry.

    - `cache_read_input_tokens: number`

      The number of input tokens read from the cache.

    - `input_tokens: number`

      The number of input tokens which were used.

    - `output_tokens: number`

      The number of output tokens which were used.

    - `server_tool_use: ServerToolUsage`

      The number of server tool requests.

      - `web_search_requests: number`

        The number of web search tool requests.

    - `service_tier: "standard" or "priority" or "batch"`

      If the request used the priority, standard, or batch tier.

      - `"standard"`

      - `"priority"`

      - `"batch"`

### Message Count Tokens Tool

- `MessageCountTokensTool = Tool or ToolBash20250124 or ToolTextEditor20250124 or 3 more`

  - `Tool = object { input_schema, name, cache_control, 2 more }`

    - `input_schema: object { type, properties, required }`

      [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

      This defines the shape of the `input` that your tool accepts and that the model will produce.

      - `type: "object"`

        - `"object"`

      - `properties: optional map[unknown]`

      - `required: optional array of string`

    - `name: string`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `description: optional string`

      Description of what this tool does.

      Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

    - `type: optional "custom"`

      - `"custom"`

  - `ToolBash20250124 = object { name, type, cache_control }`

    - `name: "bash"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"bash"`

    - `type: "bash_20250124"`

      - `"bash_20250124"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `ToolTextEditor20250124 = object { name, type, cache_control }`

    - `name: "str_replace_editor"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_editor"`

    - `type: "text_editor_20250124"`

      - `"text_editor_20250124"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `ToolTextEditor20250429 = object { name, type, cache_control }`

    - `name: "str_replace_based_edit_tool"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_based_edit_tool"`

    - `type: "text_editor_20250429"`

      - `"text_editor_20250429"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `ToolTextEditor20250728 = object { name, type, cache_control, max_characters }`

    - `name: "str_replace_based_edit_tool"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_based_edit_tool"`

    - `type: "text_editor_20250728"`

      - `"text_editor_20250728"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `max_characters: optional number`

      Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

  - `WebSearchTool20250305 = object { name, type, allowed_domains, 4 more }`

    - `name: "web_search"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"web_search"`

    - `type: "web_search_20250305"`

      - `"web_search_20250305"`

    - `allowed_domains: optional array of string`

      If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

    - `blocked_domains: optional array of string`

      If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `max_uses: optional number`

      Maximum number of times the tool can be used in the API request.

    - `user_location: optional object { type, city, country, 2 more }`

      Parameters for the user's location. Used to provide more relevant search results.

      - `type: "approximate"`

        - `"approximate"`

      - `city: optional string`

        The city of the user.

      - `country: optional string`

        The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

      - `region: optional string`

        The region of the user.

      - `timezone: optional string`

        The [IANA timezone](https://nodatime.org/TimeZones) of the user.

### Message Delta Usage

- `MessageDeltaUsage = object { cache_creation_input_tokens, cache_read_input_tokens, input_tokens, 2 more }`

  - `cache_creation_input_tokens: number`

    The cumulative number of input tokens used to create the cache entry.

  - `cache_read_input_tokens: number`

    The cumulative number of input tokens read from the cache.

  - `input_tokens: number`

    The cumulative number of input tokens which were used.

  - `output_tokens: number`

    The cumulative number of output tokens which were used.

  - `server_tool_use: ServerToolUsage`

    The number of server tool requests.

    - `web_search_requests: number`

      The number of web search tool requests.

### Message Param

- `MessageParam = object { content, role }`

  - `content: string or array of ContentBlockParam`

    - `UnionMember0 = string`

    - `UnionMember1 = array of ContentBlockParam`

      - `TextBlockParam = object { text, type, cache_control, citations }`

        - `text: string`

        - `type: "text"`

          - `"text"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional array of TextCitationParam`

          - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_char_index: number`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_page_number: number`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_block_index: number`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string`

            - `type: "search_result_location"`

              - `"search_result_location"`

      - `ImageBlockParam = object { source, type, cache_control }`

        - `source: Base64ImageSource or URLImageSource`

          - `Base64ImageSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

              - `"image/jpeg"`

              - `"image/png"`

              - `"image/gif"`

              - `"image/webp"`

            - `type: "base64"`

              - `"base64"`

          - `URLImageSource = object { type, url }`

            - `type: "url"`

              - `"url"`

            - `url: string`

        - `type: "image"`

          - `"image"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

      - `DocumentBlockParam = object { source, type, cache_control, 3 more }`

        - `source: Base64PDFSource or PlainTextSource or ContentBlockSource or URLPDFSource`

          - `Base64PDFSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "application/pdf"`

              - `"application/pdf"`

            - `type: "base64"`

              - `"base64"`

          - `PlainTextSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "text/plain"`

              - `"text/plain"`

            - `type: "text"`

              - `"text"`

          - `ContentBlockSource = object { content, type }`

            - `content: string or array of ContentBlockSourceContent`

              - `UnionMember0 = string`

              - `ContentBlockSourceContent = array of ContentBlockSourceContent`

                - `TextBlockParam = object { text, type, cache_control, citations }`

                  - `text: string`

                  - `type: "text"`

                    - `"text"`

                  - `cache_control: optional CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: "ephemeral"`

                      - `"ephemeral"`

                    - `ttl: optional "5m" or "1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `"5m"`

                      - `"1h"`

                  - `citations: optional array of TextCitationParam`

                    - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_char_index: number`

                      - `start_char_index: number`

                      - `type: "char_location"`

                        - `"char_location"`

                    - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_page_number: number`

                      - `start_page_number: number`

                      - `type: "page_location"`

                        - `"page_location"`

                    - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_block_index: number`

                      - `start_block_index: number`

                      - `type: "content_block_location"`

                        - `"content_block_location"`

                    - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                      - `cited_text: string`

                      - `encrypted_index: string`

                      - `title: string`

                      - `type: "web_search_result_location"`

                        - `"web_search_result_location"`

                      - `url: string`

                    - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                      - `cited_text: string`

                      - `end_block_index: number`

                      - `search_result_index: number`

                      - `source: string`

                      - `start_block_index: number`

                      - `title: string`

                      - `type: "search_result_location"`

                        - `"search_result_location"`

                - `ImageBlockParam = object { source, type, cache_control }`

                  - `source: Base64ImageSource or URLImageSource`

                    - `Base64ImageSource = object { data, media_type, type }`

                      - `data: string`

                      - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                        - `"image/jpeg"`

                        - `"image/png"`

                        - `"image/gif"`

                        - `"image/webp"`

                      - `type: "base64"`

                        - `"base64"`

                    - `URLImageSource = object { type, url }`

                      - `type: "url"`

                        - `"url"`

                      - `url: string`

                  - `type: "image"`

                    - `"image"`

                  - `cache_control: optional CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: "ephemeral"`

                      - `"ephemeral"`

                    - `ttl: optional "5m" or "1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `"5m"`

                      - `"1h"`

            - `type: "content"`

              - `"content"`

          - `URLPDFSource = object { type, url }`

            - `type: "url"`

              - `"url"`

            - `url: string`

        - `type: "document"`

          - `"document"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional CitationsConfigParam`

          - `enabled: optional boolean`

        - `context: optional string`

        - `title: optional string`

      - `SearchResultBlockParam = object { content, source, title, 3 more }`

        - `content: array of TextBlockParam`

          - `text: string`

          - `type: "text"`

            - `"text"`

          - `cache_control: optional CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl: optional "5m" or "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

          - `citations: optional array of TextCitationParam`

            - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_char_index: number`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_page_number: number`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_block_index: number`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string`

              - `type: "search_result_location"`

                - `"search_result_location"`

        - `source: string`

        - `title: string`

        - `type: "search_result"`

          - `"search_result"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional CitationsConfigParam`

          - `enabled: optional boolean`

      - `ThinkingBlockParam = object { signature, thinking, type }`

        - `signature: string`

        - `thinking: string`

        - `type: "thinking"`

          - `"thinking"`

      - `RedactedThinkingBlockParam = object { data, type }`

        - `data: string`

        - `type: "redacted_thinking"`

          - `"redacted_thinking"`

      - `ToolUseBlockParam = object { id, input, name, 2 more }`

        - `id: string`

        - `input: map[unknown]`

        - `name: string`

        - `type: "tool_use"`

          - `"tool_use"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

      - `ToolResultBlockParam = object { tool_use_id, type, cache_control, 2 more }`

        - `tool_use_id: string`

        - `type: "tool_result"`

          - `"tool_result"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `content: optional string or array of TextBlockParam or ImageBlockParam or SearchResultBlockParam or DocumentBlockParam`

          - `UnionMember0 = string`

          - `UnionMember1 = array of TextBlockParam or ImageBlockParam or SearchResultBlockParam or DocumentBlockParam`

            - `TextBlockParam = object { text, type, cache_control, citations }`

              - `text: string`

              - `type: "text"`

                - `"text"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations: optional array of TextCitationParam`

                - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_char_index: number`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_page_number: number`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_block_index: number`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

            - `ImageBlockParam = object { source, type, cache_control }`

              - `source: Base64ImageSource or URLImageSource`

                - `Base64ImageSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                    - `"image/jpeg"`

                    - `"image/png"`

                    - `"image/gif"`

                    - `"image/webp"`

                  - `type: "base64"`

                    - `"base64"`

                - `URLImageSource = object { type, url }`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

              - `type: "image"`

                - `"image"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

            - `SearchResultBlockParam = object { content, source, title, 3 more }`

              - `content: array of TextBlockParam`

                - `text: string`

                - `type: "text"`

                  - `"text"`

                - `cache_control: optional CacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `type: "ephemeral"`

                    - `"ephemeral"`

                  - `ttl: optional "5m" or "1h"`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `"5m"`

                    - `"1h"`

                - `citations: optional array of TextCitationParam`

                  - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string`

                    - `end_char_index: number`

                    - `start_char_index: number`

                    - `type: "char_location"`

                      - `"char_location"`

                  - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string`

                    - `end_page_number: number`

                    - `start_page_number: number`

                    - `type: "page_location"`

                      - `"page_location"`

                  - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string`

                    - `end_block_index: number`

                    - `start_block_index: number`

                    - `type: "content_block_location"`

                      - `"content_block_location"`

                  - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                    - `cited_text: string`

                    - `encrypted_index: string`

                    - `title: string`

                    - `type: "web_search_result_location"`

                      - `"web_search_result_location"`

                    - `url: string`

                  - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                    - `cited_text: string`

                    - `end_block_index: number`

                    - `search_result_index: number`

                    - `source: string`

                    - `start_block_index: number`

                    - `title: string`

                    - `type: "search_result_location"`

                      - `"search_result_location"`

              - `source: string`

              - `title: string`

              - `type: "search_result"`

                - `"search_result"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations: optional CitationsConfigParam`

                - `enabled: optional boolean`

            - `DocumentBlockParam = object { source, type, cache_control, 3 more }`

              - `source: Base64PDFSource or PlainTextSource or ContentBlockSource or URLPDFSource`

                - `Base64PDFSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "application/pdf"`

                    - `"application/pdf"`

                  - `type: "base64"`

                    - `"base64"`

                - `PlainTextSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "text/plain"`

                    - `"text/plain"`

                  - `type: "text"`

                    - `"text"`

                - `ContentBlockSource = object { content, type }`

                  - `content: string or array of ContentBlockSourceContent`

                    - `UnionMember0 = string`

                    - `ContentBlockSourceContent = array of ContentBlockSourceContent`

                      - `TextBlockParam = object { text, type, cache_control, citations }`

                        - `text: string`

                        - `type: "text"`

                          - `"text"`

                        - `cache_control: optional CacheControlEphemeral`

                          Create a cache control breakpoint at this content block.

                          - `type: "ephemeral"`

                            - `"ephemeral"`

                          - `ttl: optional "5m" or "1h"`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `"5m"`

                            - `"1h"`

                        - `citations: optional array of TextCitationParam`

                          - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_char_index: number`

                            - `start_char_index: number`

                            - `type: "char_location"`

                              - `"char_location"`

                          - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_page_number: number`

                            - `start_page_number: number`

                            - `type: "page_location"`

                              - `"page_location"`

                          - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_block_index: number`

                            - `start_block_index: number`

                            - `type: "content_block_location"`

                              - `"content_block_location"`

                          - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                            - `cited_text: string`

                            - `encrypted_index: string`

                            - `title: string`

                            - `type: "web_search_result_location"`

                              - `"web_search_result_location"`

                            - `url: string`

                          - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                            - `cited_text: string`

                            - `end_block_index: number`

                            - `search_result_index: number`

                            - `source: string`

                            - `start_block_index: number`

                            - `title: string`

                            - `type: "search_result_location"`

                              - `"search_result_location"`

                      - `ImageBlockParam = object { source, type, cache_control }`

                        - `source: Base64ImageSource or URLImageSource`

                          - `Base64ImageSource = object { data, media_type, type }`

                            - `data: string`

                            - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                              - `"image/jpeg"`

                              - `"image/png"`

                              - `"image/gif"`

                              - `"image/webp"`

                            - `type: "base64"`

                              - `"base64"`

                          - `URLImageSource = object { type, url }`

                            - `type: "url"`

                              - `"url"`

                            - `url: string`

                        - `type: "image"`

                          - `"image"`

                        - `cache_control: optional CacheControlEphemeral`

                          Create a cache control breakpoint at this content block.

                          - `type: "ephemeral"`

                            - `"ephemeral"`

                          - `ttl: optional "5m" or "1h"`

                            The time-to-live for the cache control breakpoint.

                            This may be one the following values:

                            - `5m`: 5 minutes
                            - `1h`: 1 hour

                            Defaults to `5m`.

                            - `"5m"`

                            - `"1h"`

                  - `type: "content"`

                    - `"content"`

                - `URLPDFSource = object { type, url }`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

              - `type: "document"`

                - `"document"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations: optional CitationsConfigParam`

                - `enabled: optional boolean`

              - `context: optional string`

              - `title: optional string`

        - `is_error: optional boolean`

      - `ServerToolUseBlockParam = object { id, input, name, 2 more }`

        - `id: string`

        - `input: map[unknown]`

        - `name: "web_search"`

          - `"web_search"`

        - `type: "server_tool_use"`

          - `"server_tool_use"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

      - `WebSearchToolResultBlockParam = object { content, tool_use_id, type, cache_control }`

        - `content: WebSearchToolResultBlockParamContent`

          - `WebSearchToolResultBlockItem = array of WebSearchResultBlockParam`

            - `encrypted_content: string`

            - `title: string`

            - `type: "web_search_result"`

              - `"web_search_result"`

            - `url: string`

            - `page_age: optional string`

          - `WebSearchToolRequestError = object { error_code, type }`

            - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

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

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

  - `role: "user" or "assistant"`

    - `"user"`

    - `"assistant"`

### Message Tokens Count

- `MessageTokensCount = object { input_tokens }`

  - `input_tokens: number`

    The total number of tokens across the provided list of messages, system prompt, and tools.

### Metadata

- `Metadata = object { user_id }`

  - `user_id: optional string`

    An external identifier for the user who is associated with the request.

    This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

### Model

- `Model = "claude-opus-4-5-20251101" or "claude-opus-4-5" or "claude-3-7-sonnet-latest" or 17 more or string`

  The model that will complete your prompt.

  See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

  - `UnionMember0 = "claude-opus-4-5-20251101" or "claude-opus-4-5" or "claude-3-7-sonnet-latest" or 17 more`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

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

  - `UnionMember1 = string`

### Plain Text Source

- `PlainTextSource = object { data, media_type, type }`

  - `data: string`

  - `media_type: "text/plain"`

    - `"text/plain"`

  - `type: "text"`

    - `"text"`

### Raw Content Block Delta

- `RawContentBlockDelta = TextDelta or InputJSONDelta or CitationsDelta or 2 more`

  - `TextDelta = object { text, type }`

    - `text: string`

    - `type: "text_delta"`

      - `"text_delta"`

  - `InputJSONDelta = object { partial_json, type }`

    - `partial_json: string`

    - `type: "input_json_delta"`

      - `"input_json_delta"`

  - `CitationsDelta = object { citation, type }`

    - `citation: CitationCharLocation or CitationPageLocation or CitationContentBlockLocation or 2 more`

      - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_char_index: number`

        - `file_id: string`

        - `start_char_index: number`

        - `type: "char_location"`

          - `"char_location"`

      - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_page_number: number`

        - `file_id: string`

        - `start_page_number: number`

        - `type: "page_location"`

          - `"page_location"`

      - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_block_index: number`

        - `file_id: string`

        - `start_block_index: number`

        - `type: "content_block_location"`

          - `"content_block_location"`

      - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

        - `cited_text: string`

        - `encrypted_index: string`

        - `title: string`

        - `type: "web_search_result_location"`

          - `"web_search_result_location"`

        - `url: string`

      - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

        - `cited_text: string`

        - `end_block_index: number`

        - `search_result_index: number`

        - `source: string`

        - `start_block_index: number`

        - `title: string`

        - `type: "search_result_location"`

          - `"search_result_location"`

    - `type: "citations_delta"`

      - `"citations_delta"`

  - `ThinkingDelta = object { thinking, type }`

    - `thinking: string`

    - `type: "thinking_delta"`

      - `"thinking_delta"`

  - `SignatureDelta = object { signature, type }`

    - `signature: string`

    - `type: "signature_delta"`

      - `"signature_delta"`

### Raw Content Block Delta Event

- `RawContentBlockDeltaEvent = object { delta, index, type }`

  - `delta: RawContentBlockDelta`

    - `TextDelta = object { text, type }`

      - `text: string`

      - `type: "text_delta"`

        - `"text_delta"`

    - `InputJSONDelta = object { partial_json, type }`

      - `partial_json: string`

      - `type: "input_json_delta"`

        - `"input_json_delta"`

    - `CitationsDelta = object { citation, type }`

      - `citation: CitationCharLocation or CitationPageLocation or CitationContentBlockLocation or 2 more`

        - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_char_index: number`

          - `file_id: string`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_page_number: number`

          - `file_id: string`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_block_index: number`

          - `file_id: string`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

          - `cited_text: string`

          - `end_block_index: number`

          - `search_result_index: number`

          - `source: string`

          - `start_block_index: number`

          - `title: string`

          - `type: "search_result_location"`

            - `"search_result_location"`

      - `type: "citations_delta"`

        - `"citations_delta"`

    - `ThinkingDelta = object { thinking, type }`

      - `thinking: string`

      - `type: "thinking_delta"`

        - `"thinking_delta"`

    - `SignatureDelta = object { signature, type }`

      - `signature: string`

      - `type: "signature_delta"`

        - `"signature_delta"`

  - `index: number`

  - `type: "content_block_delta"`

    - `"content_block_delta"`

### Raw Content Block Start Event

- `RawContentBlockStartEvent = object { content_block, index, type }`

  - `content_block: TextBlock or ThinkingBlock or RedactedThinkingBlock or 3 more`

    - `TextBlock = object { citations, text, type }`

      - `citations: array of TextCitation`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_char_index: number`

          - `file_id: string`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_page_number: number`

          - `file_id: string`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_block_index: number`

          - `file_id: string`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

          - `cited_text: string`

          - `end_block_index: number`

          - `search_result_index: number`

          - `source: string`

          - `start_block_index: number`

          - `title: string`

          - `type: "search_result_location"`

            - `"search_result_location"`

      - `text: string`

      - `type: "text"`

        - `"text"`

    - `ThinkingBlock = object { signature, thinking, type }`

      - `signature: string`

      - `thinking: string`

      - `type: "thinking"`

        - `"thinking"`

    - `RedactedThinkingBlock = object { data, type }`

      - `data: string`

      - `type: "redacted_thinking"`

        - `"redacted_thinking"`

    - `ToolUseBlock = object { id, input, name, type }`

      - `id: string`

      - `input: map[unknown]`

      - `name: string`

      - `type: "tool_use"`

        - `"tool_use"`

    - `ServerToolUseBlock = object { id, input, name, type }`

      - `id: string`

      - `input: map[unknown]`

      - `name: "web_search"`

        - `"web_search"`

      - `type: "server_tool_use"`

        - `"server_tool_use"`

    - `WebSearchToolResultBlock = object { content, tool_use_id, type }`

      - `content: WebSearchToolResultBlockContent`

        - `WebSearchToolResultError = object { error_code, type }`

          - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"max_uses_exceeded"`

            - `"too_many_requests"`

            - `"query_too_long"`

          - `type: "web_search_tool_result_error"`

            - `"web_search_tool_result_error"`

        - `UnionMember1 = array of WebSearchResultBlock`

          - `encrypted_content: string`

          - `page_age: string`

          - `title: string`

          - `type: "web_search_result"`

            - `"web_search_result"`

          - `url: string`

      - `tool_use_id: string`

      - `type: "web_search_tool_result"`

        - `"web_search_tool_result"`

  - `index: number`

  - `type: "content_block_start"`

    - `"content_block_start"`

### Raw Content Block Stop Event

- `RawContentBlockStopEvent = object { index, type }`

  - `index: number`

  - `type: "content_block_stop"`

    - `"content_block_stop"`

### Raw Message Delta Event

- `RawMessageDeltaEvent = object { delta, type, usage }`

  - `delta: object { stop_reason, stop_sequence }`

    - `stop_reason: StopReason`

      - `"end_turn"`

      - `"max_tokens"`

      - `"stop_sequence"`

      - `"tool_use"`

      - `"pause_turn"`

      - `"refusal"`

    - `stop_sequence: string`

  - `type: "message_delta"`

    - `"message_delta"`

  - `usage: MessageDeltaUsage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `cache_creation_input_tokens: number`

      The cumulative number of input tokens used to create the cache entry.

    - `cache_read_input_tokens: number`

      The cumulative number of input tokens read from the cache.

    - `input_tokens: number`

      The cumulative number of input tokens which were used.

    - `output_tokens: number`

      The cumulative number of output tokens which were used.

    - `server_tool_use: ServerToolUsage`

      The number of server tool requests.

      - `web_search_requests: number`

        The number of web search tool requests.

### Raw Message Start Event

- `RawMessageStartEvent = object { message, type }`

  - `message: Message`

    - `id: string`

      Unique object identifier.

      The format and length of IDs may change over time.

    - `content: array of ContentBlock`

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

      - `TextBlock = object { citations, text, type }`

        - `citations: array of TextCitation`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_char_index: number`

            - `file_id: string`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_page_number: number`

            - `file_id: string`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_block_index: number`

            - `file_id: string`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string`

            - `type: "search_result_location"`

              - `"search_result_location"`

        - `text: string`

        - `type: "text"`

          - `"text"`

      - `ThinkingBlock = object { signature, thinking, type }`

        - `signature: string`

        - `thinking: string`

        - `type: "thinking"`

          - `"thinking"`

      - `RedactedThinkingBlock = object { data, type }`

        - `data: string`

        - `type: "redacted_thinking"`

          - `"redacted_thinking"`

      - `ToolUseBlock = object { id, input, name, type }`

        - `id: string`

        - `input: map[unknown]`

        - `name: string`

        - `type: "tool_use"`

          - `"tool_use"`

      - `ServerToolUseBlock = object { id, input, name, type }`

        - `id: string`

        - `input: map[unknown]`

        - `name: "web_search"`

          - `"web_search"`

        - `type: "server_tool_use"`

          - `"server_tool_use"`

      - `WebSearchToolResultBlock = object { content, tool_use_id, type }`

        - `content: WebSearchToolResultBlockContent`

          - `WebSearchToolResultError = object { error_code, type }`

            - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"max_uses_exceeded"`

              - `"too_many_requests"`

              - `"query_too_long"`

            - `type: "web_search_tool_result_error"`

              - `"web_search_tool_result_error"`

          - `UnionMember1 = array of WebSearchResultBlock`

            - `encrypted_content: string`

            - `page_age: string`

            - `title: string`

            - `type: "web_search_result"`

              - `"web_search_result"`

            - `url: string`

        - `tool_use_id: string`

        - `type: "web_search_tool_result"`

          - `"web_search_tool_result"`

    - `model: Model`

      The model that will complete your prompt.

      See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

      - `UnionMember0 = "claude-opus-4-5-20251101" or "claude-opus-4-5" or "claude-3-7-sonnet-latest" or 17 more`

        The model that will complete your prompt.

        See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

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

      - `UnionMember1 = string`

    - `role: "assistant"`

      Conversational role of the generated message.

      This will always be `"assistant"`.

      - `"assistant"`

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

      - `"end_turn"`

      - `"max_tokens"`

      - `"stop_sequence"`

      - `"tool_use"`

      - `"pause_turn"`

      - `"refusal"`

    - `stop_sequence: string`

      Which custom stop sequence was generated, if any.

      This value will be a non-null string if one of your custom stop sequences was generated.

    - `type: "message"`

      Object type.

      For Messages, this is always `"message"`.

      - `"message"`

    - `usage: Usage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cache_creation: CacheCreation`

        Breakdown of cached tokens by TTL

        - `ephemeral_1h_input_tokens: number`

          The number of input tokens used to create the 1 hour cache entry.

        - `ephemeral_5m_input_tokens: number`

          The number of input tokens used to create the 5 minute cache entry.

      - `cache_creation_input_tokens: number`

        The number of input tokens used to create the cache entry.

      - `cache_read_input_tokens: number`

        The number of input tokens read from the cache.

      - `input_tokens: number`

        The number of input tokens which were used.

      - `output_tokens: number`

        The number of output tokens which were used.

      - `server_tool_use: ServerToolUsage`

        The number of server tool requests.

        - `web_search_requests: number`

          The number of web search tool requests.

      - `service_tier: "standard" or "priority" or "batch"`

        If the request used the priority, standard, or batch tier.

        - `"standard"`

        - `"priority"`

        - `"batch"`

  - `type: "message_start"`

    - `"message_start"`

### Raw Message Stop Event

- `RawMessageStopEvent = object { type }`

  - `type: "message_stop"`

    - `"message_stop"`

### Raw Message Stream Event

- `RawMessageStreamEvent = RawMessageStartEvent or RawMessageDeltaEvent or RawMessageStopEvent or 3 more`

  - `RawMessageStartEvent = object { message, type }`

    - `message: Message`

      - `id: string`

        Unique object identifier.

        The format and length of IDs may change over time.

      - `content: array of ContentBlock`

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

        - `TextBlock = object { citations, text, type }`

          - `citations: array of TextCitation`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_char_index: number`

              - `file_id: string`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_page_number: number`

              - `file_id: string`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_block_index: number`

              - `file_id: string`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string`

              - `type: "search_result_location"`

                - `"search_result_location"`

          - `text: string`

          - `type: "text"`

            - `"text"`

        - `ThinkingBlock = object { signature, thinking, type }`

          - `signature: string`

          - `thinking: string`

          - `type: "thinking"`

            - `"thinking"`

        - `RedactedThinkingBlock = object { data, type }`

          - `data: string`

          - `type: "redacted_thinking"`

            - `"redacted_thinking"`

        - `ToolUseBlock = object { id, input, name, type }`

          - `id: string`

          - `input: map[unknown]`

          - `name: string`

          - `type: "tool_use"`

            - `"tool_use"`

        - `ServerToolUseBlock = object { id, input, name, type }`

          - `id: string`

          - `input: map[unknown]`

          - `name: "web_search"`

            - `"web_search"`

          - `type: "server_tool_use"`

            - `"server_tool_use"`

        - `WebSearchToolResultBlock = object { content, tool_use_id, type }`

          - `content: WebSearchToolResultBlockContent`

            - `WebSearchToolResultError = object { error_code, type }`

              - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"max_uses_exceeded"`

                - `"too_many_requests"`

                - `"query_too_long"`

              - `type: "web_search_tool_result_error"`

                - `"web_search_tool_result_error"`

            - `UnionMember1 = array of WebSearchResultBlock`

              - `encrypted_content: string`

              - `page_age: string`

              - `title: string`

              - `type: "web_search_result"`

                - `"web_search_result"`

              - `url: string`

          - `tool_use_id: string`

          - `type: "web_search_tool_result"`

            - `"web_search_tool_result"`

      - `model: Model`

        The model that will complete your prompt.

        See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

        - `UnionMember0 = "claude-opus-4-5-20251101" or "claude-opus-4-5" or "claude-3-7-sonnet-latest" or 17 more`

          The model that will complete your prompt.

          See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

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

        - `UnionMember1 = string`

      - `role: "assistant"`

        Conversational role of the generated message.

        This will always be `"assistant"`.

        - `"assistant"`

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

        - `"end_turn"`

        - `"max_tokens"`

        - `"stop_sequence"`

        - `"tool_use"`

        - `"pause_turn"`

        - `"refusal"`

      - `stop_sequence: string`

        Which custom stop sequence was generated, if any.

        This value will be a non-null string if one of your custom stop sequences was generated.

      - `type: "message"`

        Object type.

        For Messages, this is always `"message"`.

        - `"message"`

      - `usage: Usage`

        Billing and rate-limit usage.

        Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

        Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

        For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

        Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

        - `cache_creation: CacheCreation`

          Breakdown of cached tokens by TTL

          - `ephemeral_1h_input_tokens: number`

            The number of input tokens used to create the 1 hour cache entry.

          - `ephemeral_5m_input_tokens: number`

            The number of input tokens used to create the 5 minute cache entry.

        - `cache_creation_input_tokens: number`

          The number of input tokens used to create the cache entry.

        - `cache_read_input_tokens: number`

          The number of input tokens read from the cache.

        - `input_tokens: number`

          The number of input tokens which were used.

        - `output_tokens: number`

          The number of output tokens which were used.

        - `server_tool_use: ServerToolUsage`

          The number of server tool requests.

          - `web_search_requests: number`

            The number of web search tool requests.

        - `service_tier: "standard" or "priority" or "batch"`

          If the request used the priority, standard, or batch tier.

          - `"standard"`

          - `"priority"`

          - `"batch"`

    - `type: "message_start"`

      - `"message_start"`

  - `RawMessageDeltaEvent = object { delta, type, usage }`

    - `delta: object { stop_reason, stop_sequence }`

      - `stop_reason: StopReason`

        - `"end_turn"`

        - `"max_tokens"`

        - `"stop_sequence"`

        - `"tool_use"`

        - `"pause_turn"`

        - `"refusal"`

      - `stop_sequence: string`

    - `type: "message_delta"`

      - `"message_delta"`

    - `usage: MessageDeltaUsage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cache_creation_input_tokens: number`

        The cumulative number of input tokens used to create the cache entry.

      - `cache_read_input_tokens: number`

        The cumulative number of input tokens read from the cache.

      - `input_tokens: number`

        The cumulative number of input tokens which were used.

      - `output_tokens: number`

        The cumulative number of output tokens which were used.

      - `server_tool_use: ServerToolUsage`

        The number of server tool requests.

        - `web_search_requests: number`

          The number of web search tool requests.

  - `RawMessageStopEvent = object { type }`

    - `type: "message_stop"`

      - `"message_stop"`

  - `RawContentBlockStartEvent = object { content_block, index, type }`

    - `content_block: TextBlock or ThinkingBlock or RedactedThinkingBlock or 3 more`

      - `TextBlock = object { citations, text, type }`

        - `citations: array of TextCitation`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_char_index: number`

            - `file_id: string`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_page_number: number`

            - `file_id: string`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_block_index: number`

            - `file_id: string`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string`

            - `type: "search_result_location"`

              - `"search_result_location"`

        - `text: string`

        - `type: "text"`

          - `"text"`

      - `ThinkingBlock = object { signature, thinking, type }`

        - `signature: string`

        - `thinking: string`

        - `type: "thinking"`

          - `"thinking"`

      - `RedactedThinkingBlock = object { data, type }`

        - `data: string`

        - `type: "redacted_thinking"`

          - `"redacted_thinking"`

      - `ToolUseBlock = object { id, input, name, type }`

        - `id: string`

        - `input: map[unknown]`

        - `name: string`

        - `type: "tool_use"`

          - `"tool_use"`

      - `ServerToolUseBlock = object { id, input, name, type }`

        - `id: string`

        - `input: map[unknown]`

        - `name: "web_search"`

          - `"web_search"`

        - `type: "server_tool_use"`

          - `"server_tool_use"`

      - `WebSearchToolResultBlock = object { content, tool_use_id, type }`

        - `content: WebSearchToolResultBlockContent`

          - `WebSearchToolResultError = object { error_code, type }`

            - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"max_uses_exceeded"`

              - `"too_many_requests"`

              - `"query_too_long"`

            - `type: "web_search_tool_result_error"`

              - `"web_search_tool_result_error"`

          - `UnionMember1 = array of WebSearchResultBlock`

            - `encrypted_content: string`

            - `page_age: string`

            - `title: string`

            - `type: "web_search_result"`

              - `"web_search_result"`

            - `url: string`

        - `tool_use_id: string`

        - `type: "web_search_tool_result"`

          - `"web_search_tool_result"`

    - `index: number`

    - `type: "content_block_start"`

      - `"content_block_start"`

  - `RawContentBlockDeltaEvent = object { delta, index, type }`

    - `delta: RawContentBlockDelta`

      - `TextDelta = object { text, type }`

        - `text: string`

        - `type: "text_delta"`

          - `"text_delta"`

      - `InputJSONDelta = object { partial_json, type }`

        - `partial_json: string`

        - `type: "input_json_delta"`

          - `"input_json_delta"`

      - `CitationsDelta = object { citation, type }`

        - `citation: CitationCharLocation or CitationPageLocation or CitationContentBlockLocation or 2 more`

          - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_char_index: number`

            - `file_id: string`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_page_number: number`

            - `file_id: string`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_block_index: number`

            - `file_id: string`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string`

            - `type: "search_result_location"`

              - `"search_result_location"`

        - `type: "citations_delta"`

          - `"citations_delta"`

      - `ThinkingDelta = object { thinking, type }`

        - `thinking: string`

        - `type: "thinking_delta"`

          - `"thinking_delta"`

      - `SignatureDelta = object { signature, type }`

        - `signature: string`

        - `type: "signature_delta"`

          - `"signature_delta"`

    - `index: number`

    - `type: "content_block_delta"`

      - `"content_block_delta"`

  - `RawContentBlockStopEvent = object { index, type }`

    - `index: number`

    - `type: "content_block_stop"`

      - `"content_block_stop"`

### Redacted Thinking Block

- `RedactedThinkingBlock = object { data, type }`

  - `data: string`

  - `type: "redacted_thinking"`

    - `"redacted_thinking"`

### Redacted Thinking Block Param

- `RedactedThinkingBlockParam = object { data, type }`

  - `data: string`

  - `type: "redacted_thinking"`

    - `"redacted_thinking"`

### Search Result Block Param

- `SearchResultBlockParam = object { content, source, title, 3 more }`

  - `content: array of TextBlockParam`

    - `text: string`

    - `type: "text"`

      - `"text"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `citations: optional array of TextCitationParam`

      - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_char_index: number`

        - `start_char_index: number`

        - `type: "char_location"`

          - `"char_location"`

      - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_page_number: number`

        - `start_page_number: number`

        - `type: "page_location"`

          - `"page_location"`

      - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_block_index: number`

        - `start_block_index: number`

        - `type: "content_block_location"`

          - `"content_block_location"`

      - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

        - `cited_text: string`

        - `encrypted_index: string`

        - `title: string`

        - `type: "web_search_result_location"`

          - `"web_search_result_location"`

        - `url: string`

      - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

        - `cited_text: string`

        - `end_block_index: number`

        - `search_result_index: number`

        - `source: string`

        - `start_block_index: number`

        - `title: string`

        - `type: "search_result_location"`

          - `"search_result_location"`

  - `source: string`

  - `title: string`

  - `type: "search_result"`

    - `"search_result"`

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

  - `citations: optional CitationsConfigParam`

    - `enabled: optional boolean`

### Server Tool Usage

- `ServerToolUsage = object { web_search_requests }`

  - `web_search_requests: number`

    The number of web search tool requests.

### Server Tool Use Block

- `ServerToolUseBlock = object { id, input, name, type }`

  - `id: string`

  - `input: map[unknown]`

  - `name: "web_search"`

    - `"web_search"`

  - `type: "server_tool_use"`

    - `"server_tool_use"`

### Server Tool Use Block Param

- `ServerToolUseBlockParam = object { id, input, name, 2 more }`

  - `id: string`

  - `input: map[unknown]`

  - `name: "web_search"`

    - `"web_search"`

  - `type: "server_tool_use"`

    - `"server_tool_use"`

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

### Signature Delta

- `SignatureDelta = object { signature, type }`

  - `signature: string`

  - `type: "signature_delta"`

    - `"signature_delta"`

### Stop Reason

- `StopReason = "end_turn" or "max_tokens" or "stop_sequence" or 3 more`

  - `"end_turn"`

  - `"max_tokens"`

  - `"stop_sequence"`

  - `"tool_use"`

  - `"pause_turn"`

  - `"refusal"`

### Text Block

- `TextBlock = object { citations, text, type }`

  - `citations: array of TextCitation`

    Citations supporting the text block.

    The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

    - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string`

      - `end_char_index: number`

      - `file_id: string`

      - `start_char_index: number`

      - `type: "char_location"`

        - `"char_location"`

    - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string`

      - `end_page_number: number`

      - `file_id: string`

      - `start_page_number: number`

      - `type: "page_location"`

        - `"page_location"`

    - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string`

      - `end_block_index: number`

      - `file_id: string`

      - `start_block_index: number`

      - `type: "content_block_location"`

        - `"content_block_location"`

    - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

      - `cited_text: string`

      - `encrypted_index: string`

      - `title: string`

      - `type: "web_search_result_location"`

        - `"web_search_result_location"`

      - `url: string`

    - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

      - `cited_text: string`

      - `end_block_index: number`

      - `search_result_index: number`

      - `source: string`

      - `start_block_index: number`

      - `title: string`

      - `type: "search_result_location"`

        - `"search_result_location"`

  - `text: string`

  - `type: "text"`

    - `"text"`

### Text Block Param

- `TextBlockParam = object { text, type, cache_control, citations }`

  - `text: string`

  - `type: "text"`

    - `"text"`

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

  - `citations: optional array of TextCitationParam`

    - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string`

      - `end_char_index: number`

      - `start_char_index: number`

      - `type: "char_location"`

        - `"char_location"`

    - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string`

      - `end_page_number: number`

      - `start_page_number: number`

      - `type: "page_location"`

        - `"page_location"`

    - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

      - `cited_text: string`

      - `document_index: number`

      - `document_title: string`

      - `end_block_index: number`

      - `start_block_index: number`

      - `type: "content_block_location"`

        - `"content_block_location"`

    - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

      - `cited_text: string`

      - `encrypted_index: string`

      - `title: string`

      - `type: "web_search_result_location"`

        - `"web_search_result_location"`

      - `url: string`

    - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

      - `cited_text: string`

      - `end_block_index: number`

      - `search_result_index: number`

      - `source: string`

      - `start_block_index: number`

      - `title: string`

      - `type: "search_result_location"`

        - `"search_result_location"`

### Text Citation

- `TextCitation = CitationCharLocation or CitationPageLocation or CitationContentBlockLocation or 2 more`

  - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

    - `cited_text: string`

    - `document_index: number`

    - `document_title: string`

    - `end_char_index: number`

    - `file_id: string`

    - `start_char_index: number`

    - `type: "char_location"`

      - `"char_location"`

  - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

    - `cited_text: string`

    - `document_index: number`

    - `document_title: string`

    - `end_page_number: number`

    - `file_id: string`

    - `start_page_number: number`

    - `type: "page_location"`

      - `"page_location"`

  - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

    - `cited_text: string`

    - `document_index: number`

    - `document_title: string`

    - `end_block_index: number`

    - `file_id: string`

    - `start_block_index: number`

    - `type: "content_block_location"`

      - `"content_block_location"`

  - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

    - `cited_text: string`

    - `encrypted_index: string`

    - `title: string`

    - `type: "web_search_result_location"`

      - `"web_search_result_location"`

    - `url: string`

  - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

    - `cited_text: string`

    - `end_block_index: number`

    - `search_result_index: number`

    - `source: string`

    - `start_block_index: number`

    - `title: string`

    - `type: "search_result_location"`

      - `"search_result_location"`

### Text Citation Param

- `TextCitationParam = CitationCharLocationParam or CitationPageLocationParam or CitationContentBlockLocationParam or 2 more`

  - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

    - `cited_text: string`

    - `document_index: number`

    - `document_title: string`

    - `end_char_index: number`

    - `start_char_index: number`

    - `type: "char_location"`

      - `"char_location"`

  - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

    - `cited_text: string`

    - `document_index: number`

    - `document_title: string`

    - `end_page_number: number`

    - `start_page_number: number`

    - `type: "page_location"`

      - `"page_location"`

  - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

    - `cited_text: string`

    - `document_index: number`

    - `document_title: string`

    - `end_block_index: number`

    - `start_block_index: number`

    - `type: "content_block_location"`

      - `"content_block_location"`

  - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

    - `cited_text: string`

    - `encrypted_index: string`

    - `title: string`

    - `type: "web_search_result_location"`

      - `"web_search_result_location"`

    - `url: string`

  - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

    - `cited_text: string`

    - `end_block_index: number`

    - `search_result_index: number`

    - `source: string`

    - `start_block_index: number`

    - `title: string`

    - `type: "search_result_location"`

      - `"search_result_location"`

### Text Delta

- `TextDelta = object { text, type }`

  - `text: string`

  - `type: "text_delta"`

    - `"text_delta"`

### Thinking Block

- `ThinkingBlock = object { signature, thinking, type }`

  - `signature: string`

  - `thinking: string`

  - `type: "thinking"`

    - `"thinking"`

### Thinking Block Param

- `ThinkingBlockParam = object { signature, thinking, type }`

  - `signature: string`

  - `thinking: string`

  - `type: "thinking"`

    - `"thinking"`

### Thinking Config Disabled

- `ThinkingConfigDisabled = object { type }`

  - `type: "disabled"`

    - `"disabled"`

### Thinking Config Enabled

- `ThinkingConfigEnabled = object { budget_tokens, type }`

  - `budget_tokens: number`

    Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

    Must be ≥1024 and less than `max_tokens`.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `type: "enabled"`

    - `"enabled"`

### Thinking Config Param

- `ThinkingConfigParam = ThinkingConfigEnabled or ThinkingConfigDisabled`

  Configuration for enabling Claude's extended thinking.

  When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

  See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `ThinkingConfigEnabled = object { budget_tokens, type }`

    - `budget_tokens: number`

      Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

      Must be ≥1024 and less than `max_tokens`.

      See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

    - `type: "enabled"`

      - `"enabled"`

  - `ThinkingConfigDisabled = object { type }`

    - `type: "disabled"`

      - `"disabled"`

### Thinking Delta

- `ThinkingDelta = object { thinking, type }`

  - `thinking: string`

  - `type: "thinking_delta"`

    - `"thinking_delta"`

### Tool

- `Tool = object { input_schema, name, cache_control, 2 more }`

  - `input_schema: object { type, properties, required }`

    [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

    This defines the shape of the `input` that your tool accepts and that the model will produce.

    - `type: "object"`

      - `"object"`

    - `properties: optional map[unknown]`

    - `required: optional array of string`

  - `name: string`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

  - `description: optional string`

    Description of what this tool does.

    Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

  - `type: optional "custom"`

    - `"custom"`

### Tool Bash 20250124

- `ToolBash20250124 = object { name, type, cache_control }`

  - `name: "bash"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"bash"`

  - `type: "bash_20250124"`

    - `"bash_20250124"`

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

### Tool Choice

- `ToolChoice = ToolChoiceAuto or ToolChoiceAny or ToolChoiceTool or ToolChoiceNone`

  How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `ToolChoiceAuto = object { type, disable_parallel_tool_use }`

    The model will automatically decide whether to use tools.

    - `type: "auto"`

      - `"auto"`

    - `disable_parallel_tool_use: optional boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output at most one tool use.

  - `ToolChoiceAny = object { type, disable_parallel_tool_use }`

    The model will use any available tools.

    - `type: "any"`

      - `"any"`

    - `disable_parallel_tool_use: optional boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output exactly one tool use.

  - `ToolChoiceTool = object { name, type, disable_parallel_tool_use }`

    The model will use the specified tool with `tool_choice.name`.

    - `name: string`

      The name of the tool to use.

    - `type: "tool"`

      - `"tool"`

    - `disable_parallel_tool_use: optional boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output exactly one tool use.

  - `ToolChoiceNone = object { type }`

    The model will not be allowed to use tools.

    - `type: "none"`

      - `"none"`

### Tool Choice Any

- `ToolChoiceAny = object { type, disable_parallel_tool_use }`

  The model will use any available tools.

  - `type: "any"`

    - `"any"`

  - `disable_parallel_tool_use: optional boolean`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output exactly one tool use.

### Tool Choice Auto

- `ToolChoiceAuto = object { type, disable_parallel_tool_use }`

  The model will automatically decide whether to use tools.

  - `type: "auto"`

    - `"auto"`

  - `disable_parallel_tool_use: optional boolean`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output at most one tool use.

### Tool Choice None

- `ToolChoiceNone = object { type }`

  The model will not be allowed to use tools.

  - `type: "none"`

    - `"none"`

### Tool Choice Tool

- `ToolChoiceTool = object { name, type, disable_parallel_tool_use }`

  The model will use the specified tool with `tool_choice.name`.

  - `name: string`

    The name of the tool to use.

  - `type: "tool"`

    - `"tool"`

  - `disable_parallel_tool_use: optional boolean`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output exactly one tool use.

### Tool Result Block Param

- `ToolResultBlockParam = object { tool_use_id, type, cache_control, 2 more }`

  - `tool_use_id: string`

  - `type: "tool_result"`

    - `"tool_result"`

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

  - `content: optional string or array of TextBlockParam or ImageBlockParam or SearchResultBlockParam or DocumentBlockParam`

    - `UnionMember0 = string`

    - `UnionMember1 = array of TextBlockParam or ImageBlockParam or SearchResultBlockParam or DocumentBlockParam`

      - `TextBlockParam = object { text, type, cache_control, citations }`

        - `text: string`

        - `type: "text"`

          - `"text"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional array of TextCitationParam`

          - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_char_index: number`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_page_number: number`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_block_index: number`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string`

            - `type: "search_result_location"`

              - `"search_result_location"`

      - `ImageBlockParam = object { source, type, cache_control }`

        - `source: Base64ImageSource or URLImageSource`

          - `Base64ImageSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

              - `"image/jpeg"`

              - `"image/png"`

              - `"image/gif"`

              - `"image/webp"`

            - `type: "base64"`

              - `"base64"`

          - `URLImageSource = object { type, url }`

            - `type: "url"`

              - `"url"`

            - `url: string`

        - `type: "image"`

          - `"image"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

      - `SearchResultBlockParam = object { content, source, title, 3 more }`

        - `content: array of TextBlockParam`

          - `text: string`

          - `type: "text"`

            - `"text"`

          - `cache_control: optional CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `type: "ephemeral"`

              - `"ephemeral"`

            - `ttl: optional "5m" or "1h"`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `"5m"`

              - `"1h"`

          - `citations: optional array of TextCitationParam`

            - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_char_index: number`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_page_number: number`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_block_index: number`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string`

              - `type: "search_result_location"`

                - `"search_result_location"`

        - `source: string`

        - `title: string`

        - `type: "search_result"`

          - `"search_result"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional CitationsConfigParam`

          - `enabled: optional boolean`

      - `DocumentBlockParam = object { source, type, cache_control, 3 more }`

        - `source: Base64PDFSource or PlainTextSource or ContentBlockSource or URLPDFSource`

          - `Base64PDFSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "application/pdf"`

              - `"application/pdf"`

            - `type: "base64"`

              - `"base64"`

          - `PlainTextSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "text/plain"`

              - `"text/plain"`

            - `type: "text"`

              - `"text"`

          - `ContentBlockSource = object { content, type }`

            - `content: string or array of ContentBlockSourceContent`

              - `UnionMember0 = string`

              - `ContentBlockSourceContent = array of ContentBlockSourceContent`

                - `TextBlockParam = object { text, type, cache_control, citations }`

                  - `text: string`

                  - `type: "text"`

                    - `"text"`

                  - `cache_control: optional CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: "ephemeral"`

                      - `"ephemeral"`

                    - `ttl: optional "5m" or "1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `"5m"`

                      - `"1h"`

                  - `citations: optional array of TextCitationParam`

                    - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_char_index: number`

                      - `start_char_index: number`

                      - `type: "char_location"`

                        - `"char_location"`

                    - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_page_number: number`

                      - `start_page_number: number`

                      - `type: "page_location"`

                        - `"page_location"`

                    - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_block_index: number`

                      - `start_block_index: number`

                      - `type: "content_block_location"`

                        - `"content_block_location"`

                    - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                      - `cited_text: string`

                      - `encrypted_index: string`

                      - `title: string`

                      - `type: "web_search_result_location"`

                        - `"web_search_result_location"`

                      - `url: string`

                    - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                      - `cited_text: string`

                      - `end_block_index: number`

                      - `search_result_index: number`

                      - `source: string`

                      - `start_block_index: number`

                      - `title: string`

                      - `type: "search_result_location"`

                        - `"search_result_location"`

                - `ImageBlockParam = object { source, type, cache_control }`

                  - `source: Base64ImageSource or URLImageSource`

                    - `Base64ImageSource = object { data, media_type, type }`

                      - `data: string`

                      - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                        - `"image/jpeg"`

                        - `"image/png"`

                        - `"image/gif"`

                        - `"image/webp"`

                      - `type: "base64"`

                        - `"base64"`

                    - `URLImageSource = object { type, url }`

                      - `type: "url"`

                        - `"url"`

                      - `url: string`

                  - `type: "image"`

                    - `"image"`

                  - `cache_control: optional CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: "ephemeral"`

                      - `"ephemeral"`

                    - `ttl: optional "5m" or "1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `"5m"`

                      - `"1h"`

            - `type: "content"`

              - `"content"`

          - `URLPDFSource = object { type, url }`

            - `type: "url"`

              - `"url"`

            - `url: string`

        - `type: "document"`

          - `"document"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional CitationsConfigParam`

          - `enabled: optional boolean`

        - `context: optional string`

        - `title: optional string`

  - `is_error: optional boolean`

### Tool Text Editor 20250124

- `ToolTextEditor20250124 = object { name, type, cache_control }`

  - `name: "str_replace_editor"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"str_replace_editor"`

  - `type: "text_editor_20250124"`

    - `"text_editor_20250124"`

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

### Tool Text Editor 20250429

- `ToolTextEditor20250429 = object { name, type, cache_control }`

  - `name: "str_replace_based_edit_tool"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"str_replace_based_edit_tool"`

  - `type: "text_editor_20250429"`

    - `"text_editor_20250429"`

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

### Tool Text Editor 20250728

- `ToolTextEditor20250728 = object { name, type, cache_control, max_characters }`

  - `name: "str_replace_based_edit_tool"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"str_replace_based_edit_tool"`

  - `type: "text_editor_20250728"`

    - `"text_editor_20250728"`

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

  - `max_characters: optional number`

    Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

### Tool Union

- `ToolUnion = Tool or ToolBash20250124 or ToolTextEditor20250124 or 3 more`

  - `Tool = object { input_schema, name, cache_control, 2 more }`

    - `input_schema: object { type, properties, required }`

      [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

      This defines the shape of the `input` that your tool accepts and that the model will produce.

      - `type: "object"`

        - `"object"`

      - `properties: optional map[unknown]`

      - `required: optional array of string`

    - `name: string`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `description: optional string`

      Description of what this tool does.

      Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

    - `type: optional "custom"`

      - `"custom"`

  - `ToolBash20250124 = object { name, type, cache_control }`

    - `name: "bash"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"bash"`

    - `type: "bash_20250124"`

      - `"bash_20250124"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `ToolTextEditor20250124 = object { name, type, cache_control }`

    - `name: "str_replace_editor"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_editor"`

    - `type: "text_editor_20250124"`

      - `"text_editor_20250124"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `ToolTextEditor20250429 = object { name, type, cache_control }`

    - `name: "str_replace_based_edit_tool"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_based_edit_tool"`

    - `type: "text_editor_20250429"`

      - `"text_editor_20250429"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

  - `ToolTextEditor20250728 = object { name, type, cache_control, max_characters }`

    - `name: "str_replace_based_edit_tool"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_based_edit_tool"`

    - `type: "text_editor_20250728"`

      - `"text_editor_20250728"`

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `max_characters: optional number`

      Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

  - `WebSearchTool20250305 = object { name, type, allowed_domains, 4 more }`

    - `name: "web_search"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"web_search"`

    - `type: "web_search_20250305"`

      - `"web_search_20250305"`

    - `allowed_domains: optional array of string`

      If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

    - `blocked_domains: optional array of string`

      If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

    - `cache_control: optional CacheControlEphemeral`

      Create a cache control breakpoint at this content block.

      - `type: "ephemeral"`

        - `"ephemeral"`

      - `ttl: optional "5m" or "1h"`

        The time-to-live for the cache control breakpoint.

        This may be one the following values:

        - `5m`: 5 minutes
        - `1h`: 1 hour

        Defaults to `5m`.

        - `"5m"`

        - `"1h"`

    - `max_uses: optional number`

      Maximum number of times the tool can be used in the API request.

    - `user_location: optional object { type, city, country, 2 more }`

      Parameters for the user's location. Used to provide more relevant search results.

      - `type: "approximate"`

        - `"approximate"`

      - `city: optional string`

        The city of the user.

      - `country: optional string`

        The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

      - `region: optional string`

        The region of the user.

      - `timezone: optional string`

        The [IANA timezone](https://nodatime.org/TimeZones) of the user.

### Tool Use Block

- `ToolUseBlock = object { id, input, name, type }`

  - `id: string`

  - `input: map[unknown]`

  - `name: string`

  - `type: "tool_use"`

    - `"tool_use"`

### Tool Use Block Param

- `ToolUseBlockParam = object { id, input, name, 2 more }`

  - `id: string`

  - `input: map[unknown]`

  - `name: string`

  - `type: "tool_use"`

    - `"tool_use"`

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

### URL Image Source

- `URLImageSource = object { type, url }`

  - `type: "url"`

    - `"url"`

  - `url: string`

### URL PDF Source

- `URLPDFSource = object { type, url }`

  - `type: "url"`

    - `"url"`

  - `url: string`

### Usage

- `Usage = object { cache_creation, cache_creation_input_tokens, cache_read_input_tokens, 4 more }`

  - `cache_creation: CacheCreation`

    Breakdown of cached tokens by TTL

    - `ephemeral_1h_input_tokens: number`

      The number of input tokens used to create the 1 hour cache entry.

    - `ephemeral_5m_input_tokens: number`

      The number of input tokens used to create the 5 minute cache entry.

  - `cache_creation_input_tokens: number`

    The number of input tokens used to create the cache entry.

  - `cache_read_input_tokens: number`

    The number of input tokens read from the cache.

  - `input_tokens: number`

    The number of input tokens which were used.

  - `output_tokens: number`

    The number of output tokens which were used.

  - `server_tool_use: ServerToolUsage`

    The number of server tool requests.

    - `web_search_requests: number`

      The number of web search tool requests.

  - `service_tier: "standard" or "priority" or "batch"`

    If the request used the priority, standard, or batch tier.

    - `"standard"`

    - `"priority"`

    - `"batch"`

### Web Search Result Block

- `WebSearchResultBlock = object { encrypted_content, page_age, title, 2 more }`

  - `encrypted_content: string`

  - `page_age: string`

  - `title: string`

  - `type: "web_search_result"`

    - `"web_search_result"`

  - `url: string`

### Web Search Result Block Param

- `WebSearchResultBlockParam = object { encrypted_content, title, type, 2 more }`

  - `encrypted_content: string`

  - `title: string`

  - `type: "web_search_result"`

    - `"web_search_result"`

  - `url: string`

  - `page_age: optional string`

### Web Search Tool 20250305

- `WebSearchTool20250305 = object { name, type, allowed_domains, 4 more }`

  - `name: "web_search"`

    Name of the tool.

    This is how the tool will be called by the model and in `tool_use` blocks.

    - `"web_search"`

  - `type: "web_search_20250305"`

    - `"web_search_20250305"`

  - `allowed_domains: optional array of string`

    If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

  - `blocked_domains: optional array of string`

    If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

  - `max_uses: optional number`

    Maximum number of times the tool can be used in the API request.

  - `user_location: optional object { type, city, country, 2 more }`

    Parameters for the user's location. Used to provide more relevant search results.

    - `type: "approximate"`

      - `"approximate"`

    - `city: optional string`

      The city of the user.

    - `country: optional string`

      The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

    - `region: optional string`

      The region of the user.

    - `timezone: optional string`

      The [IANA timezone](https://nodatime.org/TimeZones) of the user.

### Web Search Tool Request Error

- `WebSearchToolRequestError = object { error_code, type }`

  - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"max_uses_exceeded"`

    - `"too_many_requests"`

    - `"query_too_long"`

  - `type: "web_search_tool_result_error"`

    - `"web_search_tool_result_error"`

### Web Search Tool Result Block

- `WebSearchToolResultBlock = object { content, tool_use_id, type }`

  - `content: WebSearchToolResultBlockContent`

    - `WebSearchToolResultError = object { error_code, type }`

      - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

        - `"invalid_tool_input"`

        - `"unavailable"`

        - `"max_uses_exceeded"`

        - `"too_many_requests"`

        - `"query_too_long"`

      - `type: "web_search_tool_result_error"`

        - `"web_search_tool_result_error"`

    - `UnionMember1 = array of WebSearchResultBlock`

      - `encrypted_content: string`

      - `page_age: string`

      - `title: string`

      - `type: "web_search_result"`

        - `"web_search_result"`

      - `url: string`

  - `tool_use_id: string`

  - `type: "web_search_tool_result"`

    - `"web_search_tool_result"`

### Web Search Tool Result Block Content

- `WebSearchToolResultBlockContent = WebSearchToolResultError or array of WebSearchResultBlock`

  - `WebSearchToolResultError = object { error_code, type }`

    - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

      - `"invalid_tool_input"`

      - `"unavailable"`

      - `"max_uses_exceeded"`

      - `"too_many_requests"`

      - `"query_too_long"`

    - `type: "web_search_tool_result_error"`

      - `"web_search_tool_result_error"`

  - `UnionMember1 = array of WebSearchResultBlock`

    - `encrypted_content: string`

    - `page_age: string`

    - `title: string`

    - `type: "web_search_result"`

      - `"web_search_result"`

    - `url: string`

### Web Search Tool Result Block Param

- `WebSearchToolResultBlockParam = object { content, tool_use_id, type, cache_control }`

  - `content: WebSearchToolResultBlockParamContent`

    - `WebSearchToolResultBlockItem = array of WebSearchResultBlockParam`

      - `encrypted_content: string`

      - `title: string`

      - `type: "web_search_result"`

        - `"web_search_result"`

      - `url: string`

      - `page_age: optional string`

    - `WebSearchToolRequestError = object { error_code, type }`

      - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

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

  - `cache_control: optional CacheControlEphemeral`

    Create a cache control breakpoint at this content block.

    - `type: "ephemeral"`

      - `"ephemeral"`

    - `ttl: optional "5m" or "1h"`

      The time-to-live for the cache control breakpoint.

      This may be one the following values:

      - `5m`: 5 minutes
      - `1h`: 1 hour

      Defaults to `5m`.

      - `"5m"`

      - `"1h"`

### Web Search Tool Result Block Param Content

- `WebSearchToolResultBlockParamContent = array of WebSearchResultBlockParam or WebSearchToolRequestError`

  - `WebSearchToolResultBlockItem = array of WebSearchResultBlockParam`

    - `encrypted_content: string`

    - `title: string`

    - `type: "web_search_result"`

      - `"web_search_result"`

    - `url: string`

    - `page_age: optional string`

  - `WebSearchToolRequestError = object { error_code, type }`

    - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

      - `"invalid_tool_input"`

      - `"unavailable"`

      - `"max_uses_exceeded"`

      - `"too_many_requests"`

      - `"query_too_long"`

    - `type: "web_search_tool_result_error"`

      - `"web_search_tool_result_error"`

### Web Search Tool Result Error

- `WebSearchToolResultError = object { error_code, type }`

  - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"max_uses_exceeded"`

    - `"too_many_requests"`

    - `"query_too_long"`

  - `type: "web_search_tool_result_error"`

    - `"web_search_tool_result_error"`

# Batches

## Create

**post** `/v1/messages/batches`

Send a batch of Message creation requests.

The Message Batches API can be used to process multiple Messages API requests at once. Once a Message Batch is created, it begins processing immediately. Batches can take up to 24 hours to complete.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Body Parameters

- `requests: array of object { custom_id, params }`

  List of requests for prompt completion. Each is an individual request to create a Message.

  - `custom_id: string`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `params: object { max_tokens, messages, model, 11 more }`

    Messages API creation parameters for the individual request.

    See the [Messages API reference](https://docs.claude.com/en/api/messages) for full documentation on available parameters.

    - `max_tokens: number`

      The maximum number of tokens to generate before stopping.

      Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

      Different models have different maximum values for this parameter.  See [models](https://docs.claude.com/en/docs/models-overview) for details.

    - `messages: array of MessageParam`

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

      - `content: string or array of ContentBlockParam`

        - `UnionMember0 = string`

        - `UnionMember1 = array of ContentBlockParam`

          - `TextBlockParam = object { text, type, cache_control, citations }`

            - `text: string`

            - `type: "text"`

              - `"text"`

            - `cache_control: optional CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: "ephemeral"`

                - `"ephemeral"`

              - `ttl: optional "5m" or "1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `"5m"`

                - `"1h"`

            - `citations: optional array of TextCitationParam`

              - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_char_index: number`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_page_number: number`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_block_index: number`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string`

                - `type: "search_result_location"`

                  - `"search_result_location"`

          - `ImageBlockParam = object { source, type, cache_control }`

            - `source: Base64ImageSource or URLImageSource`

              - `Base64ImageSource = object { data, media_type, type }`

                - `data: string`

                - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                  - `"image/jpeg"`

                  - `"image/png"`

                  - `"image/gif"`

                  - `"image/webp"`

                - `type: "base64"`

                  - `"base64"`

              - `URLImageSource = object { type, url }`

                - `type: "url"`

                  - `"url"`

                - `url: string`

            - `type: "image"`

              - `"image"`

            - `cache_control: optional CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: "ephemeral"`

                - `"ephemeral"`

              - `ttl: optional "5m" or "1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `"5m"`

                - `"1h"`

          - `DocumentBlockParam = object { source, type, cache_control, 3 more }`

            - `source: Base64PDFSource or PlainTextSource or ContentBlockSource or URLPDFSource`

              - `Base64PDFSource = object { data, media_type, type }`

                - `data: string`

                - `media_type: "application/pdf"`

                  - `"application/pdf"`

                - `type: "base64"`

                  - `"base64"`

              - `PlainTextSource = object { data, media_type, type }`

                - `data: string`

                - `media_type: "text/plain"`

                  - `"text/plain"`

                - `type: "text"`

                  - `"text"`

              - `ContentBlockSource = object { content, type }`

                - `content: string or array of ContentBlockSourceContent`

                  - `UnionMember0 = string`

                  - `ContentBlockSourceContent = array of ContentBlockSourceContent`

                    - `TextBlockParam = object { text, type, cache_control, citations }`

                      - `text: string`

                      - `type: "text"`

                        - `"text"`

                      - `cache_control: optional CacheControlEphemeral`

                        Create a cache control breakpoint at this content block.

                        - `type: "ephemeral"`

                          - `"ephemeral"`

                        - `ttl: optional "5m" or "1h"`

                          The time-to-live for the cache control breakpoint.

                          This may be one the following values:

                          - `5m`: 5 minutes
                          - `1h`: 1 hour

                          Defaults to `5m`.

                          - `"5m"`

                          - `"1h"`

                      - `citations: optional array of TextCitationParam`

                        - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                          - `cited_text: string`

                          - `document_index: number`

                          - `document_title: string`

                          - `end_char_index: number`

                          - `start_char_index: number`

                          - `type: "char_location"`

                            - `"char_location"`

                        - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                          - `cited_text: string`

                          - `document_index: number`

                          - `document_title: string`

                          - `end_page_number: number`

                          - `start_page_number: number`

                          - `type: "page_location"`

                            - `"page_location"`

                        - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                          - `cited_text: string`

                          - `document_index: number`

                          - `document_title: string`

                          - `end_block_index: number`

                          - `start_block_index: number`

                          - `type: "content_block_location"`

                            - `"content_block_location"`

                        - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                          - `cited_text: string`

                          - `encrypted_index: string`

                          - `title: string`

                          - `type: "web_search_result_location"`

                            - `"web_search_result_location"`

                          - `url: string`

                        - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                          - `cited_text: string`

                          - `end_block_index: number`

                          - `search_result_index: number`

                          - `source: string`

                          - `start_block_index: number`

                          - `title: string`

                          - `type: "search_result_location"`

                            - `"search_result_location"`

                    - `ImageBlockParam = object { source, type, cache_control }`

                      - `source: Base64ImageSource or URLImageSource`

                        - `Base64ImageSource = object { data, media_type, type }`

                          - `data: string`

                          - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                            - `"image/jpeg"`

                            - `"image/png"`

                            - `"image/gif"`

                            - `"image/webp"`

                          - `type: "base64"`

                            - `"base64"`

                        - `URLImageSource = object { type, url }`

                          - `type: "url"`

                            - `"url"`

                          - `url: string`

                      - `type: "image"`

                        - `"image"`

                      - `cache_control: optional CacheControlEphemeral`

                        Create a cache control breakpoint at this content block.

                        - `type: "ephemeral"`

                          - `"ephemeral"`

                        - `ttl: optional "5m" or "1h"`

                          The time-to-live for the cache control breakpoint.

                          This may be one the following values:

                          - `5m`: 5 minutes
                          - `1h`: 1 hour

                          Defaults to `5m`.

                          - `"5m"`

                          - `"1h"`

                - `type: "content"`

                  - `"content"`

              - `URLPDFSource = object { type, url }`

                - `type: "url"`

                  - `"url"`

                - `url: string`

            - `type: "document"`

              - `"document"`

            - `cache_control: optional CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: "ephemeral"`

                - `"ephemeral"`

              - `ttl: optional "5m" or "1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `"5m"`

                - `"1h"`

            - `citations: optional CitationsConfigParam`

              - `enabled: optional boolean`

            - `context: optional string`

            - `title: optional string`

          - `SearchResultBlockParam = object { content, source, title, 3 more }`

            - `content: array of TextBlockParam`

              - `text: string`

              - `type: "text"`

                - `"text"`

              - `cache_control: optional CacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `type: "ephemeral"`

                  - `"ephemeral"`

                - `ttl: optional "5m" or "1h"`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `"5m"`

                  - `"1h"`

              - `citations: optional array of TextCitationParam`

                - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_char_index: number`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_page_number: number`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_block_index: number`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

            - `source: string`

            - `title: string`

            - `type: "search_result"`

              - `"search_result"`

            - `cache_control: optional CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: "ephemeral"`

                - `"ephemeral"`

              - `ttl: optional "5m" or "1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `"5m"`

                - `"1h"`

            - `citations: optional CitationsConfigParam`

              - `enabled: optional boolean`

          - `ThinkingBlockParam = object { signature, thinking, type }`

            - `signature: string`

            - `thinking: string`

            - `type: "thinking"`

              - `"thinking"`

          - `RedactedThinkingBlockParam = object { data, type }`

            - `data: string`

            - `type: "redacted_thinking"`

              - `"redacted_thinking"`

          - `ToolUseBlockParam = object { id, input, name, 2 more }`

            - `id: string`

            - `input: map[unknown]`

            - `name: string`

            - `type: "tool_use"`

              - `"tool_use"`

            - `cache_control: optional CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: "ephemeral"`

                - `"ephemeral"`

              - `ttl: optional "5m" or "1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `"5m"`

                - `"1h"`

          - `ToolResultBlockParam = object { tool_use_id, type, cache_control, 2 more }`

            - `tool_use_id: string`

            - `type: "tool_result"`

              - `"tool_result"`

            - `cache_control: optional CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: "ephemeral"`

                - `"ephemeral"`

              - `ttl: optional "5m" or "1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `"5m"`

                - `"1h"`

            - `content: optional string or array of TextBlockParam or ImageBlockParam or SearchResultBlockParam or DocumentBlockParam`

              - `UnionMember0 = string`

              - `UnionMember1 = array of TextBlockParam or ImageBlockParam or SearchResultBlockParam or DocumentBlockParam`

                - `TextBlockParam = object { text, type, cache_control, citations }`

                  - `text: string`

                  - `type: "text"`

                    - `"text"`

                  - `cache_control: optional CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: "ephemeral"`

                      - `"ephemeral"`

                    - `ttl: optional "5m" or "1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `"5m"`

                      - `"1h"`

                  - `citations: optional array of TextCitationParam`

                    - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_char_index: number`

                      - `start_char_index: number`

                      - `type: "char_location"`

                        - `"char_location"`

                    - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_page_number: number`

                      - `start_page_number: number`

                      - `type: "page_location"`

                        - `"page_location"`

                    - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_block_index: number`

                      - `start_block_index: number`

                      - `type: "content_block_location"`

                        - `"content_block_location"`

                    - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                      - `cited_text: string`

                      - `encrypted_index: string`

                      - `title: string`

                      - `type: "web_search_result_location"`

                        - `"web_search_result_location"`

                      - `url: string`

                    - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                      - `cited_text: string`

                      - `end_block_index: number`

                      - `search_result_index: number`

                      - `source: string`

                      - `start_block_index: number`

                      - `title: string`

                      - `type: "search_result_location"`

                        - `"search_result_location"`

                - `ImageBlockParam = object { source, type, cache_control }`

                  - `source: Base64ImageSource or URLImageSource`

                    - `Base64ImageSource = object { data, media_type, type }`

                      - `data: string`

                      - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                        - `"image/jpeg"`

                        - `"image/png"`

                        - `"image/gif"`

                        - `"image/webp"`

                      - `type: "base64"`

                        - `"base64"`

                    - `URLImageSource = object { type, url }`

                      - `type: "url"`

                        - `"url"`

                      - `url: string`

                  - `type: "image"`

                    - `"image"`

                  - `cache_control: optional CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: "ephemeral"`

                      - `"ephemeral"`

                    - `ttl: optional "5m" or "1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `"5m"`

                      - `"1h"`

                - `SearchResultBlockParam = object { content, source, title, 3 more }`

                  - `content: array of TextBlockParam`

                    - `text: string`

                    - `type: "text"`

                      - `"text"`

                    - `cache_control: optional CacheControlEphemeral`

                      Create a cache control breakpoint at this content block.

                      - `type: "ephemeral"`

                        - `"ephemeral"`

                      - `ttl: optional "5m" or "1h"`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `"5m"`

                        - `"1h"`

                    - `citations: optional array of TextCitationParam`

                      - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string`

                        - `end_char_index: number`

                        - `start_char_index: number`

                        - `type: "char_location"`

                          - `"char_location"`

                      - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string`

                        - `end_page_number: number`

                        - `start_page_number: number`

                        - `type: "page_location"`

                          - `"page_location"`

                      - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                        - `cited_text: string`

                        - `document_index: number`

                        - `document_title: string`

                        - `end_block_index: number`

                        - `start_block_index: number`

                        - `type: "content_block_location"`

                          - `"content_block_location"`

                      - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                        - `cited_text: string`

                        - `encrypted_index: string`

                        - `title: string`

                        - `type: "web_search_result_location"`

                          - `"web_search_result_location"`

                        - `url: string`

                      - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                        - `cited_text: string`

                        - `end_block_index: number`

                        - `search_result_index: number`

                        - `source: string`

                        - `start_block_index: number`

                        - `title: string`

                        - `type: "search_result_location"`

                          - `"search_result_location"`

                  - `source: string`

                  - `title: string`

                  - `type: "search_result"`

                    - `"search_result"`

                  - `cache_control: optional CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: "ephemeral"`

                      - `"ephemeral"`

                    - `ttl: optional "5m" or "1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `"5m"`

                      - `"1h"`

                  - `citations: optional CitationsConfigParam`

                    - `enabled: optional boolean`

                - `DocumentBlockParam = object { source, type, cache_control, 3 more }`

                  - `source: Base64PDFSource or PlainTextSource or ContentBlockSource or URLPDFSource`

                    - `Base64PDFSource = object { data, media_type, type }`

                      - `data: string`

                      - `media_type: "application/pdf"`

                        - `"application/pdf"`

                      - `type: "base64"`

                        - `"base64"`

                    - `PlainTextSource = object { data, media_type, type }`

                      - `data: string`

                      - `media_type: "text/plain"`

                        - `"text/plain"`

                      - `type: "text"`

                        - `"text"`

                    - `ContentBlockSource = object { content, type }`

                      - `content: string or array of ContentBlockSourceContent`

                        - `UnionMember0 = string`

                        - `ContentBlockSourceContent = array of ContentBlockSourceContent`

                          - `TextBlockParam = object { text, type, cache_control, citations }`

                            - `text: string`

                            - `type: "text"`

                              - `"text"`

                            - `cache_control: optional CacheControlEphemeral`

                              Create a cache control breakpoint at this content block.

                              - `type: "ephemeral"`

                                - `"ephemeral"`

                              - `ttl: optional "5m" or "1h"`

                                The time-to-live for the cache control breakpoint.

                                This may be one the following values:

                                - `5m`: 5 minutes
                                - `1h`: 1 hour

                                Defaults to `5m`.

                                - `"5m"`

                                - `"1h"`

                            - `citations: optional array of TextCitationParam`

                              - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                                - `cited_text: string`

                                - `document_index: number`

                                - `document_title: string`

                                - `end_char_index: number`

                                - `start_char_index: number`

                                - `type: "char_location"`

                                  - `"char_location"`

                              - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                                - `cited_text: string`

                                - `document_index: number`

                                - `document_title: string`

                                - `end_page_number: number`

                                - `start_page_number: number`

                                - `type: "page_location"`

                                  - `"page_location"`

                              - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                                - `cited_text: string`

                                - `document_index: number`

                                - `document_title: string`

                                - `end_block_index: number`

                                - `start_block_index: number`

                                - `type: "content_block_location"`

                                  - `"content_block_location"`

                              - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                                - `cited_text: string`

                                - `encrypted_index: string`

                                - `title: string`

                                - `type: "web_search_result_location"`

                                  - `"web_search_result_location"`

                                - `url: string`

                              - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                                - `cited_text: string`

                                - `end_block_index: number`

                                - `search_result_index: number`

                                - `source: string`

                                - `start_block_index: number`

                                - `title: string`

                                - `type: "search_result_location"`

                                  - `"search_result_location"`

                          - `ImageBlockParam = object { source, type, cache_control }`

                            - `source: Base64ImageSource or URLImageSource`

                              - `Base64ImageSource = object { data, media_type, type }`

                                - `data: string`

                                - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                                  - `"image/jpeg"`

                                  - `"image/png"`

                                  - `"image/gif"`

                                  - `"image/webp"`

                                - `type: "base64"`

                                  - `"base64"`

                              - `URLImageSource = object { type, url }`

                                - `type: "url"`

                                  - `"url"`

                                - `url: string`

                            - `type: "image"`

                              - `"image"`

                            - `cache_control: optional CacheControlEphemeral`

                              Create a cache control breakpoint at this content block.

                              - `type: "ephemeral"`

                                - `"ephemeral"`

                              - `ttl: optional "5m" or "1h"`

                                The time-to-live for the cache control breakpoint.

                                This may be one the following values:

                                - `5m`: 5 minutes
                                - `1h`: 1 hour

                                Defaults to `5m`.

                                - `"5m"`

                                - `"1h"`

                      - `type: "content"`

                        - `"content"`

                    - `URLPDFSource = object { type, url }`

                      - `type: "url"`

                        - `"url"`

                      - `url: string`

                  - `type: "document"`

                    - `"document"`

                  - `cache_control: optional CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `type: "ephemeral"`

                      - `"ephemeral"`

                    - `ttl: optional "5m" or "1h"`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `"5m"`

                      - `"1h"`

                  - `citations: optional CitationsConfigParam`

                    - `enabled: optional boolean`

                  - `context: optional string`

                  - `title: optional string`

            - `is_error: optional boolean`

          - `ServerToolUseBlockParam = object { id, input, name, 2 more }`

            - `id: string`

            - `input: map[unknown]`

            - `name: "web_search"`

              - `"web_search"`

            - `type: "server_tool_use"`

              - `"server_tool_use"`

            - `cache_control: optional CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: "ephemeral"`

                - `"ephemeral"`

              - `ttl: optional "5m" or "1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `"5m"`

                - `"1h"`

          - `WebSearchToolResultBlockParam = object { content, tool_use_id, type, cache_control }`

            - `content: WebSearchToolResultBlockParamContent`

              - `WebSearchToolResultBlockItem = array of WebSearchResultBlockParam`

                - `encrypted_content: string`

                - `title: string`

                - `type: "web_search_result"`

                  - `"web_search_result"`

                - `url: string`

                - `page_age: optional string`

              - `WebSearchToolRequestError = object { error_code, type }`

                - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

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

            - `cache_control: optional CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `type: "ephemeral"`

                - `"ephemeral"`

              - `ttl: optional "5m" or "1h"`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `"5m"`

                - `"1h"`

      - `role: "user" or "assistant"`

        - `"user"`

        - `"assistant"`

    - `model: Model`

      The model that will complete your prompt.

      See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

      - `UnionMember0 = "claude-opus-4-5-20251101" or "claude-opus-4-5" or "claude-3-7-sonnet-latest" or 17 more`

        The model that will complete your prompt.

        See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

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

      - `UnionMember1 = string`

    - `metadata: optional Metadata`

      An object describing metadata about the request.

      - `user_id: optional string`

        An external identifier for the user who is associated with the request.

        This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

    - `service_tier: optional "auto" or "standard_only"`

      Determines whether to use priority capacity (if available) or standard capacity for this request.

      Anthropic offers different levels of service for your API requests. See [service-tiers](https://docs.claude.com/en/api/service-tiers) for details.

      - `"auto"`

      - `"standard_only"`

    - `stop_sequences: optional array of string`

      Custom text sequences that will cause the model to stop generating.

      Our models will normally stop when they have naturally completed their turn, which will result in a response `stop_reason` of `"end_turn"`.

      If you want the model to stop generating when it encounters custom strings of text, you can use the `stop_sequences` parameter. If the model encounters one of the custom sequences, the response `stop_reason` value will be `"stop_sequence"` and the response `stop_sequence` value will contain the matched stop sequence.

    - `stream: optional boolean`

      Whether to incrementally stream the response using server-sent events.

      See [streaming](https://docs.claude.com/en/api/messages-streaming) for details.

    - `system: optional string or array of TextBlockParam`

      System prompt.

      A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

      - `UnionMember0 = string`

      - `UnionMember1 = array of TextBlockParam`

        - `text: string`

        - `type: "text"`

          - `"text"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `citations: optional array of TextCitationParam`

          - `CitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_char_index: number`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `CitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_page_number: number`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `CitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_block_index: number`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `CitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `CitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string`

            - `type: "search_result_location"`

              - `"search_result_location"`

    - `temperature: optional number`

      Amount of randomness injected into the response.

      Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.

      Note that even with `temperature` of `0.0`, the results will not be fully deterministic.

    - `thinking: optional ThinkingConfigParam`

      Configuration for enabling Claude's extended thinking.

      When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

      See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

      - `ThinkingConfigEnabled = object { budget_tokens, type }`

        - `budget_tokens: number`

          Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

          Must be ≥1024 and less than `max_tokens`.

          See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

        - `type: "enabled"`

          - `"enabled"`

      - `ThinkingConfigDisabled = object { type }`

        - `type: "disabled"`

          - `"disabled"`

    - `tool_choice: optional ToolChoice`

      How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

      - `ToolChoiceAuto = object { type, disable_parallel_tool_use }`

        The model will automatically decide whether to use tools.

        - `type: "auto"`

          - `"auto"`

        - `disable_parallel_tool_use: optional boolean`

          Whether to disable parallel tool use.

          Defaults to `false`. If set to `true`, the model will output at most one tool use.

      - `ToolChoiceAny = object { type, disable_parallel_tool_use }`

        The model will use any available tools.

        - `type: "any"`

          - `"any"`

        - `disable_parallel_tool_use: optional boolean`

          Whether to disable parallel tool use.

          Defaults to `false`. If set to `true`, the model will output exactly one tool use.

      - `ToolChoiceTool = object { name, type, disable_parallel_tool_use }`

        The model will use the specified tool with `tool_choice.name`.

        - `name: string`

          The name of the tool to use.

        - `type: "tool"`

          - `"tool"`

        - `disable_parallel_tool_use: optional boolean`

          Whether to disable parallel tool use.

          Defaults to `false`. If set to `true`, the model will output exactly one tool use.

      - `ToolChoiceNone = object { type }`

        The model will not be allowed to use tools.

        - `type: "none"`

          - `"none"`

    - `tools: optional array of ToolUnion`

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

      - `Tool = object { input_schema, name, cache_control, 2 more }`

        - `input_schema: object { type, properties, required }`

          [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

          This defines the shape of the `input` that your tool accepts and that the model will produce.

          - `type: "object"`

            - `"object"`

          - `properties: optional map[unknown]`

          - `required: optional array of string`

        - `name: string`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `description: optional string`

          Description of what this tool does.

          Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

        - `type: optional "custom"`

          - `"custom"`

      - `ToolBash20250124 = object { name, type, cache_control }`

        - `name: "bash"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"bash"`

        - `type: "bash_20250124"`

          - `"bash_20250124"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

      - `ToolTextEditor20250124 = object { name, type, cache_control }`

        - `name: "str_replace_editor"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"str_replace_editor"`

        - `type: "text_editor_20250124"`

          - `"text_editor_20250124"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

      - `ToolTextEditor20250429 = object { name, type, cache_control }`

        - `name: "str_replace_based_edit_tool"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"str_replace_based_edit_tool"`

        - `type: "text_editor_20250429"`

          - `"text_editor_20250429"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

      - `ToolTextEditor20250728 = object { name, type, cache_control, max_characters }`

        - `name: "str_replace_based_edit_tool"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"str_replace_based_edit_tool"`

        - `type: "text_editor_20250728"`

          - `"text_editor_20250728"`

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `max_characters: optional number`

          Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

      - `WebSearchTool20250305 = object { name, type, allowed_domains, 4 more }`

        - `name: "web_search"`

          Name of the tool.

          This is how the tool will be called by the model and in `tool_use` blocks.

          - `"web_search"`

        - `type: "web_search_20250305"`

          - `"web_search_20250305"`

        - `allowed_domains: optional array of string`

          If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

        - `blocked_domains: optional array of string`

          If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

        - `cache_control: optional CacheControlEphemeral`

          Create a cache control breakpoint at this content block.

          - `type: "ephemeral"`

            - `"ephemeral"`

          - `ttl: optional "5m" or "1h"`

            The time-to-live for the cache control breakpoint.

            This may be one the following values:

            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.

            - `"5m"`

            - `"1h"`

        - `max_uses: optional number`

          Maximum number of times the tool can be used in the API request.

        - `user_location: optional object { type, city, country, 2 more }`

          Parameters for the user's location. Used to provide more relevant search results.

          - `type: "approximate"`

            - `"approximate"`

          - `city: optional string`

            The city of the user.

          - `country: optional string`

            The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

          - `region: optional string`

            The region of the user.

          - `timezone: optional string`

            The [IANA timezone](https://nodatime.org/TimeZones) of the user.

    - `top_k: optional number`

      Only sample from the top K options for each subsequent token.

      Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

      Recommended for advanced use cases only. You usually only need to use `temperature`.

    - `top_p: optional number`

      Use nucleus sampling.

      In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

      Recommended for advanced use cases only. You usually only need to use `temperature`.

### Returns

- `MessageBatch = object { id, archived_at, cancel_initiated_at, 7 more }`

  - `id: string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archived_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancel_initiated_at: string`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `created_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `ended_at: string`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expires_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processing_status: "in_progress" or "canceling" or "ended"`

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

  - `results_url: string`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: "message_batch"`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `"message_batch"`

### Example

```http
curl https://api.anthropic.com/v1/messages/batches \
    -H 'Content-Type: application/json' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY" \
    -d '{
          "requests": [
            {
              "custom_id": "my-custom-id-1",
              "params": {
                "max_tokens": 1024,
                "messages": [
                  {
                    "content": "Hello, world",
                    "role": "user"
                  }
                ],
                "model": "claude-sonnet-4-5-20250929"
              }
            }
          ]
        }'
```

## Retrieve

**get** `/v1/messages/batches/{message_batch_id}`

This endpoint is idempotent and can be used to poll for Message Batch completion. To access the results of a Message Batch, make a request to the `results_url` field in the response.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Path Parameters

- `message_batch_id: string`

  ID of the Message Batch.

### Returns

- `MessageBatch = object { id, archived_at, cancel_initiated_at, 7 more }`

  - `id: string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archived_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancel_initiated_at: string`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `created_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `ended_at: string`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expires_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processing_status: "in_progress" or "canceling" or "ended"`

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

  - `results_url: string`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: "message_batch"`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `"message_batch"`

### Example

```http
curl https://api.anthropic.com/v1/messages/batches/$MESSAGE_BATCH_ID \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

## List

**get** `/v1/messages/batches`

List all Message Batches within a Workspace. Most recently created batches are returned first.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Query Parameters

- `after_id: optional string`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: optional string`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `limit: optional number`

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

### Returns

- `data: array of MessageBatch`

  - `id: string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archived_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancel_initiated_at: string`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `created_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `ended_at: string`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expires_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processing_status: "in_progress" or "canceling" or "ended"`

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

  - `results_url: string`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: "message_batch"`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `"message_batch"`

- `first_id: string`

  First ID in the `data` list. Can be used as the `before_id` for the previous page.

- `has_more: boolean`

  Indicates if there are more results in the requested page direction.

- `last_id: string`

  Last ID in the `data` list. Can be used as the `after_id` for the next page.

### Example

```http
curl https://api.anthropic.com/v1/messages/batches \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

## Cancel

**post** `/v1/messages/batches/{message_batch_id}/cancel`

Batches may be canceled any time before processing ends. Once cancellation is initiated, the batch enters a `canceling` state, at which time the system may complete any in-progress, non-interruptible requests before finalizing cancellation.

The number of canceled requests is specified in `request_counts`. To determine which requests were canceled, check the individual results within the batch. Note that cancellation may not result in any canceled requests if they were non-interruptible.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Path Parameters

- `message_batch_id: string`

  ID of the Message Batch.

### Returns

- `MessageBatch = object { id, archived_at, cancel_initiated_at, 7 more }`

  - `id: string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archived_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancel_initiated_at: string`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `created_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `ended_at: string`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expires_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processing_status: "in_progress" or "canceling" or "ended"`

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

  - `results_url: string`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: "message_batch"`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `"message_batch"`

### Example

```http
curl https://api.anthropic.com/v1/messages/batches/$MESSAGE_BATCH_ID/cancel \
    -X POST \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

## Delete

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Path Parameters

- `message_batch_id: string`

  ID of the Message Batch.

### Returns

- `DeletedMessageBatch = object { id, type }`

  - `id: string`

    ID of the Message Batch.

  - `type: "message_batch_deleted"`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `"message_batch_deleted"`

### Example

```http
curl https://api.anthropic.com/v1/messages/batches/$MESSAGE_BATCH_ID \
    -X DELETE \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

## Results

**get** `/v1/messages/batches/{message_batch_id}/results`

Streams the results of a Message Batch as a `.jsonl` file.

Each line in the file is a JSON object containing the result of a single request in the Message Batch. Results are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Path Parameters

- `message_batch_id: string`

  ID of the Message Batch.

### Returns

- `MessageBatchIndividualResponse = object { custom_id, result }`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `custom_id: string`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: MessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `MessageBatchSucceededResult = object { message, type }`

      - `message: Message`

        - `id: string`

          Unique object identifier.

          The format and length of IDs may change over time.

        - `content: array of ContentBlock`

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

          - `TextBlock = object { citations, text, type }`

            - `citations: array of TextCitation`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_char_index: number`

                - `file_id: string`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_page_number: number`

                - `file_id: string`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_block_index: number`

                - `file_id: string`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string`

                - `type: "search_result_location"`

                  - `"search_result_location"`

            - `text: string`

            - `type: "text"`

              - `"text"`

          - `ThinkingBlock = object { signature, thinking, type }`

            - `signature: string`

            - `thinking: string`

            - `type: "thinking"`

              - `"thinking"`

          - `RedactedThinkingBlock = object { data, type }`

            - `data: string`

            - `type: "redacted_thinking"`

              - `"redacted_thinking"`

          - `ToolUseBlock = object { id, input, name, type }`

            - `id: string`

            - `input: map[unknown]`

            - `name: string`

            - `type: "tool_use"`

              - `"tool_use"`

          - `ServerToolUseBlock = object { id, input, name, type }`

            - `id: string`

            - `input: map[unknown]`

            - `name: "web_search"`

              - `"web_search"`

            - `type: "server_tool_use"`

              - `"server_tool_use"`

          - `WebSearchToolResultBlock = object { content, tool_use_id, type }`

            - `content: WebSearchToolResultBlockContent`

              - `WebSearchToolResultError = object { error_code, type }`

                - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"max_uses_exceeded"`

                  - `"too_many_requests"`

                  - `"query_too_long"`

                - `type: "web_search_tool_result_error"`

                  - `"web_search_tool_result_error"`

              - `UnionMember1 = array of WebSearchResultBlock`

                - `encrypted_content: string`

                - `page_age: string`

                - `title: string`

                - `type: "web_search_result"`

                  - `"web_search_result"`

                - `url: string`

            - `tool_use_id: string`

            - `type: "web_search_tool_result"`

              - `"web_search_tool_result"`

        - `model: Model`

          The model that will complete your prompt.

          See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

          - `UnionMember0 = "claude-opus-4-5-20251101" or "claude-opus-4-5" or "claude-3-7-sonnet-latest" or 17 more`

            The model that will complete your prompt.

            See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

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

          - `UnionMember1 = string`

        - `role: "assistant"`

          Conversational role of the generated message.

          This will always be `"assistant"`.

          - `"assistant"`

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

          - `"end_turn"`

          - `"max_tokens"`

          - `"stop_sequence"`

          - `"tool_use"`

          - `"pause_turn"`

          - `"refusal"`

        - `stop_sequence: string`

          Which custom stop sequence was generated, if any.

          This value will be a non-null string if one of your custom stop sequences was generated.

        - `type: "message"`

          Object type.

          For Messages, this is always `"message"`.

          - `"message"`

        - `usage: Usage`

          Billing and rate-limit usage.

          Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

          Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

          For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

          Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

          - `cache_creation: CacheCreation`

            Breakdown of cached tokens by TTL

            - `ephemeral_1h_input_tokens: number`

              The number of input tokens used to create the 1 hour cache entry.

            - `ephemeral_5m_input_tokens: number`

              The number of input tokens used to create the 5 minute cache entry.

          - `cache_creation_input_tokens: number`

            The number of input tokens used to create the cache entry.

          - `cache_read_input_tokens: number`

            The number of input tokens read from the cache.

          - `input_tokens: number`

            The number of input tokens which were used.

          - `output_tokens: number`

            The number of output tokens which were used.

          - `server_tool_use: ServerToolUsage`

            The number of server tool requests.

            - `web_search_requests: number`

              The number of web search tool requests.

          - `service_tier: "standard" or "priority" or "batch"`

            If the request used the priority, standard, or batch tier.

            - `"standard"`

            - `"priority"`

            - `"batch"`

      - `type: "succeeded"`

        - `"succeeded"`

    - `MessageBatchErroredResult = object { error, type }`

      - `error: ErrorResponse`

        - `error: ErrorObject`

          - `InvalidRequestError = object { message, type }`

            - `message: string`

            - `type: "invalid_request_error"`

              - `"invalid_request_error"`

          - `AuthenticationError = object { message, type }`

            - `message: string`

            - `type: "authentication_error"`

              - `"authentication_error"`

          - `BillingError = object { message, type }`

            - `message: string`

            - `type: "billing_error"`

              - `"billing_error"`

          - `PermissionError = object { message, type }`

            - `message: string`

            - `type: "permission_error"`

              - `"permission_error"`

          - `NotFoundError = object { message, type }`

            - `message: string`

            - `type: "not_found_error"`

              - `"not_found_error"`

          - `RateLimitError = object { message, type }`

            - `message: string`

            - `type: "rate_limit_error"`

              - `"rate_limit_error"`

          - `GatewayTimeoutError = object { message, type }`

            - `message: string`

            - `type: "timeout_error"`

              - `"timeout_error"`

          - `APIErrorObject = object { message, type }`

            - `message: string`

            - `type: "api_error"`

              - `"api_error"`

          - `OverloadedError = object { message, type }`

            - `message: string`

            - `type: "overloaded_error"`

              - `"overloaded_error"`

        - `request_id: string`

        - `type: "error"`

          - `"error"`

      - `type: "errored"`

        - `"errored"`

    - `MessageBatchCanceledResult = object { type }`

      - `type: "canceled"`

        - `"canceled"`

    - `MessageBatchExpiredResult = object { type }`

      - `type: "expired"`

        - `"expired"`

### Example

```http
curl https://api.anthropic.com/v1/messages/batches/$MESSAGE_BATCH_ID/results \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

## Domain Types

### Deleted Message Batch

- `DeletedMessageBatch = object { id, type }`

  - `id: string`

    ID of the Message Batch.

  - `type: "message_batch_deleted"`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `"message_batch_deleted"`

### Message Batch

- `MessageBatch = object { id, archived_at, cancel_initiated_at, 7 more }`

  - `id: string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `archived_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch was archived and its results became unavailable.

  - `cancel_initiated_at: string`

    RFC 3339 datetime string representing the time at which cancellation was initiated for the Message Batch. Specified only if cancellation was initiated.

  - `created_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch was created.

  - `ended_at: string`

    RFC 3339 datetime string representing the time at which processing for the Message Batch ended. Specified only once processing ends.

    Processing ends when every request in a Message Batch has either succeeded, errored, canceled, or expired.

  - `expires_at: string`

    RFC 3339 datetime string representing the time at which the Message Batch will expire and end processing, which is 24 hours after creation.

  - `processing_status: "in_progress" or "canceling" or "ended"`

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

  - `results_url: string`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: "message_batch"`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `"message_batch"`

### Message Batch Canceled Result

- `MessageBatchCanceledResult = object { type }`

  - `type: "canceled"`

    - `"canceled"`

### Message Batch Errored Result

- `MessageBatchErroredResult = object { error, type }`

  - `error: ErrorResponse`

    - `error: ErrorObject`

      - `InvalidRequestError = object { message, type }`

        - `message: string`

        - `type: "invalid_request_error"`

          - `"invalid_request_error"`

      - `AuthenticationError = object { message, type }`

        - `message: string`

        - `type: "authentication_error"`

          - `"authentication_error"`

      - `BillingError = object { message, type }`

        - `message: string`

        - `type: "billing_error"`

          - `"billing_error"`

      - `PermissionError = object { message, type }`

        - `message: string`

        - `type: "permission_error"`

          - `"permission_error"`

      - `NotFoundError = object { message, type }`

        - `message: string`

        - `type: "not_found_error"`

          - `"not_found_error"`

      - `RateLimitError = object { message, type }`

        - `message: string`

        - `type: "rate_limit_error"`

          - `"rate_limit_error"`

      - `GatewayTimeoutError = object { message, type }`

        - `message: string`

        - `type: "timeout_error"`

          - `"timeout_error"`

      - `APIErrorObject = object { message, type }`

        - `message: string`

        - `type: "api_error"`

          - `"api_error"`

      - `OverloadedError = object { message, type }`

        - `message: string`

        - `type: "overloaded_error"`

          - `"overloaded_error"`

    - `request_id: string`

    - `type: "error"`

      - `"error"`

  - `type: "errored"`

    - `"errored"`

### Message Batch Expired Result

- `MessageBatchExpiredResult = object { type }`

  - `type: "expired"`

    - `"expired"`

### Message Batch Individual Response

- `MessageBatchIndividualResponse = object { custom_id, result }`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `custom_id: string`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: MessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `MessageBatchSucceededResult = object { message, type }`

      - `message: Message`

        - `id: string`

          Unique object identifier.

          The format and length of IDs may change over time.

        - `content: array of ContentBlock`

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

          - `TextBlock = object { citations, text, type }`

            - `citations: array of TextCitation`

              Citations supporting the text block.

              The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

              - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_char_index: number`

                - `file_id: string`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_page_number: number`

                - `file_id: string`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_block_index: number`

                - `file_id: string`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string`

                - `type: "search_result_location"`

                  - `"search_result_location"`

            - `text: string`

            - `type: "text"`

              - `"text"`

          - `ThinkingBlock = object { signature, thinking, type }`

            - `signature: string`

            - `thinking: string`

            - `type: "thinking"`

              - `"thinking"`

          - `RedactedThinkingBlock = object { data, type }`

            - `data: string`

            - `type: "redacted_thinking"`

              - `"redacted_thinking"`

          - `ToolUseBlock = object { id, input, name, type }`

            - `id: string`

            - `input: map[unknown]`

            - `name: string`

            - `type: "tool_use"`

              - `"tool_use"`

          - `ServerToolUseBlock = object { id, input, name, type }`

            - `id: string`

            - `input: map[unknown]`

            - `name: "web_search"`

              - `"web_search"`

            - `type: "server_tool_use"`

              - `"server_tool_use"`

          - `WebSearchToolResultBlock = object { content, tool_use_id, type }`

            - `content: WebSearchToolResultBlockContent`

              - `WebSearchToolResultError = object { error_code, type }`

                - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

                  - `"invalid_tool_input"`

                  - `"unavailable"`

                  - `"max_uses_exceeded"`

                  - `"too_many_requests"`

                  - `"query_too_long"`

                - `type: "web_search_tool_result_error"`

                  - `"web_search_tool_result_error"`

              - `UnionMember1 = array of WebSearchResultBlock`

                - `encrypted_content: string`

                - `page_age: string`

                - `title: string`

                - `type: "web_search_result"`

                  - `"web_search_result"`

                - `url: string`

            - `tool_use_id: string`

            - `type: "web_search_tool_result"`

              - `"web_search_tool_result"`

        - `model: Model`

          The model that will complete your prompt.

          See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

          - `UnionMember0 = "claude-opus-4-5-20251101" or "claude-opus-4-5" or "claude-3-7-sonnet-latest" or 17 more`

            The model that will complete your prompt.

            See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

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

          - `UnionMember1 = string`

        - `role: "assistant"`

          Conversational role of the generated message.

          This will always be `"assistant"`.

          - `"assistant"`

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

          - `"end_turn"`

          - `"max_tokens"`

          - `"stop_sequence"`

          - `"tool_use"`

          - `"pause_turn"`

          - `"refusal"`

        - `stop_sequence: string`

          Which custom stop sequence was generated, if any.

          This value will be a non-null string if one of your custom stop sequences was generated.

        - `type: "message"`

          Object type.

          For Messages, this is always `"message"`.

          - `"message"`

        - `usage: Usage`

          Billing and rate-limit usage.

          Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

          Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

          For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

          Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

          - `cache_creation: CacheCreation`

            Breakdown of cached tokens by TTL

            - `ephemeral_1h_input_tokens: number`

              The number of input tokens used to create the 1 hour cache entry.

            - `ephemeral_5m_input_tokens: number`

              The number of input tokens used to create the 5 minute cache entry.

          - `cache_creation_input_tokens: number`

            The number of input tokens used to create the cache entry.

          - `cache_read_input_tokens: number`

            The number of input tokens read from the cache.

          - `input_tokens: number`

            The number of input tokens which were used.

          - `output_tokens: number`

            The number of output tokens which were used.

          - `server_tool_use: ServerToolUsage`

            The number of server tool requests.

            - `web_search_requests: number`

              The number of web search tool requests.

          - `service_tier: "standard" or "priority" or "batch"`

            If the request used the priority, standard, or batch tier.

            - `"standard"`

            - `"priority"`

            - `"batch"`

      - `type: "succeeded"`

        - `"succeeded"`

    - `MessageBatchErroredResult = object { error, type }`

      - `error: ErrorResponse`

        - `error: ErrorObject`

          - `InvalidRequestError = object { message, type }`

            - `message: string`

            - `type: "invalid_request_error"`

              - `"invalid_request_error"`

          - `AuthenticationError = object { message, type }`

            - `message: string`

            - `type: "authentication_error"`

              - `"authentication_error"`

          - `BillingError = object { message, type }`

            - `message: string`

            - `type: "billing_error"`

              - `"billing_error"`

          - `PermissionError = object { message, type }`

            - `message: string`

            - `type: "permission_error"`

              - `"permission_error"`

          - `NotFoundError = object { message, type }`

            - `message: string`

            - `type: "not_found_error"`

              - `"not_found_error"`

          - `RateLimitError = object { message, type }`

            - `message: string`

            - `type: "rate_limit_error"`

              - `"rate_limit_error"`

          - `GatewayTimeoutError = object { message, type }`

            - `message: string`

            - `type: "timeout_error"`

              - `"timeout_error"`

          - `APIErrorObject = object { message, type }`

            - `message: string`

            - `type: "api_error"`

              - `"api_error"`

          - `OverloadedError = object { message, type }`

            - `message: string`

            - `type: "overloaded_error"`

              - `"overloaded_error"`

        - `request_id: string`

        - `type: "error"`

          - `"error"`

      - `type: "errored"`

        - `"errored"`

    - `MessageBatchCanceledResult = object { type }`

      - `type: "canceled"`

        - `"canceled"`

    - `MessageBatchExpiredResult = object { type }`

      - `type: "expired"`

        - `"expired"`

### Message Batch Request Counts

- `MessageBatchRequestCounts = object { canceled, errored, expired, 2 more }`

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

### Message Batch Result

- `MessageBatchResult = MessageBatchSucceededResult or MessageBatchErroredResult or MessageBatchCanceledResult or MessageBatchExpiredResult`

  Processing result for this request.

  Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

  - `MessageBatchSucceededResult = object { message, type }`

    - `message: Message`

      - `id: string`

        Unique object identifier.

        The format and length of IDs may change over time.

      - `content: array of ContentBlock`

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

        - `TextBlock = object { citations, text, type }`

          - `citations: array of TextCitation`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_char_index: number`

              - `file_id: string`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_page_number: number`

              - `file_id: string`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_block_index: number`

              - `file_id: string`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

              - `cited_text: string`

              - `end_block_index: number`

              - `search_result_index: number`

              - `source: string`

              - `start_block_index: number`

              - `title: string`

              - `type: "search_result_location"`

                - `"search_result_location"`

          - `text: string`

          - `type: "text"`

            - `"text"`

        - `ThinkingBlock = object { signature, thinking, type }`

          - `signature: string`

          - `thinking: string`

          - `type: "thinking"`

            - `"thinking"`

        - `RedactedThinkingBlock = object { data, type }`

          - `data: string`

          - `type: "redacted_thinking"`

            - `"redacted_thinking"`

        - `ToolUseBlock = object { id, input, name, type }`

          - `id: string`

          - `input: map[unknown]`

          - `name: string`

          - `type: "tool_use"`

            - `"tool_use"`

        - `ServerToolUseBlock = object { id, input, name, type }`

          - `id: string`

          - `input: map[unknown]`

          - `name: "web_search"`

            - `"web_search"`

          - `type: "server_tool_use"`

            - `"server_tool_use"`

        - `WebSearchToolResultBlock = object { content, tool_use_id, type }`

          - `content: WebSearchToolResultBlockContent`

            - `WebSearchToolResultError = object { error_code, type }`

              - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

                - `"invalid_tool_input"`

                - `"unavailable"`

                - `"max_uses_exceeded"`

                - `"too_many_requests"`

                - `"query_too_long"`

              - `type: "web_search_tool_result_error"`

                - `"web_search_tool_result_error"`

            - `UnionMember1 = array of WebSearchResultBlock`

              - `encrypted_content: string`

              - `page_age: string`

              - `title: string`

              - `type: "web_search_result"`

                - `"web_search_result"`

              - `url: string`

          - `tool_use_id: string`

          - `type: "web_search_tool_result"`

            - `"web_search_tool_result"`

      - `model: Model`

        The model that will complete your prompt.

        See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

        - `UnionMember0 = "claude-opus-4-5-20251101" or "claude-opus-4-5" or "claude-3-7-sonnet-latest" or 17 more`

          The model that will complete your prompt.

          See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

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

        - `UnionMember1 = string`

      - `role: "assistant"`

        Conversational role of the generated message.

        This will always be `"assistant"`.

        - `"assistant"`

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

        - `"end_turn"`

        - `"max_tokens"`

        - `"stop_sequence"`

        - `"tool_use"`

        - `"pause_turn"`

        - `"refusal"`

      - `stop_sequence: string`

        Which custom stop sequence was generated, if any.

        This value will be a non-null string if one of your custom stop sequences was generated.

      - `type: "message"`

        Object type.

        For Messages, this is always `"message"`.

        - `"message"`

      - `usage: Usage`

        Billing and rate-limit usage.

        Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

        Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

        For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

        Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

        - `cache_creation: CacheCreation`

          Breakdown of cached tokens by TTL

          - `ephemeral_1h_input_tokens: number`

            The number of input tokens used to create the 1 hour cache entry.

          - `ephemeral_5m_input_tokens: number`

            The number of input tokens used to create the 5 minute cache entry.

        - `cache_creation_input_tokens: number`

          The number of input tokens used to create the cache entry.

        - `cache_read_input_tokens: number`

          The number of input tokens read from the cache.

        - `input_tokens: number`

          The number of input tokens which were used.

        - `output_tokens: number`

          The number of output tokens which were used.

        - `server_tool_use: ServerToolUsage`

          The number of server tool requests.

          - `web_search_requests: number`

            The number of web search tool requests.

        - `service_tier: "standard" or "priority" or "batch"`

          If the request used the priority, standard, or batch tier.

          - `"standard"`

          - `"priority"`

          - `"batch"`

    - `type: "succeeded"`

      - `"succeeded"`

  - `MessageBatchErroredResult = object { error, type }`

    - `error: ErrorResponse`

      - `error: ErrorObject`

        - `InvalidRequestError = object { message, type }`

          - `message: string`

          - `type: "invalid_request_error"`

            - `"invalid_request_error"`

        - `AuthenticationError = object { message, type }`

          - `message: string`

          - `type: "authentication_error"`

            - `"authentication_error"`

        - `BillingError = object { message, type }`

          - `message: string`

          - `type: "billing_error"`

            - `"billing_error"`

        - `PermissionError = object { message, type }`

          - `message: string`

          - `type: "permission_error"`

            - `"permission_error"`

        - `NotFoundError = object { message, type }`

          - `message: string`

          - `type: "not_found_error"`

            - `"not_found_error"`

        - `RateLimitError = object { message, type }`

          - `message: string`

          - `type: "rate_limit_error"`

            - `"rate_limit_error"`

        - `GatewayTimeoutError = object { message, type }`

          - `message: string`

          - `type: "timeout_error"`

            - `"timeout_error"`

        - `APIErrorObject = object { message, type }`

          - `message: string`

          - `type: "api_error"`

            - `"api_error"`

        - `OverloadedError = object { message, type }`

          - `message: string`

          - `type: "overloaded_error"`

            - `"overloaded_error"`

      - `request_id: string`

      - `type: "error"`

        - `"error"`

    - `type: "errored"`

      - `"errored"`

  - `MessageBatchCanceledResult = object { type }`

    - `type: "canceled"`

      - `"canceled"`

  - `MessageBatchExpiredResult = object { type }`

    - `type: "expired"`

      - `"expired"`

### Message Batch Succeeded Result

- `MessageBatchSucceededResult = object { message, type }`

  - `message: Message`

    - `id: string`

      Unique object identifier.

      The format and length of IDs may change over time.

    - `content: array of ContentBlock`

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

      - `TextBlock = object { citations, text, type }`

        - `citations: array of TextCitation`

          Citations supporting the text block.

          The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

          - `CitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_char_index: number`

            - `file_id: string`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `CitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_page_number: number`

            - `file_id: string`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `CitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_block_index: number`

            - `file_id: string`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `CitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `CitationsSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string`

            - `type: "search_result_location"`

              - `"search_result_location"`

        - `text: string`

        - `type: "text"`

          - `"text"`

      - `ThinkingBlock = object { signature, thinking, type }`

        - `signature: string`

        - `thinking: string`

        - `type: "thinking"`

          - `"thinking"`

      - `RedactedThinkingBlock = object { data, type }`

        - `data: string`

        - `type: "redacted_thinking"`

          - `"redacted_thinking"`

      - `ToolUseBlock = object { id, input, name, type }`

        - `id: string`

        - `input: map[unknown]`

        - `name: string`

        - `type: "tool_use"`

          - `"tool_use"`

      - `ServerToolUseBlock = object { id, input, name, type }`

        - `id: string`

        - `input: map[unknown]`

        - `name: "web_search"`

          - `"web_search"`

        - `type: "server_tool_use"`

          - `"server_tool_use"`

      - `WebSearchToolResultBlock = object { content, tool_use_id, type }`

        - `content: WebSearchToolResultBlockContent`

          - `WebSearchToolResultError = object { error_code, type }`

            - `error_code: "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"max_uses_exceeded"`

              - `"too_many_requests"`

              - `"query_too_long"`

            - `type: "web_search_tool_result_error"`

              - `"web_search_tool_result_error"`

          - `UnionMember1 = array of WebSearchResultBlock`

            - `encrypted_content: string`

            - `page_age: string`

            - `title: string`

            - `type: "web_search_result"`

              - `"web_search_result"`

            - `url: string`

        - `tool_use_id: string`

        - `type: "web_search_tool_result"`

          - `"web_search_tool_result"`

    - `model: Model`

      The model that will complete your prompt.

      See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

      - `UnionMember0 = "claude-opus-4-5-20251101" or "claude-opus-4-5" or "claude-3-7-sonnet-latest" or 17 more`

        The model that will complete your prompt.

        See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

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

      - `UnionMember1 = string`

    - `role: "assistant"`

      Conversational role of the generated message.

      This will always be `"assistant"`.

      - `"assistant"`

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

      - `"end_turn"`

      - `"max_tokens"`

      - `"stop_sequence"`

      - `"tool_use"`

      - `"pause_turn"`

      - `"refusal"`

    - `stop_sequence: string`

      Which custom stop sequence was generated, if any.

      This value will be a non-null string if one of your custom stop sequences was generated.

    - `type: "message"`

      Object type.

      For Messages, this is always `"message"`.

      - `"message"`

    - `usage: Usage`

      Billing and rate-limit usage.

      Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

      Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

      For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

      Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

      - `cache_creation: CacheCreation`

        Breakdown of cached tokens by TTL

        - `ephemeral_1h_input_tokens: number`

          The number of input tokens used to create the 1 hour cache entry.

        - `ephemeral_5m_input_tokens: number`

          The number of input tokens used to create the 5 minute cache entry.

      - `cache_creation_input_tokens: number`

        The number of input tokens used to create the cache entry.

      - `cache_read_input_tokens: number`

        The number of input tokens read from the cache.

      - `input_tokens: number`

        The number of input tokens which were used.

      - `output_tokens: number`

        The number of output tokens which were used.

      - `server_tool_use: ServerToolUsage`

        The number of server tool requests.

        - `web_search_requests: number`

          The number of web search tool requests.

      - `service_tier: "standard" or "priority" or "batch"`

        If the request used the priority, standard, or batch tier.

        - `"standard"`

        - `"priority"`

        - `"batch"`

  - `type: "succeeded"`

    - `"succeeded"`
