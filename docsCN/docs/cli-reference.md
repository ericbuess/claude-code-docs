# CLI 参考

> Claude Code 命令行的完整参考：命令与参数。

## 常用命令

| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `claude` | 启动交互式 REPL | `claude` |
| `claude "query"` | 启动 REPL 并以该提示开场 | `claude "explain this project"` |
| `claude -p "query"` | 以 SDK 模式打印响应后退出 | `claude -p "explain this function"` |
| `cat file \| claude -p "query"` | 通过管道传递内容 | `cat logs.txt \| claude -p "explain"` |
| `claude -c` | 继续最近会话 | `claude -c` |
| `claude -c -p "query"` | 以 SDK 模式继续 | `claude -c -p "Check for type errors"` |
| `claude -r "<session-id>" "query"` | 按 ID 恢复会话 | `claude -r "abc123" "Finish this PR"` |
| `claude update` | 更新到最新版本 | `claude update` |
| `claude mcp` | 配置 MCP 服务器 | 参见 MCP 文档 |

## 常用参数（节选）

- `--add-dir`：添加额外可访问目录
- `--allowedTools` / `--disallowedTools`：额外允许/禁止的工具
- `--print, -p`：打印模式（详见 SDK 文档）
- `--output-format`：输出格式（text/json/stream-json）
- `--input-format`：输入格式（text/stream-json）
- `--verbose`：详细日志
- `--max-turns`：非交互模式下最大回合数
- `--model`：指定模型或别名
- `--permission-mode`：指定权限模式
- `--resume` / `--continue`：恢复历史会话
- `--dangerously-skip-permissions`：跳过权限确认（谨慎使用）

更多细节与示例参见 SDK 文档与相关页面：
- 交互模式
- 斜杠命令
- 快速开始
- 常见工作流
- 设置
- SDK 文档

