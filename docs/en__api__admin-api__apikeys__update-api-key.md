# Update API Keys

## OpenAPI

````yaml post /v1/organizations/api_keys/{api_key_id}
paths:
  path: /v1/organizations/api_keys/{api_key_id}
  method: post
  servers:
    - url: https://api.anthropic.com
  request:
    security: []
    parameters:
      path:
        api_key_id:
          schema:
            - type: string
              required: true
              title: Api Key Id
              description: ID of the API key.
      query: {}
      header:
        x-api-key:
          schema:
            - type: string
              required: true
              title: X-Api-Key
              description: >-
                Your unique Admin API key for authentication. 


                This key is required in the header of all Admin API requests, to
                authenticate your account and access Anthropic's services. Get
                your Admin API key through the
                [Console](https://console.anthropic.com/settings/admin-keys).
        anthropic-version:
          schema:
            - type: string
              required: true
              title: Anthropic-Version
              description: >-
                The version of the Claude API you want to use.


                Read more about versioning and our version history
                [here](https://docs.claude.com/en/api/versioning).
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              name:
                allOf:
                  - description: Name of the API key.
                    maxLength: 500
                    minLength: 1
                    title: Name
                    type: string
              status:
                allOf:
                  - anyOf:
                      - enum:
                          - active
                          - inactive
                          - archived
                        type: string
                      - type: 'null'
                    description: Status of the API key.
                    title: Status
            required: true
            title: ApiKeyUpdateParams
            refIdentifier: '#/components/schemas/ApiKeyUpdateParams'
            additionalProperties: false
        examples:
          example:
            value:
              name: <string>
              status: active
    codeSamples:
      - lang: bash
        source: >-
          curl
          "https://api.anthropic.com/v1/organizations/api_keys/apikey_01Rj2N8SVvo6BePZj99NhmiT"
          \
            --header "anthropic-version: 2023-06-01" \
            --header "content-type: application/json" \
            --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
            --data '{
              "status": "active",
              "name": "Developer Key"
            }'
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              created_at:
                allOf:
                  - type: string
                    format: date-time
                    title: Created At
                    description: >-
                      RFC 3339 datetime string indicating when the API Key was
                      created.
                    examples:
                      - '2024-10-30T23:58:27.427722Z'
              created_by:
                allOf:
                  - $ref: '#/components/schemas/CreatedBy'
                    title: Created By
                    description: The ID and type of the actor that created the API key.
                    examples:
                      - id: user_01WCz1FkmYMm4gnmykNKUu3Q
                        type: user
              id:
                allOf:
                  - type: string
                    title: Id
                    description: ID of the API key.
                    examples:
                      - apikey_01Rj2N8SVvo6BePZj99NhmiT
              name:
                allOf:
                  - type: string
                    title: Name
                    description: Name of the API key.
                    examples:
                      - Developer Key
              partial_key_hint:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Partial Key Hint
                    description: Partially redacted hint for the API key.
                    examples:
                      - sk-ant-api03-R2D...igAA
              status:
                allOf:
                  - type: string
                    enum:
                      - active
                      - inactive
                      - archived
                    title: Status
                    description: Status of the API key.
                    examples:
                      - active
              type:
                allOf:
                  - type: string
                    enum:
                      - api_key
                    const: api_key
                    title: Type
                    description: |-
                      Object type.

                      For API Keys, this is always `"api_key"`.
                    default: api_key
              workspace_id:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Workspace Id
                    description: >-
                      ID of the Workspace associated with the API key, or null
                      if the API key belongs to the default Workspace.
                    examples:
                      - wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
            title: ApiKey
            refIdentifier: '#/components/schemas/ApiKey'
            requiredProperties:
              - created_at
              - created_by
              - id
              - name
              - partial_key_hint
              - status
              - type
              - workspace_id
        examples:
          example:
            value:
              created_at: '2024-10-30T23:58:27.427722Z'
              created_by:
                id: user_01WCz1FkmYMm4gnmykNKUu3Q
                type: user
              id: apikey_01Rj2N8SVvo6BePZj99NhmiT
              name: Developer Key
              partial_key_hint: sk-ant-api03-R2D...igAA
              status: active
              type: api_key
              workspace_id: wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
        description: Successful Response
    4XX:
      application/json:
        schemaArray:
          - type: object
            properties:
              error:
                allOf:
                  - oneOf:
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
                    discriminator:
                      propertyName: type
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
              request_id:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Request Id
              type:
                allOf:
                  - type: string
                    enum:
                      - error
                    const: error
                    title: Type
                    default: error
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
          type: string
          title: Message
          default: Internal server error
        type:
          type: string
          enum:
            - api_error
          const: api_error
          title: Type
          default: api_error
      type: object
      required:
        - message
        - type
      title: APIError
    AuthenticationError:
      properties:
        message:
          type: string
          title: Message
          default: Authentication error
        type:
          type: string
          enum:
            - authentication_error
          const: authentication_error
          title: Type
          default: authentication_error
      type: object
      required:
        - message
        - type
      title: AuthenticationError
    BillingError:
      properties:
        message:
          type: string
          title: Message
          default: Billing error
        type:
          type: string
          enum:
            - billing_error
          const: billing_error
          title: Type
          default: billing_error
      type: object
      required:
        - message
        - type
      title: BillingError
    CreatedBy:
      properties:
        id:
          type: string
          title: Id
          description: ID of the actor that created the object.
          examples:
            - user_01WCz1FkmYMm4gnmykNKUu3Q
        type:
          type: string
          title: Type
          description: Type of the actor that created the object.
          examples:
            - user
      type: object
      required:
        - id
        - type
      title: CreatedBy
    GatewayTimeoutError:
      properties:
        message:
          type: string
          title: Message
          default: Request timeout
        type:
          type: string
          enum:
            - timeout_error
          const: timeout_error
          title: Type
          default: timeout_error
      type: object
      required:
        - message
        - type
      title: GatewayTimeoutError
    InvalidRequestError:
      properties:
        message:
          type: string
          title: Message
          default: Invalid request
        type:
          type: string
          enum:
            - invalid_request_error
          const: invalid_request_error
          title: Type
          default: invalid_request_error
      type: object
      required:
        - message
        - type
      title: InvalidRequestError
    NotFoundError:
      properties:
        message:
          type: string
          title: Message
          default: Not found
        type:
          type: string
          enum:
            - not_found_error
          const: not_found_error
          title: Type
          default: not_found_error
      type: object
      required:
        - message
        - type
      title: NotFoundError
    OverloadedError:
      properties:
        message:
          type: string
          title: Message
          default: Overloaded
        type:
          type: string
          enum:
            - overloaded_error
          const: overloaded_error
          title: Type
          default: overloaded_error
      type: object
      required:
        - message
        - type
      title: OverloadedError
    PermissionError:
      properties:
        message:
          type: string
          title: Message
          default: Permission denied
        type:
          type: string
          enum:
            - permission_error
          const: permission_error
          title: Type
          default: permission_error
      type: object
      required:
        - message
        - type
      title: PermissionError
    RateLimitError:
      properties:
        message:
          type: string
          title: Message
          default: Rate limited
        type:
          type: string
          enum:
            - rate_limit_error
          const: rate_limit_error
          title: Type
          default: rate_limit_error
      type: object
      required:
        - message
        - type
      title: RateLimitError

````