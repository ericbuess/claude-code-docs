# List Skill Versions

## OpenAPI

````yaml get /v1/skills/{skill_id}/versions
paths:
  path: /v1/skills/{skill_id}/versions
  method: get
  servers:
    - url: https://api.anthropic.com
  request:
    security: []
    parameters:
      path:
        skill_id:
          schema:
            - type: string
              required: true
              title: Skill Id
              description: |-
                Unique identifier for the skill.

                The format and length of IDs may change over time.
      query:
        page:
          schema:
            - type: string
              required: false
              title: Page
              description: >-
                Optionally set to the `next_page` token from the previous
                response.
            - type: 'null'
              required: false
              title: Page
              description: >-
                Optionally set to the `next_page` token from the previous
                response.
        limit:
          schema:
            - type: integer
              required: false
              title: Limit
              description: |-
                Number of items to return per page.

                Defaults to `20`. Ranges from `1` to `1000`.
            - type: 'null'
              required: false
              title: Limit
              description: |-
                Number of items to return per page.

                Defaults to `20`. Ranges from `1` to `1000`.
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
          "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions"
          \
               -H "x-api-key: $ANTHROPIC_API_KEY" \
               -H "anthropic-version: 2023-06-01" \
               -H "anthropic-beta: skills-2025-10-02"
      - lang: python
        source: |-
          import anthropic

          client = anthropic.Anthropic()

          client.beta.skills.versions.list(
              skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
              betas=["skills-2025-10-02"],
          )
      - lang: javascript
        source: >-
          import Anthropic from '@anthropic-ai/sdk';


          const anthropic = new Anthropic();


          await
          anthropic.beta.skills.versions.list('skill_01AbCdEfGhIjKlMnOpQrStUv',
          {{
            betas: ["skills-2025-10-02"],
          }});
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              data:
                allOf:
                  - items:
                      $ref: '#/components/schemas/SkillVersion'
                    type: array
                    title: Data
                    description: List of skill versions.
              has_more:
                allOf:
                  - type: boolean
                    title: Has More
                    description: >-
                      Indicates if there are more results in the requested page
                      direction.
              next_page:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Next Page
                    description: >-
                      Token to provide in as `page` in the subsequent request to
                      retrieve the next page of data.
                    examples:
                      - page_MjAyNS0wNS0xNFQwMDowMDowMFo=
                      - null
            title: ListSkillVersionsResponse
            refIdentifier: '#/components/schemas/ListSkillVersionsResponse'
            requiredProperties:
              - data
              - has_more
              - next_page
        examples:
          example:
            value:
              data:
                - created_at: '2024-10-30T23:58:27.427722Z'
                  description: A custom skill for doing something useful
                  directory: my-skill
                  id: skillver_01JAbcdefghijklmnopqrstuvw
                  name: my-skill
                  skill_id: skill_01JAbcdefghijklmnopqrstuvw
                  type: skill_version
                  version: '1759178010641129'
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
          title: Type
          type: string
      required:
        - message
        - type
      title: RateLimitError
      type: object
    SkillVersion:
      properties:
        created_at:
          type: string
          title: Created At
          description: ISO 8601 timestamp of when the skill version was created.
          examples:
            - '2024-10-30T23:58:27.427722Z'
        description:
          type: string
          title: Description
          description: |-
            Description of the skill version.

            This is extracted from the SKILL.md file in the skill upload.
          examples:
            - A custom skill for doing something useful
        directory:
          type: string
          title: Directory
          description: >-
            Directory name of the skill version.


            This is the top-level directory name that was extracted from the
            uploaded files.
          examples:
            - my-skill
        id:
          type: string
          title: Id
          description: |-
            Unique identifier for the skill version.

            The format and length of IDs may change over time.
          examples:
            - skillver_01JAbcdefghijklmnopqrstuvw
        name:
          type: string
          title: Name
          description: |-
            Human-readable name of the skill version.

            This is extracted from the SKILL.md file in the skill upload.
          examples:
            - my-skill
        skill_id:
          type: string
          title: Skill Id
          description: Identifier for the skill that this version belongs to.
          examples:
            - skill_01JAbcdefghijklmnopqrstuvw
        type:
          type: string
          title: Type
          description: |-
            Object type.

            For Skill Versions, this is always `"skill_version"`.
          default: skill_version
        version:
          type: string
          title: Version
          description: >-
            Version identifier for the skill.


            Each version is identified by a Unix epoch timestamp (e.g.,
            "1759178010641129").
          examples:
            - '1759178010641129'
      type: object
      required:
        - created_at
        - description
        - directory
        - id
        - name
        - skill_id
        - type
        - version
      title: SkillVersion

````