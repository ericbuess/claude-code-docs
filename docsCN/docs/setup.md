# 设置 Claude Code

> 在开发机上安装、认证并开始使用 Claude Code。

## 系统要求

- 操作系统：macOS 10.15+、Ubuntu 20.04+/Debian 10+，或 Windows 10+（WSL1/WSL2 或 Git for Windows）
- 硬件：4GB+ 内存
- 软件：[Node.js 18+](https://nodejs.org/en/download)
- 网络：需要联网以完成认证与 AI 交互
- Shell：推荐 Bash、Zsh 或 Fish
- 地区：需在 Anthropic 支持的国家/地区

## 标准安装

运行：

```sh
npm install -g @anthropic-ai/claude-code
```

<Warning>
  不要使用 `sudo npm install -g`，否则可能引发权限与安全问题。如遇权限错误，参见故障排查中的 Linux 权限部分。
</Warning>

<Note>
  部分用户可能被自动迁移到改进的安装方式。安装后运行 `claude doctor` 查看安装类型。
</Note>

安装完成后进入你的项目并启动：

```bash
cd your-awesome-project
claude
```

支持的认证方式：
1. Anthropic Console（默认，需开启计费）
2. Claude App 订阅（Pro/Max，统一订阅、同价更多功能）
3. 企业平台：通过 [Amazon Bedrock 或 Google Vertex AI](/en/docs/claude-code/third-party-integrations)

<Note>
  凭据安全存储，详见 [Credential Management](/en/docs/claude-code/iam#credential-management)。
</Note>

## Windows 配置

- 方案一：在 WSL 中运行（支持 WSL1/WSL2）
- 方案二：原生 Windows 配合 Git Bash（可设置 `CLAUDE_CODE_GIT_BASH_PATH` 指向 bash.exe）

## 其它安装方式

- 全局 npm 安装（如上）
- 原生二进制安装（Beta）：curl 安装脚本，支持 macOS/Linux/WSL/Windows
- 本地安装：`claude migrate-installer` 迁移到 `~/.claude/local/`，避免 npm 权限问题

## 在 AWS 或 GCP 上运行

默认使用 Anthropic API。要在 AWS/GCP 上运行，参见第三方集成文档。

## 更新 Claude Code

### 自动更新

- 启动和运行期间定期检查
- 后台下载并安装
- 安装完成会提示，下次启动生效

禁用自动更新：
```bash
claude config set autoUpdates false --global
export DISABLE_AUTOUPDATER=1
```

### 手动更新

```bash
claude update
```

