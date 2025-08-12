# 开始使用 Claude Code 钩子

> 学习如何通过注册 shell 命令来自定义和扩展 Claude Code 的行为

Claude Code 钩子是用户定义的 shell 命令，在 Claude Code 生命周期的各个点执行。钩子提供对 Claude Code 行为的确定性控制，确保某些操作总是发生，而不是依赖 LLM 选择运行它们。

<Tip>
  有关钩子的参考文档，请参阅 [钩子参考](/zh-CN/docs/claude-code/hooks)。
</Tip>

钩子的示例用例包括：

* **通知**：自定义当 Claude Code 等待您的输入或运行某些内容的权限时如何获得通知。
* **自动格式化**：在每次文件编辑后对 .ts 文件运行 `prettier`，对 .go 文件运行 `gofmt` 等。
* **日志记录**：跟踪和计算所有执行的命令以用于合规性或调试。
* **反馈**：当 Claude Code 产生不遵循您的代码库约定的代码时提供自动反馈。
* **自定义权限**：阻止对生产文件或敏感目录的修改。

通过将这些规则编码为钩子而不是提示指令，您将建议转换为应用程序级代码，每次预期运行时都会执行。

<Warning>
  您必须考虑添加钩子时的安全影响，因为钩子在代理循环期间使用您当前环境的凭据自动运行。
  例如，恶意钩子代码可以泄露您的数据。在注册钩子之前，请始终检查您的钩子实现。

  有关完整的安全最佳实践，请参阅钩子参考文档中的 [安全注意事项](/zh-CN/docs/claude-code/hooks#security-considerations)。
</Warning>

## 钩子事件概述

Claude Code 提供了几个在工作流程不同点运行的钩子事件：

* **PreToolUse**：在工具调用之前运行（可以阻止它们）
* **PostToolUse**：在工具调用完成后运行
* **Notification**：当 Claude Code 发送通知时运行
* **Stop**：当 Claude Code 完成响应时运行
* **Subagent Stop**：当子代理任务完成时运行

每个事件接收不同的数据，并可以以不同的方式控制 Claude 的行为。

## 快速开始

在这个快速开始中，您将添加一个记录 Claude Code 运行的 shell 命令的钩子。

### 先决条件

安装 `jq` 用于命令行中的 JSON 处理。

### 步骤 1：打开钩子配置

运行 `/hooks` [斜杠命令](/zh-CN/docs/claude-code/slash-commands) 并选择 `PreToolUse` 钩子事件。

`PreToolUse` 钩子在工具调用之前运行，可以阻止它们，同时向 Claude 提供关于如何做不同事情的反馈。

### 步骤 2：添加匹配器

选择 `+ Add new matcher…` 以仅在 Bash 工具调用上运行您的钩子。

为匹配器输入 `Bash`。

<Note>您可以使用 `*` 来匹配所有工具。</Note>

### 步骤 3：添加钩子

选择 `+ Add new hook…` 并输入此命令：

```bash
jq -r '"\(.tool_input.command) - \(.tool_input.description // "No description")"' >> ~/.claude/bash-command-log.txt
```

### 步骤 4：保存您的配置

对于存储位置，选择 `User settings`，因为您正在记录到您的主目录。然后此钩子将应用于所有项目，而不仅仅是您当前的项目。

然后按 Esc 直到您返回到 REPL。您的钩子现在已注册！

### 步骤 5：验证您的钩子

再次运行 `/hooks` 或检查 `~/.claude/settings.json` 以查看您的配置：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \"No description\")\"' >> ~/.claude/bash-command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### 步骤 6：测试您的钩子

要求 Claude 运行一个简单的命令，如 `ls` 并检查您的日志文件：

```bash
cat ~/.claude/bash-command-log.txt
```

您应该看到类似这样的条目：

```
ls - Lists files and directories
```

## 更多示例

<Note>
  有关完整的示例实现，请参阅我们公共代码库中的 [bash 命令验证器示例](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)。
</Note>

### 代码格式化钩子

编辑后自动格式化 TypeScript 文件：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -q '\\.ts$'; then npx prettier --write \"$file_path\"; fi; }"
          }
        ]
      }
    ]
  }
}
```

### 自定义通知钩子

当 Claude 需要输入时获得桌面通知：

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting your input'"
          }
        ]
      }
    ]
  }
}
```

### 文件保护钩子

阻止对敏感文件的编辑：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); sys.exit(2 if any(p in path for p in ['.env', 'package-lock.json', '.git/']) else 0)\""
          }
        ]
      }
    ]
  }
}
```

## 了解更多

* 有关钩子的参考文档，请参阅 [钩子参考](/zh-CN/docs/claude-code/hooks)。
* 有关全面的安全最佳实践和安全指南，请参阅钩子参考文档中的 [安全注意事项](/zh-CN/docs/claude-code/hooks#security-considerations)。
* 有关故障排除步骤和调试技术，请参阅钩子参考文档中的 [调试](/zh-CN/docs/claude-code/hooks#debugging)。
