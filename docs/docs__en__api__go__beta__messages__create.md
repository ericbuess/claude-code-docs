## Create

`client.Beta.Messages.New(ctx, params) (*BetaMessage, error)`

**post** `/v1/messages`

Send a structured list of input messages with text and/or image content, and the model will generate the next message in the conversation.

The Messages API can be used for either single queries or stateless multi-turn conversations.

Learn more about the Messages API in our [user guide](https://docs.claude.com/en/docs/initial-setup)

### Parameters

- `params BetaMessageNewParams`

  - `MaxTokens param.Field[int64]`

    Body param: The maximum number of tokens to generate before stopping.

    Note that our models may stop _before_ reaching this maximum. This parameter only specifies the absolute maximum number of tokens to generate.

    Different models have different maximum values for this parameter.  See [models](https://docs.claude.com/en/docs/models-overview) for details.

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

  - `Container param.Field[BetaMessageNewParamsContainerUnion]`

    Body param: Container identifier for reuse across requests.

    - `type BetaContainerParamsResp struct{…}`

      Container parameters with skills to be loaded.

      - `ID string`

        Container id

      - `Skills []BetaSkillParamsResp`

        List of skills to load in the container

        - `SkillID string`

          Skill ID

        - `Type BetaSkillParamsType`

          Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

          - `const BetaSkillParamsTypeAnthropic BetaSkillParamsType = "anthropic"`

          - `const BetaSkillParamsTypeCustom BetaSkillParamsType = "custom"`

        - `Version string`

          Skill version or 'latest' for most recent version

    - `string`

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

  - `Metadata param.Field[BetaMetadata]`

    Body param: An object describing metadata about the request.

  - `OutputConfig param.Field[BetaOutputConfig]`

    Body param: Configuration options for the model's output. Controls aspects like how much effort the model puts into its response.

  - `OutputFormat param.Field[BetaJSONOutputFormat]`

    Body param:
    A schema to specify Claude's output format in responses.

  - `ServiceTier param.Field[BetaMessageNewParamsServiceTier]`

    Body param: Determines whether to use priority capacity (if available) or standard capacity for this request.

    Anthropic offers different levels of service for your API requests. See [service-tiers](https://docs.claude.com/en/api/service-tiers) for details.

    - `const BetaMessageNewParamsServiceTierAuto BetaMessageNewParamsServiceTier = "auto"`

    - `const BetaMessageNewParamsServiceTierStandardOnly BetaMessageNewParamsServiceTier = "standard_only"`

  - `StopSequences param.Field[[]string]`

    Body param: Custom text sequences that will cause the model to stop generating.

    Our models will normally stop when they have naturally completed their turn, which will result in a response `stop_reason` of `"end_turn"`.

    If you want the model to stop generating when it encounters custom strings of text, you can use the `stop_sequences` parameter. If the model encounters one of the custom sequences, the response `stop_reason` value will be `"stop_sequence"` and the response `stop_sequence` value will contain the matched stop sequence.

  - ``

  - `System param.Field[[]BetaTextBlockParamResp]`

    Body param: System prompt.

    A system prompt is a way of providing context and instructions to Claude, such as specifying a particular goal or role. See our [guide to system prompts](https://docs.claude.com/en/docs/system-prompts).

    - `[]BetaTextBlockParam`

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

  - `Temperature param.Field[float64]`

    Body param: Amount of randomness injected into the response.

    Defaults to `1.0`. Ranges from `0.0` to `1.0`. Use `temperature` closer to `0.0` for analytical / multiple choice, and closer to `1.0` for creative and generative tasks.

    Note that even with `temperature` of `0.0`, the results will not be fully deterministic.

  - `Thinking param.Field[BetaThinkingConfigParamUnionResp]`

    Body param: Configuration for enabling Claude's extended thinking.

    When enabled, responses include `thinking` content blocks showing Claude's thinking process before the final answer. Requires a minimum budget of 1,024 tokens and counts towards your `max_tokens` limit.

    See [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) for details.

  - `ToolChoice param.Field[BetaToolChoiceUnion]`

    Body param: How the model should use the provided tools. The model can use a specific tool, any available tool, decide by itself, or not use tools at all.

  - `Tools param.Field[[]BetaToolUnion]`

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

  - `TopK param.Field[int64]`

    Body param: Only sample from the top K options for each subsequent token.

    Used to remove "long tail" low probability responses. [Learn more technical details here](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277).

    Recommended for advanced use cases only. You usually only need to use `temperature`.

  - `TopP param.Field[float64]`

    Body param: Use nucleus sampling.

    In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by `top_p`. You should either alter `temperature` or `top_p`, but not both.

    Recommended for advanced use cases only. You usually only need to use `temperature`.

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

- `type BetaMessage struct{…}`

  - `ID string`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `Container BetaContainer`

    Information about the container used in the request (for the code execution tool)

    - `ID string`

      Identifier for the container used in this request

    - `ExpiresAt Time`

      The time at which the container will expire.

    - `Skills []BetaSkill`

      Skills loaded in the container

      - `SkillID string`

        Skill ID

      - `Type BetaSkillType`

        Type of skill - either 'anthropic' (built-in) or 'custom' (user-defined)

        - `const BetaSkillTypeAnthropic BetaSkillType = "anthropic"`

        - `const BetaSkillTypeCustom BetaSkillType = "custom"`

      - `Version string`

        Skill version or 'latest' for most recent version

  - `Content []BetaContentBlockUnion`

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

    - `type BetaTextBlock struct{…}`

      - `Citations []BetaTextCitationUnion`

        Citations supporting the text block.

        The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

        - `type BetaCitationCharLocation struct{…}`

          - `CitedText string`

          - `DocumentIndex int64`

          - `DocumentTitle string`

          - `EndCharIndex int64`

          - `FileID string`

          - `StartCharIndex int64`

          - `Type CharLocation`

            - `const CharLocationCharLocation CharLocation = "char_location"`

        - `type BetaCitationPageLocation struct{…}`

          - `CitedText string`

          - `DocumentIndex int64`

          - `DocumentTitle string`

          - `EndPageNumber int64`

          - `FileID string`

          - `StartPageNumber int64`

          - `Type PageLocation`

            - `const PageLocationPageLocation PageLocation = "page_location"`

        - `type BetaCitationContentBlockLocation struct{…}`

          - `CitedText string`

          - `DocumentIndex int64`

          - `DocumentTitle string`

          - `EndBlockIndex int64`

          - `FileID string`

          - `StartBlockIndex int64`

          - `Type ContentBlockLocation`

            - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

        - `type BetaCitationsWebSearchResultLocation struct{…}`

          - `CitedText string`

          - `EncryptedIndex string`

          - `Title string`

          - `Type WebSearchResultLocation`

            - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

          - `URL string`

        - `type BetaCitationSearchResultLocation struct{…}`

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

    - `type BetaThinkingBlock struct{…}`

      - `Signature string`

      - `Thinking string`

      - `Type Thinking`

        - `const ThinkingThinking Thinking = "thinking"`

    - `type BetaRedactedThinkingBlock struct{…}`

      - `Data string`

      - `Type RedactedThinking`

        - `const RedactedThinkingRedactedThinking RedactedThinking = "redacted_thinking"`

    - `type BetaToolUseBlock struct{…}`

      - `ID string`

      - `Input map[string, any]`

      - `Name string`

      - `Type ToolUse`

        - `const ToolUseToolUse ToolUse = "tool_use"`

      - `Caller BetaToolUseBlockCallerUnion`

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

    - `type BetaServerToolUseBlock struct{…}`

      - `ID string`

      - `Caller BetaServerToolUseBlockCallerUnion`

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

      - `Input map[string, any]`

      - `Name BetaServerToolUseBlockName`

        - `const BetaServerToolUseBlockNameWebSearch BetaServerToolUseBlockName = "web_search"`

        - `const BetaServerToolUseBlockNameWebFetch BetaServerToolUseBlockName = "web_fetch"`

        - `const BetaServerToolUseBlockNameCodeExecution BetaServerToolUseBlockName = "code_execution"`

        - `const BetaServerToolUseBlockNameBashCodeExecution BetaServerToolUseBlockName = "bash_code_execution"`

        - `const BetaServerToolUseBlockNameTextEditorCodeExecution BetaServerToolUseBlockName = "text_editor_code_execution"`

        - `const BetaServerToolUseBlockNameToolSearchToolRegex BetaServerToolUseBlockName = "tool_search_tool_regex"`

        - `const BetaServerToolUseBlockNameToolSearchToolBm25 BetaServerToolUseBlockName = "tool_search_tool_bm25"`

      - `Type ServerToolUse`

        - `const ServerToolUseServerToolUse ServerToolUse = "server_tool_use"`

    - `type BetaWebSearchToolResultBlock struct{…}`

      - `Content BetaWebSearchToolResultBlockContentUnion`

        - `type BetaWebSearchToolResultError struct{…}`

          - `ErrorCode BetaWebSearchToolResultErrorCode`

            - `const BetaWebSearchToolResultErrorCodeInvalidToolInput BetaWebSearchToolResultErrorCode = "invalid_tool_input"`

            - `const BetaWebSearchToolResultErrorCodeUnavailable BetaWebSearchToolResultErrorCode = "unavailable"`

            - `const BetaWebSearchToolResultErrorCodeMaxUsesExceeded BetaWebSearchToolResultErrorCode = "max_uses_exceeded"`

            - `const BetaWebSearchToolResultErrorCodeTooManyRequests BetaWebSearchToolResultErrorCode = "too_many_requests"`

            - `const BetaWebSearchToolResultErrorCodeQueryTooLong BetaWebSearchToolResultErrorCode = "query_too_long"`

          - `Type WebSearchToolResultError`

            - `const WebSearchToolResultErrorWebSearchToolResultError WebSearchToolResultError = "web_search_tool_result_error"`

        - `type BetaWebSearchToolResultBlockContentArray []BetaWebSearchResultBlock`

          - `EncryptedContent string`

          - `PageAge string`

          - `Title string`

          - `Type WebSearchResult`

            - `const WebSearchResultWebSearchResult WebSearchResult = "web_search_result"`

          - `URL string`

      - `ToolUseID string`

      - `Type WebSearchToolResult`

        - `const WebSearchToolResultWebSearchToolResult WebSearchToolResult = "web_search_tool_result"`

    - `type BetaWebFetchToolResultBlock struct{…}`

      - `Content BetaWebFetchToolResultBlockContentUnion`

        - `type BetaWebFetchToolResultErrorBlock struct{…}`

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

        - `type BetaWebFetchBlock struct{…}`

          - `Content BetaDocumentBlock`

            - `Citations BetaCitationConfig`

              Citation configuration for the document

              - `Enabled bool`

            - `Source BetaDocumentBlockSourceUnion`

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

            - `Title string`

              The title of the document

            - `Type Document`

              - `const DocumentDocument Document = "document"`

          - `RetrievedAt string`

            ISO 8601 timestamp when the content was retrieved

          - `Type WebFetchResult`

            - `const WebFetchResultWebFetchResult WebFetchResult = "web_fetch_result"`

          - `URL string`

            Fetched content URL

      - `ToolUseID string`

      - `Type WebFetchToolResult`

        - `const WebFetchToolResultWebFetchToolResult WebFetchToolResult = "web_fetch_tool_result"`

    - `type BetaCodeExecutionToolResultBlock struct{…}`

      - `Content BetaCodeExecutionToolResultBlockContentUnion`

        - `type BetaCodeExecutionToolResultError struct{…}`

          - `ErrorCode BetaCodeExecutionToolResultErrorCode`

            - `const BetaCodeExecutionToolResultErrorCodeInvalidToolInput BetaCodeExecutionToolResultErrorCode = "invalid_tool_input"`

            - `const BetaCodeExecutionToolResultErrorCodeUnavailable BetaCodeExecutionToolResultErrorCode = "unavailable"`

            - `const BetaCodeExecutionToolResultErrorCodeTooManyRequests BetaCodeExecutionToolResultErrorCode = "too_many_requests"`

            - `const BetaCodeExecutionToolResultErrorCodeExecutionTimeExceeded BetaCodeExecutionToolResultErrorCode = "execution_time_exceeded"`

          - `Type CodeExecutionToolResultError`

            - `const CodeExecutionToolResultErrorCodeExecutionToolResultError CodeExecutionToolResultError = "code_execution_tool_result_error"`

        - `type BetaCodeExecutionResultBlock struct{…}`

          - `Content []BetaCodeExecutionOutputBlock`

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

    - `type BetaBashCodeExecutionToolResultBlock struct{…}`

      - `Content BetaBashCodeExecutionToolResultBlockContentUnion`

        - `type BetaBashCodeExecutionToolResultError struct{…}`

          - `ErrorCode BetaBashCodeExecutionToolResultErrorErrorCode`

            - `const BetaBashCodeExecutionToolResultErrorErrorCodeInvalidToolInput BetaBashCodeExecutionToolResultErrorErrorCode = "invalid_tool_input"`

            - `const BetaBashCodeExecutionToolResultErrorErrorCodeUnavailable BetaBashCodeExecutionToolResultErrorErrorCode = "unavailable"`

            - `const BetaBashCodeExecutionToolResultErrorErrorCodeTooManyRequests BetaBashCodeExecutionToolResultErrorErrorCode = "too_many_requests"`

            - `const BetaBashCodeExecutionToolResultErrorErrorCodeExecutionTimeExceeded BetaBashCodeExecutionToolResultErrorErrorCode = "execution_time_exceeded"`

            - `const BetaBashCodeExecutionToolResultErrorErrorCodeOutputFileTooLarge BetaBashCodeExecutionToolResultErrorErrorCode = "output_file_too_large"`

          - `Type BashCodeExecutionToolResultError`

            - `const BashCodeExecutionToolResultErrorBashCodeExecutionToolResultError BashCodeExecutionToolResultError = "bash_code_execution_tool_result_error"`

        - `type BetaBashCodeExecutionResultBlock struct{…}`

          - `Content []BetaBashCodeExecutionOutputBlock`

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

    - `type BetaTextEditorCodeExecutionToolResultBlock struct{…}`

      - `Content BetaTextEditorCodeExecutionToolResultBlockContentUnion`

        - `type BetaTextEditorCodeExecutionToolResultError struct{…}`

          - `ErrorCode BetaTextEditorCodeExecutionToolResultErrorErrorCode`

            - `const BetaTextEditorCodeExecutionToolResultErrorErrorCodeInvalidToolInput BetaTextEditorCodeExecutionToolResultErrorErrorCode = "invalid_tool_input"`

            - `const BetaTextEditorCodeExecutionToolResultErrorErrorCodeUnavailable BetaTextEditorCodeExecutionToolResultErrorErrorCode = "unavailable"`

            - `const BetaTextEditorCodeExecutionToolResultErrorErrorCodeTooManyRequests BetaTextEditorCodeExecutionToolResultErrorErrorCode = "too_many_requests"`

            - `const BetaTextEditorCodeExecutionToolResultErrorErrorCodeExecutionTimeExceeded BetaTextEditorCodeExecutionToolResultErrorErrorCode = "execution_time_exceeded"`

            - `const BetaTextEditorCodeExecutionToolResultErrorErrorCodeFileNotFound BetaTextEditorCodeExecutionToolResultErrorErrorCode = "file_not_found"`

          - `ErrorMessage string`

          - `Type TextEditorCodeExecutionToolResultError`

            - `const TextEditorCodeExecutionToolResultErrorTextEditorCodeExecutionToolResultError TextEditorCodeExecutionToolResultError = "text_editor_code_execution_tool_result_error"`

        - `type BetaTextEditorCodeExecutionViewResultBlock struct{…}`

          - `Content string`

          - `FileType BetaTextEditorCodeExecutionViewResultBlockFileType`

            - `const BetaTextEditorCodeExecutionViewResultBlockFileTypeText BetaTextEditorCodeExecutionViewResultBlockFileType = "text"`

            - `const BetaTextEditorCodeExecutionViewResultBlockFileTypeImage BetaTextEditorCodeExecutionViewResultBlockFileType = "image"`

            - `const BetaTextEditorCodeExecutionViewResultBlockFileTypePDF BetaTextEditorCodeExecutionViewResultBlockFileType = "pdf"`

          - `NumLines int64`

          - `StartLine int64`

          - `TotalLines int64`

          - `Type TextEditorCodeExecutionViewResult`

            - `const TextEditorCodeExecutionViewResultTextEditorCodeExecutionViewResult TextEditorCodeExecutionViewResult = "text_editor_code_execution_view_result"`

        - `type BetaTextEditorCodeExecutionCreateResultBlock struct{…}`

          - `IsFileUpdate bool`

          - `Type TextEditorCodeExecutionCreateResult`

            - `const TextEditorCodeExecutionCreateResultTextEditorCodeExecutionCreateResult TextEditorCodeExecutionCreateResult = "text_editor_code_execution_create_result"`

        - `type BetaTextEditorCodeExecutionStrReplaceResultBlock struct{…}`

          - `Lines []string`

          - `NewLines int64`

          - `NewStart int64`

          - `OldLines int64`

          - `OldStart int64`

          - `Type TextEditorCodeExecutionStrReplaceResult`

            - `const TextEditorCodeExecutionStrReplaceResultTextEditorCodeExecutionStrReplaceResult TextEditorCodeExecutionStrReplaceResult = "text_editor_code_execution_str_replace_result"`

      - `ToolUseID string`

      - `Type TextEditorCodeExecutionToolResult`

        - `const TextEditorCodeExecutionToolResultTextEditorCodeExecutionToolResult TextEditorCodeExecutionToolResult = "text_editor_code_execution_tool_result"`

    - `type BetaToolSearchToolResultBlock struct{…}`

      - `Content BetaToolSearchToolResultBlockContentUnion`

        - `type BetaToolSearchToolResultError struct{…}`

          - `ErrorCode BetaToolSearchToolResultErrorErrorCode`

            - `const BetaToolSearchToolResultErrorErrorCodeInvalidToolInput BetaToolSearchToolResultErrorErrorCode = "invalid_tool_input"`

            - `const BetaToolSearchToolResultErrorErrorCodeUnavailable BetaToolSearchToolResultErrorErrorCode = "unavailable"`

            - `const BetaToolSearchToolResultErrorErrorCodeTooManyRequests BetaToolSearchToolResultErrorErrorCode = "too_many_requests"`

            - `const BetaToolSearchToolResultErrorErrorCodeExecutionTimeExceeded BetaToolSearchToolResultErrorErrorCode = "execution_time_exceeded"`

          - `ErrorMessage string`

          - `Type ToolSearchToolResultError`

            - `const ToolSearchToolResultErrorToolSearchToolResultError ToolSearchToolResultError = "tool_search_tool_result_error"`

        - `type BetaToolSearchToolSearchResultBlock struct{…}`

          - `ToolReferences []BetaToolReferenceBlock`

            - `ToolName string`

            - `Type ToolReference`

              - `const ToolReferenceToolReference ToolReference = "tool_reference"`

          - `Type ToolSearchToolSearchResult`

            - `const ToolSearchToolSearchResultToolSearchToolSearchResult ToolSearchToolSearchResult = "tool_search_tool_search_result"`

      - `ToolUseID string`

      - `Type ToolSearchToolResult`

        - `const ToolSearchToolResultToolSearchToolResult ToolSearchToolResult = "tool_search_tool_result"`

    - `type BetaMCPToolUseBlock struct{…}`

      - `ID string`

      - `Input map[string, any]`

      - `Name string`

        The name of the MCP tool

      - `ServerName string`

        The name of the MCP server

      - `Type MCPToolUse`

        - `const MCPToolUseMCPToolUse MCPToolUse = "mcp_tool_use"`

    - `type BetaMCPToolResultBlock struct{…}`

      - `Content BetaMCPToolResultBlockContentUnion`

        - `string`

        - `type BetaMCPToolResultBlockContentBetaMCPToolResultBlockContent []BetaTextBlock`

          - `Citations []BetaTextCitationUnion`

            Citations supporting the text block.

            The type of citation returned will depend on the type of document being cited. Citing a PDF results in `page_location`, plain text results in `char_location`, and content document results in `content_block_location`.

            - `type BetaCitationCharLocation struct{…}`

              - `CitedText string`

              - `DocumentIndex int64`

              - `DocumentTitle string`

              - `EndCharIndex int64`

              - `FileID string`

              - `StartCharIndex int64`

              - `Type CharLocation`

                - `const CharLocationCharLocation CharLocation = "char_location"`

            - `type BetaCitationPageLocation struct{…}`

              - `CitedText string`

              - `DocumentIndex int64`

              - `DocumentTitle string`

              - `EndPageNumber int64`

              - `FileID string`

              - `StartPageNumber int64`

              - `Type PageLocation`

                - `const PageLocationPageLocation PageLocation = "page_location"`

            - `type BetaCitationContentBlockLocation struct{…}`

              - `CitedText string`

              - `DocumentIndex int64`

              - `DocumentTitle string`

              - `EndBlockIndex int64`

              - `FileID string`

              - `StartBlockIndex int64`

              - `Type ContentBlockLocation`

                - `const ContentBlockLocationContentBlockLocation ContentBlockLocation = "content_block_location"`

            - `type BetaCitationsWebSearchResultLocation struct{…}`

              - `CitedText string`

              - `EncryptedIndex string`

              - `Title string`

              - `Type WebSearchResultLocation`

                - `const WebSearchResultLocationWebSearchResultLocation WebSearchResultLocation = "web_search_result_location"`

              - `URL string`

            - `type BetaCitationSearchResultLocation struct{…}`

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

      - `IsError bool`

      - `ToolUseID string`

      - `Type MCPToolResult`

        - `const MCPToolResultMCPToolResult MCPToolResult = "mcp_tool_result"`

    - `type BetaContainerUploadBlock struct{…}`

      Response model for a file uploaded to the container.

      - `FileID string`

      - `Type ContainerUpload`

        - `const ContainerUploadContainerUpload ContainerUpload = "container_upload"`

  - `ContextManagement BetaContextManagementResponse`

    Context management response.

    Information about context management strategies applied during the request.

    - `AppliedEdits []BetaContextManagementResponseAppliedEditUnion`

      List of context management edits that were applied.

      - `type BetaClearToolUses20250919EditResponse struct{…}`

        - `ClearedInputTokens int64`

          Number of input tokens cleared by this edit.

        - `ClearedToolUses int64`

          Number of tool uses that were cleared.

        - `Type ClearToolUses20250919`

          The type of context management edit applied.

          - `const ClearToolUses20250919ClearToolUses20250919 ClearToolUses20250919 = "clear_tool_uses_20250919"`

      - `type BetaClearThinking20251015EditResponse struct{…}`

        - `ClearedInputTokens int64`

          Number of input tokens cleared by this edit.

        - `ClearedThinkingTurns int64`

          Number of thinking turns that were cleared.

        - `Type ClearThinking20251015`

          The type of context management edit applied.

          - `const ClearThinking20251015ClearThinking20251015 ClearThinking20251015 = "clear_thinking_20251015"`

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

  - `StopReason BetaStopReason`

    The reason that we stopped.

    This may be one the following values:

    * `"end_turn"`: the model reached a natural stopping point
    * `"max_tokens"`: we exceeded the requested `max_tokens` or the model's maximum
    * `"stop_sequence"`: one of your provided custom `stop_sequences` was generated
    * `"tool_use"`: the model invoked one or more tools
    * `"pause_turn"`: we paused a long-running turn. You may provide the response back as-is in a subsequent request to let the model continue.
    * `"refusal"`: when streaming classifiers intervene to handle potential policy violations

    In non-streaming mode this value is always non-null. In streaming mode, it is null in the `message_start` event and non-null otherwise.

    - `const BetaStopReasonEndTurn BetaStopReason = "end_turn"`

    - `const BetaStopReasonMaxTokens BetaStopReason = "max_tokens"`

    - `const BetaStopReasonStopSequence BetaStopReason = "stop_sequence"`

    - `const BetaStopReasonToolUse BetaStopReason = "tool_use"`

    - `const BetaStopReasonPauseTurn BetaStopReason = "pause_turn"`

    - `const BetaStopReasonRefusal BetaStopReason = "refusal"`

    - `const BetaStopReasonModelContextWindowExceeded BetaStopReason = "model_context_window_exceeded"`

  - `StopSequence string`

    Which custom stop sequence was generated, if any.

    This value will be a non-null string if one of your custom stop sequences was generated.

  - `Type Message`

    Object type.

    For Messages, this is always `"message"`.

    - `const MessageMessage Message = "message"`

  - `Usage BetaUsage`

    Billing and rate-limit usage.

    Anthropic's API bills and rate-limits by token counts, as tokens represent the underlying cost to our systems.

    Under the hood, the API transforms requests into a format suitable for the model. The model's output then goes through a parsing stage before becoming an API response. As a result, the token counts in `usage` will not match one-to-one with the exact visible content of an API request or response.

    For example, `output_tokens` will be non-zero, even for an empty string response from Claude.

    Total input tokens in a request is the summation of `input_tokens`, `cache_creation_input_tokens`, and `cache_read_input_tokens`.

    - `CacheCreation BetaCacheCreation`

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

    - `ServerToolUse BetaServerToolUsage`

      The number of server tool requests.

      - `WebFetchRequests int64`

        The number of web fetch tool requests.

      - `WebSearchRequests int64`

        The number of web search tool requests.

    - `ServiceTier BetaUsageServiceTier`

      If the request used the priority, standard, or batch tier.

      - `const BetaUsageServiceTierStandard BetaUsageServiceTier = "standard"`

      - `const BetaUsageServiceTierPriority BetaUsageServiceTier = "priority"`

      - `const BetaUsageServiceTierBatch BetaUsageServiceTier = "batch"`

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
  betaMessage, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
    MaxTokens: 1024,
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
  fmt.Printf("%+v\n", betaMessage.ID)
}
```
