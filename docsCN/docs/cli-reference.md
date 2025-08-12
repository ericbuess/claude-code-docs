# CLI 参考

> Claude Code 命令行界面的完整参考，包括命令和标志。

## CLI 命令

| 命令                                 | 描述                  | 示例                                                     |
| :--------------------------------- | :------------------ | :----------------------------------------------------- |
| `claude`                           | 启动交互式 REPL          | `claude`                                               |
| `claude "query"`                   | 使用初始提示启动 REPL       | `claude "explain this project"`                        |
| `claude -p "query"`                | 通过 SDK 查询，然后退出      | `claude -p "explain this function"`                    |
| `cat file \| claude -p "query"`    | 处理管道内容              | `cat logs.txt \| claude -p "explain"`                  |
| `claude -c`                        | 继续最近的对话             | `claude -c`                                            |
| `claude -c -p "query"`             | 通过 SDK 继续           | `claude -c -p "Check for type errors"`                 |
| `claude -r "<session-id>" "query"` | 通过 ID 恢复会话          | `claude -r "abc123" "Finish this PR"`                  |
| `claude update`                    | 更新到最新版本             | `claude update`                                        |
| `claude mcp`                       | 配置模型上下文协议 (MCP) 服务器 | 请参阅 [Claude Code MCP 文档](/zh-CN/docs/claude-code/mcp)。 |

## CLI 标志

使用这些命令行标志自定义 Claude Code 的行为：

| 标志                               | 描述                                                                               | 示例                                                          |
| :------------------------------- | :------------------------------------------------------------------------------- | :---------------------------------------------------------- |
| `--add-dir`                      | 添加额外的工作目录供 Claude 访问（验证每个路径是否作为目录存在）                                             | `claude --add-dir ../apps ../lib`                           |
| `--allowedTools`                 | 除了 [settings.json 文件](/zh-CN/docs/claude-code/settings) 之外，应该在不提示用户许可的情况下允许的工具列表 | `"Bash(git log:*)" "Bash(git diff:*)" "Read"`               |
| `--disallowedTools`              | 除了 [settings.json 文件](/zh-CN/docs/claude-code/settings) 之外，应该在不提示用户许可的情况下禁止的工具列表 | `"Bash(git log:*)" "Bash(git diff:*)" "Edit"`               |
| `--print`, `-p`                  | 打印响应而不使用交互模式（有关编程使用详细信息，请参阅 [SDK 文档](/zh-CN/docs/claude-code/sdk)）               | `claude -p "query"`                                         |
| `--output-format`                | 指定打印模式的输出格式（选项：`text`、`json`、`stream-json`）                                      | `claude -p "query" --output-format json`                    |
| `--input-format`                 | 指定打印模式的输入格式（选项：`text`、`stream-json`）                                             | `claude -p --output-format json --input-format stream-json` |
| `--verbose`                      | 启用详细日志记录，显示完整的逐轮输出（在打印和交互模式下都有助于调试）                                              | `claude --verbose`                                          |
| `--max-turns`                    | 限制非交互模式下的代理轮数                                                                    | `claude -p --max-turns 3 "query"`                           |
| `--model`                        | 使用最新模型的别名（`sonnet` 或 `opus`）或模型的全名为当前会话设置模型                                      | `claude --model claude-sonnet-4-20250514`                   |
| `--permission-mode`              | 在指定的 [权限模式](iam#permission-modes) 下开始                                            | `claude --permission-mode plan`                             |
| `--permission-prompt-tool`       | 指定一个 MCP 工具来处理非交互模式下的权限提示                                                        | `claude -p --permission-prompt-tool mcp_auth_tool "query"`  |
| `--resume`                       | 通过 ID 恢复特定会话，或在交互模式下选择                                                           | `claude --resume abc123 "query"`                            |
| `--continue`                     | 在当前目录中加载最近的对话                                                                    | `claude --continue`                                         |
| `--dangerously-skip-permissions` | 跳过权限提示（谨慎使用）                                                                     | `claude --dangerously-skip-permissions`                     |

<Tip>
  `--output-format json` 标志对于脚本编写和自动化特别有用，允许您以编程方式解析 Claude 的响应。
</Tip>

有关打印模式（`-p`）的详细信息，包括输出格式、流式传输、详细日志记录和编程使用，请参阅 [SDK 文档](/zh-CN/docs/claude-code/sdk)。

## 另请参阅

* [交互模式](/zh-CN/docs/claude-code/interactive-mode) - 快捷键、输入模式和交互功能
* [斜杠命令](/zh-CN/docs/claude-code/slash-commands) - 交互会话命令
* [快速入门指南](/zh-CN/docs/claude-code/quickstart) - Claude Code 入门
* [常见工作流程](/zh-CN/docs/claude-code/common-workflows) - 高级工作流程和模式
* [设置](/zh-CN/docs/claude-code/settings) - 配置选项
* [SDK 文档](/zh-CN/docs/claude-code/sdk) - 编程使用和集成
