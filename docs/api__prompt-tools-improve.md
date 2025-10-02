# Improve a prompt

> Create a new-and-improved prompt guided by feedback

## OpenAPI

````yaml post /v1/experimental/improve_prompt
paths:
  path: /v1/experimental/improve_prompt
  method: post
  servers:
    - url: https://api.anthropic.com
  request:
    security: []
    parameters:
      path: {}
      query: {}
      header:
        anthropic-beta:
          schema:
            - type: array
              items:
                allOf:
                  - type: string
              required: false
              title: Anthropic-Beta
              description: >-
                Optional header to specify the beta version(s) you want to use.


                To use multiple betas, use a comma separated list like
                `beta1,beta2` or specify the header multiple times for each
                beta.
        x-api-key:
          schema:
            - type: string
              required: true
              title: X-Api-Key
              description: >-
                Your unique API key for authentication.


                This key is required in the header of all API requests, to
                authenticate your account and access Anthropic's services. Get
                your API key through the
                [Console](https://console.anthropic.com/settings/keys). Each key
                is scoped to a Workspace.
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              feedback:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    default: null
                    description: >-
                      Feedback for improving the prompt.


                      Use this parameter to share specific guidance on what
                      aspects of the prompt should be enhanced or modified.


                      Example:

                      ```json

                      {
                        "messages": [...],
                        "feedback": "Make the recipes shorter"
                      }

                      ```


                      When not set, the API will improve the prompt using
                      general prompt engineering best practices.
                    examples:
                      - Make it more detailed and include cooking times
                    title: Feedback
              messages:
                allOf:
                  - description: >-
                      The prompt to improve, structured as a list of `message`
                      objects.


                      Each message in the `messages` array must:

                      - Contain only text-only content blocks

                      - Not include tool calls, images, or prompt caching blocks


                      As a simple text prompt:


                      ```json

                      [
                        {
                          "role": "user", 
                          "content": [
                            {
                              "type": "text",
                              "text": "Concise recipe for {{food}}"
                            }
                          ]
                        }
                      ]

                      ```


                      With example interactions to guide improvement:


                      ```json

                      [
                        {
                          "role": "user", 
                          "content": [
                            {
                              "type": "text",
                              "text": "Concise for {{food}}.\n\nexample\mandu: Put the mandu in the air fryer at 380F for 7 minutes."
                            }
                          ]
                        }
                      ]

                      ```


                      Note that only contiguous user messages with text content
                      are allowed. Assistant prefill is permitted, but other
                      content types will cause validation errors.
                    examples:
                      - - content:
                            - text: <generated prompt>
                              type: text
                          role: user
                    items:
                      $ref: '#/components/schemas/InputMessage'
                    title: Messages
                    type: array
              system:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    default: null
                    description: >-
                      The existing system prompt to incorporate, if any.


                      ```json

                      {
                        "system": "You are a professional meal prep chef",
                        [...]
                      }

                      ```


                      Note that while system prompts typically appear as
                      separate parameters in standard API calls, in the
                      `improve_prompt` response, the system content will be
                      incorporated directly into the returned user message.
                    examples:
                      - You are a professional chef
                    title: System
              target_model:
                allOf:
                  - anyOf:
                      - maxLength: 256
                        minLength: 1
                        type: string
                      - type: 'null'
                    default: ''
                    description: >-
                      The model this prompt will be used for. This optional
                      parameter helps us understand which models our prompt
                      tools are being used with, but it doesn't currently affect
                      functionality.


                      Example:

                      ```

                      "claude-3-7-sonnet-20250219"

                      ```
                    examples:
                      - claude-3-7-sonnet-20250219
                    title: Target Model
            required: true
            title: ImprovePromptParams
            refIdentifier: '#/components/schemas/ImprovePromptParams'
            requiredProperties:
              - messages
        examples:
          example:
            value:
              feedback: Make it more detailed and include cooking times
              messages:
                - content:
                    - text: <generated prompt>
                      type: text
                  role: user
              system: You are a professional chef
              target_model: claude-3-7-sonnet-20250219
    codeSamples:
      - lang: bash
        source: >-
          curl -X POST https://api.anthropic.com/v1/experimental/improve_prompt
          \
               --header "x-api-key: $ANTHROPIC_API_KEY" \
               --header "anthropic-version: 2023-06-01" \
               --header "anthropic-beta: prompt-tools-2025-04-02" \
               --header "content-type: application/json" \
               --data \
          '{
              "messages": [{"role": "user", "content": [{"type": "text", "text": "Create a recipe for {{food}}"}]}],
              "system": "You are a professional chef",
              "feedback": "Make it more detailed and include cooking times",
              "target_model": "claude-3-7-sonnet-20250219"
          }'
      - lang: python
        source: |-
          import requests

          response = requests.post(
              "https://api.anthropic.com/v1/experimental/improve_prompt",
              headers={
                  "Content-Type": "application/json", 
                  "x-api-key": "$ANTHROPIC_API_KEY",
                  "anthropic-version": "2023-06-01",
                  "anthropic-beta": "prompt-tools-2025-04-02"
              },
              json={
                  "messages": [{"role": "user", "content": [{"type": "text", "text": "Create a recipe for {{food}}"}]}],
                  "system": "You are a professional chef",
                  "feedback": "Make it more detailed and include cooking times",
                  "target_model": "claude-3-7-sonnet-20250219"
              }
          )
      - lang: javascript
        source: >-
          const response = await
          fetch('https://api.anthropic.com/v1/experimental/improve_prompt', {
            method: 'POST',
            headers: {
              'x-api-key': '$ANTHROPIC_API_KEY',
              'anthropic-version': '2023-06-01',
              'anthropic-beta': 'prompt-tools-2025-04-02',
              'content-type': 'application/json'
            },
            body: JSON.stringify({
              'messages': [{"role": "user", "content": [{"type": "text", "text": "Create a recipe for {{food}}"}]}],
              'system': "You are a professional chef",
              'feedback': "Make it more detailed and include cooking times",
              'target_model': "claude-3-7-sonnet-20250219"
            })
          });


          const data = await response.json();
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              messages:
                allOf:
                  - description: >-
                      Contains the result of the prompt improvement process in a
                      list of `message` objects.


                      Includes a `user`-role message with the improved prompt
                      text and may optionally include an `assistant`-role
                      message with a prefill. These messages follow the standard
                      Messages API format and can be used directly in subsequent
                      API calls.
                    examples:
                      - - content:
                            - text: <improved prompt>
                              type: text
                          role: user
                        - content:
                            - text: <assistant prefill>
                              type: text
                          role: assistant
                    items:
                      $ref: '#/components/schemas/InputMessage'
                    title: Messages
                    type: array
              system:
                allOf:
                  - description: >-
                      Currently, the `system` field is always returned as an
                      empty string (""). In future iterations, this field may
                      contain generated system prompts.


                      Directions similar to what would normally be included in a
                      system prompt are included in `messages` when improving a
                      prompt.
                    examples:
                      - ''
                    title: System
                    type: string
              usage:
                allOf:
                  - $ref: '#/components/schemas/Usage'
                    description: Usage information
                    examples:
                      - - input_tokens: 490
                          output_tokens: 661
            title: ImprovePromptResponse
            refIdentifier: '#/components/schemas/ImprovePromptResponse'
            requiredProperties:
              - messages
              - system
              - usage
        examples:
          example:
            value:
              messages:
                - content:
                    - text: <improved prompt>
                      type: text
                  role: user
                - content:
                    - text: <assistant prefill>
                      type: text
                  role: assistant
              system: ''
              usage:
                - input_tokens: 490
                  output_tokens: 661
        description: Successful Response
    4XX:
      application/json:
        schemaArray:
          - type: object
            properties:
              error:
                allOf:
                  - discriminator:
                      mapping:
                        api_error: '#/components/schemas/APIError'
                        authentication_error: '#/components/schemas/AuthenticationError'
                        billing_error: '#/components/schemas/BillingError'
                        invalid_request_error: '#/components/schemas/InvalidRequestError'
                        not_found_error: '#/components/schemas/NotFoundError'
                        overloaded_error: '#/components/schemas/OverloadedError'
                        permission_error: '#/components/schemas/PermissionError'
                        rate_limit_error: '#/components/schemas/RateLimitError'
                        timeout_error: '#/components/schemas/GatewayTimeoutError'
                      propertyName: type
                    oneOf:
                      - $ref: '#/components/schemas/InvalidRequestError'
                      - $ref: '#/components/schemas/AuthenticationError'
                      - $ref: '#/components/schemas/BillingError'
                      - $ref: '#/components/schemas/PermissionError'
                      - $ref: '#/components/schemas/NotFoundError'
                      - $ref: '#/components/schemas/RateLimitError'
                      - $ref: '#/components/schemas/GatewayTimeoutError'
                      - $ref: '#/components/schemas/APIError'
                      - $ref: '#/components/schemas/OverloadedError'
                    title: Error
              request_id:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    default: null
                    title: Request Id
              type:
                allOf:
                  - const: error
                    default: error
                    enum:
                      - error
                    title: Type
                    type: string
            title: ErrorResponse
            refIdentifier: '#/components/schemas/ErrorResponse'
            requiredProperties:
              - error
              - request_id
              - type
        examples:
          example:
            value:
              error:
                message: Invalid request
                type: invalid_request_error
              request_id: <string>
              type: error
        description: >-
          Error response.


          See our [errors documentation](https://docs.claude.com/en/api/errors)
          for more details.
  deprecated: false
  type: path
components:
  schemas:
    APIError:
      properties:
        message:
          default: Internal server error
          title: Message
          type: string
        type:
          const: api_error
          default: api_error
          enum:
            - api_error
          title: Type
          type: string
      required:
        - message
        - type
      title: APIError
      type: object
    AuthenticationError:
      properties:
        message:
          default: Authentication error
          title: Message
          type: string
        type:
          const: authentication_error
          default: authentication_error
          enum:
            - authentication_error
          title: Type
          type: string
      required:
        - message
        - type
      title: AuthenticationError
      type: object
    Base64ImageSource:
      additionalProperties: false
      properties:
        data:
          format: byte
          title: Data
          type: string
        media_type:
          enum:
            - image/jpeg
            - image/png
            - image/gif
            - image/webp
          title: Media Type
          type: string
        type:
          const: base64
          enum:
            - base64
          title: Type
          type: string
      required:
        - data
        - media_type
        - type
      title: Base64ImageSource
      type: object
    Base64PDFSource:
      additionalProperties: false
      properties:
        data:
          format: byte
          title: Data
          type: string
        media_type:
          const: application/pdf
          enum:
            - application/pdf
          title: Media Type
          type: string
        type:
          const: base64
          enum:
            - base64
          title: Type
          type: string
      required:
        - data
        - media_type
        - type
      title: PDF (base64)
      type: object
    BashCodeExecutionToolResultErrorCode:
      enum:
        - invalid_tool_input
        - unavailable
        - too_many_requests
        - execution_time_exceeded
        - output_file_too_large
      title: BashCodeExecutionToolResultErrorCode
      type: string
    BillingError:
      properties:
        message:
          default: Billing error
          title: Message
          type: string
        type:
          const: billing_error
          default: billing_error
          enum:
            - billing_error
          title: Type
          type: string
      required:
        - message
        - type
      title: BillingError
      type: object
    CacheControlEphemeral:
      additionalProperties: false
      properties:
        ttl:
          description: |-
            The time-to-live for the cache control breakpoint.

            This may be one the following values:
            - `5m`: 5 minutes
            - `1h`: 1 hour

            Defaults to `5m`.
          enum:
            - 5m
            - 1h
          title: Ttl
          type: string
        type:
          const: ephemeral
          enum:
            - ephemeral
          title: Type
          type: string
      required:
        - type
      title: CacheControlEphemeral
      type: object
    CacheCreation:
      properties:
        ephemeral_1h_input_tokens:
          default: 0
          description: The number of input tokens used to create the 1 hour cache entry.
          minimum: 0
          title: Ephemeral 1H Input Tokens
          type: integer
        ephemeral_5m_input_tokens:
          default: 0
          description: The number of input tokens used to create the 5 minute cache entry.
          minimum: 0
          title: Ephemeral 5M Input Tokens
          type: integer
      required:
        - ephemeral_1h_input_tokens
        - ephemeral_5m_input_tokens
      title: CacheCreation
      type: object
    CodeExecutionToolResultErrorCode:
      enum:
        - invalid_tool_input
        - unavailable
        - too_many_requests
        - execution_time_exceeded
      title: CodeExecutionToolResultErrorCode
      type: string
    ContentBlockSource:
      additionalProperties: false
      properties:
        content:
          anyOf:
            - type: string
            - items:
                discriminator:
                  mapping:
                    image: '#/components/schemas/RequestImageBlock'
                    text: '#/components/schemas/RequestTextBlock'
                  propertyName: type
                oneOf:
                  - $ref: '#/components/schemas/RequestTextBlock'
                  - $ref: '#/components/schemas/RequestImageBlock'
              type: array
          title: Content
        type:
          const: content
          enum:
            - content
          title: Type
          type: string
      required:
        - content
        - type
      title: Content block
      type: object
    FileDocumentSource:
      additionalProperties: false
      properties:
        file_id:
          title: File Id
          type: string
        type:
          const: file
          enum:
            - file
          title: Type
          type: string
      required:
        - file_id
        - type
      title: File document
      type: object
    FileImageSource:
      additionalProperties: false
      properties:
        file_id:
          title: File Id
          type: string
        type:
          const: file
          enum:
            - file
          title: Type
          type: string
      required:
        - file_id
        - type
      title: FileImageSource
      type: object
    GatewayTimeoutError:
      properties:
        message:
          default: Request timeout
          title: Message
          type: string
        type:
          const: timeout_error
          default: timeout_error
          enum:
            - timeout_error
          title: Type
          type: string
      required:
        - message
        - type
      title: GatewayTimeoutError
      type: object
    InputMessage:
      additionalProperties: false
      properties:
        content:
          anyOf:
            - type: string
            - items:
                discriminator:
                  mapping:
                    bash_code_execution_tool_result: >-
                      #/components/schemas/RequestBashCodeExecutionToolResultBlock
                    code_execution_tool_result: '#/components/schemas/RequestCodeExecutionToolResultBlock'
                    container_upload: '#/components/schemas/RequestContainerUploadBlock'
                    document: '#/components/schemas/RequestDocumentBlock'
                    image: '#/components/schemas/RequestImageBlock'
                    mcp_tool_result: '#/components/schemas/RequestMCPToolResultBlock'
                    mcp_tool_use: '#/components/schemas/RequestMCPToolUseBlock'
                    redacted_thinking: '#/components/schemas/RequestRedactedThinkingBlock'
                    search_result: '#/components/schemas/RequestSearchResultBlock'
                    server_tool_use: '#/components/schemas/RequestServerToolUseBlock'
                    text: '#/components/schemas/RequestTextBlock'
                    text_editor_code_execution_tool_result: >-
                      #/components/schemas/RequestTextEditorCodeExecutionToolResultBlock
                    thinking: '#/components/schemas/RequestThinkingBlock'
                    tool_result: '#/components/schemas/RequestToolResultBlock'
                    tool_use: '#/components/schemas/RequestToolUseBlock'
                    web_fetch_tool_result: '#/components/schemas/RequestWebFetchToolResultBlock'
                    web_search_tool_result: '#/components/schemas/RequestWebSearchToolResultBlock'
                  propertyName: type
                oneOf:
                  - $ref: '#/components/schemas/RequestTextBlock'
                    description: Regular text content.
                  - $ref: '#/components/schemas/RequestImageBlock'
                    description: >-
                      Image content specified directly as base64 data or as a
                      reference via a URL.
                  - $ref: '#/components/schemas/RequestDocumentBlock'
                    description: >-
                      Document content, either specified directly as base64
                      data, as text, or as a reference via a URL.
                  - $ref: '#/components/schemas/RequestSearchResultBlock'
                    description: >-
                      A search result block containing source, title, and
                      content from search operations.
                  - $ref: '#/components/schemas/RequestThinkingBlock'
                    description: A block specifying internal thinking by the model.
                  - $ref: '#/components/schemas/RequestRedactedThinkingBlock'
                    description: >-
                      A block specifying internal, redacted thinking by the
                      model.
                  - $ref: '#/components/schemas/RequestToolUseBlock'
                    description: A block indicating a tool use by the model.
                  - $ref: '#/components/schemas/RequestToolResultBlock'
                    description: A block specifying the results of a tool use by the model.
                  - $ref: '#/components/schemas/RequestServerToolUseBlock'
                  - $ref: '#/components/schemas/RequestWebSearchToolResultBlock'
                  - $ref: '#/components/schemas/RequestWebFetchToolResultBlock'
                  - $ref: '#/components/schemas/RequestCodeExecutionToolResultBlock'
                  - $ref: >-
                      #/components/schemas/RequestBashCodeExecutionToolResultBlock
                  - $ref: >-
                      #/components/schemas/RequestTextEditorCodeExecutionToolResultBlock
                  - $ref: '#/components/schemas/RequestMCPToolUseBlock'
                  - $ref: '#/components/schemas/RequestMCPToolResultBlock'
                  - $ref: '#/components/schemas/RequestContainerUploadBlock'
              type: array
          title: Content
        role:
          enum:
            - user
            - assistant
          title: Role
          type: string
      required:
        - content
        - role
      title: InputMessage
      type: object
    InvalidRequestError:
      properties:
        message:
          default: Invalid request
          title: Message
          type: string
        type:
          const: invalid_request_error
          default: invalid_request_error
          enum:
            - invalid_request_error
          title: Type
          type: string
      required:
        - message
        - type
      title: InvalidRequestError
      type: object
    NotFoundError:
      properties:
        message:
          default: Not found
          title: Message
          type: string
        type:
          const: not_found_error
          default: not_found_error
          enum:
            - not_found_error
          title: Type
          type: string
      required:
        - message
        - type
      title: NotFoundError
      type: object
    OverloadedError:
      properties:
        message:
          default: Overloaded
          title: Message
          type: string
        type:
          const: overloaded_error
          default: overloaded_error
          enum:
            - overloaded_error
          title: Type
          type: string
      required:
        - message
        - type
      title: OverloadedError
      type: object
    PermissionError:
      properties:
        message:
          default: Permission denied
          title: Message
          type: string
        type:
          const: permission_error
          default: permission_error
          enum:
            - permission_error
          title: Type
          type: string
      required:
        - message
        - type
      title: PermissionError
      type: object
    PlainTextSource:
      additionalProperties: false
      properties:
        data:
          title: Data
          type: string
        media_type:
          const: text/plain
          enum:
            - text/plain
          title: Media Type
          type: string
        type:
          const: text
          enum:
            - text
          title: Type
          type: string
      required:
        - data
        - media_type
        - type
      title: Plain text
      type: object
    RateLimitError:
      properties:
        message:
          default: Rate limited
          title: Message
          type: string
        type:
          const: rate_limit_error
          default: rate_limit_error
          enum:
            - rate_limit_error
          title: Type
          type: string
      required:
        - message
        - type
      title: RateLimitError
      type: object
    RequestBashCodeExecutionOutputBlock:
      additionalProperties: false
      properties:
        file_id:
          title: File Id
          type: string
        type:
          const: bash_code_execution_output
          enum:
            - bash_code_execution_output
          title: Type
          type: string
      required:
        - file_id
        - type
      title: RequestBashCodeExecutionOutputBlock
      type: object
    RequestBashCodeExecutionResultBlock:
      additionalProperties: false
      properties:
        content:
          items:
            $ref: '#/components/schemas/RequestBashCodeExecutionOutputBlock'
          title: Content
          type: array
        return_code:
          title: Return Code
          type: integer
        stderr:
          title: Stderr
          type: string
        stdout:
          title: Stdout
          type: string
        type:
          const: bash_code_execution_result
          enum:
            - bash_code_execution_result
          title: Type
          type: string
      required:
        - content
        - return_code
        - stderr
        - stdout
        - type
      title: RequestBashCodeExecutionResultBlock
      type: object
    RequestBashCodeExecutionToolResultBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        content:
          anyOf:
            - $ref: '#/components/schemas/RequestBashCodeExecutionToolResultError'
            - $ref: '#/components/schemas/RequestBashCodeExecutionResultBlock'
          title: Content
        tool_use_id:
          pattern: ^srvtoolu_[a-zA-Z0-9_]+$
          title: Tool Use Id
          type: string
        type:
          const: bash_code_execution_tool_result
          enum:
            - bash_code_execution_tool_result
          title: Type
          type: string
      required:
        - content
        - tool_use_id
        - type
      title: RequestBashCodeExecutionToolResultBlock
      type: object
    RequestBashCodeExecutionToolResultError:
      additionalProperties: false
      properties:
        error_code:
          $ref: '#/components/schemas/BashCodeExecutionToolResultErrorCode'
        type:
          const: bash_code_execution_tool_result_error
          enum:
            - bash_code_execution_tool_result_error
          title: Type
          type: string
      required:
        - error_code
        - type
      title: RequestBashCodeExecutionToolResultError
      type: object
    RequestCharLocationCitation:
      additionalProperties: false
      properties:
        cited_text:
          title: Cited Text
          type: string
        document_index:
          minimum: 0
          title: Document Index
          type: integer
        document_title:
          anyOf:
            - maxLength: 255
              minLength: 1
              type: string
            - type: 'null'
          title: Document Title
        end_char_index:
          title: End Char Index
          type: integer
        start_char_index:
          minimum: 0
          title: Start Char Index
          type: integer
        type:
          const: char_location
          enum:
            - char_location
          title: Type
          type: string
      required:
        - cited_text
        - document_index
        - document_title
        - end_char_index
        - start_char_index
        - type
      title: Character location
      type: object
    RequestCitationsConfig:
      additionalProperties: false
      properties:
        enabled:
          title: Enabled
          type: boolean
      title: RequestCitationsConfig
      type: object
    RequestCodeExecutionOutputBlock:
      additionalProperties: false
      properties:
        file_id:
          title: File Id
          type: string
        type:
          const: code_execution_output
          enum:
            - code_execution_output
          title: Type
          type: string
      required:
        - file_id
        - type
      title: RequestCodeExecutionOutputBlock
      type: object
    RequestCodeExecutionResultBlock:
      additionalProperties: false
      properties:
        content:
          items:
            $ref: '#/components/schemas/RequestCodeExecutionOutputBlock'
          title: Content
          type: array
        return_code:
          title: Return Code
          type: integer
        stderr:
          title: Stderr
          type: string
        stdout:
          title: Stdout
          type: string
        type:
          const: code_execution_result
          enum:
            - code_execution_result
          title: Type
          type: string
      required:
        - content
        - return_code
        - stderr
        - stdout
        - type
      title: Code execution result
      type: object
    RequestCodeExecutionToolResultBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        content:
          anyOf:
            - $ref: '#/components/schemas/RequestCodeExecutionToolResultError'
            - $ref: '#/components/schemas/RequestCodeExecutionResultBlock'
          title: Content
        tool_use_id:
          pattern: ^srvtoolu_[a-zA-Z0-9_]+$
          title: Tool Use Id
          type: string
        type:
          const: code_execution_tool_result
          enum:
            - code_execution_tool_result
          title: Type
          type: string
      required:
        - content
        - tool_use_id
        - type
      title: Code execution tool result
      type: object
    RequestCodeExecutionToolResultError:
      additionalProperties: false
      properties:
        error_code:
          $ref: '#/components/schemas/CodeExecutionToolResultErrorCode'
        type:
          const: code_execution_tool_result_error
          enum:
            - code_execution_tool_result_error
          title: Type
          type: string
      required:
        - error_code
        - type
      title: Code execution tool error
      type: object
    RequestContainerUploadBlock:
      additionalProperties: false
      description: >-
        A content block that represents a file to be uploaded to the container

        Files uploaded via this block will be available in the container's input
        directory.
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        file_id:
          title: File Id
          type: string
        type:
          const: container_upload
          enum:
            - container_upload
          title: Type
          type: string
      required:
        - file_id
        - type
      title: Container upload
      type: object
    RequestContentBlockLocationCitation:
      additionalProperties: false
      properties:
        cited_text:
          title: Cited Text
          type: string
        document_index:
          minimum: 0
          title: Document Index
          type: integer
        document_title:
          anyOf:
            - maxLength: 255
              minLength: 1
              type: string
            - type: 'null'
          title: Document Title
        end_block_index:
          title: End Block Index
          type: integer
        start_block_index:
          minimum: 0
          title: Start Block Index
          type: integer
        type:
          const: content_block_location
          enum:
            - content_block_location
          title: Type
          type: string
      required:
        - cited_text
        - document_index
        - document_title
        - end_block_index
        - start_block_index
        - type
      title: Content block location
      type: object
    RequestDocumentBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        citations:
          anyOf:
            - $ref: '#/components/schemas/RequestCitationsConfig'
            - type: 'null'
        context:
          anyOf:
            - minLength: 1
              type: string
            - type: 'null'
          title: Context
        source:
          discriminator:
            mapping:
              base64: '#/components/schemas/Base64PDFSource'
              content: '#/components/schemas/ContentBlockSource'
              file: '#/components/schemas/FileDocumentSource'
              text: '#/components/schemas/PlainTextSource'
              url: '#/components/schemas/URLPDFSource'
            propertyName: type
          oneOf:
            - $ref: '#/components/schemas/Base64PDFSource'
            - $ref: '#/components/schemas/PlainTextSource'
            - $ref: '#/components/schemas/ContentBlockSource'
            - $ref: '#/components/schemas/URLPDFSource'
            - $ref: '#/components/schemas/FileDocumentSource'
        title:
          anyOf:
            - maxLength: 500
              minLength: 1
              type: string
            - type: 'null'
          title: Title
        type:
          const: document
          enum:
            - document
          title: Type
          type: string
      required:
        - source
        - type
      title: Document
      type: object
    RequestImageBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        source:
          discriminator:
            mapping:
              base64: '#/components/schemas/Base64ImageSource'
              file: '#/components/schemas/FileImageSource'
              url: '#/components/schemas/URLImageSource'
            propertyName: type
          oneOf:
            - $ref: '#/components/schemas/Base64ImageSource'
            - $ref: '#/components/schemas/URLImageSource'
            - $ref: '#/components/schemas/FileImageSource'
          title: Source
        type:
          const: image
          enum:
            - image
          title: Type
          type: string
      required:
        - source
        - type
      title: Image
      type: object
    RequestMCPToolResultBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        content:
          anyOf:
            - type: string
            - items:
                $ref: '#/components/schemas/RequestTextBlock'
              type: array
          title: Content
        is_error:
          title: Is Error
          type: boolean
        tool_use_id:
          pattern: ^[a-zA-Z0-9_-]+$
          title: Tool Use Id
          type: string
        type:
          const: mcp_tool_result
          enum:
            - mcp_tool_result
          title: Type
          type: string
      required:
        - tool_use_id
        - type
      title: MCP tool result
      type: object
    RequestMCPToolUseBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        id:
          pattern: ^[a-zA-Z0-9_-]+$
          title: Id
          type: string
        input:
          title: Input
          type: object
        name:
          title: Name
          type: string
        server_name:
          description: The name of the MCP server
          title: Server Name
          type: string
        type:
          const: mcp_tool_use
          enum:
            - mcp_tool_use
          title: Type
          type: string
      required:
        - id
        - input
        - name
        - server_name
        - type
      title: MCP tool use
      type: object
    RequestPageLocationCitation:
      additionalProperties: false
      properties:
        cited_text:
          title: Cited Text
          type: string
        document_index:
          minimum: 0
          title: Document Index
          type: integer
        document_title:
          anyOf:
            - maxLength: 255
              minLength: 1
              type: string
            - type: 'null'
          title: Document Title
        end_page_number:
          title: End Page Number
          type: integer
        start_page_number:
          minimum: 1
          title: Start Page Number
          type: integer
        type:
          const: page_location
          enum:
            - page_location
          title: Type
          type: string
      required:
        - cited_text
        - document_index
        - document_title
        - end_page_number
        - start_page_number
        - type
      title: Page location
      type: object
    RequestRedactedThinkingBlock:
      additionalProperties: false
      properties:
        data:
          title: Data
          type: string
        type:
          const: redacted_thinking
          enum:
            - redacted_thinking
          title: Type
          type: string
      required:
        - data
        - type
      title: Redacted thinking
      type: object
    RequestSearchResultBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        citations:
          $ref: '#/components/schemas/RequestCitationsConfig'
        content:
          items:
            $ref: '#/components/schemas/RequestTextBlock'
          title: Content
          type: array
        source:
          title: Source
          type: string
        title:
          title: Title
          type: string
        type:
          const: search_result
          enum:
            - search_result
          title: Type
          type: string
      required:
        - content
        - source
        - title
        - type
      title: Search result
      type: object
    RequestSearchResultLocationCitation:
      additionalProperties: false
      properties:
        cited_text:
          title: Cited Text
          type: string
        end_block_index:
          title: End Block Index
          type: integer
        search_result_index:
          minimum: 0
          title: Search Result Index
          type: integer
        source:
          title: Source
          type: string
        start_block_index:
          minimum: 0
          title: Start Block Index
          type: integer
        title:
          anyOf:
            - type: string
            - type: 'null'
          title: Title
        type:
          const: search_result_location
          enum:
            - search_result_location
          title: Type
          type: string
      required:
        - cited_text
        - end_block_index
        - search_result_index
        - source
        - start_block_index
        - title
        - type
      title: RequestSearchResultLocationCitation
      type: object
    RequestServerToolUseBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        id:
          pattern: ^srvtoolu_[a-zA-Z0-9_]+$
          title: Id
          type: string
        input:
          title: Input
          type: object
        name:
          enum:
            - web_search
            - web_fetch
            - code_execution
            - bash_code_execution
            - text_editor_code_execution
          title: Name
          type: string
        type:
          const: server_tool_use
          enum:
            - server_tool_use
          title: Type
          type: string
      required:
        - id
        - input
        - name
        - type
      title: Server tool use
      type: object
    RequestTextBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        citations:
          anyOf:
            - items:
                discriminator:
                  mapping:
                    char_location: '#/components/schemas/RequestCharLocationCitation'
                    content_block_location: '#/components/schemas/RequestContentBlockLocationCitation'
                    page_location: '#/components/schemas/RequestPageLocationCitation'
                    search_result_location: '#/components/schemas/RequestSearchResultLocationCitation'
                    web_search_result_location: >-
                      #/components/schemas/RequestWebSearchResultLocationCitation
                  propertyName: type
                oneOf:
                  - $ref: '#/components/schemas/RequestCharLocationCitation'
                  - $ref: '#/components/schemas/RequestPageLocationCitation'
                  - $ref: '#/components/schemas/RequestContentBlockLocationCitation'
                  - $ref: >-
                      #/components/schemas/RequestWebSearchResultLocationCitation
                  - $ref: '#/components/schemas/RequestSearchResultLocationCitation'
              type: array
            - type: 'null'
          title: Citations
        text:
          minLength: 1
          title: Text
          type: string
        type:
          const: text
          enum:
            - text
          title: Type
          type: string
      required:
        - text
        - type
      title: Text
      type: object
    RequestTextEditorCodeExecutionCreateResultBlock:
      additionalProperties: false
      properties:
        is_file_update:
          title: Is File Update
          type: boolean
        type:
          const: text_editor_code_execution_create_result
          enum:
            - text_editor_code_execution_create_result
          title: Type
          type: string
      required:
        - is_file_update
        - type
      title: RequestTextEditorCodeExecutionCreateResultBlock
      type: object
    RequestTextEditorCodeExecutionStrReplaceResultBlock:
      additionalProperties: false
      properties:
        lines:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Lines
        new_lines:
          anyOf:
            - type: integer
            - type: 'null'
          title: New Lines
        new_start:
          anyOf:
            - type: integer
            - type: 'null'
          title: New Start
        old_lines:
          anyOf:
            - type: integer
            - type: 'null'
          title: Old Lines
        old_start:
          anyOf:
            - type: integer
            - type: 'null'
          title: Old Start
        type:
          const: text_editor_code_execution_str_replace_result
          enum:
            - text_editor_code_execution_str_replace_result
          title: Type
          type: string
      required:
        - type
      title: RequestTextEditorCodeExecutionStrReplaceResultBlock
      type: object
    RequestTextEditorCodeExecutionToolResultBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        content:
          anyOf:
            - $ref: >-
                #/components/schemas/RequestTextEditorCodeExecutionToolResultError
            - $ref: >-
                #/components/schemas/RequestTextEditorCodeExecutionViewResultBlock
            - $ref: >-
                #/components/schemas/RequestTextEditorCodeExecutionCreateResultBlock
            - $ref: >-
                #/components/schemas/RequestTextEditorCodeExecutionStrReplaceResultBlock
          title: Content
        tool_use_id:
          pattern: ^srvtoolu_[a-zA-Z0-9_]+$
          title: Tool Use Id
          type: string
        type:
          const: text_editor_code_execution_tool_result
          enum:
            - text_editor_code_execution_tool_result
          title: Type
          type: string
      required:
        - content
        - tool_use_id
        - type
      title: RequestTextEditorCodeExecutionToolResultBlock
      type: object
    RequestTextEditorCodeExecutionToolResultError:
      additionalProperties: false
      properties:
        error_code:
          $ref: '#/components/schemas/TextEditorCodeExecutionToolResultErrorCode'
        error_message:
          anyOf:
            - type: string
            - type: 'null'
          title: Error Message
        type:
          const: text_editor_code_execution_tool_result_error
          enum:
            - text_editor_code_execution_tool_result_error
          title: Type
          type: string
      required:
        - error_code
        - type
      title: RequestTextEditorCodeExecutionToolResultError
      type: object
    RequestTextEditorCodeExecutionViewResultBlock:
      additionalProperties: false
      properties:
        content:
          title: Content
          type: string
        file_type:
          enum:
            - text
            - image
            - pdf
          title: File Type
          type: string
        num_lines:
          anyOf:
            - type: integer
            - type: 'null'
          title: Num Lines
        start_line:
          anyOf:
            - type: integer
            - type: 'null'
          title: Start Line
        total_lines:
          anyOf:
            - type: integer
            - type: 'null'
          title: Total Lines
        type:
          const: text_editor_code_execution_view_result
          enum:
            - text_editor_code_execution_view_result
          title: Type
          type: string
      required:
        - content
        - file_type
        - type
      title: RequestTextEditorCodeExecutionViewResultBlock
      type: object
    RequestThinkingBlock:
      additionalProperties: false
      properties:
        signature:
          title: Signature
          type: string
        thinking:
          title: Thinking
          type: string
        type:
          const: thinking
          enum:
            - thinking
          title: Type
          type: string
      required:
        - signature
        - thinking
        - type
      title: Thinking
      type: object
    RequestToolResultBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        content:
          anyOf:
            - type: string
            - items:
                discriminator:
                  mapping:
                    document: '#/components/schemas/RequestDocumentBlock'
                    image: '#/components/schemas/RequestImageBlock'
                    search_result: '#/components/schemas/RequestSearchResultBlock'
                    text: '#/components/schemas/RequestTextBlock'
                  propertyName: type
                oneOf:
                  - $ref: '#/components/schemas/RequestTextBlock'
                  - $ref: '#/components/schemas/RequestImageBlock'
                  - $ref: '#/components/schemas/RequestSearchResultBlock'
                  - $ref: '#/components/schemas/RequestDocumentBlock'
              type: array
          title: Content
        is_error:
          title: Is Error
          type: boolean
        tool_use_id:
          pattern: ^[a-zA-Z0-9_-]+$
          title: Tool Use Id
          type: string
        type:
          const: tool_result
          enum:
            - tool_result
          title: Type
          type: string
      required:
        - tool_use_id
        - type
      title: Tool result
      type: object
    RequestToolUseBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        id:
          pattern: ^[a-zA-Z0-9_-]+$
          title: Id
          type: string
        input:
          title: Input
          type: object
        name:
          maxLength: 200
          minLength: 1
          title: Name
          type: string
        type:
          const: tool_use
          enum:
            - tool_use
          title: Type
          type: string
      required:
        - id
        - input
        - name
        - type
      title: Tool use
      type: object
    RequestWebFetchResultBlock:
      additionalProperties: false
      properties:
        content:
          $ref: '#/components/schemas/RequestDocumentBlock'
        retrieved_at:
          anyOf:
            - type: string
            - type: 'null'
          description: ISO 8601 timestamp when the content was retrieved
          title: Retrieved At
        type:
          const: web_fetch_result
          enum:
            - web_fetch_result
          title: Type
          type: string
        url:
          description: Fetched content URL
          title: Url
          type: string
      required:
        - content
        - type
        - url
      title: RequestWebFetchResultBlock
      type: object
    RequestWebFetchToolResultBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        content:
          anyOf:
            - $ref: '#/components/schemas/RequestWebFetchToolResultError'
            - $ref: '#/components/schemas/RequestWebFetchResultBlock'
          title: Content
        tool_use_id:
          pattern: ^srvtoolu_[a-zA-Z0-9_]+$
          title: Tool Use Id
          type: string
        type:
          const: web_fetch_tool_result
          enum:
            - web_fetch_tool_result
          title: Type
          type: string
      required:
        - content
        - tool_use_id
        - type
      title: RequestWebFetchToolResultBlock
      type: object
    RequestWebFetchToolResultError:
      additionalProperties: false
      properties:
        error_code:
          $ref: '#/components/schemas/WebFetchToolResultErrorCode'
        type:
          const: web_fetch_tool_result_error
          enum:
            - web_fetch_tool_result_error
          title: Type
          type: string
      required:
        - error_code
        - type
      title: RequestWebFetchToolResultError
      type: object
    RequestWebSearchResultBlock:
      additionalProperties: false
      properties:
        encrypted_content:
          title: Encrypted Content
          type: string
        page_age:
          anyOf:
            - type: string
            - type: 'null'
          title: Page Age
        title:
          title: Title
          type: string
        type:
          const: web_search_result
          enum:
            - web_search_result
          title: Type
          type: string
        url:
          title: Url
          type: string
      required:
        - encrypted_content
        - title
        - type
        - url
      title: RequestWebSearchResultBlock
      type: object
    RequestWebSearchResultLocationCitation:
      additionalProperties: false
      properties:
        cited_text:
          title: Cited Text
          type: string
        encrypted_index:
          title: Encrypted Index
          type: string
        title:
          anyOf:
            - maxLength: 512
              minLength: 1
              type: string
            - type: 'null'
          title: Title
        type:
          const: web_search_result_location
          enum:
            - web_search_result_location
          title: Type
          type: string
        url:
          maxLength: 2048
          minLength: 1
          title: Url
          type: string
      required:
        - cited_text
        - encrypted_index
        - title
        - type
        - url
      title: RequestWebSearchResultLocationCitation
      type: object
    RequestWebSearchToolResultBlock:
      additionalProperties: false
      properties:
        cache_control:
          anyOf:
            - discriminator:
                mapping:
                  ephemeral: '#/components/schemas/CacheControlEphemeral'
                propertyName: type
              oneOf:
                - $ref: '#/components/schemas/CacheControlEphemeral'
            - type: 'null'
          description: Create a cache control breakpoint at this content block.
          title: Cache Control
        content:
          anyOf:
            - items:
                $ref: '#/components/schemas/RequestWebSearchResultBlock'
              type: array
            - $ref: '#/components/schemas/RequestWebSearchToolResultError'
          title: Content
        tool_use_id:
          pattern: ^srvtoolu_[a-zA-Z0-9_]+$
          title: Tool Use Id
          type: string
        type:
          const: web_search_tool_result
          enum:
            - web_search_tool_result
          title: Type
          type: string
      required:
        - content
        - tool_use_id
        - type
      title: Web search tool result
      type: object
    RequestWebSearchToolResultError:
      additionalProperties: false
      properties:
        error_code:
          $ref: '#/components/schemas/WebSearchToolResultErrorCode'
        type:
          const: web_search_tool_result_error
          enum:
            - web_search_tool_result_error
          title: Type
          type: string
      required:
        - error_code
        - type
      title: RequestWebSearchToolResultError
      type: object
    ServerToolUsage:
      properties:
        web_fetch_requests:
          default: 0
          description: The number of web fetch tool requests.
          examples:
            - 2
          minimum: 0
          title: Web Fetch Requests
          type: integer
        web_search_requests:
          default: 0
          description: The number of web search tool requests.
          examples:
            - 0
          minimum: 0
          title: Web Search Requests
          type: integer
      required:
        - web_fetch_requests
        - web_search_requests
      title: ServerToolUsage
      type: object
    TextEditorCodeExecutionToolResultErrorCode:
      enum:
        - invalid_tool_input
        - unavailable
        - too_many_requests
        - execution_time_exceeded
        - file_not_found
      title: TextEditorCodeExecutionToolResultErrorCode
      type: string
    URLImageSource:
      additionalProperties: false
      properties:
        type:
          const: url
          enum:
            - url
          title: Type
          type: string
        url:
          title: Url
          type: string
      required:
        - type
        - url
      title: URLImageSource
      type: object
    URLPDFSource:
      additionalProperties: false
      properties:
        type:
          const: url
          enum:
            - url
          title: Type
          type: string
        url:
          title: Url
          type: string
      required:
        - type
        - url
      title: PDF (URL)
      type: object
    Usage:
      properties:
        cache_creation:
          anyOf:
            - $ref: '#/components/schemas/CacheCreation'
            - type: 'null'
          default: null
          description: Breakdown of cached tokens by TTL
        cache_creation_input_tokens:
          anyOf:
            - minimum: 0
              type: integer
            - type: 'null'
          default: null
          description: The number of input tokens used to create the cache entry.
          examples:
            - 2051
          title: Cache Creation Input Tokens
        cache_read_input_tokens:
          anyOf:
            - minimum: 0
              type: integer
            - type: 'null'
          default: null
          description: The number of input tokens read from the cache.
          examples:
            - 2051
          title: Cache Read Input Tokens
        input_tokens:
          description: The number of input tokens which were used.
          examples:
            - 2095
          minimum: 0
          title: Input Tokens
          type: integer
        output_tokens:
          description: The number of output tokens which were used.
          examples:
            - 503
          minimum: 0
          title: Output Tokens
          type: integer
        server_tool_use:
          anyOf:
            - $ref: '#/components/schemas/ServerToolUsage'
            - type: 'null'
          default: null
          description: The number of server tool requests.
        service_tier:
          anyOf:
            - enum:
                - standard
                - priority
                - batch
              type: string
            - type: 'null'
          default: null
          description: If the request used the priority, standard, or batch tier.
          title: Service Tier
      required:
        - cache_creation
        - cache_creation_input_tokens
        - cache_read_input_tokens
        - input_tokens
        - output_tokens
        - server_tool_use
        - service_tier
      title: Usage
      type: object
    WebFetchToolResultErrorCode:
      enum:
        - invalid_tool_input
        - url_too_long
        - url_not_allowed
        - url_not_accessible
        - unsupported_content_type
        - too_many_requests
        - max_uses_exceeded
        - unavailable
      title: WebFetchToolResultErrorCode
      type: string
    WebSearchToolResultErrorCode:
      enum:
        - invalid_tool_input
        - unavailable
        - max_uses_exceeded
        - too_many_requests
        - query_too_long
      title: WebSearchToolResultErrorCode
      type: string

````