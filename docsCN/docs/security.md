# 安全性

> 了解 Claude Code 的安全保护措施和安全使用的最佳实践。

## 我们的安全方法

### 安全基础

您代码的安全性至关重要。Claude Code 以安全为核心构建，根据 Anthropic 的综合安全计划开发。在 [Anthropic 信任中心](https://trust.anthropic.com) 了解更多信息并获取资源（SOC 2 Type 2 报告、ISO 27001 证书等）。

### 基于权限的架构

Claude Code 默认使用严格的只读权限。当需要额外操作时（编辑文件、运行测试、执行命令），Claude Code 会请求明确权限。用户控制是否一次性批准操作或允许自动执行。

我们设计 Claude Code 以透明和安全为目标。例如，我们在执行 bash 命令之前需要批准，让您直接控制。这种方法使用户和组织能够直接配置权限。

有关详细的权限配置，请参阅[身份和访问管理](/zh-CN/docs/claude-code/iam)。

### 内置保护

为了降低代理系统中的风险：

* **写入访问限制**：Claude Code 只能写入启动它的文件夹及其子文件夹——它无法修改父目录中的文件。虽然 Claude Code 可以读取工作目录外的文件（对访问系统库和依赖项很有用），但写入操作严格限制在项目范围内，创建了明确的安全边界
* **提示疲劳缓解**：支持按用户、按代码库或按组织对常用安全命令进行白名单
* **接受编辑模式**：批量接受多个编辑，同时保持对有副作用命令的权限提示

### 用户责任

Claude Code 只拥有您授予它的权限。您有责任在批准之前审查建议的代码和命令的安全性。

## 防范提示注入

提示注入是攻击者试图通过插入恶意文本来覆盖或操纵 AI 助手指令的技术。Claude Code 包含针对这些攻击的多项保护措施：

### 核心保护

* **权限系统**：敏感操作需要明确批准
* **上下文感知分析**：通过分析完整请求检测潜在有害指令
* **输入清理**：通过处理用户输入防止命令注入
* **命令黑名单**：阻止从网络获取任意内容的风险命令，如 `curl` 和 `wget`

### Privacy safeguards

We have implemented several safeguards to protect your data, including:

* Limited retention periods for sensitive information
* Restricted access to user session data
* Clear policies against using feedback for model training

For full details, please review our [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) and [Privacy Policy](https://www.anthropic.com/legal/privacy).

### 额外保护措施

* **网络请求批准**：发出网络请求的工具默认需要用户批准
* **隔离上下文窗口**：网络获取使用单独的上下文窗口以避免注入潜在恶意提示
* **信任验证**：首次代码库运行和新 MCP 服务器需要信任验证
* **命令注入检测**：可疑的 bash 命令即使之前已列入白名单也需要手动批准
* **失败关闭匹配**：不匹配的命令默认需要手动批准
* **自然语言描述**：复杂的 bash 命令包含解释以便用户理解
* **安全凭据存储**：API 密钥和令牌已加密。请参阅[凭据管理](/zh-CN/docs/claude-code/iam#credential-management)

**处理不可信内容的最佳实践**：

1. 在批准之前审查建议的命令
2. 避免将不可信内容直接传输给 Claude
3. 验证对关键文件的建议更改
4. 使用虚拟机 (VM) 运行脚本和进行工具调用，特别是在与外部网络服务交互时
5. 使用 `/bug` 报告可疑行为

<Warning>
  虽然这些保护措施显著降低了风险，但没有系统能完全免疫所有攻击。在使用任何 AI 工具时始终保持良好的安全实践。
</Warning>

## MCP 安全性

Claude Code 允许用户配置模型上下文协议 (MCP) 服务器。允许的 MCP 服务器列表在您的源代码中配置，作为工程师检入源代码控制的 Claude Code 设置的一部分。

我们鼓励编写您自己的 MCP 服务器或使用来自您信任的提供商的 MCP 服务器。您能够为 MCP 服务器配置 Claude Code 权限。Anthropic 不管理或审计任何 MCP 服务器。

## 安全最佳实践

### 处理敏感代码

* 在批准之前审查所有建议的更改
* 对敏感存储库使用项目特定的权限设置
* 考虑使用[开发容器](/zh-CN/docs/claude-code/devcontainer)进行额外隔离
* 使用 `/permissions` 定期审计您的权限设置

### 团队安全

* 使用[企业管理策略](/zh-CN/docs/claude-code/iam#enterprise-managed-policy-settings)强制执行组织标准
* 通过版本控制共享已批准的权限配置
* 培训团队成员安全最佳实践
* 通过 [OpenTelemetry 指标](/zh-CN/docs/claude-code/monitoring-usage)监控 Claude Code 使用情况

### 报告安全问题

如果您在 Claude Code 中发现安全漏洞：

1. 不要公开披露
2. 通过我们的 [HackerOne 计划](https://hackerone.com/anthropic-vdp/reports/new?type=team\&report_type=vulnerability)报告
3. 包含详细的复现步骤
4. 在公开披露之前给我们时间解决问题

## 相关资源

* [身份和访问管理](/zh-CN/docs/claude-code/iam) - 配置权限和访问控制
* [监控使用情况](/zh-CN/docs/claude-code/monitoring-usage) - 跟踪和审计 Claude Code 活动
* [开发容器](/zh-CN/docs/claude-code/devcontainer) - 安全、隔离的环境
* [Anthropic 信任中心](https://trust.anthropic.com) - 安全认证和合规性
