---
title: Multiagent orchestration
url: https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration
description: Coordinate multiple agents within a single session.
---

Multiagent orchestration lets one agent coordinate with others to complete complex work. Agents can act in parallel with their own isolated context, which helps improve output quality and can also improve time to completion.

Not sure a multiagent setup fits your problem? See [when to use multiagent systems (and when not to)](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them).

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](https://platform.claude.com/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## How it works

All agents share the same sandbox, filesystem, and [vault credentials](https://platform.claude.com/docs/en/managed-agents/vaults), but each agent runs in its own **session thread**, a context-isolated event stream with its own conversation history. The coordinator reports activity in the **primary thread** (which is the same as the session-level [event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)); additional threads are spawned at runtime when the coordinator delegates work.

Threads are persistent: the coordinator can send a follow-up to an agent it called earlier, and that agent retains everything from its previous turns.

Each agent uses its own configuration: model, system prompt, tools, MCP servers, and skills. Session-level [agent configuration overrides](https://platform.claude.com/docs/en/managed-agents/sessions#override-agent-configuration-for-a-session) are the exception; they apply to the coordinator and its `self` copies. Tools, MCP servers, and context are not shared.

### What to delegate

Multiagent coordination is best suited for complex tasks that either require work across a variety of surfaces, or where multiple well-scoped tasks contribute to an overall goal.

Patterns that work well:

* **Parallelization:** Fan out independent subtasks simultaneously (searching multiple sources, analyzing separate files) and have the coordinator synthesize the results.
* **Specialization:** Route to agents with domain-focused system prompts and tools, such as a security agent or a documentation agent, rather than loading a single agent with every capability.
* **Escalation:** Consult a more capable agent or model for a subset of complex subtasks.

## Configure the coordinator

When [defining your agent](https://platform.claude.com/docs/en/managed-agents/agent-setup), set `multiagent` to declare the roster of agents the coordinator can delegate to:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  coordinator=$(curl -fsS https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "name": "Engineering Lead",
    "model": "claude-opus-5",
    "system": "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
    "tools": [
      {
        "type": "agent_toolset_20260401"
      }
    ],
    "multiagent": {
      "type": "coordinator",
      "agents": [
        {"type": "agent", "id": "$REVIEWER_AGENT_ID"},
        {"type": "agent", "id": "$TEST_WRITER_AGENT_ID"}
      ]
    }
  }
  EOF
  )
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    ant beta:agents create < coordinator.agent.yaml
    ```

    <File filename="coordinator.agent.yaml">
      ```yaml
      name: Engineering Lead
      model: claude-opus-5
      system: You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.
      tools:
        - type: agent_toolset_20260401
      multiagent:
        type: coordinator
        agents:
          - type: agent
            id: $REVIEWER_AGENT_ID # replace before running command
          - type: agent
            id: $TEST_WRITER_AGENT_ID # replace before running command
      ```
    </File>
  </MultiFileExample>

  ```python Python
  coordinator = client.beta.agents.create(
      name="Engineering Lead",
      model="claude-opus-5",
      system="You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
      tools=[
          {"type": "agent_toolset_20260401"},
      ],
      multiagent={
          "type": "coordinator",
          "agents": [
              {"type": "agent", "id": reviewer_agent.id},
              {"type": "agent", "id": test_writer_agent.id},
          ],
      },
  )
  ```

  ```typescript TypeScript
  const coordinator = await client.beta.agents.create({
    name: "Engineering Lead",
    model: "claude-opus-5",
    system:
      "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
    tools: [{ type: "agent_toolset_20260401" }],
    multiagent: {
      type: "coordinator",
      agents: [
        { type: "agent", id: reviewerAgent.id },
        { type: "agent", id: testWriterAgent.id },
      ],
    },
  });
  ```

  ```csharp C#
  var coordinator = await client.Beta.Agents.Create(new()
  {
      Name = "Engineering Lead",
      Model = BetaManagedAgentsModel.ClaudeOpus5,
      System = "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = BetaManagedAgentsAgentToolset20260401ParamsType.AgentToolset20260401,
          },
      ],
      Multiagent = new BetaManagedAgentsMultiagentParams
      {
          Type = BetaManagedAgentsMultiagentParamsType.Coordinator,
          Agents = [reviewerAgent.ID, testWriterAgent.ID],
      },
  });
  ```

  ```go Go
  coordinator, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name:   "Engineering Lead",
  	Model:  anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeOpus5},
  	System: anthropic.String("You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent."),
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  		},
  	}},
  	Multiagent: anthropic.BetaManagedAgentsMultiagentParams{
  		Type: anthropic.BetaManagedAgentsMultiagentParamsTypeCoordinator,
  		Agents: []anthropic.BetaManagedAgentsMultiagentRosterEntryParamsUnion{
  			{OfString: anthropic.String(reviewerAgent.ID)},
  			{OfString: anthropic.String(testWriterAgent.ID)},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var coordinator = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Engineering Lead")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
          .system("You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.")
          .addTool(
              BetaManagedAgentsAgentToolset20260401Params.builder()
                  .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                  .build()
          )
          .multiagent(BetaManagedAgentsMultiagentParams.builder()
              .type(BetaManagedAgentsMultiagentParams.Type.COORDINATOR)
              .addAgent(BetaManagedAgentsAgentParams.builder()
                  .type(BetaManagedAgentsAgentParams.Type.AGENT)
                  .id(reviewerAgent.id())
                  .build())
              .addAgent(BetaManagedAgentsAgentParams.builder()
                  .type(BetaManagedAgentsAgentParams.Type.AGENT)
                  .id(testWriterAgent.id())
                  .build())
              .build())
          .build()
  );
  ```

  ```php PHP
  $coordinator = $client->beta->agents->create(
      name: 'Engineering Lead',
      model: 'claude-opus-5',
      system: 'You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.',
      tools: [
          ['type' => 'agent_toolset_20260401'],
      ],
      multiagent: [
          'type' => 'coordinator',
          'agents' => [
              ['type' => 'agent', 'id' => $reviewerAgent->id],
              ['type' => 'agent', 'id' => $testWriterAgent->id],
          ],
      ],
  );
  ```

  ```ruby Ruby
  coordinator = client.beta.agents.create(
    name: "Engineering Lead",
    model: "claude-opus-5",
    system: "You coordinate engineering work. Delegate code review to the reviewer agent and test writing to the test agent.",
    tools: [
      {type: "agent_toolset_20260401"}
    ],
    multiagent: {
      type: "coordinator",
      agents: [
        {type: "agent", id: reviewer_agent.id},
        {type: "agent", id: test_writer_agent.id}
      ]
    }
  )
  ```
</CodeGroup>

`multiagent.agents` can accept any of the following:

* `{"type": "agent", "id": agent.id}` references a previously created `agent` by ID. If no `version` is specified, the reference is pinned to the latest version of that agent at the time the coordinator is created.
* `{"type": "agent", "id": agent.id, "version": agent.version}` pins a specific agent version.
* `{"type": "self"}` allows the coordinator to spawn copies of itself. If the session was created with [agent configuration overrides](https://platform.claude.com/docs/en/managed-agents/sessions#override-agent-configuration-for-a-session), those overrides also apply to these copies; roster entries referenced by ID are unaffected.
* `{"type": "advisor", "model": "<model id>"}` gives the session's primary thread an advisor it can consult mid-turn. At most one advisor entry per roster. See [Give the session an advisor](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration#give-the-session-an-advisor).

The coordinator's configuration, including its `multiagent.agents` roster, is snapshotted when the coordinator is created or updated. Referenced agents stay pinned to the versions resolved at that time and do not automatically pick up later updates to their definitions. To delegate to a newer version of a referenced agent, [update the coordinator](https://platform.claude.com/docs/en/managed-agents/agent-setup#update-an-agent) so its roster references that version.

The coordinator can only delegate to one level of agents; referencing an agent that has its own `multiagent.agents` roster fails the create or update request with a validation error. A maximum of 20 unique agents can be listed in `multiagent.agents`, but the coordinator can call multiple copies of each agent.

When agents pin an [inference geography](https://platform.claude.com/docs/en/manage-claude/data-residency) (`model.inference_geo` in the [agent definition](https://platform.claude.com/docs/en/managed-agents/agent-setup)), the coordinator's pin and every roster member's pin must either all be set to the same value or all be unset. A mismatched roster is rejected with a 400 validation error, both when the agent is saved and when a [session-create override](https://platform.claude.com/docs/en/managed-agents/sessions#override-agent-configuration-for-a-session) changes any of the pins.

### Give the session an advisor

An advisor entry in `multiagent.agents` gives the session's primary thread an **advisor**: a model it can consult mid-turn for strategic guidance, such as planning an approach, getting unstuck, or reviewing work before finishing. The entry has exactly two fields, `type` and `model`:

```bash cURL
curl -fsS https://api.anthropic.com/v1/agents \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d '{
    "name": "Backend engineer",
    "model": "claude-sonnet-5",
    "system": "You implement backend features end to end. Consult the advisor before major backend design decisions.",
    "multiagent": {
      "type": "coordinator",
      "agents": [
        {"type": "advisor", "model": "claude-opus-5"}
      ]
    }
  }'
```

A roster can contain at most one advisor entry, alongside any of the other roster forms. The entry occupies the reserved roster name `anthropic.advisor`: a roster that lists both an advisor entry and a member literally named `anthropic.advisor` is rejected with a 400 validation error. In responses, the advisor entry is echoed last in the roster regardless of the position it was submitted in.

The advisor model must meet a minimum capability bar, and the agent's own model must not be more capable than its advisor; models of equal capability can pair. An invalid pairing is rejected with a 400 validation error when the agent is saved. Valid pairings follow the advisor tool's [model compatibility](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool#model-compatibility) table.

The advisor is also available as a [server tool on the Messages API](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool). The Managed Agents surface differs in configuration and delivery: the roster entry has no `max_uses`, `max_tokens`, or `caching` fields, and advice arrives through thread events rather than `advisor_tool_result` blocks.

#### How consultations work

Each consultation runs as a platform-spawned thread named `anthropic.advisor` that terminates itself when the consultation completes, and the advice is delivered to the primary thread as an `agent.thread_message_received` event. A consultation emits the standard thread events, identified by the reserved name `anthropic.advisor` (the thread lifecycle events carry it as `agent_name`, and the advice delivery carries it as `from_agent_name`), typically in this order:

1. `session.thread_created`
2. `session.thread_status_running`
3. `agent.thread_message_received` (the advice)
4. `session.thread_status_idle` (`stop_reason: end_turn`)
5. `session.thread_status_terminated`

No `agent.tool_use` events are emitted for a consultation, and no `agent.thread_message_sent` event appears on the session's event stream, because the consultation input is composed by the platform rather than sent by the agent. If you list the advisor thread's own events, the advice also appears there as an `agent.thread_message_sent` event. The advice delivery (event 3) is not guaranteed to arrive before the advisor thread's idle and terminated events, so don't treat those as a signal that the advice has already been delivered.

Whether your client can read the advice is the advisor model's policy, and it mirrors the [result variants](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool#result-variants) split on the Messages API advisor tool. Advisor models that return plaintext results there deliver the advice as readable text content here; advisor models that return redacted results there deliver a `[{"type": "redacted"}]` placeholder as the message content on every client surface, while the agent itself still reads the full advice server-side. In the preceding example, Claude Opus 5 is a redacted-result advisor, so your client sees the placeholder while the agent reads the full advice; choose Claude Opus 4.8 as the advisor instead if you want the advice readable on the event stream. Advisor thinking is never surfaced. Clients cannot send `redacted` blocks themselves; an event containing one is rejected with a 400 validation error.

A failed or interrupted consultation never fails the agent's turn: the agent continues after a generic notice that the consultation failed. A session-level `user.interrupt` during a consultation terminates the advisor thread with no advice delivered; a `user.interrupt` with the advisor thread's `session_thread_id` abandons only that consultation.

#### Advisor threads

The advisor is not a roster agent: it is invisible to the coordinator's `list_agents` tool, it cannot be messaged with `send_to_agent`, and only the session's primary thread can consult it. Roster agents cannot.

Advisor threads are exempt from the concurrent-thread limit. They appear in the session's [thread list](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration#threads) with `agent` set to the advisor form exactly as configured (`{"type": "advisor", "model": ...}`) and `parent_thread_id` set to the primary thread.

Prompt caching on the advisor's side is automatic; there is nothing to configure. Consultations are billed at the advisor model's rates, and their tokens appear in the advisor thread's usage and in the session's usage totals.

#### Removing the advisor

To remove the advisor, [update the agent](https://platform.claude.com/docs/en/managed-agents/agent-setup#update-an-agent) with a roster that no longer includes the advisor entry. If the advisor is the roster's only entry, clear the roster entirely by setting `"multiagent": null`.

## Create the session

Create a session referencing the coordinator. The coordinator delegates to the agents in its roster as needed.

<CodeGroup>
  ```bash cURL
  session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$COORDINATOR_ID",
    "environment_id": "$ENVIRONMENT_ID"
  }
  EOF
  )
  SESSION_ID=$(jq -r '.id' <<< "$session")
  ```

  ```bash CLI
  ant beta:sessions create \
    --agent "$COORDINATOR_ID" \
    --environment-id "$ENVIRONMENT_ID"
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=coordinator.id,
      environment_id=environment.id,
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: coordinator.id,
    environment_id: environment.id,
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = coordinator.ID,
      EnvironmentID = environment.ID,
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(coordinator.ID),
  	},
  	EnvironmentID: environment.ID,
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(coordinator.id())
      .environmentId(environment.id())
      .build());
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $coordinator->id,
      environmentID: $environment->id,
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: coordinator.id,
    environment_id: environment.id
  )
  ```
</CodeGroup>

## Connect agents to MCP servers

MCP servers are agent-scoped (each agent definition declares its own servers and tools), while vault credentials are session-scoped (`vault_ids` passed at session creation apply to every thread). Two implications for your integration:

* To authenticate MCP servers, include a vault credential for every MCP server used across all agents.
* To limit an agent's access, declare only the servers it needs in its agent definition.

[Agent configuration overrides](https://platform.claude.com/docs/en/managed-agents/sessions#override-agent-configuration-for-a-session) at session creation can replace the coordinator's MCP servers and those of its `self` copies.

<CodeGroup>
  ```bash cURL
  research_agent_id=$(curl --fail-with-body -sS "$BASE/v1/agents" "${H[@]}" --data @- <<'EOF' | jq -er '.id'
  {
    "name": "researcher",
    "model": "claude-haiku-4-5",
    "mcp_servers": [{"type": "url", "name": "github", "url": "https://api.githubcopilot.com/mcp/"}],
    "tools": [{"type": "mcp_toolset", "mcp_server_name": "github"}]
  }
  EOF
  )

  coordinator_id=$(curl --fail-with-body -sS "$BASE/v1/agents" "${H[@]}" --data @- <<EOF | jq -er '.id'
  {
    "name": "coordinator",
    "model": "claude-opus-5",
    "tools": [{"type": "agent_toolset_20260401"}],
    "multiagent": {
      "type": "coordinator",
      "agents": [{"type": "agent", "id": "$research_agent_id"}]
    }
  }
  EOF
  )

  session_id=$(curl --fail-with-body -sS "$BASE/v1/sessions" "${H[@]}" --data @- <<EOF | jq -er '.id'
  {
    "agent": "$coordinator_id",
    "environment_id": "$environment_id",
    "vault_ids": ["$vault_id"]
  }
  EOF
  )
  echo "$session_id"
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    research_agent_id=$(ant beta:agents create --transform id --raw-output < researcher.agent.yaml)
    ```

    <File filename="researcher.agent.yaml">
      ```yaml
      name: researcher
      model: claude-haiku-4-5
      mcp_servers:
        - type: url
          name: github
          url: https://api.githubcopilot.com/mcp/
      tools:
        - type: mcp_toolset
          mcp_server_name: github
      ```
    </File>

    <File filename="subagent-coordinator.agent.yaml">
      ```yaml
      name: coordinator
      model: claude-opus-5
      tools:
        - type: agent_toolset_20260401
      multiagent:
        type: coordinator
        agents:
          - type: agent
            id: $research_agent_id # replace before running command
      ```
    </File>

    ```bash CLI
    coordinator_id=$(ant beta:agents create --transform id --raw-output < subagent-coordinator.agent.yaml)

    session_id=$(ant beta:sessions create \
      --agent "$coordinator_id" \
      --environment-id "$environment_id" \
      --vault-id "$vault_id" \
      --transform id --raw-output)
    echo "$session_id"
    ```
  </MultiFileExample>

  ```python Python
  research_agent = client.beta.agents.create(
      name="researcher",
      model="claude-haiku-4-5",
      mcp_servers=[
          {"type": "url", "name": "github", "url": "https://api.githubcopilot.com/mcp/"},
      ],
      tools=[{"type": "mcp_toolset", "mcp_server_name": "github"}],
  )

  coordinator = client.beta.agents.create(
      name="coordinator",
      model="claude-opus-5",
      tools=[{"type": "agent_toolset_20260401"}],
      multiagent={
          "type": "coordinator",
          "agents": [{"type": "agent", "id": research_agent.id}],
      },
  )

  session = client.beta.sessions.create(
      agent=coordinator.id,
      environment_id=environment.id,
      vault_ids=[vault.id],
  )
  print(session.id)
  ```

  ```typescript TypeScript
  const researchAgent = await client.beta.agents.create({
    name: "researcher",
    model: "claude-haiku-4-5",
    mcp_servers: [
      { type: "url", name: "github", url: "https://api.githubcopilot.com/mcp/" },
    ],
    tools: [{ type: "mcp_toolset", mcp_server_name: "github" }],
  });

  const coordinator = await client.beta.agents.create({
    name: "coordinator",
    model: "claude-opus-5",
    tools: [{ type: "agent_toolset_20260401" }],
    multiagent: {
      type: "coordinator",
      agents: [{ type: "agent", id: researchAgent.id }],
    },
  });

  const session = await client.beta.sessions.create({
    agent: coordinator.id,
    environment_id: environment.id,
    vault_ids: [vault.id],
  });
  console.log(session.id);
  ```

  ```csharp C#
  var researchAgent = await client.Beta.Agents.Create(new()
  {
      Name = "researcher",
      Model = BetaManagedAgentsModel.ClaudeHaiku4_5,
      McpServers =
      [
          new()
          {
              Type = BetaManagedAgentsUrlMcpServerParamsType.Url,
              Name = "github",
              Url = "https://api.githubcopilot.com/mcp/",
          },
      ],
      Tools =
      [
          new BetaManagedAgentsMcpToolsetParams
          {
              Type = BetaManagedAgentsMcpToolsetParamsType.McpToolset,
              McpServerName = "github",
          },
      ],
  });

  var coordinator = await client.Beta.Agents.Create(new()
  {
      Name = "coordinator",
      Model = BetaManagedAgentsModel.ClaudeOpus5,
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = BetaManagedAgentsAgentToolset20260401ParamsType.AgentToolset20260401,
          },
      ],
      Multiagent = new()
      {
          Type = BetaManagedAgentsMultiagentParamsType.Coordinator,
          Agents =
          [
              new BetaManagedAgentsAgentParams
              {
                  Type = BetaManagedAgentsAgentParamsType.Agent,
                  ID = researchAgent.ID,
              },
          ],
      },
  });

  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = coordinator.ID,
      EnvironmentID = environment.ID,
      VaultIds = [vault.ID],
  });
  Console.WriteLine(session.ID);
  ```

  ```go Go
  researcher, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name:  "researcher",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeHaiku4_5},
  	MCPServers: []anthropic.BetaManagedAgentsURLMCPServerParams{{
  		Type: anthropic.BetaManagedAgentsURLMCPServerParamsTypeURL,
  		Name: "github",
  		URL:  "https://api.githubcopilot.com/mcp/",
  	}},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfMCPToolset: &anthropic.BetaManagedAgentsMCPToolsetParams{
  			Type:          anthropic.BetaManagedAgentsMCPToolsetParamsTypeMCPToolset,
  			MCPServerName: "github",
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }

  coordinator, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name:  "coordinator",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeOpus5},
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  		},
  	}},
  	Multiagent: anthropic.BetaManagedAgentsMultiagentParams{
  		Type: anthropic.BetaManagedAgentsMultiagentParamsTypeCoordinator,
  		Agents: []anthropic.BetaManagedAgentsMultiagentRosterEntryParamsUnion{{
  			OfBetaManagedAgentsAgents: &anthropic.BetaManagedAgentsAgentParams{
  				Type: anthropic.BetaManagedAgentsAgentParamsTypeAgent,
  				ID:   researcher.ID,
  			},
  		}},
  	},
  })
  if err != nil {
  	panic(err)
  }

  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(coordinator.ID),
  	},
  	EnvironmentID: environment.ID,
  	VaultIDs:      []string{vault.ID},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(session.ID)
  ```

  ```java Java
  var researcher = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("researcher")
          .model(BetaManagedAgentsModel.CLAUDE_HAIKU_4_5)
          .addMcpServer(BetaManagedAgentsUrlMcpServerParams.builder()
              .name("github")
              .type(BetaManagedAgentsUrlMcpServerParams.Type.URL)
              .url("https://api.githubcopilot.com/mcp/")
              .build())
          .addTool(BetaManagedAgentsMcpToolsetParams.builder()
              .type(BetaManagedAgentsMcpToolsetParams.Type.MCP_TOOLSET)
              .mcpServerName("github")
              .build())
          .build()
  );

  var coordinator = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("coordinator")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
          .addTool(BetaManagedAgentsAgentToolset20260401Params.builder()
              .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
              .build())
          .multiagent(BetaManagedAgentsMultiagentParams.builder()
              .type(BetaManagedAgentsMultiagentParams.Type.COORDINATOR)
              .addAgent(BetaManagedAgentsAgentParams.builder()
                  .type(BetaManagedAgentsAgentParams.Type.AGENT)
                  .id(researcher.id())
                  .build())
              .build())
          .build()
  );

  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(coordinator.id())
      .environmentId(environment.id())
      .vaultIds(List.of(vault.id()))
      .build());
  IO.println(session.id());
  ```

  ```php PHP
  $researchAgent = $client->beta->agents->create(
      name: 'researcher',
      model: 'claude-haiku-4-5',
      mcpServers: [
          ['type' => 'url', 'name' => 'github', 'url' => 'https://api.githubcopilot.com/mcp/'],
      ],
      tools: [
          ['type' => 'mcp_toolset', 'mcp_server_name' => 'github'],
      ],
  );

  $coordinator = $client->beta->agents->create(
      name: 'coordinator',
      model: 'claude-opus-5',
      tools: [
          ['type' => 'agent_toolset_20260401'],
      ],
      multiagent: [
          'type' => 'coordinator',
          'agents' => [
              ['type' => 'agent', 'id' => $researchAgent->id],
          ],
      ],
  );

  $session = $client->beta->sessions->create(
      agent: $coordinator->id,
      environmentID: $environment->id,
      vaultIDs: [$vault->id],
  );
  echo "{$session->id}\n";
  ```

  ```ruby Ruby
  research_agent = client.beta.agents.create(
    name: "researcher",
    model: "claude-haiku-4-5",
    mcp_servers: [
      {type: "url", name: "github", url: "https://api.githubcopilot.com/mcp/"}
    ],
    tools: [
      {type: "mcp_toolset", mcp_server_name: "github"}
    ]
  )

  coordinator = client.beta.agents.create(
    name: "coordinator",
    model: "claude-opus-5",
    tools: [
      {type: "agent_toolset_20260401"}
    ],
    multiagent: {
      type: "coordinator",
      agents: [
        {type: "agent", id: research_agent.id}
      ]
    }
  )

  session = client.beta.sessions.create(
    agent: coordinator.id,
    environment_id: environment.id,
    vault_ids: [vault.id]
  )
  puts session.id
  ```
</CodeGroup>

In this example, only the researcher declares the GitHub MCP server, so the coordinator does not have access. The session's `vault_ids` supply the GitHub credential to the researcher's thread.

<Tip>
  If an agent's MCP calls fail to authenticate after you declare the server, confirm the credential's `mcp_server_url` refers to the same server as the agent's `mcp_servers[].url`. Both URLs are normalized before matching (scheme and host lowercased, default ports and trailing slashes stripped), so differences in host casing, a default port, or a trailing slash don't prevent a match; a different path, subdomain, or non-default port does.
</Tip>

## Threads

The **session-level event stream** (`/v1/sessions/{session_id}/events/stream`) is considered the **primary thread**, containing a condensed view of all activity across all threads. You don't see the full activity from subagents, but you do see the start and end of their work, and blocking events such as tool permission requests.

**Session threads** are where you drill into a specific agent's activity.

The session `status` is an aggregation of all agent activity; if at least one thread is `running`, then the overall session status is `running` as well.

A [session budget](https://platform.claude.com/docs/en/managed-agents/budgets) is a single shared cap across all of a session's threads. As the cap is reached, threads pause independently, and each thread's cost is priced at the thread's own served model.

<Note>
  A maximum of 25 concurrent threads is supported. The coordinator can call multiple copies of a single agent in the roster, creating multiple threads associated with one `agent`. [Advisor](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration#give-the-session-an-advisor) consultation threads are exempt from this limit.
</Note>

<Tabs>
  <Tab title="List threads">
    List all threads associated with a session as follows:

    <CodeGroup>
      ```bash cURL
      curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        | jq -r '.data[] | "[\(.agent.name)] \(.status)"'
      ```

      ```bash CLI
      ant beta:sessions:threads list --session-id "$SESSION_ID"
      ```

      ```python Python
      for thread in client.beta.sessions.threads.list(session.id):
          print(f"[{thread.agent.name}] {thread.status}")
      ```

      ```typescript TypeScript
      for await (const thread of client.beta.sessions.threads.list(session.id)) {
        console.log(`[${thread.agent.name}] ${thread.status}`);
      }
      ```

      ```csharp C#
      await foreach (var thread in (await client.Beta.Sessions.Threads.List(session.ID)).Paginate())
      {
          Console.WriteLine($"[{thread.Agent.Name}] {thread.Status}");
      }
      ```

      ```go Go
      threads := client.Beta.Sessions.Threads.ListAutoPaging(ctx, session.ID, anthropic.BetaSessionThreadListParams{})
      for threads.Next() {
      	thread := threads.Current()
      	fmt.Printf("[%s] %s\n", thread.Agent.Name, thread.Status)
      }
      if err := threads.Err(); err != nil {
      	panic(err)
      }
      ```

      ```java Java
      for (var thread : client.beta().sessions().threads().list(session.id()).autoPager()) {
          var name = thread.agent().isAgent() ? thread.agent().asAgent().name() : "advisor";
          IO.println("[" + name + "] " + thread.status());
      }
      ```

      ```php PHP
      foreach ($client->beta->sessions->threads->list($session->id)->pagingEachItem() as $thread) {
          echo "[{$thread->agent->name}] {$thread->status}\n";
      }
      ```

      ```ruby Ruby
      client.beta.sessions.threads.list(session.id).auto_paging_each do |thread|
        puts "[#{thread.agent.name}] #{thread.status}"
      end
      ```
    </CodeGroup>

    The full list includes the primary thread. `parent_thread_id` is null for the primary thread.
  </Tab>

  <Tab title="Interrupt a session thread">
    Send `user.interrupt` with `session_thread_id` to stop a specific thread. Omitting `session_thread_id` interrupts every non-archived thread in the session, including the primary.

    <CodeGroup>
      ```bash cURL
      curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        -d "{\"events\": [{\"type\": \"user.interrupt\", \"session_thread_id\": \"$THREAD_ID\"}]}"
      ```

      ```bash CLI
      ant beta:sessions:events send \
        --session-id "$SESSION_ID" \
        --event "{type: user.interrupt, session_thread_id: $THREAD_ID}"
      ```

      ```python Python
      client.beta.sessions.events.send(
          session.id,
          events=[{"type": "user.interrupt", "session_thread_id": thread.id}],
      )
      ```

      ```typescript TypeScript
      await client.beta.sessions.events.send(session.id, {
        events: [{ type: "user.interrupt", session_thread_id: thread.id }],
      });
      ```

      ```csharp C#
      await client.Beta.Sessions.Events.Send(session.ID, new()
      {
          Events =
          [
              new BetaManagedAgentsUserInterruptEventParams
              {
                  Type = BetaManagedAgentsUserInterruptEventParamsType.UserInterrupt,
                  SessionThreadID = thread.ID,
              },
          ],
      });
      ```

      ```go Go
      if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
      	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
      		OfUserInterrupt: &anthropic.BetaManagedAgentsUserInterruptEventParams{
      			Type:            anthropic.BetaManagedAgentsUserInterruptEventParamsTypeUserInterrupt,
      			SessionThreadID: anthropic.String(thread.ID),
      		},
      	}},
      }); err != nil {
      	panic(err)
      }
      ```

      ```java Java
      client.beta().sessions().events().send(
          session.id(),
          EventSendParams.builder()
              .addEvent(BetaManagedAgentsUserInterruptEventParams.builder()
                  .type(BetaManagedAgentsUserInterruptEventParams.Type.USER_INTERRUPT)
                  .sessionThreadId(thread.id())
                  .build())
              .build());
      ```

      ```php PHP
      $client->beta->sessions->events->send(
          $session->id,
          events: [
              ['type' => 'user.interrupt', 'session_thread_id' => $thread->id],
          ],
      );
      ```

      ```ruby Ruby
      client.beta.sessions.events.send_(
        session.id,
        events: [{type: "user.interrupt", session_thread_id: thread.id}]
      )
      ```
    </CodeGroup>

    Against a child thread blocked on `requires_action`, the interrupt closes each pending tool call with an error tool result ("Tool execution was interrupted before completion. Please retry.") and re-emits `session.thread_status_idle` with `stop_reason: end_turn` directly; the model is not sampled. Against a thread already at `idle`, the interrupt is a no-op.
  </Tab>

  <Tab title="Archive a session thread">
    Optionally archive a session thread when it has completed its work. This frees up a thread against the 25-thread limit.

    <CodeGroup>
      ```bash cURL
      curl -fsS -X POST "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads/$THREAD_ID/archive" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01"
      ```

      ```bash CLI
      ant beta:sessions:threads archive \
        --session-id "$SESSION_ID" \
        --thread-id "$THREAD_ID"
      ```

      ```python Python
      archived = client.beta.sessions.threads.archive(thread.id, session_id=session.id)
      print(archived.status, archived.archived_at)
      ```

      ```typescript TypeScript
      const archived = await client.beta.sessions.threads.archive(thread.id, {
        session_id: session.id,
      });
      console.log(archived.status, archived.archived_at);
      ```

      ```csharp C#
      var archived = await client.Beta.Sessions.Threads.Archive(thread.ID, new() { SessionID = session.ID });
      Console.WriteLine($"{archived.Status} {archived.ArchivedAt}");
      ```

      ```go Go
      archived, err := client.Beta.Sessions.Threads.Archive(ctx, thread.ID, anthropic.BetaSessionThreadArchiveParams{
      	SessionID: session.ID,
      })
      if err != nil {
      	panic(err)
      }
      fmt.Println(archived.Status, archived.ArchivedAt)
      ```

      ```java Java
      var archived = client.beta().sessions().threads().archive(
          thread.id(),
          ThreadArchiveParams.builder()
              .sessionId(session.id())
              .build());
      IO.println(archived.status() + " " + archived.archivedAt().orElseThrow());
      ```

      ```php PHP
      $archived = $client->beta->sessions->threads->archive($thread->id, sessionID: $session->id);
      echo "{$archived->status} {$archived->archivedAt->format(DATE_ATOM)}\n";
      ```

      ```ruby Ruby
      archived = client.beta.sessions.threads.archive(thread.id, session_id: session.id)
      puts "#{archived.status} #{archived.archived_at}"
      ```
    </CodeGroup>

    Archive only succeeds if the thread is `idle`. A thread parked on `requires_action` counts as idle and can be archived directly; only a running thread must be interrupted first:

    <CodeGroup>
      ```bash cURL
      # Interrupt the thread, then archive it
      curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        -d "{\"events\": [{\"type\": \"user.interrupt\", \"session_thread_id\": \"$THREAD_ID\"}]}"

      curl -fsS -X POST "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads/$THREAD_ID/archive" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01"
      ```

      ```bash CLI
      ant beta:sessions:events send \
        --session-id "$SESSION_ID" \
        --event "{type: user.interrupt, session_thread_id: $THREAD_ID}"

      ant beta:sessions:threads archive \
        --session-id "$SESSION_ID" \
        --thread-id "$THREAD_ID"
      ```

      ```python Python
      client.beta.sessions.events.send(
          session.id,
          events=[{"type": "user.interrupt", "session_thread_id": thread.id}],
      )
      archived = client.beta.sessions.threads.archive(thread.id, session_id=session.id)
      print(archived.status, archived.archived_at)
      ```

      ```typescript TypeScript
      await client.beta.sessions.events.send(session.id, {
        events: [{ type: "user.interrupt", session_thread_id: thread.id }],
      });
      const archived = await client.beta.sessions.threads.archive(thread.id, {
        session_id: session.id,
      });
      console.log(archived.status, archived.archived_at);
      ```

      ```csharp C#
      await client.Beta.Sessions.Events.Send(session.ID, new()
      {
          Events =
          [
              new BetaManagedAgentsUserInterruptEventParams
              {
                  Type = BetaManagedAgentsUserInterruptEventParamsType.UserInterrupt,
                  SessionThreadID = thread.ID,
              },
          ],
      });
      archived = await client.Beta.Sessions.Threads.Archive(thread.ID, new() { SessionID = session.ID });
      Console.WriteLine($"{archived.Status} {archived.ArchivedAt}");
      ```

      ```go Go
      if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
      	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
      		OfUserInterrupt: &anthropic.BetaManagedAgentsUserInterruptEventParams{
      			Type:            anthropic.BetaManagedAgentsUserInterruptEventParamsTypeUserInterrupt,
      			SessionThreadID: anthropic.String(thread.ID),
      		},
      	}},
      }); err != nil {
      	panic(err)
      }

      archived, err := client.Beta.Sessions.Threads.Archive(ctx, thread.ID, anthropic.BetaSessionThreadArchiveParams{
      	SessionID: session.ID,
      })
      if err != nil {
      	panic(err)
      }
      fmt.Println(archived.Status, archived.ArchivedAt)
      ```

      ```java Java
      client.beta().sessions().events().send(
          session.id(),
          EventSendParams.builder()
              .addEvent(BetaManagedAgentsUserInterruptEventParams.builder()
                  .type(BetaManagedAgentsUserInterruptEventParams.Type.USER_INTERRUPT)
                  .sessionThreadId(thread.id())
                  .build())
              .build());

      archived = client.beta().sessions().threads().archive(
          thread.id(),
          ThreadArchiveParams.builder()
              .sessionId(session.id())
              .build());
      IO.println(archived.status() + " " + archived.archivedAt().orElseThrow());
      ```

      ```php PHP
      $client->beta->sessions->events->send(
          $session->id,
          events: [['type' => 'user.interrupt', 'session_thread_id' => $thread->id]],
      );
      $archived = $client->beta->sessions->threads->archive($thread->id, sessionID: $session->id);
      echo "{$archived->status} {$archived->archivedAt->format(DATE_ATOM)}\n";
      ```

      ```ruby Ruby
      client.beta.sessions.events.send_(
        session.id,
        events: [{type: "user.interrupt", session_thread_id: thread.id}]
      )
      archived = client.beta.sessions.threads.archive(thread.id, session_id: session.id)
      puts "#{archived.status} #{archived.archived_at}"
      ```
    </CodeGroup>
  </Tab>
</Tabs>

### Primary thread events

These events surface multiagent activity on the primary thread at `/v1/sessions/{session_id}/events/stream`. Message-direction events are named relative to the thread whose stream they appear on: `agent.thread_message_received` means a message arrived on this thread from another thread, and `agent.thread_message_sent` means this thread sent one. The task the coordinator delegates, for example, arrives on the child's own stream as an `agent.thread_message_received` event.

| Type                               | Description                                                                                                                                                |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `session.thread_created`           | A thread was created. Includes `session_thread_id` and `agent_name`.                                                                                       |
| `session.thread_status_running`    | A thread started activity.                                                                                                                                 |
| `session.thread_status_idle`       | The agent associated with the thread is awaiting input. Includes a `stop_reason` indicating why the agent stopped.                                         |
| `session.thread_status_terminated` | A thread was archived or encountered a terminal error.                                                                                                     |
| `agent.thread_message_received`    | On the primary thread, an agent sent a report or question to the coordinator. Includes `from_session_thread_id`, `from_agent_name`, and `content`.         |
| `agent.thread_message_sent`        | On the primary thread, the coordinator sent a task or follow-up message to another agent. Includes `to_session_thread_id`, `to_agent_name`, and `content`. |

Advisor consultations emit these same thread events under the reserved name `anthropic.advisor` (as `agent_name` on the thread lifecycle events and `from_agent_name` on the advice delivery); see [Give the session an advisor](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration#give-the-session-an-advisor) for the sequence.

### Session thread events

Critical events are proxied to the primary thread. However, you might still want to investigate a specific agent's reasoning and tool calls. To do so, stream or list the events from the associated session thread.

Each session thread has its own event stream at `/v1/sessions/{session_id}/threads/{thread_id}/stream`, and it accepts the same `event_deltas[]` parameter as the session-level stream, so you can preview a subagent's text as the model generates it. A connection previews only the thread it's reading: a child thread's previews never appear on the session-level stream, so to watch a subagent live, open its own thread stream. See [Preview session thread events](https://platform.claude.com/docs/en/managed-agents/events-and-streaming#preview-session-thread-events) for opting in, accumulating, and reconciling previews.

<Tabs>
  <Tab title="Stream session thread events">
    <CodeGroup>
      ```bash cURL
      curl -fsSN "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads/$THREAD_ID/stream?beta=true" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" |
        while IFS= read -r line; do
          [[ $line == data:* ]] || continue
          json=${line#data: }
          case $(jq -r '.type' <<<"$json") in
            agent.message)
              printf '%s' "$(jq -j '.content[] | select(.type == "text") | .text' <<<"$json")"
              ;;
            session.thread_status_idle)
              break
              ;;
          esac
        done
      ```

      ```bash CLI
      ant beta:sessions:threads:events stream \
        --session-id "$SESSION_ID" \
        --thread-id "$THREAD_ID"
      ```

      ```python Python
      with client.beta.sessions.threads.events.stream(
          thread.id,
          session_id=session.id,
      ) as stream:
          for event in stream:
              match event.type:
                  case "agent.message":
                      for block in event.content:
                          if block.type == "text":
                              print(block.text, end="")
                  case "session.thread_status_idle":
                      break
      ```

      ```typescript TypeScript
      const stream = await client.beta.sessions.threads.events.stream(thread.id, {
        session_id: session.id,
      });

      for await (const event of stream) {
        if (event.type === "agent.message") {
          for (const block of event.content) {
            if (block.type === "text") {
              process.stdout.write(block.text);
            }
          }
        } else if (event.type === "session.thread_status_idle") {
          break;
        }
      }
      ```

      ```csharp C#
      await foreach (var evt in client.Beta.Sessions.Threads.Events.StreamStreaming(thread.ID, new() { SessionID = session.ID }))
      {
          if (evt.Value is BetaManagedAgentsAgentMessageEvent message)
          {
              foreach (var block in message.Content)
              {
                  if (block.Type == "text")
                  {
                      Console.Write(block.Text);
                  }
              }
          }
          else if (evt.Value is BetaManagedAgentsSessionThreadStatusIdleEvent)
          {
              break;
          }
      }
      ```

      ```go Go
      	stream := client.Beta.Sessions.Threads.Events.StreamEvents(ctx, thread.ID, anthropic.BetaSessionThreadEventStreamParams{
      		SessionID: session.ID,
      	})
      	defer stream.Close()

      loop:
      	for stream.Next() {
      		event := stream.Current()
      		switch event.Type {
      		case "agent.message":
      			for _, block := range event.AsAgentMessage().Content {
      				if block.Type == "text" {
      					fmt.Print(block.Text)
      				}
      			}
      		case "session.thread_status_idle":
      			break loop
      		}
      	}
      	if err := stream.Err(); err != nil {
      		panic(err)
      	}
      ```

      ```java Java
      try (var streamResponse = client.beta().sessions().threads().events().streamStreaming(
          thread.id(),
          EventStreamParams.builder().sessionId(session.id()).build()
      )) {
          for (var event : (Iterable<BetaManagedAgentsStreamSessionThreadEvents>) streamResponse.stream()::iterator) {
              if (event.isAgentMessage()) {
                  for (var block : event.asAgentMessage().content()) {
                      block.text().ifPresent(textBlock -> IO.print(textBlock.text()));
                  }
              } else if (event.isSessionThreadStatusIdle()) {
                  break;
              }
          }
      }
      ```

      ```php PHP
      $stream = $client->beta->sessions->threads->events->streamStream(
          $thread->id,
          sessionID: $session->id,
      );

      foreach ($stream as $event) {
          if ($event->type === 'agent.message') {
              foreach ($event->content as $block) {
                  if ($block->type === 'text') {
                      echo $block->text;
                  }
              }
          } elseif ($event->type === 'session.thread_status_idle') {
              break;
          }
      }
      ```

      ```ruby Ruby
      client.beta.sessions.threads.events.stream_events(thread.id, session_id: session.id).each do |event|
        case event.type
        when :"agent.message"
          event.content.each do |block|
            print block.text if block.type == :text
          end
        when :"session.thread_status_idle"
          break
        end
      end
      ```
    </CodeGroup>
  </Tab>

  <Tab title="List session thread events">
    List all past session thread events to pull a complete history.

    <CodeGroup>
      ```bash cURL
      curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/threads/$THREAD_ID/events" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        | jq -r '.data[] | "[\(.type)] \(.processed_at)"'
      ```

      ```bash CLI
      ant beta:sessions:threads:events list \
        --session-id "$SESSION_ID" \
        --thread-id "$THREAD_ID"
      ```

      ```python Python
      for event in client.beta.sessions.threads.events.list(
          thread.id,
          session_id=session.id,
      ):
          print(f"[{event.type}] {event.processed_at}")
      ```

      ```typescript TypeScript
      for await (const event of client.beta.sessions.threads.events.list(thread.id, {
        session_id: session.id,
      })) {
        console.log(`[${event.type}] ${event.processed_at}`);
      }
      ```

      ```csharp C#
      var page = await client.Beta.Sessions.Threads.Events.List(thread.ID, new() { SessionID = session.ID });
      await foreach (var evt in page.Paginate())
      {
          Console.WriteLine($"[{evt.Type}] {evt.ProcessedAt}");
      }
      ```

      ```go Go
      pager := client.Beta.Sessions.Threads.Events.ListAutoPaging(ctx, thread.ID, anthropic.BetaSessionThreadEventListParams{
      	SessionID: session.ID,
      })
      for pager.Next() {
      	event := pager.Current()
      	fmt.Printf("[%s] %s\n", event.Type, event.ProcessedAt)
      }
      if err := pager.Err(); err != nil {
      	panic(err)
      }
      ```

      ```java Java
      for (var event : client.beta().sessions().threads().events().list(
              thread.id(),
              EventListParams.builder().sessionId(session.id()).build()
          ).autoPager()) {
          var type = event._json().orElseThrow() instanceof JsonObject json
              ? json.values().get("type").asStringOrThrow()
              : "unknown";
          var processedAt = event.processedAt().map(OffsetDateTime::toString).orElse("pending");
          IO.println("[" + type + "] " + processedAt);
      }
      ```

      ```php PHP
      foreach (
          $client->beta->sessions->threads->events->list(
              $thread->id,
              sessionID: $session->id,
          )->pagingEachItem() as $event
      ) {
          echo "[{$event->type}] {$event->processedAt->format(DATE_RFC3339)}\n";
      }
      ```

      ```ruby Ruby
      client.beta.sessions.threads.events.list(
        thread.id,
        session_id: session.id
      ).auto_paging_each do |event|
        puts "[#{event.type}] #{event.processed_at}"
      end
      ```
    </CodeGroup>
  </Tab>
</Tabs>

### Tool permissions and custom tools

If a subagent needs something from your client, such as [permission](https://platform.claude.com/docs/en/managed-agents/events-and-streaming#tool-confirmation) to run an `always_ask` tool, or the [result of a custom tool](https://platform.claude.com/docs/en/managed-agents/events-and-streaming#handling-custom-tool-calls), the event is cross-posted to the **primary thread** with `session_thread_id` identifying the originating session thread.

```json
{
  "type": "session.thread_status_idle",
  "id": "sevt_01ABC...",
  "session_thread_id": "sth_01DEF...",
  "agent_name": "code-reviewer",
  "stop_reason": {
    "type": "requires_action",
    "event_ids": ["sevt_01XYZ..."]
  }
}
```

Post `user.tool_confirmation` (with `tool_use_id`) or `user.custom_tool_result` (with `custom_tool_use_id`); the server routes the response to the correct thread automatically.

The following example extends the [tool confirmation handler](https://platform.claude.com/docs/en/managed-agents/events-and-streaming#tool-confirmation) to route replies. The same pattern applies to `user.custom_tool_result`.

<CodeGroup>
  ```bash cURL
  while IFS= read -r event_id; do
    jq -n --arg id "$event_id" \
      '{events: [{type: "user.tool_confirmation", tool_use_id: $id, result: "allow"}]}' |
      curl -fsS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        -d @-
  done < <(jq -r '.stop_reason.event_ids[]' <<<"$data")
  ```

  ```bash CLI
  # This workflow does not translate well to a one-off shell command.
  # Use one of the SDK examples in this code group instead.
  ```

  ```python Python
  for event_id in stop.event_ids:
      client.beta.sessions.events.send(
          session.id,
          events=[
              {
                  "type": "user.tool_confirmation",
                  "tool_use_id": event_id,
                  "result": "allow",
              }
          ],
      )
  ```

  ```typescript TypeScript
  for (const eventId of stop.event_ids) {
    await client.beta.sessions.events.send(session.id, {
      events: [
        {
          type: "user.tool_confirmation",
          tool_use_id: eventId,
          result: "allow",
        },
      ],
    });
  }
  ```

  ```csharp C#
  foreach (var eventId in requiresAction.EventIds)
  {
      await client.Beta.Sessions.Events.Send(session.ID, new()
      {
          Events =
          [
              new BetaManagedAgentsUserToolConfirmationEventParams
              {
                  Type = BetaManagedAgentsUserToolConfirmationEventParamsType.UserToolConfirmation,
                  ToolUseID = eventId,
                  Result = BetaManagedAgentsUserToolConfirmationEventParamsResult.Allow,
              },
          ],
      });
  }
  ```

  ```go Go
  for _, eventID := range stopReason.EventIDs {
  	params := anthropic.BetaManagedAgentsUserToolConfirmationEventParams{
  		Type:      anthropic.BetaManagedAgentsUserToolConfirmationEventParamsTypeUserToolConfirmation,
  		ToolUseID: eventID,
  		Result:    anthropic.BetaManagedAgentsUserToolConfirmationEventParamsResultAllow,
  	}
  	if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  		Events: []anthropic.BetaManagedAgentsEventParamsUnion{{OfUserToolConfirmation: &params}},
  	}); err != nil {
  		panic(err)
  	}
  }
  ```

  ```java Java
  for (var eventId : pendingToolUseIds) {
      client.beta().sessions().events().send(
          session.id(),
          EventSendParams.builder()
              .addEvent(BetaManagedAgentsUserToolConfirmationEventParams.builder()
                  .toolUseId(eventId)
                  .result(BetaManagedAgentsUserToolConfirmationEventParams.Result.ALLOW)
                  .build())
              .build()
      );
  }
  ```

  ```php PHP
  foreach ($event->stopReason->eventIDs as $eventId) {
      $client->beta->sessions->events->send($session->id, events: [[
          'type' => 'user.tool_confirmation',
          'tool_use_id' => $eventId,
          'result' => 'allow',
      ]]);
  }
  ```

  ```ruby Ruby
  event_ids.each do |event_id|
    client.beta.sessions.events.send_(session.id, events: [{
      type: "user.tool_confirmation",
      tool_use_id: event_id,
      result: "allow"
    }])
  end
  ```
</CodeGroup>
