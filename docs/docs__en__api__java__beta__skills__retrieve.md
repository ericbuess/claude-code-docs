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
