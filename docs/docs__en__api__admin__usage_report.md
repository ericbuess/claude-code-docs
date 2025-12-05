# Usage Report

## Retrieve Messages

**get** `/v1/organizations/usage_report/messages`

Get Messages Usage Report

### Query Parameters

- `starting_at: string`

  Time buckets that start on or after this RFC 3339 timestamp will be returned.
  Each time bucket will be snapped to the start of the minute/hour/day in UTC.

- `api_key_ids: optional array of string`

  Restrict usage returned to the specified API key ID(s).

- `bucket_width: optional "1d" or "1m" or "1h"`

  Time granularity of the response data.

  - `"1d"`

  - `"1m"`

  - `"1h"`

- `context_window: optional array of "0-200k" or "200k-1M"`

  Restrict usage returned to the specified context window(s).

  - `"0-200k"`

  - `"200k-1M"`

- `ending_at: optional string`

  Time buckets that end before this RFC 3339 timestamp will be returned.

- `group_by: optional array of "api_key_id" or "workspace_id" or "model" or 2 more`

  Group by any subset of the available options.

  - `"api_key_id"`

  - `"workspace_id"`

  - `"model"`

  - `"service_tier"`

  - `"context_window"`

- `limit: optional number`

  Maximum number of time buckets to return in the response.

  The default and max limits depend on `bucket_width`:
  • `"1d"`: Default of 7 days, maximum of 31 days
  • `"1h"`: Default of 24 hours, maximum of 168 hours
  • `"1m"`: Default of 60 minutes, maximum of 1440 minutes

- `models: optional array of string`

  Restrict usage returned to the specified model(s).

- `page: optional string`

  Optionally set to the `next_page` token from the previous response.

- `service_tiers: optional array of "standard" or "batch" or "priority" or 3 more`

  Restrict usage returned to the specified service tier(s).

  - `"standard"`

  - `"batch"`

  - `"priority"`

  - `"priority_on_demand"`

  - `"flex"`

  - `"flex_discount"`

- `workspace_ids: optional array of string`

  Restrict usage returned to the specified workspace ID(s).

### Returns

- `MessagesUsageReport = object { data, has_more, next_page }`

  - `data: array of object { ending_at, results, starting_at }`

    - `ending_at: string`

      End of the time bucket (exclusive) in RFC 3339 format.

    - `results: array of object { api_key_id, cache_creation, cache_read_input_tokens, 7 more }`

      List of usage items for this time bucket.  There may be multiple items if one or more `group_by[]` parameters are specified.

      - `api_key_id: string`

        ID of the API key used. Null if not grouping by API key or for usage in the Anthropic Console.

      - `cache_creation: object { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens }`

        The number of input tokens for cache creation.

        - `ephemeral_1h_input_tokens: number`

          The number of input tokens used to create the 1 hour cache entry.

        - `ephemeral_5m_input_tokens: number`

          The number of input tokens used to create the 5 minute cache entry.

      - `cache_read_input_tokens: number`

        The number of input tokens read from the cache.

      - `context_window: "0-200k" or "200k-1M"`

        Context window used. Null if not grouping by context window.

        - `"0-200k"`

        - `"200k-1M"`

      - `model: string`

        Model used. Null if not grouping by model.

      - `output_tokens: number`

        The number of output tokens generated.

      - `server_tool_use: object { web_search_requests }`

        Server-side tool usage metrics.

        - `web_search_requests: number`

          The number of web search requests made.

      - `service_tier: "standard" or "batch" or "priority" or 3 more`

        Service tier used. Null if not grouping by service tier.

        - `"standard"`

        - `"batch"`

        - `"priority"`

        - `"priority_on_demand"`

        - `"flex"`

        - `"flex_discount"`

      - `uncached_input_tokens: number`

        The number of uncached input tokens processed.

      - `workspace_id: string`

        ID of the Workspace used. Null if not grouping by workspace or for the default workspace.

    - `starting_at: string`

      Start of the time bucket (inclusive) in RFC 3339 format.

  - `has_more: boolean`

    Indicates if there are more results.

  - `next_page: string`

    Token to provide in as `page` in the subsequent request to retrieve the next page of data.

### Example

```http
curl https://api.anthropic.com/v1/organizations/usage_report/messages \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Retrieve Claude Code

**get** `/v1/organizations/usage_report/claude_code`

Retrieve daily aggregated usage metrics for Claude Code users.
Enables organizations to analyze developer productivity and build custom dashboards.

### Query Parameters

- `starting_at: string`

  UTC date in YYYY-MM-DD format. Returns metrics for this single day only.

- `limit: optional number`

  Number of records per page (default: 20, max: 1000).

- `page: optional string`

  Opaque cursor token from previous response's `next_page` field.

### Returns

- `ClaudeCodeUsageReport = object { data, has_more, next_page }`

  - `data: array of object { actor, core_metrics, customer_type, 6 more }`

    List of Claude Code usage records for the requested date.

    - `actor: object { email_address, type }  or object { api_key_name, type }`

      The user or API key that performed the Claude Code actions.

      - `UserActor = object { email_address, type }`

        - `email_address: string`

          Email address of the user who performed Claude Code actions.

        - `type: "user_actor"`

          - `"user_actor"`

      - `APIActor = object { api_key_name, type }`

        - `api_key_name: string`

          Name of the API key used to perform Claude Code actions.

        - `type: "api_actor"`

          - `"api_actor"`

    - `core_metrics: object { commits_by_claude_code, lines_of_code, num_sessions, pull_requests_by_claude_code }`

      Core productivity metrics measuring Claude Code usage and impact.

      - `commits_by_claude_code: number`

        Number of git commits created through Claude Code's commit functionality.

      - `lines_of_code: object { added, removed }`

        Statistics on code changes made through Claude Code.

        - `added: number`

          Total number of lines of code added across all files by Claude Code.

        - `removed: number`

          Total number of lines of code removed across all files by Claude Code.

      - `num_sessions: number`

        Number of distinct Claude Code sessions initiated by this actor.

      - `pull_requests_by_claude_code: number`

        Number of pull requests created through Claude Code's PR functionality.

    - `customer_type: "api" or "subscription"`

      Type of customer account (api for API customers, subscription for Pro/Team customers).

      - `"api"`

      - `"subscription"`

    - `date: string`

      UTC date for the usage metrics in YYYY-MM-DD format.

    - `model_breakdown: array of object { estimated_cost, model, tokens }`

      Token usage and cost breakdown by AI model used.

      - `estimated_cost: object { amount, currency }`

        Estimated cost for using this model

        - `amount: number`

          Estimated cost amount in minor currency units (e.g., cents for USD).

        - `currency: string`

          Currency code for the estimated cost (e.g., 'USD').

      - `model: string`

        Name of the AI model used for Claude Code interactions.

      - `tokens: object { cache_creation, cache_read, input, output }`

        Token usage breakdown for this model

        - `cache_creation: number`

          Number of cache creation tokens consumed by this model.

        - `cache_read: number`

          Number of cache read tokens consumed by this model.

        - `input: number`

          Number of input tokens consumed by this model.

        - `output: number`

          Number of output tokens generated by this model.

    - `organization_id: string`

      ID of the organization that owns the Claude Code usage.

    - `terminal_type: string`

      Type of terminal or environment where Claude Code was used.

    - `tool_actions: map[object { accepted, rejected } ]`

      Breakdown of tool action acceptance and rejection rates by tool type.

      - `accepted: number`

        Number of tool action proposals that the user accepted.

      - `rejected: number`

        Number of tool action proposals that the user rejected.

    - `subscription_type: optional "enterprise" or "team"`

      Subscription tier for subscription customers. Null for API customers.

      - `"enterprise"`

      - `"team"`

  - `has_more: boolean`

    True if there are more records available beyond the current page.

  - `next_page: string`

    Opaque cursor token for fetching the next page of results, or null if no more pages are available.

### Example

```http
curl https://api.anthropic.com/v1/organizations/usage_report/claude_code \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Domain Types

### Claude Code Usage Report

- `ClaudeCodeUsageReport = object { data, has_more, next_page }`

  - `data: array of object { actor, core_metrics, customer_type, 6 more }`

    List of Claude Code usage records for the requested date.

    - `actor: object { email_address, type }  or object { api_key_name, type }`

      The user or API key that performed the Claude Code actions.

      - `UserActor = object { email_address, type }`

        - `email_address: string`

          Email address of the user who performed Claude Code actions.

        - `type: "user_actor"`

          - `"user_actor"`

      - `APIActor = object { api_key_name, type }`

        - `api_key_name: string`

          Name of the API key used to perform Claude Code actions.

        - `type: "api_actor"`

          - `"api_actor"`

    - `core_metrics: object { commits_by_claude_code, lines_of_code, num_sessions, pull_requests_by_claude_code }`

      Core productivity metrics measuring Claude Code usage and impact.

      - `commits_by_claude_code: number`

        Number of git commits created through Claude Code's commit functionality.

      - `lines_of_code: object { added, removed }`

        Statistics on code changes made through Claude Code.

        - `added: number`

          Total number of lines of code added across all files by Claude Code.

        - `removed: number`

          Total number of lines of code removed across all files by Claude Code.

      - `num_sessions: number`

        Number of distinct Claude Code sessions initiated by this actor.

      - `pull_requests_by_claude_code: number`

        Number of pull requests created through Claude Code's PR functionality.

    - `customer_type: "api" or "subscription"`

      Type of customer account (api for API customers, subscription for Pro/Team customers).

      - `"api"`

      - `"subscription"`

    - `date: string`

      UTC date for the usage metrics in YYYY-MM-DD format.

    - `model_breakdown: array of object { estimated_cost, model, tokens }`

      Token usage and cost breakdown by AI model used.

      - `estimated_cost: object { amount, currency }`

        Estimated cost for using this model

        - `amount: number`

          Estimated cost amount in minor currency units (e.g., cents for USD).

        - `currency: string`

          Currency code for the estimated cost (e.g., 'USD').

      - `model: string`

        Name of the AI model used for Claude Code interactions.

      - `tokens: object { cache_creation, cache_read, input, output }`

        Token usage breakdown for this model

        - `cache_creation: number`

          Number of cache creation tokens consumed by this model.

        - `cache_read: number`

          Number of cache read tokens consumed by this model.

        - `input: number`

          Number of input tokens consumed by this model.

        - `output: number`

          Number of output tokens generated by this model.

    - `organization_id: string`

      ID of the organization that owns the Claude Code usage.

    - `terminal_type: string`

      Type of terminal or environment where Claude Code was used.

    - `tool_actions: map[object { accepted, rejected } ]`

      Breakdown of tool action acceptance and rejection rates by tool type.

      - `accepted: number`

        Number of tool action proposals that the user accepted.

      - `rejected: number`

        Number of tool action proposals that the user rejected.

    - `subscription_type: optional "enterprise" or "team"`

      Subscription tier for subscription customers. Null for API customers.

      - `"enterprise"`

      - `"team"`

  - `has_more: boolean`

    True if there are more records available beyond the current page.

  - `next_page: string`

    Opaque cursor token for fetching the next page of results, or null if no more pages are available.

### Messages Usage Report

- `MessagesUsageReport = object { data, has_more, next_page }`

  - `data: array of object { ending_at, results, starting_at }`

    - `ending_at: string`

      End of the time bucket (exclusive) in RFC 3339 format.

    - `results: array of object { api_key_id, cache_creation, cache_read_input_tokens, 7 more }`

      List of usage items for this time bucket.  There may be multiple items if one or more `group_by[]` parameters are specified.

      - `api_key_id: string`

        ID of the API key used. Null if not grouping by API key or for usage in the Anthropic Console.

      - `cache_creation: object { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens }`

        The number of input tokens for cache creation.

        - `ephemeral_1h_input_tokens: number`

          The number of input tokens used to create the 1 hour cache entry.

        - `ephemeral_5m_input_tokens: number`

          The number of input tokens used to create the 5 minute cache entry.

      - `cache_read_input_tokens: number`

        The number of input tokens read from the cache.

      - `context_window: "0-200k" or "200k-1M"`

        Context window used. Null if not grouping by context window.

        - `"0-200k"`

        - `"200k-1M"`

      - `model: string`

        Model used. Null if not grouping by model.

      - `output_tokens: number`

        The number of output tokens generated.

      - `server_tool_use: object { web_search_requests }`

        Server-side tool usage metrics.

        - `web_search_requests: number`

          The number of web search requests made.

      - `service_tier: "standard" or "batch" or "priority" or 3 more`

        Service tier used. Null if not grouping by service tier.

        - `"standard"`

        - `"batch"`

        - `"priority"`

        - `"priority_on_demand"`

        - `"flex"`

        - `"flex_discount"`

      - `uncached_input_tokens: number`

        The number of uncached input tokens processed.

      - `workspace_id: string`

        ID of the Workspace used. Null if not grouping by workspace or for the default workspace.

    - `starting_at: string`

      Start of the time bucket (inclusive) in RFC 3339 format.

  - `has_more: boolean`

    Indicates if there are more results.

  - `next_page: string`

    Token to provide in as `page` in the subsequent request to retrieve the next page of data.
