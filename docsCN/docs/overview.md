# Claude Code 概览

> 了解 Anthropic 的终端内编码智能体 Claude Code：它可以帮助你以前所未有的速度将想法变成代码。

## 30 秒上手

前提条件：[Node.js 18+](https://nodejs.org/en/download/)

```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 切换到你的项目
cd your-awesome-project

# 开始与 Claude 协作编程
claude
```

就这么简单！现在你已经可以开始使用 Claude 了。[继续阅读：快速开始（5 分钟）→](/en/docs/claude-code/quickstart)

（有特殊设置需求或遇到问题？请查看[高级设置](/en/docs/claude-code/setup)或[故障排查](/en/docs/claude-code/troubleshooting)。）

## Claude Code 能为你做什么

- 从描述构建功能：用自然语言描述你要做的事情。Claude 会规划、编写并确保其可用。
- 调试并修复问题：描述 Bug 或粘贴报错。Claude 会分析代码库、定位问题并实施修复。
- 游走任意代码库：向 Claude 提问你的团队代码库的任何问题。它会维护项目结构的全局意识、可从 Web 获取最新信息，并可通过 [MCP](/en/docs/claude-code/mcp) 访问外部数据源（如 Google Drive、Figma、Slack）。
- 自动化繁琐任务：修复 Lint 细节、解决合并冲突、撰写发布说明；既可在本机一条命令完成，也可在 CI 中自动化运行。

## 为什么开发者喜欢 Claude Code

- 终端优先：不是另一个聊天窗口，不是另一个 IDE。Claude Code 在你熟悉的终端与工具中与你相遇。
- 能直接行动：Claude 可直接编辑文件、运行命令并创建提交。需要更多？通过 [MCP](/en/docs/claude-code/mcp) 可读取设计文档、更新 Jira 工单或调用你的自定义工具。
- Unix 哲学：可组合、可脚本化。`tail -f app.log | claude -p "在日志出现异常时提醒我发 Slack"` 可行；CI 也能运行 `claude -p "若出现新文案，翻译成法语并为 @lang-fr-team 创建 PR"`。
- 企业就绪：可使用 Anthropic API，或在 AWS/GCP 部署。内建[安全](/en/docs/claude-code/security)、[隐私](/en/docs/claude-code/data-usage)与[合规](https://trust.anthropic.com/)。

## 下一步

<CardGroup>
  <Card title="快速开始" icon="rocket" href="/en/docs/claude-code/quickstart">
    通过实际示例了解 Claude Code
  </Card>

  <Card title="常见工作流" icon="graduation-cap" href="/en/docs/claude-code/common-workflows">
    常见工作流的分步指南
  </Card>

  <Card title="故障排查" icon="wrench" href="/en/docs/claude-code/troubleshooting">
    Claude Code 常见问题解决方案
  </Card>

  <Card title="IDE 配置" icon="laptop" href="/en/docs/claude-code/ide-integrations">
    在你的 IDE 中使用 Claude Code
  </Card>
</CardGroup>

## 其他资源

<CardGroup>
  <Card title="托管到 AWS/GCP" icon="cloud" href="/en/docs/claude-code/third-party-integrations">
    通过 Amazon Bedrock 或 Google Vertex AI 配置 Claude Code
  </Card>

  <Card title="设置" icon="gear" href="/en/docs/claude-code/settings">
    根据你的工作流自定义 Claude Code
  </Card>

  <Card title="命令" icon="terminal" href="/en/docs/claude-code/cli-reference">
    了解 CLI 命令与控制
  </Card>

  <Card title="参考实现" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
    克隆我们的开发容器参考实现
  </Card>

  <Card title="安全" icon="shield" href="/en/docs/claude-code/security">
    了解 Claude Code 的防护与安全最佳实践
  </Card>

  <Card title="隐私与数据使用" icon="lock" href="/en/docs/claude-code/data-usage">
    了解 Claude Code 如何处理你的数据
  </Card>
</CardGroup>

