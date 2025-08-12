# 子智能体（Subagents）

> 在 Claude Code 中创建和使用专用 AI 子智能体，以适配特定任务并改进上下文管理。

子智能体是具备独立上下文窗口、可配置工具权限与系统提示的专用助手。Claude 可在合适场景自动委派，或由你显式调用。

## 关键优势

- 上下文隔离：保持主会话聚焦
- 专业化：为领域任务提供更高命中率
- 可复用：项目/用户级共享
- 灵活权限：按子智能体粒度授予工具

## 快速开始

使用 `/agents` 打开界面，创建项目级或用户级子智能体，填写描述、选择工具（可留空继承全部），保存后可显式调用例如：`Use the code-reviewer subagent ...`。

## 存储位置与格式

- 项目：`.claude/agents/`
- 用户：`~/.claude/agents/`

以 Markdown+YAML frontmatter 定义 name/description/tools 与系统提示正文；同名时项目优先于用户。

## 工具与权限

- 省略 tools 字段则继承主线程全部工具（含 MCP）
- 或列出具体工具实现精细控制
- 推荐用 `/agents` 交互式编辑

## 管理与使用

- `/agents` 提供查看/创建/编辑/删除/冲突解析与工具权限管理
- 自动委派基于请求描述、子智能体 description 与当前上下文；可显式点名调用

## 示例

- code-reviewer：关注质量/安全/可维护性；工具：Read/Grep/Glob/Bash
- debugger：根因分析/最小修复；工具：Read/Edit/Bash/Grep/Glob
- data-scientist：SQL/BigQuery 分析；工具：Bash/Read/Write

## 最佳实践

- 先由 Claude 生成再个性化
- 单一职责、详细提示、最小必要权限
- 项目子智能体纳入版本控制

## 性能注意

- 独立上下文有助于延长主会话可用上下文
- 首次唤起需收集必要上下文，可能增加时延

## 参阅

- 斜杠命令、设置、Hooks 文档
