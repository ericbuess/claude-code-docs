---
title: Define your agent
url: https://platform.claude.com/docs/en/managed-agents/agent-setup
description: Create a reusable, versioned agent configuration.
---

An agent is a reusable, versioned configuration that defines persona and capabilities. It bundles the model, system prompt, tools, MCP servers, and skills that shape how Claude behaves during a session.

Create the agent once as a reusable resource and reference it by ID each time you [start a session](https://platform.claude.com/docs/en/managed-agents/sessions). Agents are versioned and easier to manage across many sessions.

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](https://platform.claude.com/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Agent configuration fields

| Field         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | Required. A human-readable name for the agent.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `model`       | Required. The Claude [model](https://platform.claude.com/docs/en/about-claude/models/overview) that powers the agent. Accepts a model ID string or an object, for example `{"id": "claude-opus-5"}`. Claude 4.5 and later models are supported. The object form also accepts `speed`, `effort`, and `inference_geo` fields; see the tips under [Create an agent](https://platform.claude.com/docs/en/managed-agents/agent-setup#create-an-agent), [Effort levels](https://platform.claude.com/docs/en/build-with-claude/effort#effort-levels), and [Pin the inference geo](https://platform.claude.com/docs/en/managed-agents/agent-setup#pin-the-inference-geo). |
| `system`      | A [system prompt](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#give-claude-a-role) that defines the agent's behavior and persona. The system prompt is distinct from [user messages](https://platform.claude.com/docs/en/managed-agents/reference#event-types), which should describe the work to be done.                                                                                                                                                                                                                                                                                            |
| `tools`       | The tools available to the agent. Combines [pre-built agent tools](https://platform.claude.com/docs/en/managed-agents/tools), [MCP tools](https://platform.claude.com/docs/en/managed-agents/mcp-connector), and [custom tools](https://platform.claude.com/docs/en/managed-agents/tools#custom-tools).                                                                                                                                                                                                                                                                                                                                                           |
| `mcp_servers` | [MCP servers](https://platform.claude.com/docs/en/managed-agents/mcp-connector) that provide standardized third-party capabilities.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `skills`      | [Skills](https://platform.claude.com/docs/en/managed-agents/skills) that supply domain-specific context with progressive disclosure.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `multiagent`  | A coordinator declaration listing the agents this agent can delegate to. See [Multiagent orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration).                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `description` | A description of what the agent does.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `metadata`    | Arbitrary key-value pairs for your own tracking.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

You can also override `model`, `system`, `tools`, `mcp_servers`, and `skills` for a single session without changing the agent. An `effort` level set inside a per-session `model` override isn't applied, and because the override replaces the agent's `model` object in full, a session created with a `model` override runs at the model's default effort level; to run at a specific effort level, set `effort` on the agent and don't override `model` for that session. See [Override agent configuration for a session](https://platform.claude.com/docs/en/managed-agents/sessions#override-agent-configuration-for-a-session).

## Create an agent

The following example defines a coding agent that uses Claude Opus 5 with access to the pre-built agent toolset. The toolset lets the agent write code, read files, search the web, and more. See the [agent tools reference](https://platform.claude.com/docs/en/managed-agents/tools) for the full list of supported tools.

The examples use curl, the `ant` CLI, or one of the SDKs. If you haven't set one up, the [quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart#install-the-cli) covers installation and client setup.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Coding Assistant",
      "model": "claude-opus-5",
      "system": "You are a helpful coding agent.",
      "tools": [{"type": "agent_toolset_20260401"}]
    }')

  AGENT_ID=$(jq -r '.id' <<< "$agent")
  AGENT_VERSION=$(jq -r '.version' <<< "$agent")
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    agent=$(ant beta:agents create --format json < coding-assistant.agent.yaml)

    AGENT_ID=$(jq -r '.id' <<< "$agent")
    ```

    <File filename="coding-assistant.agent.yaml">
      ```yaml
      name: Coding Assistant
      model:
        id: claude-opus-5
      system: You are a helpful coding agent.
      tools:
        - type: agent_toolset_20260401
      ```
    </File>
  </MultiFileExample>

  ```python Python
  agent = client.beta.agents.create(
      name="Coding Assistant",
      model="claude-opus-5",
      system="You are a helpful coding agent.",
      tools=[
          {"type": "agent_toolset_20260401"},
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Coding Assistant",
    model: "claude-opus-5",
    system: "You are a helpful coding agent.",
    tools: [{ type: "agent_toolset_20260401" }],
  });
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Coding Assistant",
      Model = BetaManagedAgentsModel.ClaudeOpus5,
      System = "You are a helpful coding agent.",
      Tools =
      [
          new BetaManagedAgentsAgentToolset20260401Params
          {
              Type = "agent_toolset_20260401",
          },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Coding Assistant",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: anthropic.BetaManagedAgentsModelClaudeOpus5,
  	},
  	System: anthropic.String("You are a helpful coding agent."),
  	Tools: []anthropic.BetaAgentNewParamsToolUnion{{
  		OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
  			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Coding Assistant")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_5)
          .system("You are a helpful coding agent.")
          .addTool(
              BetaManagedAgentsAgentToolset20260401Params.builder()
                  .type(BetaManagedAgentsAgentToolset20260401Params.Type.AGENT_TOOLSET_20260401)
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'Coding Assistant',
      model: 'claude-opus-5',
      system: 'You are a helpful coding agent.',
      tools: [
          BetaManagedAgentsAgentToolset20260401Params::with(
              type: 'agent_toolset_20260401',
          ),
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Coding Assistant",
    model: "claude-opus-5",
    system_: "You are a helpful coding agent.",
    tools: [{type: "agent_toolset_20260401"}]
  )
  ```
</CodeGroup>

The response echoes your configuration and adds `id`, `type`, `version`, `created_at`, `updated_at`, and `archived_at` fields, and fills in `model` fields you omit, such as `effort`, with their defaults. The `version` starts at 1 and increments each time an update changes the agent.

```json
{
  "id": "agent_01HqR2k7vXbZ9mNpL3wYcT8f",
  "type": "agent",
  "name": "Coding Assistant",
  "model": {
    "id": "claude-opus-5",
    "effort": { "type": "high" },
    "speed": "standard"
  },
  "system": "You are a helpful coding agent.",
  "description": null,
  "tools": [
    {
      "type": "agent_toolset_20260401",
      "default_config": {
        "permission_policy": { "type": "always_allow" }
      }
    }
  ],
  "skills": [],
  "mcp_servers": [],
  "multiagent": null,
  "metadata": {},
  "version": 1,
  "created_at": "2026-04-03T18:24:10.412Z",
  "updated_at": "2026-04-03T18:24:10.412Z",
  "archived_at": null
}
```

The `default_config` on the toolset shows its default [permission policy](https://platform.claude.com/docs/en/managed-agents/permission-policies), `always_allow`, which applies unless you configure one.

<Tip>
  To use Claude Opus 5 or Claude Opus 4.8 with [fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode), pass `model` as an object, for example: `{"id": "claude-opus-5", "speed": "fast"}`. See the fast mode page's [supported models](https://platform.claude.com/docs/en/build-with-claude/fast-mode#supported-models).
</Tip>

<Tip>
  To set the model's effort level, pass `model` as an object, for example: `{"id": "claude-opus-5", "effort": "high"}`. The `effort` field accepts a level string (`low`, `medium`, `high`, `xhigh`, or `max`) or an object such as `{"type": "high"}`. See [Effort levels](https://platform.claude.com/docs/en/build-with-claude/effort#effort-levels) for what each level does.
</Tip>

### Pin the inference geo

Like `speed` and `effort`, `inference_geo` is set through the object form of `model`: pass `model` as an object and set `inference_geo` alongside `id`. The field accepts `"us"` or `"global"`. When it's unset, each model request follows the workspace's default inference geo at the time it's served. See [Data residency](https://platform.claude.com/docs/en/manage-claude/data-residency) for the workspace-level geo controls and pricing.

The following example pins an agent to US inference and prints the `inference_geo` value echoed in the response's `model` object:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent=$(curl -fsSL https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "name": "Geo-pinned assistant",
      "model": {"id": "claude-opus-5", "inference_geo": "us"},
      "system": "You are a helpful assistant."
    }')

  echo "Inference geo: $(jq -r '.model.inference_geo' <<< "$agent")"
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    agent=$(ant beta:agents create --format json < geo-pinned.agent.yaml)

    echo "Inference geo: $(jq -r '.model.inference_geo' <<< "$agent")"
    ```

    <File filename="geo-pinned.agent.yaml">
      ```yaml
      name: Geo-pinned assistant
      model:
        id: claude-opus-5
        inference_geo: us
      system: You are a helpful assistant.
      ```
    </File>
  </MultiFileExample>

  ```python Python
  agent = client.beta.agents.create(
      name="Geo-pinned assistant",
      model={
          "id": "claude-opus-5",
          "inference_geo": "us",
      },
      system="You are a helpful assistant.",
  )

  print(f"Inference geo: {agent.model.inference_geo}")
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Geo-pinned assistant",
    model: { id: "claude-opus-5", inference_geo: "us" },
    system: "You are a helpful assistant.",
  });

  console.log(`Inference geo: ${agent.model.inference_geo}`);
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Geo-pinned assistant",
      Model = new BetaManagedAgentsModelConfigParams
      {
          ID = BetaManagedAgentsModel.ClaudeOpus5,
          InferenceGeo = "us",
      },
      System = "You are a helpful assistant.",
  });

  Console.WriteLine($"Inference geo: {agent.Model.InferenceGeo}");
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Geo-pinned assistant",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID:           anthropic.BetaManagedAgentsModelClaudeOpus5,
  		InferenceGeo: anthropic.String("us"),
  	},
  	System: anthropic.String("You are a helpful assistant."),
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("Inference geo: %s\n", agent.Model.InferenceGeo)
  ```

  ```java Java
  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Geo-pinned assistant")
          .model(
              BetaManagedAgentsModelConfigParams.builder()
                  .id(BetaManagedAgentsModel.CLAUDE_OPUS_5)
                  .inferenceGeo("us")
                  .build()
          )
          .system("You are a helpful assistant.")
          .build()
  );

  IO.println("Inference geo: " + agent.model().inferenceGeo().orElseThrow());
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'Geo-pinned assistant',
      model: BetaManagedAgentsModelConfigParams::with(
          id: 'claude-opus-5',
          inferenceGeo: 'us',
      ),
      system: 'You are a helpful assistant.',
  );

  echo "Inference geo: {$agent->model->inferenceGeo}\n";
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Geo-pinned assistant",
    model: {id: "claude-opus-5", inference_geo: "us"},
    system_: "You are a helpful assistant."
  )

  puts "Inference geo: #{agent.model.inference_geo}"
  ```
</CodeGroup>

An `inference_geo` pin is validated against the workspace's [`allowed_inference_geos`](https://platform.claude.com/docs/en/manage-claude/data-residency#workspace-level-restrictions) when the agent is saved, when a session is created from it, and on every turn the session serves. If the workspace allowlist narrows so a pin is no longer allowed, new sessions can't be created from the agent and running sessions refuse further turns; pins are never exempted, because workspaces rely on them for compliance and data residency.

Setting `inference_geo` on a model that doesn't support geographic inference pinning returns a 400 error; see [Model availability](https://platform.claude.com/docs/en/manage-claude/data-residency#model-availability) for the models that do. In a `multiagent` configuration, the coordinator's pin and every roster member's must all be set to the same value or all be unset; see [Multiagent orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration). To change or clear the pin later, update the agent's `model` object; supplying `model` without `inference_geo` clears it, as described under [Update semantics](https://platform.claude.com/docs/en/managed-agents/agent-setup#update-semantics).

## Update an agent

Updating an agent generates a new version when the configuration changes. The `version` field is optional: supply it for optimistic concurrency (a mismatch returns a 409), or omit it to apply the update unconditionally (last write wins). Updates to archived agents are rejected.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  updated_agent=$(curl -fsSL "https://api.anthropic.com/v1/agents/$AGENT_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "version": $AGENT_VERSION,
    "system": "You are a helpful coding agent. Always write tests."
  }
  EOF
  )

  echo "New version: $(jq -r '.version' <<< "$updated_agent")"
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    ant beta:agents update --agent-id "$AGENT_ID" < coding-assistant.agent.yaml
    ```

    <File filename="coding-assistant.agent.yaml">
      ```yaml
      name: Coding Assistant
      model:
        id: claude-opus-5
      system: You are a helpful coding agent. Always write tests.
      tools:
        - type: agent_toolset_20260401
      ```
    </File>
  </MultiFileExample>

  ```python Python
  updated_agent = client.beta.agents.update(
      agent.id,
      version=agent.version,
      system="You are a helpful coding agent. Always write tests.",
  )

  print(f"New version: {updated_agent.version}")
  ```

  ```typescript TypeScript
  const updatedAgent = await client.beta.agents.update(agent.id, {
    version: agent.version,
    system: "You are a helpful coding agent. Always write tests.",
  });

  console.log(`New version: ${updatedAgent.version}`);
  ```

  ```csharp C#
  var updatedAgent = await client.Beta.Agents.Update(agent.ID, new()
  {
      Version = agent.Version,
      System = "You are a helpful coding agent. Always write tests.",
  });

  Console.WriteLine($"New version: {updatedAgent.Version}");
  ```

  ```go Go
  updatedAgent, err := client.Beta.Agents.Update(ctx, agent.ID, anthropic.BetaAgentUpdateParams{
  	Version: anthropic.Int(agent.Version),
  	System:  anthropic.String("You are a helpful coding agent. Always write tests."),
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("New version: %d\n", updatedAgent.Version)
  ```

  ```java Java
  var updatedAgent = client.beta().agents().update(
      agent.id(),
      AgentUpdateParams.builder()
          .version(agent.version())
          .system("You are a helpful coding agent. Always write tests.")
          .build()
  );

  IO.println("New version: " + updatedAgent.version());
  ```

  ```php PHP
  $updatedAgent = $client->beta->agents->update(
      $agent->id,
      version: $agent->version,
      system: 'You are a helpful coding agent. Always write tests.',
  );

  echo "New version: {$updatedAgent->version}\n";
  ```

  ```ruby Ruby
  updated_agent = client.beta.agents.update(
    agent.id,
    version: agent.version,
    system_: "You are a helpful coding agent. Always write tests."
  )

  puts "New version: #{updated_agent.version}"
  ```
</CodeGroup>

The preceding example supplies `version` from the create response, so the update only applies if nothing else has changed the agent since you read it. To apply an update unconditionally, omit `version` from the request:

<CodeGroup defaultLanguage="cURL">
  ```bash cURL
  updated_agent=$(curl -fsSL "https://api.anthropic.com/v1/agents/$AGENT_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{
      "description": "Writes and reviews code."
    }')

  echo "New version: $(jq -r '.version' <<< "$updated_agent")"
  ```
</CodeGroup>

### Update semantics

* **`version`** is optional and must be at least 1 when supplied. When supplied, the request returns a 409 if it doesn't match the agent's current version, even when the fields you send already match the stored values; re-read the agent and retry. When omitted, the update applies unconditionally and the most recent update silently replaces any concurrent one, with no error to either caller. Supplying `version` is the recommended default for interactive callers, and omitting it fits declarative apply loops, such as a CI job that syncs checked-in agent definitions, where the loop owns the agent.

* **Omitted fields are preserved.** You only need to include the fields you want to change.

* **Scalar fields** (`model`, `system`, `name`, `description`) are replaced with the new value. `system` and `description` can be cleared by passing `null`. `model` and `name` are mandatory and cannot be cleared. Within a `model` object you supply, `effort` is the sole exception: if the model `id` is unchanged, omitting `effort` leaves the stored effort level unchanged. If you change the model `id`, an omitted `effort` resets to the new model's default. Other `model` fields are replaced along with the object: supplying `model` without `inference_geo` clears the agent's inference geo pin.

* **Array fields** (`tools`, `mcp_servers`, `skills`) are fully replaced by the new array. To clear an array field entirely, pass `null` or an empty array.

* **`multiagent`** is replaced as a whole, including its `agents` roster. Pass `null` to clear it.

* **Metadata** is merged at the key level. Keys you provide are added or updated. Keys you omit are preserved. To delete a specific key, set its value to `null`.

* **No-op detection.** If the update produces no change relative to the current version, no new version is created and the existing version is returned.

* **Coordinator rosters are not updated.** Coordinators that reference this agent in their `multiagent.agents` roster keep the version that was pinned when the coordinator was created or last updated, even if the reference omits `version`. To delegate to the new version, [update the coordinator](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration#configure-the-coordinator) so its roster references it.

## Agent lifecycle

| Operation         | Behavior                                                                                            |
| ----------------- | --------------------------------------------------------------------------------------------------- |
| **Update**        | Generates a new agent version when the configuration changes.                                       |
| **List versions** | Returns the full version history so you can track changes over time.                                |
| **Archive**       | Makes the agent read-only. New sessions cannot reference it, but existing sessions continue to run. |

### List versions

Fetch the full version history to track how an agent has changed over time. Results are paginated, and the SDK examples fetch every page automatically.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -fsSL "https://api.anthropic.com/v1/agents/$AGENT_ID/versions" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    | jq -r '.data[] | "Version \(.version): \(.updated_at)"'
  ```

  ```bash CLI
  ant beta:agents:versions list --agent-id "$AGENT_ID"
  ```

  ```python Python
  for version in client.beta.agents.versions.list(agent.id):
      print(f"Version {version.version}: {version.updated_at.isoformat()}")
  ```

  ```typescript TypeScript
  for await (const version of client.beta.agents.versions.list(agent.id)) {
    console.log(`Version ${version.version}: ${version.updated_at}`);
  }
  ```

  ```csharp C#
  var versions = await client.Beta.Agents.Versions.List(agent.ID);
  await foreach (var version in versions.Paginate())
  {
      Console.WriteLine($"Version {version.Version}: {version.UpdatedAt:O}");
  }
  ```

  ```go Go
  iter := client.Beta.Agents.Versions.ListAutoPaging(ctx, agent.ID, anthropic.BetaAgentVersionListParams{})
  for iter.Next() {
  	version := iter.Current()
  	fmt.Printf("Version %d: %s\n", version.Version, version.UpdatedAt.Format(time.RFC3339))
  }
  if err := iter.Err(); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  for (var version : client.beta().agents().versions().list(agent.id()).autoPager()) {
      IO.println("Version " + version.version() + ": " + version.updatedAt());
  }
  ```

  ```php PHP
  foreach ($client->beta->agents->versions->list($agent->id)->pagingEachItem() as $version) {
      echo "Version {$version->version}: {$version->updatedAt->format(DateTimeInterface::ATOM)}\n";
  }
  ```

  ```ruby Ruby
  client.beta.agents.versions.list(agent.id).auto_paging_each do |agent_version|
    puts "Version #{agent_version.version}: #{agent_version.updated_at.iso8601}"
  end
  ```
</CodeGroup>

### Archive an agent

Archiving makes the agent read-only and cannot be undone. Existing sessions continue to run, but new sessions cannot reference the agent. The response sets `archived_at` to the archive timestamp.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  archived=$(curl -fsSL -X POST "https://api.anthropic.com/v1/agents/$AGENT_ID/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")

  echo "Archived at: $(jq -r '.archived_at' <<< "$archived")"
  ```

  ```bash CLI
  ant beta:agents archive --agent-id "$AGENT_ID"
  ```

  ```python Python
  archived = client.beta.agents.archive(agent.id)

  print(f"Archived at: {archived.archived_at.isoformat()}")
  ```

  ```typescript TypeScript
  const archived = await client.beta.agents.archive(agent.id);
  console.log(`Archived at: ${archived.archived_at}`);
  ```

  ```csharp C#
  var archived = await client.Beta.Agents.Archive(agent.ID);
  Console.WriteLine($"Archived at: {archived.ArchivedAt:O}");
  ```

  ```go Go
  archived, err := client.Beta.Agents.Archive(ctx, agent.ID, anthropic.BetaAgentArchiveParams{})
  if err != nil {
  	panic(err)
  }
  fmt.Printf("Archived at: %s\n", archived.ArchivedAt.Format(time.RFC3339))
  ```

  ```java Java
  var archived = client.beta().agents().archive(agent.id());
  IO.println("Archived at: " + archived.archivedAt().orElseThrow());
  ```

  ```php PHP
  $archived = $client->beta->agents->archive($agent->id);

  echo "Archived at: {$archived->archivedAt->format(DateTimeInterface::ATOM)}\n";
  ```

  ```ruby Ruby
  archived = client.beta.agents.archive(agent.id)
  puts "Archived at: #{archived.archived_at.iso8601}"
  ```
</CodeGroup>

## Next steps

<CardGroup cols={2}>
  <Card title="Tools" icon="tool" href="https://platform.claude.com/docs/en/managed-agents/tools">
    Configure tools available to your agent.
  </Card>

  <Card title="Skills" icon="graduation-cap" href="https://platform.claude.com/docs/en/managed-agents/skills">
    Attach reusable, filesystem-based expertise to your agent for domain-specific workflows.
  </Card>

  <Card title="Start a session" icon="play" href="https://platform.claude.com/docs/en/managed-agents/sessions">
    Create a session to run your agent and begin executing tasks.
  </Card>

  <Card title="Reference" icon="book" href="https://platform.claude.com/docs/en/managed-agents/reference">
    Event types, self-hosted worker CLI flags, supported MCP server types, rate limits, and branding guidelines for Claude Managed Agents.
  </Card>
</CardGroup>
