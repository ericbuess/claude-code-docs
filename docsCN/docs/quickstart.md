# 快速开始

> 欢迎使用 Claude Code！

这个快速开始指南将让您在几分钟内使用 AI 驱动的编程辅助。完成后，您将了解如何使用 Claude Code 进行常见的开发任务。

## 开始之前

确保您有：

* 打开的终端或命令提示符
* 要使用的代码项目

## 步骤 1：安装 Claude Code

### NPM 安装

如果您已[安装 Node.js 18 或更新版本](https://nodejs.org/en/download/)：

```sh
npm install -g @anthropic-ai/claude-code
```

### 原生安装

<Tip>
  或者，尝试我们新的原生安装，现在处于测试版。
</Tip>

**macOS、Linux、WSL：**

```bash
curl -fsSL claude.ai/install.sh | bash
```

**Windows PowerShell：**

```powershell
irm https://claude.ai/install.ps1 | iex
```

## 步骤 2：开始您的第一个会话

在任何项目目录中打开终端并启动 Claude Code：

```bash
cd /path/to/your/project
claude
```

您将在新的交互式会话中看到 Claude Code 提示符：

```
✻ 欢迎使用 Claude Code！

...

> 尝试 "create a util logging.py that..." 
```

<Tip>
  您的凭据安全地存储在您的系统上。在[凭据管理](/zh-CN/docs/claude-code/iam#credential-management)中了解更多。
</Tip>

## 步骤 3：提出您的第一个问题

让我们从了解您的代码库开始。尝试这些命令之一：

```
> what does this project do?
```

Claude 将分析您的文件并提供摘要。您也可以提出更具体的问题：

```
> what technologies does this project use?
```

```
> where is the main entry point?
```

```
> explain the folder structure
```

您也可以询问 Claude 关于其自身功能的问题：

```
> what can Claude Code do?
```

```
> how do I use slash commands in Claude Code?
```

```
> can Claude Code work with Docker?
```

<Note>
  Claude Code 根据需要读取您的文件 - 您不必手动添加上下文。Claude 还可以访问其自己的文档，并可以回答有关其功能和能力的问题。
</Note>

## 步骤 4：进行您的第一次代码更改

现在让我们让 Claude Code 进行一些实际的编程。尝试一个简单的任务：

```
> add a hello world function to the main file
```

Claude Code 将：

1. 找到适当的文件
2. 向您显示建议的更改
3. 请求您的批准
4. 进行编辑

<Note>
  Claude Code 在修改文件之前总是请求许可。您可以批准单个更改或为会话启用"全部接受"模式。
</Note>

## 步骤 5：在 Claude Code 中使用 Git

Claude Code 使 Git 操作变得对话式：

```
> what files have I changed?
```

```
> commit my changes with a descriptive message
```

您也可以提示更复杂的 Git 操作：

```
> create a new branch called feature/quickstart
```

```
> show me the last 5 commits
```

```
> help me resolve merge conflicts
```

## 步骤 6：修复错误或添加功能

Claude 擅长调试和功能实现。

用自然语言描述您想要的：

```
> add input validation to the user registration form
```

或修复现有问题：

```
> there's a bug where users can submit empty forms - fix it
```

Claude Code 将：

* 定位相关代码
* 理解上下文
* 实施解决方案
* 如果可用，运行测试

## 步骤 7：测试其他常见工作流程

有多种方式与 Claude 协作：

**重构代码**

```
> refactor the authentication module to use async/await instead of callbacks
```

**编写测试**

```
> write unit tests for the calculator functions
```

**更新文档**

```
> update the README with installation instructions
```

**代码审查**

```
> review my changes and suggest improvements
```

<Tip>
  **记住**：Claude Code 是您的 AI 结对编程伙伴。像与有用的同事交谈一样与它交谈 - 描述您想要实现的目标，它将帮助您达到目标。
</Tip>

## 基本命令

以下是日常使用最重要的命令：

| 命令                  | 功能             | 示例                                  |
| ------------------- | -------------- | ----------------------------------- |
| `claude`            | 启动交互模式         | `claude`                            |
| `claude "task"`     | 运行一次性任务        | `claude "fix the build error"`      |
| `claude -p "query"` | 运行一次性查询，然后退出   | `claude -p "explain this function"` |
| `claude -c`         | 继续最近的对话        | `claude -c`                         |
| `claude -r`         | 恢复之前的对话        | `claude -r`                         |
| `claude commit`     | 创建 Git 提交      | `claude commit`                     |
| `/clear`            | 清除对话历史         | `> /clear`                          |
| `/help`             | 显示可用命令         | `> /help`                           |
| `exit` 或 Ctrl+C     | 退出 Claude Code | `> exit`                            |

查看[CLI 参考](/zh-CN/docs/claude-code/cli-reference)获取完整的命令列表。

## 初学者专业提示

<AccordionGroup>
  <Accordion title="对您的请求要具体">
    不要说："fix the bug"

    尝试："fix the login bug where users see a blank screen after entering wrong credentials"
  </Accordion>

  <Accordion title="使用分步说明">
    将复杂任务分解为步骤：

    ```
    > 1. create a new database table for user profiles
    ```

    ```
    > 2. create an API endpoint to get and update user profiles
    ```

    ```
    > 3. build a webpage that allows users to see and edit their information
    ```
  </Accordion>

  <Accordion title="让 Claude 先探索">
    在进行更改之前，让 Claude 了解您的代码：

    ```
    > analyze the database schema
    ```

    ```
    > build a dashboard showing products that are most frequently returned by our UK customers
    ```
  </Accordion>

  <Accordion title="使用快捷方式节省时间">
    * 使用 Tab 进行命令补全
    * 按 ↑ 查看命令历史
    * 输入 `/` 查看所有斜杠命令
  </Accordion>
</AccordionGroup>

## 下一步是什么？

现在您已经学会了基础知识，探索更高级的功能：

<CardGroup cols={3}>
  <Card title="常见工作流程" icon="graduation-cap" href="/zh-CN/docs/claude-code/common-workflows">
    常见任务的分步指南
  </Card>

  <Card title="CLI 参考" icon="terminal" href="/zh-CN/docs/claude-code/cli-reference">
    掌握所有命令和选项
  </Card>

  <Card title="配置" icon="gear" href="/zh-CN/docs/claude-code/settings">
    为您的工作流程自定义 Claude Code
  </Card>
</CardGroup>

## 获取帮助

* **在 Claude Code 中**：输入 `/help` 或询问 "how do I..."
* **文档**：您就在这里！浏览其他指南
* **社区**：加入我们的 [Discord](https://www.anthropic.com/discord) 获取提示和支持
