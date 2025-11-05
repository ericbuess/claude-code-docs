# Get Cost Report

## OpenAPI

````yaml get /v1/organizations/cost_report
paths:
  path: /v1/organizations/cost_report
  method: get
  servers:
    - url: https://api.anthropic.com
  request:
    security: []
    parameters:
      path: {}
      query:
        limit:
          schema:
            - type: integer
              required: false
              title: Limit
              description: Maximum number of time buckets to return in the response.
              examples:
                - 7
              maximum: 31
              minimum: 1
              default: 7
              example: 7
        page:
          schema:
            - type: string
              required: false
              title: Page
              description: >-
                Optionally set to the `next_page` token from the previous
                response.
              examples: &ref_0
                - page_MjAyNS0wNS0xNFQwMDowMDowMFo=
                - null
              format: date-time
              example: page_MjAyNS0wNS0xNFQwMDowMDowMFo=
            - type: 'null'
              required: false
              title: Page
              description: >-
                Optionally set to the `next_page` token from the previous
                response.
              examples: *ref_0
              example: page_MjAyNS0wNS0xNFQwMDowMDowMFo=
        starting_at:
          schema:
            - type: string
              required: true
              title: Starting At
              description: >-
                Time buckets that start on or after this RFC 3339 timestamp will
                be returned.

                Each time bucket will be snapped to the start of the
                minute/hour/day in UTC.
              examples:
                - '2024-10-30T23:58:27.427722Z'
              format: date-time
              example: '2024-10-30T23:58:27.427722Z'
        ending_at:
          schema:
            - type: string
              required: false
              title: Ending At
              description: >-
                Time buckets that end before this RFC 3339 timestamp will be
                returned.
              examples: &ref_1
                - '2024-10-30T23:58:27.427722Z'
              format: date-time
              example: '2024-10-30T23:58:27.427722Z'
            - type: 'null'
              required: false
              title: Ending At
              description: >-
                Time buckets that end before this RFC 3339 timestamp will be
                returned.
              examples: *ref_1
              example: '2024-10-30T23:58:27.427722Z'
        group_by[]:
          schema:
            - type: array
              items:
                allOf:
                  - $ref: '#/components/schemas/CostReportGroupBy'
              required: false
              title: Group By[]
              description: Group by any subset of the available options.
              examples: &ref_2
                - workspace_id
                - description
              example: workspace_id
            - type: 'null'
              required: false
              title: Group By[]
              description: Group by any subset of the available options.
              examples: *ref_2
              example: workspace_id
        bucket_width:
          schema:
            - type: enum<string>
              enum:
                - 1d
              required: false
              title: CostReportTimeBucketWidth
              description: Time granularity of the response data.
              const: 1d
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
        source: |-
          curl "https://api.anthropic.com/v1/organizations/cost_report\
          ?starting_at=2025-08-01T00:00:00Z\
          &group_by[]=workspace_id\
          &group_by[]=description\
          &limit=1" \
            --header "anthropic-version: 2023-06-01" \
            --header "content-type: application/json" \
            --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              data:
                allOf:
                  - items:
                      $ref: '#/components/schemas/CostReportTimeBucket'
                    type: array
                    title: Data
              has_more:
                allOf:
                  - type: boolean
                    title: Has More
                    description: Indicates if there are more results.
              next_page:
                allOf:
                  - anyOf:
                      - type: string
                        format: date-time
                      - type: 'null'
                    title: Next Page
                    description: >-
                      Token to provide in as `page` in the subsequent request to
                      retrieve the next page of data.
                    examples:
                      - page_MjAyNS0wNS0xNFQwMDowMDowMFo=
                      - null
            title: GetCostReportResponse
            refIdentifier: '#/components/schemas/GetCostReportResponse'
            requiredProperties:
              - data
              - has_more
              - next_page
        examples:
          example:
            value:
              data:
                - starting_at: '2025-08-01T00:00:00Z'
                  ending_at: '2025-08-02T00:00:00Z'
                  results:
                    - currency: USD
                      amount: '123.78912'
                      workspace_id: wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
                      description: Claude Sonnet 4 Usage - Input Tokens
                      cost_type: tokens
                      context_window: 0-200k
                      model: claude-sonnet-4-20250514
                      service_tier: standard
                      token_type: uncached_input_tokens
              has_more: true
              next_page: page_MjAyNS0wNS0xNFQwMDowMDowMFo=
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
    CostReportGroupBy:
      type: string
      enum:
        - workspace_id
        - description
      title: CostReportGroupBy
    CostReportItem:
      properties:
        currency:
          type: string
          title: Currency
          description: Currency code for the cost amount. Currently always `"USD"`.
          examples:
            - USD
        amount:
          type: string
          title: Amount
          description: >-
            Cost amount in lowest currency units (e.g. cents) as a decimal
            string. For example, `"123.45"` in `"USD"` represents `$1.23`.
          examples:
            - '123.78912'
            - '0.1'
            - '1500'
        workspace_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Workspace Id
          description: >-
            ID of the Workspace this cost is associated with. Null if not
            grouping by workspace or for the default workspace.
          examples:
            - wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
          description: Description of the cost item. Null if not grouping by description.
          examples:
            - Claude Sonnet 4 Usage - Input Tokens
        cost_type:
          anyOf:
            - $ref: '#/components/schemas/CostType'
            - type: 'null'
          description: Type of cost. Null if not grouping by description.
          examples:
            - tokens
            - web_search
            - code_execution
        context_window:
          anyOf:
            - $ref: '#/components/schemas/MessagesUsageReportContextWindow'
            - type: 'null'
          description: >-
            Input context window used. Null if not grouping by description or
            for non-token costs.
          examples:
            - 0-200k
            - 200k-1M
        model:
          anyOf:
            - type: string
            - type: 'null'
          title: Model
          description: >-
            Model name used. Null if not grouping by description or for
            non-token costs.
          examples:
            - claude-sonnet-4-20250514
            - claude-3-5-haiku-20241022
        service_tier:
          anyOf:
            - $ref: '#/components/schemas/CostReportServiceTier'
            - type: 'null'
          description: >-
            Service tier used. Null if not grouping by description or for
            non-token costs.
          examples:
            - standard
            - batch
        token_type:
          anyOf:
            - $ref: '#/components/schemas/CostReportTokenType'
            - type: 'null'
          description: >-
            Type of token. Null if not grouping by description or for non-token
            costs.
          examples:
            - uncached_input_tokens
            - output_tokens
            - cache_read_input_tokens
            - cache_creation.ephemeral_1h_input_tokens
            - cache_creation.ephemeral_5m_input_tokens
      type: object
      required:
        - currency
        - amount
        - workspace_id
        - description
        - cost_type
        - context_window
        - model
        - service_tier
        - token_type
      title: CostReportItem
    CostReportServiceTier:
      type: string
      enum:
        - standard
        - batch
      title: CostReportServiceTier
    CostReportTimeBucket:
      properties:
        starting_at:
          type: string
          title: Starting At
          description: Start of the time bucket (inclusive) in RFC 3339 format.
          examples:
            - '2025-08-01T00:00:00Z'
        ending_at:
          type: string
          title: Ending At
          description: End of the time bucket (exclusive) in RFC 3339 format.
          examples:
            - '2025-08-02T00:00:00Z'
        results:
          items:
            $ref: '#/components/schemas/CostReportItem'
          type: array
          title: Results
          description: >-
            List of cost items for this time bucket. There may be multiple items
            if one or more `group_by[]` parameters are specified.
      type: object
      required:
        - starting_at
        - ending_at
        - results
      title: CostReportTimeBucket
    CostReportTokenType:
      type: string
      enum:
        - uncached_input_tokens
        - output_tokens
        - cache_read_input_tokens
        - cache_creation.ephemeral_1h_input_tokens
        - cache_creation.ephemeral_5m_input_tokens
      title: CostReportTokenType
    CostType:
      type: string
      enum:
        - tokens
        - web_search
        - code_execution
      title: CostType
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
    MessagesUsageReportContextWindow:
      type: string
      enum:
        - 0-200k
        - 200k-1M
      title: MessagesUsageReportContextWindow
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