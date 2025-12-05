## Upload

`beta.files.upload(**kwargs) -> FileMetadata`

**post** `/v1/files`

Upload File

### Parameters

- `file: String`

  The file to upload

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

- `class FileMetadata`

  - `id: String`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `created_at: Time`

    RFC 3339 datetime string representing when the file was created.

  - `filename: String`

    Original filename of the uploaded file.

  - `mime_type: String`

    MIME type of the file.

  - `size_bytes: Integer`

    Size of the file in bytes.

  - `type: :file`

    Object type.

    For files, this is always `"file"`.

    - `:file`

  - `downloadable: bool`

    Whether the file can be downloaded.

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

file_metadata = anthropic.beta.files.upload(file: Pathname(__FILE__))

puts(file_metadata)
```
