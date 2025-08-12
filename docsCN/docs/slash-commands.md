# 斜杠命令

> 在交互式会话中使用斜杠命令控制 Claude 的行为。

## 内置斜杠命令

| 命令                        | 用途                                                             |
| :------------------------ | :------------------------------------------------------------- |
| `/add-dir`                | 添加额外的工作目录                                                      |
| `/agents`                 | 管理用于专门任务的自定义 AI 子代理                                            |
| `/bug`                    | 报告错误（将对话发送给 Anthropic）                                         |
| `/clear`                  | 清除对话历史                                                         |
| `/compact [instructions]` | 压缩对话，可选择性地提供重点指令                                               |
| `/config`                 | 查看/修改配置                                                        |
| `/cost`                   | 显示令牌使用统计                                                       |
| `/doctor`                 | 检查您的 Claude Code 安装的健康状况                                       |
| `/help`                   | 获取使用帮助                                                         |
| `/init`                   | 使用 CLAUDE.md 指南初始化项目                                           |
| `/login`                  | 切换 Anthropic 账户                                                |
| `/logout`                 | 从您的 Anthropic 账户登出                                             |
| `/mcp`                    | 管理 MCP 服务器连接和 OAuth 身份验证                                       |
| `/memory`                 | 编辑 CLAUDE.md 内存文件                                              |
| `/model`                  | 选择或更改 AI 模型                                                    |
| `/permissions`            | 查看或更新[权限](/zh-CN/docs/claude-code/iam#configuring-permissions) |
| `/pr_comments`            | 查看拉取请求评论                                                       |
| `/review`                 | 请求代码审查                                                         |
| `/status`                 | 查看账户和系统状态                                                      |
| `/terminal-setup`         | 安装 Shift+Enter 键绑定用于换行（仅限 iTerm2 和 VSCode）                     |
| `/vim`                    | 进入 vim 模式，在插入模式和命令模式之间切换                                       |

## 自定义斜杠命令

自定义斜杠命令允许您将常用提示定义为 Markdown 文件，Claude Code 可以执行这些文件。命令按作用域（项目特定或个人）组织，并通过目录结构支持命名空间。

### 语法

```
/<command-name> [arguments]
```

#### 参数

| 参数               | 描述                                 |
| :--------------- | :--------------------------------- |
| `<command-name>` | 从 Markdown 文件名派生的名称（不包括 `.md` 扩展名） |
| `[arguments]`    | 传递给命令的可选参数                         |

### 命令类型

#### 项目命令

存储在您的仓库中并与您的团队共享的命令。在 `/help` 中列出时，这些命令在其描述后显示"(project)"。

**位置**：`.claude/commands/`

在以下示例中，我们创建 `/optimize` 命令：

```bash
# 创建项目命令
mkdir -p .claude/commands
echo "分析此代码的性能问题并建议优化：" > .claude/commands/optimize.md
```

#### 个人命令

在您所有项目中可用的命令。在 `/help` 中列出时，这些命令在其描述后显示"(user)"。

**位置**：`~/.claude/commands/`

在以下示例中，我们创建 `/security-review` 命令：

```bash
# 创建个人命令
mkdir -p ~/.claude/commands
echo "审查此代码的安全漏洞：" > ~/.claude/commands/security-review.md
```

### 功能

#### 命名空间

在子目录中组织命令。子目录决定命令的完整名称。描述将显示命令是来自项目目录（`.claude/commands`）还是用户级目录（`~/.claude/commands`）。

不支持用户级和项目级命令之间的冲突。否则，具有相同基本文件名的多个命令可以共存。

例如，`.claude/commands/frontend/component.md` 处的文件创建命令 `/frontend:component`，描述显示"(project)"。
同时，`~/.claude/commands/component.md` 处的文件创建命令 `/component`，描述显示"(user)"。

#### 参数

使用 `$ARGUMENTS` 占位符将动态值传递给命令。

例如：

```bash
# 命令定义
echo '按照我们的编码标准修复问题 #$ARGUMENTS' > .claude/commands/fix-issue.md

# 使用
> /fix-issue 123
```

#### Bash 命令执行

使用 `!` 前缀在斜杠命令运行之前执行 bash 命令。输出包含在命令上下文中。您\_必须\_包含带有 `Bash` 工具的 `allowed-tools`，但您可以选择允许的特定 bash 命令。

例如：

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: 创建 git 提交
---

## 上下文

- 当前 git 状态：!`git status`
- 当前 git 差异（已暂存和未暂存的更改）：!`git diff HEAD`
- 当前分支：!`git branch --show-current`
- 最近的提交：!`git log --oneline -10`

## 您的任务

基于上述更改，创建一个 git 提交。
```

#### 文件引用

使用 `@` 前缀在命令中包含文件内容以[引用文件](/zh-CN/docs/claude-code/common-workflows#reference-files-and-directories)。

例如：

```markdown
# 引用特定文件

审查 @src/utils/helpers.js 中的实现

# 引用多个文件

比较 @src/old-version.js 与 @src/new-version.js
```

#### 思考模式

斜杠命令可以通过包含[扩展思考关键词](/zh-CN/docs/claude-code/common-workflows#use-extended-thinking)来触发扩展思考。

### 前置元数据

命令文件支持前置元数据，对于指定命令的元数据很有用：

| 前置元数据           | 用途                                                                                        | 默认值      |
| :-------------- | :---------------------------------------------------------------------------------------- | :------- |
| `allowed-tools` | 命令可以使用的工具列表                                                                               | 从对话中继承   |
| `argument-hint` | 斜杠命令预期的参数。示例：`argument-hint: add [tagId] \| remove [tagId] \| list`。此提示在用户自动完成斜杠命令时显示给用户。 | 无        |
| `description`   | 命令的简要描述                                                                                   | 使用提示的第一行 |
| `model`         | 特定模型字符串（参见[模型概述](/zh-CN/docs/about-claude/models/overview)）                               | 从对话中继承   |

例如：

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: [message]
description: 创建 git 提交
model: claude-3-5-haiku-20241022
---

示例命令
```

## MCP 斜杠命令

MCP 服务器可以将提示作为斜杠命令公开，这些命令在 Claude Code 中变得可用。这些命令从连接的 MCP 服务器动态发现。

### 命令格式

MCP 命令遵循以下模式：

```
/mcp__<server-name>__<prompt-name> [arguments]
```

### 功能

#### 动态发现

MCP 命令在以下情况下自动可用：

* MCP 服务器已连接并处于活动状态
* 服务器通过 MCP 协议公开提示
* 在连接期间成功检索提示

#### 参数

MCP 提示可以接受服务器定义的参数：

```
# 不带参数
> /mcp__github__list_prs

# 带参数
> /mcp__github__pr_review 456
> /mcp__jira__create_issue "Bug title" high
```

#### 命名约定

* 服务器和提示名称被标准化
* 空格和特殊字符变成下划线
* 名称小写以保持一致性

### 管理 MCP 连接

使用 `/mcp` 命令来：

* 查看所有配置的 MCP 服务器
* 检查连接状态
* 使用启用 OAuth 的服务器进行身份验证
* 清除身份验证令牌
* 查看每个服务器的可用工具和提示

## 另请参阅

* [交互模式](/zh-CN/docs/claude-code/interactive-mode) - 快捷键、输入模式和交互功能
* [CLI 参考](/zh-CN/docs/claude-code/cli-reference) - 命令行标志和选项
* [设置](/zh-CN/docs/claude-code/settings) - 配置选项
* [内存管理](/zh-CN/docs/claude-code/memory) - 跨会话管理 Claude 的内存
