# 在 Google Vertex AI 上使用 Claude Code

> 配置、IAM 与故障排查指南。

## 前提条件

- 启用计费的 GCP 项目，已开启 Vertex AI API
- 已为所需 Claude 模型开通访问
- 安装并配置 `gcloud`
- 目标区域（通常 `us-east5`）具备配额

## 设置步骤

1. 启用 Vertex AI API
2. 在 Model Garden 请求模型访问
3. 配置凭据（遵循标准 GCP 认证）
4. 设置环境变量：`CLAUDE_CODE_USE_VERTEX=1`、`CLOUD_ML_REGION`、`ANTHROPIC_VERTEX_PROJECT_ID`
5. 自定义模型（可选），或禁用 Prompt Caching（可选）

## 默认模型

- 主模型：`claude-sonnet-4@20250514`
- 小快模型：`claude-3-5-haiku@20241022`

## IAM 权限

- 需要 `aiplatform.endpoints.predict` 与 `aiplatform.endpoints.computeTokens`（可由 `roles/aiplatform.user` 提供）

## 故障排查

- 404：检验区域与启用状态
- 429：确认主/小快模型支持该区域
- 配额不足：在控制台查看或申请提升

