# 有效管理成本

> 了解如何在使用 Claude Code 时跟踪和优化令牌使用量和成本。

Claude Code 每次交互都会消耗令牌。平均成本为每个开发者每天 $6，90% 的用户每日成本保持在 $12 以下。

对于团队使用，Claude Code 按 API 令牌消耗量收费。平均而言，使用 Sonnet 4 的 Claude Code 每个开发者每月成本约为 \$100-200，但根据用户运行的实例数量以及是否在自动化中使用，会有很大差异。

## 跟踪您的成本

* 使用 `/cost` 查看当前会话使用量
* **Anthropic Console 用户**：
  * 在 Anthropic Console 中查看[历史使用量](https://support.anthropic.com/en/articles/9534590-cost-and-usage-reporting-in-console)（需要管理员或计费角色）
  * 为 Claude Code 工作区设置[工作区支出限制](https://support.anthropic.com/en/articles/9796807-creating-and-managing-workspaces)（需要管理员角色）
* **Pro 和 Max 计划用户**：使用量包含在您的订阅中

## 为团队管理成本

使用 Anthropic API 时，您可以限制 Claude Code 工作区的总支出。要配置，请[按照这些说明操作](https://support.anthropic.com/en/articles/9796807-creating-and-managing-workspaces)。管理员可以通过[按照这些说明操作](https://support.anthropic.com/en/articles/9534590-cost-and-usage-reporting-in-console)查看成本和使用量报告。

在 Bedrock 和 Vertex 上，Claude Code 不会从您的云端发送指标。为了获取成本指标，几家大型企业报告使用了 [LiteLLM](/zh-CN/docs/claude-code/bedrock-vertex-proxies#litellm)，这是一个开源工具，帮助公司[按密钥跟踪支出](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend)。该项目与 Anthropic 无关，我们也未审核其安全性。

### 速率限制建议

为团队设置 Claude Code 时，请根据您的组织规模考虑以下每用户每分钟令牌数（TPM）建议：

| 团队规模       | 每用户 TPM   |
| ---------- | --------- |
| 1-5 用户     | 200k-300k |
| 5-20 用户    | 100k-150k |
| 20-50 用户   | 50k-75k   |
| 50-100 用户  | 25k-35k   |
| 100-500 用户 | 15k-20k   |
| 500+ 用户    | 10k-15k   |

例如，如果您有 200 个用户，您可能会为每个用户请求 20k TPM，或总共 400 万 TPM（200\*20,000 = 400 万）。

随着团队规模的增长，每用户 TPM 会减少，因为我们预期在大型组织中同时使用 Claude Code 的用户会更少。这些速率限制适用于组织级别，而不是每个单独用户，这意味着当其他人没有积极使用服务时，单个用户可以暂时消耗超过其计算份额的资源。

<Note>
  如果您预期会出现异常高的并发使用场景（例如大型团体的现场培训会话），您可能需要为每个用户分配更高的 TPM。
</Note>

## 减少令牌使用量

* **紧凑对话：**

  * Claude 默认在上下文超过 95% 容量时使用自动紧凑
  * 切换自动紧凑：运行 `/config` 并导航到"Auto-compact enabled"
  * 当上下文变大时手动使用 `/compact`
  * 添加自定义指令：`/compact Focus on code samples and API usage`
  * 通过添加到 CLAUDE.md 来自定义紧凑：

    ```markdown
    # Summary instructions

    When you are using compact, please focus on test output and code changes
    ```

* **编写具体查询：** 避免触发不必要扫描的模糊请求

* **分解复杂任务：** 将大型任务拆分为专注的交互

* **在任务之间清除历史记录：** 使用 `/clear` 重置上下文

成本可能因以下因素而显著变化：

* 被分析代码库的大小
* 查询的复杂性
* 被搜索或修改的文件数量
* 对话历史的长度
* 紧凑对话的频率
* 后台进程（俳句生成、对话摘要）

## 后台令牌使用量

Claude Code 即使在空闲时也会为某些后台功能使用令牌：

* **俳句生成**：您输入时出现的小型创意消息（大约每天 1 分钱）
* **对话摘要**：为 `claude --resume` 功能摘要之前对话的后台作业
* **命令处理**：一些命令如 `/cost` 可能会生成请求来检查状态

这些后台进程即使没有主动交互也会消耗少量令牌（通常每个会话少于 \$0.04）。

<Note>
  对于团队部署，我们建议从小型试点组开始建立使用模式，然后再进行更广泛的推广。
</Note>
