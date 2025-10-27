# Connect Claude Code to tools via MCP

> Learn how to connect Claude Code to your tools with the Model Context Protocol.

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
      const baseCommand = `claude mcp add --transport stdio ${server.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}`;
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
    description: "Generate better code by bringing in full Figma context",
    documentation: "https://developers.figma.com",
    urls: {
      http: "https://mcp.figma.com/mcp"
    },
    customCommands: {
      claudeCode: "claude mcp add --transport http figma-remote-mcp https://mcp.figma.com/mcp"
    },
    availability: {
      claudeCode: true,
      mcpConnector: false,
      claudeDesktop: false
    },
    notes: "Visit developers.figma.com for local server setup."
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
    name: "Cloudinary",
    category: "Design & Media",
    description: "Upload, manage, transform, and analyze your media assets",
    documentation: "https://cloudinary.com/documentation/cloudinary_llm_mcp#mcp_servers",
    urls: {},
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    },
    notes: "Multiple services available. See documentation for specific server URLs."
  }, {
    name: "Intercom",
    category: "Project Management & Documentation",
    description: "Access real-time customer conversations, tickets, and user data",
    documentation: "https://developers.intercom.com/docs/guides/mcp",
    urls: {
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
      http: "https://mcp.linear.app/mcp"
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
  }, {
    name: "Box",
    category: "Project Management & Documentation",
    description: "Ask questions about your enterprise content, get insights from unstructured data, automate content workflows",
    documentation: "https://box.dev/guides/box-mcp/remote/",
    urls: {
      http: "https://mcp.box.com/"
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
    name: "Canva",
    category: "Design & Media",
    description: "Browse, summarize, autofill, and even generate new Canva designs directly from Claude",
    documentation: "https://www.canva.dev/docs/connect/canva-mcp-server-setup/",
    urls: {
      http: "https://mcp.canva.com/mcp"
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
    name: "Daloopa",
    category: "Databases & Data Management",
    description: "Supplies high quality fundamental financial data sourced from SEC Filings, investor presentations",
    documentation: "https://docs.daloopa.com/docs/daloopa-mcp",
    urls: {
      http: "https://mcp.daloopa.com/server/mcp"
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
    name: "Fireflies",
    category: "Project Management & Documentation",
    description: "Extract valuable insights from meeting transcripts and summaries",
    documentation: "https://guide.fireflies.ai/articles/8272956938-learn-about-the-fireflies-mcp-server-model-context-protocol",
    urls: {
      http: "https://api.fireflies.ai/mcp"
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
    name: "HubSpot",
    category: "Databases & Data Management",
    description: "Access and manage HubSpot CRM data by fetching contacts, companies, and deals, and creating and updating records",
    documentation: "https://developers.hubspot.com/mcp",
    urls: {
      http: "https://mcp.hubspot.com/anthropic"
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
    name: "Hugging Face",
    category: "Development & Testing Tools",
    description: "Provides access to Hugging Face Hub information and Gradio AI Applications",
    documentation: "https://huggingface.co/settings/mcp",
    urls: {
      http: "https://huggingface.co/mcp"
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
    name: "Jam",
    category: "Development & Testing Tools",
    description: "Debug faster with AI agents that can access Jam recordings like video, console logs, network requests, and errors",
    documentation: "https://jam.dev/docs/debug-a-jam/mcp",
    urls: {
      http: "https://mcp.jam.dev/mcp"
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
    name: "Monday",
    category: "Project Management & Documentation",
    description: "Manage monday.com boards by creating items, updating columns, assigning owners, setting timelines, adding CRM activities, and writing summaries",
    documentation: "https://developer.monday.com/apps/docs/mondaycom-mcp-integration",
    urls: {
      sse: "https://mcp.monday.com/sse"
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
    name: "Netlify",
    category: "Infrastructure & DevOps",
    description: "Create, deploy, and manage websites on Netlify. Control all aspects of your site from creating secrets to enforcing access controls to aggregating form submissions",
    documentation: "https://docs.netlify.com/build/build-with-ai/netlify-mcp-server/",
    urls: {
      http: "https://netlify-mcp.netlify.app/mcp"
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
    name: "Stytch",
    category: "Infrastructure & DevOps",
    description: "Configure and manage Stytch authentication services, redirect URLs, email templates, and workspace settings",
    documentation: "https://stytch.com/docs/workspace-management/stytch-mcp",
    urls: {
      http: "http://mcp.stytch.dev/mcp"
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
    name: "Vercel",
    category: "Infrastructure & DevOps",
    description: "Vercel's official MCP server, allowing you to search and navigate documentation, manage projects and deployments, and analyze deployment logs—all in one place",
    documentation: "https://vercel.com/docs/mcp/vercel-mcp",
    urls: {
      http: "https://mcp.vercel.com/"
    },
    authentication: {
      type: "oauth"
    },
    availability: {
      claudeCode: true,
      mcpConnector: true,
      claudeDesktop: false
    }
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

Claude Code can connect to hundreds of external tools and data sources through the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), an open-source standard for AI-tool integrations. MCP servers give Claude Code access to your tools, databases, and APIs.

## What you can do with MCP

With MCP servers connected, you can ask Claude Code to:

* **Implement features from issue trackers**: "Add the feature described in JIRA issue ENG-4521 and create a PR on GitHub."
* **Analyze monitoring data**: "Check Sentry and Statsig to check the usage of the feature described in ENG-4521."
* **Query databases**: "Find emails of 10 random users who used feature ENG-4521, based on our Postgres database."
* **Integrate designs**: "Update our standard email template based on the new Figma designs that were posted in Slack"
* **Automate workflows**: "Create Gmail drafts inviting these 10 users to a feedback session about the new feature."

## Popular MCP servers

Here are some commonly used MCP servers you can connect to Claude Code:

<Warning>
  Use third party MCP servers at your own risk - Anthropic has not verified
  the correctness or security of all these servers.
  Make sure you trust MCP servers you are installing.
  Be especially careful when using MCP servers that could fetch untrusted
  content, as these can expose you to prompt injection risk.
</Warning>

<MCPServersTable platform="claudeCode" />

<Note>
  **Need a specific integration?** [Find hundreds more MCP servers on GitHub](https://github.com/modelcontextprotocol/servers), or build your own using the [MCP SDK](https://modelcontextprotocol.io/quickstart/server).
</Note>

## Installing MCP servers

MCP servers can be configured in three different ways depending on your needs:

### Option 1: Add a remote HTTP server

HTTP servers are the recommended option for connecting to remote MCP servers. This is the most widely supported transport for cloud-based services.

```bash  theme={null}
# Basic syntax
claude mcp add --transport http <name> <url>

# Real example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Example with Bearer token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Option 2: Add a remote SSE server

<Warning>
  The SSE (Server-Sent Events) transport is deprecated. Use HTTP servers instead, where available.
</Warning>

```bash  theme={null}
# Basic syntax
claude mcp add --transport sse <name> <url>

# Real example: Connect to Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Example with authentication header
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### Option 3: Add a local stdio server

Stdio servers run as local processes on your machine. They're ideal for tools that need direct system access or custom scripts.

```bash  theme={null}
# Basic syntax
claude mcp add --transport stdio <name> <command> [args...]

# Real example: Add Airtable server
claude mcp add --transport stdio airtable --env AIRTABLE_API_KEY=YOUR_KEY \
  -- npx -y airtable-mcp-server
```

<Note>
  **Understanding the "--" parameter:**
  The `--` (double dash) separates Claude's own CLI flags from the command and arguments that get passed to the MCP server. Everything before `--` are options for Claude (like `--env`, `--scope`), and everything after `--` is the actual command to run the MCP server.

  For example:

  * `claude mcp add --transport stdio myserver -- npx server` → runs `npx server`
  * `claude mcp add --transport stdio myserver --env KEY=value -- python server.py --port 8080` → runs `python server.py --port 8080` with `KEY=value` in environment

  This prevents conflicts between Claude's flags and the server's flags.
</Note>

### Managing your servers

Once configured, you can manage your MCP servers with these commands:

```bash  theme={null}
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Remove a server
claude mcp remove github

# (within Claude Code) Check server status
/mcp
```

<Tip>
  Tips:

  * Use the `--scope` flag to specify where the configuration is stored:
    * `local` (default): Available only to you in the current project (was called `project` in older versions)
    * `project`: Shared with everyone in the project via `.mcp.json` file
    * `user`: Available to you across all projects (was called `global` in older versions)
  * Set environment variables with `--env` flags (e.g., `--env KEY=value`)
  * Configure MCP server startup timeout using the MCP\_TIMEOUT environment variable (e.g., `MCP_TIMEOUT=10000 claude` sets a 10-second timeout)
  * Claude Code will display a warning when MCP tool output exceeds 10,000 tokens. To increase this limit, set the `MAX_MCP_OUTPUT_TOKENS` environment variable (e.g., `MAX_MCP_OUTPUT_TOKENS=50000`)
  * Use `/mcp` to authenticate with remote servers that require OAuth 2.0 authentication
</Tip>

<Warning>
  **Windows Users**: On native Windows (not WSL), local MCP servers that use `npx` require the `cmd /c` wrapper to ensure proper execution.

  ```bash  theme={null}
  # This creates command="cmd" which Windows can execute
  claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
  ```

  Without the `cmd /c` wrapper, you'll encounter "Connection closed" errors because Windows cannot directly execute `npx`. (See the note above for an explanation of the `--` parameter.)
</Warning>

### Plugin-provided MCP servers

[Plugins](/en/docs/claude-code/plugins) can bundle MCP servers, automatically providing tools and integrations when the plugin is enabled. Plugin MCP servers work identically to user-configured servers.

**How plugin MCP servers work**:

* Plugins define MCP servers in `.mcp.json` at the plugin root or inline in `plugin.json`
* When a plugin is enabled, its MCP servers start automatically
* Plugin MCP tools appear alongside manually configured MCP tools
* Plugin servers are managed through plugin installation (not `/mcp` commands)

**Example plugin MCP configuration**:

In `.mcp.json` at plugin root:

```json  theme={null}
{
  "database-tools": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "DB_URL": "${DB_URL}"
    }
  }
}
```

Or inline in `plugin.json`:

```json  theme={null}
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**Plugin MCP features**:

* **Automatic lifecycle**: Servers start when plugin enables, but you must restart Claude Code to apply MCP server changes (enabling or disabling)
* **Environment variables**: Use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths
* **User environment access**: Access to same environment variables as manually configured servers
* **Multiple transport types**: Support stdio, SSE, and HTTP transports (transport support may vary by server)

**Viewing plugin MCP servers**:

```bash  theme={null}
# Within Claude Code, see all MCP servers including plugin ones
/mcp
```

Plugin servers appear in the list with indicators showing they come from plugins.

**Benefits of plugin MCP servers**:

* **Bundled distribution**: Tools and servers packaged together
* **Automatic setup**: No manual MCP configuration needed
* **Team consistency**: Everyone gets the same tools when plugin is installed

See the [plugin components reference](/en/docs/claude-code/plugins-reference#mcp-servers) for details on bundling MCP servers with plugins.

## MCP installation scopes

MCP servers can be configured at three different scope levels, each serving distinct purposes for managing server accessibility and sharing. Understanding these scopes helps you determine the best way to configure servers for your specific needs.

### Local scope

Local-scoped servers represent the default configuration level and are stored in your project-specific user settings. These servers remain private to you and are only accessible when working within the current project directory. This scope is ideal for personal development servers, experimental configurations, or servers containing sensitive credentials that shouldn't be shared.

```bash  theme={null}
# Add a local-scoped server (default)
claude mcp add --transport http stripe https://mcp.stripe.com

# Explicitly specify local scope
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

### Project scope

Project-scoped servers enable team collaboration by storing configurations in a `.mcp.json` file at your project's root directory. This file is designed to be checked into version control, ensuring all team members have access to the same MCP tools and services. When you add a project-scoped server, Claude Code automatically creates or updates this file with the appropriate configuration structure.

```bash  theme={null}
# Add a project-scoped server
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

The resulting `.mcp.json` file follows a standardized format:

```json  theme={null}
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

For security reasons, Claude Code prompts for approval before using project-scoped servers from `.mcp.json` files. If you need to reset these approval choices, use the `claude mcp reset-project-choices` command.

### User scope

User-scoped servers provide cross-project accessibility, making them available across all projects on your machine while remaining private to your user account. This scope works well for personal utility servers, development tools, or services you frequently use across different projects.

```bash  theme={null}
# Add a user server
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### Choosing the right scope

Select your scope based on:

* **Local scope**: Personal servers, experimental configurations, or sensitive credentials specific to one project
* **Project scope**: Team-shared servers, project-specific tools, or services required for collaboration
* **User scope**: Personal utilities needed across multiple projects, development tools, or frequently-used services

### Scope hierarchy and precedence

MCP server configurations follow a clear precedence hierarchy. When servers with the same name exist at multiple scopes, the system resolves conflicts by prioritizing local-scoped servers first, followed by project-scoped servers, and finally user-scoped servers. This design ensures that personal configurations can override shared ones when needed.

### Environment variable expansion in `.mcp.json`

Claude Code supports environment variable expansion in `.mcp.json` files, allowing teams to share configurations while maintaining flexibility for machine-specific paths and sensitive values like API keys.

**Supported syntax:**

* `${VAR}` - Expands to the value of environment variable `VAR`
* `${VAR:-default}` - Expands to `VAR` if set, otherwise uses `default`

**Expansion locations:**
Environment variables can be expanded in:

* `command` - The server executable path
* `args` - Command-line arguments
* `env` - Environment variables passed to the server
* `url` - For HTTP server types
* `headers` - For HTTP server authentication

**Example with variable expansion:**

```json  theme={null}
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

If a required environment variable is not set and has no default value, Claude Code will fail to parse the config.

## Practical examples

{/* ### Example: Automate browser testing with Playwright

  ```bash
  # 1. Add the Playwright MCP server
  claude mcp add --transport stdio playwright -- npx -y @playwright/mcp@latest

  # 2. Write and run browser tests
  > "Test if the login flow works with test@example.com"
  > "Take a screenshot of the checkout page on mobile"
  > "Verify that the search feature returns results"
  ``` */}

### Example: Monitor errors with Sentry

```bash  theme={null}
# 1. Add the Sentry MCP server
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# 2. Use /mcp to authenticate with your Sentry account
> /mcp

# 3. Debug production issues
> "What are the most common errors in the last 24 hours?"
> "Show me the stack trace for error ID abc123"
> "Which deployment introduced these new errors?"
```

### Example: Connect to GitHub for code reviews

```bash  theme={null}
# 1. Add the GitHub MCP server
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# 2. In Claude Code, authenticate if needed
> /mcp
# Select "Authenticate" for GitHub

# 3. Now you can ask Claude to work with GitHub
> "Review PR #456 and suggest improvements"
> "Create a new issue for the bug we just found"
> "Show me all open PRs assigned to me"
```

### Example: Query your PostgreSQL database

```bash  theme={null}
# 1. Add the database server with your connection string
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"

# 2. Query your database naturally
> "What's our total revenue this month?"
> "Show me the schema for the orders table"
> "Find customers who haven't made a purchase in 90 days"
```

## Authenticate with remote MCP servers

Many cloud-based MCP servers require authentication. Claude Code supports OAuth 2.0 for secure connections.

<Steps>
  <Step title="Add the server that requires authentication">
    For example:

    ```bash  theme={null}
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
    ```
  </Step>

  <Step title="Use the /mcp command within Claude Code">
    In Claude code, use the command:

    ```
    > /mcp
    ```

    Then follow the steps in your browser to login.
  </Step>
</Steps>

<Tip>
  Tips:

  * Authentication tokens are stored securely and refreshed automatically
  * Use "Clear authentication" in the `/mcp` menu to revoke access
  * If your browser doesn't open automatically, copy the provided URL
  * OAuth authentication works with HTTP servers
</Tip>

## Add MCP servers from JSON configuration

If you have a JSON configuration for an MCP server, you can add it directly:

<Steps>
  <Step title="Add an MCP server from JSON">
    ```bash  theme={null}
    # Basic syntax
    claude mcp add-json <name> '<json>'

    # Example: Adding an HTTP server with JSON configuration
    claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

    # Example: Adding a stdio server with JSON configuration
    claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'
    ```
  </Step>

  <Step title="Verify the server was added">
    ```bash  theme={null}
    claude mcp get weather-api
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Make sure the JSON is properly escaped in your shell
  * The JSON must conform to the MCP server configuration schema
  * You can use `--scope user` to add the server to your user configuration instead of the project-specific one
</Tip>

## Import MCP servers from Claude Desktop

If you've already configured MCP servers in Claude Desktop, you can import them:

<Steps>
  <Step title="Import servers from Claude Desktop">
    ```bash  theme={null}
    # Basic syntax 
    claude mcp add-from-claude-desktop 
    ```
  </Step>

  <Step title="Select which servers to import">
    After running the command, you'll see an interactive dialog that allows you to select which servers you want to import.
  </Step>

  <Step title="Verify the servers were imported">
    ```bash  theme={null}
    claude mcp list 
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * This feature only works on macOS and Windows Subsystem for Linux (WSL)
  * It reads the Claude Desktop configuration file from its standard location on those platforms
  * Use the `--scope user` flag to add servers to your user configuration
  * Imported servers will have the same names as in Claude Desktop
  * If servers with the same names already exist, they will get a numerical suffix (e.g., `server_1`)
</Tip>

## Use Claude Code as an MCP server

You can use Claude Code itself as an MCP server that other applications can connect to:

```bash  theme={null}
# Start Claude as a stdio MCP server
claude mcp serve
```

You can use this in Claude Desktop by adding this configuration to claude\_desktop\_config.json:

```json  theme={null}
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

<Tip>
  Tips:

  * The server provides access to Claude's tools like View, Edit, LS, etc.
  * In Claude Desktop, try asking Claude to read files in a directory, make edits, and more.
  * Note that this MCP server is simply exposing Claude Code's tools to your MCP client, so your own client is responsible for implementing user confirmation for individual tool calls.
</Tip>

## MCP output limits and warnings

When MCP tools produce large outputs, Claude Code helps manage the token usage to prevent overwhelming your conversation context:

* **Output warning threshold**: Claude Code displays a warning when any MCP tool output exceeds 10,000 tokens
* **Configurable limit**: You can adjust the maximum allowed MCP output tokens using the `MAX_MCP_OUTPUT_TOKENS` environment variable
* **Default limit**: The default maximum is 25,000 tokens

To increase the limit for tools that produce large outputs:

```bash  theme={null}
# Set a higher limit for MCP tool outputs
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

This is particularly useful when working with MCP servers that:

* Query large datasets or databases
* Generate detailed reports or documentation
* Process extensive log files or debugging information

<Warning>
  If you frequently encounter output warnings with specific MCP servers, consider increasing the limit or configuring the server to paginate or filter its responses.
</Warning>

## Use MCP resources

MCP servers can expose resources that you can reference using @ mentions, similar to how you reference files.

### Reference MCP resources

<Steps>
  <Step title="List available resources">
    Type `@` in your prompt to see available resources from all connected MCP servers. Resources appear alongside files in the autocomplete menu.
  </Step>

  <Step title="Reference a specific resource">
    Use the format `@server:protocol://resource/path` to reference a resource:

    ```
    > Can you analyze @github:issue://123 and suggest a fix?
    ```

    ```
    > Please review the API documentation at @docs:file://api/authentication
    ```
  </Step>

  <Step title="Multiple resource references">
    You can reference multiple resources in a single prompt:

    ```
    > Compare @postgres:schema://users with @docs:file://database/user-model
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Resources are automatically fetched and included as attachments when referenced
  * Resource paths are fuzzy-searchable in the @ mention autocomplete
  * Claude Code automatically provides tools to list and read MCP resources when servers support them
  * Resources can contain any type of content that the MCP server provides (text, JSON, structured data, etc.)
</Tip>

## Use MCP prompts as slash commands

MCP servers can expose prompts that become available as slash commands in Claude Code.

### Execute MCP prompts

<Steps>
  <Step title="Discover available prompts">
    Type `/` to see all available commands, including those from MCP servers. MCP prompts appear with the format `/mcp__servername__promptname`.
  </Step>

  <Step title="Execute a prompt without arguments">
    ```
    > /mcp__github__list_prs
    ```
  </Step>

  <Step title="Execute a prompt with arguments">
    Many prompts accept arguments. Pass them space-separated after the command:

    ```
    > /mcp__github__pr_review 456
    ```

    ```
    > /mcp__jira__create_issue "Bug in login flow" high
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * MCP prompts are dynamically discovered from connected servers
  * Arguments are parsed based on the prompt's defined parameters
  * Prompt results are injected directly into the conversation
  * Server and prompt names are normalized (spaces become underscores)
</Tip>

## Enterprise MCP configuration

For organizations that need centralized control over MCP servers, Claude Code supports enterprise-managed MCP configurations. This allows IT administrators to:

* **Control which MCP servers employees can access**: Deploy a standardized set of approved MCP servers across the organization
* **Prevent unauthorized MCP servers**: Optionally restrict users from adding their own MCP servers
* **Disable MCP entirely**: Remove MCP functionality completely if needed

### Setting up enterprise MCP configuration

System administrators can deploy an enterprise MCP configuration file alongside the managed settings file:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-mcp.json`
* **Windows**: `C:\ProgramData\ClaudeCode\managed-mcp.json`
* **Linux**: `/etc/claude-code/managed-mcp.json`

The `managed-mcp.json` file uses the same format as a standard `.mcp.json` file:

```json  theme={null}
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}
```

### Restricting MCP servers with allowlists and denylists

In addition to providing enterprise-managed servers, administrators can control which MCP servers users are allowed to configure using `allowedMcpServers` and `deniedMcpServers` in the `managed-settings.json` file:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Windows**: `C:\ProgramData\ClaudeCode\managed-settings.json`
* **Linux**: `/etc/claude-code/managed-settings.json`

```json  theme={null}
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverName": "sentry" },
    { "serverName": "company-internal" }
  ],
  "deniedMcpServers": [
    { "serverName": "filesystem" }
  ]
}
```

**Allowlist behavior (`allowedMcpServers`)**:

* `undefined` (default): No restrictions - users can configure any MCP server
* Empty array `[]`: Complete lockdown - users cannot configure any MCP servers
* List of server names: Users can only configure the specified servers

**Denylist behavior (`deniedMcpServers`)**:

* `undefined` (default): No servers are blocked
* Empty array `[]`: No servers are blocked
* List of server names: Specified servers are explicitly blocked across all scopes

**Important notes**:

* These restrictions apply to all scopes: user, project, local, and even enterprise servers from `managed-mcp.json`
* **Denylist takes absolute precedence**: If a server appears in both lists, it will be blocked

<Note>
  **Enterprise configuration precedence**: The enterprise MCP configuration has the highest precedence and cannot be overridden by user, local, or project configurations when `useEnterpriseMcpConfigOnly` is enabled.
</Note>
