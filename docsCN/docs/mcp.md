# 通过 MCP 连接工具

> 使用 Model Context Protocol（MCP）将 Claude Code 连接到你的工具、数据库与 API。

Claude Code 可通过 MCP 连接上百个外部工具与数据源。下面概述了可做什么、如何安装与管理 MCP 服务器、作用域与共享、认证、资源与提示（prompts）等。

## 能做什么

连接后你可以让 Claude：
- 从问题跟踪系统实施功能并创建 PR
- 分析监控数据（如 Sentry/Statsig）
- 查询数据库（如 Postgres）
- 基于 Figma 设计更新模板
- 自动化工作流（如草拟邮件邀请用户反馈）

## 安装与管理 MCP 服务器

- 本地 stdio：适合需要本机访问或自定义脚本的工具
- 远程 SSE：常见于云服务的实时流式连接
- 远程 HTTP：标准请求/响应模式

常用命令：
```bash
# 添加本地服务器
claude mcp add <name> <command> [args...]

# 添加 SSE 服务器
claude mcp add --transport sse <name> <url>

# 添加 HTTP 服务器
claude mcp add --transport http <name> <url>

# 列出/查看/移除
claude mcp list
claude mcp get <name>
claude mcp remove <name>

# 会话内检查状态
> /mcp
```

Windows 原生环境下，使用 `npx` 的本地服务器需 `cmd /c` 包裹，否则会因无法直接执行 `npx` 而断开。

## 作用域与共享（Scopes）

- local（默认）：仅你在当前项目可用
- project：写入项目根目录 `.mcp.json`，可随仓库共享给团队
- user：对你本机的所有项目可用

`.mcp.json` 支持环境变量展开（`${VAR}`/`${VAR:-default}`）以便跨机器共享。多作用域同名服务器优先级：local > project > user。

## 认证与 JSON 导入

- 许多云端服务器需要 OAuth2 认证：先添加服务器，再在会话内运行 `/mcp` 完成浏览器登录；令牌安全存储且自动刷新。
- 也可通过 `claude mcp add-json <name> '<json>'` 直接导入 JSON 配置。
- 可从 Claude Desktop 导入已配置的 MCP 服务器：`claude mcp add-from-claude-desktop`。

## 作为 MCP 服务器使用 Claude Code

你也可以让 Claude Code 自身作为 MCP 服务器：
```bash
claude mcp serve
```
在 Claude Desktop 中将其加入配置即可使用（提供 View/Edit/LS 等工具）。

## 使用 MCP 资源与提示

- 资源引用：在输入中使用 `@server:protocol://resource/path`，引用时会自动读取并附加。
- 多资源可在同一条消息中引用。
- MCP 暴露的提示会注册为斜杠命令，形式为 `/mcp__servername__promptname`，可带参数执行。

## 安全提示

第三方 MCP 服务器的正确性与安全性未由 Anthropic 全量验证。安装前请确认来源可信，谨防能抓取不受信内容的服务器引入提示注入风险。

