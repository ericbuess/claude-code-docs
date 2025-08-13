# 设置 Claude Code

> 在您的开发机器上安装、认证并开始使用 Claude Code。

## 系统要求

* **操作系统**: macOS 10.15+、Ubuntu 20.04+/Debian 10+ 或 Windows 10+（使用 WSL 1、WSL 2 或 Git for Windows）
* **硬件**: 4GB+ RAM
* **软件**: [Node.js 18+](https://nodejs.org/en/download)
* **网络**: 需要互联网连接进行认证和 AI 处理
* **Shell**: 在 Bash、Zsh 或 Fish 中效果最佳
* **位置**: [Anthropic 支持的国家](https://www.anthropic.com/supported-countries)

## 标准安装

To install Claude Code, run the following command:

```sh
npm install -g @anthropic-ai/claude-code
```

<Warning>
  请勿使用 `sudo npm install -g`，因为这可能导致权限问题和安全风险。
  如果遇到权限错误，请参阅[配置 Claude Code](/zh-CN/docs/claude-code/troubleshooting#linux-permission-issues)获取推荐解决方案。
</Warning>

<Note>
  某些用户可能会自动迁移到改进的安装方法。
  安装后运行 `claude doctor` 检查您的安装类型。
</Note>

安装过程完成后，导航到您的项目并启动 Claude Code：

```bash
cd your-awesome-project
claude
```

Claude Code 提供以下认证选项：

1. **Anthropic Console**: 默认选项。通过 Anthropic Console 连接并完成 OAuth 流程。需要在 [console.anthropic.com](https://console.anthropic.com) 激活计费。
2. **Claude App（Pro 或 Max 计划）**: 订阅 Claude 的 [Pro 或 Max 计划](https://www.anthropic.com/pricing)，获得包含 Claude Code 和 Web 界面的统一订阅。以相同价格获得更多价值，同时在一个地方管理您的账户。使用您的 Claude.ai 账户登录。启动期间，选择与您的订阅类型匹配的选项。
3. **企业平台**: 配置 Claude Code 使用 [Amazon Bedrock 或 Google Vertex AI](/zh-CN/docs/claude-code/third-party-integrations) 进行企业部署，使用您现有的云基础设施。

<Note>
  Claude Code 安全地存储您的凭据。详情请参阅[凭据管理](/zh-CN/docs/claude-code/iam#credential-management)。
</Note>

## Windows 设置

**选项 1: WSL 中的 Claude Code**

* 支持 WSL 1 和 WSL 2

**选项 2: 使用 Git Bash 在原生 Windows 上运行 Claude Code**

* 需要 [Git for Windows](https://git-scm.com/downloads/win)
* 对于便携式 Git 安装，请指定 `bash.exe` 的路径：
  ```powershell
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## 替代安装方法

Claude Code 提供多种安装方法以适应不同环境。

如果在安装过程中遇到任何问题，请查阅[故障排除指南](/zh-CN/docs/claude-code/troubleshooting#linux-permission-issues)。

<Tip>
  安装后运行 `claude doctor` 检查您的安装类型和版本。
</Tip>

### 全局 npm 安装

上述[安装步骤](#install-and-authenticate)中显示的传统方法

### 原生二进制安装（Beta）

如果您已有 Claude Code 安装，请使用 `claude install` 开始原生二进制安装。

对于全新安装，运行以下命令：

**macOS、Linux、WSL:**

```bash
# 安装稳定版本（默认）
curl -fsSL https://claude.ai/install.sh | bash

# 安装最新版本
curl -fsSL https://claude.ai/install.sh | bash -s latest

# 安装特定版本号
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```

**Windows PowerShell:**

```powershell
# 安装稳定版本（默认）
irm https://claude.ai/install.ps1 | iex

# 安装最新版本
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest

# 安装特定版本号
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58

```

原生 Claude Code 安装程序支持 macOS、Linux 和 Windows。

<Tip>
  确保删除任何过时的别名或符号链接。
  安装完成后，运行 `claude doctor` 验证安装。
</Tip>

### 本地安装

* 通过 npm 全局安装后，使用 `claude migrate-installer` 迁移到本地
* 避免自动更新程序的 npm 权限问题
* 某些用户可能会自动迁移到此方法

## 在 AWS 或 GCP 上运行

默认情况下，Claude Code 使用 Anthropic 的 API。

有关在 AWS 或 GCP 上运行 Claude Code 的详细信息，请参阅[第三方集成](/zh-CN/docs/claude-code/third-party-integrations)。

## 更新 Claude Code

### 自动更新

Claude Code 自动保持最新状态，确保您拥有最新功能和安全修复。

* **更新检查**: 在启动时和运行期间定期执行
* **更新过程**: 在后台自动下载和安装
* **通知**: 安装更新时您会看到通知
* **应用更新**: 更新在下次启动 Claude Code 时生效

**禁用自动更新:**

```bash
# 通过配置
claude config set autoUpdates false --global

# 或通过环境变量
export DISABLE_AUTOUPDATER=1
```

### 手动更新

```bash
claude update
```
