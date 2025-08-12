# Claude Code 文档镜像（中文）

[![最后更新](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

本仓库是 Claude Code 文档的本地镜像，源自 https://docs.anthropic.com/en/docs/claude-code/，每 3 小时自动更新一次。

## 🆕 版本 0.3.2 - 重要更新

如果你之前安装过旧版本，请重新运行安装程序完成更新：

```bash
curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install.sh | bash
```

本次更新修复了自动更新机制失效的问题。

## 为什么需要这个仓库

- 更快的访问：直接读取本地文件，无需联网取文档
- 自动更新：尽量保持与官方文档最新同步
- 追踪变更：查看文档在不同时间的变化
- 更好地配合 Claude Code：便于 Claude 在本地高效检索文档

## 先决条件

需要安装以下工具：
- git：用于克隆与更新仓库（macOS 通常已预装）
- jq：在自动更新 Hook 中处理 JSON（macOS 通常预装；Linux 可通过 `apt install jq` 或 `yum install jq` 安装）
- curl：下载安装脚本（通常已预装）
- Claude Code：当然需要 :)

平台支持：完整支持 macOS 与 Linux。欢迎贡献 Windows 支持！

## 安装

执行以下单条命令：

```bash
curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install.sh | bash
```

该脚本将：
1. 安装到 `~/.claude-code-docs`（或迁移已有安装）
2. 创建 `/docs` 斜杠命令，将参数传递给工具并指向本地文档目录
3. 在 Claude 中添加一个 PreToolUse Read 钩子，在读取 `~/.claude-code-docs` 中的文档时自动执行 `git pull`

注意：命令在列表中显示为 `/docs (user)`，表示用户自定义命令。

## 使用方法

`/docs` 命令提供开箱即用的本地文档访问，并可按需检查新鲜度。

### 默认：极速访问（不检查）
```bash
/docs hooks
/docs mcp
/docs memory
```
你会看到：`📚 Reading from local docs (run /docs -t to check freshness)`

### 使用 -t 检查文档同步状态
```bash
/docs -t           # 显示与 GitHub 的同步状态
/docs -t hooks     # 检查并读取 hooks 文档
/docs -t mcp       # 检查并读取 MCP 文档
```

### 查看最近更新
```bash
/docs what's new   # 显示最新文档变更及 diff
```

### 卸载
```bash
/docs uninstall    # 获取完全卸载 claude-code-docs 的命令
```

### 创意用法示例
```bash
# 自然语言查询
/docs what environment variables exist and how do I use them?
/docs explain the differences between hooks and MCP

# 查看最近变更
/docs -t what's new in the latest documentation?

# 全文检索
/docs find all mentions of authentication
/docs how do I customize Claude Code's behavior?
```

## 更新机制

文档尝试保持最新：
- GitHub Actions 定期抓取新文档
- 使用 `/docs` 时可检查更新
- 如果有更新会自动拉取
- 你可能会看到 “🔄 Updating documentation...” 提示

如自动更新失败，可随时重新运行安装脚本获取最新版本。

## 从旧版本更新

无论当前版本如何，直接运行：

```bash
curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install.sh | bash
```

安装器会自动处理迁移与更新。

## 故障排查

### 命令未找到
如果 `/docs` 提示 “command not found”：
1. 检查命令文件：`ls ~/.claude/commands/docs.md`
2. 重启 Claude Code 以重新加载命令
3. 重新运行安装脚本

### 文档没有更新
如果文档看起来过期：
1. 运行 `/docs -t` 检查同步并强制更新
2. 手动更新：`cd ~/.claude-code-docs && git pull`
3. 检查 GitHub Actions 状态

### 安装错误
- “git/jq/curl not found”：先安装缺失工具
- “Failed to clone repository”：检查网络
- “Failed to update settings.json”：检查 `~/.claude/settings.json` 权限

## 卸载

完全移除集成：

```bash
/docs uninstall
```

或运行：
```bash
~/.claude-code-docs/uninstall.sh
```
参见 UNINSTALL.md 获取手动卸载说明。

## 安全说明

- 安装器会修改 `~/.claude/settings.json` 以添加自动更新 Hook
- Hook 仅在读取文档时运行 `git pull`
- 所有操作限制在文档目录
- 不会向外发送数据，一切在本地完成
- 仓库信任：通过 HTTPS 从 GitHub 克隆。更高安全性可：
  - Fork 到你的仓库并从自有 Fork 安装
  - 手动克隆并从本地目录执行安装器
  - 安装前审阅脚本

## v0.3.2 更新内容

- 修复自动更新功能
- 改进本地仓库变更处理
- 提升更新过程的错误恢复

## 许可证

文档内容归 Anthropic 所有。

