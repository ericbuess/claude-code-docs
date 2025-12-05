# Versions

## Create

`client.beta.skills.versions.create(stringskillID, VersionCreateParamsparams?, RequestOptionsoptions?): VersionCreateResponse`

**post** `/v1/skills/{skill_id}/versions`

Create Skill Version

### Parameters

- `skillID: string`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `params: VersionCreateParams`

  - `files?: Array<Uploadable> | null`

    Body param: Files to upload for the skill.

    All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.

  - `betas?: Array<AnthropicBeta>`

    Header param: Optional header to specify the beta version(s) you want to use.

    - `(string & {})`

    - `"message-batches-2024-09-24" | "prompt-caching-2024-07-31" | "computer-use-2024-10-22" | 16 more`

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

- `VersionCreateResponse`

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

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: 'my-anthropic-api-key',
});

const version = await client.beta.skills.versions.create('skill_id');

console.log(version.id);
```

## List

`client.beta.skills.versions.list(stringskillID, VersionListParamsparams?, RequestOptionsoptions?): PageCursor<VersionListResponse>`

**get** `/v1/skills/{skill_id}/versions`

List Skill Versions

### Parameters

- `skillID: string`

  Unique identifier for the skill.

  The format and length of IDs may change over time.

- `params: VersionListParams`

  - `limit?: number | null`

    Query param: Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `1000`.

  - `page?: string | null`

    Query param: Optionally set to the `next_page` token from the previous response.

  - `betas?: Array<AnthropicBeta>`

    Header param: Optional header to specify the beta version(s) you want to use.

    - `(string & {})`

    - `"message-batches-2024-09-24" | "prompt-caching-2024-07-31" | "computer-use-2024-10-22" | 16 more`

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

- `VersionListResponse`

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

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: 'my-anthropic-api-key',
});

// Automatically fetches more pages as needed.
for await (const versionListResponse of client.beta.skills.versions.list('skill_id')) {
  console.log(versionListResponse.id);
}
```

## Retrieve

`client.beta.skills.versions.retrieve(stringversion, VersionRetrieveParamsparams, RequestOptionsoptions?): VersionRetrieveResponse`

**get** `/v1/skills/{skill_id}/versions/{version}`

Get Skill Version

### Parameters

- `version: string`

  Version identifier for the skill.

  Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

- `params: VersionRetrieveParams`

  - `skill_id: string`

    Path param: Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `betas?: Array<AnthropicBeta>`

    Header param: Optional header to specify the beta version(s) you want to use.

    - `(string & {})`

    - `"message-batches-2024-09-24" | "prompt-caching-2024-07-31" | "computer-use-2024-10-22" | 16 more`

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

- `VersionRetrieveResponse`

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

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: 'my-anthropic-api-key',
});

const version = await client.beta.skills.versions.retrieve('version', { skill_id: 'skill_id' });

console.log(version.id);
```

## Delete

`client.beta.skills.versions.delete(stringversion, VersionDeleteParamsparams, RequestOptionsoptions?): VersionDeleteResponse`

**delete** `/v1/skills/{skill_id}/versions/{version}`

Delete Skill Version

### Parameters

- `version: string`

  Version identifier for the skill.

  Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

- `params: VersionDeleteParams`

  - `skill_id: string`

    Path param: Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `betas?: Array<AnthropicBeta>`

    Header param: Optional header to specify the beta version(s) you want to use.

    - `(string & {})`

    - `"message-batches-2024-09-24" | "prompt-caching-2024-07-31" | "computer-use-2024-10-22" | 16 more`

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

- `VersionDeleteResponse`

  - `id: string`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

  - `type: string`

    Deleted object type.

    For Skill Versions, this is always `"skill_version_deleted"`.

### Example

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: 'my-anthropic-api-key',
});

const version = await client.beta.skills.versions.delete('version', { skill_id: 'skill_id' });

console.log(version.id);
```
