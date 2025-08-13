# Amazon Bedrock 上的 Claude Code

> 了解如何通过 Amazon Bedrock 配置 Claude Code，包括设置、IAM 配置和故障排除。

## 先决条件

在使用 Bedrock 配置 Claude Code 之前，请确保您具备：

* 启用了 Bedrock 访问权限的 AWS 账户
* 在 Bedrock 中访问所需的 Claude 模型（例如 Claude Sonnet 4）
* 已安装并配置的 AWS CLI（可选 - 仅在您没有其他获取凭证机制时需要）
* 适当的 IAM 权限

## 设置

### 1. 启用模型访问

首先，确保您在 AWS 账户中可以访问所需的 Claude 模型：

1. 导航到 [Amazon Bedrock 控制台](https://console.aws.amazon.com/bedrock/)
2. 在左侧导航中转到**模型访问**
3. 请求访问所需的 Claude 模型（例如 Claude Sonnet 4）
4. 等待批准（大多数区域通常是即时的）

### 2. 配置 AWS 凭证

Claude Code 使用默认的 AWS SDK 凭证链。使用以下方法之一设置您的凭证：

<Note>
  Claude Code 目前不支持动态凭证管理（例如自动调用 `aws sts assume-role`）。您需要自己运行 `aws configure`、`aws sso login` 或设置 `AWS_` 环境变量。
</Note>

**选项 A：AWS CLI 配置**

```bash
aws configure
```

**选项 B：环境变量（访问密钥）**

```bash
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**选项 C：环境变量（SSO 配置文件）**

```bash
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**选项 D：Bedrock API 密钥**

```bash
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Bedrock API 密钥提供了一种更简单的身份验证方法，无需完整的 AWS 凭证。[了解更多关于 Bedrock API 密钥的信息](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/)。

### 3. 配置 Claude Code

设置以下环境变量以启用 Bedrock：

```bash
# 启用 Bedrock 集成
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # 或您首选的区域

# 可选：覆盖小型/快速模型（Haiku）的区域
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2
```

<Note>
  `AWS_REGION` 是必需的环境变量。Claude Code 不会从 `.aws` 配置文件中读取此设置。
</Note>

<Note>
  使用 Bedrock 时，`/login` 和 `/logout` 命令被禁用，因为身份验证通过 AWS 凭证处理。
</Note>

### 4. 模型配置

Claude Code 为 Bedrock 使用这些默认模型：

| 模型类型    | 默认值                                            |
| :------ | :--------------------------------------------- |
| 主要模型    | `us.anthropic.claude-3-7-sonnet-20250219-v1:0` |
| 小型/快速模型 | `us.anthropic.claude-3-5-haiku-20241022-v1:0`  |

要自定义模型，请使用以下方法之一：

```bash
# 使用推理配置文件 ID
export ANTHROPIC_MODEL='us.anthropic.claude-opus-4-20250514-v1:0'
export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-3-5-haiku-20241022-v1:0'

# 使用应用程序推理配置文件 ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# 可选：如果需要，禁用提示缓存
export DISABLE_PROMPT_CACHING=1
```

<Note>
  [提示缓存](/zh-CN/docs/build-with-claude/prompt-caching) 可能在所有区域都不可用
</Note>

## IAM 配置

为 Claude Code 创建具有所需权限的 IAM 策略：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*"
      ]
    }
  ]
}
```

对于更严格的权限，您可以将资源限制为特定的推理配置文件 ARN。

有关详细信息，请参阅 [Bedrock IAM 文档](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html)。

<Note>
  我们建议为 Claude Code 创建专用的 AWS 账户，以简化成本跟踪和访问控制。
</Note>

## 故障排除

如果您遇到区域问题：

* 检查模型可用性：`aws bedrock list-inference-profiles --region your-region`
* 切换到支持的区域：`export AWS_REGION=us-east-1`
* 考虑使用推理配置文件进行跨区域访问

如果您收到"不支持按需吞吐量"错误：

* 将模型指定为[推理配置文件](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) ID

## 其他资源

* [Bedrock 文档](https://docs.aws.amazon.com/bedrock/)
* [Bedrock 定价](https://aws.amazon.com/bedrock/pricing/)
* [Bedrock 推理配置文件](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Amazon Bedrock 上的 Claude Code：快速设置指南](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
