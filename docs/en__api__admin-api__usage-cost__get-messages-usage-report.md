# Get Usage Report for the Messages API

## OpenAPI

````yaml get /v1/organizations/usage_report/messages
paths:
  path: /v1/organizations/usage_report/messages
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
              description: |-
                Maximum number of time buckets to return in the response.

                The default and max limits depend on `bucket_width`:
                • `"1d"`: Default of 7 days, maximum of 31 days
                • `"1h"`: Default of 24 hours, maximum of 168 hours
                • `"1m"`: Default of 60 minutes, maximum of 1440 minutes
              examples:
                - 7
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
        api_key_ids[]:
          schema:
            - type: array
              items:
                allOf:
                  - type: string
              required: false
              title: Api Key Ids[]
              description: Restrict usage returned to the specified API key ID(s).
              examples: &ref_2
                - apikey_01Rj2N8SVvo6BePZj99NhmiT
              example: apikey_01Rj2N8SVvo6BePZj99NhmiT
            - type: 'null'
              required: false
              title: Api Key Ids[]
              description: Restrict usage returned to the specified API key ID(s).
              examples: *ref_2
              example: apikey_01Rj2N8SVvo6BePZj99NhmiT
        workspace_ids[]:
          schema:
            - type: array
              items:
                allOf:
                  - type: string
              required: false
              title: Workspace Ids[]
              description: Restrict usage returned to the specified workspace ID(s).
              examples: &ref_3
                - wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
              example: wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
            - type: 'null'
              required: false
              title: Workspace Ids[]
              description: Restrict usage returned to the specified workspace ID(s).
              examples: *ref_3
              example: wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
        models[]:
          schema:
            - type: array
              items:
                allOf:
                  - type: string
              required: false
              title: Models[]
              description: Restrict usage returned to the specified model(s).
              examples: &ref_4
                - claude-sonnet-4-20250514
                - claude-3-5-haiku-20241022
              example: claude-sonnet-4-20250514
            - type: 'null'
              required: false
              title: Models[]
              description: Restrict usage returned to the specified model(s).
              examples: *ref_4
              example: claude-sonnet-4-20250514
        service_tiers[]:
          schema:
            - type: array
              items:
                allOf:
                  - $ref: '#/components/schemas/UsageReportServiceTier'
              required: false
              title: Service Tiers[]
              description: Restrict usage returned to the specified service tier(s).
              examples: &ref_5
                - standard
                - batch
                - priority
              example: standard
            - type: 'null'
              required: false
              title: Service Tiers[]
              description: Restrict usage returned to the specified service tier(s).
              examples: *ref_5
              example: standard
        context_window[]:
          schema:
            - type: array
              items:
                allOf:
                  - $ref: '#/components/schemas/MessagesUsageReportContextWindow'
              required: false
              title: Context Window[]
              description: Restrict usage returned to the specified context window(s).
              examples: &ref_6
                - 0-200k
                - 200k-1M
              example: 0-200k
            - type: 'null'
              required: false
              title: Context Window[]
              description: Restrict usage returned to the specified context window(s).
              examples: *ref_6
              example: 0-200k
        group_by[]:
          schema:
            - type: array
              items:
                allOf:
                  - $ref: '#/components/schemas/MessagesUsageReportGroupBy'
              required: false
              title: Group By[]
              description: Group by any subset of the available options.
              examples: &ref_7
                - api_key_id
                - workspace_id
                - model
                - service_tier
                - context_window
              example: api_key_id
            - type: 'null'
              required: false
              title: Group By[]
              description: Group by any subset of the available options.
              examples: *ref_7
              example: api_key_id
        bucket_width:
          schema:
            - type: enum<string>
              enum:
                - 1d
                - 1m
                - 1h
              required: false
              title: MessagesUsageReportTimeBucketWidth
              description: Time granularity of the response data.
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
          "https://api.anthropic.com/v1/organizations/usage_report/messages\

          ?starting_at=2025-08-01T00:00:00Z\

          &group_by[]=api_key_id\

          &group_by[]=workspace_id\

          &group_by[]=model\

          &group_by[]=service_tier\

          &group_by[]=context_window\

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
                      $ref: '#/components/schemas/MessagesUsageReportTimeBucket'
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
            title: GetMessagesUsageReportResponse
            refIdentifier: '#/components/schemas/GetMessagesUsageReportResponse'
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
                    - uncached_input_tokens: 1500
                      cache_creation:
                        ephemeral_1h_input_tokens: 1000
                        ephemeral_5m_input_tokens: 500
                      cache_read_input_tokens: 200
                      output_tokens: 500
                      server_tool_use:
                        web_search_requests: 10
                      api_key_id: apikey_01Rj2N8SVvo6BePZj99NhmiT
                      workspace_id: wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
                      model: claude-sonnet-4-20250514
                      service_tier: standard
                      context_window: 0-200k
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
    CacheCreation:
      properties:
        ephemeral_1h_input_tokens:
          type: integer
          title: Ephemeral 1H Input Tokens
          description: The number of input tokens used to create the 1 hour cache entry.
          examples:
            - 1000
        ephemeral_5m_input_tokens:
          type: integer
          title: Ephemeral 5M Input Tokens
          description: The number of input tokens used to create the 5 minute cache entry.
          examples:
            - 500
      type: object
      required:
        - ephemeral_1h_input_tokens
        - ephemeral_5m_input_tokens
      title: CacheCreation
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
    MessagesUsageReportGroupBy:
      type: string
      enum:
        - api_key_id
        - workspace_id
        - model
        - service_tier
        - context_window
      title: MessagesUsageReportGroupBy
    MessagesUsageReportItem:
      properties:
        uncached_input_tokens:
          type: integer
          title: Uncached Input Tokens
          description: The number of uncached input tokens processed.
          examples:
            - 1500
        cache_creation:
          $ref: '#/components/schemas/CacheCreation'
          description: The number of input tokens for cache creation.
        cache_read_input_tokens:
          type: integer
          title: Cache Read Input Tokens
          description: The number of input tokens read from the cache.
          examples:
            - 200
        output_tokens:
          type: integer
          title: Output Tokens
          description: The number of output tokens generated.
          examples:
            - 500
        server_tool_use:
          $ref: '#/components/schemas/ServerToolUse'
          description: Server-side tool usage metrics.
        api_key_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Api Key Id
          description: >-
            ID of the API key used. Null if not grouping by API key or for usage
            in the Anthropic Console.
          examples:
            - apikey_01Rj2N8SVvo6BePZj99NhmiT
        workspace_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Workspace Id
          description: >-
            ID of the Workspace used. Null if not grouping by workspace or for
            the default workspace.
          examples:
            - wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
        model:
          anyOf:
            - type: string
            - type: 'null'
          title: Model
          description: Model used. Null if not grouping by model.
          examples:
            - claude-sonnet-4-20250514
            - claude-3-5-haiku-20241022
        service_tier:
          anyOf:
            - $ref: '#/components/schemas/UsageReportServiceTier'
            - type: 'null'
          description: Service tier used. Null if not grouping by service tier.
          examples:
            - standard
            - batch
            - priority
        context_window:
          anyOf:
            - $ref: '#/components/schemas/MessagesUsageReportContextWindow'
            - type: 'null'
          description: Context window used. Null if not grouping by context window.
          examples:
            - 0-200k
            - 200k-1M
      type: object
      required:
        - uncached_input_tokens
        - cache_creation
        - cache_read_input_tokens
        - output_tokens
        - server_tool_use
        - api_key_id
        - workspace_id
        - model
        - service_tier
        - context_window
      title: MessagesUsageReportItem
    MessagesUsageReportTimeBucket:
      properties:
        starting_at:
          type: string
          format: date-time
          title: Starting At
          description: Start of the time bucket (inclusive) in RFC 3339 format.
          examples:
            - '2025-08-01T00:00:00Z'
        ending_at:
          type: string
          format: date-time
          title: Ending At
          description: End of the time bucket (exclusive) in RFC 3339 format.
          examples:
            - '2025-08-02T00:00:00Z'
        results:
          items:
            $ref: '#/components/schemas/MessagesUsageReportItem'
          type: array
          title: Results
          description: >-
            List of usage items for this time bucket.  There may be multiple
            items if one or more `group_by[]` parameters are specified.
      type: object
      required:
        - starting_at
        - ending_at
        - results
      title: MessagesUsageReportTimeBucket
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
    ServerToolUse:
      properties:
        web_search_requests:
          type: integer
          title: Web Search Requests
          description: The number of web search requests made.
          examples:
            - 10
      type: object
      required:
        - web_search_requests
      title: ServerToolUse
    UsageReportServiceTier:
      type: string
      enum:
        - standard
        - batch
        - priority
      title: UsageReportServiceTier

````