企业部署概述
======

> 了解 Claude Code 如何与各种第三方服务和基础设施集成，以满足企业部署需求。

本页面概述了可用的部署选项，并帮助您为您的组织选择正确的配置。

提供商比较
-----

```
<tr>
  <td>Prompt caching</td>
  <td>Enabled by default</td>
  <td>Enabled by default</td>
  <td>Enabled by default</td>
</tr>

<tr>
  <td>Authentication</td>
  <td>API key</td>
  <td>AWS credentials (IAM)</td>
  <td>GCP credentials (OAuth/Service Account)</td>
</tr>

<tr>
  <td>Cost tracking</td>
  <td>Dashboard</td>
  <td>AWS Cost Explorer</td>
  <td>GCP Billing</td>
</tr>

<tr>
  <td>Enterprise features</td>
  <td>Teams, usage monitoring</td>
  <td>IAM policies, CloudTrail</td>
  <td>IAM roles, Cloud Audit Logs</td>
</tr>

```

| 特性 | Anthropic | Amazon Bedrock | Google Vertex AI |
| --- |  --- |  --- |  --- |
| 地区 | 支持的\[国家\](<https://www.anthropic.com/supported-countries>) | 多个 AWS \[地区\](<https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html>) | 多个 GCP \[地区\](<https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations>) |
| --- |  --- |  --- |  --- |

云服务提供商
------

通过 AWS 基础设施使用 Claude 模型，采用基于 IAM 的认证和 AWS 原生的监控 通过 Google Cloud Platform 访问 Claude 模型，具备企业级安全性和合规性

企业基础设施
------

配置 Claude Code 以配合您组织的代理服务器和 SSL/TLS 要求 部署集中式模型访问，包含使用跟踪、预算管理和审计日志

配置概述
----

Claude Code 支持灵活的配置选项，允许您组合不同的提供商和基础设施：

了解以下区别：

-   **企业代理** ：用于路由流量的 HTTP/HTTPS 代理（通过 `HTTPS_PROXY` 或 `HTTP_PROXY` 设置）
-   **LLM 网关** : 一个处理认证并提供与提供者兼容端点（通过 `ANTHROPIC_BASE_URL`、`ANTHROPIC_BEDROCK_BASE_URL` 或 `ANTHROPIC_VERTEX_BASE_URL` 设置）的服务

两种配置可以同时使用。

### 使用 Bedrock 与企业代理

将 Bedrock 流量通过企业 HTTP/HTTPS 代理路由：

```
# Enable Bedrock
export CLAUDE\_CODE\_USE\_BEDROCK=1
export AWS\_REGION=us-east-1

# Configure corporate proxy
export HTTPS\_PROXY='https://proxy.example.com:8080'
```

### 使用 Bedrock 与 LLM Gateway

使用提供 Bedrock 兼容端点的网关服务：

```
# Enable Bedrock
export CLAUDE\_CODE\_USE\_BEDROCK=1

# Configure LLM gateway
export ANTHROPIC\_BEDROCK\_BASE\_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE\_CODE\_SKIP\_BEDROCK\_AUTH=1  # If gateway handles AWS auth
```

### 使用 Vertex AI 与公司代理

通过企业 HTTP/HTTPS 代理路由 Vertex AI 流量：

```
# Enable Vertex
export CLAUDE\_CODE\_USE\_VERTEX=1
export CLOUD\_ML\_REGION=us-east5
export ANTHROPIC\_VERTEX\_PROJECT\_ID=your-project-id

# Configure corporate proxy
export HTTPS\_PROXY='https://proxy.example.com:8080'
```

### 使用 Vertex AI 与 LLM 网关

将 Google Vertex AI 模型与 LLM 网关结合，实现集中管理：

```
# Enable Vertex
export CLAUDE\_CODE\_USE\_VERTEX=1

# Configure LLM gateway
export ANTHROPIC\_VERTEX\_BASE\_URL='https://your-llm-gateway.com/vertex'
export CLAUDE\_CODE\_SKIP\_VERTEX\_AUTH=1  # If gateway handles GCP auth
```

### 认证配置

Claude Code 在需要时使用 `ANTHROPIC_AUTH_TOKEN` 作为 `Authorization` 头部。在 LLM 网关场景中，当网关处理提供者认证时，会使用 `SKIP_AUTH` 标志（`CLAUDE_CODE_SKIP_BEDROCK_AUTH`、`CLAUDE_CODE_SKIP_VERTEX_AUTH`）。

选择合适的部署配置
---------

选择部署方式时，请考虑以下因素：

### 直接提供者访问

最适合以下组织：

-   希望设置最简单
-   已有 AWS 或 GCP 基础设施
-   需要提供商原生的监控和合规

### 企业代理

最适合以下组织：

-   已有企业代理需求
-   需要流量监控和合规
-   必须通过特定网络路径路由所有流量

### LLM 网关

最适合以下组织：

-   需要在团队间进行使用情况跟踪
-   想动态切换模型
-   需要自定义速率限制或预算
-   需要集中式身份验证管理

调试
--

在调试你的部署时：

-   使用 `claude /status` [命令](https://github.com/jumbojing/claude-code-docs/blob/main/en/docs/claude-code/slash-commands) 。该命令可提供对任何已应用的身份验证、代理和 URL 设置的可见性。
-   设置环境变量 `export ANTHROPIC_LOG=debug` 以记录请求。

组织的最佳实践
-------

### 1\. 投资文档和记忆

我们强烈建议投资于文档编写，以便 Claude Code 能够理解您的代码库。组织可以在多个层级部署 CLAUDE.md 文件：

-   **组织范围** ：部署到系统目录（如 `/Library/Application Support/ClaudeCode/CLAUDE.md` macOS）以实现公司范围内的标准

-   **仓库级别** ：在仓库根目录中创建 `CLAUDE.md` 文件，包含项目架构、构建命令和贡献指南。将这些文件提交到源代码管理，以便所有用户受益

    [了解更多](https://github.com/jumbojing/claude-code-docs/blob/main/en/docs/claude-code/memory)

### 2\. 简化部署

如果你有一个自定义的开发环境，我们发现创建一个"一键式"安装 Claude Code 的方法对于在组织内推广使用至关重要。

### 3\. 从引导式使用开始

鼓励新用户尝试使用 Claude Code 进行代码库问答，或在较小的 Bug 修复或功能请求上使用。请 Claude Code 制定计划。检查 Claude 的建议，并在其偏离方向时提供反馈。随着时间的推移，当用户更好地理解这种新的范式时，他们将更有效地让 Claude Code 以更自主的方式运行。

### 4\. 配置安全策略

安全团队可以配置 Claude Code 被允许和不被允许执行的操作的管理权限，这些权限不能被本地配置覆盖。 [了解更多](https://github.com/jumbojing/claude-code-docs/blob/main/en/docs/claude-code/security) 。

### 5\. 利用 MCP 进行集成

MCP 是向 Claude Code 提供更多信息的好方法，例如连接到工单管理系统或错误日志。我们建议由一个中央团队配置 MCP 服务器，并将一个 `.mcp.json` 配置检查到代码库中，以便所有用户受益。 [了解更多](https://github.com/jumbojing/claude-code-docs/blob/main/en/docs/claude-code/mcp) 。

在 Anthropic，我们信任 Claude Code 来驱动 Anthropic 所有代码库的开发。我们希望您能像我们一样享受使用 Claude Code！

下一步
---

-   [为 AWS 原生部署设置 Amazon Bedrock](https://github.com/jumbojing/claude-code-docs/blob/main/en/docs/claude-code/amazon-bedrock)
-   [为 GCP 部署配置 Google Vertex AI](https://github.com/jumbojing/claude-code-docs/blob/main/en/docs/claude-code/google-vertex-ai)
-   [为网络需求实现企业代理](https://github.com/jumbojing/claude-code-docs/blob/main/en/docs/claude-code/corporate-proxy)
-   [为企业管理部署 LLM 网关](https://github.com/jumbojing/claude-code-docs/blob/main/en/docs/claude-code/llm-gateway)
-   [设置](https://github.com/jumbojing/claude-code-docs/blob/main/en/docs/claude-code/settings)用于配置选项和环境变量
