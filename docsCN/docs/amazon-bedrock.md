# 在 Amazon Bedrock 上使用 Claude Code

> 了解如何通过 Amazon Bedrock 配置 Claude Code，包括设置、IAM 配置与故障排查。

## 前提条件

- 已开通 Bedrock 的 AWS 账号
- 已为所需 Claude 模型（如 Claude Sonnet 4）开通访问
- 已安装并配置 AWS CLI（可选）
- 具有相应 IAM 权限

## 设置步骤

### 1. 启用模型访问

在 Bedrock 控制台为所需 Claude 模型开通访问。

### 2. 配置 AWS 凭据

Claude Code 使用 AWS SDK 的默认凭据链，可通过 `aws configure`、环境变量（Access Key/SSO Profile）或 Bedrock API Key（`AWS_BEARER_TOKEN_BEDROCK`）配置。若需自动刷新 SSO 凭据，可在 Claude Code 设置中配置 `awsAuthRefresh` / `awsCredentialExport`。

### 3. 配置 Claude Code 环境变量

```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
# 可选：为小快模型单独指定区域
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2
```

注意：`AWS_REGION` 必填；启用 Bedrock 后 `/login` 与 `/logout` 将不可用。

### 4. 模型配置

默认：
- 主模型：`us.anthropic.claude-3-7-sonnet-20250219-v1:0`
- 小快模型：`us.anthropic.claude-3-5-haiku-20241022-v1:0`

也可使用推理配置文件（Inference Profile）或 ARN，自定义 `ANTHROPIC_MODEL` 与 `ANTHROPIC_SMALL_FAST_MODEL`。如需，可通过 `DISABLE_PROMPT_CACHING=1` 关闭 Prompt Caching。

### 5. 输出 Token 建议

```bash
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=4096
export MAX_THINKING_TOKENS=1024
```

理由：与 Bedrock 的令牌配额策略及代理循环稳定性相关。

## IAM 配置

授予 `bedrock:InvokeModel`、`bedrock:InvokeModelWithResponseStream`、`bedrock:ListInferenceProfiles` 等权限。可按需将资源限定为特定推理配置文件 ARN。

## 故障排查

- 区域问题：检查模型可用性、切换支持区域、或使用推理配置文件实现跨区域。
- “不支持按需吞吐量”：将模型指定为推理配置文件 ID。

## 相关资源

- Bedrock 文档、定价与推理配置文件
- AWS 社区的 Claude Code 快速上手指南

