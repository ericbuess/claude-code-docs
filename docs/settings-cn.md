# Claude Code 设置

> 通过全局和项目级设置以及环境变量配置 Claude Code。

Claude Code 提供多种设置来配置其行为以满足您的需求。您可以在使用交互式 REPL 时运行 `/config` 命令来配置 Claude Code。

## 设置文件

`settings.json` 文件是我们通过分层设置配置 Claude Code 的官方机制：

* **用户设置**在 `~/.claude/settings.json` 中定义，适用于所有项目。
* **项目设置**保存在您的项目目录中：
  * `.claude/settings.json` 用于检入源代码控制并与团队共享的设置
  * `.claude/settings.local.json` 用于不检入的设置，对个人偏好和实验很有用。Claude Code 会在创建时配置 git 忽略 `.claude/settings.local.json`。
* 对于 Claude Code 的企业部署，我们还支持**企业管理策略设置**。这些设置优先于用户和项目设置。系统管理员可以将策略部署到：
  * macOS：`/Library/Application Support/ClaudeCode/managed-settings.json`
  * Linux 和 WSL：`/etc/claude-code/managed-settings.json`
  * Windows：`C:\ProgramData\ClaudeCode\managed-settings.json`

```JSON 示例 settings.json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl:*)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  }
}
```

### 可用设置

`settings.json` 支持多个选项：

| 键                            | 描述                                                                                                             | 示例                                                      |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------ |
| `apiKeyHelper`               | 自定义脚本，在 `/bin/sh` 中执行，用于生成认证值。此值将作为 `X-Api-Key` 和 `Authorization: Bearer` 标头发送给模型请求                            | `/bin/generate_temp_api_key.sh`                         |
| `cleanupPeriodDays`          | 本地保留聊天记录的时间长度（默认：30 天）                                                                                         | `20`                                                    |
| `env`                        | 将应用于每个会话的环境变量                                                                                                  | `{"FOO": "bar"}`                                        |
| `includeCoAuthoredBy`        | 是否在 git 提交和拉取请求中包含 `co-authored-by Claude` 署名（默认：`true`）                                                       | `false`                                                 |
| `permissions`                | 权限结构见下表。                                                                                                       |                                                         |
| `hooks`                      | 配置在工具执行前后运行的自定义命令。参见[钩子文档](hooks)                                                                              | `{"PreToolUse": {"Bash": "echo 'Running command...'"}}` |
| `model`                      | 覆盖 Claude Code 使用的默认模型                                                                                         | `"claude-3-5-sonnet-20241022"`                          |
| `forceLoginMethod`           | 使用 `claudeai` 限制登录到 Claude.ai 账户，`console` 限制登录到 Anthropic Console（API 使用计费）账户                                 | `claudeai`                                              |
| `enableAllProjectMcpServers` | 自动批准项目 `.mcp.json` 文件中定义的所有 MCP 服务器                                                                            | `true`                                                  |
| `enabledMcpjsonServers`      | 从 `.mcp.json` 文件中批准的特定 MCP 服务器列表                                                                               | `["memory", "github"]`                                  |
| `disabledMcpjsonServers`     | 从 `.mcp.json` 文件中拒绝的特定 MCP 服务器列表                                                                               | `["filesystem"]`                                        |
| `awsAuthRefresh`             | 修改 `.aws` 目录的自定义脚本（参见[高级凭据配置](/zh-CN/docs/claude-code/amazon-bedrock#advanced-credential-configuration)）       | `aws sso login --profile myprofile`                     |
| `awsCredentialExport`        | 输出包含 AWS 凭据的 JSON 的自定义脚本（参见[高级凭据配置](/zh-CN/docs/claude-code/amazon-bedrock#advanced-credential-configuration)） | `/bin/generate_aws_grant.sh`                            |

### 权限设置

| 键                              | 描述                                                                                              | 示例                               |
| :----------------------------- | :---------------------------------------------------------------------------------------------- | :------------------------------- |
| `allow`                        | 允许工具使用的[权限规则](/zh-CN/docs/claude-code/iam#configuring-permissions)数组                            | `[ "Bash(git diff:*)" ]`         |
| `deny`                         | 拒绝工具使用的[权限规则](/zh-CN/docs/claude-code/iam#configuring-permissions)数组                            | `[ "WebFetch", "Bash(curl:*)" ]` |
| `additionalDirectories`        | Claude 可以访问的其他[工作目录](iam#working-directories)                                                   | `[ "../docs/" ]`                 |
| `defaultMode`                  | 打开 Claude Code 时的默认[权限模式](iam#permission-modes)                                                 | `"acceptEdits"`                  |
| `disableBypassPermissionsMode` | 设置为 `"disable"` 以防止激活 `bypassPermissions` 模式。参见[管理策略设置](iam#enterprise-managed-policy-settings) | `"disable"`                      |

### 设置优先级

设置按优先级顺序应用（从高到低）：

1. **企业管理策略**（`managed-settings.json`）
   * 由 IT/DevOps 部署
   * 无法覆盖

2. **命令行参数**
   * 特定会话的临时覆盖

3. **本地项目设置**（`.claude/settings.local.json`）
   * 个人项目特定设置

4. **共享项目设置**（`.claude/settings.json`）
   * 源代码控制中的团队共享项目设置

5. **用户设置**（`~/.claude/settings.json`）
   * 个人全局设置

此层次结构确保始终执行企业安全策略，同时仍允许团队和个人自定义其体验。

### 配置系统的要点

* **内存文件（CLAUDE.md）**：包含 Claude 在启动时加载的指令和上下文
* **设置文件（JSON）**：配置权限、环境变量和工具行为
* **斜杠命令**：可以在会话期间使用 `/command-name` 调用的自定义命令
* **MCP 服务器**：使用其他工具和集成扩展 Claude Code
* **优先级**：更高级别的配置（企业）覆盖较低级别的配置（用户/项目）
* **继承**：设置被合并，更具体的设置添加到或覆盖更广泛的设置

## 子代理配置

Claude Code 支持可在用户和项目级别配置的自定义 AI 子代理。这些子代理存储为带有 YAML 前言的 Markdown 文件：

* **用户子代理**：`~/.claude/agents/` - 在您的所有项目中可用
* **项目子代理**：`.claude/agents/` - 特定于您的项目，可以与您的团队共享

子代理文件定义具有自定义提示和工具权限的专门 AI 助手。在[子代理文档](/zh-CN/docs/claude-code/sub-agents)中了解更多关于创建和使用子代理的信息。

## 环境变量

Claude Code 支持以下环境变量来控制其行为：

<Note>
  所有环境变量也可以在[`settings.json`](#available-settings)中配置。这是为每个会话自动设置环境变量或为整个团队或组织推出一组环境变量的有用方法。
</Note>

| 变量                                         | 目的                                                                                                                                                |
| :----------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ANTHROPIC_API_KEY`                        | 作为 `X-Api-Key` 标头发送的 API 密钥，通常用于 Claude SDK（对于交互式使用，运行 `/login`）                                                                                  |
| `ANTHROPIC_AUTH_TOKEN`                     | `Authorization` 标头的自定义值（您在此处设置的值将以 `Bearer ` 为前缀）                                                                                                 |
| `ANTHROPIC_CUSTOM_HEADERS`                 | 您想要添加到请求的自定义标头（以 `Name: Value` 格式）                                                                                                                |
| `ANTHROPIC_MODEL`                          | 要使用的自定义模型名称（参见[模型配置](/zh-CN/docs/claude-code/bedrock-vertex-proxies#model-configuration)）                                                         |
| `ANTHROPIC_SMALL_FAST_MODEL`               | [后台任务的 Haiku 类模型](/zh-CN/docs/claude-code/costs)名称                                                                                                |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION`    | 使用 Bedrock 时小型/快速模型的覆盖 AWS 区域                                                                                                                     |
| `AWS_BEARER_TOKEN_BEDROCK`                 | 用于身份验证的 Bedrock API 密钥（参见[Bedrock API 密钥](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/)） |
| `BASH_DEFAULT_TIMEOUT_MS`                  | 长时间运行的 bash 命令的默认超时                                                                                                                               |
| `BASH_MAX_TIMEOUT_MS`                      | 模型可以为长时间运行的 bash 命令设置的最大超时                                                                                                                        |
| `BASH_MAX_OUTPUT_LENGTH`                   | bash 输出在中间截断之前的最大字符数                                                                                                                              |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | 每个 Bash 命令后返回到原始工作目录                                                                                                                              |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`        | 应刷新凭据的间隔（毫秒）（使用 `apiKeyHelper` 时）                                                                                                                 |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`        | 跳过 IDE 扩展的自动安装                                                                                                                                    |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`            | 为大多数请求设置最大输出令牌数                                                                                                                                   |
| `CLAUDE_CODE_USE_BEDROCK`                  | 使用[Bedrock](/zh-CN/docs/claude-code/amazon-bedrock)                                                                                               |
| `CLAUDE_CODE_USE_VERTEX`                   | 使用[Vertex](/zh-CN/docs/claude-code/google-vertex-ai)                                                                                              |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH`            | 跳过 Bedrock 的 AWS 身份验证（例如使用 LLM 网关时）                                                                                                               |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH`             | 跳过 Vertex 的 Google 身份验证（例如使用 LLM 网关时）                                                                                                             |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | 等同于设置 `DISABLE_AUTOUPDATER`、`DISABLE_BUG_COMMAND`、`DISABLE_ERROR_REPORTING` 和 `DISABLE_TELEMETRY`                                                 |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`       | 设置为 `1` 以禁用基于对话上下文的自动终端标题更新                                                                                                                       |
| `DISABLE_AUTOUPDATER`                      | 设置为 `1` 以禁用自动更新。这优先于 `autoUpdates` 配置设置。                                                                                                          |
| `DISABLE_BUG_COMMAND`                      | 设置为 `1` 以禁用 `/bug` 命令                                                                                                                             |
| `DISABLE_COST_WARNINGS`                    | 设置为 `1` 以禁用成本警告消息                                                                                                                                 |
| `DISABLE_ERROR_REPORTING`                  | 设置为 `1` 以选择退出 Sentry 错误报告                                                                                                                         |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS`        | 设置为 `1` 以禁用非关键路径（如风味文本）的模型调用                                                                                                                      |
| `DISABLE_TELEMETRY`                        | 设置为 `1` 以选择退出 Statsig 遥测（注意 Statsig 事件不包括用户数据，如代码、文件路径或 bash 命令）                                                                                  |
| `HTTP_PROXY`                               | 为网络连接指定 HTTP 代理服务器                                                                                                                                |
| `HTTPS_PROXY`                              | 为网络连接指定 HTTPS 代理服务器                                                                                                                               |
| `MAX_THINKING_TOKENS`                      | 强制模型思考预算                                                                                                                                          |
| `MCP_TIMEOUT`                              | MCP 服务器启动的超时时间（毫秒）                                                                                                                                |
| `MCP_TOOL_TIMEOUT`                         | MCP 工具执行的超时时间（毫秒）                                                                                                                                 |
| `MAX_MCP_OUTPUT_TOKENS`                    | MCP 工具响应中允许的最大令牌数（默认：25000）                                                                                                                       |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU`           | 使用 Vertex AI 时 Claude 3.5 Haiku 的覆盖区域                                                                                                             |
| `VERTEX_REGION_CLAUDE_3_5_SONNET`          | 使用 Vertex AI 时 Claude 3.5 Sonnet 的覆盖区域                                                                                                            |
| `VERTEX_REGION_CLAUDE_3_7_SONNET`          | 使用 Vertex AI 时 Claude 3.7 Sonnet 的覆盖区域                                                                                                            |
| `VERTEX_REGION_CLAUDE_4_0_OPUS`            | 使用 Vertex AI 时 Claude 4.0 Opus 的覆盖区域                                                                                                              |
| `VERTEX_REGION_CLAUDE_4_0_SONNET`          | 使用 Vertex AI 时 Claude 4.0 Sonnet 的覆盖区域                                                                                                            |
| `VERTEX_REGION_CLAUDE_4_1_OPUS`            | 使用 Vertex AI 时 Claude 4.1 Opus 的覆盖区域                                                                                                              |

## 配置选项

要管理您的配置，请使用以下命令：

* 列出设置：`claude config list`
* 查看设置：`claude config get <key>`
* 更改设置：`claude config set <key> <value>`
* 推送到设置（对于列表）：`claude config add <key> <value>`
* 从设置中删除（对于列表）：`claude config remove <key> <value>`

默认情况下，`config` 更改您的项目配置。要管理您的全局配置，请使用 `--global`（或 `-g`）标志。

### 全局配置

要设置全局配置，请使用 `claude config set -g <key> <value>`：

| 键                       | 描述                                                                      | 示例                                                                     |
| :---------------------- | :---------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `autoUpdates`           | 是否启用自动更新（默认：`true`）。启用时，Claude Code 会在后台自动下载和安装更新。重启 Claude Code 时应用更新。 | `false`                                                                |
| `preferredNotifChannel` | 您希望接收通知的位置（默认：`iterm2`）                                                 | `iterm2`、`iterm2_with_bell`、`terminal_bell` 或 `notifications_disabled` |
| `theme`                 | 颜色主题                                                                    | `dark`、`light`、`light-daltonized` 或 `dark-daltonized`                  |
| `verbose`               | 是否显示完整的 bash 和命令输出（默认：`false`）                                          | `true`                                                                 |

## Claude 可用的工具

Claude Code 可以访问一组强大的工具，帮助它理解和修改您的代码库：

| 工具               | 描述                        | 需要权限 |
| :--------------- | :------------------------ | :--- |
| **Bash**         | 在您的环境中执行 shell 命令         | 是    |
| **Edit**         | 对特定文件进行有针对性的编辑            | 是    |
| **Glob**         | 基于模式匹配查找文件                | 否    |
| **Grep**         | 在文件内容中搜索模式                | 否    |
| **LS**           | 列出文件和目录                   | 否    |
| **MultiEdit**    | 对单个文件原子性地执行多个编辑           | 是    |
| **NotebookEdit** | 修改 Jupyter notebook 单元格   | 是    |
| **NotebookRead** | 读取和显示 Jupyter notebook 内容 | 否    |
| **Read**         | 读取文件内容                    | 否    |
| **Task**         | 运行子代理来处理复杂的多步骤任务          | 否    |
| **TodoWrite**    | 创建和管理结构化任务列表              | 否    |
| **WebFetch**     | 从指定 URL 获取内容              | 是    |
| **WebSearch**    | 执行带有域过滤的网络搜索              | 是    |
| **Write**        | 创建或覆盖文件                   | 是    |

权限规则可以使用 `/allowed-tools` 或在[权限设置](/zh-CN/docs/claude-code/settings#available-settings)中配置。

### 使用钩子扩展工具

您可以使用[Claude Code 钩子](/zh-CN/docs/claude-code/hooks-guide)在任何工具执行前后运行自定义命令。

例如，您可以在 Claude 修改 Python 文件后自动运行 Python 格式化程序，或通过阻止对某些路径的写入操作来防止修改生产配置文件。

## 另请参阅

* [身份和访问管理](/zh-CN/docs/claude-code/iam#configuring-permissions) - 了解 Claude Code 的权限系统
* [IAM 和访问控制](/zh-CN/docs/claude-code/iam#enterprise-managed-policy-settings) - 企业策略管理
* [故障排除](/zh-CN/docs/claude-code/troubleshooting#auto-updater-issues) - 常见配置问题的解决方案
