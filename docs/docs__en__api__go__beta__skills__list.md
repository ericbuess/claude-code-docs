## List

`client.Beta.Skills.List(ctx, params) (*PageCursor[BetaSkillListResponse], error)`

**get** `/v1/skills`

List Skills

### Parameters

- `params BetaSkillListParams`

  - `Limit param.Field[int64]`

    Query param: Number of results to return per page.

    Maximum value is 100. Defaults to 20.

  - `Page param.Field[string]`

    Query param: Pagination token for fetching a specific page of results.

    Pass the value from a previous response's `next_page` field to get the next page of results.

  - `Source param.Field[string]`

    Query param: Filter skills by source.

    If provided, only skills from the specified source will be returned:

    * `"custom"`: only return user-created skills
    * `"anthropic"`: only return Anthropic-created skills

  - `Betas param.Field[[]AnthropicBeta]`

    Header param: Optional header to specify the beta version(s) you want to use.

    - `string`

    - `type AnthropicBeta string`

      - `const AnthropicBetaMessageBatches2024_09_24 AnthropicBeta = "message-batches-2024-09-24"`

      - `const AnthropicBetaPromptCaching2024_07_31 AnthropicBeta = "prompt-caching-2024-07-31"`

      - `const AnthropicBetaComputerUse2024_10_22 AnthropicBeta = "computer-use-2024-10-22"`

      - `const AnthropicBetaComputerUse2025_01_24 AnthropicBeta = "computer-use-2025-01-24"`

      - `const AnthropicBetaPDFs2024_09_25 AnthropicBeta = "pdfs-2024-09-25"`

      - `const AnthropicBetaTokenCounting2024_11_01 AnthropicBeta = "token-counting-2024-11-01"`

      - `const AnthropicBetaTokenEfficientTools2025_02_19 AnthropicBeta = "token-efficient-tools-2025-02-19"`

      - `const AnthropicBetaOutput128k2025_02_19 AnthropicBeta = "output-128k-2025-02-19"`

      - `const AnthropicBetaFilesAPI2025_04_14 AnthropicBeta = "files-api-2025-04-14"`

      - `const AnthropicBetaMCPClient2025_04_04 AnthropicBeta = "mcp-client-2025-04-04"`

      - `const AnthropicBetaMCPClient2025_11_20 AnthropicBeta = "mcp-client-2025-11-20"`

      - `const AnthropicBetaDevFullThinking2025_05_14 AnthropicBeta = "dev-full-thinking-2025-05-14"`

      - `const AnthropicBetaInterleavedThinking2025_05_14 AnthropicBeta = "interleaved-thinking-2025-05-14"`

      - `const AnthropicBetaCodeExecution2025_05_22 AnthropicBeta = "code-execution-2025-05-22"`

      - `const AnthropicBetaExtendedCacheTTL2025_04_11 AnthropicBeta = "extended-cache-ttl-2025-04-11"`

      - `const AnthropicBetaContext1m2025_08_07 AnthropicBeta = "context-1m-2025-08-07"`

      - `const AnthropicBetaContextManagement2025_06_27 AnthropicBeta = "context-management-2025-06-27"`

      - `const AnthropicBetaModelContextWindowExceeded2025_08_26 AnthropicBeta = "model-context-window-exceeded-2025-08-26"`

      - `const AnthropicBetaSkills2025_10_02 AnthropicBeta = "skills-2025-10-02"`

### Returns

- `type BetaSkillListResponse struct{…}`

  - `ID string`

    Unique identifier for the skill.

    The format and length of IDs may change over time.

  - `CreatedAt string`

    ISO 8601 timestamp of when the skill was created.

  - `DisplayTitle string`

    Display title for the skill.

    This is a human-readable label that is not included in the prompt sent to the model.

  - `LatestVersion string`

    The latest version identifier for the skill.

    This represents the most recent version of the skill that has been created.

  - `Source string`

    Source of the skill.

    This may be one of the following values:

    * `"custom"`: the skill was created by a user
    * `"anthropic"`: the skill was created by Anthropic

  - `Type string`

    Object type.

    For Skills, this is always `"skill"`.

  - `UpdatedAt string`

    ISO 8601 timestamp of when the skill was last updated.

### Example

```go
package main

import (
  "context"
  "fmt"

  "github.com/anthropics/anthropic-sdk-go"
  "github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
  client := anthropic.NewClient(
    option.WithAPIKey("my-anthropic-api-key"),
  )
  page, err := client.Beta.Skills.List(context.TODO(), anthropic.BetaSkillListParams{

  })
  if err != nil {
    panic(err.Error())
  }
  fmt.Printf("%+v\n", page)
}
```
