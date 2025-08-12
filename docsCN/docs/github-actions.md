# Claude Code GitHub Actions

> 了解如何使用 Claude Code GitHub Actions 将 Claude Code 集成到您的开发工作流程中

Claude Code GitHub Actions 为您的 GitHub 工作流程带来 AI 驱动的自动化。只需在任何 PR 或 issue 中简单地提及 `@claude`，Claude 就可以分析您的代码、创建拉取请求、实现功能和修复错误 - 所有这些都遵循您项目的标准。

<Info>
  Claude Code GitHub Actions 目前处于测试阶段。随着我们完善体验，功能和特性可能会发生变化。
</Info>

<Note>
  Claude Code GitHub Actions 基于 [Claude Code SDK](/zh-CN/docs/claude-code/sdk) 构建，该 SDK 支持将 Claude Code 程序化集成到您的应用程序中。您可以使用 SDK 构建超越 GitHub Actions 的自定义自动化工作流程。
</Note>

## 为什么使用 Claude Code GitHub Actions？

* **即时 PR 创建**：描述您的需求，Claude 会创建包含所有必要更改的完整 PR
* **自动化代码实现**：通过单个命令将 issue 转换为可工作的代码
* **遵循您的标准**：Claude 尊重您的 `CLAUDE.md` 指南和现有代码模式
* **简单设置**：使用我们的安装程序和 API 密钥在几分钟内开始使用
* **默认安全**：您的代码保留在 Github 的运行器上

## Claude 能做什么？

Claude Code 提供强大的 GitHub Actions，改变您处理代码的方式：

### Claude Code Action

此 GitHub Action 允许您在 GitHub Actions 工作流程中运行 Claude Code。您可以使用它在 Claude Code 之上构建任何自定义工作流程。

[查看仓库 →](https://github.com/anthropics/claude-code-action)

### Claude Code Action (Base)

使用 Claude 构建自定义 GitHub 工作流程的基础。这个可扩展的框架为您提供对 Claude 功能的完全访问权限，用于创建定制的自动化。

[查看仓库 →](https://github.com/anthropics/claude-code-base-action)

## 设置

## 快速设置

设置此操作的最简单方法是通过终端中的 Claude Code。只需打开 claude 并运行 `/install-github-app`。

此命令将指导您完成设置 GitHub 应用程序和所需密钥的过程。

<Note>
  * 您必须是仓库管理员才能安装 GitHub 应用程序和添加密钥
  * 此快速启动方法仅适用于直接 Anthropic API 用户。如果您使用 AWS Bedrock 或 Google Vertex AI，请参阅[与 AWS Bedrock 和 Google Vertex AI 一起使用](#using-with-aws-bedrock-%26-google-vertex-ai)部分。
</Note>

## 手动设置

如果 `/install-github-app` 命令失败或您更喜欢手动设置，请按照以下手动设置说明操作：

1. **将 Claude GitHub 应用程序安装**到您的仓库：[https://github.com/apps/claude](https://github.com/apps/claude)
2. **将 ANTHROPIC\_API\_KEY 添加**到您的仓库密钥中（[了解如何在 GitHub Actions 中使用密钥](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)）
3. **复制工作流程文件**从 [examples/claude.yml](https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml) 到您仓库的 `.github/workflows/`

<Tip>
  完成快速启动或手动设置后，通过在 issue 或 PR 评论中标记 `@claude` 来测试操作！
</Tip>

## 示例用例

Claude Code GitHub Actions 可以帮助您完成各种任务。有关完整的工作示例，请参阅[示例目录](https://github.com/anthropics/claude-code-action/tree/main/examples)。

### 将 issue 转换为 PR

在 issue 评论中：

```
@claude 根据 issue 描述实现此功能
```

Claude 将分析 issue，编写代码，并创建 PR 供审查。

### 获取实现帮助

在 PR 评论中：

```
@claude 我应该如何为此端点实现用户身份验证？
```

Claude 将分析您的代码并提供具体的实现指导。

### 快速修复错误

在 issue 中：

```yaml
@claude 修复用户仪表板组件中的 TypeError
```

Claude 将定位错误，实现修复，并创建 PR。

## 最佳实践

### CLAUDE.md 配置

在您的仓库根目录中创建一个 `CLAUDE.md` 文件来定义代码风格指南、审查标准、项目特定规则和首选模式。此文件指导 Claude 理解您的项目标准。

### 安全考虑

<Warning>
  永远不要直接将 API 密钥提交到您的仓库！
</Warning>

始终使用 GitHub 密钥来存储 API 密钥：

* 将您的 API 密钥添加为名为 `ANTHROPIC_API_KEY` 的仓库密钥
* 在工作流程中引用它：`anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`
* 将操作权限限制为仅必需的权限
* 在合并之前审查 Claude 的建议

始终使用 GitHub 密钥（例如，`${{ secrets.ANTHROPIC_API_KEY }}`）而不是在工作流程文件中直接硬编码 API 密钥。

### 优化性能

使用 issue 模板提供上下文，保持您的 `CLAUDE.md` 简洁和专注，并为您的工作流程配置适当的超时。

### CI 成本

使用 Claude Code GitHub Actions 时，请注意相关成本：

**GitHub Actions 成本：**

* Claude Code 在 GitHub 托管的运行器上运行，这会消耗您的 GitHub Actions 分钟数
* 有关详细定价和分钟数限制，请参阅 [GitHub 的计费文档](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions)

**API 成本：**

* 每次 Claude 交互都会根据提示和响应的长度消耗 API 令牌
* 令牌使用量因任务复杂性和代码库大小而异
* 有关当前令牌费率，请参阅 [Claude 的定价页面](https://www.anthropic.com/api)

**成本优化提示：**

* 使用特定的 `@claude` 命令来减少不必要的 API 调用
* 配置适当的 `max_turns` 限制以防止过度迭代
* 设置合理的 `timeout_minutes` 以避免失控的工作流程
* 考虑使用 GitHub 的并发控制来限制并行运行

## 配置示例

对于不同用例的即用型工作流程配置，包括：

* issue 和 PR 评论的基本工作流程设置
* 拉取请求的自动化代码审查
* 特定需求的自定义实现

访问 Claude Code Action 仓库中的[示例目录](https://github.com/anthropics/claude-code-action/tree/main/examples)。

<Tip>
  示例仓库包含完整的、经过测试的工作流程，您可以直接复制到您的 `.github/workflows/` 目录中。
</Tip>

## 与 AWS Bedrock 和 Google Vertex AI 一起使用

对于企业环境，您可以将 Claude Code GitHub Actions 与您自己的云基础设施一起使用。这种方法让您控制数据驻留和计费，同时保持相同的功能。

### 先决条件

在使用云提供商设置 Claude Code GitHub Actions 之前，您需要：

#### 对于 Google Cloud Vertex AI：

1. 启用了 Vertex AI 的 Google Cloud 项目
2. 为 GitHub Actions 配置的工作负载身份联合
3. 具有所需权限的服务帐户
4. GitHub 应用程序（推荐）或使用默认的 GITHUB\_TOKEN

#### 对于 AWS Bedrock：

1. 启用了 Amazon Bedrock 的 AWS 帐户
2. 在 AWS 中配置的 GitHub OIDC 身份提供者
3. 具有 Bedrock 权限的 IAM 角色
4. GitHub 应用程序（推荐）或使用默认的 GITHUB\_TOKEN

<Steps>
  <Step title="创建自定义 GitHub 应用程序（推荐用于第三方提供商）">
    为了在使用 Vertex AI 或 Bedrock 等第三方提供商时获得最佳控制和安全性，我们建议创建您自己的 GitHub 应用程序：

    1. 转到 [https://github.com/settings/apps/new](https://github.com/settings/apps/new)
    2. 填写基本信息：
       * **GitHub 应用程序名称**：选择一个唯一的名称（例如，"YourOrg Claude Assistant"）
       * **主页 URL**：您组织的网站或仓库 URL
    3. 配置应用程序设置：
       * **Webhooks**：取消选中"Active"（此集成不需要）
    4. 设置所需权限：
       * **仓库权限**：
         * Contents：读取和写入
         * Issues：读取和写入
         * Pull requests：读取和写入
    5. 点击"创建 GitHub 应用程序"
    6. 创建后，点击"生成私钥"并保存下载的 `.pem` 文件
    7. 从应用程序设置页面记下您的应用程序 ID
    8. 将应用程序安装到您的仓库：
       * 从您应用程序的设置页面，点击左侧边栏中的"安装应用程序"
       * 选择您的帐户或组织
       * 选择"仅选择仓库"并选择特定仓库
       * 点击"安装"
    9. 将私钥作为密钥添加到您的仓库：
       * 转到您仓库的设置 → 密钥和变量 → Actions
       * 创建一个名为 `APP_PRIVATE_KEY` 的新密钥，内容为 `.pem` 文件的内容
    10. 将应用程序 ID 作为密钥添加：

    * 创建一个名为 `APP_ID` 的新密钥，值为您的 GitHub 应用程序的 ID

    <Note>
      此应用程序将与 [actions/create-github-app-token](https://github.com/actions/create-github-app-token) 操作一起使用，在您的工作流程中生成身份验证令牌。
    </Note>

    **Anthropic API 的替代方案或如果您不想设置自己的 Github 应用程序**：使用官方 Anthropic 应用程序：

    1. 从以下位置安装：[https://github.com/apps/claude](https://github.com/apps/claude)
    2. 身份验证无需额外配置
  </Step>

  <Step title="配置云提供商身份验证">
    选择您的云提供商并设置安全身份验证：

    <AccordionGroup>
      <Accordion title="AWS Bedrock">
        **配置 AWS 以允许 GitHub Actions 安全地进行身份验证，而无需存储凭据。**

        > **安全说明**：使用特定于仓库的配置，并仅授予所需的最小权限。

        **所需设置**：

        1. **启用 Amazon Bedrock**：
           * 在 Amazon Bedrock 中请求访问 Claude 模型
           * 对于跨区域模型，请在所有必需区域中请求访问

        2. **设置 GitHub OIDC 身份提供者**：
           * 提供者 URL：`https://token.actions.githubusercontent.com`
           * 受众：`sts.amazonaws.com`

        3. **为 GitHub Actions 创建 IAM 角色**：
           * 受信任实体类型：Web 身份
           * 身份提供者：`token.actions.githubusercontent.com`
           * 权限：`AmazonBedrockFullAccess` 策略
           * 为您的特定仓库配置信任策略

        **所需值**：

        设置后，您将需要：

        * **AWS\_ROLE\_TO\_ASSUME**：您创建的 IAM 角色的 ARN

        <Tip>
          OIDC 比使用静态 AWS 访问密钥更安全，因为凭据是临时的并且会自动轮换。
        </Tip>

        有关详细的 OIDC 设置说明，请参阅 [AWS 文档](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)。
      </Accordion>

      <Accordion title="Google Vertex AI">
        **配置 Google Cloud 以允许 GitHub Actions 安全地进行身份验证，而无需存储凭据。**

        > **安全说明**：使用特定于仓库的配置，并仅授予所需的最小权限。

        **所需设置**：

        1. **在您的 Google Cloud 项目中启用 API**：
           * IAM 凭据 API
           * 安全令牌服务 (STS) API
           * Vertex AI API

        2. **创建工作负载身份联合资源**：
           * 创建工作负载身份池
           * 添加 GitHub OIDC 提供者，包含：
             * 发行者：`https://token.actions.githubusercontent.com`
             * 仓库和所有者的属性映射
             * **安全建议**：使用特定于仓库的属性条件

        3. **创建服务帐户**：
           * 仅授予 `Vertex AI User` 角色
           * **安全建议**：为每个仓库创建专用服务帐户

        4. **配置 IAM 绑定**：
           * 允许工作负载身份池模拟服务帐户
           * **安全建议**：使用特定于仓库的主体集

        **所需值**：

        设置后，您将需要：

        * **GCP\_WORKLOAD\_IDENTITY\_PROVIDER**：完整的提供者资源名称
        * **GCP\_SERVICE\_ACCOUNT**：服务帐户电子邮件地址

        <Tip>
          工作负载身份联合消除了对可下载服务帐户密钥的需求，提高了安全性。
        </Tip>

        有关详细的设置说明，请参阅 [Google Cloud 工作负载身份联合文档](https://cloud.google.com/iam/docs/workload-identity-federation)。
      </Accordion>
    </AccordionGroup>
  </Step>

  <Step title="添加所需密钥">
    将以下密钥添加到您的仓库（设置 → 密钥和变量 → Actions）：

    #### 对于 Anthropic API（直接）：

    1. **用于 API 身份验证**：
       * `ANTHROPIC_API_KEY`：来自 [console.anthropic.com](https://console.anthropic.com) 的 Anthropic API 密钥

    2. **用于 GitHub 应用程序（如果使用您自己的应用程序）**：
       * `APP_ID`：您的 GitHub 应用程序的 ID
       * `APP_PRIVATE_KEY`：私钥（.pem）内容

    #### 对于 Google Cloud Vertex AI

    1. **用于 GCP 身份验证**：
       * `GCP_WORKLOAD_IDENTITY_PROVIDER`
       * `GCP_SERVICE_ACCOUNT`

    2. **用于 GitHub 应用程序（如果使用您自己的应用程序）**：
       * `APP_ID`：您的 GitHub 应用程序的 ID
       * `APP_PRIVATE_KEY`：私钥（.pem）内容

    #### 对于 AWS Bedrock

    1. **用于 AWS 身份验证**：
       * `AWS_ROLE_TO_ASSUME`

    2. **用于 GitHub 应用程序（如果使用您自己的应用程序）**：
       * `APP_ID`：您的 GitHub 应用程序的 ID
       * `APP_PRIVATE_KEY`：私钥（.pem）内容
  </Step>

  <Step title="创建工作流程文件">
    创建与您的云提供商集成的 GitHub Actions 工作流程文件。以下示例显示了 AWS Bedrock 和 Google Vertex AI 的完整配置：

    <AccordionGroup>
      <Accordion title="AWS Bedrock 工作流程">
        **先决条件：**

        * 启用了 Claude 模型权限的 AWS Bedrock 访问
        * 在 AWS 中配置为 OIDC 身份提供者的 GitHub
        * 具有信任 GitHub Actions 的 Bedrock 权限的 IAM 角色

        **所需的 GitHub 密钥：**

        | 密钥名称                 | 描述                          |
        | -------------------- | --------------------------- |
        | `AWS_ROLE_TO_ASSUME` | 用于 Bedrock 访问的 IAM 角色 ARN   |
        | `APP_ID`             | 您的 GitHub 应用程序 ID（来自应用程序设置） |
        | `APP_PRIVATE_KEY`    | 您为 GitHub 应用程序生成的私钥         |

        ```yaml
        name: Claude PR Action 

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write 

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened, assigned]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
            runs-on: ubuntu-latest
            env:
              AWS_REGION: us-west-2
            steps:
              - name: Checkout repository
                uses: actions/checkout@v4

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Configure AWS Credentials (OIDC)
                uses: aws-actions/configure-aws-credentials@v4
                with:
                  role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
                  aws-region: us-west-2

              - uses: ./.github/actions/claude-pr-action
                with:
                  trigger_phrase: "@claude"
                  timeout_minutes: "60"
                  github_token: ${{ steps.app-token.outputs.token }}
                  use_bedrock: "true"
                  model: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
        ```

        <Tip>
          Bedrock 的模型 ID 格式包括区域前缀（例如，`us.anthropic.claude...`）和版本后缀。
        </Tip>
      </Accordion>

      <Accordion title="Google Vertex AI 工作流程">
        **先决条件：**

        * 在您的 GCP 项目中启用了 Vertex AI API
        * 为 GitHub 配置的工作负载身份联合
        * 具有 Vertex AI 权限的服务帐户

        **所需的 GitHub 密钥：**

        | 密钥名称                             | 描述                          |
        | -------------------------------- | --------------------------- |
        | `GCP_WORKLOAD_IDENTITY_PROVIDER` | 工作负载身份提供者资源名称               |
        | `GCP_SERVICE_ACCOUNT`            | 具有 Vertex AI 访问权限的服务帐户电子邮件  |
        | `APP_ID`                         | 您的 GitHub 应用程序 ID（来自应用程序设置） |
        | `APP_PRIVATE_KEY`                | 您为 GitHub 应用程序生成的私钥         |

        ```yaml
        name: Claude PR Action

        permissions: 
          contents: write
          pull-requests: write
          issues: write
          id-token: write  

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened, assigned]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
            runs-on: ubuntu-latest
            steps:
              - name: Checkout repository
                uses: actions/checkout@v4

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Authenticate to Google Cloud
                id: auth
                uses: google-github-actions/auth@v2
                with:
                  workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
                  service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}
              
              - uses: ./.github/actions/claude-pr-action
                with:
                  trigger_phrase: "@claude"
                  timeout_minutes: "60"
                  github_token: ${{ steps.app-token.outputs.token }}
                  use_vertex: "true"
                  model: "claude-3-7-sonnet@20250219"
                env:
                  ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
                  CLOUD_ML_REGION: us-east5
                  VERTEX_REGION_CLAUDE_3_7_SONNET: us-east5
        ```

        <Tip>
          项目 ID 会从 Google Cloud 身份验证步骤中自动检索，因此您无需硬编码它。
        </Tip>
      </Accordion>
    </AccordionGroup>
  </Step>
</Steps>

## 故障排除

### Claude 不响应 @claude 命令

验证 GitHub 应用程序是否正确安装，检查工作流程是否已启用，确保 API 密钥已在仓库密钥中设置，并确认评论包含 `@claude`（不是 `/claude`）。

### CI 不在 Claude 的提交上运行

确保您使用的是 GitHub 应用程序或自定义应用程序（不是 Actions 用户），检查工作流程触发器是否包含必要的事件，并验证应用程序权限是否包含 CI 触发器。

### 身份验证错误

确认 API 密钥有效且具有足够的权限。对于 Bedrock/Vertex，检查凭据配置并确保密钥在工作流程中正确命名。

## 高级配置

### 操作参数

Claude Code Action 支持以下关键参数：

| 参数                  | 描述               | 必需    |
| ------------------- | ---------------- | ----- |
| `prompt`            | 发送给 Claude 的提示   | 是\*   |
| `prompt_file`       | 包含提示的文件路径        | 是\*   |
| `anthropic_api_key` | Anthropic API 密钥 | 是\*\* |
| `max_turns`         | 最大对话轮数           | 否     |
| `timeout_minutes`   | 执行超时             | 否     |

\*需要 `prompt` 或 `prompt_file` 之一\
\*\*直接 Anthropic API 需要，Bedrock/Vertex 不需要

### 替代集成方法

虽然 `/install-github-app` 命令是推荐的方法，但您也可以：

* **自定义 GitHub 应用程序**：对于需要品牌用户名或自定义身份验证流程的组织。创建您自己的具有所需权限（内容、issue、拉取请求）的 GitHub 应用程序，并使用 actions/create-github-app-token 操作在您的工作流程中生成令牌。
* **手动 GitHub Actions**：直接工作流程配置以获得最大灵活性
* **MCP 配置**：模型上下文协议服务器的动态加载

有关详细文档，请参阅 [Claude Code Action 仓库](https://github.com/anthropics/claude-code-action)。

### 自定义 Claude 的行为

您可以通过两种方式配置 Claude 的行为：

1. **CLAUDE.md**：在仓库根目录的 `CLAUDE.md` 文件中定义编码标准、审查标准和项目特定规则。Claude 在创建 PR 和响应请求时将遵循这些指南。查看我们的[内存文档](/zh-CN/docs/claude-code/memory)了解更多详情。
2. **自定义提示**：在工作流程文件中使用 `prompt` 参数提供特定于工作流程的说明。这允许您为不同的工作流程或任务自定义 Claude 的行为。

Claude 在创建 PR 和响应请求时将遵循这些指南。
