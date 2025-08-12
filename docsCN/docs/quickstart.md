# 快速开始

> 欢迎使用 Claude Code！

本指南将在几分钟内带你上手。结束时你将会知道如何用 Claude Code 完成常见开发任务。

## 开始之前

请确保你已经：

- 打开一个终端或命令行
- 有一个要操作的代码项目

## 步骤 1：安装 Claude Code

### 通过 NPM 安装

如果你已安装 [Node.js 18+](https://nodejs.org/en/download/)：

```sh
npm install -g @anthropic-ai/claude-code
```

### 原生安装（Beta）

<Tip>
  可尝试我们的原生安装（测试中）。
</Tip>

macOS、Linux、WSL：

```bash
curl -fsSL claude.ai/install.sh | bash
```

Windows PowerShell：

```powershell
irm https://claude.ai/install.ps1 | iex
```

## 步骤 2：开启首次会话

在任意项目目录打开终端并启动 Claude：

```bash
cd /path/to/your/project
claude
```

你会看到交互式会话提示：

```
✻ Welcome to Claude Code!
...
> Try "create a util logging.py that..."
```

<Tip>
  凭据会安全地存储在你的系统中。详见 [Credential Management](/en/docs/claude-code/iam#credential-management)。
</Tip>

## 步骤 3：提出第一个问题

先让 Claude 理解你的代码库。尝试：

```
> what does this project do?
```

也可以更具体：

```
> what technologies does this project use?
```

```
> where is the main entry point?
```

```
> explain the folder structure
```

还可询问 Claude 自身能力：

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
  Claude 会按需读取文件，你无需手动提供上下文；它也能访问自身文档以回答相关问题。
</Note>

## 步骤 4：进行首次代码修改

试试一个简单任务：

```
> add a hello world function to the main file
```

Claude 将：
1. 找到合适文件
2. 展示拟修改内容
3. 征求你的批准
4. 执行编辑

<Note>
  修改文件前 Claude 总会征求你的同意。你可以逐项批准，也可开启“全部允许”模式。
</Note>

## 步骤 5：配合 Git 使用

与 Git 的常见对话式操作：

```
> what files have I changed?
```

```
> commit my changes with a descriptive message
```

更多示例：

```
> create a new branch called feature/quickstart
```

```
> show me the last 5 commits
```

```
> help me resolve merge conflicts
```

## 步骤 6：修 Bug 或加功能

用自然语言描述你的需求：

```
> add input validation to the user registration form
```

或修复现有问题：

```
> there's a bug where users can submit empty forms - fix it
```

Claude 将定位相关代码、理解上下文、实现方案并在有测试时运行测试。

## 步骤 7：探索其他常见工作流

- 重构代码：`> refactor the authentication module ...`
- 写测试：`> write unit tests for ...`
- 更新文档：`> update the README ...`
- 代码评审：`> review my changes ...`

<Tip>
  把 Claude 当作结对程序员，像同事一样自然交流。
</Tip>

## 常用命令

| 命令                | 功能                         | 示例                                 |
| ------------------- | ---------------------------- | ------------------------------------ |
| `claude`            | 启动交互模式                 | `claude`                             |
| `claude "task"`     | 运行一次性任务               | `claude "fix the build error"`      |
| `claude -p "query"` | 一次性查询后退出             | `claude -p "explain this function"` |
| `claude -c`         | 继续最近一次会话             | `claude -c`                          |
| `claude -r`         | 恢复历史会话                 | `claude -r`                          |
| `claude commit`     | 创建 Git 提交                | `claude commit`                      |
| `/clear`            | 清空会话历史                 | `> /clear`                           |
| `/help`             | 显示可用命令                 | `> /help`                            |
| `exit` 或 Ctrl+C    | 退出 Claude Code             | `> exit`                             |

更多命令参见 [CLI 参考](/en/docs/claude-code/cli-reference)。

## 新手小贴士

- 具体描述需求，避免“修一下 Bug”这类笼统请求
- 把复杂任务拆分成步骤
- 在改动前先让 Claude 探索理解代码
- 善用快捷键：Tab 自动补全、↑ 历史、`/` 查看斜杠命令

## 接下来做什么？

<CardGroup cols={3}>
  <Card title="常见工作流" icon="graduation-cap" href="/en/docs/claude-code/common-workflows">
    常见任务的分步指南
  </Card>
  <Card title="CLI 参考" icon="terminal" href="/en/docs/claude-code/cli-reference">
    掌握所有命令与选项
  </Card>
  <Card title="配置" icon="gear" href="/en/docs/claude-code/settings">
    根据你的工作流自定义
  </Card>
</CardGroup>

## 寻求帮助

- 在 Claude 中输入 `/help` 或直接提问
- 你现在就在文档里，浏览其它指南即可
- 社区：加入我们的 Discord 获取技巧与支持

