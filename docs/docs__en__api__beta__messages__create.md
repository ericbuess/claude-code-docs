## Create

**post** `/v1/messages`

Send a structured list of input messages with text and/or image content, and the model will generate the next message in the conversation.

The Messages API can be used for either single queries or stateless multi-turn conversations.

Learn more about the Messages API in our [user guide](https://docs.claude.com/en/docs/initial-setup)

### Header Parameters

- `"anthropic-beta": optional array of AnthropicBeta`

  Optional header to specify the beta version(s) you want to use.

  - `UnionMember0 = string`

  - `UnionMember1 = "message-batches-2024-09-24" or "prompt-caching-2024-07-31" or "computer-use-2024-10-22" or 16 more`

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

### Body Parameters

- `max_tokens: number`

  The maximum number of tokens to generate before stopping.

  Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

  Different models have different maximum values for this parameter.  See [models](https://docs.claude.com/en/docs/models-overview) for details.

- `messages: array of BetaMessageParam`

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

  - `content: string or array of BetaContentBlockParam`

    - `UnionMember0 = string`

    - `UnionMember1 = array of BetaContentBlockParam`

      - `BetaTextBlockParam = object { text, type, cache_control, citations }`

        - `text: string`

        - `type: "text"`

          - `"text"`

        - `cache_control: optional BetaCacheControlEphemeral`

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

        - `citations: optional array of BetaTextCitationParam`

          - `BetaCitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_char_index: number`

            - `start_char_index: number`

            - `type: "char_location"`

              - `"char_location"`

          - `BetaCitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_page_number: number`

            - `start_page_number: number`

            - `type: "page_location"`

              - `"page_location"`

          - `BetaCitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

            - `cited_text: string`

            - `document_index: number`

            - `document_title: string`

            - `end_block_index: number`

            - `start_block_index: number`

            - `type: "content_block_location"`

              - `"content_block_location"`

          - `BetaCitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

            - `cited_text: string`

            - `encrypted_index: string`

            - `title: string`

            - `type: "web_search_result_location"`

              - `"web_search_result_location"`

            - `url: string`

          - `BetaCitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

            - `cited_text: string`

            - `end_block_index: number`

            - `search_result_index: number`

            - `source: string`

            - `start_block_index: number`

            - `title: string`

            - `type: "search_result_location"`

              - `"search_result_location"`

      - `BetaImageBlockParam = object { source, type, cache_control }`

        - `source: BetaBase64ImageSource or BetaURLImageSource or BetaFileImageSource`

          - `BetaBase64ImageSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

              - `"image/jpeg"`

              - `"image/png"`

              - `"image/gif"`

              - `"image/webp"`

            - `type: "base64"`

              - `"base64"`

          - `BetaURLImageSource = object { type, url }`

            - `type: "url"`

              - `"url"`

            - `url: string`

          - `BetaFileImageSource = object { file_id, type }`

            - `file_id: string`

            - `type: "file"`

              - `"file"`

        - `type: "image"`

          - `"image"`

        - `cache_control: optional BetaCacheControlEphemeral`

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

      - `BetaRequestDocumentBlock = object { source, type, cache_control, 3 more }`

        - `source: BetaBase64PDFSource or BetaPlainTextSource or BetaContentBlockSource or 2 more`

          - `BetaBase64PDFSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "application/pdf"`

              - `"application/pdf"`

            - `type: "base64"`

              - `"base64"`

          - `BetaPlainTextSource = object { data, media_type, type }`

            - `data: string`

            - `media_type: "text/plain"`

              - `"text/plain"`

            - `type: "text"`

              - `"text"`

          - `BetaContentBlockSource = object { content, type }`

            - `content: string or array of BetaContentBlockSourceContent`

              - `UnionMember0 = string`

              - `BetaContentBlockSourceContent = array of BetaContentBlockSourceContent`

                - `BetaTextBlockParam = object { text, type, cache_control, citations }`

                  - `text: string`

                  - `type: "text"`

                    - `"text"`

                  - `cache_control: optional BetaCacheControlEphemeral`

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

                  - `citations: optional array of BetaTextCitationParam`

                    - `BetaCitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_char_index: number`

                      - `start_char_index: number`

                      - `type: "char_location"`

                        - `"char_location"`

                    - `BetaCitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_page_number: number`

                      - `start_page_number: number`

                      - `type: "page_location"`

                        - `"page_location"`

                    - `BetaCitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                      - `cited_text: string`

                      - `document_index: number`

                      - `document_title: string`

                      - `end_block_index: number`

                      - `start_block_index: number`

                      - `type: "content_block_location"`

                        - `"content_block_location"`

                    - `BetaCitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                      - `cited_text: string`

                      - `encrypted_index: string`

                      - `title: string`

                      - `type: "web_search_result_location"`

                        - `"web_search_result_location"`

                      - `url: string`

                    - `BetaCitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                      - `cited_text: string`

                      - `end_block_index: number`

                      - `search_result_index: number`

                      - `source: string`

                      - `start_block_index: number`

                      - `title: string`

                      - `type: "search_result_location"`

                        - `"search_result_location"`

                - `BetaImageBlockParam = object { source, type, cache_control }`

                  - `source: BetaBase64ImageSource or BetaURLImageSource or BetaFileImageSource`

                    - `BetaBase64ImageSource = object { data, media_type, type }`

                      - `data: string`

                      - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                        - `"image/jpeg"`

                        - `"image/png"`

                        - `"image/gif"`

                        - `"image/webp"`

                      - `type: "base64"`

                        - `"base64"`

                    - `BetaURLImageSource = object { type, url }`

                      - `type: "url"`

                        - `"url"`

                      - `url: string`

                    - `BetaFileImageSource = object { file_id, type }`

                      - `file_id: string`

                      - `type: "file"`

                        - `"file"`

                  - `type: "image"`

                    - `"image"`

                  - `cache_control: optional BetaCacheControlEphemeral`

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

          - `BetaURLPDFSource = object { type, url }`

            - `type: "url"`

              - `"url"`

            - `url: string`

          - `BetaFileDocumentSource = object { file_id, type }`

            - `file_id: string`

            - `type: "file"`

              - `"file"`

        - `type: "document"`

          - `"document"`

        - `cache_control: optional BetaCacheControlEphemeral`

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

        - `citations: optional BetaCitationsConfigParam`

          - `enabled: optional boolean`

        - `context: optional string`

        - `title: optional string`

      - `BetaSearchResultBlockParam = object { content, source, title, 3 more }`

        - `content: array of BetaTextBlockParam`

          - `text: string`

          - `type: "text"`

            - `"text"`

          - `cache_control: optional BetaCacheControlEphemeral`

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

          - `citations: optional array of BetaTextCitationParam`

            - `BetaCitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_char_index: number`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `BetaCitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_page_number: number`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `BetaCitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_block_index: number`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `BetaCitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `BetaCitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

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

        - `cache_control: optional BetaCacheControlEphemeral`

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

        - `citations: optional BetaCitationsConfigParam`

          - `enabled: optional boolean`

      - `BetaThinkingBlockParam = object { signature, thinking, type }`

        - `signature: string`

        - `thinking: string`

        - `type: "thinking"`

          - `"thinking"`

      - `BetaRedactedThinkingBlockParam = object { data, type }`

        - `data: string`

        - `type: "redacted_thinking"`

          - `"redacted_thinking"`

      - `BetaToolUseBlockParam = object { id, input, name, 3 more }`

        - `id: string`

        - `input: map[unknown]`

        - `name: string`

        - `type: "tool_use"`

          - `"tool_use"`

        - `cache_control: optional BetaCacheControlEphemeral`

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

        - `caller: optional BetaDirectCaller or BetaServerToolCaller`

          Tool invocation directly from the model.

          - `BetaDirectCaller = object { type }`

            Tool invocation directly from the model.

            - `type: "direct"`

              - `"direct"`

          - `BetaServerToolCaller = object { tool_id, type }`

            Tool invocation generated by a server-side tool.

            - `tool_id: string`

            - `type: "code_execution_20250825"`

              - `"code_execution_20250825"`

      - `BetaToolResultBlockParam = object { tool_use_id, type, cache_control, 2 more }`

        - `tool_use_id: string`

        - `type: "tool_result"`

          - `"tool_result"`

        - `cache_control: optional BetaCacheControlEphemeral`

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

        - `content: optional string or array of BetaTextBlockParam or BetaImageBlockParam or BetaSearchResultBlockParam or 2 more`

          - `UnionMember0 = string`

          - `UnionMember1 = array of BetaTextBlockParam or BetaImageBlockParam or BetaSearchResultBlockParam or 2 more`

            - `BetaTextBlockParam = object { text, type, cache_control, citations }`

              - `text: string`

              - `type: "text"`

                - `"text"`

              - `cache_control: optional BetaCacheControlEphemeral`

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

              - `citations: optional array of BetaTextCitationParam`

                - `BetaCitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_char_index: number`

                  - `start_char_index: number`

                  - `type: "char_location"`

                    - `"char_location"`

                - `BetaCitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_page_number: number`

                  - `start_page_number: number`

                  - `type: "page_location"`

                    - `"page_location"`

                - `BetaCitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                  - `cited_text: string`

                  - `document_index: number`

                  - `document_title: string`

                  - `end_block_index: number`

                  - `start_block_index: number`

                  - `type: "content_block_location"`

                    - `"content_block_location"`

                - `BetaCitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                  - `cited_text: string`

                  - `encrypted_index: string`

                  - `title: string`

                  - `type: "web_search_result_location"`

                    - `"web_search_result_location"`

                  - `url: string`

                - `BetaCitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                  - `cited_text: string`

                  - `end_block_index: number`

                  - `search_result_index: number`

                  - `source: string`

                  - `start_block_index: number`

                  - `title: string`

                  - `type: "search_result_location"`

                    - `"search_result_location"`

            - `BetaImageBlockParam = object { source, type, cache_control }`

              - `source: BetaBase64ImageSource or BetaURLImageSource or BetaFileImageSource`

                - `BetaBase64ImageSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                    - `"image/jpeg"`

                    - `"image/png"`

                    - `"image/gif"`

                    - `"image/webp"`

                  - `type: "base64"`

                    - `"base64"`

                - `BetaURLImageSource = object { type, url }`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

                - `BetaFileImageSource = object { file_id, type }`

                  - `file_id: string`

                  - `type: "file"`

                    - `"file"`

              - `type: "image"`

                - `"image"`

              - `cache_control: optional BetaCacheControlEphemeral`

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

            - `BetaSearchResultBlockParam = object { content, source, title, 3 more }`

              - `content: array of BetaTextBlockParam`

                - `text: string`

                - `type: "text"`

                  - `"text"`

                - `cache_control: optional BetaCacheControlEphemeral`

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

                - `citations: optional array of BetaTextCitationParam`

                  - `BetaCitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string`

                    - `end_char_index: number`

                    - `start_char_index: number`

                    - `type: "char_location"`

                      - `"char_location"`

                  - `BetaCitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string`

                    - `end_page_number: number`

                    - `start_page_number: number`

                    - `type: "page_location"`

                      - `"page_location"`

                  - `BetaCitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                    - `cited_text: string`

                    - `document_index: number`

                    - `document_title: string`

                    - `end_block_index: number`

                    - `start_block_index: number`

                    - `type: "content_block_location"`

                      - `"content_block_location"`

                  - `BetaCitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                    - `cited_text: string`

                    - `encrypted_index: string`

                    - `title: string`

                    - `type: "web_search_result_location"`

                      - `"web_search_result_location"`

                    - `url: string`

                  - `BetaCitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

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

              - `cache_control: optional BetaCacheControlEphemeral`

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

              - `citations: optional BetaCitationsConfigParam`

                - `enabled: optional boolean`

            - `BetaRequestDocumentBlock = object { source, type, cache_control, 3 more }`

              - `source: BetaBase64PDFSource or BetaPlainTextSource or BetaContentBlockSource or 2 more`

                - `BetaBase64PDFSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "application/pdf"`

                    - `"application/pdf"`

                  - `type: "base64"`

                    - `"base64"`

                - `BetaPlainTextSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "text/plain"`

                    - `"text/plain"`

                  - `type: "text"`

                    - `"text"`

                - `BetaContentBlockSource = object { content, type }`

                  - `content: string or array of BetaContentBlockSourceContent`

                    - `UnionMember0 = string`

                    - `BetaContentBlockSourceContent = array of BetaContentBlockSourceContent`

                      - `BetaTextBlockParam = object { text, type, cache_control, citations }`

                        - `text: string`

                        - `type: "text"`

                          - `"text"`

                        - `cache_control: optional BetaCacheControlEphemeral`

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

                        - `citations: optional array of BetaTextCitationParam`

                          - `BetaCitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_char_index: number`

                            - `start_char_index: number`

                            - `type: "char_location"`

                              - `"char_location"`

                          - `BetaCitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_page_number: number`

                            - `start_page_number: number`

                            - `type: "page_location"`

                              - `"page_location"`

                          - `BetaCitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_block_index: number`

                            - `start_block_index: number`

                            - `type: "content_block_location"`

                              - `"content_block_location"`

                          - `BetaCitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                            - `cited_text: string`

                            - `encrypted_index: string`

                            - `title: string`

                            - `type: "web_search_result_location"`

                              - `"web_search_result_location"`

                            - `url: string`

                          - `BetaCitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                            - `cited_text: string`

                            - `end_block_index: number`

                            - `search_result_index: number`

                            - `source: string`

                            - `start_block_index: number`

                            - `title: string`

                            - `type: "search_result_location"`

                              - `"search_result_location"`

                      - `BetaImageBlockParam = object { source, type, cache_control }`

                        - `source: BetaBase64ImageSource or BetaURLImageSource or BetaFileImageSource`

                          - `BetaBase64ImageSource = object { data, media_type, type }`

                            - `data: string`

                            - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                              - `"image/jpeg"`

                              - `"image/png"`

                              - `"image/gif"`

                              - `"image/webp"`

                            - `type: "base64"`

                              - `"base64"`

                          - `BetaURLImageSource = object { type, url }`

                            - `type: "url"`

                              - `"url"`

                            - `url: string`

                          - `BetaFileImageSource = object { file_id, type }`

                            - `file_id: string`

                            - `type: "file"`

                              - `"file"`

                        - `type: "image"`

                          - `"image"`

                        - `cache_control: optional BetaCacheControlEphemeral`

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

                - `BetaURLPDFSource = object { type, url }`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

                - `BetaFileDocumentSource = object { file_id, type }`

                  - `file_id: string`

                  - `type: "file"`

                    - `"file"`

              - `type: "document"`

                - `"document"`

              - `cache_control: optional BetaCacheControlEphemeral`

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

              - `citations: optional BetaCitationsConfigParam`

                - `enabled: optional boolean`

              - `context: optional string`

              - `title: optional string`

            - `BetaToolReferenceBlockParam = object { tool_name, type, cache_control }`

              Tool reference block that can be included in tool_result content.

              - `tool_name: string`

              - `type: "tool_reference"`

                - `"tool_reference"`

              - `cache_control: optional BetaCacheControlEphemeral`

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

        - `is_error: optional boolean`

      - `BetaServerToolUseBlockParam = object { id, input, name, 3 more }`

        - `id: string`

        - `input: map[unknown]`

        - `name: "web_search" or "web_fetch" or "code_execution" or 4 more`

          - `"web_search"`

          - `"web_fetch"`

          - `"code_execution"`

          - `"bash_code_execution"`

          - `"text_editor_code_execution"`

          - `"tool_search_tool_regex"`

          - `"tool_search_tool_bm25"`

        - `type: "server_tool_use"`

          - `"server_tool_use"`

        - `cache_control: optional BetaCacheControlEphemeral`

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

        - `caller: optional BetaDirectCaller or BetaServerToolCaller`

          Tool invocation directly from the model.

          - `BetaDirectCaller = object { type }`

            Tool invocation directly from the model.

            - `type: "direct"`

              - `"direct"`

          - `BetaServerToolCaller = object { tool_id, type }`

            Tool invocation generated by a server-side tool.

            - `tool_id: string`

            - `type: "code_execution_20250825"`

              - `"code_execution_20250825"`

      - `BetaWebSearchToolResultBlockParam = object { content, tool_use_id, type, cache_control }`

        - `content: BetaWebSearchToolResultBlockParamContent`

          - `ResultBlock = array of BetaWebSearchResultBlockParam`

            - `encrypted_content: string`

            - `title: string`

            - `type: "web_search_result"`

              - `"web_search_result"`

            - `url: string`

            - `page_age: optional string`

          - `BetaWebSearchToolRequestError = object { error_code, type }`

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

        - `cache_control: optional BetaCacheControlEphemeral`

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

      - `BetaWebFetchToolResultBlockParam = object { content, tool_use_id, type, cache_control }`

        - `content: BetaWebFetchToolResultErrorBlockParam or BetaWebFetchBlockParam`

          - `BetaWebFetchToolResultErrorBlockParam = object { error_code, type }`

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

          - `BetaWebFetchBlockParam = object { content, type, url, retrieved_at }`

            - `content: BetaRequestDocumentBlock`

              - `source: BetaBase64PDFSource or BetaPlainTextSource or BetaContentBlockSource or 2 more`

                - `BetaBase64PDFSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "application/pdf"`

                    - `"application/pdf"`

                  - `type: "base64"`

                    - `"base64"`

                - `BetaPlainTextSource = object { data, media_type, type }`

                  - `data: string`

                  - `media_type: "text/plain"`

                    - `"text/plain"`

                  - `type: "text"`

                    - `"text"`

                - `BetaContentBlockSource = object { content, type }`

                  - `content: string or array of BetaContentBlockSourceContent`

                    - `UnionMember0 = string`

                    - `BetaContentBlockSourceContent = array of BetaContentBlockSourceContent`

                      - `BetaTextBlockParam = object { text, type, cache_control, citations }`

                        - `text: string`

                        - `type: "text"`

                          - `"text"`

                        - `cache_control: optional BetaCacheControlEphemeral`

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

                        - `citations: optional array of BetaTextCitationParam`

                          - `BetaCitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_char_index: number`

                            - `start_char_index: number`

                            - `type: "char_location"`

                              - `"char_location"`

                          - `BetaCitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_page_number: number`

                            - `start_page_number: number`

                            - `type: "page_location"`

                              - `"page_location"`

                          - `BetaCitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                            - `cited_text: string`

                            - `document_index: number`

                            - `document_title: string`

                            - `end_block_index: number`

                            - `start_block_index: number`

                            - `type: "content_block_location"`

                              - `"content_block_location"`

                          - `BetaCitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                            - `cited_text: string`

                            - `encrypted_index: string`

                            - `title: string`

                            - `type: "web_search_result_location"`

                              - `"web_search_result_location"`

                            - `url: string`

                          - `BetaCitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                            - `cited_text: string`

                            - `end_block_index: number`

                            - `search_result_index: number`

                            - `source: string`

                            - `start_block_index: number`

                            - `title: string`

                            - `type: "search_result_location"`

                              - `"search_result_location"`

                      - `BetaImageBlockParam = object { source, type, cache_control }`

                        - `source: BetaBase64ImageSource or BetaURLImageSource or BetaFileImageSource`

                          - `BetaBase64ImageSource = object { data, media_type, type }`

                            - `data: string`

                            - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

                              - `"image/jpeg"`

                              - `"image/png"`

                              - `"image/gif"`

                              - `"image/webp"`

                            - `type: "base64"`

                              - `"base64"`

                          - `BetaURLImageSource = object { type, url }`

                            - `type: "url"`

                              - `"url"`

                            - `url: string`

                          - `BetaFileImageSource = object { file_id, type }`

                            - `file_id: string`

                            - `type: "file"`

                              - `"file"`

                        - `type: "image"`

                          - `"image"`

                        - `cache_control: optional BetaCacheControlEphemeral`

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

                - `BetaURLPDFSource = object { type, url }`

                  - `type: "url"`

                    - `"url"`

                  - `url: string`

                - `BetaFileDocumentSource = object { file_id, type }`

                  - `file_id: string`

                  - `type: "file"`

                    - `"file"`

              - `type: "document"`

                - `"document"`

              - `cache_control: optional BetaCacheControlEphemeral`

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

              - `citations: optional BetaCitationsConfigParam`

                - `enabled: optional boolean`

              - `context: optional string`

              - `title: optional string`

            - `type: "web_fetch_result"`

              - `"web_fetch_result"`

            - `url: string`

              Fetched content URL

            - `retrieved_at: optional string`

              ISO 8601 timestamp when the content was retrieved

        - `tool_use_id: string`

        - `type: "web_fetch_tool_result"`

          - `"web_fetch_tool_result"`

        - `cache_control: optional BetaCacheControlEphemeral`

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

      - `BetaCodeExecutionToolResultBlockParam = object { content, tool_use_id, type, cache_control }`

        - `content: BetaCodeExecutionToolResultBlockParamContent`

          - `BetaCodeExecutionToolResultErrorParam = object { error_code, type }`

            - `error_code: BetaCodeExecutionToolResultErrorCode`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

            - `type: "code_execution_tool_result_error"`

              - `"code_execution_tool_result_error"`

          - `BetaCodeExecutionResultBlockParam = object { content, return_code, stderr, 2 more }`

            - `content: array of BetaCodeExecutionOutputBlockParam`

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

        - `cache_control: optional BetaCacheControlEphemeral`

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

      - `BetaBashCodeExecutionToolResultBlockParam = object { content, tool_use_id, type, cache_control }`

        - `content: BetaBashCodeExecutionToolResultErrorParam or BetaBashCodeExecutionResultBlockParam`

          - `BetaBashCodeExecutionToolResultErrorParam = object { error_code, type }`

            - `error_code: "invalid_tool_input" or "unavailable" or "too_many_requests" or 2 more`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

              - `"output_file_too_large"`

            - `type: "bash_code_execution_tool_result_error"`

              - `"bash_code_execution_tool_result_error"`

          - `BetaBashCodeExecutionResultBlockParam = object { content, return_code, stderr, 2 more }`

            - `content: array of BetaBashCodeExecutionOutputBlockParam`

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

        - `cache_control: optional BetaCacheControlEphemeral`

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

      - `BetaTextEditorCodeExecutionToolResultBlockParam = object { content, tool_use_id, type, cache_control }`

        - `content: BetaTextEditorCodeExecutionToolResultErrorParam or BetaTextEditorCodeExecutionViewResultBlockParam or BetaTextEditorCodeExecutionCreateResultBlockParam or BetaTextEditorCodeExecutionStrReplaceResultBlockParam`

          - `BetaTextEditorCodeExecutionToolResultErrorParam = object { error_code, type, error_message }`

            - `error_code: "invalid_tool_input" or "unavailable" or "too_many_requests" or 2 more`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

              - `"file_not_found"`

            - `type: "text_editor_code_execution_tool_result_error"`

              - `"text_editor_code_execution_tool_result_error"`

            - `error_message: optional string`

          - `BetaTextEditorCodeExecutionViewResultBlockParam = object { content, file_type, type, 3 more }`

            - `content: string`

            - `file_type: "text" or "image" or "pdf"`

              - `"text"`

              - `"image"`

              - `"pdf"`

            - `type: "text_editor_code_execution_view_result"`

              - `"text_editor_code_execution_view_result"`

            - `num_lines: optional number`

            - `start_line: optional number`

            - `total_lines: optional number`

          - `BetaTextEditorCodeExecutionCreateResultBlockParam = object { is_file_update, type }`

            - `is_file_update: boolean`

            - `type: "text_editor_code_execution_create_result"`

              - `"text_editor_code_execution_create_result"`

          - `BetaTextEditorCodeExecutionStrReplaceResultBlockParam = object { type, lines, new_lines, 3 more }`

            - `type: "text_editor_code_execution_str_replace_result"`

              - `"text_editor_code_execution_str_replace_result"`

            - `lines: optional array of string`

            - `new_lines: optional number`

            - `new_start: optional number`

            - `old_lines: optional number`

            - `old_start: optional number`

        - `tool_use_id: string`

        - `type: "text_editor_code_execution_tool_result"`

          - `"text_editor_code_execution_tool_result"`

        - `cache_control: optional BetaCacheControlEphemeral`

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

      - `BetaToolSearchToolResultBlockParam = object { content, tool_use_id, type, cache_control }`

        - `content: BetaToolSearchToolResultErrorParam or BetaToolSearchToolSearchResultBlockParam`

          - `BetaToolSearchToolResultErrorParam = object { error_code, type }`

            - `error_code: "invalid_tool_input" or "unavailable" or "too_many_requests" or "execution_time_exceeded"`

              - `"invalid_tool_input"`

              - `"unavailable"`

              - `"too_many_requests"`

              - `"execution_time_exceeded"`

            - `type: "tool_search_tool_result_error"`

              - `"tool_search_tool_result_error"`

          - `BetaToolSearchToolSearchResultBlockParam = object { tool_references, type }`

            - `tool_references: array of BetaToolReferenceBlockParam`

              - `tool_name: string`

              - `type: "tool_reference"`

                - `"tool_reference"`

              - `cache_control: optional BetaCacheControlEphemeral`

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

            - `type: "tool_search_tool_search_result"`

              - `"tool_search_tool_search_result"`

        - `tool_use_id: string`

        - `type: "tool_search_tool_result"`

          - `"tool_search_tool_result"`

        - `cache_control: optional BetaCacheControlEphemeral`

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

      - `BetaMCPToolUseBlockParam = object { id, input, name, 3 more }`

        - `id: string`

        - `input: map[unknown]`

        - `name: string`

        - `server_name: string`

          The name of the MCP server

        - `type: "mcp_tool_use"`

          - `"mcp_tool_use"`

        - `cache_control: optional BetaCacheControlEphemeral`

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

      - `BetaRequestMCPToolResultBlockParam = object { tool_use_id, type, cache_control, 2 more }`

        - `tool_use_id: string`

        - `type: "mcp_tool_result"`

          - `"mcp_tool_result"`

        - `cache_control: optional BetaCacheControlEphemeral`

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

        - `content: optional string or array of BetaTextBlockParam`

          - `UnionMember0 = string`

          - `BetaMCPToolResultBlockParamContent = array of BetaTextBlockParam`

            - `text: string`

            - `type: "text"`

              - `"text"`

            - `cache_control: optional BetaCacheControlEphemeral`

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

            - `citations: optional array of BetaTextCitationParam`

              - `BetaCitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_char_index: number`

                - `start_char_index: number`

                - `type: "char_location"`

                  - `"char_location"`

              - `BetaCitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_page_number: number`

                - `start_page_number: number`

                - `type: "page_location"`

                  - `"page_location"`

              - `BetaCitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

                - `cited_text: string`

                - `document_index: number`

                - `document_title: string`

                - `end_block_index: number`

                - `start_block_index: number`

                - `type: "content_block_location"`

                  - `"content_block_location"`

              - `BetaCitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

                - `cited_text: string`

                - `encrypted_index: string`

                - `title: string`

                - `type: "web_search_result_location"`

                  - `"web_search_result_location"`

                - `url: string`

              - `BetaCitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

                - `cited_text: string`

                - `end_block_index: number`

                - `search_result_index: number`

                - `source: string`

                - `start_block_index: number`

                - `title: string`

                - `type: "search_result_location"`

                  - `"search_result_location"`

        - `is_error: optional boolean`

      - `BetaContainerUploadBlockParam = object { file_id, type, cache_control }`

        A content block that represents a file to be uploaded to the container
        Files uploaded via this block will be available in the container's input directory.

        - `file_id: string`

        - `type: "container_upload"`

          - `"container_upload"`

        - `cache_control: optional BetaCacheControlEphemeral`

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

- `container: optional BetaContainerParams or string`

  Container identifier for reuse across requests.

  - `BetaContainerParams = object { id, skills }`

    Container parameters with skills to be loaded.

    - `id: optional string`

      Container id

    - `skills: optional array of BetaSkillParams`

      List of skills to load in the container

      - `skill_id: string`

        Skill ID

      - `type: "anthropic" or "custom"`

        Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

        - `"anthropic"`

        - `"custom"`

      - `version: optional string`

        Skill version or 'latest' for most recent version

  - `UnionMember1 = string`

- `context_management: optional BetaContextManagementConfig`

  Context management configuration.

  This allows you to control how Claude manages context across multiple requests, such as whether to clear function results or not.

  - `edits: optional array of BetaClearToolUses20250919Edit or BetaClearThinking20251015Edit`

    List of context management edits to apply

    - `BetaClearToolUses20250919Edit = object { type, clear_at_least, clear_tool_inputs, 3 more }`

      - `type: "clear_tool_uses_20250919"`

        - `"clear_tool_uses_20250919"`

      - `clear_at_least: optional BetaInputTokensClearAtLeast`

        Minimum number of tokens that must be cleared when triggered. Context will only be modified if at least this many tokens can be removed.

        - `type: "input_tokens"`

          - `"input_tokens"`

        - `value: number`

      - `clear_tool_inputs: optional boolean or array of string`

        Whether to clear all tool inputs (bool) or specific tool inputs to clear (list)

        - `UnionMember0 = boolean`

        - `UnionMember1 = array of string`

      - `exclude_tools: optional array of string`

        Tool names whose uses are preserved from clearing

      - `keep: optional BetaToolUsesKeep`

        Number of tool uses to retain in the conversation

        - `type: "tool_uses"`

          - `"tool_uses"`

        - `value: number`

      - `trigger: optional BetaInputTokensTrigger or BetaToolUsesTrigger`

        Condition that triggers the context management strategy

        - `BetaInputTokensTrigger = object { type, value }`

          - `type: "input_tokens"`

            - `"input_tokens"`

          - `value: number`

        - `BetaToolUsesTrigger = object { type, value }`

          - `type: "tool_uses"`

            - `"tool_uses"`

          - `value: number`

    - `BetaClearThinking20251015Edit = object { type, keep }`

      - `type: "clear_thinking_20251015"`

        - `"clear_thinking_20251015"`

      - `keep: optional BetaThinkingTurns or BetaAllThinkingTurns or "all"`

        Number of most recent assistant turns to keep thinking blocks for. Older turns will have their thinking blocks removed.

        - `BetaThinkingTurns = object { type, value }`

          - `type: "thinking_turns"`

            - `"thinking_turns"`

          - `value: number`

        - `BetaAllThinkingTurns = object { type }`

          - `type: "all"`

            - `"all"`

        - `UnionMember2 = "all"`

          - `"all"`

- `mcp_servers: optional array of BetaRequestMCPServerURLDefinition`

  MCP servers to be utilized in this request

  - `name: string`

  - `type: "url"`

    - `"url"`

  - `url: string`

  - `authorization_token: optional string`

  - `tool_configuration: optional BetaRequestMCPServerToolConfiguration`

    - `allowed_tools: optional array of string`

    - `enabled: optional boolean`

- `metadata: optional BetaMetadata`

  An object describing metadata about the request.

  - `user_id: optional string`

    An external identifier for the user who is associated with the request.

    This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

- `output_config: optional BetaOutputConfig`

  Configuration options for the model's output. Controls aspects like how much effort the model puts into its response.

  - `effort: optional "low" or "medium" or "high"`

    All possible effort levels.

    - `"low"`

    - `"medium"`

    - `"high"`

- `output_format: optional BetaJSONOutputFormat`

  A schema to specify Claude's output format in responses.

  - `schema: map[unknown]`

    The JSON schema of the format

  - `type: "json_schema"`

    - `"json_schema"`

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

- `system: optional string or array of BetaTextBlockParam`

  System prompt.

  A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

  - `UnionMember0 = string`

  - `UnionMember1 = array of BetaTextBlockParam`

    - `text: string`

    - `type: "text"`

      - `"text"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `citations: optional array of BetaTextCitationParam`

      - `BetaCitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_char_index: number`

        - `start_char_index: number`

        - `type: "char_location"`

          - `"char_location"`

      - `BetaCitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_page_number: number`

        - `start_page_number: number`

        - `type: "page_location"`

          - `"page_location"`

      - `BetaCitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

        - `cited_text: string`

        - `document_index: number`

        - `document_title: string`

        - `end_block_index: number`

        - `start_block_index: number`

        - `type: "content_block_location"`

          - `"content_block_location"`

      - `BetaCitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

        - `cited_text: string`

        - `encrypted_index: string`

        - `title: string`

        - `type: "web_search_result_location"`

          - `"web_search_result_location"`

        - `url: string`

      - `BetaCitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

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

- `thinking: optional BetaThinkingConfigParam`

  Configuration for enabling Claude's extended thinking.

  When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

  See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `BetaThinkingConfigEnabled = object { budget_tokens, type }`

    - `budget_tokens: number`

      Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

      Must be ≥1024 and less than `max_tokens`.

      See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

    - `type: "enabled"`

      - `"enabled"`

  - `BetaThinkingConfigDisabled = object { type }`

    - `type: "disabled"`

      - `"disabled"`

- `tool_choice: optional BetaToolChoice`

  How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `BetaToolChoiceAuto = object { type, disable_parallel_tool_use }`

    The model will automatically decide whether to use tools.

    - `type: "auto"`

      - `"auto"`

    - `disable_parallel_tool_use: optional boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output at most one tool use.

  - `BetaToolChoiceAny = object { type, disable_parallel_tool_use }`

    The model will use any available tools.

    - `type: "any"`

      - `"any"`

    - `disable_parallel_tool_use: optional boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output exactly one tool use.

  - `BetaToolChoiceTool = object { name, type, disable_parallel_tool_use }`

    The model will use the specified tool with `tool_choice.name`.

    - `name: string`

      The name of the tool to use.

    - `type: "tool"`

      - `"tool"`

    - `disable_parallel_tool_use: optional boolean`

      Whether to disable parallel tool use.

      Defaults to `false`. If set to `true`, the model will output exactly one tool use.

  - `BetaToolChoiceNone = object { type }`

    The model will not be allowed to use tools.

    - `type: "none"`

      - `"none"`

- `tools: optional array of BetaToolUnion`

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

  - `BetaTool = object { input_schema, name, allowed_callers, 6 more }`

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

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `description: optional string`

      Description of what this tool does.

      Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

    - `input_examples: optional array of map[unknown]`

    - `strict: optional boolean`

    - `type: optional "custom"`

      - `"custom"`

  - `BetaToolBash20241022 = object { name, type, allowed_callers, 4 more }`

    - `name: "bash"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"bash"`

    - `type: "bash_20241022"`

      - `"bash_20241022"`

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples: optional array of map[unknown]`

    - `strict: optional boolean`

  - `BetaToolBash20250124 = object { name, type, allowed_callers, 4 more }`

    - `name: "bash"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"bash"`

    - `type: "bash_20250124"`

      - `"bash_20250124"`

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples: optional array of map[unknown]`

    - `strict: optional boolean`

  - `BetaCodeExecutionTool20250522 = object { name, type, allowed_callers, 3 more }`

    - `name: "code_execution"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"code_execution"`

    - `type: "code_execution_20250522"`

      - `"code_execution_20250522"`

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `strict: optional boolean`

  - `BetaCodeExecutionTool20250825 = object { name, type, allowed_callers, 3 more }`

    - `name: "code_execution"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"code_execution"`

    - `type: "code_execution_20250825"`

      - `"code_execution_20250825"`

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `strict: optional boolean`

  - `BetaToolComputerUse20241022 = object { display_height_px, display_width_px, name, 7 more }`

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

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `display_number: optional number`

      The X11 display number (e.g. 0, 1) for the display.

    - `input_examples: optional array of map[unknown]`

    - `strict: optional boolean`

  - `BetaMemoryTool20250818 = object { name, type, allowed_callers, 4 more }`

    - `name: "memory"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"memory"`

    - `type: "memory_20250818"`

      - `"memory_20250818"`

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples: optional array of map[unknown]`

    - `strict: optional boolean`

  - `BetaToolComputerUse20250124 = object { display_height_px, display_width_px, name, 7 more }`

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

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `display_number: optional number`

      The X11 display number (e.g. 0, 1) for the display.

    - `input_examples: optional array of map[unknown]`

    - `strict: optional boolean`

  - `BetaToolTextEditor20241022 = object { name, type, allowed_callers, 4 more }`

    - `name: "str_replace_editor"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_editor"`

    - `type: "text_editor_20241022"`

      - `"text_editor_20241022"`

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples: optional array of map[unknown]`

    - `strict: optional boolean`

  - `BetaToolComputerUse20251124 = object { display_height_px, display_width_px, name, 8 more }`

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

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `display_number: optional number`

      The X11 display number (e.g. 0, 1) for the display.

    - `enable_zoom: optional boolean`

      Whether to enable an action to take a zoomed-in screenshot of the screen.

    - `input_examples: optional array of map[unknown]`

    - `strict: optional boolean`

  - `BetaToolTextEditor20250124 = object { name, type, allowed_callers, 4 more }`

    - `name: "str_replace_editor"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_editor"`

    - `type: "text_editor_20250124"`

      - `"text_editor_20250124"`

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples: optional array of map[unknown]`

    - `strict: optional boolean`

  - `BetaToolTextEditor20250429 = object { name, type, allowed_callers, 4 more }`

    - `name: "str_replace_based_edit_tool"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_based_edit_tool"`

    - `type: "text_editor_20250429"`

      - `"text_editor_20250429"`

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples: optional array of map[unknown]`

    - `strict: optional boolean`

  - `BetaToolTextEditor20250728 = object { name, type, allowed_callers, 5 more }`

    - `name: "str_replace_based_edit_tool"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"str_replace_based_edit_tool"`

    - `type: "text_editor_20250728"`

      - `"text_editor_20250728"`

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `input_examples: optional array of map[unknown]`

    - `max_characters: optional number`

      Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

    - `strict: optional boolean`

  - `BetaWebSearchTool20250305 = object { name, type, allowed_callers, 7 more }`

    - `name: "web_search"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"web_search"`

    - `type: "web_search_20250305"`

      - `"web_search_20250305"`

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `allowed_domains: optional array of string`

      If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

    - `blocked_domains: optional array of string`

      If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `max_uses: optional number`

      Maximum number of times the tool can be used in the API request.

    - `strict: optional boolean`

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

  - `BetaWebFetchTool20250910 = object { name, type, allowed_callers, 8 more }`

    - `name: "web_fetch"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"web_fetch"`

    - `type: "web_fetch_20250910"`

      - `"web_fetch_20250910"`

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `allowed_domains: optional array of string`

      List of domains to allow fetching from

    - `blocked_domains: optional array of string`

      List of domains to block fetching from

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `citations: optional BetaCitationsConfigParam`

      Citations configuration for fetched documents. Citations are disabled by default.

      - `enabled: optional boolean`

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `max_content_tokens: optional number`

      Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

    - `max_uses: optional number`

      Maximum number of times the tool can be used in the API request.

    - `strict: optional boolean`

  - `BetaToolSearchToolBm25_20251119 = object { name, type, allowed_callers, 3 more }`

    - `name: "tool_search_tool_bm25"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"tool_search_tool_bm25"`

    - `type: "tool_search_tool_bm25_20251119" or "tool_search_tool_bm25"`

      - `"tool_search_tool_bm25_20251119"`

      - `"tool_search_tool_bm25"`

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `strict: optional boolean`

  - `BetaToolSearchToolRegex20251119 = object { name, type, allowed_callers, 3 more }`

    - `name: "tool_search_tool_regex"`

      Name of the tool.

      This is how the tool will be called by the model and in `tool_use` blocks.

      - `"tool_search_tool_regex"`

    - `type: "tool_search_tool_regex_20251119" or "tool_search_tool_regex"`

      - `"tool_search_tool_regex_20251119"`

      - `"tool_search_tool_regex"`

    - `allowed_callers: optional array of "direct" or "code_execution_20250825"`

      - `"direct"`

      - `"code_execution_20250825"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `defer_loading: optional boolean`

      If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

    - `strict: optional boolean`

  - `BetaMCPToolset = object { mcp_server_name, type, cache_control, 2 more }`

    Configuration for a group of tools from an MCP server.

    Allows configuring enabled status and defer_loading for all tools
    from an MCP server, with optional per-tool overrides.

    - `mcp_server_name: string`

      Name of the MCP server to configure tools for

    - `type: "mcp_toolset"`

      - `"mcp_toolset"`

    - `cache_control: optional BetaCacheControlEphemeral`

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

    - `configs: optional map[BetaMCPToolConfig]`

      Configuration overrides for specific tools, keyed by tool name

      - `defer_loading: optional boolean`

      - `enabled: optional boolean`

    - `default_config: optional BetaMCPToolDefaultConfig`

      Default configuration applied to all tools from this server

      - `defer_loading: optional boolean`

      - `enabled: optional boolean`

- `top_k: optional number`

  Only sample from the top K options for each subsequent token.

  Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

  Recommended for advanced use cases only. You usually only need to use `temperature`.

- `top_p: optional number`

  Use nucleus sampling.

  In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

  Recommended for advanced use cases only. You usually only need to use `temperature`.

### Returns

- `BetaMessage = object { id, container, content, 7 more }`

  - `id: string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `container: BetaContainer`

    Information about the container used in the request (for the code execution tool)

    - `id: string`

      Identifier for the container used in this request

    - `expires_at: string`

      The time at which the container will expire.

    - `skills: array of BetaSkill`

      Skills loaded in the container

      - `skill_id: string`

        Skill ID

      - `type: "anthropic" or "custom"`

        Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

        - `"anthropic"`

        - `"custom"`

      - `version: string`

        Skill version or 'latest' for most recent version

  - `content: array of BetaContentBlock`

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

    - `BetaTextBlock = object { citations, text, type }`

      - `citations: array of BetaTextCitation`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `BetaCitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_char_index: number`

          - `file_id: string`

          - `start_char_index: number`

          - `type: "char_location"`

            - `"char_location"`

        - `BetaCitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_page_number: number`

          - `file_id: string`

          - `start_page_number: number`

          - `type: "page_location"`

            - `"page_location"`

        - `BetaCitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

          - `cited_text: string`

          - `document_index: number`

          - `document_title: string`

          - `end_block_index: number`

          - `file_id: string`

          - `start_block_index: number`

          - `type: "content_block_location"`

            - `"content_block_location"`

        - `BetaCitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

          - `cited_text: string`

          - `encrypted_index: string`

          - `title: string`

          - `type: "web_search_result_location"`

            - `"web_search_result_location"`

          - `url: string`

        - `BetaCitationSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

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

    - `BetaThinkingBlock = object { signature, thinking, type }`

      - `signature: string`

      - `thinking: string`

      - `type: "thinking"`

        - `"thinking"`

    - `BetaRedactedThinkingBlock = object { data, type }`

      - `data: string`

      - `type: "redacted_thinking"`

        - `"redacted_thinking"`

    - `BetaToolUseBlock = object { id, input, name, 2 more }`

      - `id: string`

      - `input: map[unknown]`

      - `name: string`

      - `type: "tool_use"`

        - `"tool_use"`

      - `caller: optional BetaDirectCaller or BetaServerToolCaller`

        Tool invocation directly from the model.

        - `BetaDirectCaller = object { type }`

          Tool invocation directly from the model.

          - `type: "direct"`

            - `"direct"`

        - `BetaServerToolCaller = object { tool_id, type }`

          Tool invocation generated by a server-side tool.

          - `tool_id: string`

          - `type: "code_execution_20250825"`

            - `"code_execution_20250825"`

    - `BetaServerToolUseBlock = object { id, caller, input, 2 more }`

      - `id: string`

      - `caller: BetaDirectCaller or BetaServerToolCaller`

        Tool invocation directly from the model.

        - `BetaDirectCaller = object { type }`

          Tool invocation directly from the model.

          - `type: "direct"`

            - `"direct"`

        - `BetaServerToolCaller = object { tool_id, type }`

          Tool invocation generated by a server-side tool.

          - `tool_id: string`

          - `type: "code_execution_20250825"`

            - `"code_execution_20250825"`

      - `input: map[unknown]`

      - `name: "web_search" or "web_fetch" or "code_execution" or 4 more`

        - `"web_search"`

        - `"web_fetch"`

        - `"code_execution"`

        - `"bash_code_execution"`

        - `"text_editor_code_execution"`

        - `"tool_search_tool_regex"`

        - `"tool_search_tool_bm25"`

      - `type: "server_tool_use"`

        - `"server_tool_use"`

    - `BetaWebSearchToolResultBlock = object { content, tool_use_id, type }`

      - `content: BetaWebSearchToolResultBlockContent`

        - `BetaWebSearchToolResultError = object { error_code, type }`

          - `error_code: BetaWebSearchToolResultErrorCode`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"max_uses_exceeded"`

            - `"too_many_requests"`

            - `"query_too_long"`

          - `type: "web_search_tool_result_error"`

            - `"web_search_tool_result_error"`

        - `UnionMember1 = array of BetaWebSearchResultBlock`

          - `encrypted_content: string`

          - `page_age: string`

          - `title: string`

          - `type: "web_search_result"`

            - `"web_search_result"`

          - `url: string`

      - `tool_use_id: string`

      - `type: "web_search_tool_result"`

        - `"web_search_tool_result"`

    - `BetaWebFetchToolResultBlock = object { content, tool_use_id, type }`

      - `content: BetaWebFetchToolResultErrorBlock or BetaWebFetchBlock`

        - `BetaWebFetchToolResultErrorBlock = object { error_code, type }`

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

        - `BetaWebFetchBlock = object { content, retrieved_at, type, url }`

          - `content: BetaDocumentBlock`

            - `citations: BetaCitationConfig`

              Citation configuration for the document

              - `enabled: boolean`

            - `source: BetaBase64PDFSource or BetaPlainTextSource`

              - `BetaBase64PDFSource = object { data, media_type, type }`

                - `data: string`

                - `media_type: "application/pdf"`

                  - `"application/pdf"`

                - `type: "base64"`

                  - `"base64"`

              - `BetaPlainTextSource = object { data, media_type, type }`

                - `data: string`

                - `media_type: "text/plain"`

                  - `"text/plain"`

                - `type: "text"`

                  - `"text"`

            - `title: string`

              The title of the document

            - `type: "document"`

              - `"document"`

          - `retrieved_at: string`

            ISO 8601 timestamp when the content was retrieved

          - `type: "web_fetch_result"`

            - `"web_fetch_result"`

          - `url: string`

            Fetched content URL

      - `tool_use_id: string`

      - `type: "web_fetch_tool_result"`

        - `"web_fetch_tool_result"`

    - `BetaCodeExecutionToolResultBlock = object { content, tool_use_id, type }`

      - `content: BetaCodeExecutionToolResultBlockContent`

        - `BetaCodeExecutionToolResultError = object { error_code, type }`

          - `error_code: BetaCodeExecutionToolResultErrorCode`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

          - `type: "code_execution_tool_result_error"`

            - `"code_execution_tool_result_error"`

        - `BetaCodeExecutionResultBlock = object { content, return_code, stderr, 2 more }`

          - `content: array of BetaCodeExecutionOutputBlock`

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

    - `BetaBashCodeExecutionToolResultBlock = object { content, tool_use_id, type }`

      - `content: BetaBashCodeExecutionToolResultError or BetaBashCodeExecutionResultBlock`

        - `BetaBashCodeExecutionToolResultError = object { error_code, type }`

          - `error_code: "invalid_tool_input" or "unavailable" or "too_many_requests" or 2 more`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

            - `"output_file_too_large"`

          - `type: "bash_code_execution_tool_result_error"`

            - `"bash_code_execution_tool_result_error"`

        - `BetaBashCodeExecutionResultBlock = object { content, return_code, stderr, 2 more }`

          - `content: array of BetaBashCodeExecutionOutputBlock`

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

    - `BetaTextEditorCodeExecutionToolResultBlock = object { content, tool_use_id, type }`

      - `content: BetaTextEditorCodeExecutionToolResultError or BetaTextEditorCodeExecutionViewResultBlock or BetaTextEditorCodeExecutionCreateResultBlock or BetaTextEditorCodeExecutionStrReplaceResultBlock`

        - `BetaTextEditorCodeExecutionToolResultError = object { error_code, error_message, type }`

          - `error_code: "invalid_tool_input" or "unavailable" or "too_many_requests" or 2 more`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

            - `"file_not_found"`

          - `error_message: string`

          - `type: "text_editor_code_execution_tool_result_error"`

            - `"text_editor_code_execution_tool_result_error"`

        - `BetaTextEditorCodeExecutionViewResultBlock = object { content, file_type, num_lines, 3 more }`

          - `content: string`

          - `file_type: "text" or "image" or "pdf"`

            - `"text"`

            - `"image"`

            - `"pdf"`

          - `num_lines: number`

          - `start_line: number`

          - `total_lines: number`

          - `type: "text_editor_code_execution_view_result"`

            - `"text_editor_code_execution_view_result"`

        - `BetaTextEditorCodeExecutionCreateResultBlock = object { is_file_update, type }`

          - `is_file_update: boolean`

          - `type: "text_editor_code_execution_create_result"`

            - `"text_editor_code_execution_create_result"`

        - `BetaTextEditorCodeExecutionStrReplaceResultBlock = object { lines, new_lines, new_start, 3 more }`

          - `lines: array of string`

          - `new_lines: number`

          - `new_start: number`

          - `old_lines: number`

          - `old_start: number`

          - `type: "text_editor_code_execution_str_replace_result"`

            - `"text_editor_code_execution_str_replace_result"`

      - `tool_use_id: string`

      - `type: "text_editor_code_execution_tool_result"`

        - `"text_editor_code_execution_tool_result"`

    - `BetaToolSearchToolResultBlock = object { content, tool_use_id, type }`

      - `content: BetaToolSearchToolResultError or BetaToolSearchToolSearchResultBlock`

        - `BetaToolSearchToolResultError = object { error_code, error_message, type }`

          - `error_code: "invalid_tool_input" or "unavailable" or "too_many_requests" or "execution_time_exceeded"`

            - `"invalid_tool_input"`

            - `"unavailable"`

            - `"too_many_requests"`

            - `"execution_time_exceeded"`

          - `error_message: string`

          - `type: "tool_search_tool_result_error"`

            - `"tool_search_tool_result_error"`

        - `BetaToolSearchToolSearchResultBlock = object { tool_references, type }`

          - `tool_references: array of BetaToolReferenceBlock`

            - `tool_name: string`

            - `type: "tool_reference"`

              - `"tool_reference"`

          - `type: "tool_search_tool_search_result"`

            - `"tool_search_tool_search_result"`

      - `tool_use_id: string`

      - `type: "tool_search_tool_result"`

        - `"tool_search_tool_result"`

    - `BetaMCPToolUseBlock = object { id, input, name, 2 more }`

      - `id: string`

      - `input: map[unknown]`

      - `name: string`

        The name of the MCP tool

      - `server_name: string`

        The name of the MCP server

      - `type: "mcp_tool_use"`

        - `"mcp_tool_use"`

    - `BetaMCPToolResultBlock = object { content, is_error, tool_use_id, type }`

      - `content: string or array of BetaTextBlock`

        - `UnionMember0 = string`

        - `BetaMCPToolResultBlockContent = array of BetaTextBlock`

          - `citations: array of BetaTextCitation`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `BetaCitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_char_index: number`

              - `file_id: string`

              - `start_char_index: number`

              - `type: "char_location"`

                - `"char_location"`

            - `BetaCitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_page_number: number`

              - `file_id: string`

              - `start_page_number: number`

              - `type: "page_location"`

                - `"page_location"`

            - `BetaCitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

              - `cited_text: string`

              - `document_index: number`

              - `document_title: string`

              - `end_block_index: number`

              - `file_id: string`

              - `start_block_index: number`

              - `type: "content_block_location"`

                - `"content_block_location"`

            - `BetaCitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

              - `cited_text: string`

              - `encrypted_index: string`

              - `title: string`

              - `type: "web_search_result_location"`

                - `"web_search_result_location"`

              - `url: string`

            - `BetaCitationSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

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

      - `is_error: boolean`

      - `tool_use_id: string`

      - `type: "mcp_tool_result"`

        - `"mcp_tool_result"`

    - `BetaContainerUploadBlock = object { file_id, type }`

      Response model for a file uploaded to the container.

      - `file_id: string`

      - `type: "container_upload"`

        - `"container_upload"`

  - `context_management: BetaContextManagementResponse`

    Context management response.

    Information about context management strategies applied during the request.

    - `applied_edits: array of BetaClearToolUses20250919EditResponse or BetaClearThinking20251015EditResponse`

      List of context management edits that were applied.

      - `BetaClearToolUses20250919EditResponse = object { cleared_input_tokens, cleared_tool_uses, type }`

        - `cleared_input_tokens: number`

          Number of input tokens cleared by this edit.

        - `cleared_tool_uses: number`

          Number of tool uses that were cleared.

        - `type: "clear_tool_uses_20250919"`

          The type of context management edit applied.

          - `"clear_tool_uses_20250919"`

      - `BetaClearThinking20251015EditResponse = object { cleared_input_tokens, cleared_thinking_turns, type }`

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

    - `"end_turn"`

    - `"max_tokens"`

    - `"stop_sequence"`

    - `"tool_use"`

    - `"pause_turn"`

    - `"refusal"`

    - `"model_context_window_exceeded"`

  - `stop_sequence: string`

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

    - `cache_creation: BetaCacheCreation`

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

    - `server_tool_use: BetaServerToolUsage`

      The number of server tool requests.

      - `web_fetch_requests: number`

        The number of web fetch tool requests.

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
