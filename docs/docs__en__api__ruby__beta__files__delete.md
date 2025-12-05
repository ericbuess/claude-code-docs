## Delete

`beta.files.delete(file_id, **kwargs) -> DeletedFile`

**delete** `/v1/files/{file_id}`

Delete File

### Parameters

- `file_id: String`

  ID of the File.

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

- `class DeletedFile`

  - `id: String`

    ID of the deleted file.

  - `type: :file_deleted`

    Deleted object type.

    For file deletion, this is always `"file_deleted"`.

    - `:file_deleted`

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

deleted_file = anthropic.beta.files.delete("file_id")

puts(deleted_file)
```
