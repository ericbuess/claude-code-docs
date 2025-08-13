# 子代理

> 在Claude Code中创建和使用专门的AI子代理，用于特定任务的工作流程和改进的上下文管理。

Claude Code中的自定义子代理是专门的AI助手，可以被调用来处理特定类型的任务。它们通过提供具有自定义系统提示、工具和独立上下文窗口的特定任务配置，实现更高效的问题解决。

## 什么是子代理？

子代理是Claude Code可以委托任务的预配置AI个性。每个子代理：

* 具有特定的目的和专业领域
* 使用与主对话分离的自己的上下文窗口
* 可以配置允许使用的特定工具
* 包含指导其行为的自定义系统提示

当Claude Code遇到与子代理专业知识匹配的任务时，它可以将该任务委托给专门的子代理，该子代理独立工作并返回结果。

## 主要优势

<CardGroup cols={2}>
  <Card title="上下文保护" icon="layer-group">
    每个子代理在自己的上下文中操作，防止主对话的污染，并保持其专注于高级目标。
  </Card>

  <Card title="专业知识" icon="brain">
    子代理可以通过特定领域的详细指令进行微调，在指定任务上获得更高的成功率。
  </Card>

  <Card title="可重用性" icon="rotate">
    一旦创建，子代理可以在不同项目中使用，并与您的团队共享以实现一致的工作流程。
  </Card>

  <Card title="灵活权限" icon="shield-check">
    每个子代理可以有不同的工具访问级别，允许您将强大的工具限制在特定的子代理类型上。
  </Card>
</CardGroup>

## 快速开始

创建您的第一个子代理：

<Steps>
  <Step title="打开子代理界面">
    运行以下命令：

    ```
    /agents
    ```
  </Step>

  <Step title="选择'创建新代理'">
    选择是创建项目级还是用户级子代理
  </Step>

  <Step title="定义子代理">
    * **推荐**：首先用Claude生成，然后自定义使其成为您的
    * 详细描述您的子代理以及何时应该使用它
    * 选择您想要授予访问权限的工具（或留空以继承所有工具）
    * 界面显示所有可用工具，使选择变得容易
    * 如果您正在用Claude生成，您也可以通过按`e`在自己的编辑器中编辑系统提示
  </Step>

  <Step title="保存并使用">
    您的子代理现在可用了！Claude会在适当时自动使用它，或者您可以显式调用它：

    ```
    > 使用代码审查员子代理检查我最近的更改
    ```
  </Step>
</Steps>

## 子代理配置

### 文件位置

子代理存储为带有YAML前言的Markdown文件，位于两个可能的位置：

| 类型        | 位置                  | 范围       | 优先级 |
| :-------- | :------------------ | :------- | :-- |
| **项目子代理** | `.claude/agents/`   | 在当前项目中可用 | 最高  |
| **用户子代理** | `~/.claude/agents/` | 在所有项目中可用 | 较低  |

当子代理名称冲突时，项目级子代理优先于用户级子代理。

### 文件格式

每个子代理在Markdown文件中定义，具有以下结构：

```markdown
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all tools if omitted
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow.
```

#### 配置字段

| 字段            | 必需 | 描述                          |
| :------------ | :- | :-------------------------- |
| `name`        | 是  | 使用小写字母和连字符的唯一标识符            |
| `description` | 是  | 子代理目的的自然语言描述                |
| `tools`       | 否  | 特定工具的逗号分隔列表。如果省略，从主线程继承所有工具 |

### 可用工具

子代理可以被授予访问Claude Code的任何内部工具。请参阅[工具文档](/zh-CN/docs/claude-code/settings#tools-available-to-claude)获取可用工具的完整列表。

<Tip>
  \*\*推荐：\*\*使用`/agents`命令修改工具访问权限 - 它提供了一个交互式界面，列出所有可用工具，包括任何连接的MCP服务器工具，使您更容易选择所需的工具。
</Tip>

您有两个配置工具的选项：

* **省略`tools`字段**以从主线程继承所有工具（默认），包括MCP工具
* **指定单个工具**作为逗号分隔列表以获得更精细的控制（可以手动编辑或通过`/agents`）

**MCP工具**：子代理可以访问来自配置的MCP服务器的MCP工具。当省略`tools`字段时，子代理继承主线程可用的所有MCP工具。

## 管理子代理

### 使用/agents命令（推荐）

`/agents`命令为子代理管理提供了一个全面的界面：

```
/agents
```

这会打开一个交互式菜单，您可以：

* 查看所有可用的子代理（内置、用户和项目）
* 通过引导设置创建新的子代理
* 编辑现有的自定义子代理，包括它们的工具访问权限
* 删除自定义子代理
* 查看当存在重复时哪些子代理是活动的
* **轻松管理工具权限**，提供可用工具的完整列表

### 直接文件管理

您也可以通过直接处理子代理文件来管理它们：

```bash
# 创建项目子代理
mkdir -p .claude/agents
echo '---
name: test-runner
description: Use proactively to run tests and fix failures
---

You are a test automation expert. When you see code changes, proactively run the appropriate tests. If tests fail, analyze the failures and fix them while preserving the original test intent.' > .claude/agents/test-runner.md

# 创建用户子代理
mkdir -p ~/.claude/agents
# ... 创建子代理文件
```

## 有效使用子代理

### 自动委托

Claude Code基于以下内容主动委托任务：

* 您请求中的任务描述
* 子代理配置中的`description`字段
* 当前上下文和可用工具

<Tip>
  为了鼓励更主动的子代理使用，在您的`description`字段中包含"主动使用"或"必须使用"等短语。
</Tip>

### 显式调用

通过在命令中提及特定子代理来请求它：

```
> 使用测试运行器子代理修复失败的测试
> 让代码审查员子代理查看我最近的更改
> 请调试器子代理调查这个错误
```

## 示例子代理

### 代码审查员

```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is simple and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### 调试器

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not just symptoms.
```

### 数据科学家

```markdown
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

## 最佳实践

* **从Claude生成的代理开始**：我们强烈建议用Claude生成您的初始子代理，然后对其进行迭代以使其成为您个人的。这种方法为您提供最佳结果 - 一个您可以根据特定需求自定义的坚实基础。

* **设计专注的子代理**：创建具有单一、明确职责的子代理，而不是试图让一个子代理做所有事情。这提高了性能并使子代理更可预测。

* **编写详细的提示**：在系统提示中包含具体指令、示例和约束。您提供的指导越多，子代理的表现就越好。

* **限制工具访问**：只授予子代理目的所必需的工具。这提高了安全性并帮助子代理专注于相关操作。

* **版本控制**：将项目子代理检入版本控制，这样您的团队就可以从中受益并协作改进它们。

## 高级用法

### 链接子代理

对于复杂的工作流程，您可以链接多个子代理：

```
> 首先使用代码分析器子代理找到性能问题，然后使用优化器子代理修复它们
```

### 动态子代理选择

Claude Code基于上下文智能选择子代理。使您的`description`字段具体且面向行动，以获得最佳结果。

## 性能考虑

* **上下文效率**：代理帮助保护主上下文，实现更长的整体会话
* **延迟**：子代理每次被调用时都从干净的状态开始，可能会增加延迟，因为它们需要收集有效完成工作所需的上下文。

## 相关文档

* [斜杠命令](/zh-CN/docs/claude-code/slash-commands) - 了解其他内置命令
* [设置](/zh-CN/docs/claude-code/settings) - 配置Claude Code行为
* [钩子](/zh-CN/docs/claude-code/hooks) - 使用事件处理程序自动化工作流程
