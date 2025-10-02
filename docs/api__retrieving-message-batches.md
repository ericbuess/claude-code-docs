# Retrieve a Message Batch

> This endpoint is idempotent and can be used to poll for Message Batch completion. To access the results of a Message Batch, make a request to the `results_url` field in the response.

Learn more about the Message Batches API in our [user guide](/en/docs/build-with-claude/batch-processing)

## OpenAPI

````yaml get /v1/messages/batches/{message_batch_id}
paths:
  path: /v1/messages/batches/{message_batch_id}
  method: get
  servers:
    - url: https://api.anthropic.com
  request:
    security: []
    parameters:
      path:
        message_batch_id:
          schema:
            - type: string
              required: true
              title: Message Batch Id
              description: ID of the Message Batch.
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
        anthropic-version:
          schema:
            - type: string
              required: true
              title: Anthropic-Version
              description: >-
                The version of the Claude API you want to use.


                Read more about versioning and our version history
                [here](https://docs.claude.com/en/api/versioning).
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
    body: {}
    codeSamples:
      - lang: bash
        source: >-
          curl
          https://api.anthropic.com/v1/messages/batches/msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d
          \
               --header "x-api-key: $ANTHROPIC_API_KEY" \
               --header "anthropic-version: 2023-06-01"
      - lang: python
        source: |-
          import anthropic

          client = anthropic.Anthropic()

          client.messages.batches.retrieve(
              "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d",
          )
      - lang: javascript
        source: |-
          import Anthropic from '@anthropic-ai/sdk';

          const anthropic = new Anthropic();

          await anthropic.messages.batches.retrieve(
            "msgbatch_01HkcTjaV5uDC8jWR4ZsDV8d",
          );
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              archived_at:
                allOf:
                  - anyOf:
                      - type: string
                        format: date-time
                      - type: 'null'
                    title: Archived At
                    description: >-
                      RFC 3339 datetime string representing the time at which
                      the Message Batch was archived and its results became
                      unavailable.
                    examples:
                      - '2024-08-20T18:37:24.100435Z'
              cancel_initiated_at:
                allOf:
                  - anyOf:
                      - type: string
                        format: date-time
                      - type: 'null'
                    title: Cancel Initiated At
                    description: >-
                      RFC 3339 datetime string representing the time at which
                      cancellation was initiated for the Message Batch.
                      Specified only if cancellation was initiated.
                    examples:
                      - '2024-08-20T18:37:24.100435Z'
              created_at:
                allOf:
                  - type: string
                    format: date-time
                    title: Created At
                    description: >-
                      RFC 3339 datetime string representing the time at which
                      the Message Batch was created.
                    examples:
                      - '2024-08-20T18:37:24.100435Z'
              ended_at:
                allOf:
                  - anyOf:
                      - type: string
                        format: date-time
                      - type: 'null'
                    title: Ended At
                    description: >-
                      RFC 3339 datetime string representing the time at which
                      processing for the Message Batch ended. Specified only
                      once processing ends.


                      Processing ends when every request in a Message Batch has
                      either succeeded, errored, canceled, or expired.
                    examples:
                      - '2024-08-20T18:37:24.100435Z'
              expires_at:
                allOf:
                  - type: string
                    format: date-time
                    title: Expires At
                    description: >-
                      RFC 3339 datetime string representing the time at which
                      the Message Batch will expire and end processing, which is
                      24 hours after creation.
                    examples:
                      - '2024-08-20T18:37:24.100435Z'
              id:
                allOf:
                  - type: string
                    title: Id
                    description: |-
                      Unique object identifier.

                      The format and length of IDs may change over time.
                    examples:
                      - msgbatch_013Zva2CMHLNnXjNJJKqJ2EF
              processing_status:
                allOf:
                  - type: string
                    enum:
                      - in_progress
                      - canceling
                      - ended
                    title: Processing Status
                    description: Processing status of the Message Batch.
              request_counts:
                allOf:
                  - $ref: '#/components/schemas/RequestCounts'
                    description: >-
                      Tallies requests within the Message Batch, categorized by
                      their status.


                      Requests start as `processing` and move to one of the
                      other statuses only once processing of the entire batch
                      ends. The sum of all values always matches the total
                      number of requests in the batch.
              results_url:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Results Url
                    description: >-
                      URL to a `.jsonl` file containing the results of the
                      Message Batch requests. Specified only once processing
                      ends.


                      Results in the file are not guaranteed to be in the same
                      order as requests. Use the `custom_id` field to match
                      results to requests.
                    examples:
                      - >-
                        https://api.anthropic.com/v1/messages/batches/msgbatch_013Zva2CMHLNnXjNJJKqJ2EF/results
              type:
                allOf:
                  - type: string
                    enum:
                      - message_batch
                    const: message_batch
                    title: Type
                    description: |-
                      Object type.

                      For Message Batches, this is always `"message_batch"`.
                    default: message_batch
            title: MessageBatch
            refIdentifier: '#/components/schemas/MessageBatch'
            requiredProperties:
              - archived_at
              - cancel_initiated_at
              - created_at
              - ended_at
              - expires_at
              - id
              - processing_status
              - request_counts
              - results_url
              - type
        examples:
          example:
            value:
              archived_at: '2024-08-20T18:37:24.100435Z'
              cancel_initiated_at: '2024-08-20T18:37:24.100435Z'
              created_at: '2024-08-20T18:37:24.100435Z'
              ended_at: '2024-08-20T18:37:24.100435Z'
              expires_at: '2024-08-20T18:37:24.100435Z'
              id: msgbatch_013Zva2CMHLNnXjNJJKqJ2EF
              processing_status: in_progress
              request_counts:
                canceled: 10
                errored: 30
                expired: 10
                processing: 100
                succeeded: 50
              results_url: >-
                https://api.anthropic.com/v1/messages/batches/msgbatch_013Zva2CMHLNnXjNJJKqJ2EF/results
              type: message_batch
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
    RequestCounts:
      properties:
        canceled:
          type: integer
          title: Canceled
          description: |-
            Number of requests in the Message Batch that have been canceled.

            This is zero until processing of the entire Message Batch has ended.
          default: 0
          examples:
            - 10
        errored:
          type: integer
          title: Errored
          description: |-
            Number of requests in the Message Batch that encountered an error.

            This is zero until processing of the entire Message Batch has ended.
          default: 0
          examples:
            - 30
        expired:
          type: integer
          title: Expired
          description: |-
            Number of requests in the Message Batch that have expired.

            This is zero until processing of the entire Message Batch has ended.
          default: 0
          examples:
            - 10
        processing:
          type: integer
          title: Processing
          description: Number of requests in the Message Batch that are processing.
          default: 0
          examples:
            - 100
        succeeded:
          type: integer
          title: Succeeded
          description: >-
            Number of requests in the Message Batch that have completed
            successfully.


            This is zero until processing of the entire Message Batch has ended.
          default: 0
          examples:
            - 50
      type: object
      required:
        - canceled
        - errored
        - expired
        - processing
        - succeeded
      title: RequestCounts

````