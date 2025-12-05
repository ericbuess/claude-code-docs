# Messages

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

## Count Tokens

**post** `/v1/messages/count_tokens`

Count the number of tokens in a Message.

The Token Count API can be used to count the number of tokens in a Message, including tools, images, and documents, without creating it.

Learn more about token counting in our [user guide](https://docs.claude.com/en/docs/build-with-claude/token-counting)

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

- `tools: optional array of BetaTool or BetaToolBash20241022 or BetaToolBash20250124 or 15 more`

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

### Returns

- `BetaMessageTokensCount = object { context_management, input_tokens }`

  - `context_management: BetaCountTokensContextManagementResponse`

    Information about context management applied to the message.

    - `original_input_tokens: number`

      The original token count before context management was applied

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

### Beta All Thinking Turns

- `BetaAllThinkingTurns = object { type }`

  - `type: "all"`

    - `"all"`

### Beta Base64 Image Source

- `BetaBase64ImageSource = object { data, media_type, type }`

  - `data: string`

  - `media_type: "image/jpeg" or "image/png" or "image/gif" or "image/webp"`

    - `"image/jpeg"`

    - `"image/png"`

    - `"image/gif"`

    - `"image/webp"`

  - `type: "base64"`

    - `"base64"`

### Beta Base64 PDF Source

- `BetaBase64PDFSource = object { data, media_type, type }`

  - `data: string`

  - `media_type: "application/pdf"`

    - `"application/pdf"`

  - `type: "base64"`

    - `"base64"`

### Beta Bash Code Execution Output Block

- `BetaBashCodeExecutionOutputBlock = object { file_id, type }`

  - `file_id: string`

  - `type: "bash_code_execution_output"`

    - `"bash_code_execution_output"`

### Beta Bash Code Execution Output Block Param

- `BetaBashCodeExecutionOutputBlockParam = object { file_id, type }`

  - `file_id: string`

  - `type: "bash_code_execution_output"`

    - `"bash_code_execution_output"`

### Beta Bash Code Execution Result Block

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

### Beta Bash Code Execution Result Block Param

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

### Beta Bash Code Execution Tool Result Block

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

### Beta Bash Code Execution Tool Result Block Param

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

### Beta Bash Code Execution Tool Result Error

- `BetaBashCodeExecutionToolResultError = object { error_code, type }`

  - `error_code: "invalid_tool_input" or "unavailable" or "too_many_requests" or 2 more`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

    - `"output_file_too_large"`

  - `type: "bash_code_execution_tool_result_error"`

    - `"bash_code_execution_tool_result_error"`

### Beta Bash Code Execution Tool Result Error Param

- `BetaBashCodeExecutionToolResultErrorParam = object { error_code, type }`

  - `error_code: "invalid_tool_input" or "unavailable" or "too_many_requests" or 2 more`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

    - `"output_file_too_large"`

  - `type: "bash_code_execution_tool_result_error"`

    - `"bash_code_execution_tool_result_error"`

### Beta Cache Control Ephemeral

- `BetaCacheControlEphemeral = object { type, ttl }`

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

### Beta Cache Creation

- `BetaCacheCreation = object { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens }`

  - `ephemeral_1h_input_tokens: number`

    The number of input tokens used to create the 1 hour cache entry.

  - `ephemeral_5m_input_tokens: number`

    The number of input tokens used to create the 5 minute cache entry.

### Beta Citation Char Location

- `BetaCitationCharLocation = object { cited_text, document_index, document_title, 4 more }`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string`

  - `end_char_index: number`

  - `file_id: string`

  - `start_char_index: number`

  - `type: "char_location"`

    - `"char_location"`

### Beta Citation Char Location Param

- `BetaCitationCharLocationParam = object { cited_text, document_index, document_title, 3 more }`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string`

  - `end_char_index: number`

  - `start_char_index: number`

  - `type: "char_location"`

    - `"char_location"`

### Beta Citation Config

- `BetaCitationConfig = object { enabled }`

  - `enabled: boolean`

### Beta Citation Content Block Location

- `BetaCitationContentBlockLocation = object { cited_text, document_index, document_title, 4 more }`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string`

  - `end_block_index: number`

  - `file_id: string`

  - `start_block_index: number`

  - `type: "content_block_location"`

    - `"content_block_location"`

### Beta Citation Content Block Location Param

- `BetaCitationContentBlockLocationParam = object { cited_text, document_index, document_title, 3 more }`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string`

  - `end_block_index: number`

  - `start_block_index: number`

  - `type: "content_block_location"`

    - `"content_block_location"`

### Beta Citation Page Location

- `BetaCitationPageLocation = object { cited_text, document_index, document_title, 4 more }`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string`

  - `end_page_number: number`

  - `file_id: string`

  - `start_page_number: number`

  - `type: "page_location"`

    - `"page_location"`

### Beta Citation Page Location Param

- `BetaCitationPageLocationParam = object { cited_text, document_index, document_title, 3 more }`

  - `cited_text: string`

  - `document_index: number`

  - `document_title: string`

  - `end_page_number: number`

  - `start_page_number: number`

  - `type: "page_location"`

    - `"page_location"`

### Beta Citation Search Result Location

- `BetaCitationSearchResultLocation = object { cited_text, end_block_index, search_result_index, 4 more }`

  - `cited_text: string`

  - `end_block_index: number`

  - `search_result_index: number`

  - `source: string`

  - `start_block_index: number`

  - `title: string`

  - `type: "search_result_location"`

    - `"search_result_location"`

### Beta Citation Search Result Location Param

- `BetaCitationSearchResultLocationParam = object { cited_text, end_block_index, search_result_index, 4 more }`

  - `cited_text: string`

  - `end_block_index: number`

  - `search_result_index: number`

  - `source: string`

  - `start_block_index: number`

  - `title: string`

  - `type: "search_result_location"`

    - `"search_result_location"`

### Beta Citation Web Search Result Location Param

- `BetaCitationWebSearchResultLocationParam = object { cited_text, encrypted_index, title, 2 more }`

  - `cited_text: string`

  - `encrypted_index: string`

  - `title: string`

  - `type: "web_search_result_location"`

    - `"web_search_result_location"`

  - `url: string`

### Beta Citations Config Param

- `BetaCitationsConfigParam = object { enabled }`

  - `enabled: optional boolean`

### Beta Citations Delta

- `BetaCitationsDelta = object { citation, type }`

  - `citation: BetaCitationCharLocation or BetaCitationPageLocation or BetaCitationContentBlockLocation or 2 more`

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

  - `type: "citations_delta"`

    - `"citations_delta"`

### Beta Citations Web Search Result Location

- `BetaCitationsWebSearchResultLocation = object { cited_text, encrypted_index, title, 2 more }`

  - `cited_text: string`

  - `encrypted_index: string`

  - `title: string`

  - `type: "web_search_result_location"`

    - `"web_search_result_location"`

  - `url: string`

### Beta Clear Thinking 20251015 Edit

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

### Beta Clear Thinking 20251015 Edit Response

- `BetaClearThinking20251015EditResponse = object { cleared_input_tokens, cleared_thinking_turns, type }`

  - `cleared_input_tokens: number`

    Number of input tokens cleared by this edit.

  - `cleared_thinking_turns: number`

    Number of thinking turns that were cleared.

  - `type: "clear_thinking_20251015"`

    The type of context management edit applied.

    - `"clear_thinking_20251015"`

### Beta Clear Tool Uses 20250919 Edit

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

### Beta Clear Tool Uses 20250919 Edit Response

- `BetaClearToolUses20250919EditResponse = object { cleared_input_tokens, cleared_tool_uses, type }`

  - `cleared_input_tokens: number`

    Number of input tokens cleared by this edit.

  - `cleared_tool_uses: number`

    Number of tool uses that were cleared.

  - `type: "clear_tool_uses_20250919"`

    The type of context management edit applied.

    - `"clear_tool_uses_20250919"`

### Beta Code Execution Output Block

- `BetaCodeExecutionOutputBlock = object { file_id, type }`

  - `file_id: string`

  - `type: "code_execution_output"`

    - `"code_execution_output"`

### Beta Code Execution Output Block Param

- `BetaCodeExecutionOutputBlockParam = object { file_id, type }`

  - `file_id: string`

  - `type: "code_execution_output"`

    - `"code_execution_output"`

### Beta Code Execution Result Block

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

### Beta Code Execution Result Block Param

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

### Beta Code Execution Tool 20250522

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

### Beta Code Execution Tool 20250825

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

### Beta Code Execution Tool Result Block

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

### Beta Code Execution Tool Result Block Content

- `BetaCodeExecutionToolResultBlockContent = BetaCodeExecutionToolResultError or BetaCodeExecutionResultBlock`

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

### Beta Code Execution Tool Result Block Param

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

### Beta Code Execution Tool Result Block Param Content

- `BetaCodeExecutionToolResultBlockParamContent = BetaCodeExecutionToolResultErrorParam or BetaCodeExecutionResultBlockParam`

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

### Beta Code Execution Tool Result Error

- `BetaCodeExecutionToolResultError = object { error_code, type }`

  - `error_code: BetaCodeExecutionToolResultErrorCode`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

  - `type: "code_execution_tool_result_error"`

    - `"code_execution_tool_result_error"`

### Beta Code Execution Tool Result Error Code

- `BetaCodeExecutionToolResultErrorCode = "invalid_tool_input" or "unavailable" or "too_many_requests" or "execution_time_exceeded"`

  - `"invalid_tool_input"`

  - `"unavailable"`

  - `"too_many_requests"`

  - `"execution_time_exceeded"`

### Beta Code Execution Tool Result Error Param

- `BetaCodeExecutionToolResultErrorParam = object { error_code, type }`

  - `error_code: BetaCodeExecutionToolResultErrorCode`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

  - `type: "code_execution_tool_result_error"`

    - `"code_execution_tool_result_error"`

### Beta Container

- `BetaContainer = object { id, expires_at, skills }`

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

### Beta Container Params

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

### Beta Container Upload Block

- `BetaContainerUploadBlock = object { file_id, type }`

  Response model for a file uploaded to the container.

  - `file_id: string`

  - `type: "container_upload"`

    - `"container_upload"`

### Beta Container Upload Block Param

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

### Beta Content Block

- `BetaContentBlock = BetaTextBlock or BetaThinkingBlock or BetaRedactedThinkingBlock or 11 more`

  Response model for a file uploaded to the container.

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

### Beta Content Block Param

- `BetaContentBlockParam = BetaTextBlockParam or BetaImageBlockParam or BetaRequestDocumentBlock or 15 more`

  Regular text content.

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

### Beta Content Block Source

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

### Beta Content Block Source Content

- `BetaContentBlockSourceContent = BetaTextBlockParam or BetaImageBlockParam`

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

### Beta Context Management Config

- `BetaContextManagementConfig = object { edits }`

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

### Beta Context Management Response

- `BetaContextManagementResponse = object { applied_edits }`

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

### Beta Count Tokens Context Management Response

- `BetaCountTokensContextManagementResponse = object { original_input_tokens }`

  - `original_input_tokens: number`

    The original token count before context management was applied

### Beta Direct Caller

- `BetaDirectCaller = object { type }`

  Tool invocation directly from the model.

  - `type: "direct"`

    - `"direct"`

### Beta Document Block

- `BetaDocumentBlock = object { citations, source, title, type }`

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

### Beta File Document Source

- `BetaFileDocumentSource = object { file_id, type }`

  - `file_id: string`

  - `type: "file"`

    - `"file"`

### Beta File Image Source

- `BetaFileImageSource = object { file_id, type }`

  - `file_id: string`

  - `type: "file"`

    - `"file"`

### Beta Image Block Param

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

### Beta Input JSON Delta

- `BetaInputJSONDelta = object { partial_json, type }`

  - `partial_json: string`

  - `type: "input_json_delta"`

    - `"input_json_delta"`

### Beta Input Tokens Clear At Least

- `BetaInputTokensClearAtLeast = object { type, value }`

  - `type: "input_tokens"`

    - `"input_tokens"`

  - `value: number`

### Beta Input Tokens Trigger

- `BetaInputTokensTrigger = object { type, value }`

  - `type: "input_tokens"`

    - `"input_tokens"`

  - `value: number`

### Beta JSON Output Format

- `BetaJSONOutputFormat = object { schema, type }`

  - `schema: map[unknown]`

    The JSON schema of the format

  - `type: "json_schema"`

    - `"json_schema"`

### Beta MCP Tool Config

- `BetaMCPToolConfig = object { defer_loading, enabled }`

  Configuration for a specific tool in an MCP toolset.

  - `defer_loading: optional boolean`

  - `enabled: optional boolean`

### Beta MCP Tool Default Config

- `BetaMCPToolDefaultConfig = object { defer_loading, enabled }`

  Default configuration for tools in an MCP toolset.

  - `defer_loading: optional boolean`

  - `enabled: optional boolean`

### Beta MCP Tool Result Block

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

### Beta MCP Tool Use Block

- `BetaMCPToolUseBlock = object { id, input, name, 2 more }`

  - `id: string`

  - `input: map[unknown]`

  - `name: string`

    The name of the MCP tool

  - `server_name: string`

    The name of the MCP server

  - `type: "mcp_tool_use"`

    - `"mcp_tool_use"`

### Beta MCP Tool Use Block Param

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

### Beta MCP Toolset

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

### Beta Memory Tool 20250818

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

### Beta Memory Tool 20250818 Command

- `BetaMemoryTool20250818Command = BetaMemoryTool20250818ViewCommand or BetaMemoryTool20250818CreateCommand or BetaMemoryTool20250818StrReplaceCommand or 3 more`

  - `BetaMemoryTool20250818ViewCommand = object { command, path, view_range }`

    - `command: "view"`

      Command type identifier

      - `"view"`

    - `path: string`

      Path to directory or file to view

    - `view_range: optional array of number`

      Optional line range for viewing specific lines

  - `BetaMemoryTool20250818CreateCommand = object { command, file_text, path }`

    - `command: "create"`

      Command type identifier

      - `"create"`

    - `file_text: string`

      Content to write to the file

    - `path: string`

      Path where the file should be created

  - `BetaMemoryTool20250818StrReplaceCommand = object { command, new_str, old_str, path }`

    - `command: "str_replace"`

      Command type identifier

      - `"str_replace"`

    - `new_str: string`

      Text to replace with

    - `old_str: string`

      Text to search for and replace

    - `path: string`

      Path to the file where text should be replaced

  - `BetaMemoryTool20250818InsertCommand = object { command, insert_line, insert_text, path }`

    - `command: "insert"`

      Command type identifier

      - `"insert"`

    - `insert_line: number`

      Line number where text should be inserted

    - `insert_text: string`

      Text to insert at the specified line

    - `path: string`

      Path to the file where text should be inserted

  - `BetaMemoryTool20250818DeleteCommand = object { command, path }`

    - `command: "delete"`

      Command type identifier

      - `"delete"`

    - `path: string`

      Path to the file or directory to delete

  - `BetaMemoryTool20250818RenameCommand = object { command, new_path, old_path }`

    - `command: "rename"`

      Command type identifier

      - `"rename"`

    - `new_path: string`

      New path for the file or directory

    - `old_path: string`

      Current path of the file or directory

### Beta Memory Tool 20250818 Create Command

- `BetaMemoryTool20250818CreateCommand = object { command, file_text, path }`

  - `command: "create"`

    Command type identifier

    - `"create"`

  - `file_text: string`

    Content to write to the file

  - `path: string`

    Path where the file should be created

### Beta Memory Tool 20250818 Delete Command

- `BetaMemoryTool20250818DeleteCommand = object { command, path }`

  - `command: "delete"`

    Command type identifier

    - `"delete"`

  - `path: string`

    Path to the file or directory to delete

### Beta Memory Tool 20250818 Insert Command

- `BetaMemoryTool20250818InsertCommand = object { command, insert_line, insert_text, path }`

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

- `BetaMemoryTool20250818RenameCommand = object { command, new_path, old_path }`

  - `command: "rename"`

    Command type identifier

    - `"rename"`

  - `new_path: string`

    New path for the file or directory

  - `old_path: string`

    Current path of the file or directory

### Beta Memory Tool 20250818 Str Replace Command

- `BetaMemoryTool20250818StrReplaceCommand = object { command, new_str, old_str, path }`

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

- `BetaMemoryTool20250818ViewCommand = object { command, path, view_range }`

  - `command: "view"`

    Command type identifier

    - `"view"`

  - `path: string`

    Path to directory or file to view

  - `view_range: optional array of number`

    Optional line range for viewing specific lines

### Beta Message

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

### Beta Message Delta Usage

- `BetaMessageDeltaUsage = object { cache_creation_input_tokens, cache_read_input_tokens, input_tokens, 2 more }`

  - `cache_creation_input_tokens: number`

    The cumulative number of input tokens used to create the cache entry.

  - `cache_read_input_tokens: number`

    The cumulative number of input tokens read from the cache.

  - `input_tokens: number`

    The cumulative number of input tokens which were used.

  - `output_tokens: number`

    The cumulative number of output tokens which were used.

  - `server_tool_use: BetaServerToolUsage`

    The number of server tool requests.

    - `web_fetch_requests: number`

      The number of web fetch tool requests.

    - `web_search_requests: number`

      The number of web search tool requests.

### Beta Message Param

- `BetaMessageParam = object { content, role }`

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

### Beta Message Tokens Count

- `BetaMessageTokensCount = object { context_management, input_tokens }`

  - `context_management: BetaCountTokensContextManagementResponse`

    Information about context management applied to the message.

    - `original_input_tokens: number`

      The original token count before context management was applied

  - `input_tokens: number`

    The total number of tokens across the provided list of messages, system prompt, and tools.

### Beta Metadata

- `BetaMetadata = object { user_id }`

  - `user_id: optional string`

    An external identifier for the user who is associated with the request.

    This should be a uuid, hash value, or other opaque identifier. Anthropic may use this id to help detect abuse. Do not include any identifying information such as name, email address, or phone number.

### Beta Output Config

- `BetaOutputConfig = object { effort }`

  - `effort: optional "low" or "medium" or "high"`

    All possible effort levels.

    - `"low"`

    - `"medium"`

    - `"high"`

### Beta Plain Text Source

- `BetaPlainTextSource = object { data, media_type, type }`

  - `data: string`

  - `media_type: "text/plain"`

    - `"text/plain"`

  - `type: "text"`

    - `"text"`

### Beta Raw Content Block Delta

- `BetaRawContentBlockDelta = BetaTextDelta or BetaInputJSONDelta or BetaCitationsDelta or 2 more`

  - `BetaTextDelta = object { text, type }`

    - `text: string`

    - `type: "text_delta"`

      - `"text_delta"`

  - `BetaInputJSONDelta = object { partial_json, type }`

    - `partial_json: string`

    - `type: "input_json_delta"`

      - `"input_json_delta"`

  - `BetaCitationsDelta = object { citation, type }`

    - `citation: BetaCitationCharLocation or BetaCitationPageLocation or BetaCitationContentBlockLocation or 2 more`

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

    - `type: "citations_delta"`

      - `"citations_delta"`

  - `BetaThinkingDelta = object { thinking, type }`

    - `thinking: string`

    - `type: "thinking_delta"`

      - `"thinking_delta"`

  - `BetaSignatureDelta = object { signature, type }`

    - `signature: string`

    - `type: "signature_delta"`

      - `"signature_delta"`

### Beta Raw Content Block Delta Event

- `BetaRawContentBlockDeltaEvent = object { delta, index, type }`

  - `delta: BetaRawContentBlockDelta`

    - `BetaTextDelta = object { text, type }`

      - `text: string`

      - `type: "text_delta"`

        - `"text_delta"`

    - `BetaInputJSONDelta = object { partial_json, type }`

      - `partial_json: string`

      - `type: "input_json_delta"`

        - `"input_json_delta"`

    - `BetaCitationsDelta = object { citation, type }`

      - `citation: BetaCitationCharLocation or BetaCitationPageLocation or BetaCitationContentBlockLocation or 2 more`

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

      - `type: "citations_delta"`

        - `"citations_delta"`

    - `BetaThinkingDelta = object { thinking, type }`

      - `thinking: string`

      - `type: "thinking_delta"`

        - `"thinking_delta"`

    - `BetaSignatureDelta = object { signature, type }`

      - `signature: string`

      - `type: "signature_delta"`

        - `"signature_delta"`

  - `index: number`

  - `type: "content_block_delta"`

    - `"content_block_delta"`

### Beta Raw Content Block Start Event

- `BetaRawContentBlockStartEvent = object { content_block, index, type }`

  - `content_block: BetaTextBlock or BetaThinkingBlock or BetaRedactedThinkingBlock or 11 more`

    Response model for a file uploaded to the container.

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

  - `index: number`

  - `type: "content_block_start"`

    - `"content_block_start"`

### Beta Raw Content Block Stop Event

- `BetaRawContentBlockStopEvent = object { index, type }`

  - `index: number`

  - `type: "content_block_stop"`

    - `"content_block_stop"`

### Beta Raw Message Delta Event

- `BetaRawMessageDeltaEvent = object { context_management, delta, type, usage }`

  - `context_management: BetaContextManagementResponse`

    Information about context management strategies applied during the request

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

  - `delta: object { container, stop_reason, stop_sequence }`

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

    - `stop_reason: BetaStopReason`

      - `"end_turn"`

      - `"max_tokens"`

      - `"stop_sequence"`

      - `"tool_use"`

      - `"pause_turn"`

      - `"refusal"`

      - `"model_context_window_exceeded"`

    - `stop_sequence: string`

  - `type: "message_delta"`

    - `"message_delta"`

  - `usage: BetaMessageDeltaUsage`

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

    - `server_tool_use: BetaServerToolUsage`

      The number of server tool requests.

      - `web_fetch_requests: number`

        The number of web fetch tool requests.

      - `web_search_requests: number`

        The number of web search tool requests.

### Beta Raw Message Start Event

- `BetaRawMessageStartEvent = object { message, type }`

  - `message: BetaMessage`

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

  - `type: "message_start"`

    - `"message_start"`

### Beta Raw Message Stop Event

- `BetaRawMessageStopEvent = object { type }`

  - `type: "message_stop"`

    - `"message_stop"`

### Beta Raw Message Stream Event

- `BetaRawMessageStreamEvent = BetaRawMessageStartEvent or BetaRawMessageDeltaEvent or BetaRawMessageStopEvent or 3 more`

  - `BetaRawMessageStartEvent = object { message, type }`

    - `message: BetaMessage`

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

    - `type: "message_start"`

      - `"message_start"`

  - `BetaRawMessageDeltaEvent = object { context_management, delta, type, usage }`

    - `context_management: BetaContextManagementResponse`

      Information about context management strategies applied during the request

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

    - `delta: object { container, stop_reason, stop_sequence }`

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

      - `stop_reason: BetaStopReason`

        - `"end_turn"`

        - `"max_tokens"`

        - `"stop_sequence"`

        - `"tool_use"`

        - `"pause_turn"`

        - `"refusal"`

        - `"model_context_window_exceeded"`

      - `stop_sequence: string`

    - `type: "message_delta"`

      - `"message_delta"`

    - `usage: BetaMessageDeltaUsage`

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

      - `server_tool_use: BetaServerToolUsage`

        The number of server tool requests.

        - `web_fetch_requests: number`

          The number of web fetch tool requests.

        - `web_search_requests: number`

          The number of web search tool requests.

  - `BetaRawMessageStopEvent = object { type }`

    - `type: "message_stop"`

      - `"message_stop"`

  - `BetaRawContentBlockStartEvent = object { content_block, index, type }`

    - `content_block: BetaTextBlock or BetaThinkingBlock or BetaRedactedThinkingBlock or 11 more`

      Response model for a file uploaded to the container.

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

    - `index: number`

    - `type: "content_block_start"`

      - `"content_block_start"`

  - `BetaRawContentBlockDeltaEvent = object { delta, index, type }`

    - `delta: BetaRawContentBlockDelta`

      - `BetaTextDelta = object { text, type }`

        - `text: string`

        - `type: "text_delta"`

          - `"text_delta"`

      - `BetaInputJSONDelta = object { partial_json, type }`

        - `partial_json: string`

        - `type: "input_json_delta"`

          - `"input_json_delta"`

      - `BetaCitationsDelta = object { citation, type }`

        - `citation: BetaCitationCharLocation or BetaCitationPageLocation or BetaCitationContentBlockLocation or 2 more`

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

        - `type: "citations_delta"`

          - `"citations_delta"`

      - `BetaThinkingDelta = object { thinking, type }`

        - `thinking: string`

        - `type: "thinking_delta"`

          - `"thinking_delta"`

      - `BetaSignatureDelta = object { signature, type }`

        - `signature: string`

        - `type: "signature_delta"`

          - `"signature_delta"`

    - `index: number`

    - `type: "content_block_delta"`

      - `"content_block_delta"`

  - `BetaRawContentBlockStopEvent = object { index, type }`

    - `index: number`

    - `type: "content_block_stop"`

      - `"content_block_stop"`

### Beta Redacted Thinking Block

- `BetaRedactedThinkingBlock = object { data, type }`

  - `data: string`

  - `type: "redacted_thinking"`

    - `"redacted_thinking"`

### Beta Redacted Thinking Block Param

- `BetaRedactedThinkingBlockParam = object { data, type }`

  - `data: string`

  - `type: "redacted_thinking"`

    - `"redacted_thinking"`

### Beta Request Document Block

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

### Beta Request MCP Server Tool Configuration

- `BetaRequestMCPServerToolConfiguration = object { allowed_tools, enabled }`

  - `allowed_tools: optional array of string`

  - `enabled: optional boolean`

### Beta Request MCP Server URL Definition

- `BetaRequestMCPServerURLDefinition = object { name, type, url, 2 more }`

  - `name: string`

  - `type: "url"`

    - `"url"`

  - `url: string`

  - `authorization_token: optional string`

  - `tool_configuration: optional BetaRequestMCPServerToolConfiguration`

    - `allowed_tools: optional array of string`

    - `enabled: optional boolean`

### Beta Request MCP Tool Result Block Param

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

### Beta Search Result Block Param

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

### Beta Server Tool Caller

- `BetaServerToolCaller = object { tool_id, type }`

  Tool invocation generated by a server-side tool.

  - `tool_id: string`

  - `type: "code_execution_20250825"`

    - `"code_execution_20250825"`

### Beta Server Tool Usage

- `BetaServerToolUsage = object { web_fetch_requests, web_search_requests }`

  - `web_fetch_requests: number`

    The number of web fetch tool requests.

  - `web_search_requests: number`

    The number of web search tool requests.

### Beta Server Tool Use Block

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

### Beta Server Tool Use Block Param

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

### Beta Signature Delta

- `BetaSignatureDelta = object { signature, type }`

  - `signature: string`

  - `type: "signature_delta"`

    - `"signature_delta"`

### Beta Skill

- `BetaSkill = object { skill_id, type, version }`

  A skill that was loaded in a container (response model).

  - `skill_id: string`

    Skill ID

  - `type: "anthropic" or "custom"`

    Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

    - `"anthropic"`

    - `"custom"`

  - `version: string`

    Skill version or 'latest' for most recent version

### Beta Skill Params

- `BetaSkillParams = object { skill_id, type, version }`

  Specification for a skill to be loaded in a container (request model).

  - `skill_id: string`

    Skill ID

  - `type: "anthropic" or "custom"`

    Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

    - `"anthropic"`

    - `"custom"`

  - `version: optional string`

    Skill version or 'latest' for most recent version

### Beta Stop Reason

- `BetaStopReason = "end_turn" or "max_tokens" or "stop_sequence" or 4 more`

  - `"end_turn"`

  - `"max_tokens"`

  - `"stop_sequence"`

  - `"tool_use"`

  - `"pause_turn"`

  - `"refusal"`

  - `"model_context_window_exceeded"`

### Beta Text Block

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

### Beta Text Block Param

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

### Beta Text Citation

- `BetaTextCitation = BetaCitationCharLocation or BetaCitationPageLocation or BetaCitationContentBlockLocation or 2 more`

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

### Beta Text Citation Param

- `BetaTextCitationParam = BetaCitationCharLocationParam or BetaCitationPageLocationParam or BetaCitationContentBlockLocationParam or 2 more`

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

### Beta Text Delta

- `BetaTextDelta = object { text, type }`

  - `text: string`

  - `type: "text_delta"`

    - `"text_delta"`

### Beta Text Editor Code Execution Create Result Block

- `BetaTextEditorCodeExecutionCreateResultBlock = object { is_file_update, type }`

  - `is_file_update: boolean`

  - `type: "text_editor_code_execution_create_result"`

    - `"text_editor_code_execution_create_result"`

### Beta Text Editor Code Execution Create Result Block Param

- `BetaTextEditorCodeExecutionCreateResultBlockParam = object { is_file_update, type }`

  - `is_file_update: boolean`

  - `type: "text_editor_code_execution_create_result"`

    - `"text_editor_code_execution_create_result"`

### Beta Text Editor Code Execution Str Replace Result Block

- `BetaTextEditorCodeExecutionStrReplaceResultBlock = object { lines, new_lines, new_start, 3 more }`

  - `lines: array of string`

  - `new_lines: number`

  - `new_start: number`

  - `old_lines: number`

  - `old_start: number`

  - `type: "text_editor_code_execution_str_replace_result"`

    - `"text_editor_code_execution_str_replace_result"`

### Beta Text Editor Code Execution Str Replace Result Block Param

- `BetaTextEditorCodeExecutionStrReplaceResultBlockParam = object { type, lines, new_lines, 3 more }`

  - `type: "text_editor_code_execution_str_replace_result"`

    - `"text_editor_code_execution_str_replace_result"`

  - `lines: optional array of string`

  - `new_lines: optional number`

  - `new_start: optional number`

  - `old_lines: optional number`

  - `old_start: optional number`

### Beta Text Editor Code Execution Tool Result Block

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

### Beta Text Editor Code Execution Tool Result Block Param

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

### Beta Text Editor Code Execution Tool Result Error

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

### Beta Text Editor Code Execution Tool Result Error Param

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

### Beta Text Editor Code Execution View Result Block

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

### Beta Text Editor Code Execution View Result Block Param

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

### Beta Thinking Block

- `BetaThinkingBlock = object { signature, thinking, type }`

  - `signature: string`

  - `thinking: string`

  - `type: "thinking"`

    - `"thinking"`

### Beta Thinking Block Param

- `BetaThinkingBlockParam = object { signature, thinking, type }`

  - `signature: string`

  - `thinking: string`

  - `type: "thinking"`

    - `"thinking"`

### Beta Thinking Config Disabled

- `BetaThinkingConfigDisabled = object { type }`

  - `type: "disabled"`

    - `"disabled"`

### Beta Thinking Config Enabled

- `BetaThinkingConfigEnabled = object { budget_tokens, type }`

  - `budget_tokens: number`

    Determines how many tokens Claude can use for its internal reasoning process. Larger budgets can enable more thorough analysis for complex problems, improving response quality.

    Must be ≥1024 and less than `max_tokens`.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `type: "enabled"`

    - `"enabled"`

### Beta Thinking Config Param

- `BetaThinkingConfigParam = BetaThinkingConfigEnabled or BetaThinkingConfigDisabled`

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

### Beta Thinking Delta

- `BetaThinkingDelta = object { thinking, type }`

  - `thinking: string`

  - `type: "thinking_delta"`

    - `"thinking_delta"`

### Beta Thinking Turns

- `BetaThinkingTurns = object { type, value }`

  - `type: "thinking_turns"`

    - `"thinking_turns"`

  - `value: number`

### Beta Tool

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

### Beta Tool Bash 20241022

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

### Beta Tool Bash 20250124

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

### Beta Tool Choice

- `BetaToolChoice = BetaToolChoiceAuto or BetaToolChoiceAny or BetaToolChoiceTool or BetaToolChoiceNone`

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

### Beta Tool Choice Any

- `BetaToolChoiceAny = object { type, disable_parallel_tool_use }`

  The model will use any available tools.

  - `type: "any"`

    - `"any"`

  - `disable_parallel_tool_use: optional boolean`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output exactly one tool use.

### Beta Tool Choice Auto

- `BetaToolChoiceAuto = object { type, disable_parallel_tool_use }`

  The model will automatically decide whether to use tools.

  - `type: "auto"`

    - `"auto"`

  - `disable_parallel_tool_use: optional boolean`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output at most one tool use.

### Beta Tool Choice None

- `BetaToolChoiceNone = object { type }`

  The model will not be allowed to use tools.

  - `type: "none"`

    - `"none"`

### Beta Tool Choice Tool

- `BetaToolChoiceTool = object { name, type, disable_parallel_tool_use }`

  The model will use the specified tool with `tool_choice.name`.

  - `name: string`

    The name of the tool to use.

  - `type: "tool"`

    - `"tool"`

  - `disable_parallel_tool_use: optional boolean`

    Whether to disable parallel tool use.

    Defaults to `false`. If set to `true`, the model will output exactly one tool use.

### Beta Tool Computer Use 20241022

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

### Beta Tool Computer Use 20250124

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

### Beta Tool Computer Use 20251124

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

### Beta Tool Reference Block

- `BetaToolReferenceBlock = object { tool_name, type }`

  - `tool_name: string`

  - `type: "tool_reference"`

    - `"tool_reference"`

### Beta Tool Reference Block Param

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

### Beta Tool Result Block Param

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

### Beta Tool Search Tool Bm25 20251119

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

### Beta Tool Search Tool Regex 20251119

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

### Beta Tool Search Tool Result Block

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

### Beta Tool Search Tool Result Block Param

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

### Beta Tool Search Tool Result Error

- `BetaToolSearchToolResultError = object { error_code, error_message, type }`

  - `error_code: "invalid_tool_input" or "unavailable" or "too_many_requests" or "execution_time_exceeded"`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

  - `error_message: string`

  - `type: "tool_search_tool_result_error"`

    - `"tool_search_tool_result_error"`

### Beta Tool Search Tool Result Error Param

- `BetaToolSearchToolResultErrorParam = object { error_code, type }`

  - `error_code: "invalid_tool_input" or "unavailable" or "too_many_requests" or "execution_time_exceeded"`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"too_many_requests"`

    - `"execution_time_exceeded"`

  - `type: "tool_search_tool_result_error"`

    - `"tool_search_tool_result_error"`

### Beta Tool Search Tool Search Result Block

- `BetaToolSearchToolSearchResultBlock = object { tool_references, type }`

  - `tool_references: array of BetaToolReferenceBlock`

    - `tool_name: string`

    - `type: "tool_reference"`

      - `"tool_reference"`

  - `type: "tool_search_tool_search_result"`

    - `"tool_search_tool_search_result"`

### Beta Tool Search Tool Search Result Block Param

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

### Beta Tool Text Editor 20241022

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

### Beta Tool Text Editor 20250124

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

### Beta Tool Text Editor 20250429

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

### Beta Tool Text Editor 20250728

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

### Beta Tool Union

- `BetaToolUnion = BetaTool or BetaToolBash20241022 or BetaToolBash20250124 or 15 more`

  Configuration for a group of tools from an MCP server.

  Allows configuring enabled status and defer_loading for all tools
  from an MCP server, with optional per-tool overrides.

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

### Beta Tool Use Block

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

### Beta Tool Use Block Param

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

### Beta Tool Uses Keep

- `BetaToolUsesKeep = object { type, value }`

  - `type: "tool_uses"`

    - `"tool_uses"`

  - `value: number`

### Beta Tool Uses Trigger

- `BetaToolUsesTrigger = object { type, value }`

  - `type: "tool_uses"`

    - `"tool_uses"`

  - `value: number`

### Beta URL Image Source

- `BetaURLImageSource = object { type, url }`

  - `type: "url"`

    - `"url"`

  - `url: string`

### Beta URL PDF Source

- `BetaURLPDFSource = object { type, url }`

  - `type: "url"`

    - `"url"`

  - `url: string`

### Beta Usage

- `BetaUsage = object { cache_creation, cache_creation_input_tokens, cache_read_input_tokens, 4 more }`

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

### Beta Web Fetch Block

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

### Beta Web Fetch Block Param

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

### Beta Web Fetch Tool 20250910

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

### Beta Web Fetch Tool Result Block

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

### Beta Web Fetch Tool Result Block Param

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

### Beta Web Fetch Tool Result Error Block

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

### Beta Web Fetch Tool Result Error Block Param

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

### Beta Web Fetch Tool Result Error Code

- `BetaWebFetchToolResultErrorCode = "invalid_tool_input" or "url_too_long" or "url_not_allowed" or 5 more`

  - `"invalid_tool_input"`

  - `"url_too_long"`

  - `"url_not_allowed"`

  - `"url_not_accessible"`

  - `"unsupported_content_type"`

  - `"too_many_requests"`

  - `"max_uses_exceeded"`

  - `"unavailable"`

### Beta Web Search Result Block

- `BetaWebSearchResultBlock = object { encrypted_content, page_age, title, 2 more }`

  - `encrypted_content: string`

  - `page_age: string`

  - `title: string`

  - `type: "web_search_result"`

    - `"web_search_result"`

  - `url: string`

### Beta Web Search Result Block Param

- `BetaWebSearchResultBlockParam = object { encrypted_content, title, type, 2 more }`

  - `encrypted_content: string`

  - `title: string`

  - `type: "web_search_result"`

    - `"web_search_result"`

  - `url: string`

  - `page_age: optional string`

### Beta Web Search Tool 20250305

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

### Beta Web Search Tool Request Error

- `BetaWebSearchToolRequestError = object { error_code, type }`

  - `error_code: BetaWebSearchToolResultErrorCode`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"max_uses_exceeded"`

    - `"too_many_requests"`

    - `"query_too_long"`

  - `type: "web_search_tool_result_error"`

    - `"web_search_tool_result_error"`

### Beta Web Search Tool Result Block

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

### Beta Web Search Tool Result Block Content

- `BetaWebSearchToolResultBlockContent = BetaWebSearchToolResultError or array of BetaWebSearchResultBlock`

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

### Beta Web Search Tool Result Block Param

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

### Beta Web Search Tool Result Block Param Content

- `BetaWebSearchToolResultBlockParamContent = array of BetaWebSearchResultBlockParam or BetaWebSearchToolRequestError`

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

### Beta Web Search Tool Result Error

- `BetaWebSearchToolResultError = object { error_code, type }`

  - `error_code: BetaWebSearchToolResultErrorCode`

    - `"invalid_tool_input"`

    - `"unavailable"`

    - `"max_uses_exceeded"`

    - `"too_many_requests"`

    - `"query_too_long"`

  - `type: "web_search_tool_result_error"`

    - `"web_search_tool_result_error"`

### Beta Web Search Tool Result Error Code

- `BetaWebSearchToolResultErrorCode = "invalid_tool_input" or "unavailable" or "max_uses_exceeded" or 2 more`

  - `"invalid_tool_input"`

  - `"unavailable"`

  - `"max_uses_exceeded"`

  - `"too_many_requests"`

  - `"query_too_long"`

# Batches

## Create

**post** `/v1/messages/batches`

Send a batch of Message creation requests.

The Message Batches API can be used to process multiple Messages API requests at once. Once a Message Batch is created, it begins processing immediately. Batches can take up to 24 hours to complete.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

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

- `requests: array of object { custom_id, params }`

  List of requests for prompt completion. Each is an individual request to create a Message.

  - `custom_id: string`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `params: object { max_tokens, messages, model, 16 more }`

    Messages API creation parameters for the individual request.

    See the [Messages API reference](https://docs.claude.com/en/api/messages) for full documentation on available parameters.

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

- `BetaMessageBatch = object { id, archived_at, cancel_initiated_at, 7 more }`

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

### Returns

- `BetaMessageBatch = object { id, archived_at, cancel_initiated_at, 7 more }`

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

### Returns

- `data: array of BetaMessageBatch`

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

### Returns

- `BetaMessageBatch = object { id, archived_at, cancel_initiated_at, 7 more }`

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

### Returns

- `BetaDeletedMessageBatch = object { id, type }`

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

### Returns

- `BetaMessageBatchIndividualResponse = object { custom_id, result }`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `custom_id: string`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: BetaMessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `BetaMessageBatchSucceededResult = object { message, type }`

      - `message: BetaMessage`

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

      - `type: "succeeded"`

        - `"succeeded"`

    - `BetaMessageBatchErroredResult = object { error, type }`

      - `error: BetaErrorResponse`

        - `error: BetaError`

          - `BetaInvalidRequestError = object { message, type }`

            - `message: string`

            - `type: "invalid_request_error"`

              - `"invalid_request_error"`

          - `BetaAuthenticationError = object { message, type }`

            - `message: string`

            - `type: "authentication_error"`

              - `"authentication_error"`

          - `BetaBillingError = object { message, type }`

            - `message: string`

            - `type: "billing_error"`

              - `"billing_error"`

          - `BetaPermissionError = object { message, type }`

            - `message: string`

            - `type: "permission_error"`

              - `"permission_error"`

          - `BetaNotFoundError = object { message, type }`

            - `message: string`

            - `type: "not_found_error"`

              - `"not_found_error"`

          - `BetaRateLimitError = object { message, type }`

            - `message: string`

            - `type: "rate_limit_error"`

              - `"rate_limit_error"`

          - `BetaGatewayTimeoutError = object { message, type }`

            - `message: string`

            - `type: "timeout_error"`

              - `"timeout_error"`

          - `BetaAPIError = object { message, type }`

            - `message: string`

            - `type: "api_error"`

              - `"api_error"`

          - `BetaOverloadedError = object { message, type }`

            - `message: string`

            - `type: "overloaded_error"`

              - `"overloaded_error"`

        - `request_id: string`

        - `type: "error"`

          - `"error"`

      - `type: "errored"`

        - `"errored"`

    - `BetaMessageBatchCanceledResult = object { type }`

      - `type: "canceled"`

        - `"canceled"`

    - `BetaMessageBatchExpiredResult = object { type }`

      - `type: "expired"`

        - `"expired"`

### Example

```http
curl https://api.anthropic.com/v1/messages/batches/$MESSAGE_BATCH_ID/results \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

## Domain Types

### Beta Deleted Message Batch

- `BetaDeletedMessageBatch = object { id, type }`

  - `id: string`

    ID of the Message Batch.

  - `type: "message_batch_deleted"`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `"message_batch_deleted"`

### Beta Message Batch

- `BetaMessageBatch = object { id, archived_at, cancel_initiated_at, 7 more }`

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

  - `results_url: string`

    URL to a `.jsonl` file containing the results of the Message Batch requests. Specified only once processing ends.

    Results in the file are not guaranteed to be in the same order as requests. Use the `custom_id` field to match results to requests.

  - `type: "message_batch"`

    Object type.

    For Message Batches, this is always `"message_batch"`.

    - `"message_batch"`

### Beta Message Batch Canceled Result

- `BetaMessageBatchCanceledResult = object { type }`

  - `type: "canceled"`

    - `"canceled"`

### Beta Message Batch Errored Result

- `BetaMessageBatchErroredResult = object { error, type }`

  - `error: BetaErrorResponse`

    - `error: BetaError`

      - `BetaInvalidRequestError = object { message, type }`

        - `message: string`

        - `type: "invalid_request_error"`

          - `"invalid_request_error"`

      - `BetaAuthenticationError = object { message, type }`

        - `message: string`

        - `type: "authentication_error"`

          - `"authentication_error"`

      - `BetaBillingError = object { message, type }`

        - `message: string`

        - `type: "billing_error"`

          - `"billing_error"`

      - `BetaPermissionError = object { message, type }`

        - `message: string`

        - `type: "permission_error"`

          - `"permission_error"`

      - `BetaNotFoundError = object { message, type }`

        - `message: string`

        - `type: "not_found_error"`

          - `"not_found_error"`

      - `BetaRateLimitError = object { message, type }`

        - `message: string`

        - `type: "rate_limit_error"`

          - `"rate_limit_error"`

      - `BetaGatewayTimeoutError = object { message, type }`

        - `message: string`

        - `type: "timeout_error"`

          - `"timeout_error"`

      - `BetaAPIError = object { message, type }`

        - `message: string`

        - `type: "api_error"`

          - `"api_error"`

      - `BetaOverloadedError = object { message, type }`

        - `message: string`

        - `type: "overloaded_error"`

          - `"overloaded_error"`

    - `request_id: string`

    - `type: "error"`

      - `"error"`

  - `type: "errored"`

    - `"errored"`

### Beta Message Batch Expired Result

- `BetaMessageBatchExpiredResult = object { type }`

  - `type: "expired"`

    - `"expired"`

### Beta Message Batch Individual Response

- `BetaMessageBatchIndividualResponse = object { custom_id, result }`

  This is a single line in the response `.jsonl` file and does not represent the response as a whole.

  - `custom_id: string`

    Developer-provided ID created for each request in a Message Batch. Useful for matching results to requests, as results may be given out of request order.

    Must be unique for each request within the Message Batch.

  - `result: BetaMessageBatchResult`

    Processing result for this request.

    Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

    - `BetaMessageBatchSucceededResult = object { message, type }`

      - `message: BetaMessage`

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

      - `type: "succeeded"`

        - `"succeeded"`

    - `BetaMessageBatchErroredResult = object { error, type }`

      - `error: BetaErrorResponse`

        - `error: BetaError`

          - `BetaInvalidRequestError = object { message, type }`

            - `message: string`

            - `type: "invalid_request_error"`

              - `"invalid_request_error"`

          - `BetaAuthenticationError = object { message, type }`

            - `message: string`

            - `type: "authentication_error"`

              - `"authentication_error"`

          - `BetaBillingError = object { message, type }`

            - `message: string`

            - `type: "billing_error"`

              - `"billing_error"`

          - `BetaPermissionError = object { message, type }`

            - `message: string`

            - `type: "permission_error"`

              - `"permission_error"`

          - `BetaNotFoundError = object { message, type }`

            - `message: string`

            - `type: "not_found_error"`

              - `"not_found_error"`

          - `BetaRateLimitError = object { message, type }`

            - `message: string`

            - `type: "rate_limit_error"`

              - `"rate_limit_error"`

          - `BetaGatewayTimeoutError = object { message, type }`

            - `message: string`

            - `type: "timeout_error"`

              - `"timeout_error"`

          - `BetaAPIError = object { message, type }`

            - `message: string`

            - `type: "api_error"`

              - `"api_error"`

          - `BetaOverloadedError = object { message, type }`

            - `message: string`

            - `type: "overloaded_error"`

              - `"overloaded_error"`

        - `request_id: string`

        - `type: "error"`

          - `"error"`

      - `type: "errored"`

        - `"errored"`

    - `BetaMessageBatchCanceledResult = object { type }`

      - `type: "canceled"`

        - `"canceled"`

    - `BetaMessageBatchExpiredResult = object { type }`

      - `type: "expired"`

        - `"expired"`

### Beta Message Batch Request Counts

- `BetaMessageBatchRequestCounts = object { canceled, errored, expired, 2 more }`

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

- `BetaMessageBatchResult = BetaMessageBatchSucceededResult or BetaMessageBatchErroredResult or BetaMessageBatchCanceledResult or BetaMessageBatchExpiredResult`

  Processing result for this request.

  Contains a Message output if processing was successful, an error response if processing failed, or the reason why processing was not attempted, such as cancellation or expiration.

  - `BetaMessageBatchSucceededResult = object { message, type }`

    - `message: BetaMessage`

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

    - `type: "succeeded"`

      - `"succeeded"`

  - `BetaMessageBatchErroredResult = object { error, type }`

    - `error: BetaErrorResponse`

      - `error: BetaError`

        - `BetaInvalidRequestError = object { message, type }`

          - `message: string`

          - `type: "invalid_request_error"`

            - `"invalid_request_error"`

        - `BetaAuthenticationError = object { message, type }`

          - `message: string`

          - `type: "authentication_error"`

            - `"authentication_error"`

        - `BetaBillingError = object { message, type }`

          - `message: string`

          - `type: "billing_error"`

            - `"billing_error"`

        - `BetaPermissionError = object { message, type }`

          - `message: string`

          - `type: "permission_error"`

            - `"permission_error"`

        - `BetaNotFoundError = object { message, type }`

          - `message: string`

          - `type: "not_found_error"`

            - `"not_found_error"`

        - `BetaRateLimitError = object { message, type }`

          - `message: string`

          - `type: "rate_limit_error"`

            - `"rate_limit_error"`

        - `BetaGatewayTimeoutError = object { message, type }`

          - `message: string`

          - `type: "timeout_error"`

            - `"timeout_error"`

        - `BetaAPIError = object { message, type }`

          - `message: string`

          - `type: "api_error"`

            - `"api_error"`

        - `BetaOverloadedError = object { message, type }`

          - `message: string`

          - `type: "overloaded_error"`

            - `"overloaded_error"`

      - `request_id: string`

      - `type: "error"`

        - `"error"`

    - `type: "errored"`

      - `"errored"`

  - `BetaMessageBatchCanceledResult = object { type }`

    - `type: "canceled"`

      - `"canceled"`

  - `BetaMessageBatchExpiredResult = object { type }`

    - `type: "expired"`

      - `"expired"`

### Beta Message Batch Succeeded Result

- `BetaMessageBatchSucceededResult = object { message, type }`

  - `message: BetaMessage`

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

  - `type: "succeeded"`

    - `"succeeded"`
