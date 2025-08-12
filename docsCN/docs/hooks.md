# 钩子参考

> 本页面提供了在 Claude Code 中实现钩子的参考文档。

<Tip>
  有关带示例的快速入门指南，请参阅[Claude Code 钩子入门](/zh-CN/docs/claude-code/hooks-guide)。
</Tip>

## 配置

Claude Code 钩子在您的[设置文件](/zh-CN/docs/claude-code/settings)中配置：

* `~/.claude/settings.json` - 用户设置
* `.claude/settings.json` - 项目设置
* `.claude/settings.local.json` - 本地项目设置（不提交）
* 企业管理策略设置

### 结构

钩子按匹配器组织，每个匹配器可以有多个钩子：

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

* **matcher**：匹配工具名称的模式，区分大小写（仅适用于 `PreToolUse` 和 `PostToolUse`）
  * 简单字符串精确匹配：`Write` 仅匹配 Write 工具
  * 支持正则表达式：`Edit|Write` 或 `Notebook.*`
  * 使用 `*` 匹配所有工具。您也可以使用空字符串（`""`）或将 `matcher` 留空。
* **hooks**：当模式匹配时要执行的命令数组
  * `type`：目前仅支持 `"command"`
  * `command`：要执行的 bash 命令（可以使用 `$CLAUDE_PROJECT_DIR` 环境变量）
  * `timeout`：（可选）命令应运行多长时间（以秒为单位），超时后取消该特定命令。

对于像 `UserPromptSubmit`、`Notification`、`Stop` 和 `SubagentStop` 这样不使用匹配器的事件，您可以省略匹配器字段：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/prompt-validator.py"
          }
        ]
      }
    ]
  }
}
```

### 项目特定的钩子脚本

您可以使用环境变量 `CLAUDE_PROJECT_DIR`（仅在 Claude Code 生成钩子命令时可用）来引用存储在项目中的脚本，确保无论 Claude 的当前目录如何，它们都能正常工作：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/check-style.sh"
          }
        ]
      }
    ]
  }
}
```

## 钩子事件

### PreToolUse

在 Claude 创建工具参数之后、处理工具调用之前运行。

**常见匹配器：**

* `Task` - 子代理任务（参见[子代理文档](/zh-CN/docs/claude-code/sub-agents)）
* `Bash` - Shell 命令
* `Glob` - 文件模式匹配
* `Grep` - 内容搜索
* `Read` - 文件读取
* `Edit`、`MultiEdit` - 文件编辑
* `Write` - 文件写入
* `WebFetch`、`WebSearch` - Web 操作

### PostToolUse

在工具成功完成后立即运行。

识别与 PreToolUse 相同的匹配器值。

### Notification

当 Claude Code 发送通知时运行。通知在以下情况下发送：

1. Claude 需要您的权限来使用工具。例如："Claude 需要您的权限来使用 Bash"
2. 提示输入已空闲至少 60 秒。"Claude 正在等待您的输入"

### UserPromptSubmit

当用户提交提示时、Claude 处理之前运行。这允许您根据提示/对话添加额外的上下文、验证提示或阻止某些类型的提示。

### Stop

当主 Claude Code 代理完成响应时运行。如果停止是由于用户中断而发生的，则不会运行。

### SubagentStop

当 Claude Code 子代理（Task 工具调用）完成响应时运行。

### PreCompact

在 Claude Code 即将运行压缩操作之前运行。

**匹配器：**

* `manual` - 从 `/compact` 调用
* `auto` - 从自动压缩调用（由于上下文窗口已满）

### SessionStart

当 Claude Code 启动新会话或恢复现有会话时运行（目前确实会在底层启动新会话）。对于加载开发上下文（如现有问题或代码库的最近更改）很有用。

**匹配器：**

* `startup` - 从启动调用
* `resume` - 从 `--resume`、`--continue` 或 `/resume` 调用
* `clear` - 从 `/clear` 调用

## 钩子输入

钩子通过 stdin 接收包含会话信息和事件特定数据的 JSON 数据：

```typescript
{
  // 公共字段
  session_id: string
  transcript_path: string  // 对话 JSON 的路径
  cwd: string              // 调用钩子时的当前工作目录

  // 事件特定字段
  hook_event_name: string
  ...
}
```

### PreToolUse 输入

`tool_input` 的确切模式取决于工具。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

### PostToolUse 输入

`tool_input` 和 `tool_response` 的确切模式取决于工具。

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  }
}
```

### Notification 输入

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Task completed successfully"
}
```

### UserPromptSubmit 输入

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

### Stop 和 SubagentStop 输入

当 Claude Code 已经因为停止钩子而继续时，`stop_hook_active` 为 true。检查此值或处理记录以防止 Claude Code 无限运行。

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

### PreCompact 输入

对于 `manual`，`custom_instructions` 来自用户传递给 `/compact` 的内容。对于 `auto`，`custom_instructions` 为空。

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### SessionStart 输入

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "hook_event_name": "SessionStart",
  "source": "startup"
}
```

## 钩子输出

钩子有两种方式将输出返回给 Claude Code。输出传达是否阻止以及应该向 Claude 和用户显示的任何反馈。

### 简单：退出代码

钩子通过退出代码、stdout 和 stderr 传达状态：

* **退出代码 0**：成功。`stdout` 在记录模式（CTRL-R）中向用户显示，除了 `UserPromptSubmit` 和 `SessionStart`，其中 stdout 被添加到上下文中。
* **退出代码 2**：阻塞错误。`stderr` 被反馈给 Claude 自动处理。请参阅下面的每个钩子事件行为。
* **其他退出代码**：非阻塞错误。`stderr` 向用户显示，执行继续。

<Warning>
  提醒：如果退出代码为 0，Claude Code 不会看到 stdout，除了 `UserPromptSubmit` 钩子，其中 stdout 被注入为上下文。
</Warning>

#### 退出代码 2 行为

| 钩子事件               | 行为                         |
| ------------------ | -------------------------- |
| `PreToolUse`       | 阻止工具调用，向 Claude 显示 stderr  |
| `PostToolUse`      | 向 Claude 显示 stderr（工具已运行）  |
| `Notification`     | 不适用，仅向用户显示 stderr          |
| `UserPromptSubmit` | 阻止提示处理，擦除提示，仅向用户显示 stderr  |
| `Stop`             | 阻止停止，向 Claude 显示 stderr    |
| `SubagentStop`     | 阻止停止，向 Claude 子代理显示 stderr |
| `PreCompact`       | 不适用，仅向用户显示 stderr          |
| `SessionStart`     | 不适用，仅向用户显示 stderr          |

### 高级：JSON 输出

钩子可以在 `stdout` 中返回结构化 JSON 以获得更复杂的控制：

#### 通用 JSON 字段

所有钩子类型都可以包含这些可选字段：

```json
{
  "continue": true, // Claude 是否应在钩子执行后继续（默认：true）
  "stopReason": "string" // 当 continue 为 false 时显示的消息
  "suppressOutput": true, // 在记录模式中隐藏 stdout（默认：false）
}
```

如果 `continue` 为 false，Claude 在钩子运行后停止处理。

* 对于 `PreToolUse`，这与 `"permissionDecision": "deny"` 不同，后者只阻止特定的工具调用并向 Claude 提供自动反馈。
* 对于 `PostToolUse`，这与 `"decision": "block"` 不同，后者向 Claude 提供自动反馈。
* 对于 `UserPromptSubmit`，这防止提示被处理。
* 对于 `Stop` 和 `SubagentStop`，这优先于任何 `"decision": "block"` 输出。
* 在所有情况下，`"continue" = false` 优先于任何 `"decision": "block"` 输出。

`stopReason` 伴随 `continue` 提供向用户显示的原因，不向 Claude 显示。

#### `PreToolUse` 决策控制

`PreToolUse` 钩子可以控制工具调用是否继续。

* `"allow"` 绕过权限系统。`permissionDecisionReason` 向用户显示但不向 Claude 显示。（*已弃用的 `"approve"` 值 + `reason` 具有相同行为。*）
* `"deny"` 防止工具调用执行。`permissionDecisionReason` 向 Claude 显示。（*`"block"` 值 + `reason` 具有相同行为。*）
* `"ask"` 要求用户在 UI 中确认工具调用。`permissionDecisionReason` 向用户显示但不向 Claude 显示。

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow" | "deny" | "ask",
    "permissionDecisionReason": "My reason here (shown to user)"
  },
  "decision": "approve" | "block" | undefined, // 对 PreToolUse 已弃用但仍支持
  "reason": "Explanation for decision" // 对 PreToolUse 已弃用但仍支持
}
```

#### `PostToolUse` 决策控制

`PostToolUse` 钩子可以控制工具调用是否继续。

* `"block"` 自动用 `reason` 提示 Claude。
* `undefined` 什么都不做。`reason` 被忽略。

```json
{
  "decision": "block" | undefined,
  "reason": "Explanation for decision"
}
```

#### `UserPromptSubmit` 决策控制

`UserPromptSubmit` 钩子可以控制用户提示是否被处理。

* `"block"` 防止提示被处理。提交的提示从上下文中擦除。`"reason"` 向用户显示但不添加到上下文中。
* `undefined` 允许提示正常进行。`"reason"` 被忽略。
* `"hookSpecificOutput.additionalContext"` 如果未被阻止，将字符串添加到上下文中。

```json
{
  "decision": "block" | undefined,
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

#### `Stop`/`SubagentStop` 决策控制

`Stop` 和 `SubagentStop` 钩子可以控制 Claude 是否必须继续。

* `"block"` 防止 Claude 停止。您必须填充 `reason` 让 Claude 知道如何继续。
* `undefined` 允许 Claude 停止。`reason` 被忽略。

```json
{
  "decision": "block" | undefined,
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

#### `SessionStart` 决策控制

`SessionStart` 钩子允许您在会话开始时加载上下文。

* `"hookSpecificOutput.additionalContext"` 将字符串添加到上下文中。

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

#### 退出代码示例：Bash 命令验证

```python
#!/usr/bin/env python3
import json
import re
import sys

# 将验证规则定义为（正则表达式模式，消息）元组列表
VALIDATION_RULES = [
    (
        r"\bgrep\b(?!.*\|)",
        "Use 'rg' (ripgrep) instead of 'grep' for better performance and features",
    ),
    (
        r"\bfind\s+\S+\s+-name\b",
        "Use 'rg --files | rg pattern' or 'rg --files -g pattern' instead of 'find -name' for better performance",
    ),
]


def validate_command(command: str) -> list[str]:
    issues = []
    for pattern, message in VALIDATION_RULES:
        if re.search(pattern, command):
            issues.append(message)
    return issues


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
command = tool_input.get("command", "")

if tool_name != "Bash" or not command:
    sys.exit(1)

# 验证命令
issues = validate_command(command)

if issues:
    for message in issues:
        print(f"• {message}", file=sys.stderr)
    # 退出代码 2 阻止工具调用并向 Claude 显示 stderr
    sys.exit(2)
```

#### JSON 输出示例：UserPromptSubmit 添加上下文和验证

<Note>
  对于 `UserPromptSubmit` 钩子，您可以使用任一方法注入上下文：

  * 退出代码 0 与 stdout：Claude 看到上下文（`UserPromptSubmit` 的特殊情况）
  * JSON 输出：提供对行为的更多控制
</Note>

```python
#!/usr/bin/env python3
import json
import sys
import re
import datetime

# 从 stdin 加载输入
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

prompt = input_data.get("prompt", "")

# 检查敏感模式
sensitive_patterns = [
    (r"(?i)\b(password|secret|key|token)\s*[:=]", "Prompt contains potential secrets"),
]

for pattern, message in sensitive_patterns:
    if re.search(pattern, prompt):
        # 使用 JSON 输出以特定原因阻止
        output = {
            "decision": "block",
            "reason": f"Security policy violation: {message}. Please rephrase your request without sensitive information."
        }
        print(json.dumps(output))
        sys.exit(0)

# 将当前时间添加到上下文
context = f"Current time: {datetime.datetime.now()}"
print(context)

"""
以下也是等效的：
print(json.dumps({
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": context,
  },
}))
"""

# 允许提示继续进行，带有额外的上下文
sys.exit(0)
```

#### JSON 输出示例：PreToolUse 与批准

```python
#!/usr/bin/env python3
import json
import sys

# 从 stdin 加载输入
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

# 示例：自动批准文档文件的文件读取
if tool_name == "Read":
    file_path = tool_input.get("file_path", "")
    if file_path.endswith((".md", ".mdx", ".txt", ".json")):
        # 使用 JSON 输出自动批准工具调用
        output = {
            "decision": "approve",
            "reason": "Documentation file auto-approved",
            "suppressOutput": True  # 不在记录模式中显示
        }
        print(json.dumps(output))
        sys.exit(0)

# 对于其他情况，让正常的权限流程继续
sys.exit(0)
```

## 使用 MCP 工具

Claude Code 钩子与[模型上下文协议（MCP）工具](/zh-CN/docs/claude-code/mcp)无缝协作。当 MCP 服务器提供工具时，它们以特殊的命名模式出现，您可以在钩子中匹配。

### MCP 工具命名

MCP 工具遵循模式 `mcp__<server>__<tool>`，例如：

* `mcp__memory__create_entities` - Memory 服务器的创建实体工具
* `mcp__filesystem__read_file` - Filesystem 服务器的读取文件工具
* `mcp__github__search_repositories` - GitHub 服务器的搜索工具

### 为 MCP 工具配置钩子

您可以针对特定的 MCP 工具或整个 MCP 服务器：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

## 示例

<Tip>
  有关包括代码格式化、通知和文件保护在内的实际示例，请参阅入门指南中的[更多示例](/zh-CN/docs/claude-code/hooks-guide#more-examples)。
</Tip>

## 安全考虑

### 免责声明

**使用风险自负**：Claude Code 钩子会在您的系统上自动执行任意 shell 命令。通过使用钩子，您承认：

* 您对配置的命令负全部责任
* 钩子可以修改、删除或访问您的用户帐户可以访问的任何文件
* 恶意或编写不当的钩子可能导致数据丢失或系统损坏
* Anthropic 不提供任何保证，并且对因使用钩子而导致的任何损害不承担任何责任
* 您应该在生产使用之前在安全环境中彻底测试钩子

在将任何钩子命令添加到配置之前，请始终审查和理解它们。

### 安全最佳实践

以下是编写更安全钩子的一些关键实践：

1. **验证和清理输入** - 永远不要盲目信任输入数据
2. **始终引用 shell 变量** - 使用 `"$VAR"` 而不是 `$VAR`
3. **阻止路径遍历** - 检查文件路径中的 `..`
4. **使用绝对路径** - 为脚本指定完整路径（使用 `$CLAUDE_PROJECT_DIR` 作为项目路径）
5. **跳过敏感文件** - 避免 `.env`、`.git/`、密钥等

### 配置安全

对设置文件中钩子的直接编辑不会立即生效。Claude Code：

1. 在启动时捕获钩子的快照
2. 在整个会话中使用此快照
3. 如果钩子被外部修改则发出警告
4. 需要在 `/hooks` 菜单中审查更改才能应用

这防止恶意钩子修改影响您当前的会话。

## 钩子执行详细信息

* **超时**：默认 60 秒执行限制，每个命令可配置。
  * 单个命令的超时不会影响其他命令。
* **并行化**：所有匹配的钩子并行运行
* **环境**：在当前目录中运行，使用 Claude Code 的环境
  * `CLAUDE_PROJECT_DIR` 环境变量可用，包含项目根目录的绝对路径
* **输入**：通过 stdin 的 JSON
* **输出**：
  * PreToolUse/PostToolUse/Stop：在记录中显示进度（Ctrl-R）
  * Notification：仅记录到调试（`--debug`）

## 调试

### 基本故障排除

如果您的钩子不工作：

1. **检查配置** - 运行 `/hooks` 查看您的钩子是否已注册
2. **验证语法** - 确保您的 JSON 设置有效
3. **测试命令** - 首先手动运行钩子命令
4. **检查权限** - 确保脚本可执行
5. **查看日志** - 使用 `claude --debug` 查看钩子执行详细信息

常见问题：

* **引号未转义** - 在 JSON 字符串内使用 `\"`
* **错误的匹配器** - 检查工具名称完全匹配（区分大小写）
* **找不到命令** - 为脚本使用完整路径

### 高级调试

对于复杂的钩子问题：

1. **检查钩子执行** - 使用 `claude --debug` 查看详细的钩子执行
2. **验证 JSON 模式** - 使用外部工具测试钩子输入/输出
3. **检查环境变量** - 验证 Claude Code 的环境是否正确
4. **测试边缘情况** - 尝试使用异常文件路径或输入的钩子
5. **监控系统资源** - 检查钩子执行期间的资源耗尽
6. **使用结构化日志记录** - 在钩子脚本中实现日志记录

### 调试输出示例

使用 `claude --debug` 查看钩子执行详细信息：

```
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 60000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

进度消息出现在记录模式（Ctrl-R）中，显示：

* 哪个钩子正在运行
* 正在执行的命令
* 成功/失败状态
* 输出或错误消息
