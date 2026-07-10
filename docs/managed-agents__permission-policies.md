# Permission policies

Control when agent and MCP tools execute.

---

Permission policies control whether server-executed tools (the pre-built agent toolset and MCP toolset) run automatically or wait for your approval. Custom tools are executed by your application and controlled by you, so they are not governed by permission policies.

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Permission policy types

| Policy         | Behavior                                                                                                                                                       |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `always_allow` | The tool executes automatically with no confirmation.                                                                                                          |
| `always_ask`   | The session pauses and waits for your approval before executing. See [Respond to confirmation requests](#respond-to-confirmation-requests) for the event flow. |

Each toolset kind has its own default: the agent toolset defaults to `always_allow`, and MCP toolsets default to `always_ask`.

A permission policy controls when an enabled tool runs. To remove a tool from the agent entirely, disable it instead. See [Disabling specific tools](/docs/en/managed-agents/tools#disabling-specific-tools).

## Set a policy for a toolset

You set permission policies in the agent's `tools` configuration when you create the agent, and you can change them later by [updating the agent](/docs/en/managed-agents/agent-setup#update-an-agent). Running sessions keep the toolset configuration they were created with. Updates apply to sessions created afterward.

### Agent toolset permissions

When creating an agent, you can apply a policy to every tool in `agent_toolset_20260401` using `default_config.permission_policy`:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Coding Assistant",
      "model": "claude-opus-4-8",
      "tools": [
        {
          "type": "agent_toolset_20260401",
          "default_config": {
            "permission_policy": {"type": "always_ask"}
          }
        }
      ]
    }')
  ```

  ```bash CLI
  ant beta:agents create <<'YAML'
  name: Coding Assistant
  model: claude-opus-4-8
  tools:
    - type: agent_toolset_20260401
      default_config:
        permission_policy:
          type: always_ask
  YAML
  ```

  ```python Python
  agent = client.beta.agents.create(
      name="Coding Assistant",
      model="claude-opus-4-8",
      tools=[
          {
              "type": "agent_toolset_20260401",
              "default_config": {
                  "permission_policy": {"type": "always_ask"},
              },
          },
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Coding Assistant",
    model: "claude-opus-4-8",
    tools: [
      {
        type: "agent_toolset_20260401",
        default_config: {
          permission_policy: { type: "always_ask" }
        }
      }
    ]
  });
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Coding Assistant",
      Model = new("claude-opus-4-8"),
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
              DefaultConfig = new()
              {
                  PermissionPolicy = new BetaManagedAgentsAlwaysAskPolicy { Type = "always_ask" },
              },
          },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Coding Assistant",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: "claude-opus-4-8",
  	},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  			DefaultConfig: anthropic.BetaManagedAgentsAgentToolsetDefaultConfigParams{
  				PermissionPolicy: anthropic.BetaManagedAgentsAgentToolsetDefaultConfigParamsPermissionPolicyUnion{
  					OfAlwaysAsk: &anthropic.BetaManagedAgentsAlwaysAskPolicyParam{
  						Type: anthropic.BetaManagedAgentsAlwaysAskPolicyTypeAlwaysAsk,
  					},
  				},
  			},
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  _ = agent
  ```

  ```java Java
  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Coding Assistant")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
          .addTool(
              BetaManagedAgentsAgentToolset20260401Params.builder()
                  .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                  .defaultConfig(
                      BetaManagedAgentsAgentToolsetDefaultConfigParams.builder()
                          .permissionPolicy(
                              BetaManagedAgentsAlwaysAskPolicy.builder()
                                  .type(BetaManagedAgentsAlwaysAskPolicy.Type.ALWAYS_ASK)
                                  .build()
                          )
                          .build()
                  )
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'Coding Assistant',
      model: 'claude-opus-4-8',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
              defaultConfig: BetaManagedAgentsAgentToolsetDefaultConfigParams::with(
                  permissionPolicy: BetaManagedAgentsAlwaysAskPolicy::with(type: 'always_ask'),
              ),
          ),
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Coding Assistant",
    model: "claude-opus-4-8",
    tools: [
      {
        type: "agent_toolset_20260401",
        default_config: {
          permission_policy: {type: "always_ask"}
        }
      }
    ]
  )
  ```
</CodeGroup>

`default_config` is optional. If you omit it, the agent toolset is enabled with the default permission policy, `always_allow`.

### MCP toolset permissions

MCP toolsets default to `always_ask`. This ensures that new tools added to an MCP server do not execute in your application without approval. To auto-approve tools from a trusted MCP server, set `default_config.permission_policy` on the `mcp_toolset` entry.

The `mcp_server_name` must match the `name` of a server in the `mcp_servers` array.

This example connects a GitHub MCP server and allows its tools to run without confirmation:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Dev Assistant",
      "model": "claude-opus-4-8",
      "mcp_servers": [
        {"type": "url", "name": "github", "url": "https://mcp.example.com/github"}
      ],
      "tools": [
        {"type": "agent_toolset_20260401"},
        {
          "type": "mcp_toolset",
          "mcp_server_name": "github",
          "default_config": {
            "permission_policy": {"type": "always_allow"}
          }
        }
      ]
    }')
  ```

  ```bash CLI
  ant beta:agents create <<'YAML'
  name: Dev Assistant
  model: claude-opus-4-8
  mcp_servers:
    - type: url
      name: github
      url: https://mcp.example.com/github
  tools:
    - type: agent_toolset_20260401
    - type: mcp_toolset
      mcp_server_name: github
      default_config:
        permission_policy:
          type: always_allow
  YAML
  ```

  ```python Python
  agent = client.beta.agents.create(
      name="Dev Assistant",
      model="claude-opus-4-8",
      mcp_servers=[
          {"type": "url", "name": "github", "url": "https://mcp.example.com/github"},
      ],
      tools=[
          {"type": "agent_toolset_20260401"},
          {
              "type": "mcp_toolset",
              "mcp_server_name": "github",
              "default_config": {
                  "permission_policy": {"type": "always_allow"},
              },
          },
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Dev Assistant",
    model: "claude-opus-4-8",
    mcp_servers: [{ type: "url", name: "github", url: "https://mcp.example.com/github" }],
    tools: [
      { type: "agent_toolset_20260401" },
      {
        type: "mcp_toolset",
        mcp_server_name: "github",
        default_config: {
          permission_policy: { type: "always_allow" }
        }
      }
    ]
  });
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Dev Assistant",
      Model = new("claude-opus-4-8"),
      McpServers =
      [
          new() { Type = "url", Name = "github", Url = "https://mcp.example.com/github" },
      ],
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
          },
          new BetaManagedAgentsMcpToolsetParams
          {
              Type = "mcp_toolset",
              McpServerName = "github",
              DefaultConfig = new()
              {
                  PermissionPolicy = new BetaManagedAgentsAlwaysAllowPolicy { Type = "always_allow" },
              },
          },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Dev Assistant",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: "claude-opus-4-8",
  	},
  	MCPServers: []anthropic.BetaManagedAgentsURLMCPServerParams{{
  		Type: anthropic.BetaManagedAgentsURLMCPServerParamsTypeURL,
  		Name: "github",
  		URL:  "https://mcp.example.com/github",
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
  				DefaultConfig: anthropic.BetaManagedAgentsMCPToolsetDefaultConfigParams{
  					PermissionPolicy: anthropic.BetaManagedAgentsMCPToolsetDefaultConfigParamsPermissionPolicyUnion{
  						OfAlwaysAllow: &anthropic.BetaManagedAgentsAlwaysAllowPolicyParam{
  							Type: anthropic.BetaManagedAgentsAlwaysAllowPolicyTypeAlwaysAllow,
  						},
  					},
  				},
  			},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  _ = agent
  ```

  ```java Java
  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Dev Assistant")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
          .addMcpServer(
              BetaManagedAgentsUrlMcpServerParams.builder()
                  .type(BetaManagedAgentsUrlMcpServerParams.Type.URL)
                  .name("github")
                  .url("https://mcp.example.com/github")
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
                  .defaultConfig(
                      BetaManagedAgentsMcpToolsetDefaultConfigParams.builder()
                          .permissionPolicy(
                              BetaManagedAgentsAlwaysAllowPolicy.builder()
                                  .type(BetaManagedAgentsAlwaysAllowPolicy.Type.ALWAYS_ALLOW)
                                  .build()
                          )
                          .build()
                  )
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  use Anthropic\Beta\Agents\BetaManagedAgentsMCPToolsetDefaultConfigParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsMCPToolsetParams;
  use Anthropic\Beta\Agents\BetaManagedAgentsURLMCPServerParams;

  $agent = $client->beta->agents->create(
      name: 'Dev Assistant',
      model: 'claude-opus-4-8',
      mcpServers: [
          BetaManagedAgentsURLMCPServerParams::with(
              type: 'url',
              name: 'github',
              url: 'https://mcp.example.com/github',
          ),
      ],
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
          ),
          BetaManagedAgentsMCPToolsetParams::with(
              type: 'mcp_toolset',
              mcpServerName: 'github',
              defaultConfig: BetaManagedAgentsMCPToolsetDefaultConfigParams::with(
                  permissionPolicy: BetaManagedAgentsAlwaysAllowPolicy::with(type: 'always_allow'),
              ),
          ),
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Dev Assistant",
    model: "claude-opus-4-8",
    mcp_servers: [
      {type: "url", name: "github", url: "https://mcp.example.com/github"}
    ],
    tools: [
      {type: "agent_toolset_20260401"},
      {
        type: "mcp_toolset",
        mcp_server_name: "github",
        default_config: {
          permission_policy: {type: "always_allow"}
        }
      }
    ]
  )
  ```
</CodeGroup>

## Override an individual tool policy

Use the `configs` array to override the default for individual tools. The `name` values for the agent toolset are listed in [Available tools](/docs/en/managed-agents/tools#available-tools). This example allows the full agent toolset by default but requires confirmation before any bash command runs:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  tools='[
    {
      "type": "agent_toolset_20260401",
      "default_config": {
        "permission_policy": {"type": "always_allow"}
      },
      "configs": [
        {
          "name": "bash",
          "permission_policy": {"type": "always_ask"}
        }
      ]
    }
  ]'
  ```

  ```bash CLI
  ant beta:agents create <<'YAML'
  name: Coding Assistant
  model: claude-opus-4-8
  tools:
    - type: agent_toolset_20260401
      default_config:
        permission_policy:
          type: always_allow
      configs:
        - name: bash
          permission_policy:
            type: always_ask
  YAML
  ```

  ```python Python
  tools = [
      {
          "type": "agent_toolset_20260401",
          "default_config": {
              "permission_policy": {"type": "always_allow"},
          },
          "configs": [
              {
                  "name": "bash",
                  "permission_policy": {"type": "always_ask"},
              },
          ],
      },
  ]
  ```

  ```typescript TypeScript
  const tools = [
    {
      type: "agent_toolset_20260401",
      default_config: {
        permission_policy: { type: "always_allow" }
      },
      configs: [
        {
          name: "bash",
          permission_policy: { type: "always_ask" }
        }
      ]
    }
  ] satisfies Anthropic.Beta.AgentCreateParams["tools"];
  ```

  ```csharp C#
  Tool[] tools =
  [
      new BetaManagedAgentsAgentToolset20260401Params
      {
          Type = "agent_toolset_20260401",
          DefaultConfig = new()
          {
              PermissionPolicy = new BetaManagedAgentsAlwaysAllowPolicy { Type = "always_allow" },
          },
          Configs =
          [
              new()
              {
                  Name = "bash",
                  PermissionPolicy = new BetaManagedAgentsAlwaysAskPolicy { Type = "always_ask" },
              },
          ],
      },
  ];
  ```

  ```go Go
  tools := []anthropic.BetaAgentNewParamsToolUnion{{
  	OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  		Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  		DefaultConfig: anthropic.BetaManagedAgentsAgentToolsetDefaultConfigParams{
  			PermissionPolicy: anthropic.BetaManagedAgentsAgentToolsetDefaultConfigParamsPermissionPolicyUnion{
  				OfAlwaysAllow: &anthropic.BetaManagedAgentsAlwaysAllowPolicyParam{
  					Type: anthropic.BetaManagedAgentsAlwaysAllowPolicyTypeAlwaysAllow,
  				},
  			},
  		},
  		Configs: []anthropic.BetaManagedAgentsAgentToolConfigParams{{
  			Name: anthropic.BetaManagedAgentsAgentToolConfigParamsNameBash,
  			PermissionPolicy: anthropic.BetaManagedAgentsAgentToolConfigParamsPermissionPolicyUnion{
  				OfAlwaysAsk: &anthropic.BetaManagedAgentsAlwaysAskPolicyParam{
  					Type: anthropic.BetaManagedAgentsAlwaysAskPolicyTypeAlwaysAsk,
  				},
  			},
  		}},
  	},
  }}
  ```

  ```java Java
  var tools = List.of(
      AgentCreateParams.Tool.ofAgentToolset20260401(
          BetaManagedAgentsAgentToolset20260401Params.builder()
              .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
              .defaultConfig(
                  BetaManagedAgentsAgentToolsetDefaultConfigParams.builder()
                      .permissionPolicy(
                          BetaManagedAgentsAlwaysAllowPolicy.builder()
                              .type(BetaManagedAgentsAlwaysAllowPolicy.Type.ALWAYS_ALLOW)
                              .build()
                      )
                      .build()
              )
              .addConfig(
                  BetaManagedAgentsAgentToolConfigParams.builder()
                      .name(BetaManagedAgentsAgentToolConfigParams.Name.BASH)
                      .permissionPolicy(
                          BetaManagedAgentsAlwaysAskPolicy.builder()
                              .type(BetaManagedAgentsAlwaysAskPolicy.Type.ALWAYS_ASK)
                              .build()
                      )
                      .build()
              )
              .build()
      )
  );
  ```

  ```php PHP
  use Anthropic\Beta\Agents\BetaManagedAgentsAlwaysAskPolicy;

  $tools = [
      BetaManagedAgentsAgentToolset20260401Params::with(
          type: 'agent_toolset_20260401',
          defaultConfig: BetaManagedAgentsAgentToolsetDefaultConfigParams::with(
              permissionPolicy: BetaManagedAgentsAlwaysAllowPolicy::with(type: 'always_allow'),
          ),
          configs: [
              BetaManagedAgentsAgentToolConfigParams::with(
                  name: 'bash',
                  permissionPolicy: BetaManagedAgentsAlwaysAskPolicy::with(type: 'always_ask'),
              ),
          ],
      ),
  ];
  ```

  ```ruby Ruby
  tools = [
    {
      type: "agent_toolset_20260401",
      default_config: {
        permission_policy: {type: "always_allow"}
      },
      configs: [
        {
          name: "bash",
          permission_policy: {type: "always_ask"}
        }
      ]
    }
  ]
  ```
</CodeGroup>

Pass this `tools` configuration in the agent create request (the CLI tab shows the complete command). MCP toolsets support the same per-tool overrides, with `name` set to the tool name reported by the MCP server. See [Configure which MCP tools are available](/docs/en/managed-agents/mcp-connector#configure-which-mcp-tools-are-available).

## Respond to confirmation requests

When the agent invokes a tool with an `always_ask` policy:

1. The session emits an `agent.tool_use` or `agent.mcp_tool_use` event.
2. The session pauses with a `session.status_idle` event whose `stop_reason.type` is `requires_action`. The blocking event IDs are in the `stop_reason.event_ids` array. The session waits indefinitely for a response.
3. Send a `user.tool_confirmation` event for each blocking event, passing the event ID in the `tool_use_id` parameter. Set `result` to `"allow"` or `"deny"`. Use `deny_message` to explain a denial. You can send several confirmations in a single `events` request.
4. Once all blocking events are resolved, the session transitions back to `running`. Allowed tools execute. Denied tools do not run, and the agent receives a tool result saying the call was rejected, including your `deny_message`.

In the following examples, the tool-use event IDs come from the `stop_reason.event_ids` array of the `session.status_idle` event. Learn more about receiving events in the [Session event stream](/docs/en/managed-agents/events-and-streaming#integrating-events) guide, or [subscribe to webhooks](/docs/en/managed-agents/webhooks) to be notified when a session pauses for input.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  # Allow the tool to execute
  curl -fsSL "https://api.anthropic.com/v1/sessions/$SESSION_ID/events" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "events": [
        {
          "type": "user.tool_confirmation",
          "tool_use_id": "'$AGENT_TOOL_USE_EVENT_ID'",
          "result": "allow"
        }
      ]
    }'

  # Or deny it with an explanation
  curl -fsSL "https://api.anthropic.com/v1/sessions/$SESSION_ID/events" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "events": [
        {
          "type": "user.tool_confirmation",
          "tool_use_id": "'$MCP_TOOL_USE_EVENT_ID'",
          "result": "deny",
          "deny_message": "Don'\''t create issues in the production project. Use the staging project."
        }
      ]
    }'
  ```

  ```bash CLI
  # Allow the tool to execute
  ant beta:sessions:events send \
    --session-id "$SESSION_ID" \
    --event "{type: user.tool_confirmation, tool_use_id: $AGENT_TOOL_USE_EVENT_ID, result: allow}"

  # Or deny it with an explanation
  ant beta:sessions:events send \
    --session-id "$SESSION_ID" \
    --event "{type: user.tool_confirmation, tool_use_id: $MCP_TOOL_USE_EVENT_ID, result: deny,
      deny_message: Don't create issues in the production project. Use the staging project.}"
  ```

  ```python Python
  # Allow the tool to execute
  client.beta.sessions.events.send(
      session.id,
      events=[
          {
              "type": "user.tool_confirmation",
              "tool_use_id": agent_tool_use_event.id,
              "result": "allow",
          },
      ],
  )

  # Or deny it with an explanation
  client.beta.sessions.events.send(
      session.id,
      events=[
          {
              "type": "user.tool_confirmation",
              "tool_use_id": mcp_tool_use_event.id,
              "result": "deny",
              "deny_message": "Don't create issues in the production project. Use the staging project.",
          },
      ],
  )
  ```

  ```typescript TypeScript
  // Allow the tool to execute
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.tool_confirmation",
        tool_use_id: agent_tool_use_event.id,
        result: "allow"
      }
    ]
  });

  // Or deny it with an explanation
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.tool_confirmation",
        tool_use_id: mcp_tool_use_event.id,
        result: "deny",
        deny_message: "Don't create issues in the production project. Use the staging project."
      }
    ]
  });
  ```

  ```csharp C#
  // Allow the tool to execute
  await client.Beta.Sessions.Events.Send(session.ID, new()
  {
      Events =
      [
          new BetaManagedAgentsUserToolConfirmationEventParams
          {
              Type = "user.tool_confirmation",
              ToolUseID = agentToolUseEvent.ID,
              Result = "allow",
          },
      ],
  });

  // Or deny it with an explanation
  await client.Beta.Sessions.Events.Send(session.ID, new()
  {
      Events =
      [
          new BetaManagedAgentsUserToolConfirmationEventParams
          {
              Type = "user.tool_confirmation",
              ToolUseID = mcpToolUseEvent.ID,
              Result = "deny",
              DenyMessage = "Don't create issues in the production project. Use the staging project.",
          },
      ],
  });
  ```

  ```go Go
  // Allow the tool to execute
  _, err = client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  		OfUserToolConfirmation: &anthropic.BetaManagedAgentsUserToolConfirmationEventParams{
  			Type:      anthropic.BetaManagedAgentsUserToolConfirmationEventParamsTypeUserToolConfirmation,
  			ToolUseID: agentToolUseEvent.ID,
  			Result:    anthropic.BetaManagedAgentsUserToolConfirmationEventParamsResultAllow,
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }

  // Or deny it with an explanation
  _, err = client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  		OfUserToolConfirmation: &anthropic.BetaManagedAgentsUserToolConfirmationEventParams{
  			Type:        anthropic.BetaManagedAgentsUserToolConfirmationEventParamsTypeUserToolConfirmation,
  			ToolUseID:   mcpToolUseEvent.ID,
  			Result:      anthropic.BetaManagedAgentsUserToolConfirmationEventParamsResultDeny,
  			DenyMessage: anthropic.String("Don't create issues in the production project. Use the staging project."),
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  // Allow the tool to execute
  client.beta().sessions().events().send(
      session.id(),
      EventSendParams.builder()
          .addEvent(
              BetaManagedAgentsUserToolConfirmationEventParams.builder()
                  .type(BetaManagedAgentsUserToolConfirmationEventParams.Type.USER_TOOL_CONFIRMATION)
                  .toolUseId(agentToolUseEvent.id())
                  .result(BetaManagedAgentsUserToolConfirmationEventParams.Result.ALLOW)
                  .build()
          )
          .build()
  );

  // Or deny it with an explanation
  client.beta().sessions().events().send(
      session.id(),
      EventSendParams.builder()
          .addEvent(
              BetaManagedAgentsUserToolConfirmationEventParams.builder()
                  .type(BetaManagedAgentsUserToolConfirmationEventParams.Type.USER_TOOL_CONFIRMATION)
                  .toolUseId(mcpToolUseEvent.id())
                  .result(BetaManagedAgentsUserToolConfirmationEventParams.Result.DENY)
                  .denyMessage("Don't create issues in the production project. Use the staging project.")
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  use Anthropic\Beta\Sessions\Events\ManagedAgentsUserToolConfirmationEventParams;

  // Allow the tool to execute
  $client->beta->sessions->events->send(
      $session->id,
      events: [
          ManagedAgentsUserToolConfirmationEventParams::with(
              type: 'user.tool_confirmation',
              toolUseID: $agentToolUseEvent->id,
              result: 'allow',
          ),
      ],
  );

  // Or deny it with an explanation
  $client->beta->sessions->events->send(
      $session->id,
      events: [
          ManagedAgentsUserToolConfirmationEventParams::with(
              type: 'user.tool_confirmation',
              toolUseID: $mcpToolUseEvent->id,
              result: 'deny',
              denyMessage: "Don't create issues in the production project. Use the staging project.",
          ),
      ],
  );
  ```

  ```ruby Ruby
  # Allow the tool to execute
  client.beta.sessions.events.send_(
    session.id,
    events: [
      {
        type: "user.tool_confirmation",
        tool_use_id: agent_tool_use_event.id,
        result: "allow"
      }
    ]
  )

  # Or deny it with an explanation
  client.beta.sessions.events.send_(
    session.id,
    events: [
      {
        type: "user.tool_confirmation",
        tool_use_id: mcp_tool_use_event.id,
        result: "deny",
        deny_message: "Don't create issues in the production project. Use the staging project."
      }
    ]
  )
  ```
</CodeGroup>

## Custom tools

Permission policies do not apply to custom tools. When the agent invokes a custom tool, your application receives an `agent.custom_tool_use` event and is responsible for deciding whether to execute it before sending back a `user.custom_tool_result`. See [Session event stream](/docs/en/managed-agents/events-and-streaming#handling-custom-tool-calls) for the full flow.

## Next steps

<CardGroup cols={2}>
  <Card title="Skills" icon="books" href="/docs/en/managed-agents/skills">
    Attach reusable, filesystem-based expertise to your agent for domain-specific workflows.
  </Card>

  <Card title="Session event stream" icon="lightning" href="/docs/en/managed-agents/events-and-streaming">
    Send events, stream responses, and interrupt or redirect your session mid-execution.
  </Card>
</CardGroup>
