# Skills

## Create

`beta().skills().create(SkillCreateParamsparams = SkillCreateParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : SkillCreateResponse`

**post** `/v1/skills`

Create Skill

### Parameters

- `params: SkillCreateParams`

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

  - `displayTitle: Optional<String>`

    Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the model.

  - `files: Optional<List<String>>`

    Files to upload for the skill.

    All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.

### Returns

- `class SkillCreateResponse:`

  - `id: String`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `createdAt: String`

    ISO 8601 timestamp of when the skill was created.

  - `displayTitle: Optional<String>`

    Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the model.

  - `latestVersion: Optional<String>`

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

  - `updatedAt: String`

    ISO 8601 timestamp of when the skill was last updated.

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.skills.SkillCreateParams
import com.anthropic.models.beta.skills.SkillCreateResponse

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val skill: SkillCreateResponse = client.beta().skills().create()
}
```

## List

`beta().skills().list(SkillListParamsparams = SkillListParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : SkillListPage`

**get** `/v1/skills`

List Skills

### Parameters

- `params: SkillListParams`

  - `limit: Optional<Long>`

    Number of results to return per page.

    Maximum value is 100. Defaults to 20.

  - `page: Optional<String>`

    Pagination token for fetching a specific page of results.

    Pass the value from a previous response's `next_page` field to get the next page of results.

  - `source: Optional<String>`

    Filter skills by source.

    If provided, only skills from the specified source will be returned:

    * `"custom"`: only return user-created skills
    * `"anthropic"`: only return Anthropic-created skills

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

### Returns

- `class SkillListResponse:`

  - `id: String`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `createdAt: String`

    ISO 8601 timestamp of when the skill was created.

  - `displayTitle: Optional<String>`

    Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the model.

  - `latestVersion: Optional<String>`

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

  - `updatedAt: String`

    ISO 8601 timestamp of when the skill was last updated.

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.skills.SkillListPage
import com.anthropic.models.beta.skills.SkillListParams

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val page: SkillListPage = client.beta().skills().list()
}
```

## Retrieve

`beta().skills().retrieve(SkillRetrieveParamsparams = SkillRetrieveParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : SkillRetrieveResponse`

**get** `/v1/skills/{skill_id}`

Get Skill

### Parameters

- `params: SkillRetrieveParams`

  - `skillId: Optional<String>`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

### Returns

- `class SkillRetrieveResponse:`

  - `id: String`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `createdAt: String`

    ISO 8601 timestamp of when the skill was created.

  - `displayTitle: Optional<String>`

    Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the model.

  - `latestVersion: Optional<String>`

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

  - `updatedAt: String`

    ISO 8601 timestamp of when the skill was last updated.

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.skills.SkillRetrieveParams
import com.anthropic.models.beta.skills.SkillRetrieveResponse

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val skill: SkillRetrieveResponse = client.beta().skills().retrieve("skill_id")
}
```

## Delete

`beta().skills().delete(SkillDeleteParamsparams = SkillDeleteParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : SkillDeleteResponse`

**delete** `/v1/skills/{skill_id}`

Delete Skill

### Parameters

- `params: SkillDeleteParams`

  - `skillId: Optional<String>`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

### Returns

- `class SkillDeleteResponse:`

  - `id: String`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `type: String`

    Deleted object type.

    For Skills, this is always `"skill_deleted"`.

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.skills.SkillDeleteParams
import com.anthropic.models.beta.skills.SkillDeleteResponse

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val skill: SkillDeleteResponse = client.beta().skills().delete("skill_id")
}
```

# Versions

## Create

`beta().skills().versions().create(VersionCreateParamsparams = VersionCreateParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : VersionCreateResponse`

**post** `/v1/skills/{skill_id}/versions`

Create Skill Version

### Parameters

- `params: VersionCreateParams`

  - `skillId: Optional<String>`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

  - `files: Optional<List<String>>`

    Files to upload for the skill.

    All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.

### Returns

- `class VersionCreateResponse:`

  - `id: String`

    Unique identifier for the skill version.

    The format and length of IDs may change over time.

  - `createdAt: String`

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

  - `skillId: String`

    Identifier for the skill that this version belongs to.

  - `type: String`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `version: String`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.skills.versions.VersionCreateParams
import com.anthropic.models.beta.skills.versions.VersionCreateResponse

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val version: VersionCreateResponse = client.beta().skills().versions().create("skill_id")
}
```

## List

`beta().skills().versions().list(VersionListParamsparams = VersionListParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : VersionListPage`

**get** `/v1/skills/{skill_id}/versions`

List Skill Versions

### Parameters

- `params: VersionListParams`

  - `skillId: Optional<String>`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `limit: Optional<Long>`

    Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `1000`.

  - `page: Optional<String>`

    Optionally set to the `next_page` token from the previous response.

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

### Returns

- `class VersionListResponse:`

  - `id: String`

    Unique identifier for the skill version.

    The format and length of IDs may change over time.

  - `createdAt: String`

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

  - `skillId: String`

    Identifier for the skill that this version belongs to.

  - `type: String`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `version: String`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.skills.versions.VersionListPage
import com.anthropic.models.beta.skills.versions.VersionListParams

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val page: VersionListPage = client.beta().skills().versions().list("skill_id")
}
```

## Retrieve

`beta().skills().versions().retrieve(VersionRetrieveParamsparams, RequestOptionsrequestOptions = RequestOptions.none()) : VersionRetrieveResponse`

**get** `/v1/skills/{skill_id}/versions/{version}`

Get Skill Version

### Parameters

- `params: VersionRetrieveParams`

  - `skillId: String`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `version: Optional<String>`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

### Returns

- `class VersionRetrieveResponse:`

  - `id: String`

    Unique identifier for the skill version.

    The format and length of IDs may change over time.

  - `createdAt: String`

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

  - `skillId: String`

    Identifier for the skill that this version belongs to.

  - `type: String`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `version: String`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.skills.versions.VersionRetrieveParams
import com.anthropic.models.beta.skills.versions.VersionRetrieveResponse

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val params: VersionRetrieveParams = VersionRetrieveParams.builder()
        .skillId("skill_id")
        .version("version")
        .build()
    val version: VersionRetrieveResponse = client.beta().skills().versions().retrieve(params)
}
```

## Delete

`beta().skills().versions().delete(VersionDeleteParamsparams, RequestOptionsrequestOptions = RequestOptions.none()) : VersionDeleteResponse`

**delete** `/v1/skills/{skill_id}/versions/{version}`

Delete Skill Version

### Parameters

- `params: VersionDeleteParams`

  - `skillId: String`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `version: Optional<String>`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

  - `betas: Optional<List<AnthropicBeta>>`

    Optional header to specify the beta version(s) you want to use.

    - `MESSAGE_BATCHES_2024_09_24("message-batches-2024-09-24")`

    - `PROMPT_CACHING_2024_07_31("prompt-caching-2024-07-31")`

    - `COMPUTER_USE_2024_10_22("computer-use-2024-10-22")`

    - `COMPUTER_USE_2025_01_24("computer-use-2025-01-24")`

    - `PDFS_2024_09_25("pdfs-2024-09-25")`

    - `TOKEN_COUNTING_2024_11_01("token-counting-2024-11-01")`

    - `TOKEN_EFFICIENT_TOOLS_2025_02_19("token-efficient-tools-2025-02-19")`

    - `OUTPUT_128K_2025_02_19("output-128k-2025-02-19")`

    - `FILES_API_2025_04_14("files-api-2025-04-14")`

    - `MCP_CLIENT_2025_04_04("mcp-client-2025-04-04")`

    - `MCP_CLIENT_2025_11_20("mcp-client-2025-11-20")`

    - `DEV_FULL_THINKING_2025_05_14("dev-full-thinking-2025-05-14")`

    - `INTERLEAVED_THINKING_2025_05_14("interleaved-thinking-2025-05-14")`

    - `CODE_EXECUTION_2025_05_22("code-execution-2025-05-22")`

    - `EXTENDED_CACHE_TTL_2025_04_11("extended-cache-ttl-2025-04-11")`

    - `CONTEXT_1M_2025_08_07("context-1m-2025-08-07")`

    - `CONTEXT_MANAGEMENT_2025_06_27("context-management-2025-06-27")`

    - `MODEL_CONTEXT_WINDOW_EXCEEDED_2025_08_26("model-context-window-exceeded-2025-08-26")`

    - `SKILLS_2025_10_02("skills-2025-10-02")`

### Returns

- `class VersionDeleteResponse:`

  - `id: String`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

  - `type: String`

    Deleted object type.

    For Skill Versions, this is always `"skill_version_deleted"`.

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.skills.versions.VersionDeleteParams
import com.anthropic.models.beta.skills.versions.VersionDeleteResponse

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val params: VersionDeleteParams = VersionDeleteParams.builder()
        .skillId("skill_id")
        .version("version")
        .build()
    val version: VersionDeleteResponse = client.beta().skills().versions().delete(params)
}
```
