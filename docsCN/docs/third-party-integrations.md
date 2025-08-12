# 企业级部署总览

> 了解 Claude Code 如何与第三方服务与基础设施集成以满足企业部署需求。

本页提供部署选项对比与选型参考：直连提供方、企业代理、LLM 网关等，也介绍它们如何组合使用。

## 提供方对比

- 区域与可用性：Anthropic/Bedrock/Vertex 各自多区域
- 提示缓存：默认启用
- 认证：API Key / AWS 凭据（IAM）/ GCP 凭据
- 成本追踪：各自原生计费/看板
- 企业特性：团队/用量监控、IAM 策略、审计日志

## 云提供方

- Amazon Bedrock：基于 AWS 基建与 IAM 的访问与监控
- Google Vertex AI：基于 GCP 的企业级安全与合规

## 企业内网设施

- 企业代理：按组织代理与证书要求配置
- LLM 网关：集中模型访问、用量统计、预算与审计

## 组合配置概览

注意企业代理（HTTP(S) 代理，HTTPS_PROXY/HTTP_PROXY）与 LLM 网关（提供兼容端点的服务，ANTHROPIC_*_BASE_URL）差异，两者可同时使用。

示例：
- Bedrock + 企业代理
- Bedrock + LLM 网关（必要时跳过本地云认证）
- Vertex + 企业代理
- Vertex + LLM 网关（必要时跳过本地云认证）

认证：在需要时通过 `ANTHROPIC_AUTH_TOKEN` 设置 Authorization；在网关场景使用 `CLAUDE_CODE_SKIP_*_AUTH` 跳过本地云认证。

## 选型建议

- 直连提供方：最简单、可复用现有云账务/监控
- 企业代理：满足网络监管与合规路径要求
- LLM 网关：统一用量/预算/路由/认证，灵活切换模型

## 调试

- 使用 `/status` 查看当前认证、代理与 URL 配置
- 设置 `ANTHROPIC_LOG=debug` 输出请求日志

## 组织最佳实践

- 文档与记忆：多层级 CLAUDE.md（组织/仓库），帮助 Claude 了解代码库
- 简化部署：提供一键安装体验促进采纳
- 引导使用：从问答/小变更入手，逐步放权
- 安全策略：受管权限策略不可被本地覆盖
- 利用 MCP：集中配置 `.mcp.json` 以接入工单/日志/文档等

下一步：按需前往 Bedrock/Vertex/企业代理/LLM 网关/设置 文档继续配置。

