# Start a session

Create a session to run your agent and begin executing tasks.

---

A session is an agent instance within an environment. Each session references an [agent](/docs/en/managed-agents/agent-setup) and an [environment](/docs/en/managed-agents/environments) (both created separately), and maintains conversation history across multiple interactions. Sessions follow a two-step lifecycle: first [create the session](#creating-a-session) to provision its sandbox, then [send a user event](#starting-the-session) to start work.

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Creating a session

A session requires an `agent` ID and an `environment` ID. Agents are versioned resources; passing in the `agent` ID as a string starts the session with the latest agent version.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$AGENT_ID",
    "environment_id": "$ENVIRONMENT_ID"
  }
  EOF
  )
  SESSION_ID=$(jq -r '.id' <<< "$session")
  ```

  ```bash CLI
  ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID"
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(agent.id())
      .environmentId(environment.id())
      .build());
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id
  )
  ```
</CodeGroup>

To pin a session to a specific agent version, pass an object. This lets you control exactly which version runs and stage rollouts of new versions independently.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  pinned_session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": {"type": "agent", "id": "$AGENT_ID", "version": 1},
    "environment_id": "$ENVIRONMENT_ID"
  }
  EOF
  )
  PINNED_SESSION_ID=$(jq -r '.id' <<< "$pinned_session")
  ```

  ```bash CLI
  ant beta:sessions create <<YAML
  agent:
    type: agent
    id: $AGENT_ID
    version: 1
  environment_id: $ENVIRONMENT_ID
  YAML
  ```

  ```python Python
  pinned_session = client.beta.sessions.create(
      agent={"type": "agent", "id": agent.id, "version": 1},
      environment_id=environment.id,
  )
  ```

  ```typescript TypeScript
  const pinnedSession = await client.beta.sessions.create({
    agent: { type: "agent", id: agent.id, version: 1 },
    environment_id: environment.id
  });
  ```

  ```csharp C#
  var pinnedSession = await client.Beta.Sessions.Create(new()
  {
      Agent = new BetaManagedAgentsAgentParams
      {
          Type = Anthropic.Models.Beta.Sessions.Type.Agent,
          ID = agent.ID,
          Version = 1,
      },
      EnvironmentID = environment.ID,
  });
  ```

  ```go Go
  pinnedSession, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfBetaManagedAgentsAgents: &anthropic.BetaManagedAgentsAgentParams{
  			Type:    anthropic.BetaManagedAgentsAgentParamsTypeAgent,
  			ID:      agent.ID,
  			Version: anthropic.Int(1),
  		},
  	},
  	EnvironmentID: environment.ID,
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var pinnedSession = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(BetaManagedAgentsAgentParams.builder()
          .type(BetaManagedAgentsAgentParams.Type.AGENT)
          .id(agent.id())
          .version(1)
          .build())
      .environmentId(environment.id())
      .build());
  ```

  ```php PHP
  $pinnedSession = $client->beta->sessions->create(
      agent: ['type' => 'agent', 'id' => $agent->id, 'version' => 1],
      environmentID: $environment->id,
  );
  ```

  ```ruby Ruby
  pinned_session = client.beta.sessions.create(
    agent: {type: :agent, id: agent.id, version: 1},
    environment_id: environment.id
  )
  ```
</CodeGroup>

### Override agent configuration for a session

You can pass `agent` in three forms: an agent ID string, a pinned-version object (`type: "agent"`), or an overrides object. The overrides form changes parts of the agent's configuration for a single session. Use it to try a different model or grant an extra tool in one session without versioning the agent. For the overrides form, set `type` to `agent_with_overrides` and pass the agent's `id` and optionally a `version` (omit `version` to use the agent's latest version). Then include any of `model`, `system`, `tools`, `mcp_servers`, or `skills` with the values the session should use.

Each overridable field follows the same three rules:

* **Omit the field:** The session inherits the value from the agent version it references.

* **Set the field to `null`, or to an empty array for list fields:** The session runs with that field cleared. This rule applies in full to `system`, `mcp_servers`, and `skills`. There are two exceptions:

  * `model` is never clearable. A session always needs a model, so `model: null` returns a 400 `agent_model_required` error.
  * Clearing `tools` returns a 400 error when the session's effective `skills` is non-empty, because skills require the `read` tool. Otherwise, `tools: null` and `tools: []` clear the field.

* **Set the field to a value:** The value replaces the agent's value in full. Overrides never merge with the agent's configuration, so a `tools` override must list every tool the session should have.

Overrides apply only to the session you create. They do not modify the agent resource or create a new agent version, so other sessions that reference the same agent are unaffected.

In the response, the `agent` object reflects the configuration the session runs with after the overrides are applied. Its `id` and `version` still identify the agent and version the overrides are applied to. This lets you trace a session back to its base agent.

The following example starts a session that overrides the model and clears the system prompt:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  override_session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": {
      "type": "agent_with_overrides",
      "id": "$AGENT_ID",
      "model": {"id": "claude-sonnet-5"},
      "system": null
    },
    "environment_id": "$ENVIRONMENT_ID"
  }
  EOF
  )
  jq '.agent | {id, version, model, system}' <<< "$override_session"
  OVERRIDE_SESSION_ID=$(jq -r '.id' <<< "$override_session")
  ```

  ```bash CLI
  # The response's `agent` is the resolved snapshot: each override replaces that
  # field for this session only, and the agent resource keeps its id and version.
  ant beta:sessions create \
    --transform 'agent.{id,version,model,system}' \
    --format json <<YAML
  agent:
    type: agent_with_overrides
    id: $AGENT_ID
    model:
      id: claude-sonnet-5
    system: null
  environment_id: $ENVIRONMENT_ID
  YAML
  ```

  ```python Python
  override_session = client.beta.sessions.create(
      agent={
          "type": "agent_with_overrides",
          "id": agent.id,
          "model": {"id": "claude-sonnet-5"},
          "system": None,  # clear the agent's system prompt for this session
      },
      environment_id=environment.id,
  )
  # The response's agent is the resolved snapshot with the overrides applied.
  print(f"Model: {override_session.agent.model.id}")
  print(f"System: {override_session.agent.system}")
  ```

  ```typescript TypeScript
  const overrideSession = await client.beta.sessions.create({
    agent: {
      type: "agent_with_overrides",
      id: agent.id,
      model: { id: "claude-sonnet-5" },
      system: null // clear the agent's system prompt for this session
    },
    environment_id: environment.id
  });
  // The response's agent is the resolved snapshot with the overrides applied.
  console.log(`Model: ${overrideSession.agent.model.id}`);
  console.log(`System: ${overrideSession.agent.system}`);
  ```

  ```csharp C#
  var overrideSession = await client.Beta.Sessions.Create(new()
  {
      Agent = new BetaManagedAgentsAgentWithOverridesParams
      {
          Type = BetaManagedAgentsAgentWithOverridesParamsType.AgentWithOverrides,
          ID = agent.ID,
          Model = new BetaManagedAgentsModelConfigParams
          {
              ID = BetaManagedAgentsModel.ClaudeSonnet5,
          },
          System = null, // clear the agent's system prompt for this session
      },
      EnvironmentID = environment.ID,
  });
  // The response's agent is the resolved snapshot with the overrides applied.
  Console.WriteLine($"Model: {overrideSession.Agent.Model.ID.Raw()}");
  Console.WriteLine($"System: {overrideSession.Agent.System ?? "null"}");
  ```

  ```go Go
  overrideSession, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfBetaManagedAgentsAgentWithOverridess: &anthropic.BetaManagedAgentsAgentWithOverridesParams{
  			Type: anthropic.BetaManagedAgentsAgentWithOverridesParamsTypeAgentWithOverrides,
  			ID:   agent.ID,
  			Model: anthropic.BetaManagedAgentsModelConfigParams{
  				ID: anthropic.BetaManagedAgentsModelClaudeSonnet5,
  			},
  			// Clear the agent's system prompt for this session.
  			System: param.Null[string](),
  		},
  	},
  	EnvironmentID: environment.ID,
  })
  if err != nil {
  	panic(err)
  }
  // The response's agent is the resolved snapshot with the overrides applied.
  fmt.Printf("Model: %s\n", overrideSession.Agent.Model.ID)
  fmt.Printf("System: %q\n", overrideSession.Agent.System)
  ```

  ```java Java
  var overrideSession = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(BetaManagedAgentsAgentWithOverridesParams.builder()
          .type(BetaManagedAgentsAgentWithOverridesParams.Type.AGENT_WITH_OVERRIDES)
          .id(agent.id())
          .model(BetaManagedAgentsModelConfigParams.builder()
              .id(BetaManagedAgentsModel.CLAUDE_SONNET_5)
              .build())
          .system((String) null) // clear the agent's system prompt for this session
          .build())
      .environmentId(environment.id())
      .build());
  // The response's agent is the resolved snapshot with the overrides applied.
  IO.println("Model: " + overrideSession.agent().model().id());
  IO.println("System: " + overrideSession.agent().system().orElse("null"));
  ```

  ```php PHP
  $overrides = BetaManagedAgentsAgentWithOverridesParams::with(
      id: $agent->id,
      type: 'agent_with_overrides',
      model: ['id' => 'claude-sonnet-5'],
  );
  // Clear the system prompt for this session. Array access is load-bearing here:
  // create() strips nulls from raw arrays and ::with() treats null args as omitted.
  $overrides['system'] = null;

  $overrideSession = $client->beta->sessions->create(
      agent: $overrides,
      environmentID: $environment->id,
  );
  // The response's agent is the resolved snapshot with the overrides applied.
  echo "Model: {$overrideSession->agent->model->id}\n";
  echo 'System: ' . ($overrideSession->agent->system ?? 'null') . "\n";
  ```

  ```ruby Ruby
  # The system prompt override is `system_` (trailing underscore) because plain
  # `system` is Ruby's Kernel#system. Setting it to nil clears the prompt.
  override_session = client.beta.sessions.create(
    agent: Anthropic::Beta::BetaManagedAgentsAgentWithOverridesParams.new(
      type: :agent_with_overrides,
      id: agent.id,
      model: {id: "claude-sonnet-5"},
      system_: nil
    ),
    environment_id: environment.id
  )
  # The response's agent is the resolved snapshot with the overrides applied.
  puts "Model: #{override_session.agent.model.id}"
  puts "System: #{override_session.agent.system_.inspect}"
  ```
</CodeGroup>

<Tip>
  The agent defines how Claude behaves within the session, including the model, system prompt, tools, and MCP servers. See [Define your agent](/docs/en/managed-agents/agent-setup) for details.
</Tip>

## MCP authentication through vaults

If your agent uses MCP tools that require authentication, pass `vault_ids` at session creation to reference a vault containing stored OAuth credentials. Anthropic manages token refresh on your behalf. See [Authenticate with vaults](/docs/en/managed-agents/vaults) for how to create vaults and register credentials.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  vault_session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$AGENT_ID",
    "environment_id": "$ENVIRONMENT_ID",
    "vault_ids": ["$VAULT_ID"]
  }
  EOF
  )
  VAULT_SESSION_ID=$(jq -r '.id' <<< "$vault_session")
  ```

  ```bash CLI
  ant beta:sessions create <<YAML
  agent: $AGENT_ID
  environment_id: $ENVIRONMENT_ID
  vault_ids:
    - $VAULT_ID
  YAML
  ```

  ```python Python
  vault_session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      vault_ids=[vault.id],
  )
  ```

  ```typescript TypeScript
  const vaultSession = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    vault_ids: [vault.id]
  });
  ```

  ```csharp C#
  var vaultSession = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      VaultIds = [vault.ID],
  });
  ```

  ```go Go
  vaultSession, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  	VaultIDs:      []string{vault.ID},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var vaultSession = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(agent.id())
      .environmentId(environment.id())
      .addVaultId(vault.id())
      .build());
  ```

  ```php PHP
  $vaultSession = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      vaultIDs: [$vault->id],
  );
  ```

  ```ruby Ruby
  vault_session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    vault_ids: [vault.id]
  )
  ```
</CodeGroup>

## Starting the session

Creating a session provisions the environment's sandbox but does not start any work. To delegate a task, send events to the session using a [user event](/docs/en/managed-agents/reference#event-types). The session acts as a state machine that tracks progress while events drive the actual execution.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsSL "https://api.anthropic.com/v1/sessions/$SESSION_ID/events" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "events": [
      {
        "type": "user.message",
        "content": [{"type": "text", "text": "List the files in the working directory."}]
      }
    ]
  }
  EOF
  ```

  ```bash CLI
  ant beta:sessions:events send \
    --session-id "$SESSION_ID" <<'YAML'
  events:
    - type: user.message
      content:
        - type: text
          text: List the files in the working directory.
  YAML
  ```

  ```python Python
  client.beta.sessions.events.send(
      session.id,
      events=[
          {
              "type": "user.message",
              "content": [
                  {"type": "text", "text": "List the files in the working directory."}
              ],
          },
      ],
  )
  ```

  ```typescript TypeScript
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.message",
        content: [{ type: "text", text: "List the files in the working directory." }]
      }
    ]
  });
  ```

  ```csharp C#
  await client.Beta.Sessions.Events.Send(session.ID, new()
  {
      Events =
      [
          new BetaManagedAgentsUserMessageEventParams
          {
              Type = BetaManagedAgentsUserMessageEventParamsType.UserMessage,
              Content =
              [
                  new BetaManagedAgentsTextBlock
                  {
                      Type = BetaManagedAgentsTextBlockType.Text,
                      Text = "List the files in the working directory.",
                  },
              ],
          },
      ],
  });
  ```

  ```go Go
  if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  		OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
  			Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
  			Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
  				OfText: &anthropic.BetaManagedAgentsTextBlockParam{
  					Type: anthropic.BetaManagedAgentsTextBlockTypeText,
  					Text: "List the files in the working directory.",
  				},
  			}},
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
          .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
              .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
              .addTextContent("List the files in the working directory.")
              .build())
          .build());
  ```

  ```php PHP
  $client->beta->sessions->events->send(
      $session->id,
      events: [
          [
              'type' => 'user.message',
              'content' => [['type' => 'text', 'text' => 'List the files in the working directory.']],
          ],
      ],
  );
  ```

  ```ruby Ruby
  client.beta.sessions.events.send_(
    session.id,
    events: [
      {
        type: :"user.message",
        content: [{type: :text, text: "List the files in the working directory."}]
      }
    ]
  )
  ```
</CodeGroup>

See [Session event stream](/docs/en/managed-agents/events-and-streaming) for how to stream the agent's responses and handle tool confirmations.

See [Session statuses](/docs/en/managed-agents/session-operations#session-statuses) for the statuses a session moves through.

## Next steps

<CardGroup cols={3}>
  <Card title="Session operations" icon="settings" href="/docs/en/managed-agents/session-operations">
    Retrieve, list, update, archive, and delete Claude Managed Agents sessions.
  </Card>

  <Card title="Session event stream" icon="lightning" href="/docs/en/managed-agents/events-and-streaming">
    Send events, stream responses, and interrupt or redirect your session mid-execution.
  </Card>

  <Card title="Scheduled deployments" icon="arrows-clockwise" href="/docs/en/managed-agents/scheduled-deployments">
    Create and manage deployments with the Claude API: run an agent on a recurring cron schedule and inspect its run history.
  </Card>
</CardGroup>
