# Claude Code SDK（开发包）

> 使用 Claude Code SDK 构建自定义 AI 智能体。

## 为什么使用 SDK？

- 深度优化的 Claude 集成（含提示缓存与性能优化）
- 丰富的工具生态：文件操作、命令执行、网页搜索、MCP 可扩展
- 细粒度权限控制
- 生产必备：错误处理、会话管理、监控

## 能构建哪些智能体

- 编码类：SRE 故障排查、代码安全审计、Oncall 助手、代码评审机器人
- 业务类：法务审阅、财务分析、客服助手、内容创作

提供 TypeScript 与 Python，以及命令行原型入口。

## 快速开始

- 安装：NPM / PyPI
- 设置 API Key：`ANTHROPIC_API_KEY`
- 创建示例智能体：命令行、TS、Python 示例均可 5 分钟内运行

## 核心用法

- 命令行：`claude -p` 非交互模式，支持 `--output-format`/`--allowedTools`/`--permission-mode`/`--cwd` 等
- TypeScript：`query()` 返回异步迭代器流式消息
- Python：`ClaudeSDKClient`（推荐）与 `query()` 两种接口，支持流式、图片引用、连续消息

## 认证

- 直连 Anthropic：设置 `ANTHROPIC_API_KEY`
- 三方：Bedrock（`CLAUDE_CODE_USE_BEDROCK=1`）、Vertex（`CLAUDE_CODE_USE_VERTEX=1`）并配置相应云端凭据

## 多轮会话

- 继续最近会话：`--continue` 或 SDK 对应选项
- 恢复指定会话：`--resume <session-id>` 或 SDK 对应选项

## 自定义系统提示（System Prompt）

- 定义角色、专业、行为
- 支持在默认系统提示上追加

示例：SRE/法务/开发重构等场景的命令行、TS、Python 片段。


