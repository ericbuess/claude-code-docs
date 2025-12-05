## Retrieve

**get** `/v1/skills/{skill_id}`

Get Skill

### Path Parameters

- `skill_id: string`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

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

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `created_at: string`

  ISO 8601 timestamp of when the skill was created.

- `display_title: string`

  Display title for the skill.

  This is a human-readable label that is not included in the prompt sent to the model.

- `latest_version: string`

  The latest version identifier for the skill.

  This represents the most recent version of the skill that has been created.

- `source: string`

  Source of the skill.

  This may be one of the following values:

  * `"custom"`: the skill was created by a user
  * `"anthropic"`: the skill was created by Anthropic

- `type: string`

  Object type.

  For Skills, this is always `"skill"`.

- `updated_at: string`

  ISO 8601 timestamp of when the skill was last updated.

### Example

```http
curl https://api.anthropic.com/v1/skills/$SKILL_ID \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```
