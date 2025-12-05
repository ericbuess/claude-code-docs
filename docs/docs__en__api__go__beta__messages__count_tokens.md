## Count Tokens

`client.Beta.Messages.CountTokens(ctx, params) (*BetaMessageTokensCount, error)`

**post** `/v1/messages/count_tokens`

Count the number of tokens in a Message.

The Token Count API can be used to count the number of tokens in a Message, including tools, images, and documents, without creating it.

Learn more about token counting in our [user guide](https://docs.claude.com/en/docs/build-with-claude/token-counting)

### Parameters

- `params BetaMessageCountTokensParams`

  - `Messages param.Field[[]BetaMessageParamResp]`

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

    - `Content []BetaContentBlockParamUnionResp`

      - `[]BetaContentBlockParamUnionResp`

        - `type BetaTextBlockParamResp struct{…}`

          - `Text string`

          - `Type Text`

            - `const TextText Text = "text"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

          - `Citations []BetaTextCitationParamUnionResp`

            - `type BetaCitationCharLocationParamResp struct{…}`

              - `CitedText string`

              - `DocumentIndex int64`

              - `DocumentTitle string`

              - `EndCharIndex int64`

              - `StartCharIndex int64`

              - `Type CharLocation`

                - `const CharLocationCharLocation CharLocation = "char_location"`

            - `type BetaCitationPageLocationParamResp struct{…}`

              - `CitedText string`

              - `DocumentIndex int64`

              - `DocumentTitle string`

              - `EndPageNumber int64`

              - `StartPageNumber int64`

              - `Type PageLocation`

                - `const PageLocationPageLocation PageLocation = "page_location"`

            - `type BetaCitationContentBlockLocationParamResp struct{…}`

              - `CitedText string`

              - `DocumentIndex int64`

              - `DocumentTitle string`

              - `EndBlockIndex int64`

              - `StartBlockIndex int64`

              - `Type ContentBlockLocation`

                - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

            - `type BetaCitationWebSearchResultLocationParamResp struct{…}`

              - `CitedText string`

              - `EncryptedIndex string`

              - `Title string`

              - `Type WebSearchResultLocation`

                - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

              - `URL string`

            - `type BetaCitationSearchResultLocationParamResp struct{…}`

              - `CitedText string`

              - `EndBlockIndex int64`

              - `SearchResultIndex int64`

              - `Source string`

              - `StartBlockIndex int64`

              - `Title string`

              - `Type SearchResultLocation`

                - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

        - `type BetaImageBlockParamResp struct{…}`

          - `Source BetaImageBlockParamSourceUnionResp`

            - `type BetaBase64ImageSource struct{…}`

              - `Data string`

              - `MediaType BetaBase64ImageSourceMediaType`

                - `const BetaBase64ImageSourceMediaTypeImageJPEG BetaBase64ImageSourceMediaType = "image/jpeg"`

                - `const BetaBase64ImageSourceMediaTypeImagePNG BetaBase64ImageSourceMediaType = "image/png"`

                - `const BetaBase64ImageSourceMediaTypeImageGIF BetaBase64ImageSourceMediaType = "image/gif"`

                - `const BetaBase64ImageSourceMediaTypeImageWebP BetaBase64ImageSourceMediaType = "image/webp"`

              - `Type Base64`

                - `const Base64Base64 Base64 = "base64"`

            - `type BetaURLImageSource struct{…}`

              - `Type URL`

                - `const URLURL URL = "url"`

              - `URL string`

            - `type BetaFileImageSource struct{…}`

              - `FileID string`

              - `Type File`

                - `const FileFile File = "file"`

          - `Type Image`

            - `const ImageImage Image = "image"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

        - `type BetaRequestDocumentBlock struct{…}`

          - `Source BetaRequestDocumentBlockSourceUnion`

            - `type BetaBase64PDFSource struct{…}`

              - `Data string`

              - `MediaType ApplicationPDF`

                - `const ApplicationPDFApplicationPDF ApplicationPDF = "application/pdf"`

              - `Type Base64`

                - `const Base64Base64 Base64 = "base64"`

            - `type BetaPlainTextSource struct{…}`

              - `Data string`

              - `MediaType TextPlain`

                - `const TextPlainTextPlain TextPlain = "text/plain"`

              - `Type Text`

                - `const TextText Text = "text"`

            - `type BetaContentBlockSource struct{…}`

              - `Content BetaContentBlockSourceContentUnion`

                - `string`

                - `[]BetaContentBlockSourceContentUnion`

                  - `type BetaTextBlockParamResp struct{…}`

                    - `Text string`

                    - `Type Text`

                      - `const TextText Text = "text"`

                    - `CacheControl BetaCacheControlEphemeral`

                      Create a cache control breakpoint at this content block.

                      - `Type Ephemeral`

                        - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                      - `TTL BetaCacheControlEphemeralTTL`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                        - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

                    - `Citations []BetaTextCitationParamUnionResp`

                      - `type BetaCitationCharLocationParamResp struct{…}`

                        - `CitedText string`

                        - `DocumentIndex int64`

                        - `DocumentTitle string`

                        - `EndCharIndex int64`

                        - `StartCharIndex int64`

                        - `Type CharLocation`

                          - `const CharLocationCharLocation CharLocation = "char_location"`

                      - `type BetaCitationPageLocationParamResp struct{…}`

                        - `CitedText string`

                        - `DocumentIndex int64`

                        - `DocumentTitle string`

                        - `EndPageNumber int64`

                        - `StartPageNumber int64`

                        - `Type PageLocation`

                          - `const PageLocationPageLocation PageLocation = "page_location"`

                      - `type BetaCitationContentBlockLocationParamResp struct{…}`

                        - `CitedText string`

                        - `DocumentIndex int64`

                        - `DocumentTitle string`

                        - `EndBlockIndex int64`

                        - `StartBlockIndex int64`

                        - `Type ContentBlockLocation`

                          - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

                      - `type BetaCitationWebSearchResultLocationParamResp struct{…}`

                        - `CitedText string`

                        - `EncryptedIndex string`

                        - `Title string`

                        - `Type WebSearchResultLocation`

                          - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

                        - `URL string`

                      - `type BetaCitationSearchResultLocationParamResp struct{…}`

                        - `CitedText string`

                        - `EndBlockIndex int64`

                        - `SearchResultIndex int64`

                        - `Source string`

                        - `StartBlockIndex int64`

                        - `Title string`

                        - `Type SearchResultLocation`

                          - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

                  - `type BetaImageBlockParamResp struct{…}`

                    - `Source BetaImageBlockParamSourceUnionResp`

                      - `type BetaBase64ImageSource struct{…}`

                        - `Data string`

                        - `MediaType BetaBase64ImageSourceMediaType`

                          - `const BetaBase64ImageSourceMediaTypeImageJPEG BetaBase64ImageSourceMediaType = "image/jpeg"`

                          - `const BetaBase64ImageSourceMediaTypeImagePNG BetaBase64ImageSourceMediaType = "image/png"`

                          - `const BetaBase64ImageSourceMediaTypeImageGIF BetaBase64ImageSourceMediaType = "image/gif"`

                          - `const BetaBase64ImageSourceMediaTypeImageWebP BetaBase64ImageSourceMediaType = "image/webp"`

                        - `Type Base64`

                          - `const Base64Base64 Base64 = "base64"`

                      - `type BetaURLImageSource struct{…}`

                        - `Type URL`

                          - `const URLURL URL = "url"`

                        - `URL string`

                      - `type BetaFileImageSource struct{…}`

                        - `FileID string`

                        - `Type File`

                          - `const FileFile File = "file"`

                    - `Type Image`

                      - `const ImageImage Image = "image"`

                    - `CacheControl BetaCacheControlEphemeral`

                      Create a cache control breakpoint at this content block.

                      - `Type Ephemeral`

                        - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                      - `TTL BetaCacheControlEphemeralTTL`

                        The time-to-live for the cache control breakpoint.

                        This may be one the following values:

                        - `5m`: 5 minutes
                        - `1h`: 1 hour

                        Defaults to `5m`.

                        - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                        - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

              - `Type Content`

                - `const ContentContent Content = "content"`

            - `type BetaURLPDFSource struct{…}`

              - `Type URL`

                - `const URLURL URL = "url"`

              - `URL string`

            - `type BetaFileDocumentSource struct{…}`

              - `FileID string`

              - `Type File`

                - `const FileFile File = "file"`

          - `Type Document`

            - `const DocumentDocument Document = "document"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

          - `Citations BetaCitationsConfigParamResp`

            - `Enabled bool`

          - `Context string`

          - `Title string`

        - `type BetaSearchResultBlockParamResp struct{…}`

          - `Content []BetaTextBlockParamResp`

            - `Text string`

            - `Type Text`

              - `const TextText Text = "text"`

            - `CacheControl BetaCacheControlEphemeral`

              Create a cache control breakpoint at this content block.

              - `Type Ephemeral`

                - `const EphemeralEphemeral Ephemeral = "ephemeral"`

              - `TTL BetaCacheControlEphemeralTTL`

                The time-to-live for the cache control breakpoint.

                This may be one the following values:

                - `5m`: 5 minutes
                - `1h`: 1 hour

                Defaults to `5m`.

                - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

            - `Citations []BetaTextCitationParamUnionResp`

              - `type BetaCitationCharLocationParamResp struct{…}`

                - `CitedText string`

                - `DocumentIndex int64`

                - `DocumentTitle string`

                - `EndCharIndex int64`

                - `StartCharIndex int64`

                - `Type CharLocation`

                  - `const CharLocationCharLocation CharLocation = "char_location"`

              - `type BetaCitationPageLocationParamResp struct{…}`

                - `CitedText string`

                - `DocumentIndex int64`

                - `DocumentTitle string`

                - `EndPageNumber int64`

                - `StartPageNumber int64`

                - `Type PageLocation`

                  - `const PageLocationPageLocation PageLocation = "page_location"`

              - `type BetaCitationContentBlockLocationParamResp struct{…}`

                - `CitedText string`

                - `DocumentIndex int64`

                - `DocumentTitle string`

                - `EndBlockIndex int64`

                - `StartBlockIndex int64`

                - `Type ContentBlockLocation`

                  - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

              - `type BetaCitationWebSearchResultLocationParamResp struct{…}`

                - `CitedText string`

                - `EncryptedIndex string`

                - `Title string`

                - `Type WebSearchResultLocation`

                  - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

                - `URL string`

              - `type BetaCitationSearchResultLocationParamResp struct{…}`

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

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

          - `Citations BetaCitationsConfigParamResp`

            - `Enabled bool`

        - `type BetaThinkingBlockParamResp struct{…}`

          - `Signature string`

          - `Thinking string`

          - `Type Thinking`

            - `const ThinkingThinking Thinking = "thinking"`

        - `type BetaRedactedThinkingBlockParamResp struct{…}`

          - `Data string`

          - `Type RedactedThinking`

            - `const RedactedThinkingRedactedThinking RedactedThinking = "redacted_thinking"`

        - `type BetaToolUseBlockParamResp struct{…}`

          - `ID string`

          - `Input map[string, any]`

          - `Name string`

          - `Type ToolUse`

            - `const ToolUseToolUse ToolUse = "tool_use"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

          - `Caller BetaToolUseBlockParamCallerUnionResp`

            Tool invocation directly from the model.

            - `type BetaDirectCaller struct{…}`

              Tool invocation directly from the model.

              - `Type Direct`

                - `const DirectDirect Direct = "direct"`

            - `type BetaServerToolCaller struct{…}`

              Tool invocation generated by a server-side tool.

              - `ToolID string`

              - `Type CodeExecution20250825`

                - `const CodeExecution20250825CodeExecution20250825 CodeExecution20250825 = "code_execution_20250825"`

        - `type BetaToolResultBlockParamResp struct{…}`

          - `ToolUseID string`

          - `Type ToolResult`

            - `const ToolResultToolResult ToolResult = "tool_result"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

          - `Content []BetaToolResultBlockParamContentUnionResp`

            - `[]BetaToolResultBlockParamContentUnionResp`

              - `type BetaTextBlockParamResp struct{…}`

                - `Text string`

                - `Type Text`

                  - `const TextText Text = "text"`

                - `CacheControl BetaCacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `Type Ephemeral`

                    - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                  - `TTL BetaCacheControlEphemeralTTL`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                    - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

                - `Citations []BetaTextCitationParamUnionResp`

                  - `type BetaCitationCharLocationParamResp struct{…}`

                    - `CitedText string`

                    - `DocumentIndex int64`

                    - `DocumentTitle string`

                    - `EndCharIndex int64`

                    - `StartCharIndex int64`

                    - `Type CharLocation`

                      - `const CharLocationCharLocation CharLocation = "char_location"`

                  - `type BetaCitationPageLocationParamResp struct{…}`

                    - `CitedText string`

                    - `DocumentIndex int64`

                    - `DocumentTitle string`

                    - `EndPageNumber int64`

                    - `StartPageNumber int64`

                    - `Type PageLocation`

                      - `const PageLocationPageLocation PageLocation = "page_location"`

                  - `type BetaCitationContentBlockLocationParamResp struct{…}`

                    - `CitedText string`

                    - `DocumentIndex int64`

                    - `DocumentTitle string`

                    - `EndBlockIndex int64`

                    - `StartBlockIndex int64`

                    - `Type ContentBlockLocation`

                      - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

                  - `type BetaCitationWebSearchResultLocationParamResp struct{…}`

                    - `CitedText string`

                    - `EncryptedIndex string`

                    - `Title string`

                    - `Type WebSearchResultLocation`

                      - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

                    - `URL string`

                  - `type BetaCitationSearchResultLocationParamResp struct{…}`

                    - `CitedText string`

                    - `EndBlockIndex int64`

                    - `SearchResultIndex int64`

                    - `Source string`

                    - `StartBlockIndex int64`

                    - `Title string`

                    - `Type SearchResultLocation`

                      - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

              - `type BetaImageBlockParamResp struct{…}`

                - `Source BetaImageBlockParamSourceUnionResp`

                  - `type BetaBase64ImageSource struct{…}`

                    - `Data string`

                    - `MediaType BetaBase64ImageSourceMediaType`

                      - `const BetaBase64ImageSourceMediaTypeImageJPEG BetaBase64ImageSourceMediaType = "image/jpeg"`

                      - `const BetaBase64ImageSourceMediaTypeImagePNG BetaBase64ImageSourceMediaType = "image/png"`

                      - `const BetaBase64ImageSourceMediaTypeImageGIF BetaBase64ImageSourceMediaType = "image/gif"`

                      - `const BetaBase64ImageSourceMediaTypeImageWebP BetaBase64ImageSourceMediaType = "image/webp"`

                    - `Type Base64`

                      - `const Base64Base64 Base64 = "base64"`

                  - `type BetaURLImageSource struct{…}`

                    - `Type URL`

                      - `const URLURL URL = "url"`

                    - `URL string`

                  - `type BetaFileImageSource struct{…}`

                    - `FileID string`

                    - `Type File`

                      - `const FileFile File = "file"`

                - `Type Image`

                  - `const ImageImage Image = "image"`

                - `CacheControl BetaCacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `Type Ephemeral`

                    - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                  - `TTL BetaCacheControlEphemeralTTL`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                    - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

              - `type BetaSearchResultBlockParamResp struct{…}`

                - `Content []BetaTextBlockParamResp`

                  - `Text string`

                  - `Type Text`

                    - `const TextText Text = "text"`

                  - `CacheControl BetaCacheControlEphemeral`

                    Create a cache control breakpoint at this content block.

                    - `Type Ephemeral`

                      - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                    - `TTL BetaCacheControlEphemeralTTL`

                      The time-to-live for the cache control breakpoint.

                      This may be one the following values:

                      - `5m`: 5 minutes
                      - `1h`: 1 hour

                      Defaults to `5m`.

                      - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                      - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

                  - `Citations []BetaTextCitationParamUnionResp`

                    - `type BetaCitationCharLocationParamResp struct{…}`

                      - `CitedText string`

                      - `DocumentIndex int64`

                      - `DocumentTitle string`

                      - `EndCharIndex int64`

                      - `StartCharIndex int64`

                      - `Type CharLocation`

                        - `const CharLocationCharLocation CharLocation = "char_location"`

                    - `type BetaCitationPageLocationParamResp struct{…}`

                      - `CitedText string`

                      - `DocumentIndex int64`

                      - `DocumentTitle string`

                      - `EndPageNumber int64`

                      - `StartPageNumber int64`

                      - `Type PageLocation`

                        - `const PageLocationPageLocation PageLocation = "page_location"`

                    - `type BetaCitationContentBlockLocationParamResp struct{…}`

                      - `CitedText string`

                      - `DocumentIndex int64`

                      - `DocumentTitle string`

                      - `EndBlockIndex int64`

                      - `StartBlockIndex int64`

                      - `Type ContentBlockLocation`

                        - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

                    - `type BetaCitationWebSearchResultLocationParamResp struct{…}`

                      - `CitedText string`

                      - `EncryptedIndex string`

                      - `Title string`

                      - `Type WebSearchResultLocation`

                        - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

                      - `URL string`

                    - `type BetaCitationSearchResultLocationParamResp struct{…}`

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

                - `CacheControl BetaCacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `Type Ephemeral`

                    - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                  - `TTL BetaCacheControlEphemeralTTL`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                    - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

                - `Citations BetaCitationsConfigParamResp`

                  - `Enabled bool`

              - `type BetaRequestDocumentBlock struct{…}`

                - `Source BetaRequestDocumentBlockSourceUnion`

                  - `type BetaBase64PDFSource struct{…}`

                    - `Data string`

                    - `MediaType ApplicationPDF`

                      - `const ApplicationPDFApplicationPDF ApplicationPDF = "application/pdf"`

                    - `Type Base64`

                      - `const Base64Base64 Base64 = "base64"`

                  - `type BetaPlainTextSource struct{…}`

                    - `Data string`

                    - `MediaType TextPlain`

                      - `const TextPlainTextPlain TextPlain = "text/plain"`

                    - `Type Text`

                      - `const TextText Text = "text"`

                  - `type BetaContentBlockSource struct{…}`

                    - `Content BetaContentBlockSourceContentUnion`

                      - `string`

                      - `[]BetaContentBlockSourceContentUnion`

                        - `type BetaTextBlockParamResp struct{…}`

                          - `Text string`

                          - `Type Text`

                            - `const TextText Text = "text"`

                          - `CacheControl BetaCacheControlEphemeral`

                            Create a cache control breakpoint at this content block.

                            - `Type Ephemeral`

                              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                            - `TTL BetaCacheControlEphemeralTTL`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

                          - `Citations []BetaTextCitationParamUnionResp`

                            - `type BetaCitationCharLocationParamResp struct{…}`

                              - `CitedText string`

                              - `DocumentIndex int64`

                              - `DocumentTitle string`

                              - `EndCharIndex int64`

                              - `StartCharIndex int64`

                              - `Type CharLocation`

                                - `const CharLocationCharLocation CharLocation = "char_location"`

                            - `type BetaCitationPageLocationParamResp struct{…}`

                              - `CitedText string`

                              - `DocumentIndex int64`

                              - `DocumentTitle string`

                              - `EndPageNumber int64`

                              - `StartPageNumber int64`

                              - `Type PageLocation`

                                - `const PageLocationPageLocation PageLocation = "page_location"`

                            - `type BetaCitationContentBlockLocationParamResp struct{…}`

                              - `CitedText string`

                              - `DocumentIndex int64`

                              - `DocumentTitle string`

                              - `EndBlockIndex int64`

                              - `StartBlockIndex int64`

                              - `Type ContentBlockLocation`

                                - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

                            - `type BetaCitationWebSearchResultLocationParamResp struct{…}`

                              - `CitedText string`

                              - `EncryptedIndex string`

                              - `Title string`

                              - `Type WebSearchResultLocation`

                                - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

                              - `URL string`

                            - `type BetaCitationSearchResultLocationParamResp struct{…}`

                              - `CitedText string`

                              - `EndBlockIndex int64`

                              - `SearchResultIndex int64`

                              - `Source string`

                              - `StartBlockIndex int64`

                              - `Title string`

                              - `Type SearchResultLocation`

                                - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

                        - `type BetaImageBlockParamResp struct{…}`

                          - `Source BetaImageBlockParamSourceUnionResp`

                            - `type BetaBase64ImageSource struct{…}`

                              - `Data string`

                              - `MediaType BetaBase64ImageSourceMediaType`

                                - `const BetaBase64ImageSourceMediaTypeImageJPEG BetaBase64ImageSourceMediaType = "image/jpeg"`

                                - `const BetaBase64ImageSourceMediaTypeImagePNG BetaBase64ImageSourceMediaType = "image/png"`

                                - `const BetaBase64ImageSourceMediaTypeImageGIF BetaBase64ImageSourceMediaType = "image/gif"`

                                - `const BetaBase64ImageSourceMediaTypeImageWebP BetaBase64ImageSourceMediaType = "image/webp"`

                              - `Type Base64`

                                - `const Base64Base64 Base64 = "base64"`

                            - `type BetaURLImageSource struct{…}`

                              - `Type URL`

                                - `const URLURL URL = "url"`

                              - `URL string`

                            - `type BetaFileImageSource struct{…}`

                              - `FileID string`

                              - `Type File`

                                - `const FileFile File = "file"`

                          - `Type Image`

                            - `const ImageImage Image = "image"`

                          - `CacheControl BetaCacheControlEphemeral`

                            Create a cache control breakpoint at this content block.

                            - `Type Ephemeral`

                              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                            - `TTL BetaCacheControlEphemeralTTL`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

                    - `Type Content`

                      - `const ContentContent Content = "content"`

                  - `type BetaURLPDFSource struct{…}`

                    - `Type URL`

                      - `const URLURL URL = "url"`

                    - `URL string`

                  - `type BetaFileDocumentSource struct{…}`

                    - `FileID string`

                    - `Type File`

                      - `const FileFile File = "file"`

                - `Type Document`

                  - `const DocumentDocument Document = "document"`

                - `CacheControl BetaCacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `Type Ephemeral`

                    - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                  - `TTL BetaCacheControlEphemeralTTL`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                    - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

                - `Citations BetaCitationsConfigParamResp`

                  - `Enabled bool`

                - `Context string`

                - `Title string`

              - `type BetaToolReferenceBlockParamResp struct{…}`

                Tool reference block that can be included in tool_result content.

                - `ToolName string`

                - `Type ToolReference`

                  - `const ToolReferenceToolReference ToolReference = "tool_reference"`

                - `CacheControl BetaCacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `Type Ephemeral`

                    - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                  - `TTL BetaCacheControlEphemeralTTL`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                    - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

          - `IsError bool`

        - `type BetaServerToolUseBlockParamResp struct{…}`

          - `ID string`

          - `Input map[string, any]`

          - `Name BetaServerToolUseBlockParamName`

            - `const BetaServerToolUseBlockParamNameWebSearch BetaServerToolUseBlockParamName = "web_search"`

            - `const BetaServerToolUseBlockParamNameWebFetch BetaServerToolUseBlockParamName = "web_fetch"`

            - `const BetaServerToolUseBlockParamNameCodeExecution BetaServerToolUseBlockParamName = "code_execution"`

            - `const BetaServerToolUseBlockParamNameBashCodeExecution BetaServerToolUseBlockParamName = "bash_code_execution"`

            - `const BetaServerToolUseBlockParamNameTextEditorCodeExecution BetaServerToolUseBlockParamName = "text_editor_code_execution"`

            - `const BetaServerToolUseBlockParamNameToolSearchToolRegex BetaServerToolUseBlockParamName = "tool_search_tool_regex"`

            - `const BetaServerToolUseBlockParamNameToolSearchToolBm25 BetaServerToolUseBlockParamName = "tool_search_tool_bm25"`

          - `Type ServerToolUse`

            - `const ServerToolUseServerToolUse ServerToolUse = "server_tool_use"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

          - `Caller BetaServerToolUseBlockParamCallerUnionResp`

            Tool invocation directly from the model.

            - `type BetaDirectCaller struct{…}`

              Tool invocation directly from the model.

              - `Type Direct`

                - `const DirectDirect Direct = "direct"`

            - `type BetaServerToolCaller struct{…}`

              Tool invocation generated by a server-side tool.

              - `ToolID string`

              - `Type CodeExecution20250825`

                - `const CodeExecution20250825CodeExecution20250825 CodeExecution20250825 = "code_execution_20250825"`

        - `type BetaWebSearchToolResultBlockParamResp struct{…}`

          - `Content BetaWebSearchToolResultBlockParamContentUnionResp`

            - `[]BetaWebSearchResultBlockParamResp`

              - `EncryptedContent string`

              - `Title string`

              - `Type WebSearchResult`

                - `const WebSearchResultWebSearchResult WebSearchResult = "web_search_result"`

              - `URL string`

              - `PageAge string`

            - `type BetaWebSearchToolRequestError struct{…}`

              - `ErrorCode BetaWebSearchToolResultErrorCode`

                - `const BetaWebSearchToolResultErrorCodeInvalidToolInput BetaWebSearchToolResultErrorCode = "invalid_tool_input"`

                - `const BetaWebSearchToolResultErrorCodeUnavailable BetaWebSearchToolResultErrorCode = "unavailable"`

                - `const BetaWebSearchToolResultErrorCodeMaxUsesExceeded BetaWebSearchToolResultErrorCode = "max_uses_exceeded"`

                - `const BetaWebSearchToolResultErrorCodeTooManyRequests BetaWebSearchToolResultErrorCode = "too_many_requests"`

                - `const BetaWebSearchToolResultErrorCodeQueryTooLong BetaWebSearchToolResultErrorCode = "query_too_long"`

              - `Type WebSearchToolResultError`

                - `const WebSearchToolResultErrorWebSearchToolResultError WebSearchToolResultError = "web_search_tool_result_error"`

          - `ToolUseID string`

          - `Type WebSearchToolResult`

            - `const WebSearchToolResultWebSearchToolResult WebSearchToolResult = "web_search_tool_result"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

        - `type BetaWebFetchToolResultBlockParamResp struct{…}`

          - `Content BetaWebFetchToolResultBlockParamContentUnionResp`

            - `type BetaWebFetchToolResultErrorBlockParamResp struct{…}`

              - `ErrorCode BetaWebFetchToolResultErrorCode`

                - `const BetaWebFetchToolResultErrorCodeInvalidToolInput BetaWebFetchToolResultErrorCode = "invalid_tool_input"`

                - `const BetaWebFetchToolResultErrorCodeURLTooLong BetaWebFetchToolResultErrorCode = "url_too_long"`

                - `const BetaWebFetchToolResultErrorCodeURLNotAllowed BetaWebFetchToolResultErrorCode = "url_not_allowed"`

                - `const BetaWebFetchToolResultErrorCodeURLNotAccessible BetaWebFetchToolResultErrorCode = "url_not_accessible"`

                - `const BetaWebFetchToolResultErrorCodeUnsupportedContentType BetaWebFetchToolResultErrorCode = "unsupported_content_type"`

                - `const BetaWebFetchToolResultErrorCodeTooManyRequests BetaWebFetchToolResultErrorCode = "too_many_requests"`

                - `const BetaWebFetchToolResultErrorCodeMaxUsesExceeded BetaWebFetchToolResultErrorCode = "max_uses_exceeded"`

                - `const BetaWebFetchToolResultErrorCodeUnavailable BetaWebFetchToolResultErrorCode = "unavailable"`

              - `Type WebFetchToolResultError`

                - `const WebFetchToolResultErrorWebFetchToolResultError WebFetchToolResultError = "web_fetch_tool_result_error"`

            - `type BetaWebFetchBlockParamResp struct{…}`

              - `Content BetaRequestDocumentBlock`

                - `Source BetaRequestDocumentBlockSourceUnion`

                  - `type BetaBase64PDFSource struct{…}`

                    - `Data string`

                    - `MediaType ApplicationPDF`

                      - `const ApplicationPDFApplicationPDF ApplicationPDF = "application/pdf"`

                    - `Type Base64`

                      - `const Base64Base64 Base64 = "base64"`

                  - `type BetaPlainTextSource struct{…}`

                    - `Data string`

                    - `MediaType TextPlain`

                      - `const TextPlainTextPlain TextPlain = "text/plain"`

                    - `Type Text`

                      - `const TextText Text = "text"`

                  - `type BetaContentBlockSource struct{…}`

                    - `Content BetaContentBlockSourceContentUnion`

                      - `string`

                      - `[]BetaContentBlockSourceContentUnion`

                        - `type BetaTextBlockParamResp struct{…}`

                          - `Text string`

                          - `Type Text`

                            - `const TextText Text = "text"`

                          - `CacheControl BetaCacheControlEphemeral`

                            Create a cache control breakpoint at this content block.

                            - `Type Ephemeral`

                              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                            - `TTL BetaCacheControlEphemeralTTL`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

                          - `Citations []BetaTextCitationParamUnionResp`

                            - `type BetaCitationCharLocationParamResp struct{…}`

                              - `CitedText string`

                              - `DocumentIndex int64`

                              - `DocumentTitle string`

                              - `EndCharIndex int64`

                              - `StartCharIndex int64`

                              - `Type CharLocation`

                                - `const CharLocationCharLocation CharLocation = "char_location"`

                            - `type BetaCitationPageLocationParamResp struct{…}`

                              - `CitedText string`

                              - `DocumentIndex int64`

                              - `DocumentTitle string`

                              - `EndPageNumber int64`

                              - `StartPageNumber int64`

                              - `Type PageLocation`

                                - `const PageLocationPageLocation PageLocation = "page_location"`

                            - `type BetaCitationContentBlockLocationParamResp struct{…}`

                              - `CitedText string`

                              - `DocumentIndex int64`

                              - `DocumentTitle string`

                              - `EndBlockIndex int64`

                              - `StartBlockIndex int64`

                              - `Type ContentBlockLocation`

                                - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

                            - `type BetaCitationWebSearchResultLocationParamResp struct{…}`

                              - `CitedText string`

                              - `EncryptedIndex string`

                              - `Title string`

                              - `Type WebSearchResultLocation`

                                - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

                              - `URL string`

                            - `type BetaCitationSearchResultLocationParamResp struct{…}`

                              - `CitedText string`

                              - `EndBlockIndex int64`

                              - `SearchResultIndex int64`

                              - `Source string`

                              - `StartBlockIndex int64`

                              - `Title string`

                              - `Type SearchResultLocation`

                                - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

                        - `type BetaImageBlockParamResp struct{…}`

                          - `Source BetaImageBlockParamSourceUnionResp`

                            - `type BetaBase64ImageSource struct{…}`

                              - `Data string`

                              - `MediaType BetaBase64ImageSourceMediaType`

                                - `const BetaBase64ImageSourceMediaTypeImageJPEG BetaBase64ImageSourceMediaType = "image/jpeg"`

                                - `const BetaBase64ImageSourceMediaTypeImagePNG BetaBase64ImageSourceMediaType = "image/png"`

                                - `const BetaBase64ImageSourceMediaTypeImageGIF BetaBase64ImageSourceMediaType = "image/gif"`

                                - `const BetaBase64ImageSourceMediaTypeImageWebP BetaBase64ImageSourceMediaType = "image/webp"`

                              - `Type Base64`

                                - `const Base64Base64 Base64 = "base64"`

                            - `type BetaURLImageSource struct{…}`

                              - `Type URL`

                                - `const URLURL URL = "url"`

                              - `URL string`

                            - `type BetaFileImageSource struct{…}`

                              - `FileID string`

                              - `Type File`

                                - `const FileFile File = "file"`

                          - `Type Image`

                            - `const ImageImage Image = "image"`

                          - `CacheControl BetaCacheControlEphemeral`

                            Create a cache control breakpoint at this content block.

                            - `Type Ephemeral`

                              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                            - `TTL BetaCacheControlEphemeralTTL`

                              The time-to-live for the cache control breakpoint.

                              This may be one the following values:

                              - `5m`: 5 minutes
                              - `1h`: 1 hour

                              Defaults to `5m`.

                              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

                    - `Type Content`

                      - `const ContentContent Content = "content"`

                  - `type BetaURLPDFSource struct{…}`

                    - `Type URL`

                      - `const URLURL URL = "url"`

                    - `URL string`

                  - `type BetaFileDocumentSource struct{…}`

                    - `FileID string`

                    - `Type File`

                      - `const FileFile File = "file"`

                - `Type Document`

                  - `const DocumentDocument Document = "document"`

                - `CacheControl BetaCacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `Type Ephemeral`

                    - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                  - `TTL BetaCacheControlEphemeralTTL`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                    - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

                - `Citations BetaCitationsConfigParamResp`

                  - `Enabled bool`

                - `Context string`

                - `Title string`

              - `Type WebFetchResult`

                - `const WebFetchResultWebFetchResult WebFetchResult = "web_fetch_result"`

              - `URL string`

                Fetched content URL

              - `RetrievedAt string`

                ISO 8601 timestamp when the content was retrieved

          - `ToolUseID string`

          - `Type WebFetchToolResult`

            - `const WebFetchToolResultWebFetchToolResult WebFetchToolResult = "web_fetch_tool_result"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

        - `type BetaCodeExecutionToolResultBlockParamResp struct{…}`

          - `Content BetaCodeExecutionToolResultBlockParamContentUnionResp`

            - `type BetaCodeExecutionToolResultErrorParamResp struct{…}`

              - `ErrorCode BetaCodeExecutionToolResultErrorCode`

                - `const BetaCodeExecutionToolResultErrorCodeInvalidToolInput BetaCodeExecutionToolResultErrorCode = "invalid_tool_input"`

                - `const BetaCodeExecutionToolResultErrorCodeUnavailable BetaCodeExecutionToolResultErrorCode = "unavailable"`

                - `const BetaCodeExecutionToolResultErrorCodeTooManyRequests BetaCodeExecutionToolResultErrorCode = "too_many_requests"`

                - `const BetaCodeExecutionToolResultErrorCodeExecutionTimeExceeded BetaCodeExecutionToolResultErrorCode = "execution_time_exceeded"`

              - `Type CodeExecutionToolResultError`

                - `const CodeExecutionToolResultErrorCodeExecutionToolResultError CodeExecutionToolResultError = "code_execution_tool_result_error"`

            - `type BetaCodeExecutionResultBlockParamResp struct{…}`

              - `Content []BetaCodeExecutionOutputBlockParamResp`

                - `FileID string`

                - `Type CodeExecutionOutput`

                  - `const CodeExecutionOutputCodeExecutionOutput CodeExecutionOutput = "code_execution_output"`

              - `ReturnCode int64`

              - `Stderr string`

              - `Stdout string`

              - `Type CodeExecutionResult`

                - `const CodeExecutionResultCodeExecutionResult CodeExecutionResult = "code_execution_result"`

          - `ToolUseID string`

          - `Type CodeExecutionToolResult`

            - `const CodeExecutionToolResultCodeExecutionToolResult CodeExecutionToolResult = "code_execution_tool_result"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

        - `type BetaBashCodeExecutionToolResultBlockParamResp struct{…}`

          - `Content BetaBashCodeExecutionToolResultBlockParamContentUnionResp`

            - `type BetaBashCodeExecutionToolResultErrorParamResp struct{…}`

              - `ErrorCode BetaBashCodeExecutionToolResultErrorParamErrorCode`

                - `const BetaBashCodeExecutionToolResultErrorParamErrorCodeInvalidToolInput BetaBashCodeExecutionToolResultErrorParamErrorCode = "invalid_tool_input"`

                - `const BetaBashCodeExecutionToolResultErrorParamErrorCodeUnavailable BetaBashCodeExecutionToolResultErrorParamErrorCode = "unavailable"`

                - `const BetaBashCodeExecutionToolResultErrorParamErrorCodeTooManyRequests BetaBashCodeExecutionToolResultErrorParamErrorCode = "too_many_requests"`

                - `const BetaBashCodeExecutionToolResultErrorParamErrorCodeExecutionTimeExceeded BetaBashCodeExecutionToolResultErrorParamErrorCode = "execution_time_exceeded"`

                - `const BetaBashCodeExecutionToolResultErrorParamErrorCodeOutputFileTooLarge BetaBashCodeExecutionToolResultErrorParamErrorCode = "output_file_too_large"`

              - `Type BashCodeExecutionToolResultError`

                - `const BashCodeExecutionToolResultErrorBashCodeExecutionToolResultError BashCodeExecutionToolResultError = "bash_code_execution_tool_result_error"`

            - `type BetaBashCodeExecutionResultBlockParamResp struct{…}`

              - `Content []BetaBashCodeExecutionOutputBlockParamResp`

                - `FileID string`

                - `Type BashCodeExecutionOutput`

                  - `const BashCodeExecutionOutputBashCodeExecutionOutput BashCodeExecutionOutput = "bash_code_execution_output"`

              - `ReturnCode int64`

              - `Stderr string`

              - `Stdout string`

              - `Type BashCodeExecutionResult`

                - `const BashCodeExecutionResultBashCodeExecutionResult BashCodeExecutionResult = "bash_code_execution_result"`

          - `ToolUseID string`

          - `Type BashCodeExecutionToolResult`

            - `const BashCodeExecutionToolResultBashCodeExecutionToolResult BashCodeExecutionToolResult = "bash_code_execution_tool_result"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

        - `type BetaTextEditorCodeExecutionToolResultBlockParamResp struct{…}`

          - `Content BetaTextEditorCodeExecutionToolResultBlockParamContentUnionResp`

            - `type BetaTextEditorCodeExecutionToolResultErrorParamResp struct{…}`

              - `ErrorCode BetaTextEditorCodeExecutionToolResultErrorParamErrorCode`

                - `const BetaTextEditorCodeExecutionToolResultErrorParamErrorCodeInvalidToolInput BetaTextEditorCodeExecutionToolResultErrorParamErrorCode = "invalid_tool_input"`

                - `const BetaTextEditorCodeExecutionToolResultErrorParamErrorCodeUnavailable BetaTextEditorCodeExecutionToolResultErrorParamErrorCode = "unavailable"`

                - `const BetaTextEditorCodeExecutionToolResultErrorParamErrorCodeTooManyRequests BetaTextEditorCodeExecutionToolResultErrorParamErrorCode = "too_many_requests"`

                - `const BetaTextEditorCodeExecutionToolResultErrorParamErrorCodeExecutionTimeExceeded BetaTextEditorCodeExecutionToolResultErrorParamErrorCode = "execution_time_exceeded"`

                - `const BetaTextEditorCodeExecutionToolResultErrorParamErrorCodeFileNotFound BetaTextEditorCodeExecutionToolResultErrorParamErrorCode = "file_not_found"`

              - `Type TextEditorCodeExecutionToolResultError`

                - `const TextEditorCodeExecutionToolResultErrorTextEditorCodeExecutionToolResultError TextEditorCodeExecutionToolResultError = "text_editor_code_execution_tool_result_error"`

              - `ErrorMessage string`

            - `type BetaTextEditorCodeExecutionViewResultBlockParamResp struct{…}`

              - `Content string`

              - `FileType BetaTextEditorCodeExecutionViewResultBlockParamFileType`

                - `const BetaTextEditorCodeExecutionViewResultBlockParamFileTypeText BetaTextEditorCodeExecutionViewResultBlockParamFileType = "text"`

                - `const BetaTextEditorCodeExecutionViewResultBlockParamFileTypeImage BetaTextEditorCodeExecutionViewResultBlockParamFileType = "image"`

                - `const BetaTextEditorCodeExecutionViewResultBlockParamFileTypePDF BetaTextEditorCodeExecutionViewResultBlockParamFileType = "pdf"`

              - `Type TextEditorCodeExecutionViewResult`

                - `const TextEditorCodeExecutionViewResultTextEditorCodeExecutionViewResult TextEditorCodeExecutionViewResult = "text_editor_code_execution_view_result"`

              - `NumLines int64`

              - `StartLine int64`

              - `TotalLines int64`

            - `type BetaTextEditorCodeExecutionCreateResultBlockParamResp struct{…}`

              - `IsFileUpdate bool`

              - `Type TextEditorCodeExecutionCreateResult`

                - `const TextEditorCodeExecutionCreateResultTextEditorCodeExecutionCreateResult TextEditorCodeExecutionCreateResult = "text_editor_code_execution_create_result"`

            - `type BetaTextEditorCodeExecutionStrReplaceResultBlockParamResp struct{…}`

              - `Type TextEditorCodeExecutionStrReplaceResult`

                - `const TextEditorCodeExecutionStrReplaceResultTextEditorCodeExecutionStrReplaceResult TextEditorCodeExecutionStrReplaceResult = "text_editor_code_execution_str_replace_result"`

              - `Lines []string`

              - `NewLines int64`

              - `NewStart int64`

              - `OldLines int64`

              - `OldStart int64`

          - `ToolUseID string`

          - `Type TextEditorCodeExecutionToolResult`

            - `const TextEditorCodeExecutionToolResultTextEditorCodeExecutionToolResult TextEditorCodeExecutionToolResult = "text_editor_code_execution_tool_result"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

        - `type BetaToolSearchToolResultBlockParamResp struct{…}`

          - `Content BetaToolSearchToolResultBlockParamContentUnionResp`

            - `type BetaToolSearchToolResultErrorParamResp struct{…}`

              - `ErrorCode BetaToolSearchToolResultErrorParamErrorCode`

                - `const BetaToolSearchToolResultErrorParamErrorCodeInvalidToolInput BetaToolSearchToolResultErrorParamErrorCode = "invalid_tool_input"`

                - `const BetaToolSearchToolResultErrorParamErrorCodeUnavailable BetaToolSearchToolResultErrorParamErrorCode = "unavailable"`

                - `const BetaToolSearchToolResultErrorParamErrorCodeTooManyRequests BetaToolSearchToolResultErrorParamErrorCode = "too_many_requests"`

                - `const BetaToolSearchToolResultErrorParamErrorCodeExecutionTimeExceeded BetaToolSearchToolResultErrorParamErrorCode = "execution_time_exceeded"`

              - `Type ToolSearchToolResultError`

                - `const ToolSearchToolResultErrorToolSearchToolResultError ToolSearchToolResultError = "tool_search_tool_result_error"`

            - `type BetaToolSearchToolSearchResultBlockParamResp struct{…}`

              - `ToolReferences []BetaToolReferenceBlockParamResp`

                - `ToolName string`

                - `Type ToolReference`

                  - `const ToolReferenceToolReference ToolReference = "tool_reference"`

                - `CacheControl BetaCacheControlEphemeral`

                  Create a cache control breakpoint at this content block.

                  - `Type Ephemeral`

                    - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                  - `TTL BetaCacheControlEphemeralTTL`

                    The time-to-live for the cache control breakpoint.

                    This may be one the following values:

                    - `5m`: 5 minutes
                    - `1h`: 1 hour

                    Defaults to `5m`.

                    - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                    - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

              - `Type ToolSearchToolSearchResult`

                - `const ToolSearchToolSearchResultToolSearchToolSearchResult ToolSearchToolSearchResult = "tool_search_tool_search_result"`

          - `ToolUseID string`

          - `Type ToolSearchToolResult`

            - `const ToolSearchToolResultToolSearchToolResult ToolSearchToolResult = "tool_search_tool_result"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

        - `type BetaMCPToolUseBlockParamResp struct{…}`

          - `ID string`

          - `Input map[string, any]`

          - `Name string`

          - `ServerName string`

            The name of the MCP server

          - `Type MCPToolUse`

            - `const MCPToolUseMCPToolUse MCPToolUse = "mcp_tool_use"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

        - `type BetaRequestMCPToolResultBlockParamResp struct{…}`

          - `ToolUseID string`

          - `Type MCPToolResult`

            - `const MCPToolResultMCPToolResult MCPToolResult = "mcp_tool_result"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

          - `Content BetaRequestMCPToolResultBlockParamContentUnionResp`

            - `string`

            - `[]BetaTextBlockParamResp`

              - `Text string`

              - `Type Text`

                - `const TextText Text = "text"`

              - `CacheControl BetaCacheControlEphemeral`

                Create a cache control breakpoint at this content block.

                - `Type Ephemeral`

                  - `const EphemeralEphemeral Ephemeral = "ephemeral"`

                - `TTL BetaCacheControlEphemeralTTL`

                  The time-to-live for the cache control breakpoint.

                  This may be one the following values:

                  - `5m`: 5 minutes
                  - `1h`: 1 hour

                  Defaults to `5m`.

                  - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

                  - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

              - `Citations []BetaTextCitationParamUnionResp`

                - `type BetaCitationCharLocationParamResp struct{…}`

                  - `CitedText string`

                  - `DocumentIndex int64`

                  - `DocumentTitle string`

                  - `EndCharIndex int64`

                  - `StartCharIndex int64`

                  - `Type CharLocation`

                    - `const CharLocationCharLocation CharLocation = "char_location"`

                - `type BetaCitationPageLocationParamResp struct{…}`

                  - `CitedText string`

                  - `DocumentIndex int64`

                  - `DocumentTitle string`

                  - `EndPageNumber int64`

                  - `StartPageNumber int64`

                  - `Type PageLocation`

                    - `const PageLocationPageLocation PageLocation = "page_location"`

                - `type BetaCitationContentBlockLocationParamResp struct{…}`

                  - `CitedText string`

                  - `DocumentIndex int64`

                  - `DocumentTitle string`

                  - `EndBlockIndex int64`

                  - `StartBlockIndex int64`

                  - `Type ContentBlockLocation`

                    - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

                - `type BetaCitationWebSearchResultLocationParamResp struct{…}`

                  - `CitedText string`

                  - `EncryptedIndex string`

                  - `Title string`

                  - `Type WebSearchResultLocation`

                    - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

                  - `URL string`

                - `type BetaCitationSearchResultLocationParamResp struct{…}`

                  - `CitedText string`

                  - `EndBlockIndex int64`

                  - `SearchResultIndex int64`

                  - `Source string`

                  - `StartBlockIndex int64`

                  - `Title string`

                  - `Type SearchResultLocation`

                    - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

          - `IsError bool`

        - `type BetaContainerUploadBlockParamResp struct{…}`

          A content block that represents a file to be uploaded to the container
          Files uploaded via this block will be available in the container's input directory.

          - `FileID string`

          - `Type ContainerUpload`

            - `const ContainerUploadContainerUpload ContainerUpload = "container_upload"`

          - `CacheControl BetaCacheControlEphemeral`

            Create a cache control breakpoint at this content block.

            - `Type Ephemeral`

              - `const EphemeralEphemeral Ephemeral = "ephemeral"`

            - `TTL BetaCacheControlEphemeralTTL`

              The time-to-live for the cache control breakpoint.

              This may be one the following values:

              - `5m`: 5 minutes
              - `1h`: 1 hour

              Defaults to `5m`.

              - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

              - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

    - `Role BetaMessageParamRole`

      - `const BetaMessageParamRoleUser BetaMessageParamRole = "user"`

      - `const BetaMessageParamRoleAssistant BetaMessageParamRole = "assistant"`

  - `Model param.Field[Model]`

    Body param: The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional details and options.

  - `ContextManagement param.Field[BetaContextManagementConfig]`

    Body param: Context management configuration.

    This allows you to control how Claude manages context across multiple requests, such as whether to clear function results or not.

  - `MCPServers param.Field[[]BetaRequestMCPServerURLDefinition]`

    Body param: MCP servers to be utilized in this request

    - `Name string`

    - `Type URL`

      - `const URLURL URL = "url"`

    - `URL string`

    - `AuthorizationToken string`

    - `ToolConfiguration BetaRequestMCPServerToolConfiguration`

      - `AllowedTools []string`

      - `Enabled bool`

  - `OutputConfig param.Field[BetaOutputConfig]`

    Body param: Configuration options for the model's output. Controls aspects like how much effort the model puts into its response.

  - `OutputFormat param.Field[BetaJSONOutputFormat]`

    Body param:
    A schema to specify Claude's output format in responses.

  - `System param.Field[BetaMessageCountTokensParamsSystemUnion]`

    Body param: System prompt.

    A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

    - `string`

    - `type BetaMessageCountTokensParamsSystemArray []BetaTextBlockParamResp`

      - `Text string`

      - `Type Text`

        - `const TextText Text = "text"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `Citations []BetaTextCitationParamUnionResp`

        - `type BetaCitationCharLocationParamResp struct{…}`

          - `CitedText string`

          - `DocumentIndex int64`

          - `DocumentTitle string`

          - `EndCharIndex int64`

          - `StartCharIndex int64`

          - `Type CharLocation`

            - `const CharLocationCharLocation CharLocation = "char_location"`

        - `type BetaCitationPageLocationParamResp struct{…}`

          - `CitedText string`

          - `DocumentIndex int64`

          - `DocumentTitle string`

          - `EndPageNumber int64`

          - `StartPageNumber int64`

          - `Type PageLocation`

            - `const PageLocationPageLocation PageLocation = "page_location"`

        - `type BetaCitationContentBlockLocationParamResp struct{…}`

          - `CitedText string`

          - `DocumentIndex int64`

          - `DocumentTitle string`

          - `EndBlockIndex int64`

          - `StartBlockIndex int64`

          - `Type ContentBlockLocation`

            - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

        - `type BetaCitationWebSearchResultLocationParamResp struct{…}`

          - `CitedText string`

          - `EncryptedIndex string`

          - `Title string`

          - `Type WebSearchResultLocation`

            - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

          - `URL string`

        - `type BetaCitationSearchResultLocationParamResp struct{…}`

          - `CitedText string`

          - `EndBlockIndex int64`

          - `SearchResultIndex int64`

          - `Source string`

          - `StartBlockIndex int64`

          - `Title string`

          - `Type SearchResultLocation`

            - `const SearchResultLocationSearchResultLocation SearchResultLocation = "search_result_location"`

  - `Thinking param.Field[BetaThinkingConfigParamUnionResp]`

    Body param: Configuration for enabling Claude's extended thinking.

    When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `ToolChoice param.Field[BetaToolChoiceUnion]`

    Body param: How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `Tools param.Field[[]BetaMessageCountTokensParamsToolUnion]`

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

    - `type BetaTool struct{…}`

      - `InputSchema BetaToolInputSchema`

        [JSON schema](https://json-schema.org/draft/2020-12) for this tool's input.

        This defines the shape of the `input` that your tool accepts and that the model will produce.

        - `Type Object`

          - `const ObjectObject Object = "object"`

        - `Properties map[string, any]`

        - `Required []string`

      - `Name string`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

      - `AllowedCallers []string`

        - `const BetaToolAllowedCallerDirect BetaToolAllowedCaller = "direct"`

        - `const BetaToolAllowedCallerCodeExecution20250825 BetaToolAllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Description string`

        Description of what this tool does.

        Tool descriptions should be as detailed as possible. The more information that the model has about what the tool is and how to use it, the better it will perform. You can use natural language descriptions to reinforce important aspects of the tool input JSON schema.

      - `InputExamples []map[string, any]`

      - `Strict bool`

      - `Type BetaToolType`

        - `const BetaToolTypeCustom BetaToolType = "custom"`

    - `type BetaToolBash20241022 struct{…}`

      - `Name Bash`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const BashBash Bash = "bash"`

      - `Type Bash20241022`

        - `const Bash20241022Bash20241022 Bash20241022 = "bash_20241022"`

      - `AllowedCallers []string`

        - `const BetaToolBash20241022AllowedCallerDirect BetaToolBash20241022AllowedCaller = "direct"`

        - `const BetaToolBash20241022AllowedCallerCodeExecution20250825 BetaToolBash20241022AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `InputExamples []map[string, any]`

      - `Strict bool`

    - `type BetaToolBash20250124 struct{…}`

      - `Name Bash`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const BashBash Bash = "bash"`

      - `Type Bash20250124`

        - `const Bash20250124Bash20250124 Bash20250124 = "bash_20250124"`

      - `AllowedCallers []string`

        - `const BetaToolBash20250124AllowedCallerDirect BetaToolBash20250124AllowedCaller = "direct"`

        - `const BetaToolBash20250124AllowedCallerCodeExecution20250825 BetaToolBash20250124AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `InputExamples []map[string, any]`

      - `Strict bool`

    - `type BetaCodeExecutionTool20250522 struct{…}`

      - `Name CodeExecution`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const CodeExecutionCodeExecution CodeExecution = "code_execution"`

      - `Type CodeExecution20250522`

        - `const CodeExecution20250522CodeExecution20250522 CodeExecution20250522 = "code_execution_20250522"`

      - `AllowedCallers []string`

        - `const BetaCodeExecutionTool20250522AllowedCallerDirect BetaCodeExecutionTool20250522AllowedCaller = "direct"`

        - `const BetaCodeExecutionTool20250522AllowedCallerCodeExecution20250825 BetaCodeExecutionTool20250522AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Strict bool`

    - `type BetaCodeExecutionTool20250825 struct{…}`

      - `Name CodeExecution`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const CodeExecutionCodeExecution CodeExecution = "code_execution"`

      - `Type CodeExecution20250825`

        - `const CodeExecution20250825CodeExecution20250825 CodeExecution20250825 = "code_execution_20250825"`

      - `AllowedCallers []string`

        - `const BetaCodeExecutionTool20250825AllowedCallerDirect BetaCodeExecutionTool20250825AllowedCaller = "direct"`

        - `const BetaCodeExecutionTool20250825AllowedCallerCodeExecution20250825 BetaCodeExecutionTool20250825AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Strict bool`

    - `type BetaToolComputerUse20241022 struct{…}`

      - `DisplayHeightPx int64`

        The height of the display in pixels.

      - `DisplayWidthPx int64`

        The width of the display in pixels.

      - `Name Computer`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const ComputerComputer Computer = "computer"`

      - `Type Computer20241022`

        - `const Computer20241022Computer20241022 Computer20241022 = "computer_20241022"`

      - `AllowedCallers []string`

        - `const BetaToolComputerUse20241022AllowedCallerDirect BetaToolComputerUse20241022AllowedCaller = "direct"`

        - `const BetaToolComputerUse20241022AllowedCallerCodeExecution20250825 BetaToolComputerUse20241022AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `DisplayNumber int64`

        The X11 display number (e.g. 0, 1) for the display.

      - `InputExamples []map[string, any]`

      - `Strict bool`

    - `type BetaMemoryTool20250818 struct{…}`

      - `Name Memory`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const MemoryMemory Memory = "memory"`

      - `Type Memory20250818`

        - `const Memory20250818Memory20250818 Memory20250818 = "memory_20250818"`

      - `AllowedCallers []string`

        - `const BetaMemoryTool20250818AllowedCallerDirect BetaMemoryTool20250818AllowedCaller = "direct"`

        - `const BetaMemoryTool20250818AllowedCallerCodeExecution20250825 BetaMemoryTool20250818AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `InputExamples []map[string, any]`

      - `Strict bool`

    - `type BetaToolComputerUse20250124 struct{…}`

      - `DisplayHeightPx int64`

        The height of the display in pixels.

      - `DisplayWidthPx int64`

        The width of the display in pixels.

      - `Name Computer`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const ComputerComputer Computer = "computer"`

      - `Type Computer20250124`

        - `const Computer20250124Computer20250124 Computer20250124 = "computer_20250124"`

      - `AllowedCallers []string`

        - `const BetaToolComputerUse20250124AllowedCallerDirect BetaToolComputerUse20250124AllowedCaller = "direct"`

        - `const BetaToolComputerUse20250124AllowedCallerCodeExecution20250825 BetaToolComputerUse20250124AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `DisplayNumber int64`

        The X11 display number (e.g. 0, 1) for the display.

      - `InputExamples []map[string, any]`

      - `Strict bool`

    - `type BetaToolTextEditor20241022 struct{…}`

      - `Name StrReplaceEditor`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const StrReplaceEditorStrReplaceEditor StrReplaceEditor = "str_replace_editor"`

      - `Type TextEditor20241022`

        - `const TextEditor20241022TextEditor20241022 TextEditor20241022 = "text_editor_20241022"`

      - `AllowedCallers []string`

        - `const BetaToolTextEditor20241022AllowedCallerDirect BetaToolTextEditor20241022AllowedCaller = "direct"`

        - `const BetaToolTextEditor20241022AllowedCallerCodeExecution20250825 BetaToolTextEditor20241022AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `InputExamples []map[string, any]`

      - `Strict bool`

    - `type BetaToolComputerUse20251124 struct{…}`

      - `DisplayHeightPx int64`

        The height of the display in pixels.

      - `DisplayWidthPx int64`

        The width of the display in pixels.

      - `Name Computer`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const ComputerComputer Computer = "computer"`

      - `Type Computer20251124`

        - `const Computer20251124Computer20251124 Computer20251124 = "computer_20251124"`

      - `AllowedCallers []string`

        - `const BetaToolComputerUse20251124AllowedCallerDirect BetaToolComputerUse20251124AllowedCaller = "direct"`

        - `const BetaToolComputerUse20251124AllowedCallerCodeExecution20250825 BetaToolComputerUse20251124AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `DisplayNumber int64`

        The X11 display number (e.g. 0, 1) for the display.

      - `EnableZoom bool`

        Whether to enable an action to take a zoomed-in screenshot of the screen.

      - `InputExamples []map[string, any]`

      - `Strict bool`

    - `type BetaToolTextEditor20250124 struct{…}`

      - `Name StrReplaceEditor`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const StrReplaceEditorStrReplaceEditor StrReplaceEditor = "str_replace_editor"`

      - `Type TextEditor20250124`

        - `const TextEditor20250124TextEditor20250124 TextEditor20250124 = "text_editor_20250124"`

      - `AllowedCallers []string`

        - `const BetaToolTextEditor20250124AllowedCallerDirect BetaToolTextEditor20250124AllowedCaller = "direct"`

        - `const BetaToolTextEditor20250124AllowedCallerCodeExecution20250825 BetaToolTextEditor20250124AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `InputExamples []map[string, any]`

      - `Strict bool`

    - `type BetaToolTextEditor20250429 struct{…}`

      - `Name StrReplaceBasedEditTool`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const StrReplaceBasedEditToolStrReplaceBasedEditTool StrReplaceBasedEditTool = "str_replace_based_edit_tool"`

      - `Type TextEditor20250429`

        - `const TextEditor20250429TextEditor20250429 TextEditor20250429 = "text_editor_20250429"`

      - `AllowedCallers []string`

        - `const BetaToolTextEditor20250429AllowedCallerDirect BetaToolTextEditor20250429AllowedCaller = "direct"`

        - `const BetaToolTextEditor20250429AllowedCallerCodeExecution20250825 BetaToolTextEditor20250429AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `InputExamples []map[string, any]`

      - `Strict bool`

    - `type BetaToolTextEditor20250728 struct{…}`

      - `Name StrReplaceBasedEditTool`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const StrReplaceBasedEditToolStrReplaceBasedEditTool StrReplaceBasedEditTool = "str_replace_based_edit_tool"`

      - `Type TextEditor20250728`

        - `const TextEditor20250728TextEditor20250728 TextEditor20250728 = "text_editor_20250728"`

      - `AllowedCallers []string`

        - `const BetaToolTextEditor20250728AllowedCallerDirect BetaToolTextEditor20250728AllowedCaller = "direct"`

        - `const BetaToolTextEditor20250728AllowedCallerCodeExecution20250825 BetaToolTextEditor20250728AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `InputExamples []map[string, any]`

      - `MaxCharacters int64`

        Maximum number of characters to display when viewing a file. If not specified, defaults to displaying the full file.

      - `Strict bool`

    - `type BetaWebSearchTool20250305 struct{…}`

      - `Name WebSearch`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const WebSearchWebSearch WebSearch = "web_search"`

      - `Type WebSearch20250305`

        - `const WebSearch20250305WebSearch20250305 WebSearch20250305 = "web_search_20250305"`

      - `AllowedCallers []string`

        - `const BetaWebSearchTool20250305AllowedCallerDirect BetaWebSearchTool20250305AllowedCaller = "direct"`

        - `const BetaWebSearchTool20250305AllowedCallerCodeExecution20250825 BetaWebSearchTool20250305AllowedCaller = "code_execution_20250825"`

      - `AllowedDomains []string`

        If provided, only these domains will be included in results. Cannot be used alongside `blocked_domains`.

      - `BlockedDomains []string`

        If provided, these domains will never appear in results. Cannot be used alongside `allowed_domains`.

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `MaxUses int64`

        Maximum number of times the tool can be used in the API request.

      - `Strict bool`

      - `UserLocation BetaWebSearchTool20250305UserLocation`

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

    - `type BetaWebFetchTool20250910 struct{…}`

      - `Name WebFetch`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const WebFetchWebFetch WebFetch = "web_fetch"`

      - `Type WebFetch20250910`

        - `const WebFetch20250910WebFetch20250910 WebFetch20250910 = "web_fetch_20250910"`

      - `AllowedCallers []string`

        - `const BetaWebFetchTool20250910AllowedCallerDirect BetaWebFetchTool20250910AllowedCaller = "direct"`

        - `const BetaWebFetchTool20250910AllowedCallerCodeExecution20250825 BetaWebFetchTool20250910AllowedCaller = "code_execution_20250825"`

      - `AllowedDomains []string`

        List of domains to allow fetching from

      - `BlockedDomains []string`

        List of domains to block fetching from

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `Citations BetaCitationsConfigParamResp`

        Citations configuration for fetched documents. Citations are disabled by default.

        - `Enabled bool`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `MaxContentTokens int64`

        Maximum number of tokens used by including web page text content in the context. The limit is approximate and does not apply to binary content such as PDFs.

      - `MaxUses int64`

        Maximum number of times the tool can be used in the API request.

      - `Strict bool`

    - `type BetaToolSearchToolBm25_20251119 struct{…}`

      - `Name ToolSearchToolBm25`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const ToolSearchToolBm25ToolSearchToolBm25 ToolSearchToolBm25 = "tool_search_tool_bm25"`

      - `Type BetaToolSearchToolBm25_20251119Type`

        - `const BetaToolSearchToolBm25_20251119TypeToolSearchToolBm25_20251119 BetaToolSearchToolBm25_20251119Type = "tool_search_tool_bm25_20251119"`

        - `const BetaToolSearchToolBm25_20251119TypeToolSearchToolBm25 BetaToolSearchToolBm25_20251119Type = "tool_search_tool_bm25"`

      - `AllowedCallers []string`

        - `const BetaToolSearchToolBm25_20251119AllowedCallerDirect BetaToolSearchToolBm25_20251119AllowedCaller = "direct"`

        - `const BetaToolSearchToolBm25_20251119AllowedCallerCodeExecution20250825 BetaToolSearchToolBm25_20251119AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Strict bool`

    - `type BetaToolSearchToolRegex20251119 struct{…}`

      - `Name ToolSearchToolRegex`

        Name of the tool.

        This is how the tool will be called by the model and in `tool_use` blocks.

        - `const ToolSearchToolRegexToolSearchToolRegex ToolSearchToolRegex = "tool_search_tool_regex"`

      - `Type BetaToolSearchToolRegex20251119Type`

        - `const BetaToolSearchToolRegex20251119TypeToolSearchToolRegex20251119 BetaToolSearchToolRegex20251119Type = "tool_search_tool_regex_20251119"`

        - `const BetaToolSearchToolRegex20251119TypeToolSearchToolRegex BetaToolSearchToolRegex20251119Type = "tool_search_tool_regex"`

      - `AllowedCallers []string`

        - `const BetaToolSearchToolRegex20251119AllowedCallerDirect BetaToolSearchToolRegex20251119AllowedCaller = "direct"`

        - `const BetaToolSearchToolRegex20251119AllowedCallerCodeExecution20250825 BetaToolSearchToolRegex20251119AllowedCaller = "code_execution_20250825"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `DeferLoading bool`

        If true, tool will not be included in initial system prompt. Only loaded when returned via tool_reference from tool search.

      - `Strict bool`

    - `type BetaMCPToolset struct{…}`

      Configuration for a group of tools from an MCP server.

      Allows configuring enabled status and defer_loading for all tools
      from an MCP server, with optional per-tool overrides.

      - `MCPServerName string`

        Name of the MCP server to configure tools for

      - `Type MCPToolset`

        - `const MCPToolsetMCPToolset MCPToolset = "mcp_toolset"`

      - `CacheControl BetaCacheControlEphemeral`

        Create a cache control breakpoint at this content block.

        - `Type Ephemeral`

          - `const EphemeralEphemeral Ephemeral = "ephemeral"`

        - `TTL BetaCacheControlEphemeralTTL`

          The time-to-live for the cache control breakpoint.

          This may be one the following values:

          - `5m`: 5 minutes
          - `1h`: 1 hour

          Defaults to `5m`.

          - `const BetaCacheControlEphemeralTTLTTL5m BetaCacheControlEphemeralTTL = "5m"`

          - `const BetaCacheControlEphemeralTTLTTL1h BetaCacheControlEphemeralTTL = "1h"`

      - `Configs map[string, BetaMCPToolConfig]`

        Configuration overrides for specific tools, keyed by tool name

        - `DeferLoading bool`

        - `Enabled bool`

      - `DefaultConfig BetaMCPToolDefaultConfig`

        Default configuration applied to all tools from this server

        - `DeferLoading bool`

        - `Enabled bool`

  - `Betas param.Field[[]AnthropicBeta]`

    Header param: Optional header to specify the beta version(s) you want to use.

    - `string`

    - `type AnthropicBeta string`

      - `const AnthropicBetaMessageBatches2024_09_24 AnthropicBeta = "message-batches-2024-09-24"`

      - `const AnthropicBetaPromptCaching2024_07_31 AnthropicBeta = "prompt-caching-2024-07-31"`

      - `const AnthropicBetaComputerUse2024_10_22 AnthropicBeta = "computer-use-2024-10-22"`

      - `const AnthropicBetaComputerUse2025_01_24 AnthropicBeta = "computer-use-2025-01-24"`

      - `const AnthropicBetaPDFs2024_09_25 AnthropicBeta = "pdfs-2024-09-25"`

      - `const AnthropicBetaTokenCounting2024_11_01 AnthropicBeta = "token-counting-2024-11-01"`

      - `const AnthropicBetaTokenEfficientTools2025_02_19 AnthropicBeta = "token-efficient-tools-2025-02-19"`

      - `const AnthropicBetaOutput128k2025_02_19 AnthropicBeta = "output-128k-2025-02-19"`

      - `const AnthropicBetaFilesAPI2025_04_14 AnthropicBeta = "files-api-2025-04-14"`

      - `const AnthropicBetaMCPClient2025_04_04 AnthropicBeta = "mcp-client-2025-04-04"`

      - `const AnthropicBetaMCPClient2025_11_20 AnthropicBeta = "mcp-client-2025-11-20"`

      - `const AnthropicBetaDevFullThinking2025_05_14 AnthropicBeta = "dev-full-thinking-2025-05-14"`

      - `const AnthropicBetaInterleavedThinking2025_05_14 AnthropicBeta = "interleaved-thinking-2025-05-14"`

      - `const AnthropicBetaCodeExecution2025_05_22 AnthropicBeta = "code-execution-2025-05-22"`

      - `const AnthropicBetaExtendedCacheTTL2025_04_11 AnthropicBeta = "extended-cache-ttl-2025-04-11"`

      - `const AnthropicBetaContext1m2025_08_07 AnthropicBeta = "context-1m-2025-08-07"`

      - `const AnthropicBetaContextManagement2025_06_27 AnthropicBeta = "context-management-2025-06-27"`

      - `const AnthropicBetaModelContextWindowExceeded2025_08_26 AnthropicBeta = "model-context-window-exceeded-2025-08-26"`

      - `const AnthropicBetaSkills2025_10_02 AnthropicBeta = "skills-2025-10-02"`

### Returns

- `type BetaMessageTokensCount struct{…}`

  - `ContextManagement BetaCountTokensContextManagementResponse`

    Information about context management applied to the message.

    - `OriginalInputTokens int64`

      The original token count before context management was applied

  - `InputTokens int64`

    The total number of tokens across the provided list of messages, system prompt, and tools.

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
  betaMessageTokensCount, err := client.Beta.Messages.CountTokens(context.TODO(), anthropic.BetaMessageCountTokensParams{
    Messages: []anthropic.BetaMessageParam{anthropic.BetaMessageParam{
      Content: []anthropic.BetaContentBlockParamUnion{anthropic.BetaContentBlockParamUnion{
        OfText: &anthropic.BetaTextBlockParam{Text: "What is a quaternion?", CacheControl: anthropic.BetaCacheControlEphemeralParam{TTL: anthropic.BetaCacheControlEphemeralTTLTTL5m}, Citations: []anthropic.BetaTextCitationParamUnion{anthropic.BetaTextCitationParamUnion{
          OfCharLocation: &anthropic.BetaCitationCharLocationParam{CitedText: "cited_text", DocumentIndex: 0, DocumentTitle: anthropic.String("x"), EndCharIndex: 0, StartCharIndex: 0},
        }}},
      }},
      Role: anthropic.BetaMessageParamRoleUser,
    }},
    Model: anthropic.ModelClaudeOpus4_5_20251101,
  })
  if err != nil {
    panic(err.Error())
  }
  fmt.Printf("%+v\n", betaMessageTokensCount.ContextManagement)
}
```
