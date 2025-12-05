# Skills

## Create

`beta.skills.create(**kwargs) -> SkillCreateResponse`

**post** `/v1/skills`

Create Skill

### Parameters

- `display_title: String`

  Display title for the skill.

  This is a human-readable label that is not included in the prompt sent to the model.

- `files: Array[String]`

  Files to upload for the skill.

  All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.

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

- `class SkillCreateResponse`

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

skill = anthropic.beta.skills.create

puts(skill)
```

## List

`beta.skills.list(**kwargs) -> PageCursor<SkillListResponse>`

**get** `/v1/skills`

List Skills

### Parameters

- `limit: Integer`

  Number of results to return per page.

  Maximum value is 100. Defaults to 20.

- `page: String`

  Pagination token for fetching a specific page of results.

  Pass the value from a previous response's `next_page` field to get the next page of results.

- `source: String`

  Filter skills by source.

  If provided, only skills from the specified source will be returned:

  * `"custom"`: only return user-created skills
  * `"anthropic"`: only return Anthropic-created skills

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

- `class SkillListResponse`

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

page = anthropic.beta.skills.list

puts(page)
```

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

## Delete

`beta.skills.delete(skill_id, **kwargs) -> SkillDeleteResponse`

**delete** `/v1/skills/{skill_id}`

Delete Skill

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

- `class SkillDeleteResponse`

  - `id: String`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `type: String`

    Deleted object type.

    For Skills, this is always `"skill_deleted"`.

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

skill = anthropic.beta.skills.delete("skill_id")

puts(skill)
```

# Versions

## Create

`beta.skills.versions.create(skill_id, **kwargs) -> VersionCreateResponse`

**post** `/v1/skills/{skill_id}/versions`

Create Skill Version

### Parameters

- `skill_id: String`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `files: Array[String]`

  Files to upload for the skill.

  All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.

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

- `class VersionCreateResponse`

  - `id: String`

    Unique identifier for the skill version.

    The format and length of IDs may change over time.

  - `created_at: String`

    ISO 8601 timestamp of when the skill version was created.

  - `description: String`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `directory: String`

    Directory name of the skill version.

    This is the top-level directory name that was extracted from the uploaded files.

  - `name: String`

    Human-readable name of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `skill_id: String`

    Identifier for the skill that this version belongs to.

  - `type: String`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `version: String`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

version = anthropic.beta.skills.versions.create("skill_id")

puts(version)
```

## List

`beta.skills.versions.list(skill_id, **kwargs) -> PageCursor<VersionListResponse>`

**get** `/v1/skills/{skill_id}/versions`

List Skill Versions

### Parameters

- `skill_id: String`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `limit: Integer`

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

- `page: String`

  Optionally set to the `next_page` token from the previous response.

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

- `class VersionListResponse`

  - `id: String`

    Unique identifier for the skill version.

    The format and length of IDs may change over time.

  - `created_at: String`

    ISO 8601 timestamp of when the skill version was created.

  - `description: String`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `directory: String`

    Directory name of the skill version.

    This is the top-level directory name that was extracted from the uploaded files.

  - `name: String`

    Human-readable name of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `skill_id: String`

    Identifier for the skill that this version belongs to.

  - `type: String`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `version: String`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

page = anthropic.beta.skills.versions.list("skill_id")

puts(page)
```

## Retrieve

`beta.skills.versions.retrieve(version, **kwargs) -> VersionRetrieveResponse`

**get** `/v1/skills/{skill_id}/versions/{version}`

Get Skill Version

### Parameters

- `skill_id: String`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `version: String`

  Version identifier for the skill.

  Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

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

- `class VersionRetrieveResponse`

  - `id: String`

    Unique identifier for the skill version.

    The format and length of IDs may change over time.

  - `created_at: String`

    ISO 8601 timestamp of when the skill version was created.

  - `description: String`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `directory: String`

    Directory name of the skill version.

    This is the top-level directory name that was extracted from the uploaded files.

  - `name: String`

    Human-readable name of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `skill_id: String`

    Identifier for the skill that this version belongs to.

  - `type: String`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `version: String`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

version = anthropic.beta.skills.versions.retrieve("version", skill_id: "skill_id")

puts(version)
```

## Delete

`beta.skills.versions.delete(version, **kwargs) -> VersionDeleteResponse`

**delete** `/v1/skills/{skill_id}/versions/{version}`

Delete Skill Version

### Parameters

- `skill_id: String`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `version: String`

  Version identifier for the skill.

  Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

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

- `class VersionDeleteResponse`

  - `id: String`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

  - `type: String`

    Deleted object type.

    For Skill Versions, this is always `"skill_version_deleted"`.

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

version = anthropic.beta.skills.versions.delete("version", skill_id: "skill_id")

puts(version)
```
