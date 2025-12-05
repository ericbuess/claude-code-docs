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
