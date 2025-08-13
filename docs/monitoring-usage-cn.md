# 监控

> 了解如何为 Claude Code 启用和配置 OpenTelemetry。

Claude Code 支持 OpenTelemetry (OTel) 指标和事件，用于监控和可观测性。

所有指标都是通过 OpenTelemetry 标准指标协议导出的时间序列数据，事件通过 OpenTelemetry 的日志/事件协议导出。用户有责任确保其指标和日志后端配置正确，并且聚合粒度满足其监控要求。

<Note>
  OpenTelemetry 支持目前处于测试阶段，详细信息可能会发生变化。
</Note>

## 快速开始

使用环境变量配置 OpenTelemetry：

```bash
# 1. 启用遥测
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. 选择导出器（两者都是可选的 - 只配置您需要的）
export OTEL_METRICS_EXPORTER=otlp       # 选项：otlp、prometheus、console
export OTEL_LOGS_EXPORTER=otlp          # 选项：otlp、console

# 3. 配置 OTLP 端点（用于 OTLP 导出器）
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. 设置身份验证（如果需要）
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. 用于调试：减少导出间隔
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 秒（默认：60000ms）
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 秒（默认：5000ms）

# 6. 运行 Claude Code
claude
```

<Note>
  默认导出间隔为指标 60 秒，日志 5 秒。在设置期间，您可能希望使用较短的间隔进行调试。请记住在生产使用时重置这些设置。
</Note>

有关完整配置选项，请参阅 [OpenTelemetry 规范](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options)。

## 管理员配置

管理员可以通过托管设置文件为所有用户配置 OpenTelemetry 设置。这允许在整个组织中集中控制遥测设置。有关设置如何应用的更多信息，请参阅[设置优先级](/zh-CN/docs/claude-code/settings#settings-precedence)。

托管设置文件位于：

* macOS：`/Library/Application Support/ClaudeCode/managed-settings.json`
* Linux 和 WSL：`/etc/claude-code/managed-settings.json`
* Windows：`C:\ProgramData\ClaudeCode\managed-settings.json`

托管设置配置示例：

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.company.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer company-token"
  }
}
```

<Note>
  托管设置可以通过 MDM（移动设备管理）或其他设备管理解决方案分发。在托管设置文件中定义的环境变量具有高优先级，用户无法覆盖。
</Note>

## 配置详细信息

### 常用配置变量

| 环境变量                                            | 描述                  | 示例值                                |
| ----------------------------------------------- | ------------------- | ---------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                  | 启用遥测收集（必需）          | `1`                                |
| `OTEL_METRICS_EXPORTER`                         | 指标导出器类型（逗号分隔）       | `console`、`otlp`、`prometheus`      |
| `OTEL_LOGS_EXPORTER`                            | 日志/事件导出器类型（逗号分隔）    | `console`、`otlp`                   |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                   | OTLP 导出器协议（所有信号）    | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                   | OTLP 收集器端点（所有信号）    | `http://localhost:4317`            |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`           | 指标协议（覆盖通用设置）        | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`           | OTLP 指标端点（覆盖通用设置）   | `http://localhost:4318/v1/metrics` |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`              | 日志协议（覆盖通用设置）        | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`              | OTLP 日志端点（覆盖通用设置）   | `http://localhost:4318/v1/logs`    |
| `OTEL_EXPORTER_OTLP_HEADERS`                    | OTLP 身份验证标头         | `Authorization=Bearer token`       |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`         | mTLS 身份验证的客户端密钥     | 客户端密钥文件路径                          |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE` | mTLS 身份验证的客户端证书     | 客户端证书文件路径                          |
| `OTEL_METRIC_EXPORT_INTERVAL`                   | 导出间隔（毫秒）（默认：60000）  | `5000`、`60000`                     |
| `OTEL_LOGS_EXPORT_INTERVAL`                     | 日志导出间隔（毫秒）（默认：5000） | `1000`、`10000`                     |
| `OTEL_LOG_USER_PROMPTS`                         | 启用用户提示内容日志记录（默认：禁用） | `1` 启用                             |

### 指标基数控制

以下环境变量控制指标中包含哪些属性以管理基数：

| 环境变量                                | 描述                           | 默认值     | 禁用示例    |
| ----------------------------------- | ---------------------------- | ------- | ------- |
| `OTEL_METRICS_INCLUDE_SESSION_ID`   | 在指标中包含 session.id 属性         | `true`  | `false` |
| `OTEL_METRICS_INCLUDE_VERSION`      | 在指标中包含 app.version 属性        | `false` | `true`  |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | 在指标中包含 user.account\_uuid 属性 | `true`  | `false` |

这些变量有助于控制指标的基数，这会影响指标后端的存储要求和查询性能。较低的基数通常意味着更好的性能和更低的存储成本，但分析数据的粒度较低。

### 动态标头

对于需要动态身份验证的企业环境，您可以配置脚本来动态生成标头：

#### 设置配置

添加到您的 `.claude/settings.json`：

```json
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### 脚本要求

脚本必须输出有效的 JSON，其中包含表示 HTTP 标头的字符串键值对：

```bash
#!/bin/bash
# 示例：多个标头
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### 重要限制

**标头仅在启动时获取，而不是在运行时获取。** 这是由于 OpenTelemetry 导出器架构限制。

对于需要频繁令牌刷新的场景，请使用 OpenTelemetry Collector 作为代理，它可以刷新自己的标头。

### 多团队组织支持

拥有多个团队或部门的组织可以使用 `OTEL_RESOURCE_ATTRIBUTES` 环境变量添加自定义属性来区分不同的组：

```bash
# 添加用于团队识别的自定义属性
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

这些自定义属性将包含在所有指标和事件中，允许您：

* 按团队或部门过滤指标
* 按成本中心跟踪成本
* 创建特定于团队的仪表板
* 为特定团队设置警报

<Warning>
  **OTEL\_RESOURCE\_ATTRIBUTES 的重要格式要求：**

  `OTEL_RESOURCE_ATTRIBUTES` 环境变量遵循 [W3C Baggage 规范](https://www.w3.org/TR/baggage/)，该规范有严格的格式要求：

  * **不允许空格**：值不能包含空格。例如，`user.organizationName=My Company` 是无效的
  * **格式**：必须是逗号分隔的 key=value 对：`key1=value1,key2=value2`
  * **允许的字符**：仅限 US-ASCII 字符，不包括控制字符、空白字符、双引号、逗号、分号和反斜杠
  * **特殊字符**：超出允许范围的字符必须进行百分号编码

  **示例：**

  ```bash
  # ❌ 无效 - 包含空格
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John's Organization"

  # ✅ 有效 - 使用下划线或驼峰命名法
  export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
  export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"

  # ✅ 有效 - 如需要，对特殊字符进行百分号编码
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
  ```

  注意：引用整个 key=value 对（例如，`"key=value with spaces"`）不受 OpenTelemetry 规范支持，会导致属性以引号为前缀。
</Warning>

### 配置示例

```bash
# 控制台调试（1 秒间隔）
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus

# 多个导出器
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json

# 指标和日志使用不同的端点/后端
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.company.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.company.com:4317

# 仅指标（无事件/日志）
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 仅事件/日志（无指标）
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## 可用指标和事件

### 标准属性

所有指标和事件共享这些标准属性：

| 属性                  | 描述                                            | 控制变量                                         |
| ------------------- | --------------------------------------------- | -------------------------------------------- |
| `session.id`        | 唯一会话标识符                                       | `OTEL_METRICS_INCLUDE_SESSION_ID`（默认：true）   |
| `app.version`       | 当前 Claude Code 版本                             | `OTEL_METRICS_INCLUDE_VERSION`（默认：false）     |
| `organization.id`   | 组织 UUID（已认证时）                                 | 可用时始终包含                                      |
| `user.account_uuid` | 账户 UUID（已认证时）                                 | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID`（默认：true） |
| `terminal.type`     | 终端类型（例如，`iTerm.app`、`vscode`、`cursor`、`tmux`） | 检测到时始终包含                                     |

### 指标

Claude Code 导出以下指标：

| 指标名称                                  | 描述                | 单位     |
| ------------------------------------- | ----------------- | ------ |
| `claude_code.session.count`           | 启动的 CLI 会话计数      | count  |
| `claude_code.lines_of_code.count`     | 修改的代码行数计数         | count  |
| `claude_code.pull_request.count`      | 创建的拉取请求数量         | count  |
| `claude_code.commit.count`            | 创建的 git 提交数量      | count  |
| `claude_code.cost.usage`              | Claude Code 会话的成本 | USD    |
| `claude_code.token.usage`             | 使用的令牌数量           | tokens |
| `claude_code.code_edit_tool.decision` | 代码编辑工具权限决策计数      | count  |
| `claude_code.active_time.total`       | 总活跃时间（秒）          | s      |

### 指标详细信息

#### 会话计数器

在每个会话开始时递增。

**属性**：

* 所有[标准属性](#标准属性)

#### 代码行计数器

在添加或删除代码时递增。

**属性**：

* 所有[标准属性](#标准属性)
* `type`：（`"added"`、`"removed"`）

#### 拉取请求计数器

通过 Claude Code 创建拉取请求时递增。

**属性**：

* 所有[标准属性](#标准属性)

#### 提交计数器

通过 Claude Code 创建 git 提交时递增。

**属性**：

* 所有[标准属性](#标准属性)

#### 成本计数器

每次 API 请求后递增。

**属性**：

* 所有[标准属性](#标准属性)
* `model`：模型标识符（例如，"claude-3-5-sonnet-20241022"）

#### 令牌计数器

每次 API 请求后递增。

**属性**：

* 所有[标准属性](#标准属性)
* `type`：（`"input"`、`"output"`、`"cacheRead"`、`"cacheCreation"`）
* `model`：模型标识符（例如，"claude-3-5-sonnet-20241022"）

#### 代码编辑工具决策计数器

当用户接受或拒绝 Edit、MultiEdit、Write 或 NotebookEdit 工具使用时递增。

**属性**：

* 所有[标准属性](#标准属性)
* `tool`：工具名称（`"Edit"`、`"MultiEdit"`、`"Write"`、`"NotebookEdit"`）
* `decision`：用户决策（`"accept"`、`"reject"`）
* `language`：编辑文件的编程语言（例如，`"TypeScript"`、`"Python"`、`"JavaScript"`、`"Markdown"`）。对于无法识别的文件扩展名返回 `"unknown"`。

#### 活跃时间计数器

跟踪实际花费在积极使用 Claude Code 上的时间（不是空闲时间）。此指标在用户交互期间递增，例如输入提示或接收响应。

**属性**：

* 所有[标准属性](#标准属性)

### 事件

Claude Code 通过 OpenTelemetry 日志/事件导出以下事件（当配置了 `OTEL_LOGS_EXPORTER` 时）：

#### 用户提示事件

当用户提交提示时记录。

**事件名称**：`claude_code.user_prompt`

**属性**：

* 所有[标准属性](#标准属性)
* `event.name`：`"user_prompt"`
* `event.timestamp`：ISO 8601 时间戳
* `prompt_length`：提示长度
* `prompt`：提示内容（默认编辑，使用 `OTEL_LOG_USER_PROMPTS=1` 启用）

#### 工具结果事件

当工具完成执行时记录。

**事件名称**：`claude_code.tool_result`

**属性**：

* 所有[标准属性](#标准属性)
* `event.name`：`"tool_result"`
* `event.timestamp`：ISO 8601 时间戳
* `tool_name`：工具名称
* `success`：`"true"` 或 `"false"`
* `duration_ms`：执行时间（毫秒）
* `error`：错误消息（如果失败）
* `decision`：`"accept"` 或 `"reject"`
* `source`：决策来源 - `"config"`、`"user_permanent"`、`"user_temporary"`、`"user_abort"` 或 `"user_reject"`
* `tool_parameters`：包含工具特定参数的 JSON 字符串（可用时）
  * 对于 Bash 工具：包括 `bash_command`、`full_command`、`timeout`、`description`、`sandbox`

#### API 请求事件

为每个对 Claude 的 API 请求记录。

**事件名称**：`claude_code.api_request`

**属性**：

* 所有[标准属性](#标准属性)
* `event.name`：`"api_request"`
* `event.timestamp`：ISO 8601 时间戳
* `model`：使用的模型（例如，"claude-3-5-sonnet-20241022"）
* `cost_usd`：估计成本（美元）
* `duration_ms`：请求持续时间（毫秒）
* `input_tokens`：输入令牌数量
* `output_tokens`：输出令牌数量
* `cache_read_tokens`：从缓存读取的令牌数量
* `cache_creation_tokens`：用于缓存创建的令牌数量

#### API 错误事件

当对 Claude 的 API 请求失败时记录。

**事件名称**：`claude_code.api_error`

**属性**：

* 所有[标准属性](#标准属性)
* `event.name`：`"api_error"`
* `event.timestamp`：ISO 8601 时间戳
* `model`：使用的模型（例如，"claude-3-5-sonnet-20241022"）
* `error`：错误消息
* `status_code`：HTTP 状态码（如果适用）
* `duration_ms`：请求持续时间（毫秒）
* `attempt`：尝试次数（对于重试的请求）

#### 工具决策事件

当做出工具权限决策（接受/拒绝）时记录。

**事件名称**：`claude_code.tool_decision`

**属性**：

* 所有[标准属性](#标准属性)
* `event.name`：`"tool_decision"`
* `event.timestamp`：ISO 8601 时间戳
* `tool_name`：工具名称（例如，"Read"、"Edit"、"MultiEdit"、"Write"、"NotebookEdit" 等）
* `decision`：`"accept"` 或 `"reject"`
* `source`：决策来源 - `"config"`、`"user_permanent"`、`"user_temporary"`、`"user_abort"` 或 `"user_reject"`

## 解释指标和事件数据

Claude Code 导出的指标为使用模式和生产力提供了有价值的见解。以下是您可以创建的一些常见可视化和分析：

### 使用监控

| 指标                                                            | 分析机会                       |
| ------------------------------------------------------------- | -------------------------- |
| `claude_code.token.usage`                                     | 按 `type`（输入/输出）、用户、团队或模型分解 |
| `claude_code.session.count`                                   | 跟踪随时间的采用和参与度               |
| `claude_code.lines_of_code.count`                             | 通过跟踪代码添加/删除来衡量生产力          |
| `claude_code.commit.count` 和 `claude_code.pull_request.count` | 了解对开发工作流程的影响               |

### 成本监控

`claude_code.cost.usage` 指标有助于：

* 跟踪团队或个人的使用趋势
* 识别高使用量会话以进行优化

<Note>
  成本指标是近似值。有关官方计费数据，请参考您的 API 提供商（Anthropic Console、AWS Bedrock 或 Google Cloud Vertex）。
</Note>

### 警报和分段

要考虑的常见警报：

* 成本激增
* 异常令牌消耗
* 特定用户的高会话量

所有指标都可以按 `user.account_uuid`、`organization.id`、`session.id`、`model` 和 `app.version` 进行分段。

### 事件分析

事件数据为 Claude Code 交互提供了详细的见解：

**工具使用模式**：分析工具结果事件以识别：

* 最常用的工具
* 工具成功率
* 平均工具执行时间
* 按工具类型的错误模式

**性能监控**：跟踪 API 请求持续时间和工具执行时间以识别性能瓶颈。

## 后端考虑

您选择的指标和日志后端将决定您可以执行的分析类型：

### 对于指标：

* **时间序列数据库（例如，Prometheus）**：速率计算、聚合指标
* **列式存储（例如，ClickHouse）**：复杂查询、唯一用户分析
* **全功能可观测性平台（例如，Honeycomb、Datadog）**：高级查询、可视化、警报

### 对于事件/日志：

* **日志聚合系统（例如，Elasticsearch、Loki）**：全文搜索、日志分析
* **列式存储（例如，ClickHouse）**：结构化事件分析
* **全功能可观测性平台（例如，Honeycomb、Datadog）**：指标和事件之间的关联

对于需要日活跃用户/周活跃用户/月活跃用户（DAU/WAU/MAU）指标的组织，请考虑支持高效唯一值查询的后端。

## 服务信息

所有指标和事件都使用以下资源属性导出：

* `service.name`：`claude-code`
* `service.version`：当前 Claude Code 版本
* `os.type`：操作系统类型（例如，`linux`、`darwin`、`windows`）
* `os.version`：操作系统版本字符串
* `host.arch`：主机架构（例如，`amd64`、`arm64`）
* `wsl.version`：WSL 版本号（仅在 Windows Subsystem for Linux 上运行时存在）
* 计量器名称：`com.anthropic.claude_code`

## ROI 测量资源

有关测量 Claude Code 投资回报率的综合指南，包括遥测设置、成本分析、生产力指标和自动化报告，请参阅 [Claude Code ROI 测量指南](https://github.com/anthropics/claude-code-monitoring-guide)。此存储库提供即用型 Docker Compose 配置、Prometheus 和 OpenTelemetry 设置，以及与 Linear 等工具集成的生产力报告模板。

## 安全/隐私考虑

* 遥测是选择性加入的，需要明确配置
* 敏感信息如 API 密钥或文件内容永远不会包含在指标或事件中
* 用户提示内容默认编辑 - 仅记录提示长度。要启用用户提示日志记录，请设置 `OTEL_LOG_USER_PROMPTS=1`
