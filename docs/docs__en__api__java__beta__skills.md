# Skills

## Create

`SkillCreateResponse beta().skills().create(SkillCreateParamsparams = SkillCreateParams.none(), RequestOptionsrequestOptions = RequestOptions.none())`

**post** `/v1/skills`

Create Skill

### Parameters

- `SkillCreateParams params`

  - `Optional<List<AnthropicBeta>> betas`

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

  - `Optional<String> displayTitle`

    Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the model.

  - `Optional<List<String>> files`

    Files to upload for the skill.

    All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.

### Returns

- `class SkillCreateResponse:`

  - `String id`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `String createdAt`

    ISO 8601 timestamp of when the skill was created.

  - `Optional<String> displayTitle`

    Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the model.

  - `Optional<String> latestVersion`

    The latest version identifier for the skill.

    This represents the most recent version of the skill that has been created.

  - `String source`

    Source of the skill.

    This may be one of the following values:

    * `"custom"`: the skill was created by a user
    * `"anthropic"`: the skill was created by Anthropic

  - `String type`

    Object type.

    For Skills, this is always `"skill"`.

  - `String updatedAt`

    ISO 8601 timestamp of when the skill was last updated.

### Example

```java
package com.anthropic.example;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.SkillCreateParams;
import com.anthropic.models.beta.skills.SkillCreateResponse;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        SkillCreateResponse skill = client.beta().skills().create();
    }
}
```

## List

`SkillListPage beta().skills().list(SkillListParamsparams = SkillListParams.none(), RequestOptionsrequestOptions = RequestOptions.none())`

**get** `/v1/skills`

List Skills

### Parameters

- `SkillListParams params`

  - `Optional<Long> limit`

    Number of results to return per page.

    Maximum value is 100. Defaults to 20.

  - `Optional<String> page`

    Pagination token for fetching a specific page of results.

    Pass the value from a previous response's `next_page` field to get the next page of results.

  - `Optional<String> source`

    Filter skills by source.

    If provided, only skills from the specified source will be returned:

    * `"custom"`: only return user-created skills
    * `"anthropic"`: only return Anthropic-created skills

  - `Optional<List<AnthropicBeta>> betas`

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

  - `String id`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `String createdAt`

    ISO 8601 timestamp of when the skill was created.

  - `Optional<String> displayTitle`

    Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the model.

  - `Optional<String> latestVersion`

    The latest version identifier for the skill.

    This represents the most recent version of the skill that has been created.

  - `String source`

    Source of the skill.

    This may be one of the following values:

    * `"custom"`: the skill was created by a user
    * `"anthropic"`: the skill was created by Anthropic

  - `String type`

    Object type.

    For Skills, this is always `"skill"`.

  - `String updatedAt`

    ISO 8601 timestamp of when the skill was last updated.

### Example

```java
package com.anthropic.example;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.SkillListPage;
import com.anthropic.models.beta.skills.SkillListParams;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        SkillListPage page = client.beta().skills().list();
    }
}
```

## Retrieve

`SkillRetrieveResponse beta().skills().retrieve(SkillRetrieveParamsparams = SkillRetrieveParams.none(), RequestOptionsrequestOptions = RequestOptions.none())`

**get** `/v1/skills/{skill_id}`

Get Skill

### Parameters

- `SkillRetrieveParams params`

  - `Optional<String> skillId`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `Optional<List<AnthropicBeta>> betas`

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

  - `String id`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `String createdAt`

    ISO 8601 timestamp of when the skill was created.

  - `Optional<String> displayTitle`

    Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the model.

  - `Optional<String> latestVersion`

    The latest version identifier for the skill.

    This represents the most recent version of the skill that has been created.

  - `String source`

    Source of the skill.

    This may be one of the following values:

    * `"custom"`: the skill was created by a user
    * `"anthropic"`: the skill was created by Anthropic

  - `String type`

    Object type.

    For Skills, this is always `"skill"`.

  - `String updatedAt`

    ISO 8601 timestamp of when the skill was last updated.

### Example

```java
package com.anthropic.example;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.SkillRetrieveParams;
import com.anthropic.models.beta.skills.SkillRetrieveResponse;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        SkillRetrieveResponse skill = client.beta().skills().retrieve("skill_id");
    }
}
```

## Delete

`SkillDeleteResponse beta().skills().delete(SkillDeleteParamsparams = SkillDeleteParams.none(), RequestOptionsrequestOptions = RequestOptions.none())`

**delete** `/v1/skills/{skill_id}`

Delete Skill

### Parameters

- `SkillDeleteParams params`

  - `Optional<String> skillId`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `Optional<List<AnthropicBeta>> betas`

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

  - `String id`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `String type`

    Deleted object type.

    For Skills, this is always `"skill_deleted"`.

### Example

```java
package com.anthropic.example;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.SkillDeleteParams;
import com.anthropic.models.beta.skills.SkillDeleteResponse;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        SkillDeleteResponse skill = client.beta().skills().delete("skill_id");
    }
}
```

# Versions

## Create

`VersionCreateResponse beta().skills().versions().create(VersionCreateParamsparams = VersionCreateParams.none(), RequestOptionsrequestOptions = RequestOptions.none())`

**post** `/v1/skills/{skill_id}/versions`

Create Skill Version

### Parameters

- `VersionCreateParams params`

  - `Optional<String> skillId`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `Optional<List<AnthropicBeta>> betas`

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

  - `Optional<List<String>> files`

    Files to upload for the skill.

    All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.

### Returns

- `class VersionCreateResponse:`

  - `String id`

    Unique identifier for the skill version.

    The format and length of IDs may change over time.

  - `String createdAt`

    ISO 8601 timestamp of when the skill version was created.

  - `String description`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `String directory`

    Directory name of the skill version.

    This is the top-level directory name that was extracted from the uploaded files.

  - `String name`

    Human-readable name of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `String skillId`

    Identifier for the skill that this version belongs to.

  - `String type`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `String version`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```java
package com.anthropic.example;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.versions.VersionCreateParams;
import com.anthropic.models.beta.skills.versions.VersionCreateResponse;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        VersionCreateResponse version = client.beta().skills().versions().create("skill_id");
    }
}
```

## List

`VersionListPage beta().skills().versions().list(VersionListParamsparams = VersionListParams.none(), RequestOptionsrequestOptions = RequestOptions.none())`

**get** `/v1/skills/{skill_id}/versions`

List Skill Versions

### Parameters

- `VersionListParams params`

  - `Optional<String> skillId`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `Optional<Long> limit`

    Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `1000`.

  - `Optional<String> page`

    Optionally set to the `next_page` token from the previous response.

  - `Optional<List<AnthropicBeta>> betas`

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

  - `String id`

    Unique identifier for the skill version.

    The format and length of IDs may change over time.

  - `String createdAt`

    ISO 8601 timestamp of when the skill version was created.

  - `String description`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `String directory`

    Directory name of the skill version.

    This is the top-level directory name that was extracted from the uploaded files.

  - `String name`

    Human-readable name of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `String skillId`

    Identifier for the skill that this version belongs to.

  - `String type`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `String version`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```java
package com.anthropic.example;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.versions.VersionListPage;
import com.anthropic.models.beta.skills.versions.VersionListParams;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        VersionListPage page = client.beta().skills().versions().list("skill_id");
    }
}
```

## Retrieve

`VersionRetrieveResponse beta().skills().versions().retrieve(VersionRetrieveParamsparams, RequestOptionsrequestOptions = RequestOptions.none())`

**get** `/v1/skills/{skill_id}/versions/{version}`

Get Skill Version

### Parameters

- `VersionRetrieveParams params`

  - `String skillId`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `Optional<String> version`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

  - `Optional<List<AnthropicBeta>> betas`

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

  - `String id`

    Unique identifier for the skill version.

    The format and length of IDs may change over time.

  - `String createdAt`

    ISO 8601 timestamp of when the skill version was created.

  - `String description`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `String directory`

    Directory name of the skill version.

    This is the top-level directory name that was extracted from the uploaded files.

  - `String name`

    Human-readable name of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `String skillId`

    Identifier for the skill that this version belongs to.

  - `String type`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `String version`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```java
package com.anthropic.example;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.versions.VersionRetrieveParams;
import com.anthropic.models.beta.skills.versions.VersionRetrieveResponse;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        VersionRetrieveParams params = VersionRetrieveParams.builder()
            .skillId("skill_id")
            .version("version")
            .build();
        VersionRetrieveResponse version = client.beta().skills().versions().retrieve(params);
    }
}
```

## Delete

`VersionDeleteResponse beta().skills().versions().delete(VersionDeleteParamsparams, RequestOptionsrequestOptions = RequestOptions.none())`

**delete** `/v1/skills/{skill_id}/versions/{version}`

Delete Skill Version

### Parameters

- `VersionDeleteParams params`

  - `String skillId`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `Optional<String> version`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

  - `Optional<List<AnthropicBeta>> betas`

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

  - `String id`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

  - `String type`

    Deleted object type.

    For Skill Versions, this is always `"skill_version_deleted"`.

### Example

```java
package com.anthropic.example;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.skills.versions.VersionDeleteParams;
import com.anthropic.models.beta.skills.versions.VersionDeleteResponse;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        VersionDeleteParams params = VersionDeleteParams.builder()
            .skillId("skill_id")
            .version("version")
            .build();
        VersionDeleteResponse version = client.beta().skills().versions().delete(params);
    }
}
```
