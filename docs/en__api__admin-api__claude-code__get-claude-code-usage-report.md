# Get Claude Code Usage Report

> Retrieve daily aggregated usage metrics for Claude Code users.
Enables organizations to analyze developer productivity and build custom dashboards.

## OpenAPI

````yaml get /v1/organizations/usage_report/claude_code
paths:
  path: /v1/organizations/usage_report/claude_code
  method: get
  servers:
    - url: https://api.anthropic.com
  request:
    security: []
    parameters:
      path: {}
      query:
        starting_at:
          schema:
            - type: string
              required: true
              title: Starting At
              description: >-
                UTC date in YYYY-MM-DD format. Returns metrics for this single
                day only.
        limit:
          schema:
            - type: integer
              required: false
              title: Limit
              description: 'Number of records per page (default: 20, max: 1000).'
              maximum: 1000
              minimum: 1
              default: 20
        page:
          schema:
            - type: string
              required: false
              title: Page
              description: Opaque cursor token from previous response's `next_page` field.
            - type: 'null'
              required: false
              title: Page
              description: Opaque cursor token from previous response's `next_page` field.
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
          "https://api.anthropic.com/v1/organizations/usage_report/claude_code\

          ?starting_at=2025-08-08\

          &limit=20" \
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
                      $ref: '#/components/schemas/ClaudeCodeUsageReportItem'
                    type: array
                    title: Data
                    description: List of Claude Code usage records for the requested date.
              has_more:
                allOf:
                  - type: boolean
                    title: Has More
                    description: >-
                      True if there are more records available beyond the
                      current page.
              next_page:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Next Page
                    description: >-
                      Opaque cursor token for fetching the next page of results,
                      or null if no more pages are available.
                    examples:
                      - page_MjAyNS0wNS0xNFQwMDowMDowMFo=
                      - null
            title: GetClaudeCodeUsageReportResponse
            refIdentifier: '#/components/schemas/GetClaudeCodeUsageReportResponse'
            requiredProperties:
              - data
              - has_more
              - next_page
        examples:
          example:
            value:
              data:
                - actor:
                    email_address: user@emaildomain.com
                    type: user_actor
                  core_metrics:
                    commits_by_claude_code: 8
                    lines_of_code:
                      added: 342
                      removed: 128
                    num_sessions: 15
                    pull_requests_by_claude_code: 2
                  customer_type: api
                  date: '2025-08-08T00:00:00Z'
                  model_breakdown:
                    - estimated_cost:
                        amount: 186
                        currency: USD
                      model: claude-sonnet-4-20250514
                      tokens:
                        cache_creation: 2340
                        cache_read: 8790
                        input: 45230
                        output: 12450
                    - estimated_cost:
                        amount: 42
                        currency: USD
                      model: claude-3-5-haiku-20241022
                      tokens:
                        cache_creation: 890
                        cache_read: 3420
                        input: 23100
                        output: 5680
                  organization_id: 12345678-1234-5678-1234-567812345678
                  subscription_type: enterprise
                  terminal_type: iTerm.app
                  tool_actions:
                    edit_tool:
                      accepted: 25
                      rejected: 3
                    multi_edit_tool:
                      accepted: 12
                      rejected: 1
                    notebook_edit_tool:
                      accepted: 5
                      rejected: 2
                    write_tool:
                      accepted: 8
                      rejected: 0
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
    ApiActor:
      properties:
        api_key_name:
          type: string
          title: Api Key Name
          description: Name of the API key used to perform Claude Code actions.
          examples:
            - Developer Key
        type:
          type: string
          enum:
            - api_actor
          const: api_actor
          title: Type
      type: object
      required:
        - api_key_name
        - type
      title: ApiActor
    ApprovalMetrics:
      properties:
        accepted:
          type: integer
          title: Accepted
          description: Number of tool action proposals that the user accepted.
        rejected:
          type: integer
          title: Rejected
          description: Number of tool action proposals that the user rejected.
      type: object
      required:
        - accepted
        - rejected
      title: ApprovalMetrics
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
    ClaudeCodeUsageReportItem:
      properties:
        actor:
          anyOf:
            - $ref: '#/components/schemas/UserActor'
            - $ref: '#/components/schemas/ApiActor'
          title: Actor
          description: The user or API key that performed the Claude Code actions.
        core_metrics:
          $ref: '#/components/schemas/CoreMetrics'
          description: Core productivity metrics measuring Claude Code usage and impact.
          examples:
            - commits_by_claude_code: 8
              lines_of_code:
                added: 342
                removed: 128
              num_sessions: 15
              pull_requests_by_claude_code: 2
        customer_type:
          $ref: '#/components/schemas/CustomerType'
          description: >-
            Type of customer account (api for API customers, subscription for
            Pro/Team customers).
          examples:
            - api
            - subscription
        date:
          type: string
          format: date-time
          title: Date
          description: UTC date for the usage metrics in YYYY-MM-DD format.
          examples:
            - '2025-08-08T00:00:00Z'
        model_breakdown:
          items:
            $ref: '#/components/schemas/ModelBreakdown'
          type: array
          title: Model Breakdown
          description: Token usage and cost breakdown by AI model used.
          examples:
            - - estimated_cost:
                  amount: 186
                  currency: USD
                model: claude-sonnet-4-20250514
                tokens:
                  cache_creation: 2340
                  cache_read: 8790
                  input: 45230
                  output: 12450
              - estimated_cost:
                  amount: 42
                  currency: USD
                model: claude-3-5-haiku-20241022
                tokens:
                  cache_creation: 890
                  cache_read: 3420
                  input: 23100
                  output: 5680
        organization_id:
          type: string
          title: Organization Id
          description: ID of the organization that owns the Claude Code usage.
          examples:
            - 12345678-1234-5678-1234-567812345678
        subscription_type:
          anyOf:
            - $ref: '#/components/schemas/SubscriptionType'
            - type: 'null'
          description: >-
            Subscription tier for subscription customers. Null for API
            customers.
          examples:
            - enterprise
            - team
            - null
        terminal_type:
          type: string
          title: Terminal Type
          description: Type of terminal or environment where Claude Code was used.
          examples:
            - iTerm.app
            - vscode
            - tmux
        tool_actions:
          additionalProperties:
            $ref: '#/components/schemas/ApprovalMetrics'
          type: object
          title: Tool Actions
          description: >-
            Breakdown of tool action acceptance and rejection rates by tool
            type.
          examples:
            - edit_tool:
                accepted: 25
                rejected: 3
              multi_edit_tool:
                accepted: 12
                rejected: 1
              notebook_edit_tool:
                accepted: 5
                rejected: 2
              write_tool:
                accepted: 8
                rejected: 0
      type: object
      required:
        - actor
        - core_metrics
        - customer_type
        - date
        - model_breakdown
        - organization_id
        - terminal_type
        - tool_actions
      title: ClaudeCodeUsageReportItem
    CoreMetrics:
      properties:
        commits_by_claude_code:
          type: integer
          title: Commits By Claude Code
          description: >-
            Number of git commits created through Claude Code's commit
            functionality.
        lines_of_code:
          $ref: '#/components/schemas/LinesOfCode'
          description: Statistics on code changes made through Claude Code.
        num_sessions:
          type: integer
          title: Num Sessions
          description: Number of distinct Claude Code sessions initiated by this actor.
        pull_requests_by_claude_code:
          type: integer
          title: Pull Requests By Claude Code
          description: >-
            Number of pull requests created through Claude Code's PR
            functionality.
      type: object
      required:
        - commits_by_claude_code
        - lines_of_code
        - num_sessions
        - pull_requests_by_claude_code
      title: CoreMetrics
    CustomerType:
      type: string
      enum:
        - api
        - subscription
      title: CustomerType
    EstimatedCost:
      properties:
        amount:
          type: integer
          title: Amount
          description: Estimated cost amount in minor currency units (e.g., cents for USD).
          examples:
            - 150
        currency:
          type: string
          title: Currency
          description: Currency code for the estimated cost (e.g., 'USD').
          examples:
            - USD
      type: object
      required:
        - amount
        - currency
      title: EstimatedCost
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
    LinesOfCode:
      properties:
        added:
          type: integer
          title: Added
          description: Total number of lines of code added across all files by Claude Code.
        removed:
          type: integer
          title: Removed
          description: >-
            Total number of lines of code removed across all files by Claude
            Code.
      type: object
      required:
        - added
        - removed
      title: LinesOfCode
    ModelBreakdown:
      properties:
        estimated_cost:
          $ref: '#/components/schemas/EstimatedCost'
          description: Estimated cost for using this model
        model:
          type: string
          title: Model
          description: Name of the AI model used for Claude Code interactions.
          examples:
            - claude-sonnet-4-20250514
        tokens:
          $ref: '#/components/schemas/TokenUsage'
          description: Token usage breakdown for this model
      type: object
      required:
        - estimated_cost
        - model
        - tokens
      title: ModelBreakdown
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
    SubscriptionType:
      type: string
      enum:
        - enterprise
        - team
      title: SubscriptionType
    TokenUsage:
      properties:
        cache_creation:
          type: integer
          title: Cache Creation
          description: Number of cache creation tokens consumed by this model.
        cache_read:
          type: integer
          title: Cache Read
          description: Number of cache read tokens consumed by this model.
        input:
          type: integer
          title: Input
          description: Number of input tokens consumed by this model.
        output:
          type: integer
          title: Output
          description: Number of output tokens generated by this model.
      type: object
      required:
        - cache_creation
        - cache_read
        - input
        - output
      title: TokenUsage
    UserActor:
      properties:
        email_address:
          type: string
          title: Email Address
          description: Email address of the user who performed Claude Code actions.
          examples:
            - user@emaildomain.com
        type:
          type: string
          enum:
            - user_actor
          const: user_actor
          title: Type
      type: object
      required:
        - email_address
        - type
      title: UserActor

````