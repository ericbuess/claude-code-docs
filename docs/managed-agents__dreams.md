# Dreams

Let Claude reflect on past sessions to curate an agent's memory and surface new insights.

---

<Tip>
  Dreaming is a research preview feature. [Request access](https://claude.com/form/claude-managed-agents) to try it.
</Tip>

Agents write to their [memory stores](/docs/en/managed-agents/memory) as they work, but these writes are local and incremental: over many sessions a memory store accumulates duplicates, contradictions, and stale entries.

**Dreams** let Claude clean that up. A dream reads an existing memory store alongside past session transcripts, then produces a new, reorganized memory store: duplicates merged, stale or contradicted entries replaced with the latest value, and new insights surfaced.

The input store is never modified, so you can review the output and discard it if you don't like the result.

<Note>
  All Managed Agents API requests require the `managed-agents-2026-04-01` beta header. Dreams additionally require the `dreaming-2026-04-21` beta header. The SDK sets these automatically.
</Note>

## How it works

A **dream** is an asynchronous job that takes:

* a pre-existing **memory store**: the store Claude verifies, deduplicates, and reorganizes, and
* 1 to 100 **sessions**: past transcripts Claude mines for patterns and insights to fold into the output.

The dream produces another **output memory store**, separate from the input. The output store ID appears in the dream's `outputs[]` once it starts `running`.

## Create a dream

<CodeGroup>
  ```bash curl
  dream=$(curl -s https://api.anthropic.com/v1/dreams \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01,dreaming-2026-04-21" \
    -H "content-type: application/json" \
    --data @- <<EOF
  {
    "inputs": [
      { "type": "memory_store", "memory_store_id": "$store_id" },
      { "type": "sessions", "session_ids": ["$session_a", "$session_b"] }
    ],
    "model": "claude-opus-4-8",
    "instructions": "Focus on coding-style preferences; ignore one-off debugging notes."
  }
  EOF
  )
  dream_id=$(jq -r '.id' <<< "$dream")
  echo "$dream_id"  # drm_01...
  ```

  ```bash CLI
  dream_id=$(ant beta:dreams create --transform id --raw-output <<YAML
  inputs:
    - type: memory_store
      memory_store_id: $store_id
    - type: sessions
      session_ids: [$session_a, $session_b]
  model: claude-opus-4-8
  instructions: Focus on coding-style preferences; ignore one-off debugging notes.
  YAML
  )
  ```

  ```python Python
  dream = client.beta.dreams.create(
      inputs=[
          {"type": "memory_store", "memory_store_id": store_id},
          {"type": "sessions", "session_ids": [session_a, session_b]},
      ],
      model="claude-opus-4-8",
      instructions="Focus on coding-style preferences; ignore one-off debugging notes.",
  )
  print(dream.id)  # drm_01...
  ```

  ```typescript TypeScript
  let dream = await client.beta.dreams.create({
    inputs: [
      { type: "memory_store", memory_store_id: storeId },
      { type: "sessions", session_ids: [sessionA, sessionB] },
    ],
    model: "claude-opus-4-8",
    instructions: "Focus on coding-style preferences; ignore one-off debugging notes.",
  });
  console.log(dream.id); // drm_01...
  ```

  ```csharp C#
  var dream = await client.Beta.Dreams.Create(new()
  {
      Inputs =
      [
          new BetaDreamMemoryStoreInput
          {
              Type = BetaDreamMemoryStoreInputType.MemoryStore,
              MemoryStoreID = storeID,
          },
          new BetaDreamSessionsInput
          {
              Type = BetaDreamSessionsInputType.Sessions,
              SessionIds = [sessionA, sessionB],
          },
      ],
      Model = "claude-opus-4-8",
      Instructions = "Focus on coding-style preferences; ignore one-off debugging notes.",
  });
  Console.WriteLine(dream.ID);  // drm_01...
  ```

  ```go Go
  dream, err := client.Beta.Dreams.New(ctx, anthropic.BetaDreamNewParams{
  	Inputs: []anthropic.BetaDreamInputUnionParam{
  		anthropic.BetaDreamInputParamOfMemoryStore(storeID),
  		anthropic.BetaDreamInputParamOfSessions([]string{sessionA, sessionB}),
  	},
  	Model: anthropic.BetaDreamModelParamsUnion{
  		OfString: anthropic.String("claude-opus-4-8"),
  	},
  	Instructions: anthropic.String("Focus on coding-style preferences; ignore one-off debugging notes."),
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(dream.ID) // drm_01...
  ```

  ```java Java
  var dream = client.beta().dreams().create(
      DreamCreateParams.builder()
          .addMemoryStoreInput(storeId)
          .addSessionsInput(List.of(sessionA, sessionB))
          .model("claude-opus-4-8")
          .instructions("Focus on coding-style preferences; ignore one-off debugging notes.")
          .build()
  );
  IO.println(dream.id());  // drm_01...
  ```

  ```php PHP
  $dream = $client->beta->dreams->create(
      inputs: [
          ['type' => 'memory_store', 'memory_store_id' => $storeId],
          ['type' => 'sessions', 'session_ids' => [$sessionA, $sessionB]],
      ],
      model: 'claude-opus-4-8',
      instructions: 'Focus on coding-style preferences; ignore one-off debugging notes.',
  );
  echo "{$dream->id}\n"; // drm_01...
  ```

  ```ruby Ruby
  dream = client.beta.dreams.create(
    inputs: [
      {type: "memory_store", memory_store_id: store_id},
      {type: "sessions", session_ids: [session_a, session_b]}
    ],
    model: "claude-opus-4-8",
    instructions: "Focus on coding-style preferences; ignore one-off debugging notes."
  )
  puts dream.id # drm_01...
  ```
</CodeGroup>

Dreaming inputs include the pre-existing memory store and an array of sessions. The model selected will run the dreaming pipeline; during the research preview `claude-opus-4-8`, `claude-opus-4-7`, and `claude-sonnet-4-6` are supported. You can optionally pass `instructions` to steer the dreaming process; see [Steer with instructions](#steer-with-instructions).

The response is the full `dream` resource with `status: "pending"`:

```json
{
  "type": "dream",
  "id": "drm_01AbCDefGhIjKlMnOpQrStUv",
  "status": "pending",
  "inputs": [
    { "type": "memory_store", "memory_store_id": "memstore_01Hx..." },
    { "type": "sessions", "session_ids": ["sesn_01...", "sesn_02..."] }
  ],
  "outputs": [],
  "model": { "id": "claude-opus-4-8" },
  "instructions": "Focus on coding-style preferences; ignore one-off debugging notes.",
  "session_id": null,
  "created_at": "2026-04-29T17:04:10Z",
  "ended_at": null,
  "archived_at": null,
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0
  },
  "error": null
}
```

<Tip>
  If you only have session transcripts and no existing store, [create an empty memory store](/docs/en/managed-agents/memory#create-a-memory-store) first and pass it as the `memory_store` input.
</Tip>

### Steer with instructions

The optional `instructions` field steers what the dreaming pipeline synthesizes. It is applied throughout the pipeline: what to read closely, what to merge or drop, and how to structure the output store.

Use `instructions` for high-level synthesis guidance such as focus areas ("focus on coding-style preferences"), content to preserve unchanged, or output conventions you want applied across the store. The pipeline is a synthesis pass over the inputs, not an editor applied to the text of the store, so imperative directives that target specific lines ("change sentence X to Y", "fix the count in section Z") generally produce no change. To make targeted edits to individual memories, use the [Memory Stores API](/docs/en/managed-agents/memory#view-and-edit-memories) on the output store directly.

## Track progress

Dreams run asynchronously and typically take minutes to tens of minutes depending on input size. Poll the dream by ID to check status:

<CodeGroup>
  ```bash curl
  while true; do
    dream=$(curl -s "https://api.anthropic.com/v1/dreams/$dream_id" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01,dreaming-2026-04-21")
    status=$(jq -r '.status' <<< "$dream")
    echo "status=$status input_tokens=$(jq -r '.usage.input_tokens' <<< "$dream")"
    [[ "$status" == "pending" || "$status" == "running" ]] || break
    sleep 10
  done
  ```

  ```bash CLI
  ant beta:dreams retrieve --dream-id "$dream_id"
  ```

  ```python Python
  while dream.status in ("pending", "running"):
      time.sleep(10)
      dream = client.beta.dreams.retrieve(dream.id)
      print(f"status={dream.status} input_tokens={dream.usage.input_tokens}")
  ```

  ```typescript TypeScript
  while (dream.status === "pending" || dream.status === "running") {
    await sleep(10_000);
    dream = await client.beta.dreams.retrieve(dream.id);
    console.log(`status=${dream.status} input_tokens=${dream.usage.input_tokens}`);
  }
  ```

  ```csharp C#
  while (dream.Status.Value() is BetaDreamStatus.Pending or BetaDreamStatus.Running)
  {
      await Task.Delay(TimeSpan.FromSeconds(10));
      dream = await client.Beta.Dreams.Retrieve(dream.ID);
      Console.WriteLine($"status={dream.Status.Raw()} input_tokens={dream.Usage.InputTokens}");
  }
  ```

  ```go Go
  for dream.Status == anthropic.BetaDreamStatusPending || dream.Status == anthropic.BetaDreamStatusRunning {
  	time.Sleep(10 * time.Second)
  	dream, err = client.Beta.Dreams.Get(ctx, dream.ID, anthropic.BetaDreamGetParams{})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Printf("status=%s input_tokens=%d\n", dream.Status, dream.Usage.InputTokens)
  }
  ```

  ```java Java
  while (dream.status().equals(BetaDreamStatus.PENDING)
          || dream.status().equals(BetaDreamStatus.RUNNING)) {
      Thread.sleep(10_000);
      dream = client.beta().dreams().retrieve(dream.id());
      IO.println("status=" + dream.status() + " input_tokens=" + dream.usage().inputTokens());
  }
  ```

  ```php PHP
  while (in_array($dream->status, [BetaDreamStatus::PENDING->value, BetaDreamStatus::RUNNING->value], true)) {
      sleep(10);
      $dream = $client->beta->dreams->retrieve($dream->id);
      echo "status={$dream->status} input_tokens={$dream->usage->inputTokens}\n";
  }
  ```

  ```ruby Ruby
  while %i[pending running].include?(dream.status)
    sleep 10
    dream = client.beta.dreams.retrieve(dream.id)
    puts "status=#{dream.status} input_tokens=#{dream.usage.input_tokens}"
  end
  ```
</CodeGroup>

### Lifecycle

| `status`    | Meaning                                                                                                                |
| ----------- | ---------------------------------------------------------------------------------------------------------------------- |
| `pending`   | Dream successfully created and queued.                                                                                 |
| `running`   | The pipeline is processing. `usage` updates as work progresses.                                                        |
| `completed` | Finished successfully. The `outputs[]` value is the new memory store.                                                  |
| `failed`    | Dreaming run terminated with an error. The output memory store is left as-is with whatever was written before failure. |
| `canceled`  | Dreaming run canceled. The output memory store is left as-is.                                                          |

### Watch the pipeline run

Once a dream is `running`, its `session_id` field points at the underlying [session](/docs/en/managed-agents/sessions) executing the pipeline. You can stream that session's [events](/docs/en/managed-agents/events-and-streaming) to observe what the dream is reading and writing in real time. The session is archived (not deleted) when the dream reaches a terminal state, so the transcript remains available afterward.

## Use the output

When `status` reaches `completed`, the `memory_store` entry in `outputs[]` references a fully populated store. It's an ordinary memory store in your workspace. Review it with the [Memory Stores API](/docs/en/managed-agents/memory#view-and-edit-memories) or in the Console, then either:

* **Leverage it:** attach it to future sessions as a `memory_store` resource in place of (or alongside) the input memory store, or
* **Discard it:** [delete](/docs/en/api/beta/memory_stores/delete) or [archive](/docs/en/api/beta/memory_stores/archive) it.

<CodeGroup>
  ```bash curl
  # After the dream ends, the memory_store output holds the rebuilt store
  output_store_id=$(jq -r 'first(.outputs[] | select(.type == "memory_store")).memory_store_id' <<< "$dream")

  curl -s https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    --data @- <<EOF
  {
    "agent": "$agent_id",
    "environment_id": "$environment_id",
    "resources": [
      { "type": "memory_store", "memory_store_id": "$output_store_id" }
    ]
  }
  EOF
  ```

  ```bash CLI
  output_store_id=$(ant beta:dreams retrieve --dream-id "$dream_id" --format json |
    jq -r 'first(.outputs[] | select(.type == "memory_store")).memory_store_id')

  ant beta:sessions create <<YAML
  agent: $agent_id
  environment_id: $environment_id
  resources:
    - type: memory_store
      memory_store_id: $output_store_id
  YAML
  ```

  ```python Python
  # After the dream ends, the output holds the rebuilt memory store
  output_store_id = next(
      output.memory_store_id for output in dream.outputs if output.type == "memory_store"
  )

  session = client.beta.sessions.create(
      agent=agent_id,
      environment_id=environment_id,
      resources=[
          {"type": "memory_store", "memory_store_id": output_store_id},
      ],
  )
  ```

  ```typescript TypeScript
  // After the dream ends, the output holds the rebuilt memory store
  const output = dream.outputs.find((entry) => entry.type === "memory_store");
  const outputStoreId = output!.memory_store_id;

  await client.beta.sessions.create({
    agent: agentId,
    environment_id: environmentId,
    resources: [
      { type: "memory_store", memory_store_id: outputStoreId },
    ],
  });
  ```

  ```csharp C#
  var output = dream.Outputs.FirstOrDefault(entry => entry.Type == "memory_store");
  if (output is { MemoryStoreID: var outputStoreID })
  {
      await client.Beta.Sessions.Create(new()
      {
          Agent = agentID,
          EnvironmentID = environmentID,
          Resources =
          [
              new BetaManagedAgentsMemoryStoreResourceParam
              {
                  Type = BetaManagedAgentsMemoryStoreResourceParamType.MemoryStore,
                  MemoryStoreID = outputStoreID,
              },
          ],
      });
  }
  ```

  ```go Go
  for _, output := range dream.Outputs {
  	if output.Type != "memory_store" {
  		continue
  	}
  	outputStoreID := output.MemoryStoreID

  	session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  		Agent: anthropic.BetaSessionNewParamsAgentUnion{
  			OfString: anthropic.String(agentID),
  		},
  		EnvironmentID: environmentID,
  		Resources: []anthropic.BetaSessionNewParamsResourceUnion{{
  			OfMemoryStore: &anthropic.BetaManagedAgentsMemoryStoreResourceParam{
  				MemoryStoreID: outputStoreID,
  			},
  		}},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(session.ID)
  	break
  }
  ```

  ```java Java
  var output = dream.outputs().stream()
      .filter(entry -> entry.type().equals(BetaDreamOutput.Type.MEMORY_STORE))
      .findFirst();
  if (output.isPresent()) {
      var outputStoreId = output.get().memoryStoreId();

      var session = client.beta().sessions().create(
          SessionCreateParams.builder()
              .agent(agentId)
              .environmentId(environmentId)
              .addMemoryStoreResource(outputStoreId)
              .build()
      );
  }
  ```

  ```php PHP
  $matches = array_filter($dream->outputs, fn($output) => $output->type === 'memory_store');
  $output = $matches ? reset($matches) : null;
  if ($output !== null) {
      $session = $client->beta->sessions->create(
          agent: $agentId,
          environmentID: $environmentId,
          resources: [
              ['type' => 'memory_store', 'memory_store_id' => $output->memoryStoreID],
          ],
      );
  }
  ```

  ```ruby Ruby
  output = dream.outputs.find { it.type == :memory_store }
  if output
    client.beta.sessions.create(
      agent: agent_id,
      environment_id: environment_id,
      resources: [
        {type: "memory_store", memory_store_id: output.memory_store_id}
      ]
    )
  end
  ```
</CodeGroup>

The dream itself never deletes or modifies its inputs. On `failed` or `canceled` the output store persists with partial contents so you can inspect what was produced before stopping; clean it up via the Memory Stores API if you don't need it.

<Warning>
  While a dream is `pending` or `running`, archiving or deleting its output store is rejected with a 400. Archiving or deleting an *input* store or session mid-run will cause the dream to fail with `input_memory_store_unavailable` or `input_session_unavailable`.
</Warning>

## Cancel a dream

Cancel moves a `pending` or `running` dream to `canceled` immediately. Canceling an already-`canceled` dream is an idempotent no-op; canceling a `completed` or `failed` dream returns 400.

<Note>
  After cancellation, the dream's `usage` fields might continue to update for a few seconds while in-flight work winds down. Poll the dream until `usage` stabilizes if you need the final count.
</Note>

<CodeGroup>
  ```bash curl
  curl -s -X POST "https://api.anthropic.com/v1/dreams/$dream_id/cancel" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01,dreaming-2026-04-21"
  ```

  ```bash CLI
  ant beta:dreams cancel --dream-id "$dream_id"
  ```

  ```python Python
  client.beta.dreams.cancel(dream.id)
  ```

  ```typescript TypeScript
  await client.beta.dreams.cancel(dream.id);
  ```

  ```csharp C#
  await client.Beta.Dreams.Cancel(dream.ID);
  ```

  ```go Go
  dream, err = client.Beta.Dreams.Cancel(ctx, dream.ID, anthropic.BetaDreamCancelParams{})
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().dreams().cancel(dream.id());
  ```

  ```php PHP
  $client->beta->dreams->cancel($dream->id);
  ```

  ```ruby Ruby
  client.beta.dreams.cancel(dream.id)
  ```
</CodeGroup>

## Archive a dream

Archive sets `archived_at` on a dream that has reached a terminal state (`completed`, `failed`, or `canceled`); `status` is left unchanged. Archived dreams are excluded from default list responses but remain readable by ID. Archiving an already-archived dream is an idempotent no-op. Archiving a `pending` or `running` dream returns 400; cancel it first. There is no unarchive.

<CodeGroup>
  ```bash curl
  curl -s -X POST "https://api.anthropic.com/v1/dreams/$dream_id/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01,dreaming-2026-04-21"
  ```

  ```bash CLI
  ant beta:dreams archive --dream-id "$dream_id"
  ```

  ```python Python
  client.beta.dreams.archive(dream.id)
  ```

  ```typescript TypeScript
  await client.beta.dreams.archive(dream.id);
  ```

  ```csharp C#
  await client.Beta.Dreams.Archive(dream.ID);
  ```

  ```go Go
  dream, err = client.Beta.Dreams.Archive(ctx, dream.ID, anthropic.BetaDreamArchiveParams{})
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().dreams().archive(dream.id());
  ```

  ```php PHP
  $client->beta->dreams->archive($dream->id);
  ```

  ```ruby Ruby
  client.beta.dreams.archive(dream.id)
  ```
</CodeGroup>

Archiving a dream does not touch its output memory store; manage that separately via the [Memory Stores API](/docs/en/managed-agents/memory).

## List dreams

Returns all non-archived dreams in the workspace, newest first. Use `limit` (default 20, max 100) and the `page` cursor to paginate. Pass `include_archived=true` to include archived dreams.

<CodeGroup>
  ```bash curl
  curl -s "https://api.anthropic.com/v1/dreams?limit=20" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01,dreaming-2026-04-21"
  ```

  ```bash CLI
  ant beta:dreams list --limit 20
  ```

  ```python Python
  for listed_dream in client.beta.dreams.list(limit=20):
      print(listed_dream.id, listed_dream.status)
  ```

  ```typescript TypeScript
  for await (const listedDream of client.beta.dreams.list({ limit: 20 })) {
    console.log(listedDream.id, listedDream.status);
  }
  ```

  ```csharp C#
  var page = await client.Beta.Dreams.List(new() { Limit = 20 });
  await foreach (var listed in page.Paginate())
  {
      Console.WriteLine($"{listed.ID} {listed.Status.Raw()}");
  }
  ```

  ```go Go
  dreams := client.Beta.Dreams.ListAutoPaging(ctx, anthropic.BetaDreamListParams{
  	Limit: anthropic.Int(20),
  })
  for dreams.Next() {
  	listed := dreams.Current()
  	fmt.Println(listed.ID, listed.Status)
  }
  if err := dreams.Err(); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  for (var listedDream : client.beta().dreams().list(
      DreamListParams.builder().limit(20).build()
  ).autoPager()) {
      IO.println(listedDream.id() + " " + listedDream.status());
  }
  ```

  ```php PHP
  foreach ($client->beta->dreams->list(limit: 20)->pagingEachItem() as $dream) {
      echo "{$dream->id} {$dream->status}\n";
  }
  ```

  ```ruby Ruby
  client.beta.dreams.list(limit: 20).auto_paging_each do
    puts "#{it.id} #{it.status}"
  end
  ```
</CodeGroup>

## Errors

A non-exhaustive list of possible dreaming errors is below.

| `error.type`                      | When                                                                                            |
| --------------------------------- | ----------------------------------------------------------------------------------------------- |
| `timeout`                         | The pipeline exceeded its runtime budget.                                                       |
| `internal_error`                  | Unclassified pipeline failure.                                                                  |
| `memory_store_org_limit_exceeded` | Your organization hit its memory-store cap while the pipeline was provisioning working storage. |
| `input_memory_store_too_large`    | The input memory store exceeds the pipeline's size limit.                                       |
| `input_memory_store_unavailable`  | The input memory store was archived or deleted after the dream was created.                     |
| `input_session_unavailable`       | An input session was archived or deleted after the dream was created.                           |

## Billing

Dreams are billed at standard API token rates for the model you select; `usage` on the resource reports the exact totals. Cost scales roughly linearly with the number and length of input sessions. Start with a small batch of sessions and scale up once you're satisfied with the curation quality.

## Limits

| Limit                 | Value                                                     |
| --------------------- | --------------------------------------------------------- |
| Sessions per dream    | 100                                                       |
| `instructions` length | 4,096 characters                                          |
| Supported models      | `claude-opus-4-8`, `claude-opus-4-7`, `claude-sonnet-4-6` |

Default rate limits apply to dream creation while this feature is in beta. [Contact support](https://support.claude.com) if you need higher limits.
