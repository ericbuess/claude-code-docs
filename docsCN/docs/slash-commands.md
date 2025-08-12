# 斜杠命令（Slash commands）

> 在交互会话中使用斜杠命令控制 Claude 的行为。

## 内置命令

- /add-dir：添加额外工作目录
- /agents：管理自定义子智能体
- /bug：上报问题（会话发送给 Anthropic）
- /clear：清空会话历史
- /compact [指令]：压缩会话（可附聚焦指令）
- /config：查看/修改配置
- /cost：显示 token 用量
- /doctor：检查安装健康
- /help：帮助
- /init：初始化项目 CLAUDE.md
- /login：切换 Anthropic 账号
- /logout：登出
- /mcp：管理 MCP 服务器与 OAuth 认证
- /memory：编辑 CLAUDE.md 记忆文件
- /model：选择/切换模型
- /permissions：查看/更新权限
- /pr_comments：查看 PR 评论
- /review：请求代码评审
- /status：查看账号与系统状态
- /terminal-setup：为 iTerm2/VS Code 配置 Shift+Enter
- /vim：进入 Vim 模式

## 自定义命令

- 项目命令：`.claude/commands/`（在 /help 中标注为 (project)）
- 个人命令：`~/.claude/commands/`（在 /help 中标注为 (user)）
- 命令名由 Markdown 文件名决定；支持子目录命名空间；支持 `$ARGUMENTS` 作为参数占位
- 可在 frontmatter 中声明 allowed-tools、argument-hint、description、model 等元信息
- 支持在命令中：
  - 使用 `!` 前缀执行 Bash 并将输出纳入上下文（需在 allowed-tools 中允许具体 bash 命令）
  - 使用 `@` 引用文件内容
  - 触发扩展思考关键字

示例（Bash 输出纳入上下文）：
```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---
- Current git status: !`git status`
```

## MCP 斜杠命令

连接的 MCP 服务器可暴露提示为斜杠命令，格式：
```
/mcp__<server>__<prompt> [args]
```
支持动态发现、参数传递、名称规范化（空格与特殊字符转下划线）。使用 `/mcp` 查看/认证/清除等。

