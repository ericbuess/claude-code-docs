# Files

## Upload

`beta().files().upload(FileUploadParamsparams, RequestOptionsrequestOptions = RequestOptions.none()) : FileMetadata`

**post** `/v1/files`

Upload File

### Parameters

- `params: FileUploadParams`

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

  - `file: String`

    The file to upload

### Returns

- `class FileMetadata:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `createdAt: LocalDateTime`

    RFC 3339 datetime string representing when the file was created.

  - `filename: String`

    Original filename of the uploaded file.

  - `mimeType: String`

    MIME type of the file.

  - `sizeBytes: Long`

    Size of the file in bytes.

  - `type: JsonValue; "file"constant`

    Object type.

    For files, this is always `"file"`.

    - `FILE("file")`

  - `downloadable: Optional<Boolean>`

    Whether the file can be downloaded.

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.files.FileMetadata
import com.anthropic.models.beta.files.FileUploadParams
import java.io.ByteArrayInputStream

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val params: FileUploadParams = FileUploadParams.builder()
        .file("some content".byteInputStream())
        .build()
    val fileMetadata: FileMetadata = client.beta().files().upload(params)
}
```

## List

`beta().files().list(FileListParamsparams = FileListParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : FileListPage`

**get** `/v1/files`

List Files

### Parameters

- `params: FileListParams`

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

- `class FileMetadata:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `createdAt: LocalDateTime`

    RFC 3339 datetime string representing when the file was created.

  - `filename: String`

    Original filename of the uploaded file.

  - `mimeType: String`

    MIME type of the file.

  - `sizeBytes: Long`

    Size of the file in bytes.

  - `type: JsonValue; "file"constant`

    Object type.

    For files, this is always `"file"`.

    - `FILE("file")`

  - `downloadable: Optional<Boolean>`

    Whether the file can be downloaded.

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.files.FileListPage
import com.anthropic.models.beta.files.FileListParams

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val page: FileListPage = client.beta().files().list()
}
```

## Download

`beta().files().download(FileDownloadParamsparams = FileDownloadParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : HttpResponse`

**get** `/v1/files/{file_id}/content`

Download File

### Parameters

- `params: FileDownloadParams`

  - `fileId: Optional<String>`

    ID of the File.

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

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.core.http.HttpResponse
import com.anthropic.models.beta.files.FileDownloadParams

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val response: HttpResponse = client.beta().files().download("file_id")
}
```

## Retrieve Metadata

`beta().files().retrieveMetadata(FileRetrieveMetadataParamsparams = FileRetrieveMetadataParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : FileMetadata`

**get** `/v1/files/{file_id}`

Get File Metadata

### Parameters

- `params: FileRetrieveMetadataParams`

  - `fileId: Optional<String>`

    ID of the File.

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

- `class FileMetadata:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `createdAt: LocalDateTime`

    RFC 3339 datetime string representing when the file was created.

  - `filename: String`

    Original filename of the uploaded file.

  - `mimeType: String`

    MIME type of the file.

  - `sizeBytes: Long`

    Size of the file in bytes.

  - `type: JsonValue; "file"constant`

    Object type.

    For files, this is always `"file"`.

    - `FILE("file")`

  - `downloadable: Optional<Boolean>`

    Whether the file can be downloaded.

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.files.FileMetadata
import com.anthropic.models.beta.files.FileRetrieveMetadataParams

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val fileMetadata: FileMetadata = client.beta().files().retrieveMetadata("file_id")
}
```

## Delete

`beta().files().delete(FileDeleteParamsparams = FileDeleteParams.none(), RequestOptionsrequestOptions = RequestOptions.none()) : DeletedFile`

**delete** `/v1/files/{file_id}`

Delete File

### Parameters

- `params: FileDeleteParams`

  - `fileId: Optional<String>`

    ID of the File.

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

- `class DeletedFile:`

  - `id: String`

    ID of the deleted file.

  - `type: Optional<Type>`

    Deleted object type.

    For file deletion, this is always `"file_deleted"`.

    - `FILE_DELETED("file_deleted")`

### Example

```kotlin
package com.anthropic.example

import com.anthropic.client.AnthropicClient
import com.anthropic.client.okhttp.AnthropicOkHttpClient
import com.anthropic.models.beta.files.DeletedFile
import com.anthropic.models.beta.files.FileDeleteParams

fun main() {
    val client: AnthropicClient = AnthropicOkHttpClient.fromEnv()

    val deletedFile: DeletedFile = client.beta().files().delete("file_id")
}
```

## Domain Types

### Deleted File

- `class DeletedFile:`

  - `id: String`

    ID of the deleted file.

  - `type: Optional<Type>`

    Deleted object type.

    For file deletion, this is always `"file_deleted"`.

    - `FILE_DELETED("file_deleted")`

### File Metadata

- `class FileMetadata:`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `createdAt: LocalDateTime`

    RFC 3339 datetime string representing when the file was created.

  - `filename: String`

    Original filename of the uploaded file.

  - `mimeType: String`

    MIME type of the file.

  - `sizeBytes: Long`

    Size of the file in bytes.

  - `type: JsonValue; "file"constant`

    Object type.

    For files, this is always `"file"`.

    - `FILE("file")`

  - `downloadable: Optional<Boolean>`

    Whether the file can be downloaded.
