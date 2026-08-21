---
title: Start a session
url: https://platform.claude.com/docs/en/managed-agents/sessions
description: Create a session to run your agent and begin executing tasks.
---

A session is an agent instance within an environment. Each session references an [agent](https://platform.claude.com/docs/en/managed-agents/agent-setup) and an [environment](https://platform.claude.com/docs/en/managed-agents/environments) (both created separately), and maintains conversation history across multiple interactions. Sessions follow a two-step lifecycle: first [create the session](https://platform.claude.com/docs/en/managed-agents/sessions#creating-a-session), then [send a user event](https://platform.claude.com/docs/en/managed-agents/sessions#starting-the-session) to start work. You can also collapse both steps into one call with [`initial_events`](https://platform.claude.com/docs/en/managed-agents/sessions#seed-the-session-with-initial-events).

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](https://platform.claude.com/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Creating a session

A session requires an `agent` ID and an `environment` ID. Agents are versioned resources; passing in the `agent` ID as a string creates the session with the latest agent version.

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
          Type = BetaManagedAgentsAgentParamsType.Agent,
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

### Seed the session with initial events

You can create a session and start its work in one call. `initial_events` is an optional array of initial [events](https://platform.claude.com/docs/en/managed-agents/reference#event-types) to send to the session at creation, processed in order. It supports `user.message` and [`user.define_outcome`](https://platform.claude.com/docs/en/managed-agents/define-outcomes) events, and accepts a maximum of 50 events. A non-empty list starts the agent loop in the same call: the session is created directly in the `running` status, with no further request.

The following example creates a session with a single `user.message` in `initial_events`:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  seeded_session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$AGENT_ID",
    "environment_id": "$ENVIRONMENT_ID",
    "initial_events": [
      {
        "type": "user.message",
        "content": [{"type": "text", "text": "List the files in the working directory."}]
      }
    ]
  }
  EOF
  )
  SEEDED_SESSION_ID=$(jq -r '.id' <<< "$seeded_session")

  # initial_events aren't echoed on the create response; list the session's
  # events to see the seeded message.
  seeded_events=$(curl -fsSL \
    "https://api.anthropic.com/v1/sessions/$SEEDED_SESSION_ID/events" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")
  echo "Seeded event: $(jq -r \
    '.data[] | select(.type == "user.message") | .content[0].text' <<< "$seeded_events")"
  ```

  ```bash CLI
  SEEDED_SESSION_ID=$(ant beta:sessions create \
    --transform id --raw-output <<YAML
  agent: $AGENT_ID
  environment_id: $ENVIRONMENT_ID
  initial_events:
    - type: user.message
      content:
        - type: text
          text: List the files in the working directory.
  YAML
  )

  # initial_events aren't echoed on the create response; list the session's
  # events to see the seeded message.
  echo "Seeded event: $(ant beta:sessions:events list \
    --session-id "$SEEDED_SESSION_ID" \
    --format raw \
    --transform 'data.#(type=="user.message").content.0.text' --raw-output)"
  ```

  ```python Python
  seeded_session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      initial_events=[
          {
              "type": "user.message",
              "content": [
                  {"type": "text", "text": "List the files in the working directory."}
              ],
          },
      ],
  )
  # initial_events are not echoed on the create response; read them back
  # from the session's event list.
  for event in client.beta.sessions.events.list(seeded_session.id):
      if event.type == "user.message":
          for block in event.content:
              if block.type == "text":
                  print(f"Seeded event: {block.text}")
  ```

  ```typescript TypeScript
  const seededSession = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    initial_events: [
      {
        type: "user.message",
        content: [{ type: "text", text: "List the files in the working directory." }]
      }
    ]
  });

  // initial_events are not echoed on the create response; list the session's
  // events to read the seeded message back.
  for await (const event of client.beta.sessions.events.list(seededSession.id)) {
    if (event.type === "user.message") {
      for (const block of event.content) {
        if (block.type === "text") {
          console.log(`Seeded event: ${block.text}`);
        }
      }
    }
  }
  ```

  ```csharp C#
  var seededSession = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      InitialEvents =
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
  // initial_events are not echoed on the create response; read them back
  // from the session's event list.
  var seededEvents = await client.Beta.Sessions.Events.List(seededSession.ID);
  await foreach (var sessionEvent in seededEvents.Paginate())
  {
      if (sessionEvent.TryPickUserMessage(out var userMessage))
      {
          foreach (var contentBlock in userMessage.Content)
          {
              if (contentBlock.TryPickBetaManagedAgentsTextBlock(out var textBlock))
              {
                  Console.WriteLine($"Seeded event: {textBlock.Text}");
              }
          }
      }
  }
  ```

  ```go Go
  seededSession, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  	InitialEvents: []anthropic.BetaSessionNewParamsInitialEventUnion{{
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
  })
  if err != nil {
  	panic(err)
  }
  // initial_events are not echoed on the create response, so list the
  // session's events to read the seeded user.message back.
  seededEvents, err := client.Beta.Sessions.Events.List(ctx, seededSession.ID, anthropic.BetaSessionEventListParams{})
  if err != nil {
  	panic(err)
  }
  for _, event := range seededEvents.Data {
  	if event.Type != "user.message" {
  		continue
  	}
  	for _, contentBlock := range event.AsUserMessage().Content {
  		if contentBlock.Type == "text" {
  			fmt.Printf("Seeded event: %s\n", contentBlock.AsText().Text)
  		}
  	}
  }
  ```

  ```java Java
  var seededSession = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(agent.id())
      .environmentId(environment.id())
      .addInitialEvent(BetaManagedAgentsUserMessageEventParams.builder()
          .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
          .addTextContent("List the files in the working directory.")
          .build())
      .build());
  // initial_events are not echoed on the create response; list the
  // session's events to read the seeded user.message back.
  for (var event : client.beta().sessions().events().list(seededSession.id()).autoPager()) {
      if (event.isUserMessage()) {
          for (var contentBlock : event.asUserMessage().content()) {
              if (contentBlock.isText()) {
                  IO.println("Seeded event: " + contentBlock.asText().text());
              }
          }
      }
  }
  ```

  ```php PHP
  $seededSession = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      initialEvents: [
          [
              'type' => 'user.message',
              'content' => [['type' => 'text', 'text' => 'List the files in the working directory.']],
          ],
      ],
  );

  // initial_events are not echoed on the create response; read them back
  // from the session's event list.
  $seededEvents = $client->beta->sessions->events->list($seededSession->id);
  foreach ($seededEvents->getItems() as $event) {
      if ($event->type === 'user.message') {
          echo "Seeded event: {$event->content[0]->text}\n";
      }
  }
  ```

  ```ruby Ruby
  seeded_session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    initial_events: [
      {
        type: :"user.message",
        content: [{type: :text, text: "List the files in the working directory."}]
      }
    ]
  )

  # initial_events are not echoed on the create response; read them back from
  # the session's event list.
  client.beta.sessions.events.list(seeded_session.id).auto_paging_each do |event|
    next unless event.type == :"user.message"
    event.content.each do |block|
      puts "Seeded event: #{block.text}" if block.type == :text
    end
  end
  ```
</CodeGroup>

No other event type is accepted. Events that respond to an agent turn (`user.tool_confirmation`, `user.tool_result`, and `user.custom_tool_result`) aren't accepted because no agent turn exists yet, and `user.interrupt` isn't accepted because there is no turn to stop. Unlike `initial_events` on a scheduled deployment, a session's `initial_events` don't accept `system.message`.

Each event in `initial_events` is validated and persisted before the create response returns, in list order, with a server-assigned ID, exactly as if you had posted it to the [send events](https://platform.claude.com/docs/en/managed-agents/events-and-streaming) endpoint immediately after creation. Per-event content rules are also the same as on that endpoint. An empty list is equivalent to omitting the field. Validation is all-or-nothing: if any event fails validation, the whole request is rejected and no session is created.

The create request is rejected in the following cases:

| Condition                                                                                                                                                 | Status |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| More than one `user.define_outcome` event                                                                                                                 | 400    |
| A `user.define_outcome` event without a `rubric`                                                                                                          | 400    |
| More than 100 file-sourced [`document` content blocks](https://platform.claude.com/docs/en/build-with-claude/files#document-blocks) across the whole list | 400    |
| A request body over 32 MB                                                                                                                                 | 413    |

A `user.define_outcome` event in `initial_events` is accepted under the same conditions as sending one to an existing session; see [Define outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes).

### Override agent configuration for a session

You can pass `agent` in three forms: an agent ID string, a pinned-version object (`type: "agent"`), or an overrides object. The overrides form changes parts of the agent's configuration for a single session. Use it to try a different model or grant an extra tool in one session without versioning the agent. For the overrides form, set `type` to `agent_with_overrides` and pass the agent's `id` and optionally a `version` (omit `version` to use the agent's latest version). Then include any of `model`, `system`, `tools`, `mcp_servers`, or `skills` with the values the session should use.

Each overridable field follows the same three rules:

* **Omit the field:** The session inherits the value from the agent version it references.

* **Set the field to `null`, or to an empty array for list fields:** The session runs with that field cleared. This rule applies in full to `system` and `skills`. There are three exceptions:

  * `model` is never clearable. A session always needs a model, so `model: null` returns a 400 `agent_model_required` error.
  * Clearing `tools` returns a 400 error when the session's effective `skills` is non-empty, because skills require the `read` tool. Otherwise, `tools: null` and `tools: []` clear the field.
  * Clearing `mcp_servers` returns a 400 error when the session's effective `tools` still contains an `mcp_toolset` that references one of the agent's servers. Override `tools` in the same request to remove those `mcp_toolset` entries, then clear `mcp_servers`.

* **Set the field to a value:** The value replaces the agent's value in full. Overrides never merge with the agent's configuration, so a `tools` override must list every tool the session should have. There is one exception:
  * An `effort` level inside a per-session `model` override isn't applied, and because the override replaces the agent's `model` object in full, the agent's own `effort` isn't carried over either: a session created with a `model` override runs at the model's default effort level. To run at a specific effort level, set `effort` on the [agent](https://platform.claude.com/docs/en/managed-agents/agent-setup#agent-configuration-fields) and don't override `model` for that session.

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

#### Pin the inference geo for a session

Because a `model` override replaces the agent's `model` object in full, it also sets or clears the model's [`inference_geo`](https://platform.claude.com/docs/en/manage-claude/data-residency) pin for the session: an override that includes `inference_geo` pins the geography that serves the session's model requests, and one that omits it clears the agent's pin so the session follows the workspace's `default_inference_geo`. The overridden value is validated against the workspace's `allowed_inference_geos` when the session is created.

The following example starts a session from an agent whose model has no geo pin, pins the session's model requests to US inference by including `inference_geo` in the `model` override, and prints the value echoed in the response's `agent.model`:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  # Replaces the agent's `model` in full: restate `id`, add `inference_geo` to pin.
  session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": {
      "type": "agent_with_overrides",
      "id": "$AGENT_ID",
      "model": {"id": "claude-opus-5", "inference_geo": "us"}
    },
    "environment_id": "$ENVIRONMENT_ID"
  }
  EOF
  )
  echo "Inference geo: $(jq -r '.agent.model.inference_geo' <<< "$session")"
  ```

  ```bash CLI
  # Replaces the agent's `model` in full: restate `id`, add `inference_geo` to pin.
  session=$(ant beta:sessions create <<YAML
  agent:
    type: agent_with_overrides
    id: $AGENT_ID
    model:
      id: claude-opus-5
      inference_geo: us
  environment_id: $ENVIRONMENT_ID
  YAML
  )
  echo "Inference geo: $(jq -r '.agent.model.inference_geo' <<< "$session")"
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent={
          "type": "agent_with_overrides",
          "id": agent.id,
          # Replaces the agent's `model` in full: restate `id`, add `inference_geo` to pin.
          "model": {"id": "claude-opus-5", "inference_geo": "us"},
      },
      environment_id=environment.id,
  )
  print(f"Inference geo: {session.agent.model.inference_geo}")
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: {
      type: "agent_with_overrides",
      id: agent.id,
      // Replaces the agent's `model` in full: restate `id`, add `inference_geo` to pin.
      model: { id: "claude-opus-5", inference_geo: "us" }
    },
    environment_id: environment.id
  });
  console.log(`Inference geo: ${session.agent.model.inference_geo}`);
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = new BetaManagedAgentsAgentWithOverridesParams
      {
          Type = BetaManagedAgentsAgentWithOverridesParamsType.AgentWithOverrides,
          ID = agent.ID,
          // Replaces the agent's `model` in full: restate `id`, add `inference_geo` to pin.
          Model = new BetaManagedAgentsModelConfigParams
          {
              ID = BetaManagedAgentsModel.ClaudeOpus5,
              InferenceGeo = "us",
          },
      },
      EnvironmentID = environment.ID,
  });
  Console.WriteLine($"Inference geo: {session.Agent.Model.InferenceGeo}");
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfBetaManagedAgentsAgentWithOverridess: &anthropic.BetaManagedAgentsAgentWithOverridesParams{
  			Type: anthropic.BetaManagedAgentsAgentWithOverridesParamsTypeAgentWithOverrides,
  			ID:   agent.ID,
  			// Replaces the agent's `model` in full: restate `id`, add `inference_geo` to pin.
  			Model: anthropic.BetaManagedAgentsModelConfigParams{
  				ID:           anthropic.BetaManagedAgentsModelClaudeOpus5,
  				InferenceGeo: anthropic.String("us"),
  			},
  		},
  	},
  	EnvironmentID: environment.ID,
  })
  if err != nil {
  	panic(err)
  }
  fmt.Printf("Inference geo: %s\n", session.Agent.Model.InferenceGeo)
  ```

  ```java Java
  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(BetaManagedAgentsAgentWithOverridesParams.builder()
          .type(BetaManagedAgentsAgentWithOverridesParams.Type.AGENT_WITH_OVERRIDES)
          .id(agent.id())
          // Replaces the agent's `model` in full: restate `id`, add `inference_geo` to pin.
          .model(BetaManagedAgentsModelConfigParams.builder()
              .id(BetaManagedAgentsModel.CLAUDE_OPUS_5)
              .inferenceGeo("us")
              .build())
          .build())
      .environmentId(environment.id())
      .build());
  IO.println("Inference geo: " + session.agent().model().inferenceGeo().orElseThrow());
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: BetaManagedAgentsAgentWithOverridesParams::with(
          id: $agent->id,
          type: 'agent_with_overrides',
          // Replaces the agent's `model` in full: restate `id`, add `inference_geo` to pin.
          model: BetaManagedAgentsModelConfigParams::with(
              id: 'claude-opus-5',
              inferenceGeo: 'us',
          ),
      ),
      environmentID: $environment->id,
  );
  echo "Inference geo: {$session->agent->model->inferenceGeo}\n";
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: {
      type: :agent_with_overrides,
      id: agent.id,
      # Replaces the agent's `model` in full: restate `id`, add `inference_geo` to pin.
      model: {id: "claude-opus-5", inference_geo: "us"}
    },
    environment_id: environment.id
  )
  puts "Inference geo: #{session.agent.model.inference_geo}"
  ```
</CodeGroup>

<Tip>
  The agent defines how Claude behaves within the session, including the model, system prompt, tools, and MCP servers. See [Define your agent](https://platform.claude.com/docs/en/managed-agents/agent-setup) for details.
</Tip>

### Set a session budget

To cap what a session can spend, pass the optional `budget` object when you create it. A budget is a hard ceiling on the session's list cost: the platform prices everything the session consumes at public list rates, and the session stops issuing new model requests once that running total reaches `max_list_cost`. Set `type` to `limit` and give `max_list_cost` an `amount` and a `currency`. `amount` is a whole number of US cents written as a string, such as `"2500"` for $25.00; the API takes a string rather than a number so no floating-point rounding is ever applied. `USD` is the only currency currently supported. When the session reaches the cap, it pauses and goes idle with the stop reason `budget_reached`. The cap is enforced between model requests, so the request that crosses it finishes first and the session's final list cost can land [a fraction past the cap](https://platform.claude.com/docs/en/managed-agents/budgets#when-a-session-reaches-its-budget). A budget can only be attached at creation: you can [change or remove](https://platform.claude.com/docs/en/managed-agents/session-operations#updating-the-session-budget) it later, but you can't add one to a session created without it.

The following example creates a session with a $25.00 budget; the response echoes the `budget` on the session resource:

```bash cURL
curl -fsSL https://api.anthropic.com/v1/sessions \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d @- <<EOF
{
  "agent": "$AGENT_ID",
  "environment_id": "$ENVIRONMENT_ID",
  "budget": {
    "type": "limit",
    "max_list_cost": {"amount": "2500", "currency": "USD"}
  }
}
EOF
```

See [Session budgets](https://platform.claude.com/docs/en/managed-agents/budgets) for how enforcement works, what counts toward list cost, and how budgets behave in multiagent sessions.

## MCP authentication through vaults

If your agent uses MCP tools that require authentication, pass `vault_ids` at session creation to reference a vault containing stored OAuth credentials. Anthropic manages token refresh on your behalf. See [Authenticate with vaults](https://platform.claude.com/docs/en/managed-agents/vaults) for how to create vaults and register credentials.

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

Creating a session without `initial_events` registers the session but does not start any work; the environment's sandbox begins provisioning as soon as the session is created, so the first tool call does not wait on it. To delegate a task, send events to the session using a [user event](https://platform.claude.com/docs/en/managed-agents/reference#event-types). To supply the first event in the create request instead, see [Seed the session with initial events](https://platform.claude.com/docs/en/managed-agents/sessions#seed-the-session-with-initial-events). The session acts as a state machine that tracks progress while events drive the actual execution.

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

See [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming) for how to stream the agent's responses and handle tool confirmations.

See [Session statuses](https://platform.claude.com/docs/en/managed-agents/session-operations#session-statuses) for the statuses a session moves through.

## Next steps

<CardGroup cols={3}>
  <Card title="Session operations" icon="settings" href="https://platform.claude.com/docs/en/managed-agents/session-operations">
    Retrieve, list, update, archive, and delete Claude Managed Agents sessions.
  </Card>

  <Card title="Session event stream" icon="lightning" href="https://platform.claude.com/docs/en/managed-agents/events-and-streaming">
    Send events, stream responses, and interrupt or redirect your session mid-execution.
  </Card>

  <Card title="Scheduled deployments" icon="arrows-clockwise" href="https://platform.claude.com/docs/en/managed-agents/scheduled-deployments">
    Create and manage deployments with the Claude API: run an agent on a recurring cron schedule and inspect its run history.
  </Card>
</CardGroup>
