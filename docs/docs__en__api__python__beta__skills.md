# Skills

## Create

`beta.skills.create(SkillCreateParams**kwargs)  -> SkillCreateResponse`

**post** `/v1/skills`

Create Skill

### Parameters

- `display_title: Optional[str]`

  Display title for the skill.

  This is a human-readable label that is not included in the prompt sent to the model.

- `files: Optional[SequenceNotStr[FileTypes]]`

  Files to upload for the skill.

  All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.

- `betas: Optional[List[AnthropicBetaParam]]`

  Optional header to specify the beta version(s) you want to use.

  - `UnionMember0 = str`

  - `UnionMember1 = Literal["message-batches-2024-09-24", "prompt-caching-2024-07-31", "computer-use-2024-10-22", 16 more]`

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

- `class SkillCreateResponse: …`

  - `id: str`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `created_at: str`

    ISO 8601 timestamp of when the skill was created.

  - `display_title: Optional[str]`

    Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the model.

  - `latest_version: Optional[str]`

    The latest version identifier for the skill.

    This represents the most recent version of the skill that has been created.

  - `source: str`

    Source of the skill.

    This may be one of the following values:

    * `"custom"`: the skill was created by a user
    * `"anthropic"`: the skill was created by Anthropic

  - `type: str`

    Object type.

    For Skills, this is always `"skill"`.

  - `updated_at: str`

    ISO 8601 timestamp of when the skill was last updated.

### Example

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="my-anthropic-api-key",
)
skill = client.beta.skills.create()
print(skill.id)
```

## List

`beta.skills.list(SkillListParams**kwargs)  -> SyncPageCursor[SkillListResponse]`

**get** `/v1/skills`

List Skills

### Parameters

- `limit: Optional[int]`

  Number of results to return per page.

  Maximum value is 100. Defaults to 20.

- `page: Optional[str]`

  Pagination token for fetching a specific page of results.

  Pass the value from a previous response's `next_page` field to get the next page of results.

- `source: Optional[str]`

  Filter skills by source.

  If provided, only skills from the specified source will be returned:

  * `"custom"`: only return user-created skills
  * `"anthropic"`: only return Anthropic-created skills

- `betas: Optional[List[AnthropicBetaParam]]`

  Optional header to specify the beta version(s) you want to use.

  - `UnionMember0 = str`

  - `UnionMember1 = Literal["message-batches-2024-09-24", "prompt-caching-2024-07-31", "computer-use-2024-10-22", 16 more]`

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

- `class SkillListResponse: …`

  - `id: str`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `created_at: str`

    ISO 8601 timestamp of when the skill was created.

  - `display_title: Optional[str]`

    Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the model.

  - `latest_version: Optional[str]`

    The latest version identifier for the skill.

    This represents the most recent version of the skill that has been created.

  - `source: str`

    Source of the skill.

    This may be one of the following values:

    * `"custom"`: the skill was created by a user
    * `"anthropic"`: the skill was created by Anthropic

  - `type: str`

    Object type.

    For Skills, this is always `"skill"`.

  - `updated_at: str`

    ISO 8601 timestamp of when the skill was last updated.

### Example

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="my-anthropic-api-key",
)
page = client.beta.skills.list()
page = page.data[0]
print(page.id)
```

## Retrieve

`beta.skills.retrieve(strskill_id, SkillRetrieveParams**kwargs)  -> SkillRetrieveResponse`

**get** `/v1/skills/{skill_id}`

Get Skill

### Parameters

- `skill_id: str`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `betas: Optional[List[AnthropicBetaParam]]`

  Optional header to specify the beta version(s) you want to use.

  - `UnionMember0 = str`

  - `UnionMember1 = Literal["message-batches-2024-09-24", "prompt-caching-2024-07-31", "computer-use-2024-10-22", 16 more]`

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

- `class SkillRetrieveResponse: …`

  - `id: str`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `created_at: str`

    ISO 8601 timestamp of when the skill was created.

  - `display_title: Optional[str]`

    Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the model.

  - `latest_version: Optional[str]`

    The latest version identifier for the skill.

    This represents the most recent version of the skill that has been created.

  - `source: str`

    Source of the skill.

    This may be one of the following values:

    * `"custom"`: the skill was created by a user
    * `"anthropic"`: the skill was created by Anthropic

  - `type: str`

    Object type.

    For Skills, this is always `"skill"`.

  - `updated_at: str`

    ISO 8601 timestamp of when the skill was last updated.

### Example

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="my-anthropic-api-key",
)
skill = client.beta.skills.retrieve(
    skill_id="skill_id",
)
print(skill.id)
```

## Delete

`beta.skills.delete(strskill_id, SkillDeleteParams**kwargs)  -> SkillDeleteResponse`

**delete** `/v1/skills/{skill_id}`

Delete Skill

### Parameters

- `skill_id: str`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `betas: Optional[List[AnthropicBetaParam]]`

  Optional header to specify the beta version(s) you want to use.

  - `UnionMember0 = str`

  - `UnionMember1 = Literal["message-batches-2024-09-24", "prompt-caching-2024-07-31", "computer-use-2024-10-22", 16 more]`

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

- `class SkillDeleteResponse: …`

  - `id: str`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `type: str`

    Deleted object type.

    For Skills, this is always `"skill_deleted"`.

### Example

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="my-anthropic-api-key",
)
skill = client.beta.skills.delete(
    skill_id="skill_id",
)
print(skill.id)
```

# Versions

## Create

`beta.skills.versions.create(strskill_id, VersionCreateParams**kwargs)  -> VersionCreateResponse`

**post** `/v1/skills/{skill_id}/versions`

Create Skill Version

### Parameters

- `skill_id: str`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `files: Optional[SequenceNotStr[FileTypes]]`

  Files to upload for the skill.

  All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.

- `betas: Optional[List[AnthropicBetaParam]]`

  Optional header to specify the beta version(s) you want to use.

  - `UnionMember0 = str`

  - `UnionMember1 = Literal["message-batches-2024-09-24", "prompt-caching-2024-07-31", "computer-use-2024-10-22", 16 more]`

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

- `class VersionCreateResponse: …`

  - `id: str`

    Unique identifier for the skill version.

    The format and length of IDs may change over time.

  - `created_at: str`

    ISO 8601 timestamp of when the skill version was created.

  - `description: str`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `directory: str`

    Directory name of the skill version.

    This is the top-level directory name that was extracted from the uploaded files.

  - `name: str`

    Human-readable name of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `skill_id: str`

    Identifier for the skill that this version belongs to.

  - `type: str`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `version: str`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="my-anthropic-api-key",
)
version = client.beta.skills.versions.create(
    skill_id="skill_id",
)
print(version.id)
```

## List

`beta.skills.versions.list(strskill_id, VersionListParams**kwargs)  -> SyncPageCursor[VersionListResponse]`

**get** `/v1/skills/{skill_id}/versions`

List Skill Versions

### Parameters

- `skill_id: str`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `limit: Optional[int]`

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

- `page: Optional[str]`

  Optionally set to the `next_page` token from the previous response.

- `betas: Optional[List[AnthropicBetaParam]]`

  Optional header to specify the beta version(s) you want to use.

  - `UnionMember0 = str`

  - `UnionMember1 = Literal["message-batches-2024-09-24", "prompt-caching-2024-07-31", "computer-use-2024-10-22", 16 more]`

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

- `class VersionListResponse: …`

  - `id: str`

    Unique identifier for the skill version.

    The format and length of IDs may change over time.

  - `created_at: str`

    ISO 8601 timestamp of when the skill version was created.

  - `description: str`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `directory: str`

    Directory name of the skill version.

    This is the top-level directory name that was extracted from the uploaded files.

  - `name: str`

    Human-readable name of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `skill_id: str`

    Identifier for the skill that this version belongs to.

  - `type: str`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `version: str`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="my-anthropic-api-key",
)
page = client.beta.skills.versions.list(
    skill_id="skill_id",
)
page = page.data[0]
print(page.id)
```

## Retrieve

`beta.skills.versions.retrieve(strversion, VersionRetrieveParams**kwargs)  -> VersionRetrieveResponse`

**get** `/v1/skills/{skill_id}/versions/{version}`

Get Skill Version

### Parameters

- `skill_id: str`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `version: str`

  Version identifier for the skill.

  Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

- `betas: Optional[List[AnthropicBetaParam]]`

  Optional header to specify the beta version(s) you want to use.

  - `UnionMember0 = str`

  - `UnionMember1 = Literal["message-batches-2024-09-24", "prompt-caching-2024-07-31", "computer-use-2024-10-22", 16 more]`

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

- `class VersionRetrieveResponse: …`

  - `id: str`

    Unique identifier for the skill version.

    The format and length of IDs may change over time.

  - `created_at: str`

    ISO 8601 timestamp of when the skill version was created.

  - `description: str`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `directory: str`

    Directory name of the skill version.

    This is the top-level directory name that was extracted from the uploaded files.

  - `name: str`

    Human-readable name of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `skill_id: str`

    Identifier for the skill that this version belongs to.

  - `type: str`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `version: str`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="my-anthropic-api-key",
)
version = client.beta.skills.versions.retrieve(
    version="version",
    skill_id="skill_id",
)
print(version.id)
```

## Delete

`beta.skills.versions.delete(strversion, VersionDeleteParams**kwargs)  -> VersionDeleteResponse`

**delete** `/v1/skills/{skill_id}/versions/{version}`

Delete Skill Version

### Parameters

- `skill_id: str`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `version: str`

  Version identifier for the skill.

  Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

- `betas: Optional[List[AnthropicBetaParam]]`

  Optional header to specify the beta version(s) you want to use.

  - `UnionMember0 = str`

  - `UnionMember1 = Literal["message-batches-2024-09-24", "prompt-caching-2024-07-31", "computer-use-2024-10-22", 16 more]`

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

- `class VersionDeleteResponse: …`

  - `id: str`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

  - `type: str`

    Deleted object type.

    For Skill Versions, this is always `"skill_version_deleted"`.

### Example

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="my-anthropic-api-key",
)
version = client.beta.skills.versions.delete(
    version="version",
    skill_id="skill_id",
)
print(version.id)
```
