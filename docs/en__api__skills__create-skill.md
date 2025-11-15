# Create Skill

## OpenAPI

````yaml post /v1/skills
paths:
  path: /v1/skills
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
        anthropic-version:
          schema:
            - type: string
              required: true
              title: Anthropic-Version
              description: >-
                The version of the Claude API you want to use.


                Read more about versioning and our version history
                [here](https://docs.claude.com/en/docs/build-with-claude/versioning).
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
      multipart/form-data:
        schemaArray:
          - type: object
            properties:
              display_title:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Display Title
                    description: >-
                      Display title for the skill.


                      This is a human-readable label that is not included in the
                      prompt sent to the model.
              files:
                allOf:
                  - anyOf:
                      - items:
                          type: string
                          format: binary
                        type: array
                      - type: 'null'
                    title: Files
                    description: >-
                      Files to upload for the skill.


                      All files must be in the same top-level directory and must
                      include a SKILL.md file at the root of that directory.
            title: Body_create_skill_v1_skills_post
            refIdentifier: '#/components/schemas/Body_create_skill_v1_skills_post'
        examples:
          example:
            value:
              display_title: <string>
              files:
                - null
    codeSamples:
      - lang: bash
        source: |-
          curl -X POST "https://api.anthropic.com/v1/skills" \
               -H "x-api-key: $ANTHROPIC_API_KEY" \
               -H "anthropic-version: 2023-06-01" \
               -H "anthropic-beta: skills-2025-10-02" \
               -F "display_title=My Excel Skill" \
               -F "files[]=@excel-skill/SKILL.md;filename=excel-skill/SKILL.md" \
               -F "files[]=@excel-skill/process_excel.py;filename=excel-skill/process_excel.py"
      - lang: python
        source: |-
          import anthropic
          from anthropic.lib import files_from_dir

          client = anthropic.Anthropic()

          # Option 1: Using files_from_dir helper
          client.beta.skills.create(
              betas=["skills-2025-10-02"],
              display_title="My Excel Skill",
              files=files_from_dir("excel-skill"),
          )

          # Option 2: Using a zip file
          client.beta.skills.create(
              betas=["skills-2025-10-02"],
              display_title="My Excel Skill",
              files=[open("excel-skill.zip", "rb")],
          )

          # Option 3: Using file tuples (filename, file_content, mime_type)
          client.beta.skills.create(
              betas=["skills-2025-10-02"],
              display_title="My Excel Skill",
              files=[
                  ("excel-skill/SKILL.md", open("excel-skill/SKILL.md", "rb"), "text/markdown"),
                  ("excel-skill/process_excel.py", open("excel-skill/process_excel.py", "rb"), "text/x-python"),
              ],
          )
      - lang: javascript
        source: |-
          import Anthropic, {{ toFile }} from '@anthropic-ai/sdk';
          import fs from 'fs';

          const anthropic = new Anthropic();

          // Option 1: Using a zip file
          await anthropic.beta.skills.create({{
            betas: ["skills-2025-10-02"],
            display_title: 'My Excel Skill',
            files: [fs.createReadStream('excel-skill.zip')],
          }});

          // Option 2: Using individual files
          await anthropic.beta.skills.create({{
            betas: ["skills-2025-10-02"],
            display_title: 'My Excel Skill',
            files: [
              await toFile(fs.createReadStream('excel-skill/SKILL.md'), 'excel-skill/SKILL.md'),
              await toFile(fs.createReadStream('excel-skill/process_excel.py'), 'excel-skill/process_excel.py'),
            ],
          }});
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              created_at:
                allOf:
                  - type: string
                    title: Created At
                    description: ISO 8601 timestamp of when the skill was created.
                    examples:
                      - '2024-10-30T23:58:27.427722Z'
              display_title:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Display Title
                    description: >-
                      Display title for the skill.


                      This is a human-readable label that is not included in the
                      prompt sent to the model.
                    examples:
                      - My Custom Skill
              id:
                allOf:
                  - type: string
                    title: Id
                    description: |-
                      Unique identifier for the skill.

                      The format and length of IDs may change over time.
                    examples:
                      - skill_01JAbcdefghijklmnopqrstuvw
              latest_version:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Latest Version
                    description: >-
                      The latest version identifier for the skill.


                      This represents the most recent version of the skill that
                      has been created.
                    examples:
                      - '1759178010641129'
              source:
                allOf:
                  - type: string
                    title: Source
                    description: |-
                      Source of the skill.

                      This may be one of the following values:
                      * `"custom"`: the skill was created by a user
                      * `"anthropic"`: the skill was created by Anthropic
                    examples:
                      - custom
              type:
                allOf:
                  - type: string
                    title: Type
                    description: |-
                      Object type.

                      For Skills, this is always `"skill"`.
                    default: skill
              updated_at:
                allOf:
                  - type: string
                    title: Updated At
                    description: ISO 8601 timestamp of when the skill was last updated.
                    examples:
                      - '2024-10-30T23:58:27.427722Z'
            title: CreateSkillResponse
            refIdentifier: '#/components/schemas/CreateSkillResponse'
            requiredProperties:
              - created_at
              - display_title
              - id
              - latest_version
              - source
              - type
              - updated_at
        examples:
          example:
            value:
              created_at: '2024-10-30T23:58:27.427722Z'
              display_title: My Custom Skill
              id: skill_01JAbcdefghijklmnopqrstuvw
              latest_version: '1759178010641129'
              source: custom
              type: skill
              updated_at: '2024-10-30T23:58:27.427722Z'
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


          See our [errors
          documentation](https://docs.claude.com/en/docs/build-with-claude/errors)
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

````