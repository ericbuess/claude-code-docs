# MCP connector

Claude's Model Context Protocol (MCP) connector feature enables you to connect to remote MCP servers directly from the Messages API without a separate MCP client.

<Note>
  This feature requires the beta header: `"anthropic-beta": "mcp-client-2025-04-04"`
</Note>

## Key features

* **Direct API integration**: Connect to MCP servers without implementing an MCP client
* **Tool calling support**: Access MCP tools through the Messages API
* **OAuth authentication**: Support for OAuth Bearer tokens for authenticated servers
* **Multiple servers**: Connect to multiple MCP servers in a single request

## Limitations

* Of the feature set of the [MCP specification](https://modelcontextprotocol.io/introduction#explore-mcp), only [tool calls](https://modelcontextprotocol.io/docs/concepts/tools) are currently supported.
* The server must be publicly exposed through HTTP (supports both Streamable HTTP and SSE transports). Local STDIO servers cannot be connected directly.
* The MCP connector is currently not supported on Amazon Bedrock and Google Vertex.

## Using the MCP connector in the Messages API

To connect to a remote MCP server, include the `mcp_servers` parameter in your Messages API request:

<CodeGroup>
  ```bash cURL theme={null}
  curl https://api.anthropic.com/v1/messages \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: mcp-client-2025-04-04" \
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
      ]
    }'
  ```

  ```typescript TypeScript theme={null}
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
    betas: ["mcp-client-2025-04-04"],
  });
  ```

  ```python Python theme={null}
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
      betas=["mcp-client-2025-04-04"]
  )
  ```
</CodeGroup>

## MCP server configuration

Each MCP server in the `mcp_servers` array supports the following configuration:

```json  theme={null}
{
  "type": "url",
  "url": "https://example-server.modelcontextprotocol.io/sse",
  "name": "example-mcp",
  "tool_configuration": {
    "enabled": true,
    "allowed_tools": ["example_tool_1", "example_tool_2"]
  },
  "authorization_token": "YOUR_TOKEN"
}
```

### Field descriptions

| Property                           | Type    | Required | Description                                                                                                                                                     |
| ---------------------------------- | ------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`                             | string  | Yes      | Currently only "url" is supported                                                                                                                               |
| `url`                              | string  | Yes      | The URL of the MCP server. Must start with https\://                                                                                                            |
| `name`                             | string  | Yes      | A unique identifier for this MCP server. It will be used in `mcp_tool_call` blocks to identify the server and to disambiguate tools to the model.               |
| `tool_configuration`               | object  | No       | Configure tool usage                                                                                                                                            |
| `tool_configuration.enabled`       | boolean | No       | Whether to enable tools from this server (default: true)                                                                                                        |
| `tool_configuration.allowed_tools` | array   | No       | List to restrict the tools to allow (by default, all tools are allowed)                                                                                         |
| `authorization_token`              | string  | No       | OAuth authorization token if required by the MCP server. See [MCP specification](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization). |

## Response content types

When Claude uses MCP tools, the response will include two new content block types:

### MCP Tool Use Block

```json  theme={null}
{
  "type": "mcp_tool_use",
  "id": "mcptoolu_014Q35RayjACSWkSj4X2yov1",
  "name": "echo",
  "server_name": "example-mcp",
  "input": { "param1": "value1", "param2": "value2" }
}
```

### MCP Tool Result Block

```json  theme={null}
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

You can connect to multiple MCP servers by including multiple objects in the `mcp_servers` array:

```json  theme={null}
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
  ]
}
```

## Authentication

For MCP servers that require OAuth authentication, you'll need to obtain an access token. The MCP connector beta supports passing an `authorization_token` parameter in the MCP server definition.
API consumers are expected to handle the OAuth flow and obtain the access token prior to making the API call, as well as refreshing the token as needed.

### Obtaining an access token for testing

The MCP inspector can guide you through the process of obtaining an access token for testing purposes.

1. Run the inspector with the following command. You need Node.js installed on your machine.

   ```bash  theme={null}
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

```json  theme={null}
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
