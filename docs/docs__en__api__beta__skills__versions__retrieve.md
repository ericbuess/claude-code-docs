## Retrieve

**get** `/v1/skills/{skill_id}/versions/{version}`

Get Skill Version

### Path Parameters

- `skill_id: string`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `version: string`

  Version identifier for the skill.

  Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Header Parameters

- `"anthropic-beta": optional array of AnthropicBeta`

  Optional header to specify the beta version(s) you want to use.

  - `UnionMember0 = string`

  - `UnionMember1 = "message-batches-2024-09-24" or "prompt-caching-2024-07-31" or "computer-use-2024-10-22" or 16 more`

    - `"message-batches-2024-09-24"`

    - `"prompt-caching-2024-07-31"`

    - `"computer-use-2024-10-22"`

    - `"computer-use-2025-01-24"`

    - `"pdfs-2024-09-25"`

    - `"token-counting-2024-11-01"`

    - `"token-efficient-tools-2025-02-19"`

    - `"output-128k-2025-02-19"`

    - `"files-api-2025-04-14"`

    - `"mcp-client-2025-04-04"`

    - `"mcp-client-2025-11-20"`

    - `"dev-full-thinking-2025-05-14"`

    - `"interleaved-thinking-2025-05-14"`

    - `"code-execution-2025-05-22"`

    - `"extended-cache-ttl-2025-04-11"`

    - `"context-1m-2025-08-07"`

    - `"context-management-2025-06-27"`

    - `"model-context-window-exceeded-2025-08-26"`

    - `"skills-2025-10-02"`

### Returns

- `id: string`

  Unique identifier for the skill version.

  The format and length of IDs may change over time.

- `created_at: string`

  ISO 8601 timestamp of when the skill version was created.

- `description: string`

  Description of the skill version.

  This is extracted from the SKILL.md file in the skill upload.

- `directory: string`

  Directory name of the skill version.

  This is the top-level directory name that was extracted from the uploaded files.

- `name: string`

  Human-readable name of the skill version.

  This is extracted from the SKILL.md file in the skill upload.

- `skill_id: string`

  Identifier for the skill that this version belongs to.

- `type: string`

  Object type.

  For Skill Versions, this is always `"skill_version"`.

- `version: string`

  Version identifier for the skill.

  Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```http
curl https://api.anthropic.com/v1/skills/$SKILL_ID/versions/$VERSION \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```
