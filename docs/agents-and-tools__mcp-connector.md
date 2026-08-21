---
title: MCP connector
url: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector
description: Connect to remote MCP servers directly from the Messages API without an MCP client, and allowlist, denylist, or configure individual tools.
---

## Compatibility
- Status: Beta
- [Beta header](https://platform.claude.com/docs/en/api/beta-headers): `mcp-client-2025-11-20`
- [ZDR](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention): not eligible
- Platforms: Claude API (beta), Claude Platform on AWS (beta), Microsoft Foundry (beta) [1]; not available on Amazon Bedrock, Google Cloud
1. On [Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry), the MCP connector requires a [Hosted on Anthropic deployment](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure).

Claude's Model Context Protocol (MCP) connector feature enables you to connect to remote MCP servers directly from the Messages API without a separate MCP client.

<Note>
  The previous version of this feature (`mcp-client-2025-04-04`) is deprecated. See [Deprecated version: mcp-client-2025-04-04](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector#deprecated-version-mcp-client-2025-04-04).
</Note>

## Key features

* **Direct API integration:** Connect to MCP servers without implementing an MCP client
* **Tool calling support:** Access MCP tools through the Messages API
* **Flexible tool configuration:** Enable all tools, allowlist specific tools, or denylist unwanted tools
* **Per-tool configuration:** Configure individual tools with custom settings
* **OAuth authentication:** Support for OAuth Bearer tokens for authenticated servers
* **Multiple servers:** Connect to multiple MCP servers in a single request

## When Claude uses MCP tools

Once an MCP server is connected, Claude calls its tools when the user's request maps to a tool's described capability, either explicitly ("search Jira for open bugs") or implicitly ("what's blocking the release?" with a Jira server attached).

Claude does **not** call an MCP tool for general knowledge questions about a connected service. Asking "how do Notion databases work?" with a Notion server attached is answered directly; asking "what's in my Projects database?" triggers the tool.

You can steer how readily Claude calls MCP tools through your system prompt. See [When Claude uses tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview#when-claude-uses-tools) for general guidance and example phrasings.

## Limitations

* Of the feature set of the [MCP specification](https://modelcontextprotocol.io/introduction#explore-mcp), only [tool calls](https://modelcontextprotocol.io/docs/concepts/tools) are currently supported.
* The server must be publicly exposed through HTTP (supports both Streamable HTTP and SSE transports). Local STDIO servers cannot be connected directly.

## Using the MCP connector in the Messages API

The MCP connector uses two components:

1. **MCP server definition** (`mcp_servers` array): Defines server connection details (URL, authentication)
2. **MCP toolset** (`tools` array): Configures which tools to enable and how to configure them

### Basic example

This example enables all tools from an MCP server with default configuration:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: mcp-client-2025-11-20" \
    -d '{
      "model": "claude-opus-5",
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

  ```bash CLI
  ant beta:messages create --beta mcp-client-2025-11-20 <<'YAML'
  model: claude-opus-5
  max_tokens: 1000
  messages:
    - role: user
      content: What tools do you have available?
  mcp_servers:
    - type: url
      url: https://example-server.modelcontextprotocol.io/sse
      name: example-mcp
      authorization_token: YOUR_TOKEN
  tools:
    - type: mcp_toolset
      mcp_server_name: example-mcp
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=1000,
      messages=[{"role": "user", "content": "What tools do you have available?"}],
      mcp_servers=[
          {
              "type": "url",
              "url": "https://example-server.modelcontextprotocol.io/sse",
              "name": "example-mcp",
              "authorization_token": "YOUR_TOKEN",
          }
      ],
      tools=[{"type": "mcp_toolset", "mcp_server_name": "example-mcp"}],
      betas=["mcp-client-2025-11-20"],
  )

  print(response)
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  const response = await anthropic.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 1000,
    messages: [
      {
        role: "user",
        content: "What tools do you have available?"
      }
    ],
    mcp_servers: [
      {
        type: "url",
        url: "https://example-server.modelcontextprotocol.io/sse",
        name: "example-mcp",
        authorization_token: "YOUR_TOKEN"
      }
    ],
    tools: [
      {
        type: "mcp_toolset",
        mcp_server_name: "example-mcp"
      }
    ],
    betas: ["mcp-client-2025-11-20"]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1000,
      Messages = new List<BetaMessageParam>
      {
          new() { Role = Role.User, Content = "What tools do you have available?" }
      },
      McpServers = new List<BetaRequestMcpServerUrlDefinition>
      {
          new()
          {
              Url = "https://example-server.modelcontextprotocol.io/sse",
              Name = "example-mcp",
              AuthorizationToken = "YOUR_TOKEN"
          }
      },
      Tools = new List<BetaToolUnion>
      {
          new BetaMcpToolset("example-mcp")
      },
      Betas = [AnthropicBeta.McpClient2025_11_20]
  };

  var message = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1000,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("What tools do you have available?")),
  	},
  	MCPServers: []anthropic.BetaRequestMCPServerURLDefinitionParam{
  		{
  			URL:                "https://example-server.modelcontextprotocol.io/sse",
  			Name:               "example-mcp",
  			AuthorizationToken: anthropic.String("YOUR_TOKEN"),
  		},
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfMCPToolset: &anthropic.BetaMCPToolsetParam{
  			MCPServerName: "example-mcp",
  		}},
  	},
  	Betas: []anthropic.AnthropicBeta{
  		anthropic.AnthropicBetaMCPClient2025_11_20,
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaMcpToolset;
  // ...
  import com.anthropic.models.beta.messages.BetaRequestMcpServerUrlDefinition;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1000L)
          .addUserMessage("What tools do you have available?")
          .addMcpServer(BetaRequestMcpServerUrlDefinition.builder()
              .url("https://example-server.modelcontextprotocol.io/sse")
              .name("example-mcp")
              .authorizationToken("YOUR_TOKEN")
              .build())
          .addTool(BetaMcpToolset.builder()
              .mcpServerName("example-mcp")
              .build())
          .addBeta(AnthropicBeta.MCP_CLIENT_2025_11_20)
          .build();

      BetaMessage response = client.beta().messages().create(params);
      IO.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 1000,
      messages: [
          ['role' => 'user', 'content' => 'What tools do you have available?']
      ],
      model: 'claude-opus-5',
      mcpServers: [
          [
              'type' => 'url',
              'url' => 'https://example-server.modelcontextprotocol.io/sse',
              'name' => 'example-mcp',
              'authorization_token' => 'YOUR_TOKEN',
          ],
      ],
      tools: [
          [
              'type' => 'mcp_toolset',
              'mcp_server_name' => 'example-mcp',
          ],
      ],
      betas: ['mcp-client-2025-11-20'],
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 1000,
    messages: [
      { role: "user", content: "What tools do you have available?" }
    ],
    mcp_servers: [
      {
        type: "url",
        url: "https://example-server.modelcontextprotocol.io/sse",
        name: "example-mcp",
        authorization_token: "YOUR_TOKEN"
      }
    ],
    tools: [
      {
        type: "mcp_toolset",
        mcp_server_name: "example-mcp"
      }
    ],
    betas: ["mcp-client-2025-11-20"]
  )

  puts response
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

| Property              | Type   | Required | Description                                                                                                                                                                                                                                                                                                            |
| --------------------- | ------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`                | string | Yes      | Currently only "url" is supported.                                                                                                                                                                                                                                                                                     |
| `url`                 | string | Yes      | The URL of the MCP server. Must start with https\://.                                                                                                                                                                                                                                                                  |
| `name`                | string | Yes      | A unique identifier for this MCP server. Must be referenced by exactly one MCPToolset in the `tools` array.                                                                                                                                                                                                            |
| `authorization_token` | string | No       | OAuth authorization token if required by the MCP server. See [Authentication](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector#authentication) for how to obtain one, or the [MCP specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) for protocol details. |

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

| Property          | Type   | Required | Description                                                                                                                             |
| ----------------- | ------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `type`            | string | Yes      | Must be "mcp\_toolset".                                                                                                                 |
| `mcp_server_name` | string | Yes      | Must match a server name defined in the `mcp_servers` array.                                                                            |
| `default_config`  | object | No       | Default configuration applied to all tools in this set. Individual tool configs in `configs` override these defaults.                   |
| `configs`         | object | No       | Per-tool configuration overrides. Keys are tool names, values are configuration objects.                                                |
| `cache_control`   | object | No       | [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) cache breakpoint configuration for this toolset. |

### Tool configuration options

Each tool (whether configured in `default_config` or in `configs`) supports the following fields:

| Property        | Type    | Default | Description                                                                                                                                                                 |
| --------------- | ------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `enabled`       | boolean | `true`  | Whether this tool is enabled.                                                                                                                                               |
| `defer_loading` | boolean | `false` | If true, tool description is not sent to the model initially. Used with [Tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool). |

For the full directory of Anthropic-provided tools and optional properties such as `defer_loading`, see the [Tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference). For searching across large tool sets, see [Tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool).

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

* `search_events`: `enabled: false` (from configs), `defer_loading: true` (from default\_config)
* All other tools: `enabled: true` (system default), `defer_loading: true` (from default\_config)

## Common configuration patterns

### Enable all tools with default configuration

The simplest pattern: enable all tools from a server:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-calendar-mcp"
}
```

### Allowlist: enable only specific tools

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

### Denylist: disable specific tools

Enable all tools by default, then explicitly disable unwanted tools. Denylisting write or destructive tools is recommended when building read-only assistants, or when you want a human confirmation step before state changes:

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

### Mixed: allowlist with per-tool configuration

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

* `search_events` is enabled with `defer_loading: false`
* `list_events` is enabled with `defer_loading: true` (inherited from default\_config)
* All other tools are disabled

## Validation rules

The API enforces these validation rules:

* **Server must exist:** The `mcp_server_name` in an MCPToolset must match a server defined in the `mcp_servers` array
* **Server must be used:** Every MCP server defined in `mcp_servers` must be referenced by exactly one MCPToolset
* **Unique toolset per server:** Each MCP server can only be referenced by one MCPToolset
* **Unknown tool names:** If a tool name in `configs` doesn't exist on the MCP server, a backend warning is logged but no error is returned (MCP servers may have dynamic tool availability)

## Response content types

When Claude uses MCP tools, the response includes two new content block types:

### MCP tool use block

```json
{
  "type": "mcp_tool_use",
  "id": "mcptoolu_014Q35RayjACSWkSj4X2yov1",
  "name": "echo",
  "server_name": "example-mcp",
  "input": { "param1": "value1", "param2": "value2" }
}
```

### MCP tool result block

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
  "model": "claude-opus-5",
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

With many tools available, Claude selects based on tool names and descriptions. Clear, specific tool descriptions improve selection accuracy. For large tool sets (dozens of tools across several servers), consider enabling [`defer_loading`](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector#tool-configuration-options) with the [Tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) so only relevant tools are surfaced per query.

## Authentication

For MCP servers that require OAuth authentication, you'll need to obtain an access token. The MCP connector beta supports passing an `authorization_token` parameter in the MCP server definition. API consumers are expected to handle the OAuth flow and obtain the access token prior to making the API call, and to refresh the token as needed.

### Obtaining an access token for testing

The MCP inspector can guide you through the process of obtaining an access token for testing purposes.

1. Run the inspector with the following command. You need Node.js installed on your machine.

   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. In the sidebar on the left, for **Transport type**, select either **SSE** or **Streamable HTTP**.

3. Enter the URL of the MCP server.

4. In the right area, click **Open Auth Settings** after **Need to configure authentication?**.

5. Click **Quick OAuth Flow** and authorize on the OAuth screen.

6. Follow the steps in the **OAuth Flow Progress** section of the inspector and click **Continue** until you reach **Authentication complete**.

7. Copy the `access_token` value.

8. Paste it into the `authorization_token` field in your MCP server configuration.

### Using the access token

Once you've obtained an access token using either of the preceding OAuth flows, you can use it in your MCP server configuration:

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

For detailed explanations of the OAuth flow, refer to the [Authorization section](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) in the MCP specification.

## Client-side MCP helpers

If you manage your own MCP client connection (for example, with local stdio servers, MCP prompts, or MCP resources), the SDKs provide helper functions that convert between MCP types and Claude API types. This eliminates manual conversion code when using an MCP SDK for your language (for example, the [TypeScript MCP SDK](https://github.com/modelcontextprotocol/typescript-sdk)) alongside the Anthropic SDK.

<Note>
  Use the [`mcp_servers` API parameter](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector#using-the-mcp-connector-in-the-messages-api) when you have remote servers accessible by URL and only need tool support. Use the client-side helpers when you need local servers, prompts, resources, or more control over the connection with the base SDK.
</Note>

### Installation

Install both the Anthropic SDK and the MCP SDK:

<Tabs>
  <Tab title="Python">
    The MCP helpers are included in the `mcp` extra, which requires Python 3.10 or later:

    ```bash
    pip install "anthropic[mcp]"
    ```
  </Tab>

  <Tab title="TypeScript">
    ```bash
    npm install @anthropic-ai/sdk @modelcontextprotocol/sdk
    ```
  </Tab>

  <Tab title="C#">
    The helpers live in the separate `Anthropic.Mcp` package; the MCP client itself comes from the official [ModelContextProtocol package](https://www.nuget.org/packages/ModelContextProtocol):

    ```bash
    dotnet add package Anthropic.Mcp
    dotnet add package ModelContextProtocol
    ```
  </Tab>

  <Tab title="Go">
    The helpers live in the `mcp` subpackage of the Go SDK, which builds on the [MCP Go SDK](https://github.com/modelcontextprotocol/go-sdk):

    ```bash
    go get github.com/anthropics/anthropic-sdk-go/mcp
    ```
  </Tab>

  <Tab title="Java">
    The helpers live in the separate `anthropic-java-mcp` artifact, which requires Java 17 or later (the core SDK supports Java 8):

    <Tabs>
      <Tab title="Gradle">
        ```kotlin
        implementation("com.anthropic:anthropic-java-mcp:2.57.0")
        ```
      </Tab>

      <Tab title="Maven">
        ```xml
        <dependency>
            <groupId>com.anthropic</groupId>
            <artifactId>anthropic-java-mcp</artifactId>
            <version>2.57.0</version>
        </dependency>
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="PHP">
    The helpers use the official [MCP PHP SDK](https://packagist.org/packages/mcp/sdk):

    ```bash
    composer require "anthropic-ai/sdk" "guzzlehttp/guzzle:^7" "mcp/sdk"
    ```
  </Tab>

  <Tab title="Ruby">
    The helpers use the official [`mcp` gem](https://rubygems.org/gems/mcp):

    ```bash
    bundle add anthropic mcp
    ```
  </Tab>
</Tabs>

### Available helpers

Import the helpers for your language:

<CodeGroup exclude="shell">
  ```python Python
  from anthropic.lib.tools.mcp import (
      async_mcp_tool,
      mcp_message,
      mcp_resource_to_content,
      mcp_resource_to_file,
  )
  ```

  ```typescript TypeScript
  import {
    mcpTools,
    mcpMessages,
    mcpResourceToContent,
    mcpResourceToFile
  } from "@anthropic-ai/sdk/helpers/beta/mcp";
  ```

  ```csharp C#
  using Anthropic.Helpers.Beta;
  using Anthropic.Helpers.Beta.Mcp;
  ```

  ```go Go
  import (
  	"github.com/anthropics/anthropic-sdk-go/mcp"
  )

  ```

  ```java Java
  import com.anthropic.helpers.McpBetaTool;
  import com.anthropic.mcp.BetaMcp;
  ```

  ```php PHP
  use Anthropic\Lib\Tools\BetaMcp;
  ```

  ```ruby Ruby
  require "anthropic"

  # The helpers are exposed on the Anthropic::Mcp module
  ```
</CodeGroup>

Helper names and exact signatures follow each language's conventions; this table shows the TypeScript forms:

| Helper                           | Description                                                                             |
| -------------------------------- | --------------------------------------------------------------------------------------- |
| `mcpTools(tools, mcpClient)`     | Converts MCP tools to Claude API tools for use with `client.beta.messages.toolRunner()` |
| `mcpMessages(messages)`          | Converts MCP prompt messages to Claude API message format                               |
| `mcpResourceToContent(resource)` | Converts an MCP resource to a Claude API content block                                  |
| `mcpResourceToFile(resource)`    | Converts an MCP resource to a file object for upload                                    |

### Use MCP tools

Convert MCP tools for use with the SDK's [tool runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner), which handles tool execution automatically:

<CodeGroup exclude="shell">
  ```python Python
  from anthropic.lib.tools.mcp import async_mcp_tool
  from mcp import ClientSession
  from mcp.client.stdio import StdioServerParameters, stdio_client

  client = AsyncAnthropic()


  async def main() -> None:
      # Connect to an MCP server
      server_params = StdioServerParameters(command="mcp-server")
      async with stdio_client(server_params) as (read, write):
          async with ClientSession(read, write) as mcp_client:
              await mcp_client.initialize()

              # List tools and convert them for the Claude API
              tools_result = await mcp_client.list_tools()
              runner = client.beta.messages.tool_runner(
                  model="claude-opus-5",
                  max_tokens=1024,
                  messages=[
                      {"role": "user", "content": "What tools do you have available?"},
                  ],
                  tools=[async_mcp_tool(tool, mcp_client) for tool in tools_result.tools],
              )

              final_message = await runner.until_done()
              print(final_message)


  asyncio.run(main())
  ```

  ```typescript TypeScript
  import {
    mcpTools,
    type MCPCallToolResultLike,
    type MCPClientLike
  } from "@anthropic-ai/sdk/helpers/beta/mcp";
  import { Client } from "@modelcontextprotocol/sdk/client/index.js";
  import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

  const anthropic = new Anthropic();

  // Connect to an MCP server
  const transport = new StdioClientTransport({ command: "mcp-server", args: [] });
  const mcpClient = new Client({ name: "my-client", version: "1.0.0" });
  await mcpClient.connect(transport);

  // List tools and convert them for the Claude API
  const { tools } = await mcpClient.listTools();

  // The MCP SDK's callTool return type still includes a legacy result shape that
  // mcpTools does not accept; narrow it. Drop this once MCPClientLike widens.
  const mcpClientForTools: MCPClientLike = {
    callTool: (params) => mcpClient.callTool(params) as Promise<MCPCallToolResultLike>
  };

  const finalMessage = await anthropic.beta.messages.toolRunner({
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "What tools do you have available?" }],
    tools: mcpTools(tools, mcpClientForTools)
  });

  console.log(finalMessage);
  ```

  ```csharp C#
  using Anthropic.Helpers.Beta;
  using Anthropic.Helpers.Beta.Mcp;
  using Anthropic.Models.Beta.Messages;
  using ModelContextProtocol.Client;
  using Messages = Anthropic.Models.Messages;

  var anthropic = new AnthropicClient();

  // Connect to an MCP server
  await using var mcpClient = await McpClient.CreateAsync(
      new StdioClientTransport(new StdioClientTransportOptions { Command = "mcp-server" })
  );

  // List tools and convert them for the Claude API
  var tools = await BetaMcp.ListToolsAsync(mcpClient);
  var runner = anthropic.Beta.Messages.ToolRunner(
      new MessageCreateParams
      {
          Model = Messages::Model.ClaudeOpus5,
          MaxTokens = 1024,
          Messages =
          [
              new BetaMessageParam
              {
                  Role = Role.User,
                  Content = "What tools do you have available?",
              },
          ],
      },
      tools
  );

  var finalMessage = await runner.RunUntilDoneAsync();
  Console.WriteLine(finalMessage);
  ```

  ```go Go
  import (
  // ...

  // ...
  	"github.com/anthropics/anthropic-sdk-go/mcp"
  	mcpsdk "github.com/modelcontextprotocol/go-sdk/mcp"
  )

  func main() {
  	client := anthropic.NewClient()
  	ctx := context.Background()

  	// Connect to an MCP server
  	mcpClient := mcpsdk.NewClient(&mcpsdk.Implementation{Name: "my-client", Version: "1.0.0"}, nil)
  	session, err := mcpClient.Connect(ctx, &mcpsdk.CommandTransport{Command: exec.Command("mcp-server")}, nil)
  	if err != nil {
  		log.Fatal(err)
  	}
  	defer session.Close()

  	// List tools and convert them for the Claude API
  	toolsResult, err := session.ListTools(ctx, nil)
  	if err != nil {
  		log.Fatal(err)
  	}
  	betaTools, err := mcp.NewBetaTools(toolsResult.Tools, session)
  	if err != nil {
  		log.Fatal(err)
  	}

  	runner := client.Beta.Messages.NewToolRunner(betaTools, anthropic.BetaToolRunnerParams{
  		BetaMessageNewParams: anthropic.BetaMessageNewParams{
  			Model:     anthropic.ModelClaudeOpus5,
  			MaxTokens: 1024,
  			Messages: []anthropic.BetaMessageParam{
  				anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("What tools do you have available?")),
  			},
  		},
  	})

  	finalMessage, err := runner.RunToCompletion(ctx)
  	if err != nil {
  		log.Fatal(err)
  	}
  	fmt.Println(finalMessage.RawJSON())
  }

  ```

  ```java Java
  import com.anthropic.helpers.BetaToolRunner;
  import com.anthropic.helpers.McpBetaTool;
  import com.anthropic.mcp.BetaMcp;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import io.modelcontextprotocol.client.McpClient;
  import io.modelcontextprotocol.client.McpSyncClient;
  import io.modelcontextprotocol.client.transport.ServerParameters;
  import io.modelcontextprotocol.client.transport.StdioClientTransport;
  import io.modelcontextprotocol.json.McpJsonDefaults;
  import io.modelcontextprotocol.spec.McpSchema;
  // ...

  void main() throws Exception {
      AnthropicClient anthropic = AnthropicOkHttpClient.fromEnv();

      // Connect to an MCP server
      StdioClientTransport transport = new StdioClientTransport(
              ServerParameters.builder("mcp-server").build(), McpJsonDefaults.getMapper());

      try (McpSyncClient mcpClient = McpClient.sync(transport)
              .clientInfo(new McpSchema.Implementation("my-client", "1.0.0"))
              .build()) {

          mcpClient.initialize();

          // List tools and convert them for the Claude API
          List<McpBetaTool> betaTools = BetaMcp.mcpTools(mcpClient.listTools().tools(), mcpClient);

          MessageCreateParams params = MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5)
                  .maxTokens(1024L)
                  .addUserMessage("What tools do you have available?")
                  .addTools(betaTools)
                  .build();

          // The runner yields one message per assistant turn; the last is the final response
          BetaToolRunner runner = anthropic.beta().messages().toolRunner(params);
          BetaMessage finalMessage = null;
          for (BetaMessage message : runner) {
              finalMessage = message;
          }
          IO.println(finalMessage);
      }
  }
  ```

  ```php PHP
  use Anthropic\Lib\Tools\BetaMcp;
  use Mcp\Client;
  use Mcp\Client\Transport\HttpTransport;

  $anthropic = new Anthropic();

  // Connect to an MCP server. The PHP MCP client connects over HTTP; point this
  // at your server's endpoint.
  $mcp = Client::builder()->build();
  $mcp->connect(new HttpTransport('http://localhost:8000/mcp'));

  // List tools and convert them for the Claude API
  $runner = $anthropic->beta->messages->toolRunner(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'What tools do you have available?']],
      model: 'claude-opus-5',
      tools: BetaMcp::tools($mcp->listTools()->tools, $mcp),
  );

  echo $runner->runUntilDone(), "\n";
  ```

  ```ruby Ruby
  require "mcp"

  anthropic = Anthropic::Client.new

  # Connect to an MCP server
  transport = MCP::Client::Stdio.new(command: "mcp-server")
  mcp_client = MCP::Client.new(transport: transport)
  mcp_client.connect

  # List tools and convert them for the Claude API
  runner = anthropic.beta.messages.tool_runner(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "What tools do you have available?" }],
    tools: Anthropic::Mcp.tools(mcp_client.tools, mcp_client)
  )

  final_message = runner.run_until_finished.last
  puts final_message
  ```
</CodeGroup>

### Use MCP prompts

Convert MCP prompt messages into Claude API message format:

<CodeGroup exclude="shell">
  ```python Python
  from anthropic.lib.tools.mcp import mcp_message

  prompt = await mcp_client.get_prompt(name="my-prompt")
  response = await client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[mcp_message(message) for message in prompt.messages],
  )

  print(response)
  ```

  ```typescript TypeScript
  import { mcpMessages } from "@anthropic-ai/sdk/helpers/beta/mcp";

  const { messages } = await mcpClient.getPrompt({ name: "my-prompt" });
  const response = await anthropic.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: mcpMessages(messages)
  });

  console.log(response);
  ```

  ```csharp C#
  var prompt = await mcpClient.GetPromptAsync("my-prompt");
  var response = await anthropic.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Messages::Model.ClaudeOpus5,
          MaxTokens = 1024,
          Messages = BetaMcp.Messages(prompt.Messages),
      }
  );

  Console.WriteLine(response);
  ```

  ```go Go
  prompt, err := session.GetPrompt(ctx, &mcpsdk.GetPromptParams{Name: "my-prompt"})
  if err != nil {
  	log.Fatal(err)
  }

  messages := make([]anthropic.BetaMessageParam, 0, len(prompt.Messages))
  for _, promptMessage := range prompt.Messages {
  	message, err := mcp.ToMessage(promptMessage)
  	if err != nil {
  		log.Fatal(err)
  	}
  	messages = append(messages, message)
  }

  response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages:  messages,
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.RawJSON())
  ```

  ```java Java
  McpSchema.GetPromptResult prompt = mcpClient.getPrompt(
          new McpSchema.GetPromptRequest("my-prompt", Map.of()));

  BetaMessage response = anthropic.beta().messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024L)
          .messages(BetaMcp.mcpMessages(prompt.messages()))
          .build());

  IO.println(response);
  ```

  ```php PHP
  $prompt = $mcp->getPrompt('my-prompt');

  $response = $anthropic->beta->messages->create(
      maxTokens: 1024,
      messages: array_map(BetaMcp::message(...), $prompt->messages),
      model: 'claude-opus-5',
  );

  echo $response, "\n";
  ```

  ```ruby Ruby
  prompt = mcp_client.get_prompt(name: "my-prompt")

  response = anthropic.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: prompt["messages"].map { |message| Anthropic::Mcp.message(message) }
  )

  puts response
  ```
</CodeGroup>

### Use MCP resources

Convert MCP resources into content blocks to include in messages, or into file objects for upload:

<CodeGroup exclude="shell">
  ```python Python
  from anthropic.lib.tools.mcp import (
      mcp_resource_to_content,
      mcp_resource_to_file,
  )

  # As a content block in a message
  resource = await mcp_client.read_resource(uri="file:///path/to/doc.txt")
  response = await client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": [
                  mcp_resource_to_content(resource),
                  {"type": "text", "text": "Summarize this document"},
              ],
          }
      ],
  )
  print(response)

  # As a file upload
  file_resource = await mcp_client.read_resource(
      uri="file:///path/to/data.json",
  )
  uploaded = await client.files.upload(
      file=mcp_resource_to_file(file_resource),
  )
  print(uploaded.id)
  ```

  ```typescript TypeScript
  import { mcpResourceToContent, mcpResourceToFile } from "@anthropic-ai/sdk/helpers/beta/mcp";

  // As a content block in a message
  const resource = await mcpClient.readResource({ uri: "file:///path/to/doc.txt" });
  const response = await anthropic.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          mcpResourceToContent(resource),
          { type: "text", text: "Summarize this document" }
        ]
      }
    ]
  });
  console.log(response);

  // As a file upload
  const fileResource = await mcpClient.readResource({ uri: "file:///path/to/data.json" });
  const uploaded = await anthropic.files.upload({ file: mcpResourceToFile(fileResource) });
  console.log(uploaded.id);
  ```

  ```csharp C#
  // As a content block in a message
  var resource = await mcpClient.ReadResourceAsync("file:///path/to/doc.txt");
  var response = await anthropic.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Messages::Model.ClaudeOpus5,
          MaxTokens = 1024,
          Messages =
          [
              new BetaMessageParam
              {
                  Role = Role.User,
                  Content = new BetaMessageParamContent(
                      [
                          BetaMcp.ResourceToContent(resource),
                          new BetaTextBlockParam { Text = "Summarize this document" },
                      ]
                  ),
              },
          ],
      }
  );

  Console.WriteLine(response);

  // As a file upload
  var fileResource = await mcpClient.ReadResourceAsync("file:///path/to/data.json");
  var (filename, data, mediaType) = BetaMcp.ResourceToFile(fileResource);

  // Build the file part explicitly so the resource's filename and MIME type
  // carry through to the upload.
  var file = new BinaryContent { Stream = new MemoryStream(data), FileName = filename };
  if (mediaType is not null)
  {
      file.ContentType = new(mediaType);
  }

  var uploaded = await anthropic.Files.Upload(new FileUploadParams { File = file });
  Console.WriteLine(uploaded.ID);
  ```

  ```go Go
  // As a content block in a message
  resource, err := session.ReadResource(ctx, &mcpsdk.ReadResourceParams{URI: "file:///path/to/doc.txt"})
  if err != nil {
  	log.Fatal(err)
  }
  block, err := mcp.ResourceToBlock(resource)
  if err != nil {
  	log.Fatal(err)
  }

  response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(
  			// ResourceToBlock returns the tool-result content union; message
  			// content is a separate union type, so re-wrap the shared variants
  			// (mcp.ToMessage does the same internally).
  			anthropic.BetaContentBlockParamUnion{
  				OfText:     block.OfText,
  				OfImage:    block.OfImage,
  				OfDocument: block.OfDocument,
  			},
  			anthropic.NewBetaTextBlock("Summarize this document"),
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.RawJSON())

  // As a file upload
  fileResult, err := session.ReadResource(ctx, &mcpsdk.ReadResourceParams{URI: "file:///path/to/data.json"})
  if err != nil {
  	log.Fatal(err)
  }
  fileReader, err := mcp.ResourceToFile(fileResult)
  if err != nil {
  	log.Fatal(err)
  }
  uploaded, err := client.Files.Upload(ctx, anthropic.FileUploadParams{File: fileReader})
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(uploaded.ID)
  ```

  ```java Java
  // As a content block in a message
  McpSchema.ReadResourceResult resource = mcpClient.readResource(
          new McpSchema.ReadResourceRequest("file:///path/to/doc.txt"));

  List<BetaContentBlockParam> content =
          new ArrayList<>(BetaMcp.mcpResourceContents(resource));
  content.add(BetaContentBlockParam.ofText(
          BetaTextBlockParam.builder().text("Summarize this document").build()));

  BetaMessage response = anthropic.beta().messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024L)
          .addUserMessageOfBetaContentBlockParams(content)
          .build());

  IO.println(response);

  // As a file upload
  McpSchema.ReadResourceResult fileResource = mcpClient.readResource(
          new McpSchema.ReadResourceRequest("file:///path/to/data.json"));

  McpResourceFile resourceFile = BetaMcp.mcpResourceFiles(fileResource).getFirst();

  // Build the file part explicitly so the resource's filename and MIME type
  // carry through to the upload.
  MultipartField.Builder<InputStream> fileField = MultipartField.<InputStream>builder()
          .value(new ByteArrayInputStream(resourceFile.content()))
          .filename(resourceFile.filename());
  if (resourceFile.mimeType() != null) {
      fileField.contentType(resourceFile.mimeType());
  }

  var uploaded = anthropic.files().upload(FileUploadParams.builder()
          .file(fileField.build())
          .build());

  IO.println(uploaded.id());
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  // As a content block in a message
  $resource = $mcp->readResource('file:///path/to/doc.txt');

  $response = $anthropic->beta->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  BetaMcp::resourceToContent($resource),
                  ['type' => 'text', 'text' => 'Summarize this document'],
              ],
          ],
      ],
      model: 'claude-opus-5',
  );

  echo $response, "\n";

  // As a file upload
  $fileResource = $mcp->readResource('file:///path/to/data.json');
  $file = $anthropic->beta->files->upload(file: BetaMcp::resourceToFile($fileResource));
  echo $file->id, "\n";
  ```

  ```ruby Ruby
  # As a content block in a message
  resource = mcp_client.read_resource(uri: "file:///path/to/doc.txt")

  response = anthropic.beta.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          *Anthropic::Mcp.resource_to_contents(resource),
          { type: "text", text: "Summarize this document" }
        ]
      }
    ]
  )

  puts response

  # As a file upload
  file_resource = mcp_client.read_resource(uri: "file:///path/to/data.json")
  file = Anthropic::Mcp.resource_to_files(file_resource).first
  uploaded_file = anthropic.files.upload(file: file)
  puts uploaded_file.id
  ```
</CodeGroup>

### Error handling

The conversion functions throw `UnsupportedMCPValueError` if an MCP value isn't supported by the Claude API (in Go, the helpers return an `UnsupportedValueError`; in Java and C#, they throw `AnthropicInvalidDataException`). This can happen with unsupported content types, MIME types, or resource links (resolve resource links with your MCP client before converting).

## Batch requests

You can include `mcp_servers` in [Message Batches API](https://platform.claude.com/docs/en/build-with-claude/batch-processing) requests. MCP tool calls through the Batches API are priced the same as those in regular Messages API requests.

## Data retention

The MCP connector is not covered by ZDR arrangements. Data exchanged with MCP servers, including tool definitions and execution results, is retained according to Anthropic's standard data retention policy.

For ZDR eligibility across all features, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).

## Migration guide

If you're using the deprecated `mcp-client-2025-04-04` beta header, follow this guide to migrate to the new version.

### Key changes

1. **New beta header:** Change from `mcp-client-2025-04-04` to `mcp-client-2025-11-20`
2. **Tool configuration moved:** Tool configuration now lives in the `tools` array as MCPToolset objects, not in the MCP server definition
3. **More flexible configuration:** New pattern supports allowlisting, denylisting, and per-tool configuration

### Migration steps

**Before (deprecated):**

```json
{
  "model": "claude-opus-5",
  "max_tokens": 1000,
  "messages": [
    // ...
  ],
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
  "model": "claude-opus-5",
  "max_tokens": 1000,
  "messages": [
    // ...
  ],
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

| Old pattern                                 | New pattern                                                                             |
| ------------------------------------------- | --------------------------------------------------------------------------------------- |
| No `tool_configuration` (all tools enabled) | MCPToolset with no `default_config` or `configs`                                        |
| `tool_configuration.enabled: false`         | MCPToolset with `default_config.enabled: false`                                         |
| `tool_configuration.allowed_tools: [...]`   | MCPToolset with `default_config.enabled: false` and specific tools enabled in `configs` |

## Deprecated version: mcp-client-2025-04-04

<Note type="warning">
  This version is deprecated. Migrate to `mcp-client-2025-11-20` using the preceding [migration guide](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector#migration-guide).
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

| Property                           | Type    | Description                                                        |
| ---------------------------------- | ------- | ------------------------------------------------------------------ |
| `tool_configuration`               | object  | **Deprecated:** Use MCPToolset in the `tools` array instead        |
| `tool_configuration.enabled`       | boolean | **Deprecated:** Use `default_config.enabled` in MCPToolset         |
| `tool_configuration.allowed_tools` | array   | **Deprecated:** Use allowlist pattern with `configs` in MCPToolset |
