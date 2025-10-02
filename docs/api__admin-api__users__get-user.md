# Get User

## OpenAPI

````yaml get /v1/organizations/users/{user_id}
paths:
  path: /v1/organizations/users/{user_id}
  method: get
  servers:
    - url: https://api.anthropic.com
  request:
    security: []
    parameters:
      path:
        user_id:
          schema:
            - type: string
              required: true
              title: User Id
              description: ID of the User.
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
    body: {}
    codeSamples:
      - lang: bash
        source: >-
          curl
          "https://api.anthropic.com/v1/organizations/users/user_01WCz1FkmYMm4gnmykNKUu3Q"
          \
            --header "anthropic-version: 2023-06-01" \
            --header "content-type: application/json" \
            --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              added_at:
                allOf:
                  - type: string
                    format: date-time
                    title: Added At
                    description: >-
                      RFC 3339 datetime string indicating when the User joined
                      the Organization.
                    examples:
                      - '2024-10-30T23:58:27.427722Z'
              email:
                allOf:
                  - type: string
                    title: Email
                    description: Email of the User.
                    examples:
                      - user@emaildomain.com
              id:
                allOf:
                  - type: string
                    title: Id
                    description: ID of the User.
                    examples:
                      - user_01WCz1FkmYMm4gnmykNKUu3Q
              name:
                allOf:
                  - type: string
                    title: Name
                    description: Name of the User.
                    examples:
                      - Jane Doe
              role:
                allOf:
                  - $ref: '#/components/schemas/RoleSchema'
                    description: Organization role of the User.
                    examples:
                      - user
                      - developer
                      - billing
                      - admin
                      - claude_code_user
              type:
                allOf:
                  - type: string
                    enum:
                      - user
                    const: user
                    title: Type
                    description: |-
                      Object type.

                      For Users, this is always `"user"`.
                    default: user
            title: User
            refIdentifier: '#/components/schemas/User'
            requiredProperties:
              - added_at
              - email
              - id
              - name
              - role
              - type
        examples:
          example:
            value:
              added_at: '2024-10-30T23:58:27.427722Z'
              email: user@emaildomain.com
              id: user_01WCz1FkmYMm4gnmykNKUu3Q
              name: Jane Doe
              role: user
              type: user
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
    RoleSchema:
      type: string
      enum:
        - user
        - developer
        - billing
        - admin
        - claude_code_user
      title: RoleSchema

````