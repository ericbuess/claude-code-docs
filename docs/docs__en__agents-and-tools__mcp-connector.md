# MCP connector

---

Claude's Model Context Protocol (MCP) connector feature enables you to connect to remote MCP servers directly from the Messages API without a separate MCP client.

<Note>
  **Current version**: This feature requires the beta header: `"anthropic-beta": "mcp-client-2025-11-20"`

  The previous version (`mcp-client-2025-04-04`) is deprecated. See the [deprecated version documentation](#deprecated-version-mcp-client-2025-04-04) below.
</Note>

## Key features

- **Direct API integration**: Connect to MCP servers without implementing an MCP client
- **Tool calling support**: Access MCP tools through the Messages API
- **Flexible tool configuration**: Enable all tools, allowlist specific tools, or denylist unwanted tools
- **Per-tool configuration**: Configure individual tools with custom settings
- **OAuth authentication**: Support for OAuth Bearer tokens for authenticated servers
- **Multiple servers**: Connect to multiple MCP servers in a single request

## Limitations

- Of the feature set of the [MCP specification](https://modelcontextprotocol.io/introduction#explore-mcp), only [tool calls](https://modelcontextprotocol.io/docs/concepts/tools) are currently supported.
- The server must be publicly exposed through HTTP (supports both Streamable HTTP and SSE transports). Local STDIO servers cannot be connected directly.
- The MCP connector is currently not supported on Amazon Bedrock and Google Vertex.

## Using the MCP connector in the Messages API

The MCP connector uses two components:

1. **MCP Server Definition** (`mcp_servers` array): Defines server connection details (URL, authentication)
2. **MCP Toolset** (`tools` array): Configures which tools to enable and how to configure them

### Basic example

This example enables all tools from an MCP server with default configuration:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: mcp-client-2025-11-20" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1000,
    "messages": [{"role": "user", "content": "What tools do you have available?"}],
    "mcp_servers": [
      {
        "type": "url",
        "url": "https://example-server.modelcontextprotocol.io/sse",
        "name": "example-mcp",
        "authorization_token": "YOUR_TOKEN"
      }
    ],
    "tools": [
      {
        "type": "mcp_toolset",
        "mcp_server_name": "example-mcp"
      }
    ]
  }'
```

```typescript TypeScript
import { Anthropic } from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

const response = await anthropic.beta.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 1000,
  messages: [
    {
      role: "user",
      content: "What tools do you have available?",
    },
  ],
  mcp_servers: [
    {
      type: "url",
      url: "https://example-server.modelcontextprotocol.io/sse",
      name: "example-mcp",
      authorization_token: "YOUR_TOKEN",
    },
  ],
  tools: [
    {
      type: "mcp_toolset",
      mcp_server_name: "example-mcp",
    },
  ],
  betas: ["mcp-client-2025-11-20"],
});
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    messages=[{
        "role": "user",
        "content": "What tools do you have available?"
    }],
    mcp_servers=[{
        "type": "url",
        "url": "https://mcp.example.com/sse",
        "name": "example-mcp",
        "authorization_token": "YOUR_TOKEN"
    }],
    tools=[{
        "type": "mcp_toolset",
        "mcp_server_name": "example-mcp"
    }],
    betas=["mcp-client-2025-11-20"]
)
```
</CodeGroup>

## MCP server configuration

Each MCP server in the `mcp_servers` array defines the connection details:

```json
{
  "type": "url",
  "url": "https://example-server.modelcontextprotocol.io/sse",
  "name": "example-mcp",
  "authorization_token": "YOUR_TOKEN"
}
```

### Field descriptions

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | string | Yes | Currently only "url" is supported |
| `url` | string | Yes | The URL of the MCP server. Must start with https:// |
| `name` | string | Yes | A unique identifier for this MCP server. Must be referenced by exactly one MCPToolset in the `tools` array. |
| `authorization_token` | string | No | OAuth authorization token if required by the MCP server. See [MCP specification](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization). |

## MCP toolset configuration

The MCPToolset lives in the `tools` array and configures which tools from the MCP server are enabled and how they should be configured.

### Basic structure

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "example-mcp",
  "default_config": {
    "enabled": true,
    "defer_loading": false
  },
  "configs": {
    "specific_tool_name": {
      "enabled": true,
      "defer_loading": true
    }
  }
}
```

### Field descriptions

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | string | Yes | Must be "mcp_toolset" |
| `mcp_server_name` | string | Yes | Must match a server name defined in the `mcp_servers` array |
| `default_config` | object | No | Default configuration applied to all tools in this set. Individual tool configs in `configs` will override these defaults. |
| `configs` | object | No | Per-tool configuration overrides. Keys are tool names, values are configuration objects. |
| `cache_control` | object | No | Cache breakpoint configuration for this toolset |

### Tool configuration options

Each tool (whether configured in `default_config` or in `configs`) supports the following fields:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enabled` | boolean | `true` | Whether this tool is enabled |
| `defer_loading` | boolean | `false` | If true, tool description is not sent to the model initially. Used with [Tool Search Tool](/agents-and-tools/tool-search-tool). |

### Configuration merging

Configuration values merge with this precedence (highest to lowest):

1. Tool-specific settings in `configs`
2. Set-level `default_config`
3. System defaults

Example:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-calendar-mcp",
  "default_config": {
    "defer_loading": true
  },
  "configs": {
    "search_events": {
      "enabled": false
    }
  }
}
```

Results in:
- `search_events`: `enabled: false` (from configs), `defer_loading: true` (from default_config)
- All other tools: `enabled: true` (system default), `defer_loading: true` (from default_config)

## Common configuration patterns

### Enable all tools with default configuration

The simplest pattern - enable all tools from a server:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-calendar-mcp",
}
```

### Allowlist - Enable only specific tools

Set `enabled: false` as the default, then explicitly enable specific tools:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-calendar-mcp",
  "default_config": {
    "enabled": false
  },
  "configs": {
    "search_events": {
      "enabled": true
    },
    "create_event": {
      "enabled": true
    }
  }
}
```

### Denylist - Disable specific tools

Enable all tools by default, then explicitly disable unwanted tools:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-calendar-mcp",
  "configs": {
    "delete_all_events": {
      "enabled": false
    },
    "share_calendar_publicly": {
      "enabled": false
    }
  }
}
```

### Mixed - Allowlist with per-tool configuration

Combine allowlisting with custom configuration for each tool:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-calendar-mcp",
  "default_config": {
    "enabled": false,
    "defer_loading": true
  },
  "configs": {
    "search_events": {
      "enabled": true,
      "defer_loading": false
    },
    "list_events": {
      "enabled": true
    }
  }
}
```

In this example:
- `search_events` is enabled with `defer_loading: false`
- `list_events` is enabled with `defer_loading: true` (inherited from default_config)
- All other tools are disabled

## Validation rules

The API enforces these validation rules:

- **Server must exist**: The `mcp_server_name` in an MCPToolset must match a server defined in the `mcp_servers` array
- **Server must be used**: Every MCP server defined in `mcp_servers` must be referenced by exactly one MCPToolset
- **Unique toolset per server**: Each MCP server can only be referenced by one MCPToolset
- **Unknown tool names**: If a tool name in `configs` doesn't exist on the MCP server, a backend warning is logged but no error is returned (MCP servers may have dynamic tool availability)

## Response content types

When Claude uses MCP tools, the response will include two new content block types:

### MCP Tool Use Block

```json
{
  "type": "mcp_tool_use",
  "id": "mcptoolu_014Q35RayjACSWkSj4X2yov1",
  "name": "echo",
  "server_name": "example-mcp",
  "input": { "param1": "value1", "param2": "value2" }
}
```

### MCP Tool Result Block

```json
{
  "type": "mcp_tool_result",
  "tool_use_id": "mcptoolu_014Q35RayjACSWkSj4X2yov1",
  "is_error": false,
  "content": [
    {
      "type": "text",
      "text": "Hello"
    }
  ]
}
```

## Multiple MCP servers

You can connect to multiple MCP servers by including multiple server definitions in `mcp_servers` and a corresponding MCPToolset for each in the `tools` array:

```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 1000,
  "messages": [
    {
      "role": "user",
      "content": "Use tools from both mcp-server-1 and mcp-server-2 to complete this task"
    }
  ],
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://mcp.example1.com/sse",
      "name": "mcp-server-1",
      "authorization_token": "TOKEN1"
    },
    {
      "type": "url",
      "url": "https://mcp.example2.com/sse",
      "name": "mcp-server-2",
      "authorization_token": "TOKEN2"
    }
  ],
  "tools": [
    {
      "type": "mcp_toolset",
      "mcp_server_name": "mcp-server-1"
    },
    {
      "type": "mcp_toolset",
      "mcp_server_name": "mcp-server-2",
      "default_config": {
        "defer_loading": true
      }
    }
  ]
}
```

## Authentication

For MCP servers that require OAuth authentication, you'll need to obtain an access token. The MCP connector beta supports passing an `authorization_token` parameter in the MCP server definition.
API consumers are expected to handle the OAuth flow and obtain the access token prior to making the API call, as well as refreshing the token as needed.

### Obtaining an access token for testing

The MCP inspector can guide you through the process of obtaining an access token for testing purposes.

1. Run the inspector with the following command. You need Node.js installed on your machine.

   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. In the sidebar on the left, for "Transport type", select either "SSE" or "Streamable HTTP".
3. Enter the URL of the MCP server.
4. In the right area, click on the "Open Auth Settings" button after "Need to configure authentication?".
5. Click "Quick OAuth Flow" and authorize on the OAuth screen.
6. Follow the steps in the "OAuth Flow Progress" section of the inspector and click "Continue" until you reach "Authentication complete".
7. Copy the `access_token` value.
8. Paste it into the `authorization_token` field in your MCP server configuration.

### Using the access token

Once you've obtained an access token using either OAuth flow above, you can use it in your MCP server configuration:

```json
{
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://example-server.modelcontextprotocol.io/sse",
      "name": "authenticated-server",
      "authorization_token": "YOUR_ACCESS_TOKEN_HERE"
    }
  ]
}
```

For detailed explanations of the OAuth flow, refer to the [Authorization section](https://modelcontextprotocol.io/docs/concepts/authentication) in the MCP specification.

## Migration guide

If you're using the deprecated `mcp-client-2025-04-04` beta header, follow this guide to migrate to the new version.

### Key changes

1. **New beta header**: Change from `mcp-client-2025-04-04` to `mcp-client-2025-11-20`
2. **Tool configuration moved**: Tool configuration now lives in the `tools` array as MCPToolset objects, not in the MCP server definition
3. **More flexible configuration**: New pattern supports allowlisting, denylisting, and per-tool configuration

### Migration steps

**Before (deprecated):**

```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 1000,
  "messages": [...],
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://mcp.example.com/sse",
      "name": "example-mcp",
      "authorization_token": "YOUR_TOKEN",
      "tool_configuration": {
        "enabled": true,
        "allowed_tools": ["tool1", "tool2"]
      }
    }
  ]
}
```

**After (current):**

```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 1000,
  "messages": [...],
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://mcp.example.com/sse",
      "name": "example-mcp",
      "authorization_token": "YOUR_TOKEN"
    }
  ],
  "tools": [
    {
      "type": "mcp_toolset",
      "mcp_server_name": "example-mcp",
      "default_config": {
        "enabled": false
      },
      "configs": {
        "tool1": {
          "enabled": true
        },
        "tool2": {
          "enabled": true
        }
      }
    }
  ]
}
```

### Common migration patterns

| Old pattern | New pattern |
|-------------|-------------|
| No `tool_configuration` (all tools enabled) | MCPToolset with no `default_config` or `configs` |
| `tool_configuration.enabled: false` | MCPToolset with `default_config.enabled: false` |
| `tool_configuration.allowed_tools: [...]` | MCPToolset with `default_config.enabled: false` and specific tools enabled in `configs` |

## Deprecated version: mcp-client-2025-04-04

<Note type="warning">
  This version is deprecated. Please migrate to `mcp-client-2025-11-20` using the [migration guide](#migration-guide) above.
</Note>

The previous version of the MCP connector included tool configuration directly in the MCP server definition:

```json
{
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://example-server.modelcontextprotocol.io/sse",
      "name": "example-mcp",
      "authorization_token": "YOUR_TOKEN",
      "tool_configuration": {
        "enabled": true,
        "allowed_tools": ["example_tool_1", "example_tool_2"]
      }
    }
  ]
}
```

### Deprecated field descriptions

| Property | Type | Description |
|----------|------|-------------|
| `tool_configuration` | object | **Deprecated**: Use MCPToolset in the `tools` array instead |
| `tool_configuration.enabled` | boolean | **Deprecated**: Use `default_config.enabled` in MCPToolset |
| `tool_configuration.allowed_tools` | array | **Deprecated**: Use allowlist pattern with `configs` in MCPToolset |