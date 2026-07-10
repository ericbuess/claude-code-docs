# MCP connector

Connect MCP servers to your agents for access to external tools and data sources.

---

Claude Managed Agents supports connecting [Model Context Protocol (MCP)](https://modelcontextprotocol.io) servers to your agents. This gives the agent access to external tools, data sources, and services through a standardized protocol.

MCP configuration is split across two steps:

1. **Agent creation** declares which MCP servers the agent connects to, by name and URL.
2. **Session creation** supplies auth for those servers by referencing a pre-registered [vault](/docs/en/managed-agents/vaults).

This separation keeps secrets out of reusable agent definitions while letting each session authenticate with its own credentials.

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Declare MCP servers on the agent

Specify MCP servers in the `mcp_servers` array when creating an agent. Each server needs a `type`, a unique `name`, and a `url`. No authentication tokens are provided at this stage.

Each declared server also needs a matching `mcp_toolset` entry in the `tools` array. The toolset's `mcp_server_name` must match the server's `name`.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  agent_response=$(curl -sS --fail-with-body https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "name": "GitHub Assistant",
    "model": "claude-opus-4-8",
    "mcp_servers": [
      {
        "type": "url",
        "name": "github",
        "url": "https://api.githubcopilot.com/mcp/"
      }
    ],
    "tools": [
      {"type": "agent_toolset_20260401"},
      {"type": "mcp_toolset", "mcp_server_name": "github"}
    ]
  }
  EOF
  )
  agent_id=$(jq -r '.id' <<<"$agent_response")
  ```

  ```bash CLI
  AGENT_ID=$(ant beta:agents create \
    --name "GitHub Assistant" \
    --model claude-opus-4-8 \
    --mcp-server '{type: url, name: github, url: "https://api.githubcopilot.com/mcp/"}' \
    --tool '{type: agent_toolset_20260401}' \
    --tool '{type: mcp_toolset, mcp_server_name: github}' \
    --transform id --raw-output)
  ```

  ```python Python
  agent = client.beta.agents.create(
      name="GitHub Assistant",
      model="claude-opus-4-8",
      mcp_servers=[
          {
              "type": "url",
              "name": "github",
              "url": "https://api.githubcopilot.com/mcp/",
          },
      ],
      tools=[
          {"type": "agent_toolset_20260401"},
          {"type": "mcp_toolset", "mcp_server_name": "github"},
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "GitHub Assistant",
    model: "claude-opus-4-8",
    mcp_servers: [
      {
        type: "url",
        name: "github",
        url: "https://api.githubcopilot.com/mcp/",
      },
    ],
    tools: [
      { type: "agent_toolset_20260401" },
      { type: "mcp_toolset", mcp_server_name: "github" },
    ],
  });
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "GitHub Assistant",
      Model = BetaManagedAgentsModel.ClaudeOpus4_8,
      McpServers =
      [
          new() { Type = "url", Name = "github", Url = "https://api.githubcopilot.com/mcp/" },
      ],
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
          },
          new BetaManagedAgentsMcpToolsetParams { Type = "mcp_toolset", McpServerName = "github" },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "GitHub Assistant",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: anthropic.BetaManagedAgentsModelClaudeOpus4_8,
  	},
  	MCPServers: []anthropic.BetaManagedAgentsURLMCPServerParams{{
  		Type: anthropic.BetaManagedAgentsURLMCPServerParamsTypeURL,
  		Name: "github",
  		URL:  "https://api.githubcopilot.com/mcp/",
  	}},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{
  		{
  			OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  				Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  			},
  		},
  		{
  			OfMCPToolset: &anthropic.BetaManagedAgentsMCPToolsetParams{
  				Type:          anthropic.BetaManagedAgentsMCPToolsetParamsTypeMCPToolset,
  				MCPServerName: "github",
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("GitHub Assistant")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
          .addMcpServer(
              BetaManagedAgentsUrlMcpServerParams.builder()
                  .type(BetaManagedAgentsUrlMcpServerParams.Type.URL)
                  .name("github")
                  .url("https://api.githubcopilot.com/mcp/")
                  .build()
          )
          .addTool(
              BetaManagedAgentsAgentToolset20260401Params.builder()
                  .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                  .build()
          )
          .addTool(
              BetaManagedAgentsMcpToolsetParams.builder()
                  .type(BetaManagedAgentsMcpToolsetParams.Type.MCP_TOOLSET)
                  .mcpServerName("github")
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'GitHub Assistant',
      model: 'claude-opus-4-8',
      mcpServers: [
          BetaManagedAgentsURLMCPServerParams::with(
              type: 'url',
              name: 'github',
              url: 'https://api.githubcopilot.com/mcp/',
          ),
      ],
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
          ),
          BetaManagedAgentsMCPToolsetParams::with(
              type: 'mcp_toolset',
              mcpServerName: 'github',
          ),
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "GitHub Assistant",
    model: "claude-opus-4-8",
    mcp_servers: [
      {
        type: "url",
        name: "github",
        url: "https://api.githubcopilot.com/mcp/"
      }
    ],
    tools: [
      {type: "agent_toolset_20260401"},
      {type: "mcp_toolset", mcp_server_name: "github"}
    ]
  )
  ```
</CodeGroup>

<Tip>
  The MCP toolset defaults to a permission policy of `always_ask`, which requires user approval before each tool call. See [permission policies](/docs/en/managed-agents/permission-policies) to configure this behavior.
</Tip>

### `mcp_servers` field reference

Each entry in the `mcp_servers` array defines one connection.

| Field  | Description                                                                                                                                                                                                                                  |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type` | Required. Must be `"url"`.                                                                                                                                                                                                                   |
| `name` | Required. A unique name for this server within the agent (1–255 characters). Used as the `mcp_server_name` in the `tools` array and surfaced on MCP tool events in the [session event stream](/docs/en/managed-agents/events-and-streaming). |
| `url`  | Required. The endpoint of the remote MCP server (up to 2048 characters). See [Supported MCP server types](/docs/en/managed-agents/reference#supported-mcp-server-types) for transport requirements.                                          |

Constraints:

* An agent can declare up to 20 MCP servers. Server names must be unique within the array.
* Every `mcp_servers` entry must be referenced by an `mcp_toolset` in the `tools` array, and every `mcp_toolset` must reference a declared server. The API rejects agent definitions with unreferenced servers or dangling toolsets.

## Configure which MCP tools are available

The `mcp_toolset` entry supports the same `default_config` and `configs` shape as the built-in agent toolset, applied to the tools the MCP server exposes. The `name` in each `configs` entry is the bare tool name as reported by the server.

By default all tools exposed by the MCP server are enabled. To enable only specific tools, set `default_config.enabled` to `false` and explicitly enable the tools you want:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "github",
  "default_config": { "enabled": false },
  "configs": [
    { "name": "get_issue", "enabled": true },
    { "name": "list_issues", "enabled": true },
    { "name": "add_issue_comment", "enabled": true }
  ]
}
```

This pattern is useful when a server exposes many tools but the agent only needs a few, or when you want tools added by the server operator to stay off until you review them.

To disable specific tools while keeping the rest enabled, omit `default_config` and set `enabled: false` on individual entries:

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "github",
  "configs": [{ "name": "delete_repository", "enabled": false }]
}
```

See [configuring the toolset](/docs/en/managed-agents/tools#configuring-the-toolset) for the general `default_config` / `configs` pattern, and [MCP toolset permissions](/docs/en/managed-agents/permission-policies#mcp-toolset-permissions) for setting `permission_policy` on MCP tools and handling confirmation requests.

### MCP tool output handling

When an MCP tool output exceeds 100,000 tokens, it is automatically written to a file in the sandbox. The model receives a truncated preview with the file path and can read the full content from there.

## Provide authentication at session creation

When starting a session, pass `vault_ids` to provide credentials for your MCP servers. Vaults are collections of credentials that you register once and reference by ID. See [Authenticate with vaults](/docs/en/managed-agents/vaults) for how to create vaults and manage credentials.

<CodeGroup>
  ```bash curl
  session_response=$(curl -sS --fail-with-body https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$agent_id",
    "environment_id": "$environment_id",
    "vault_ids": ["$vault_id"]
  }
  EOF
  )
  session_id=$(jq -r '.id' <<<"$session_response")
  ```

  ```bash CLI
  SESSION_ID=$(ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID" \
    --vault-id "$VAULT_ID" \
    --transform id --raw-output)
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      vault_ids=[vault.id],
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    vault_ids: [vault.id],
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      VaultIds = [vault.ID],
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent:         anthropic.BetaSessionNewParamsAgentUnion{OfString: anthropic.String(agent.ID)},
  	EnvironmentID: environment.ID,
  	VaultIDs:      []string{vault.ID},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(
      SessionCreateParams.builder()
          .agent(agent.id())
          .environmentId(environment.id())
          .addVaultId(vault.id())
          .build()
  );
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      vaultIDs: [$vault->id],
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    vault_ids: [vault.id]
  )
  ```
</CodeGroup>

Credentials are matched by URL, so the vault must contain a credential whose `mcp_server_url` exactly matches the `url` declared in `mcp_servers`. If none matches, the connection is attempted unauthenticated. See [Add a credential](/docs/en/managed-agents/vaults#add-a-credential) for the `static_bearer` and `mcp_oauth` credential types.

### Handle connection and authentication failures

Session creation does not validate MCP connectivity or credentials. If an MCP server is unreachable or rejects the supplied credential, the session still starts and interaction remains possible. A [`session.error`](/docs/en/managed-agents/events-and-streaming) event is emitted with the `mcp_server_name` of the affected server and a `retry_status`:

| Error type                        | Meaning                                                                                           |
| --------------------------------- | ------------------------------------------------------------------------------------------------- |
| `mcp_connection_failed_error`     | The MCP server could not be reached (network error, timeout, or non-authentication HTTP failure). |
| `mcp_authentication_failed_error` | The MCP server was reached but rejected the credential from the attached vault.                   |

You can decide whether to block further interaction on this error, trigger a credential rotation, or let the session continue without the affected server's tools. The connection is retried on the next `session.status_idle` to `session.status_running` transition.

## Next steps

<CardGroup cols={2}>
  <Card title="Permission policies" icon="check" href="/docs/en/managed-agents/permission-policies">
    Control when agent and MCP tools run.
  </Card>

  <Card title="Session event stream" icon="lightning" href="/docs/en/managed-agents/events-and-streaming">
    Send events, stream responses, and interrupt or redirect your session mid-execution.
  </Card>

  <Card title="Supported MCP server types" icon="book" href="/docs/en/managed-agents/reference#supported-mcp-server-types">
    Transport requirements for remote MCP servers.
  </Card>
</CardGroup>
