## Retrieve

`beta.models.retrieve(model_id, **kwargs) -> BetaModelInfo`

**get** `/v1/models/{model_id}`

Get a specific model.

The Models API response can be used to determine information about a specific model or resolve a model alias to a model ID.

### Parameters

- `model_id: String`

  Model identifier or alias.

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

- `class BetaModelInfo`

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

beta_model_info = anthropic.beta.models.retrieve("model_id")

puts(beta_model_info)
```
