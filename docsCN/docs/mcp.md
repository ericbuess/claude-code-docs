# 通过 MCP 将 Claude Code 连接到工具

> 了解如何通过 Model Context Protocol 将 Claude Code 连接到您的工具。

export const MCPServersTable = ({platform = "all"}) => {
  const generateClaudeCodeCommand = server => {
    if (server.customCommands && server.customCommands.claudeCode) {
      return server.customCommands.claudeCode;
    }
    if (server.urls.http) {
      return `claude mcp add --transport http ${server.name.toLowerCase().replace(/[^a-z0-9]/g, '-')} ${server.urls.http}`;
    }
    if (server.urls.sse) {
      return `claude mcp add --transport sse ${server.name.toLowerCase().replace(/[^a-z0-9]/g, '-')} ${server.urls.sse}`;
    }
    if (server.urls.stdio) {
      const envFlags = server.authentication && server.authentication.envVars ? server.authentication.envVars.map(v => `--env ${v}=YOUR_${v.split('_').pop()}`).join(' ') : '';
      const baseCommand = `claude mcp add ${server.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}`;
      return envFlags ? `${baseCommand} ${envFlags} -- ${server.urls.stdio}` : `${baseCommand} -- ${server.urls.stdio}`;
    }
    return null;
  };
  const servers = [{
    name: "Airtable",
    category: "Databases & Data Management",
    description: "Read/write records, manage bases and tables",
    documentation: "https://github.com/domdomegg/airtable-mcp-server",
    urls: {
      stdio: "npx -y airtable-mcp-server"
    },
    authentication: {
      type: "api_key",
      envVars: ["AIRTABLE_API_KEY"]
    },
    availability: {
      claudeCode: true,
      mcpConnector: false,
      claudeDesktop: true
    }
  }, {
    name: "Figma",
    category: "Design & Media",
    description: "Access designs, export assets",
    documentation: "https://help.figma.com/hc/en-us/articles/32132100833559",
    urls: {
      sse: "http://127.0.0.1:3845/sse"
    },
    availability: {
      claudeCode: true,
      mcpConnector: false,
      claudeDesktop: false
    },
    notes: "Requires Figma Desktop with Dev Mode MCP Server"
  }, {
    name: "Asana",
    category: "Project Management & Documentation",
    description: "Interact with your Asana workspace to keep projects on track",
    documentation: "https://developers.asana.com/docs/using-asanas-model-control-protocol-mcp-server",
    urls: {
      sse: "https://mcp.asana.com/sse"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Atlassian",
    category: "Project Management & Documentation",
    description: "Manage your Jira tickets and Confluence docs",
    documentation: "https://www.atlassian.com/platform/remote-mcp-server",
    urls: {
      sse: "https://mcp.atlassian.com/v1/sse"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "ClickUp",
    category: "Project Management & Documentation",
    description: "Task management, project tracking",
    documentation: "https://github.com/hauptsacheNet/clickup-mcp",
    urls: {
      stdio: "npx -y @hauptsache.net/clickup-mcp"
    },
    authentication: {
      type: "api_key",
      envVars: ["CLICKUP_API_KEY", "CLICKUP_TEAM_ID"]
    },
    availability: {
      claudeCode: true,
      mcpConnector: false,
      claudeDesktop: true
    }
  }, {
    name: "Cloudflare",
    category: "Infrastructure & DevOps",
    description: "Build applications, analyze traffic, monitor performance, and manage security settings through Cloudflare",
    documentation: "https://developers.cloudflare.com/agents/model-context-protocol/mcp-servers-for-cloudflare/",
    urls: {},
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    },
    notes: "Multiple services available. See documentation for specific server URLs. Claude Code can use the Cloudflare CLI if installed."
  }, {
    name: "Intercom",
    category: "Project Management & Documentation",
    description: "Access real-time customer conversations, tickets, and user data",
    documentation: "https://developers.intercom.com/docs/guides/mcp",
    urls: {
      sse: "https://mcp.intercom.com/sse",
      http: "https://mcp.intercom.com/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "invideo",
    category: "Design & Media",
    description: "Build video creation capabilities into your applications",
    documentation: "https://invideo.io/ai/mcp",
    urls: {
      sse: "https://mcp.invideo.io/sse"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Linear",
    category: "Project Management & Documentation",
    description: "Integrate with Linear's issue tracking and project management",
    documentation: "https://linear.app/docs/mcp",
    urls: {
      sse: "https://mcp.linear.app/sse"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Notion",
    category: "Project Management & Documentation",
    description: "Read docs, update pages, manage tasks",
    documentation: "https://developers.notion.com/docs/mcp",
    urls: {
      http: "https://mcp.notion.com/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: false,
      claudeDesktop: false
    }
  }, {
    name: "PayPal",
    category: "Payments & Commerce",
    description: "Integrate PayPal commerce capabilities, payment processing, transaction management",
    documentation: "https://www.paypal.ai/",
    urls: {
      sse: "https://mcp.paypal.com/sse",
      http: "https://mcp.paypal.com/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Plaid",
    category: "Payments & Commerce",
    description: "Analyze, troubleshoot, and optimize Plaid integrations. Banking data, financial account linking",
    documentation: "https://plaid.com/blog/plaid-mcp-ai-assistant-claude/",
    urls: {
      sse: "https://api.dashboard.plaid.com/mcp/sse"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Sentry",
    category: "Development & Testing Tools",
    description: "Monitor errors, debug production issues",
    documentation: "https://docs.sentry.io/product/sentry-mcp/",
    urls: {
      sse: "https://mcp.sentry.dev/sse",
      http: "https://mcp.sentry.dev/mcp"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: false,
      claudeDesktop: false
    }
  }, {
    name: "Square",
    category: "Payments & Commerce",
    description: "Use an agent to build on Square APIs. Payments, inventory, orders, and more",
    documentation: "https://developer.squareup.com/docs/mcp",
    urls: {
      sse: "https://mcp.squareup.com/sse"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Socket",
    category: "Development & Testing Tools",
    description: "Security analysis for dependencies",
    documentation: "https://github.com/SocketDev/socket-mcp",
    urls: {
      http: "https://mcp.socket.dev/"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: false,
      claudeDesktop: false
    }
  }, {
    name: "Stripe",
    category: "Payments & Commerce",
    description: "Payment processing, subscription management, and financial transactions",
    documentation: "https://docs.stripe.com/mcp",
    urls: {
      http: "https://mcp.stripe.com"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
  }, {
    name: "Workato",
    category: "Automation & Integration",
    description: "Access any application, workflows or data via Workato, made accessible for AI",
    documentation: "https://docs.workato.com/mcp.html",
    urls: {},
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    },
    notes: "MCP servers are programmatically generated"
  }, {
    name: "Zapier",
    category: "Automation & Integration",
    description: "Connect to nearly 8,000 apps through Zapier's automation platform",
    documentation: "https://help.zapier.com/hc/en-us/articles/36265392843917",
    urls: {},
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    },
    notes: "Generate a user-specific URL at mcp.zapier.com"
  }];
  const filteredServers = servers.filter(server => {
    if (platform === "claudeCode") {
      return server.availability.claudeCode;
    } else if (platform === "mcpConnector") {
      return server.availability.mcpConnector;
    } else if (platform === "claudeDesktop") {
      return server.availability.claudeDesktop;
    } else if (platform === "all") {
      return true;
    } else {
      throw new Error(`Unknown platform: ${platform}`);
    }
  });
  const serversByCategory = filteredServers.reduce((acc, server) => {
    if (!acc[server.category]) {
      acc[server.category] = [];
    }
    acc[server.category].push(server);
    return acc;
  }, {});
  const categoryOrder = ["Development & Testing Tools", "Project Management & Documentation", "Databases & Data Management", "Payments & Commerce", "Design & Media", "Infrastructure & DevOps", "Automation & Integration"];
  return <>
      <style jsx>{`
        .cards-container {
          display: grid;
          gap: 1rem;
          margin-bottom: 2rem;
        }
        .server-card {
          border: 1px solid var(--border-color, #e5e7eb);
          border-radius: 6px;
          padding: 1rem;
        }
        .command-row {
          display: flex;
          align-items: center;
          gap: 0.25rem;
        }
        .command-row code {
          font-size: 0.75rem;
          overflow-x: auto;
        }
      `}</style>
      
      {categoryOrder.map(category => {
    if (!serversByCategory[category]) return null;
    return <div key={category}>
            <h3>{category}</h3>
            <div className="cards-container">
              {serversByCategory[category].map(server => {
      const claudeCodeCommand = generateClaudeCodeCommand(server);
      const mcpUrl = server.urls.http || server.urls.sse;
      const commandToShow = platform === "claudeCode" ? claudeCodeCommand : mcpUrl;
      return <div key={server.name} className="server-card">
                    <div>
                      {server.documentation ? <a href={server.documentation}>
                          <strong>{server.name}</strong>
                        </a> : <strong>{server.name}</strong>}
                    </div>
                    
                    <p style={{
        margin: '0.5rem 0',
        fontSize: '0.9rem'
      }}>
                      {server.description}
                      {server.notes && <span style={{
        display: 'block',
        marginTop: '0.25rem',
        fontSize: '0.8rem',
        fontStyle: 'italic',
        opacity: 0.7
      }}>
                          {server.notes}
                        </span>}
                    </p>
                    
                    {commandToShow && <>
                      <p style={{
        display: 'block',
        fontSize: '0.75rem',
        fontWeight: 500,
        minWidth: 'fit-content',
        marginTop: '0.5rem',
        marginBottom: 0
      }}>
                        {platform === "claudeCode" ? "Command" : "URL"}
                      </p>
                      <div className="command-row">
                        <code>
                          {commandToShow}
                        </code>
                      </div>
                    </>}
                  </div>;
    })}
            </div>
          </div>;
  })}
    </>;
};

Claude Code 可以通过 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 连接到数百个外部工具和数据源，这是一个用于 AI 工具集成的开源标准。MCP 服务器为 Claude Code 提供对您的工具、数据库和 API 的访问。

## 您可以使用 MCP 做什么

连接 MCP 服务器后，您可以要求 Claude Code：

* **从问题跟踪器实现功能**："添加 JIRA 问题 ENG-4521 中描述的功能并在 GitHub 上创建 PR。"
* **分析监控数据**："检查 Sentry 和 Statsig 以查看 ENG-4521 中描述的功能的使用情况。"
* **查询数据库**："根据我们的 Postgres 数据库，找到 10 个使用功能 ENG-4521 的随机用户的电子邮件。"
* **集成设计**："根据在 Slack 中发布的新 Figma 设计更新我们的标准电子邮件模板"
* **自动化工作流程**："创建 Gmail 草稿，邀请这 10 个用户参加关于新功能的反馈会议。"

## 流行的 MCP 服务器

以下是一些您可以连接到 Claude Code 的常用 MCP 服务器：

<Warning>
  使用第三方 MCP 服务器需要您自担风险 - Anthropic 未验证所有这些服务器的正确性或安全性。
  确保您信任正在安装的 MCP 服务器。
  在使用可能获取不受信任内容的 MCP 服务器时要特别小心，因为这些可能会使您面临提示注入风险。
</Warning>

<MCPServersTable platform="claudeCode" />

<Note>
  **需要特定集成？** [在 GitHub 上查找数百个更多的 MCP 服务器](https://github.com/modelcontextprotocol/servers)，或使用 [MCP SDK](https://modelcontextprotocol.io/quickstart/server) 构建您自己的服务器。
</Note>

## 安装 MCP 服务器

根据您的需求，MCP 服务器可以通过三种不同的方式进行配置：

### 选项 1：添加本地 stdio 服务器

Stdio 服务器作为本地进程在您的机器上运行。它们非常适合需要直接系统访问或自定义脚本的工具。

```bash
# 基本语法
claude mcp add <name> <command> [args...]

# 实际示例：添加 Airtable 服务器
claude mcp add airtable --env AIRTABLE_API_KEY=YOUR_KEY \
  -- npx -y airtable-mcp-server
```

### 选项 2：添加远程 SSE 服务器

SSE（服务器发送事件）服务器提供实时流连接。许多云服务使用此方式进行实时更新。

```bash
# 基本语法
claude mcp add --transport sse <name> <url>

# 实际示例：连接到 Linear
claude mcp add --transport sse linear https://mcp.linear.app/sse

# 带认证头的示例
claude mcp add --transport sse private-api https://api.company.com/mcp \
  --header "X-API-Key: your-key-here"
```

### 选项 3：添加远程 HTTP 服务器

HTTP 服务器使用标准的请求/响应模式。大多数 REST API 和 Web 服务使用此传输方式。

```bash
# 基本语法
claude mcp add --transport http <name> <url>

# 实际示例：连接到 Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 带 Bearer 令牌的示例
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### 管理您的服务器

配置完成后，您可以使用以下命令管理您的 MCP 服务器：

```bash
# 列出所有已配置的服务器
claude mcp list

# 获取特定服务器的详细信息
claude mcp get github

# 删除服务器
claude mcp remove github

# （在 Claude Code 中）检查服务器状态
/mcp
```

<Tip>
  提示：

  * 使用 `--scope` 标志指定配置存储位置：
    * `local`（默认）：仅在当前项目中对您可用（在旧版本中称为 `project`）
    * `project`：通过 `.mcp.json` 文件与项目中的每个人共享
    * `user`：在所有项目中对您可用（在旧版本中称为 `global`）
  * 使用 `--env` 标志设置环境变量（例如，`--env KEY=value`）
  * 使用 MCP\_TIMEOUT 环境变量配置 MCP 服务器启动超时（例如，`MCP_TIMEOUT=10000 claude` 设置 10 秒超时）
  * 使用 `/mcp` 与需要 OAuth 2.0 认证的远程服务器进行身份验证
</Tip>

<Warning>
  **Windows 用户**：在原生 Windows（非 WSL）上，使用 `npx` 的本地 MCP 服务器需要 `cmd /c` 包装器以确保正确执行。

  ```bash
  # 这创建了 Windows 可以执行的 command="cmd"
  claude mcp add my-server -- cmd /c npx -y @some/package
  ```

  没有 `cmd /c` 包装器，您会遇到"连接关闭"错误，因为 Windows 无法直接执行 `npx`。
</Warning>

## MCP 安装范围

MCP 服务器可以在三个不同的范围级别进行配置，每个级别都有不同的目的来管理服务器可访问性和共享。了解这些范围有助于您确定为特定需求配置服务器的最佳方式。

### 本地范围

本地范围的服务器代表默认配置级别，存储在您的项目特定用户设置中。这些服务器对您保持私有，仅在当前项目目录中工作时可访问。此范围非常适合个人开发服务器、实验性配置或包含不应共享的敏感凭据的服务器。

```bash
# 添加本地范围的服务器（默认）
claude mcp add my-private-server /path/to/server

# 明确指定本地范围
claude mcp add my-private-server --scope local /path/to/server
```

### 项目范围

项目范围的服务器通过在项目根目录存储配置到 `.mcp.json` 文件中来实现团队协作。此文件设计为检入版本控制，确保所有团队成员都能访问相同的 MCP 工具和服务。当您添加项目范围的服务器时，Claude Code 会自动创建或更新此文件，使用适当的配置结构。

```bash
# 添加项目范围的服务器
claude mcp add shared-server --scope project /path/to/server
```

生成的 `.mcp.json` 文件遵循标准化格式：

```json
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

出于安全原因，Claude Code 在使用来自 `.mcp.json` 文件的项目范围服务器之前会提示批准。如果您需要重置这些批准选择，请使用 `claude mcp reset-project-choices` 命令。

### 用户范围

用户范围的服务器提供跨项目可访问性，使它们在您机器上的所有项目中可用，同时对您的用户帐户保持私有。此范围适用于个人实用程序服务器、开发工具或您在不同项目中经常使用的服务。

```bash
# 添加用户服务器
claude mcp add my-user-server --scope user /path/to/server
```

### 选择正确的范围

根据以下情况选择您的范围：

* **本地范围**：个人服务器、实验性配置或特定于一个项目的敏感凭据
* **项目范围**：团队共享服务器、项目特定工具或协作所需的服务
* **用户范围**：多个项目需要的个人实用程序、开发工具或经常使用的服务

### 范围层次结构和优先级

MCP 服务器配置遵循清晰的优先级层次结构。当多个范围中存在同名服务器时，系统通过优先考虑本地范围的服务器，然后是项目范围的服务器，最后是用户范围的服务器来解决冲突。这种设计确保个人配置可以在需要时覆盖共享配置。

### `.mcp.json` 中的环境变量扩展

Claude Code 支持在 `.mcp.json` 文件中进行环境变量扩展，允许团队共享配置，同时为机器特定路径和 API 密钥等敏感值保持灵活性。

**支持的语法：**

* `${VAR}` - 扩展为环境变量 `VAR` 的值
* `${VAR:-default}` - 如果设置了 `VAR` 则扩展为 `VAR`，否则使用 `default`

**扩展位置：**
环境变量可以在以下位置扩展：

* `command` - 服务器可执行文件路径
* `args` - 命令行参数
* `env` - 传递给服务器的环境变量
* `url` - 用于 SSE/HTTP 服务器类型
* `headers` - 用于 SSE/HTTP 服务器认证

**带变量扩展的示例：**

```json
{
  "mcpServers": {
    "api-server": {
      "type": "sse",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

如果未设置所需的环境变量且没有默认值，Claude Code 将无法解析配置。

## 实际示例

{/* These are commented out while waiting for approval in https://anthropic.slack.com/archives/C08R8A6SZEX/p1754320373845919. I'm expecting/hoping to get this approval soon, so keeping this here for easy uncommenting. Reviewer: feel free to just delete this if you'd prefer. */}

{/* ### 示例：连接到 GitHub 进行代码审查

  ```bash
  # 1. 添加 GitHub MCP 服务器
  claude mcp add --transport http github https://api.githubcopilot.com/mcp/

  # 2. 在 Claude Code 中，如果需要则进行身份验证
  > /mcp
  # 为 GitHub 选择"身份验证"

  # 3. 现在您可以要求 Claude 与 GitHub 协作
  > "审查 PR #456 并建议改进"
  > "为我们刚发现的错误创建新问题"
  > "显示分配给我的所有开放 PR"
  ```

  <Tip>
  提示：
  - 另请参阅 [GitHub Actions](/zh-CN/docs/claude-code/github-actions) 集成以自动运行此功能。
  - 如果您安装了 GitHub CLI，对于某些操作，您可能更喜欢直接使用 Claude Code 的 bash 工具而不是 MCP 服务器。
  </Tip>

  ### 示例：查询您的 PostgreSQL 数据库

  ```bash
  # 1. 使用您的连接字符串添加数据库服务器
  claude mcp add db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"

  # 2. 自然地查询您的数据库
  > "这个月我们的总收入是多少？"
  > "显示订单表的架构"
  > "找到 90 天内没有购买的客户"
  ``` */}

### 示例：使用 Sentry 监控错误

```bash
# 1. 添加 Sentry MCP 服务器
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# 2. 使用 /mcp 与您的 Sentry 帐户进行身份验证
> /mcp

# 3. 调试生产问题
> "过去 24 小时内最常见的错误是什么？"
> "显示错误 ID abc123 的堆栈跟踪"
> "哪个部署引入了这些新错误？"
```

{/* ### 示例：使用 Playwright 自动化浏览器测试

  ```bash
  # 1. 添加 Playwright MCP 服务器
  claude mcp add playwright -- npx -y @playwright/mcp@latest

  # 2. 编写并运行浏览器测试
  > "测试使用 test@example.com 的登录流程是否有效"
  > "在移动设备上截取结账页面的屏幕截图"
  > "验证搜索功能是否返回结果"
  ``` */}

## 与远程 MCP 服务器进行身份验证

许多基于云的 MCP 服务器需要身份验证。Claude Code 支持 OAuth 2.0 进行安全连接。

<Steps>
  <Step title="添加需要身份验证的服务器">
    例如：

    ```bash
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
    ```
  </Step>

  <Step title="在 Claude Code 中使用 /mcp 命令">
    在 Claude Code 中，使用命令：

    ```
    > /mcp
    ```

    然后按照浏览器中的步骤进行登录。
  </Step>
</Steps>

<Tip>
  提示：

  * 身份验证令牌安全存储并自动刷新
  * 在 `/mcp` 菜单中使用"清除身份验证"来撤销访问
  * 如果您的浏览器没有自动打开，请复制提供的 URL
  * OAuth 身份验证适用于 SSE 和 HTTP 传输
</Tip>

## 从 JSON 配置添加 MCP 服务器

如果您有 MCP 服务器的 JSON 配置，可以直接添加：

<Steps>
  <Step title="从 JSON 添加 MCP 服务器">
    ```bash
    # 基本语法
    claude mcp add-json <name> '<json>'

    # 示例：使用 JSON 配置添加 stdio 服务器
    claude mcp add-json weather-api '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'
    ```
  </Step>

  <Step title="验证服务器已添加">
    ```bash
    claude mcp get weather-api
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 确保 JSON 在您的 shell 中正确转义
  * JSON 必须符合 MCP 服务器配置架构
  * 您可以使用 `--scope global` 将服务器添加到全局配置而不是项目特定配置
</Tip>

## 从 Claude Desktop 导入 MCP 服务器

如果您已经在 Claude Desktop 中配置了 MCP 服务器，可以导入它们：

<Steps>
  <Step title="从 Claude Desktop 导入服务器">
    ```bash
    # 基本语法 
    claude mcp add-from-claude-desktop 
    ```
  </Step>

  <Step title="选择要导入的服务器">
    运行命令后，您将看到一个交互式对话框，允许您选择要导入的服务器。
  </Step>

  <Step title="验证服务器已导入">
    ```bash
    claude mcp list 
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 此功能仅在 macOS 和 Windows Subsystem for Linux (WSL) 上有效
  * 它从这些平台上的标准位置读取 Claude Desktop 配置文件
  * 使用 `--scope global` 标志将服务器添加到全局配置
  * 导入的服务器将具有与 Claude Desktop 中相同的名称
  * 如果已存在同名服务器，它们将获得数字后缀（例如，`server_1`）
</Tip>

## 将 Claude Code 用作 MCP 服务器

您可以将 Claude Code 本身用作其他应用程序可以连接的 MCP 服务器：

```bash
# 将 Claude 启动为 stdio MCP 服务器
claude mcp serve
```

您可以通过将此配置添加到 claude\_desktop\_config.json 在 Claude Desktop 中使用：

```json
{
  "mcpServers": {
    "claude-code": {
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

<Tip>
  提示：

  * 服务器提供对 Claude 工具的访问，如 View、Edit、LS 等
  * 在 Claude Desktop 中，尝试要求 Claude 读取目录中的文件、进行编辑等
  * 请注意，此 MCP 服务器只是将 Claude Code 的工具暴露给您的 MCP 客户端，因此您自己的客户端负责为单个工具调用实现用户确认
</Tip>

## 使用 MCP 资源

MCP 服务器可以公开您可以使用 @ 提及引用的资源，类似于引用文件的方式。

### 引用 MCP 资源

<Steps>
  <Step title="列出可用资源">
    在提示中输入 `@` 以查看所有连接的 MCP 服务器的可用资源。资源与文件一起出现在自动完成菜单中。
  </Step>

  <Step title="引用特定资源">
    使用格式 `@server:protocol://resource/path` 引用资源：

    ```
    > 您能分析 @github:issue://123 并建议修复吗？
    ```

    ```
    > 请查看 @docs:file://api/authentication 的 API 文档
    ```
  </Step>

  <Step title="多个资源引用">
    您可以在单个提示中引用多个资源：

    ```
    > 比较 @postgres:schema://users 与 @docs:file://database/user-model
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 引用时资源会自动获取并作为附件包含
  * 资源路径在 @ 提及自动完成中可进行模糊搜索
  * 当服务器支持时，Claude Code 自动提供列出和读取 MCP 资源的工具
  * 资源可以包含 MCP 服务器提供的任何类型的内容（文本、JSON、结构化数据等）
</Tip>

## 将 MCP 提示用作斜杠命令

MCP 服务器可以公开在 Claude Code 中作为斜杠命令可用的提示。

### 执行 MCP 提示

<Steps>
  <Step title="发现可用提示">
    输入 `/` 查看所有可用命令，包括来自 MCP 服务器的命令。MCP 提示以格式 `/mcp__servername__promptname` 出现。
  </Step>

  <Step title="执行不带参数的提示">
    ```
    > /mcp__github__list_prs
    ```
  </Step>

  <Step title="执行带参数的提示">
    许多提示接受参数。在命令后用空格分隔传递它们：

    ```
    > /mcp__github__pr_review 456
    ```

    ```
    > /mcp__jira__create_issue "登录流程中的错误" high
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * MCP 提示从连接的服务器动态发现
  * 参数根据提示定义的参数进行解析
  * 提示结果直接注入到对话中
  * 服务器和提示名称已标准化（空格变为下划线）
</Tip>
