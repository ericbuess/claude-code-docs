# Models

## List

`models().list(ModelListParamsparams = ModelListParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : ModelListPage`

**get** `/v1/models`

List available models.

The Models API response can be used to determine which models are available for use in the API. More recently released models are listed first.

### Parameters

- `params: ModelListParams`

  - `afterId: Optional<String>`

    ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

  - `beforeId: Optional<String>`

    ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

  - `limit: Optional<Long>`

    Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `1000`.

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

- `class ModelInfo:`

  - `id: String`

    Unique model identifier.

  - `createdAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the model was released. May be set to an epoch value if the release date is unknown.

  - `displayName: String`

    A human-readable name for the model.

  - `type: JsonValue; "model"constant`

    Object type.

    For Models, this is always `"model"`.

    - `MODEL("model")`

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.models.ModelListPage
import com.anthropic.models.models.ModelListParams

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val page: ModelListPage = client.models().list()
}
```

## Retrieve

`models().retrieve(ModelRetrieveParamsparams = ModelRetrieveParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : ModelInfo`

**get** `/v1/models/{model_id}`

Get a specific model.

The Models API response can be used to determine information about a specific model or resolve a model alias to a model ID.

### Parameters

- `params: ModelRetrieveParams`

  - `modelId: Optional<String>`

    Model identifier or alias.

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

- `class ModelInfo:`

  - `id: String`

    Unique model identifier.

  - `createdAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the model was released. May be set to an epoch value if the release date is unknown.

  - `displayName: String`

    A human-readable name for the model.

  - `type: JsonValue; "model"constant`

    Object type.

    For Models, this is always `"model"`.

    - `MODEL("model")`

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.models.ModelInfo
import com.anthropic.models.models.ModelRetrieveParams

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val modelInfo: ModelInfo = client.models().retrieve("model_id")
}
```

## Domain Types

### Model Info

- `class ModelInfo:`

  - `id: String`

    Unique model identifier.

  - `createdAt: LocalDateTime`

    RFC 3339 datetime string representing the time at which the model was released. May be set to an epoch value if the release date is unknown.

  - `displayName: String`

    A human-readable name for the model.

  - `type: JsonValue; "model"constant`

    Object type.

    For Models, this is always `"model"`.

    - `MODEL("model")`
