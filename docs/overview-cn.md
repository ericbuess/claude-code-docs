# Claude Code 概述

> 了解 Claude Code，Anthropic 的智能编程工具，它在您的终端中运行，帮助您比以往任何时候都更快地将想法转化为代码。

## 30 秒快速开始

前提条件：[Node.js 18 或更新版本](https://nodejs.org/en/download/)

```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 导航到您的项目
cd your-awesome-project

# 开始使用 Claude 编程
claude
```

就是这样！您已经准备好开始使用 Claude 编程了。[继续快速入门（5 分钟）→](/zh-CN/docs/claude-code/quickstart)

（有特定的设置需求或遇到问题？请参阅[高级设置](/zh-CN/docs/claude-code/setup)或[故障排除](/zh-CN/docs/claude-code/troubleshooting)。）

## Claude Code 为您做什么

* **从描述构建功能**：用简单的英语告诉 Claude 您想要构建什么。它会制定计划、编写代码并确保其正常工作。
* **调试和修复问题**：描述一个错误或粘贴错误消息。Claude Code 将分析您的代码库，识别问题并实施修复。
* **导航任何代码库**：询问有关您团队代码库的任何问题，并获得深思熟虑的答案。Claude Code 保持对您整个项目结构的感知，可以从网络上找到最新信息，并且通过 [MCP](/zh-CN/docs/claude-code/mcp) 可以从 Google Drive、Figma 和 Slack 等外部数据源获取信息。
* **自动化繁琐任务**：修复复杂的 lint 问题、解决合并冲突并编写发布说明。在您的开发机器上通过单个命令完成所有这些，或在 CI 中自动完成。

## 为什么开发者喜爱 Claude Code

* **在您的终端中工作**：不是另一个聊天窗口。不是另一个 IDE。Claude Code 在您已经工作的地方与您相遇，使用您已经喜爱的工具。
* **采取行动**：Claude Code 可以直接编辑文件、运行命令并创建提交。需要更多功能？[MCP](/zh-CN/docs/claude-code/mcp) 让 Claude 读取您在 Google Drive 中的设计文档、更新您在 Jira 中的工单，或使用\_您的\_自定义开发工具。
* **Unix 哲学**：Claude Code 是可组合和可脚本化的。`tail -f app.log | claude -p "如果您在此日志流中看到任何异常，请通过 Slack 通知我"` *有效*。您的 CI 可以运行 `claude -p "如果有新的文本字符串，将它们翻译成法语并为 @lang-fr-team 提出 PR 进行审查"`。
* **企业就绪**：使用 Anthropic 的 API，或在 AWS 或 GCP 上托管。企业级[安全性](/zh-CN/docs/claude-code/security)、[隐私](/zh-CN/docs/claude-code/data-usage)和[合规性](https://trust.anthropic.com/)是内置的。

## 下一步

<CardGroup>
  <Card title="快速入门" icon="rocket" href="/zh-CN/docs/claude-code/quickstart">
    通过实际示例查看 Claude Code 的实际应用
  </Card>

  <Card title="常见工作流程" icon="graduation-cap" href="/zh-CN/docs/claude-code/common-workflows">
    常见工作流程的分步指南
  </Card>

  <Card title="故障排除" icon="wrench" href="/zh-CN/docs/claude-code/troubleshooting">
    Claude Code 常见问题的解决方案
  </Card>

  <Card title="IDE 设置" icon="laptop" href="/zh-CN/docs/claude-code/ide-integrations">
    将 Claude Code 添加到您的 IDE
  </Card>
</CardGroup>

## 其他资源

<CardGroup>
  <Card title="在 AWS 或 GCP 上托管" icon="cloud" href="/zh-CN/docs/claude-code/third-party-integrations">
    使用 Amazon Bedrock 或 Google Vertex AI 配置 Claude Code
  </Card>

  <Card title="设置" icon="gear" href="/zh-CN/docs/claude-code/settings">
    为您的工作流程自定义 Claude Code
  </Card>

  <Card title="命令" icon="terminal" href="/zh-CN/docs/claude-code/cli-reference">
    了解 CLI 命令和控制
  </Card>

  <Card title="参考实现" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
    克隆我们的开发容器参考实现
  </Card>

  <Card title="安全性" icon="shield" href="/zh-CN/docs/claude-code/security">
    了解 Claude Code 的安全保障和安全使用的最佳实践
  </Card>

  <Card title="隐私和数据使用" icon="lock" href="/zh-CN/docs/claude-code/data-usage">
    了解 Claude Code 如何处理您的数据
  </Card>
</CardGroup>
