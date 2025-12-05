## List

`models.list(**kwargs) -> Page<ModelInfo>`

**get** `/v1/models`

List available models.

The Models API response can be used to determine which models are available for use in the API. More recently released models are listed first.

### Parameters

- `after_id: String`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: String`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `limit: Integer`

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

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

- `class ModelInfo`

  - `id: String`

    Unique model identifier.

  - `created_at: Time`

    RFC 3339 datetime string representing the time at which the model was released. May be set to an epoch value if the release date is unknown.

  - `display_name: String`

    A human-readable name for the model.

  - `type: :model`

    Object type.

    For Models, this is always `"model"`.

    - `:model`

### Example

```ruby
require "anthropic"

anthropic = Anthropic::Client.new(api_key: "my-anthropic-api-key")

page = anthropic.models.list

puts(page)
```
