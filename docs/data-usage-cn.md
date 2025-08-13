# 数据使用

> 了解 Anthropic 对 Claude 的数据使用政策

## 数据政策

### 数据训练政策

默认情况下，Anthropic 不会使用发送到 Claude Code 的代码或提示来训练生成模型。

我们致力于完全透明地说明我们如何使用您的数据。我们可能会使用反馈来改进我们的产品和服务，但我们不会使用您在 Claude Code 中的反馈来训练生成模型。

### 开发合作伙伴计划

如果您明确选择加入向我们提供训练材料的方法，例如通过[开发合作伙伴计划](https://support.anthropic.com/en/articles/11174108-about-the-development-partner-program)，我们可能会使用这些提供的材料来训练我们的模型。组织管理员可以明确为其组织选择加入开发合作伙伴计划。请注意，此计划仅适用于 Anthropic 第一方 API，不适用于 Bedrock 或 Vertex 用户。

### 反馈记录

如果您选择向我们发送关于 Claude Code 的反馈，例如您的使用记录，Anthropic 可能会使用该反馈来调试相关问题并改进 Claude Code 的功能（例如，降低未来发生类似错误的风险）。我们不会使用此反馈来训练生成模型。鉴于其潜在的敏感性，我们仅将用户反馈记录存储 30 天。

### 数据保留

您可以使用来自零数据保留组织的 API 密钥。这样做时，Claude Code 不会在我们的服务器上保留您的聊天记录。用户的本地 Claude Code 客户端可能会在本地存储会话长达 30 天，以便用户可以恢复它们。此行为是可配置的。

### Privacy safeguards

We have implemented several safeguards to protect your data, including:

* Limited retention periods for sensitive information
* Restricted access to user session data
* Clear policies against using feedback for model training

For full details, please review our [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) and [Privacy Policy](https://www.anthropic.com/legal/privacy).

## 数据流和依赖关系

![Claude Code 数据流图](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/images/claude-code-data-flow.png)

Claude Code 从 [NPM](https://www.npmjs.com/package/@anthropic-ai/claude-code) 安装。Claude Code 在本地运行。为了与 LLM 交互，Claude Code 通过网络发送数据。此数据包括所有用户提示和模型输出。数据在传输过程中通过 TLS 加密，静态时不加密。Claude Code 与大多数流行的 VPN 和 LLM 代理兼容。

Claude Code 基于 Anthropic 的 API 构建。有关我们 API 安全控制的详细信息，包括我们的 API 日志记录程序，请参阅 [Anthropic 信任中心](https://trust.anthropic.com) 中提供的合规性文档。

## 遥测服务

Claude Code 从用户的机器连接到 Statsig 服务，以记录操作指标，如延迟、可靠性和使用模式。此日志记录不包括任何代码或文件路径。数据在传输过程中使用 TLS 加密，静态时使用 256 位 AES 加密。在 [Statsig 安全文档](https://www.statsig.com/trust/security) 中了解更多信息。要选择退出 Statsig 遥测，请设置 `DISABLE_TELEMETRY` 环境变量。

Claude Code 从用户的机器连接到 Sentry 进行操作错误日志记录。数据在传输过程中使用 TLS 加密，静态时使用 256 位 AES 加密。在 [Sentry 安全文档](https://sentry.io/security/) 中了解更多信息。要选择退出错误日志记录，请设置 `DISABLE_ERROR_REPORTING` 环境变量。

当用户运行 `/bug` 命令时，包括代码在内的完整对话历史记录副本会发送到 Anthropic。数据在传输和静态时都会加密。可选地，会在我们的公共存储库中创建 Github 问题。要选择退出错误报告，请设置 `DISABLE_BUG_COMMAND` 环境变量。

## 按 API 提供商的默认行为

默认情况下，当使用 Bedrock 或 Vertex 时，我们会禁用所有非必要流量（包括错误报告、遥测和错误报告功能）。您也可以通过设置 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 环境变量来一次性选择退出所有这些功能。以下是完整的默认行为：

| 服务                           | Anthropic API                              | Vertex API                                 | Bedrock API                                 |
| ---------------------------- | ------------------------------------------ | ------------------------------------------ | ------------------------------------------- |
| **Statsig（指标）**              | 默认开启。<br />`DISABLE_TELEMETRY=1` 禁用。       | 默认关闭。<br />`CLAUDE_CODE_USE_VERTEX` 必须为 1。 | 默认关闭。<br />`CLAUDE_CODE_USE_BEDROCK` 必须为 1。 |
| **Sentry（错误）**               | 默认开启。<br />`DISABLE_ERROR_REPORTING=1` 禁用。 | 默认关闭。<br />`CLAUDE_CODE_USE_VERTEX` 必须为 1。 | 默认关闭。<br />`CLAUDE_CODE_USE_BEDROCK` 必须为 1。 |
| **Anthropic API（`/bug` 报告）** | 默认开启。<br />`DISABLE_BUG_COMMAND=1` 禁用。     | 默认关闭。<br />`CLAUDE_CODE_USE_VERTEX` 必须为 1。 | 默认关闭。<br />`CLAUDE_CODE_USE_BEDROCK` 必须为 1。 |

所有环境变量都可以检入 `settings.json`（[了解更多](/zh-CN/docs/claude-code/settings)）。
