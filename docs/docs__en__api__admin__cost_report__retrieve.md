## Retrieve

**get** `/v1/organizations/cost_report`

Get Cost Report

### Query Parameters

- `starting_at: string`

  Time buckets that start on or after this RFC 3339 timestamp will be returned.
  Each time bucket will be snapped to the start of the minute/hour/day in UTC.

- `bucket_width: optional "1d"`

  Time granularity of the response data.

  - `"1d"`

- `ending_at: optional string`

  Time buckets that end before this RFC 3339 timestamp will be returned.

- `group_by: optional array of "workspace_id" or "description"`

  Group by any subset of the available options.

  - `"workspace_id"`

  - `"description"`

- `limit: optional number`

  Maximum number of time buckets to return in the response.

- `page: optional string`

  Optionally set to the `next_page` token from the previous response.

### Returns

- `CostReport = object { data, has_more, next_page }`

  - `data: array of object { ending_at, results, starting_at }`

    - `ending_at: string`

      End of the time bucket (exclusive) in RFC 3339 format.

    - `results: array of object { amount, context_window, cost_type, 6 more }`

      List of cost items for this time bucket. There may be multiple items if one or more `group_by[]` parameters are specified.

      - `amount: string`

        Cost amount in lowest currency units (e.g. cents) as a decimal string. For example, `"123.45"` in `"USD"` represents `$1.23`.

      - `context_window: "0-200k" or "200k-1M"`

        Input context window used. Null if not grouping by description or for non-token costs.

        - `"0-200k"`

        - `"200k-1M"`

      - `cost_type: "tokens" or "web_search" or "code_execution"`

        Type of cost. Null if not grouping by description.

        - `"tokens"`

        - `"web_search"`

        - `"code_execution"`

      - `currency: string`

        Currency code for the cost amount. Currently always `"USD"`.

      - `description: string`

        Description of the cost item. Null if not grouping by description.

      - `model: string`

        Model name used. Null if not grouping by description or for non-token costs.

      - `service_tier: "standard" or "batch"`

        Service tier used. Null if not grouping by description or for non-token costs.

        - `"standard"`

        - `"batch"`

      - `token_type: "uncached_input_tokens" or "output_tokens" or "cache_read_input_tokens" or 2 more`

        Type of token. Null if not grouping by description or for non-token costs.

        - `"uncached_input_tokens"`

        - `"output_tokens"`

        - `"cache_read_input_tokens"`

        - `"cache_creation.ephemeral_1h_input_tokens"`

        - `"cache_creation.ephemeral_5m_input_tokens"`

      - `workspace_id: string`

        ID of the Workspace this cost is associated with. Null if not grouping by workspace or for the default workspace.

    - `starting_at: string`

      Start of the time bucket (inclusive) in RFC 3339 format.

  - `has_more: boolean`

    Indicates if there are more results.

  - `next_page: string`

    Token to provide in as `page` in the subsequent request to retrieve the next page of data.

### Example

```http
curl https://api.anthropic.com/v1/organizations/cost_report \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```
