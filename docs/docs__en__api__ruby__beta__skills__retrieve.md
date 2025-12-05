## Retrieve

`beta.skills.retrieve(skill_id, **kwargs) -> SkillRetrieveResponse`

**get** `/v1/skills/{skill_id}`

Get Skill

### Parameters

- `skill_id: String`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `anthropic_beta: Array[AnthropicBeta]`

  Optional header to specify the beta version(s) you want to use.

  - `String`

  - `:"message-batches-2024-09-24" | :"prompt-caching-2024-07-31" | :"computer-use-2024-10-22" | 16 more`

    - `:"message-batches-2024-09-24"`

    - `:"prompt-caching-2024-07-31"`

    - `:"computer-use-2024-10-22"`

    - `:"computer-use-2025-01-24"`

    - `:"pdfs-2024-09-25"`

    - `:"token-counting-2024-11-01"`

    - `:"token-efficient-tools-2025-02-19"`

    - `:"output-128k-2025-02-19"`

    - `:"files-api-2025-04-14"`

    - `:"mcp-client-2025-04-04"`

    - `:"mcp-client-2025-11-20"`

    - `:"dev-full-thinking-2025-05-14"`

    - `:"interleaved-thinking-2025-05-14"`

    - `:"code-execution-2025-05-22"`

    - `:"extended-cache-ttl-2025-04-11"`

    - `:"context-1m-2025-08-07"`

    - `:"context-management-2025-06-27"`

    - `:"model-context-window-exceeded-2025-08-26"`

    - `:"skills-2025-10-02"`

### Returns

- `class SkillRetrieveResponse`

  - `id: String`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `created_at: String`

    ISO 8601 timestamp of when the skill was created.

  - `display_title: String`

    Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the model.

  - `latest_version: String`

    The latest version identifier for the skill.

    This represents the most recent version of the skill that has been created.

  - `source: String`

    Source of the skill.

    This may be one of the following values:

    * `"custom"`: the skill was created by a user
    * `"anthropic"`: the skill was created by Anthropic

  - `type: String`

    Object type.

    For Skills, this is always `"skill"`.

  - `updated_at: String`

    ISO 8601 timestamp of when the skill was last updated.

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

skill = anthropic.beta.skills.retrieve("skill_id")

puts(skill)
```
