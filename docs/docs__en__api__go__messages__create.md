## Create

`client.Messages.New(ctx, body) (*Message, error)`

**post** `/v1/messages`

Send a structured list of input messages with text and/or image content, and the model will generate the next message in the conversation.

The Messages API can be used for either single queries or stateless multi-turn conversations.

Learn more about the Messages API in our [user guide](https://docs.claude.com/en/docs/initial-setup)

### Parameters

- `body MessageNewParams`

  - `MaxTokens param.Field[int64]`

    The maximum number of tokens to generate before stopping.

    Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

    Different models have different maximum values for this parameter.  See [models](https://docs.claude.com/en/docs/models-overview) for details.

  - `Messages param.Field[[]MessageParamResp]`

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

    - `Content []ContentBlockParamUnionResp`

      - `[]ContentBlockParamUnionResp`

        - `type TextBlockParamResp struct{…}`

          - `Text string`

          - `Type Text`

            - `const TextText Text = "text"`

          - `CacheControl CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL CacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

              - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

          - `Citations []TextCitationParamUnionResp`

            - `type CitationCharLocationParamResp struct{…}`

              - `CitedText string`

              - `DocumentIndex int64`

              - `DocumentTitle string`

              - `EndCharIndex int64`

              - `StartCharIndex int64`

              - `Type CharLocation`

                - `const CharLocationCharLocation CharLocation = "char_location"`

            - `type CitationPageLocationParamResp struct{…}`

              - `CitedText string`

              - `DocumentIndex int64`

              - `DocumentTitle string`

              - `EndPageNumber int64`

              - `StartPageNumber int64`

              - `Type PageLocation`

                - `const PageLocationPageLocation PageLocation = "page_location"`

            - `type CitationContentBlockLocationParamResp struct{…}`

              - `CitedText string`

              - `DocumentIndex int64`

              - `DocumentTitle string`

              - `EndBlockIndex int64`

              - `StartBlockIndex int64`

              - `Type ContentBlockLocation`

                - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

            - `type CitationWebSearchResultLocationParamResp struct{…}`

              - `CitedText string`

              - `EncryptedIndex string`

              - `Title string`

              - `Type WebSearchResultLocation`

                - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

              - `URL string`

            - `type CitationSearchResultLocationParamResp struct{…}`

              - `CitedText string`

              - `EndBlockIndex int64`

              - `SearchResultIndex int64`

              - `Source string`

              - `StartBlockIndex int64`

              - `Title string`

              - `Type SearchResultLocation`

                - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

        - `type ImageBlockParamResp struct{…}`

          - `Source ImageBlockParamSourceUnionResp`

            - `type Base64ImageSource struct{…}`

              - `Data string`

              - `MediaType Base64ImageSourceMediaType`

                - `const Base64ImageSourceMediaTypeImageJPEG Base64ImageSourceMediaType = "image/jpeg"`

                - `const Base64ImageSourceMediaTypeImagePNG Base64ImageSourceMediaType = "image/png"`

                - `const Base64ImageSourceMediaTypeImageGIF Base64ImageSourceMediaType = "image/gif"`

                - `const Base64ImageSourceMediaTypeImageWebP Base64ImageSourceMediaType = "image/webp"`

              - `Type Base64`

                - `const Base64Base64 Base64 = "base64"`

            - `type URLImageSource struct{…}`

              - `Type URL`

                - `const URLURL URL = "url"`

              - `URL string`

          - `Type Image`

            - `const ImageImage Image = "image"`

          - `CacheControl CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL CacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

              - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

        - `type DocumentBlockParamResp struct{…}`

          - `Source DocumentBlockParamSourceUnionResp`

            - `type Base64PDFSource struct{…}`

              - `Data string`

              - `MediaType ApplicationPDF`

                - `const ApplicationPDFApplicationPDF ApplicationPDF = "application/pdf"`

              - `Type Base64`

                - `const Base64Base64 Base64 = "base64"`

            - `type PlainTextSource struct{…}`

              - `Data string`

              - `MediaType TextPlain`

                - `const TextPlainTextPlain TextPlain = "text/plain"`

              - `Type Text`

                - `const TextText Text = "text"`

            - `type ContentBlockSource struct{…}`

              - `Content ContentBlockSourceContentUnion`

                - `string`

                - `[]ContentBlockSourceContentItemUnion`

                  - `type TextBlockParamResp struct{…}`

                    - `Text string`

                    - `Type Text`

                      - `const TextText Text = "text"`

                    - `CacheControl CacheControlEphemeral`

                      Create a cache control breakpoint at this content block.

                      - `Type Ephemeral`

                        - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                      - `TTL CacheControlEphemeralTTL`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

                        - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

                    - `Citations []TextCitationParamUnionResp`

                      - `type CitationCharLocationParamResp struct{…}`

                        - `CitedText string`

                        - `DocumentIndex int64`

                        - `DocumentTitle string`

                        - `EndCharIndex int64`

                        - `StartCharIndex int64`

                        - `Type CharLocation`

                          - `const CharLocationCharLocation CharLocation = "char_location"`

                      - `type CitationPageLocationParamResp struct{…}`

                        - `CitedText string`

                        - `DocumentIndex int64`

                        - `DocumentTitle string`

                        - `EndPageNumber int64`

                        - `StartPageNumber int64`

                        - `Type PageLocation`

                          - `const PageLocationPageLocation PageLocation = "page_location"`

                      - `type CitationContentBlockLocationParamResp struct{…}`

                        - `CitedText string`

                        - `DocumentIndex int64`

                        - `DocumentTitle string`

                        - `EndBlockIndex int64`

                        - `StartBlockIndex int64`

                        - `Type ContentBlockLocation`

                          - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

                      - `type CitationWebSearchResultLocationParamResp struct{…}`

                        - `CitedText string`

                        - `EncryptedIndex string`

                        - `Title string`

                        - `Type WebSearchResultLocation`

                          - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

                        - `URL string`

                      - `type CitationSearchResultLocationParamResp struct{…}`

                        - `CitedText string`

                        - `EndBlockIndex int64`

                        - `SearchResultIndex int64`

                        - `Source string`

                        - `StartBlockIndex int64`

                        - `Title string`

                        - `Type SearchResultLocation`

                          - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

                  - `type ImageBlockParamResp struct{…}`

                    - `Source ImageBlockParamSourceUnionResp`

                      - `type Base64ImageSource struct{…}`

                        - `Data string`

                        - `MediaType Base64ImageSourceMediaType`

                          - `const Base64ImageSourceMediaTypeImageJPEG Base64ImageSourceMediaType = "image/jpeg"`

                          - `const Base64ImageSourceMediaTypeImagePNG Base64ImageSourceMediaType = "image/png"`

                          - `const Base64ImageSourceMediaTypeImageGIF Base64ImageSourceMediaType = "image/gif"`

                          - `const Base64ImageSourceMediaTypeImageWebP Base64ImageSourceMediaType = "image/webp"`

                        - `Type Base64`

                          - `const Base64Base64 Base64 = "base64"`

                      - `type URLImageSource struct{…}`

                        - `Type URL`

                          - `const URLURL URL = "url"`

                        - `URL string`

                    - `Type Image`

                      - `const ImageImage Image = "image"`

                    - `CacheControl CacheControlEphemeral`

                      Create a cache control breakpoint at this content block.

                      - `Type Ephemeral`

                        - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                      - `TTL CacheControlEphemeralTTL`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

                        - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

              - `Type Content`

                - `const ContentContent Content = "content"`

            - `type URLPDFSource struct{…}`

              - `Type URL`

                - `const URLURL URL = "url"`

              - `URL string`

          - `Type Document`

            - `const DocumentDocument Document = "document"`

          - `CacheControl CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL CacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

              - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

          - `Citations CitationsConfigParamResp`

            - `Enabled bool`

          - `Context string`

          - `Title string`

        - `type SearchResultBlockParamResp struct{…}`

          - `Content []TextBlockParamResp`

            - `Text string`

            - `Type Text`

              - `const TextText Text = "text"`

            - `CacheControl CacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `Type Ephemeral`

                - `const EphemeralEphemeral Ephemeral = "ephemeral"`

              - `TTL CacheControlEphemeralTTL`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

                - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

            - `Citations []TextCitationParamUnionResp`

              - `type CitationCharLocationParamResp struct{…}`

                - `CitedText string`

                - `DocumentIndex int64`

                - `DocumentTitle string`

                - `EndCharIndex int64`

                - `StartCharIndex int64`

                - `Type CharLocation`

                  - `const CharLocationCharLocation CharLocation = "char_location"`

              - `type CitationPageLocationParamResp struct{…}`

                - `CitedText string`

                - `DocumentIndex int64`

                - `DocumentTitle string`

                - `EndPageNumber int64`

                - `StartPageNumber int64`

                - `Type PageLocation`

                  - `const PageLocationPageLocation PageLocation = "page_location"`

              - `type CitationContentBlockLocationParamResp struct{…}`

                - `CitedText string`

                - `DocumentIndex int64`

                - `DocumentTitle string`

                - `EndBlockIndex int64`

                - `StartBlockIndex int64`

                - `Type ContentBlockLocation`

                  - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

              - `type CitationWebSearchResultLocationParamResp struct{…}`

                - `CitedText string`

                - `EncryptedIndex string`

                - `Title string`

                - `Type WebSearchResultLocation`

                  - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

                - `URL string`

              - `type CitationSearchResultLocationParamResp struct{…}`

                - `CitedText string`

                - `EndBlockIndex int64`

                - `SearchResultIndex int64`

                - `Source string`

                - `StartBlockIndex int64`

                - `Title string`

                - `Type SearchResultLocation`

                  - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

          - `Source string`

          - `Title string`

          - `Type SearchResult`

            - `const SearchResultSearchResult SearchResult = "search_result"`

          - `CacheControl CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL CacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

              - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

          - `Citations CitationsConfigParamResp`

            - `Enabled bool`

        - `type ThinkingBlockParamResp struct{…}`

          - `Signature string`

          - `Thinking string`

          - `Type Thinking`

            - `const ThinkingThinking Thinking = "thinking"`

        - `type RedactedThinkingBlockParamResp struct{…}`

          - `Data string`

          - `Type RedactedThinking`

            - `const RedactedThinkingRedactedThinking RedactedThinking = "redacted_thinking"`

        - `type ToolUseBlockParamResp struct{…}`

          - `ID string`

          - `Input map[string, any]`

          - `Name string`

          - `Type ToolUse`

            - `const ToolUseToolUse ToolUse = "tool_use"`

          - `CacheControl CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL CacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

              - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

        - `type ToolResultBlockParamResp struct{…}`

          - `ToolUseID string`

          - `Type ToolResult`

            - `const ToolResultToolResult ToolResult = "tool_result"`

          - `CacheControl CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL CacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

              - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

          - `Content []ToolResultBlockParamContentUnionResp`

            - `[]ToolResultBlockParamContentUnionResp`

              - `type TextBlockParamResp struct{…}`

                - `Text string`

                - `Type Text`

                  - `const TextText Text = "text"`

                - `CacheControl CacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `Type Ephemeral`

                    - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                  - `TTL CacheControlEphemeralTTL`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

                    - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

                - `Citations []TextCitationParamUnionResp`

                  - `type CitationCharLocationParamResp struct{…}`

                    - `CitedText string`

                    - `DocumentIndex int64`

                    - `DocumentTitle string`

                    - `EndCharIndex int64`

                    - `StartCharIndex int64`

                    - `Type CharLocation`

                      - `const CharLocationCharLocation CharLocation = "char_location"`

                  - `type CitationPageLocationParamResp struct{…}`

                    - `CitedText string`

                    - `DocumentIndex int64`

                    - `DocumentTitle string`

                    - `EndPageNumber int64`

                    - `StartPageNumber int64`

                    - `Type PageLocation`

                      - `const PageLocationPageLocation PageLocation = "page_location"`

                  - `type CitationContentBlockLocationParamResp struct{…}`

                    - `CitedText string`

                    - `DocumentIndex int64`

                    - `DocumentTitle string`

                    - `EndBlockIndex int64`

                    - `StartBlockIndex int64`

                    - `Type ContentBlockLocation`

                      - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

                  - `type CitationWebSearchResultLocationParamResp struct{…}`

                    - `CitedText string`

                    - `EncryptedIndex string`

                    - `Title string`

                    - `Type WebSearchResultLocation`

                      - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

                    - `URL string`

                  - `type CitationSearchResultLocationParamResp struct{…}`

                    - `CitedText string`

                    - `EndBlockIndex int64`

                    - `SearchResultIndex int64`

                    - `Source string`

                    - `StartBlockIndex int64`

                    - `Title string`

                    - `Type SearchResultLocation`

                      - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

              - `type ImageBlockParamResp struct{…}`

                - `Source ImageBlockParamSourceUnionResp`

                  - `type Base64ImageSource struct{…}`

                    - `Data string`

                    - `MediaType Base64ImageSourceMediaType`

                      - `const Base64ImageSourceMediaTypeImageJPEG Base64ImageSourceMediaType = "image/jpeg"`

                      - `const Base64ImageSourceMediaTypeImagePNG Base64ImageSourceMediaType = "image/png"`

                      - `const Base64ImageSourceMediaTypeImageGIF Base64ImageSourceMediaType = "image/gif"`

                      - `const Base64ImageSourceMediaTypeImageWebP Base64ImageSourceMediaType = "image/webp"`

                    - `Type Base64`

                      - `const Base64Base64 Base64 = "base64"`

                  - `type URLImageSource struct{…}`

                    - `Type URL`

                      - `const URLURL URL = "url"`

                    - `URL string`

                - `Type Image`

                  - `const ImageImage Image = "image"`

                - `CacheControl CacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `Type Ephemeral`

                    - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                  - `TTL CacheControlEphemeralTTL`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

                    - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

              - `type SearchResultBlockParamResp struct{…}`

                - `Content []TextBlockParamResp`

                  - `Text string`

                  - `Type Text`

                    - `const TextText Text = "text"`

                  - `CacheControl CacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `Type Ephemeral`

                      - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                    - `TTL CacheControlEphemeralTTL`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

                      - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

                  - `Citations []TextCitationParamUnionResp`

                    - `type CitationCharLocationParamResp struct{…}`

                      - `CitedText string`

                      - `DocumentIndex int64`

                      - `DocumentTitle string`

                      - `EndCharIndex int64`

                      - `StartCharIndex int64`

                      - `Type CharLocation`

                        - `const CharLocationCharLocation CharLocation = "char_location"`

                    - `type CitationPageLocationParamResp struct{…}`

                      - `CitedText string`

                      - `DocumentIndex int64`

                      - `DocumentTitle string`

                      - `EndPageNumber int64`

                      - `StartPageNumber int64`

                      - `Type PageLocation`

                        - `const PageLocationPageLocation PageLocation = "page_location"`

                    - `type CitationContentBlockLocationParamResp struct{…}`

                      - `CitedText string`

                      - `DocumentIndex int64`

                      - `DocumentTitle string`

                      - `EndBlockIndex int64`

                      - `StartBlockIndex int64`

                      - `Type ContentBlockLocation`

                        - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

                    - `type CitationWebSearchResultLocationParamResp struct{…}`

                      - `CitedText string`

                      - `EncryptedIndex string`

                      - `Title string`

                      - `Type WebSearchResultLocation`

                        - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

                      - `URL string`

                    - `type CitationSearchResultLocationParamResp struct{…}`

                      - `CitedText string`

                      - `EndBlockIndex int64`

                      - `SearchResultIndex int64`

                      - `Source string`

                      - `StartBlockIndex int64`

                      - `Title string`

                      - `Type SearchResultLocation`

                        - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

                - `Source string`

                - `Title string`

                - `Type SearchResult`

                  - `const SearchResultSearchResult SearchResult = "search_result"`

                - `CacheControl CacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `Type Ephemeral`

                    - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                  - `TTL CacheControlEphemeralTTL`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

                    - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

                - `Citations CitationsConfigParamResp`

                  - `Enabled bool`

              - `type DocumentBlockParamResp struct{…}`

                - `Source DocumentBlockParamSourceUnionResp`

                  - `type Base64PDFSource struct{…}`

                    - `Data string`

                    - `MediaType ApplicationPDF`

                      - `const ApplicationPDFApplicationPDF ApplicationPDF = "application/pdf"`

                    - `Type Base64`

                      - `const Base64Base64 Base64 = "base64"`

                  - `type PlainTextSource struct{…}`

                    - `Data string`

                    - `MediaType TextPlain`

                      - `const TextPlainTextPlain TextPlain = "text/plain"`

                    - `Type Text`

                      - `const TextText Text = "text"`

                  - `type ContentBlockSource struct{…}`

                    - `Content ContentBlockSourceContentUnion`

                      - `string`

                      - `[]ContentBlockSourceContentItemUnion`

                        - `type TextBlockParamResp struct{…}`

                          - `Text string`

                          - `Type Text`

                            - `const TextText Text = "text"`

                          - `CacheControl CacheControlEphemeral`

                            Create a cache control breakpoint at this content block.

                            - `Type Ephemeral`

                              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                            - `TTL CacheControlEphemeralTTL`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

                              - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

                          - `Citations []TextCitationParamUnionResp`

                            - `type CitationCharLocationParamResp struct{…}`

                              - `CitedText string`

                              - `DocumentIndex int64`

                              - `DocumentTitle string`

                              - `EndCharIndex int64`

                              - `StartCharIndex int64`

                              - `Type CharLocation`

                                - `const CharLocationCharLocation CharLocation = "char_location"`

                            - `type CitationPageLocationParamResp struct{…}`

                              - `CitedText string`

                              - `DocumentIndex int64`

                              - `DocumentTitle string`

                              - `EndPageNumber int64`

                              - `StartPageNumber int64`

                              - `Type PageLocation`

                                - `const PageLocationPageLocation PageLocation = "page_location"`

                            - `type CitationContentBlockLocationParamResp struct{…}`

                              - `CitedText string`

                              - `DocumentIndex int64`

                              - `DocumentTitle string`

                              - `EndBlockIndex int64`

                              - `StartBlockIndex int64`

                              - `Type ContentBlockLocation`

                                - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

                            - `type CitationWebSearchResultLocationParamResp struct{…}`

                              - `CitedText string`

                              - `EncryptedIndex string`

                              - `Title string`

                              - `Type WebSearchResultLocation`

                                - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

                              - `URL string`

                            - `type CitationSearchResultLocationParamResp struct{…}`

                              - `CitedText string`

                              - `EndBlockIndex int64`

                              - `SearchResultIndex int64`

                              - `Source string`

                              - `StartBlockIndex int64`

                              - `Title string`

                              - `Type SearchResultLocation`

                                - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

                        - `type ImageBlockParamResp struct{…}`

                          - `Source ImageBlockParamSourceUnionResp`

                            - `type Base64ImageSource struct{…}`

                              - `Data string`

                              - `MediaType Base64ImageSourceMediaType`

                                - `const Base64ImageSourceMediaTypeImageJPEG Base64ImageSourceMediaType = "image/jpeg"`

                                - `const Base64ImageSourceMediaTypeImagePNG Base64ImageSourceMediaType = "image/png"`

                                - `const Base64ImageSourceMediaTypeImageGIF Base64ImageSourceMediaType = "image/gif"`

                                - `const Base64ImageSourceMediaTypeImageWebP Base64ImageSourceMediaType = "image/webp"`

                              - `Type Base64`

                                - `const Base64Base64 Base64 = "base64"`

                            - `type URLImageSource struct{…}`

                              - `Type URL`

                                - `const URLURL URL = "url"`

                              - `URL string`

                          - `Type Image`

                            - `const ImageImage Image = "image"`

                          - `CacheControl CacheControlEphemeral`

                            Create a cache control breakpoint at this content block.

                            - `Type Ephemeral`

                              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                            - `TTL CacheControlEphemeralTTL`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

                              - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

                    - `Type Content`

                      - `const ContentContent Content = "content"`

                  - `type URLPDFSource struct{…}`

                    - `Type URL`

                      - `const URLURL URL = "url"`

                    - `URL string`

                - `Type Document`

                  - `const DocumentDocument Document = "document"`

                - `CacheControl CacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `Type Ephemeral`

                    - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                  - `TTL CacheControlEphemeralTTL`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

                    - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

                - `Citations CitationsConfigParamResp`

                  - `Enabled bool`

                - `Context string`

                - `Title string`

          - `IsError bool`

        - `type ServerToolUseBlockParamResp struct{…}`

          - `ID string`

          - `Input map[string, any]`

          - `Name WebSearch`

            - `const WebSearchWebSearch WebSearch = "web_search"`

          - `Type ServerToolUse`

            - `const ServerToolUseServerToolUse ServerToolUse = "server_tool_use"`

          - `CacheControl CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL CacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

              - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

        - `type WebSearchToolResultBlockParamResp struct{…}`

          - `Content WebSearchToolResultBlockParamContentUnionResp`

            - `[]WebSearchResultBlockParamResp`

              - `EncryptedContent string`

              - `Title string`

              - `Type WebSearchResult`

                - `const WebSearchResultWebSearchResult WebSearchResult = "web_search_result"`

              - `URL string`

              - `PageAge string`

            - `type WebSearchToolRequestError struct{…}`

              - `ErrorCode WebSearchToolRequestErrorErrorCode`

                - `const WebSearchToolRequestErrorErrorCodeInvalidToolInput WebSearchToolRequestErrorErrorCode = "invalid_tool_input"`

                - `const WebSearchToolRequestErrorErrorCodeUnavailable WebSearchToolRequestErrorErrorCode = "unavailable"`

                - `const WebSearchToolRequestErrorErrorCodeMaxUsesExceeded WebSearchToolRequestErrorErrorCode = "max_uses_exceeded"`

                - `const WebSearchToolRequestErrorErrorCodeTooManyRequests WebSearchToolRequestErrorErrorCode = "too_many_requests"`

                - `const WebSearchToolRequestErrorErrorCodeQueryTooLong WebSearchToolRequestErrorErrorCode = "query_too_long"`

              - `Type WebSearchToolResultError`

                - `const WebSearchToolResultErrorWebSearchToolResultError WebSearchToolResultError = "web_search_tool_result_error"`

          - `ToolUseID string`

          - `Type WebSearchToolResult`

            - `const WebSearchToolResultWebSearchToolResult WebSearchToolResult = "web_search_tool_result"`

          - `CacheControl CacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL CacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

              - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

    - `Role MessageParamRole`

      - `const MessageParamRoleUser MessageParamRole = "user"`

      - `const MessageParamRoleAssistant MessageParamRole = "assistant"`

  - `Model param.Field[Model]`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

  - `Metadata param.Field[Metadata]`

    An object describing metadata about the request.

  - `ServiceTier param.Field[MessageNewParamsServiceTier]`

    Determines whether to use priority capacity (if available) or standard capacity for this request.

    Anthropic offers different levels of service for your API requests. See [service-tiers](https://docs.claude.com/en/api/service-tiers) for details.

    - `const MessageNewParamsServiceTierAuto MessageNewParamsServiceTier = "auto"`

    - `const MessageNewParamsServiceTierStandardOnly MessageNewParamsServiceTier = "standard_only"`

  - `StopSequences param.Field[[]string]`

    Custom text sequences that will cause the model to stop generating.

    Our models will normally stop when they have naturally completed their turn, which will result in a response `stop_reason` of `"end_turn"`.

    If you want the model to stop generating when it encounters custom strings of text, you can use the `stop_sequences` parameter. If the model encounters one of the custom sequences, the response `stop_reason` value will be `"stop_sequence"` and the response `stop_sequence` value will contain the matched stop sequence.

  - ``

  - `System param.Field[[]TextBlockParamResp]`

    System prompt.

    A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

    - `[]TextBlockParam`

      - `Text string`

      - `Type Text`

        - `const TextText Text = "text"`

      - `CacheControl CacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL CacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

          - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

      - `Citations []TextCitationParamUnionResp`

        - `type CitationCharLocationParamResp struct{…}`

          - `CitedText string`

          - `DocumentIndex int64`

          - `DocumentTitle string`

          - `EndCharIndex int64`

          - `StartCharIndex int64`

          - `Type CharLocation`

            - `const CharLocationCharLocation CharLocation = "char_location"`

        - `type CitationPageLocationParamResp struct{…}`

          - `CitedText string`

          - `DocumentIndex int64`

          - `DocumentTitle string`

          - `EndPageNumber int64`

          - `StartPageNumber int64`

          - `Type PageLocation`

            - `const PageLocationPageLocation PageLocation = "page_location"`

        - `type CitationContentBlockLocationParamResp struct{…}`

          - `CitedText string`

          - `DocumentIndex int64`

          - `DocumentTitle string`

          - `EndBlockIndex int64`

          - `StartBlockIndex int64`

          - `Type ContentBlockLocation`

            - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

        - `type CitationWebSearchResultLocationParamResp struct{…}`

          - `CitedText string`

          - `EncryptedIndex string`

          - `Title string`

          - `Type WebSearchResultLocation`

            - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

          - `URL string`

        - `type CitationSearchResultLocationParamResp struct{…}`

          - `CitedText string`

          - `EndBlockIndex int64`

          - `SearchResultIndex int64`

          - `Source string`

          - `StartBlockIndex int64`

          - `Title string`

          - `Type SearchResultLocation`

            - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

  - `Temperature param.Field[float64]`

    Amount of randomness injected into the response.

    Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.

    Note that even with `temperature` of `0.0`, the results will not be fully deterministic.

  - `Thinking param.Field[ThinkingConfigParamUnionResp]`

    Configuration for enabling Claude's extended thinking.

    When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `ToolChoice param.Field[ToolChoiceUnion]`

    How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `Tools param.Field[[]ToolUnion]`

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

    - `type Tool struct{…}`

      - `InputSchema ToolInputSchema`

        [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

        This defines the shape of the `input` that your tool accepts and that the model will produce.

        - `Type Object`

          - `const ObjectObject Object = "object"`

        - `Properties map[string, any]`

        - `Required []string`

      - `Name string`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

      - `CacheControl CacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL CacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

          - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

      - `Description string`

        Description of what this tool does.

        Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

      - `Type ToolType`

        - `const ToolTypeCustom ToolType = "custom"`

    - `type ToolBash20250124 struct{…}`

      - `Name Bash`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const BashBash Bash = "bash"`

      - `Type Bash20250124`

        - `const Bash20250124Bash20250124 Bash20250124 = "bash_20250124"`

      - `CacheControl CacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL CacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

          - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

    - `type ToolTextEditor20250124 struct{…}`

      - `Name StrReplaceEditor`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const StrReplaceEditorStrReplaceEditor StrReplaceEditor = "str_replace_editor"`

      - `Type TextEditor20250124`

        - `const TextEditor20250124TextEditor20250124 TextEditor20250124 = "text_editor_20250124"`

      - `CacheControl CacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL CacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

          - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

    - `type ToolTextEditor20250429 struct{…}`

      - `Name StrReplaceBasedEditTool`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const StrReplaceBasedEditToolStrReplaceBasedEditTool StrReplaceBasedEditTool = "str_replace_based_edit_tool"`

      - `Type TextEditor20250429`

        - `const TextEditor20250429TextEditor20250429 TextEditor20250429 = "text_editor_20250429"`

      - `CacheControl CacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL CacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

          - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

    - `type ToolTextEditor20250728 struct{…}`

      - `Name StrReplaceBasedEditTool`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const StrReplaceBasedEditToolStrReplaceBasedEditTool StrReplaceBasedEditTool = "str_replace_based_edit_tool"`

      - `Type TextEditor20250728`

        - `const TextEditor20250728TextEditor20250728 TextEditor20250728 = "text_editor_20250728"`

      - `CacheControl CacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL CacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

          - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

      - `MaxCharacters int64`

        Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

    - `type WebSearchTool20250305 struct{…}`

      - `Name WebSearch`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const WebSearchWebSearch WebSearch = "web_search"`

      - `Type WebSearch20250305`

        - `const WebSearch20250305WebSearch20250305 WebSearch20250305 = "web_search_20250305"`

      - `AllowedDomains []string`

        If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

      - `BlockedDomains []string`

        If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

      - `CacheControl CacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL CacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const CacheControlEphemeralTTLTTL5m CacheControlEphemeralTTL = "5m"`

          - `const CacheControlEphemeralTTLTTL1h CacheControlEphemeralTTL = "1h"`

      - `MaxUses int64`

        Maximum number of times the tool can be used in the API request.

      - `UserLocation WebSearchTool20250305UserLocation`

        Parameters for the user's location. Used to provide more relevant search results.

        - `Type Approximate`

          - `const ApproximateApproximate Approximate = "approximate"`

        - `City string`

          The city of the user.

        - `Country string`

          The two letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the user.

        - `Region string`

          The region of the user.

        - `Timezone string`

          The [IANA timezone](https://nodatime.org/TimeZones) of the user.

  - `TopK param.Field[int64]`

    Only sample from the top K options for each subsequent token.

    Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

    Recommended for advanced use cases only. You usually only need to use `temperature`.

  - `TopP param.Field[float64]`

    Use nucleus sampling.

    In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

    Recommended for advanced use cases only. You usually only need to use `temperature`.

### Returns

- `type Message struct{…}`

  - `ID string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `Content []ContentBlockUnion`

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

    - `type TextBlock struct{…}`

      - `Citations []TextCitationUnion`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `type CitationCharLocation struct{…}`

          - `CitedText string`

          - `DocumentIndex int64`

          - `DocumentTitle string`

          - `EndCharIndex int64`

          - `FileID string`

          - `StartCharIndex int64`

          - `Type CharLocation`

            - `const CharLocationCharLocation CharLocation = "char_location"`

        - `type CitationPageLocation struct{…}`

          - `CitedText string`

          - `DocumentIndex int64`

          - `DocumentTitle string`

          - `EndPageNumber int64`

          - `FileID string`

          - `StartPageNumber int64`

          - `Type PageLocation`

            - `const PageLocationPageLocation PageLocation = "page_location"`

        - `type CitationContentBlockLocation struct{…}`

          - `CitedText string`

          - `DocumentIndex int64`

          - `DocumentTitle string`

          - `EndBlockIndex int64`

          - `FileID string`

          - `StartBlockIndex int64`

          - `Type ContentBlockLocation`

            - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

        - `type CitationsWebSearchResultLocation struct{…}`

          - `CitedText string`

          - `EncryptedIndex string`

          - `Title string`

          - `Type WebSearchResultLocation`

            - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

          - `URL string`

        - `type CitationsSearchResultLocation struct{…}`

          - `CitedText string`

          - `EndBlockIndex int64`

          - `SearchResultIndex int64`

          - `Source string`

          - `StartBlockIndex int64`

          - `Title string`

          - `Type SearchResultLocation`

            - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

      - `Text string`

      - `Type Text`

        - `const TextText Text = "text"`

    - `type ThinkingBlock struct{…}`

      - `Signature string`

      - `Thinking string`

      - `Type Thinking`

        - `const ThinkingThinking Thinking = "thinking"`

    - `type RedactedThinkingBlock struct{…}`

      - `Data string`

      - `Type RedactedThinking`

        - `const RedactedThinkingRedactedThinking RedactedThinking = "redacted_thinking"`

    - `type ToolUseBlock struct{…}`

      - `ID string`

      - `Input map[string, any]`

      - `Name string`

      - `Type ToolUse`

        - `const ToolUseToolUse ToolUse = "tool_use"`

    - `type ServerToolUseBlock struct{…}`

      - `ID string`

      - `Input map[string, any]`

      - `Name WebSearch`

        - `const WebSearchWebSearch WebSearch = "web_search"`

      - `Type ServerToolUse`

        - `const ServerToolUseServerToolUse ServerToolUse = "server_tool_use"`

    - `type WebSearchToolResultBlock struct{…}`

      - `Content WebSearchToolResultBlockContentUnion`

        - `type WebSearchToolResultError struct{…}`

          - `ErrorCode WebSearchToolResultErrorErrorCode`

            - `const WebSearchToolResultErrorErrorCodeInvalidToolInput WebSearchToolResultErrorErrorCode = "invalid_tool_input"`

            - `const WebSearchToolResultErrorErrorCodeUnavailable WebSearchToolResultErrorErrorCode = "unavailable"`

            - `const WebSearchToolResultErrorErrorCodeMaxUsesExceeded WebSearchToolResultErrorErrorCode = "max_uses_exceeded"`

            - `const WebSearchToolResultErrorErrorCodeTooManyRequests WebSearchToolResultErrorErrorCode = "too_many_requests"`

            - `const WebSearchToolResultErrorErrorCodeQueryTooLong WebSearchToolResultErrorErrorCode = "query_too_long"`

          - `Type WebSearchToolResultError`

            - `const WebSearchToolResultErrorWebSearchToolResultError WebSearchToolResultError = "web_search_tool_result_error"`

        - `type WebSearchToolResultBlockContentArray []WebSearchResultBlock`

          - `EncryptedContent string`

          - `PageAge string`

          - `Title string`

          - `Type WebSearchResult`

            - `const WebSearchResultWebSearchResult WebSearchResult = "web_search_result"`

          - `URL string`

      - `ToolUseID string`

      - `Type WebSearchToolResult`

        - `const WebSearchToolResultWebSearchToolResult WebSearchToolResult = "web_search_tool_result"`

  - `Model Model`

    The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

    - `type Model string`

      The model that will complete your prompt.

      See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

      - `const ModelClaudeOpus4_5_20251101 Model = "claude-opus-4-5-20251101"`

        Premium model combining maximum intelligence with practical performance

      - `const ModelClaudeOpus4_5 Model = "claude-opus-4-5"`

        Premium model combining maximum intelligence with practical performance

      - `const ModelClaude3_7SonnetLatest Model = "claude-3-7-sonnet-latest"`

        High-performance model with early extended thinking

      - `const ModelClaude3_7Sonnet20250219 Model = "claude-3-7-sonnet-20250219"`

        High-performance model with early extended thinking

      - `const ModelClaude3_5HaikuLatest Model = "claude-3-5-haiku-latest"`

        Fastest and most compact model for near-instant responsiveness

      - `const ModelClaude3_5Haiku20241022 Model = "claude-3-5-haiku-20241022"`

        Our fastest model

      - `const ModelClaudeHaiku4_5 Model = "claude-haiku-4-5"`

        Hybrid model, capable of near-instant responses and extended thinking

      - `const ModelClaudeHaiku4_5_20251001 Model = "claude-haiku-4-5-20251001"`

        Hybrid model, capable of near-instant responses and extended thinking

      - `const ModelClaudeSonnet4_20250514 Model = "claude-sonnet-4-20250514"`

        High-performance model with extended thinking

      - `const ModelClaudeSonnet4_0 Model = "claude-sonnet-4-0"`

        High-performance model with extended thinking

      - `const ModelClaude4Sonnet20250514 Model = "claude-4-sonnet-20250514"`

        High-performance model with extended thinking

      - `const ModelClaudeSonnet4_5 Model = "claude-sonnet-4-5"`

        Our best model for real-world agents and coding

      - `const ModelClaudeSonnet4_5_20250929 Model = "claude-sonnet-4-5-20250929"`

        Our best model for real-world agents and coding

      - `const ModelClaudeOpus4_0 Model = "claude-opus-4-0"`

        Our most capable model

      - `const ModelClaudeOpus4_20250514 Model = "claude-opus-4-20250514"`

        Our most capable model

      - `const ModelClaude4Opus20250514 Model = "claude-4-opus-20250514"`

        Our most capable model

      - `const ModelClaudeOpus4_1_20250805 Model = "claude-opus-4-1-20250805"`

        Our most capable model

      - `const ModelClaude3OpusLatest Model = "claude-3-opus-latest"`

        Excels at writing and complex tasks

      - `const ModelClaude_3_Opus_20240229 Model = "claude-3-opus-20240229"`

        Excels at writing and complex tasks

      - `const ModelClaude_3_Haiku_20240307 Model = "claude-3-haiku-20240307"`

        Our previous most fast and cost-effective

    - `string`

  - `Role Assistant`

    Conversational role of the generated message.

    This will always be `"assistant"`.

    - `const AssistantAssistant Assistant = "assistant"`

  - `StopReason StopReason`

    The reason that we stopped.

    This may be one the following values:

    * `"end_turn"`: the model reached a natural stopping point
    * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
    * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
    * `"tool_use"`: the model invoked one or more tools
    * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
    * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

    In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

    - `const StopReasonEndTurn StopReason = "end_turn"`

    - `const StopReasonMaxTokens StopReason = "max_tokens"`

    - `const StopReasonStopSequence StopReason = "stop_sequence"`

    - `const StopReasonToolUse StopReason = "tool_use"`

    - `const StopReasonPauseTurn StopReason = "pause_turn"`

    - `const StopReasonRefusal StopReason = "refusal"`

  - `StopSequence string`

    Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was generated.

  - `Type Message`

    Object type.

    For Messages, this is always `"message"`.

    - `const MessageMessage Message = "message"`

  - `Usage Usage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `CacheCreation CacheCreation`

      Breakdown of cached tokens by TTL

      - `Ephemeral1hInputTokens int64`

        The number of input tokens used to create the 1 hour cache entry.

      - `Ephemeral5mInputTokens int64`

        The number of input tokens used to create the 5 minute cache entry.

    - `CacheCreationInputTokens int64`

      The number of input tokens used to create the cache entry.

    - `CacheReadInputTokens int64`

      The number of input tokens read from the cache.

    - `InputTokens int64`

      The number of input tokens which were used.

    - `OutputTokens int64`

      The number of output tokens which were used.

    - `ServerToolUse ServerToolUsage`

      The number of server tool requests.

      - `WebSearchRequests int64`

        The number of web search tool requests.

    - `ServiceTier UsageServiceTier`

      If the request used the priority, standard, or batch tier.

      - `const UsageServiceTierStandard UsageServiceTier = "standard"`

      - `const UsageServiceTierPriority UsageServiceTier = "priority"`

      - `const UsageServiceTierBatch UsageServiceTier = "batch"`

### Example

```go
package main

import (
  "context"
  "fmt"

  "github.com/anthropics/anthropic-sdk-go"
  "github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
  client := anthropic.NewClient(
    option.WithAPIKey("my-anthropic-api-key"),
  )
  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    MaxTokens: 1024,
    Messages: []anthropic.MessageParam{anthropic.MessageParam{
      Content: []anthropic.ContentBlockParamUnion{anthropic.ContentBlockParamUnion{
        OfText: &anthropic.TextBlockParam{Text: "What is a quaternion?", CacheControl: anthropic.CacheControlEphemeralParam{TTL: anthropic.CacheControlEphemeralTTLTTL5m}, Citations: []anthropic.TextCitationParamUnion{anthropic.TextCitationParamUnion{
          OfCharLocation: &anthropic.CitationCharLocationParam{CitedText: "cited_text", DocumentIndex: 0, DocumentTitle: anthropic.String("x"), EndCharIndex: 0, StartCharIndex: 0},
        }}},
      }},
      Role: anthropic.MessageParamRoleUser,
    }},
    Model: anthropic.ModelClaudeOpus4_5_20251101,
  })
  if err != nil {
    panic(err.Error())
  }
  fmt.Printf("%+v\n", message.ID)
}
```
