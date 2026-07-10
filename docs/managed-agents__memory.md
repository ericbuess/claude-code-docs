# Using agent memory

Give your agents persistent memory that survives across sessions using memory stores.

---

Each Managed Agents session starts with a fresh context by default. When a session ends, any state the agent built up is gone. Memory stores let the agent carry information across sessions: user preferences, project conventions, prior mistakes, and domain context.

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

<Note>
  Don't combine `agent-memory-2026-07-22` with `managed-agents-2026-04-01` on a memory store request: sending both returns a `400` error. If your code sets beta headers explicitly, replace `managed-agents-2026-04-01` with `agent-memory-2026-07-22` on memory store calls rather than adding a second value. Session endpoints, including attaching a memory store to a session, still use `managed-agents-2026-04-01`.

  On July 22, 2026, the `managed-agents-2026-04-01` header adopts the same list behavior on `GET /v1/memory_stores/{memory_store_id}/memories`; sending `agent-memory-2026-07-22` opts you into that behavior now. Page cursors from requests made without the header aren't valid with it, so restart from the first page.
</Note>

## Overview

A **memory store** is a workspace-scoped collection of text documents optimized for Claude. When you attach a store to a session, it is mounted as a directory inside the session's sandbox. The agent reads and writes it with the same file tools it uses for the rest of the filesystem, and a note describing each mount is automatically added to the system prompt, telling the agent where to look. The [agent toolset](/docs/en/managed-agents/tools) is required for these interactions; make sure to enable it during [agent creation](/docs/en/managed-agents/agent-setup).

Each **memory** in a store is addressed by a path and can be read and edited directly through the API or Console, allowing for tuning, importing, and exporting.

Every change to a memory creates an immutable **memory version**, giving you an audit trail and point-in-time recovery for everything the agent writes.

## Create a memory store

Give the store a `name` and a `description`. The description is passed to the agent, telling it what the store contains.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  store=$(curl -s https://api.anthropic.com/v1/memory_stores \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" \
    -H "content-type: application/json" \
    -d '{"name": "User Preferences", "description": "Per-user preferences and project context."}')
  store_id=$(jq -r '.id' <<< "$store")
  echo "$store_id"  # memstore_01Hx...
  ```

  ```bash CLI
  store_id=$(ant beta:memory-stores create \
    --name "User Preferences" \
    --description "Per-user preferences and project context." \
    --transform id --raw-output)
  ```

  ```python Python
  store = client.beta.memory_stores.create(
      name="User Preferences",
      description="Per-user preferences and project context.",
  )
  print(store.id)  # memstore_01Hx...
  ```

  ```typescript TypeScript
  const store = await client.beta.memoryStores.create({
    name: "User Preferences",
    description: "Per-user preferences and project context."
  });
  console.log(store.id); // memstore_01Hx...
  ```

  ```csharp C#
  var store = await client.Beta.MemoryStores.Create(new()
  {
      Name = "User Preferences",
      Description = "Per-user preferences and project context.",
  });
  Console.WriteLine(store.ID);  // memstore_01Hx...
  ```

  ```go Go
  store, err := client.Beta.MemoryStores.New(ctx, anthropic.BetaMemoryStoreNewParams{
  	Name:        "User Preferences",
  	Description: anthropic.String("Per-user preferences and project context."),
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(store.ID) // memstore_01Hx...
  ```

  ```java Java
  var store = client.beta().memoryStores().create(
      MemoryStoreCreateParams.builder()
          .name("User Preferences")
          .description("Per-user preferences and project context.")
          .build()
  );
  IO.println(store.id());  // memstore_01Hx...
  ```

  ```php PHP
  use Anthropic\Client;

  $client = new Client();

  $store = $client->beta->memoryStores->create(
      name: 'User Preferences',
      description: 'Per-user preferences and project context.',
  );
  echo "{$store->id}\n"; // memstore_01Hx...
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  store = client.beta.memory_stores.create(
    name: "User Preferences",
    description: "Per-user preferences and project context."
  )
  puts store.id # memstore_01Hx...
  ```
</CodeGroup>

The memory store `id` (`memstore_...`) is what you pass when attaching the store to a session.

### Seed it with content (optional)

Pre-load a store with reference material before any agent runs:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s "https://api.anthropic.com/v1/memory_stores/$store_id/memories" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" \
    -H "content-type: application/json" \
    -d '{"path": "/formatting_standards.md", "content": "All reports use GAAP formatting. Dates are ISO-8601..."}' > /dev/null
  ```

  ```bash CLI
  ant beta:memory-stores:memories create \
    --memory-store-id "$store_id" \
    --path "/formatting_standards.md" \
    --content "All reports use GAAP formatting. Dates are ISO-8601..." \
    > /dev/null
  ```

  ```python Python
  client.beta.memory_stores.memories.create(
      store.id,
      path="/formatting_standards.md",
      content="All reports use GAAP formatting. Dates are ISO-8601...",
  )
  ```

  ```typescript TypeScript
  await client.beta.memoryStores.memories.create(store.id, {
    path: "/formatting_standards.md",
    content: "All reports use GAAP formatting. Dates are ISO-8601..."
  });
  ```

  ```csharp C#
  await client.Beta.MemoryStores.Memories.Create(store.ID, new()
  {
      Path = "/formatting_standards.md",
      Content = "All reports use GAAP formatting. Dates are ISO-8601...",
  });
  ```

  ```go Go
  _, err = client.Beta.MemoryStores.Memories.New(ctx, store.ID, anthropic.BetaMemoryStoreMemoryNewParams{
  	Path:    "/formatting_standards.md",
  	Content: anthropic.String("All reports use GAAP formatting. Dates are ISO-8601..."),
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().memoryStores().memories().create(
      store.id(),
      MemoryCreateParams.builder()
          .path("/formatting_standards.md")
          .content("All reports use GAAP formatting. Dates are ISO-8601...")
          .build()
  );
  ```

  ```php PHP
  $client->beta->memoryStores->memories->create(
      $store->id,
      path: '/formatting_standards.md',
      content: 'All reports use GAAP formatting. Dates are ISO-8601...',
  );
  ```

  ```ruby Ruby
  client.beta.memory_stores.memories.create(
    store.id,
    path: "/formatting_standards.md",
    content: "All reports use GAAP formatting. Dates are ISO-8601..."
  )
  ```
</CodeGroup>

<Tip>
  Individual memories within the store are capped at 100 kB (\~25k tokens). A store holds a maximum of 2,000 memories. Structure memory as many small focused files, not a few large ones.
</Tip>

## Attach a memory store to a session

Memory stores are attached in the session's `resources[]` array when the session is created. Unlike file and repository resources, memory stores can only be attached at session creation time; adding or removing one from a running session is not supported.

Optionally include `instructions` to provide session-specific guidance for how the agent should use this store. It is shown to the agent alongside the store's `name` and `description`, and is capped at 4,096 characters.

You can configure `access` as well. It defaults to `read_write` (shown explicitly in the following example), but `read_only` is also supported.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
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
      {
        "type": "memory_store",
        "memory_store_id": "$store_id",
        "access": "read_write",
        "instructions": "User preferences and project context. Check before starting any task."
      }
    ]
  }
  EOF
  ```

  ```bash CLI
  ant beta:sessions create <<YAML
  agent: $agent_id
  environment_id: $environment_id
  resources:
    - type: memory_store
      memory_store_id: $store_id
      access: read_write
      instructions: User preferences and project context. Check before starting any task.
  YAML
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      resources=[
          {
              "type": "memory_store",
              "memory_store_id": store.id,
              "access": "read_write",
              "instructions": "User preferences and project context. Check before starting any task.",
          }
      ],
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    resources: [
      {
        type: "memory_store",
        memory_store_id: store.id,
        access: "read_write",
        instructions: "User preferences and project context. Check before starting any task."
      }
    ]
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      Resources =
      [
          new BetaManagedAgentsMemoryStoreResourceParam
          {
              Type = "memory_store",
              MemoryStoreID = store.ID,
              Access = "read_write",
              Instructions = "User preferences and project context. Check before starting any task.",
          },
      ],
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  	Resources: []anthropic.BetaSessionNewParamsResourceUnion{{
  		OfMemoryStore: &anthropic.BetaManagedAgentsMemoryStoreResourceParam{
  			Type:          anthropic.BetaManagedAgentsMemoryStoreResourceParamTypeMemoryStore,
  			MemoryStoreID: store.ID,
  			Access:        anthropic.BetaManagedAgentsMemoryStoreResourceParamAccessReadWrite,
  			Instructions:  anthropic.String("User preferences and project context. Check before starting any task."),
  		},
  	}},
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
          .addResource(
              BetaManagedAgentsMemoryStoreResourceParam.builder()
                  .type(BetaManagedAgentsMemoryStoreResourceParam.Type.MEMORY_STORE)
                  .memoryStoreId(store.id())
                  .access(BetaManagedAgentsMemoryStoreResourceParam.Access.READ_WRITE)
                  .instructions("User preferences and project context. Check before starting any task.")
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      resources: [
          [
              'type' => 'memory_store',
              'memory_store_id' => $store->id,
              'access' => 'read_write',
              'instructions' => 'User preferences and project context. Check before starting any task.',
          ],
      ],
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    resources: [
      {
        type: "memory_store",
        memory_store_id: store.id,
        access: "read_write",
        instructions: "User preferences and project context. Check before starting any task."
      }
    ]
  )
  ```
</CodeGroup>

<Warning>
  Memory stores attach with `read_write` access by default. If the agent processes untrusted input (user-supplied prompts, fetched web content, or third-party tool output), a successful prompt injection could write malicious content into the store. Later sessions then read that content as trusted memory. Use `read_only` for reference material, shared lookups, and any store the agent does not need to modify.
</Warning>

A maximum of **8 memory stores** are supported per session. Attach multiple stores when different parts of memory have different owners or access rules. Common reasons:

* **Shared reference material:** one read-only store attached to many sessions (standards, conventions, domain knowledge), kept separate from each session's own read-write store.
* **Mapping to your product's structure:** one store per end user, per team, or per project, while sharing a single agent configuration.
* **Different lifecycles:** a store that outlives any single session, or one you want to archive on its own schedule.

### How the agent accesses memory

Each attached store is mounted inside the session's sandbox as a directory under `/mnt/memory/`. The directory name is the store's display name sanitized to a filesystem-safe slug (lowercased; non-alphanumeric runs become a single hyphen), so a store named "Demo Memory" mounts at `/mnt/memory/demo-memory/`. The exact path is returned in the `mount_path` field on the session's memory-store resource; read it from there rather than constructing it yourself. The agent reads and writes the store with the standard [agent toolset](/docs/en/managed-agents/tools). Writes under the mount path are persisted back to the store and stay in sync across sessions that share it; writes to any other path under `/mnt/memory/` land in container-local scratch and are lost when the session ends. A short description of each mount (display name, mount path, access mode, store `description`, and any `instructions`) is automatically added to the system prompt.

`access` is enforced at the filesystem level: a `read_only` mount rejects writes, while writes to a `read_write` mount produce [memory versions](#audit-memory-changes) attributed to the session.

The agent's reads and writes appear in the [event stream](/docs/en/managed-agents/events-and-streaming) as ordinary `agent.tool_use` and `agent.tool_result` events for whichever tool touched the mount.

## View and edit memories

Memory stores can be managed directly through the API. Use this for building review workflows, correcting bad memories, or seeding stores before any session runs.

### List memories

List the memories in a store. Results are returned in a stable, server-defined order.

* `path_prefix` scopes the list to one directory. It must end with `/` and matches whole path segments, so `path_prefix=/notes/` returns `/notes/todo.md` but not `/notes-archive/todo.md`.
* `depth` controls how deep the listing goes below `path_prefix`: omit it (or pass `0`) to list the whole subtree, or pass `1` to list only the immediate children. Other values return a `400` error.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s "https://api.anthropic.com/v1/memory_stores/$store_id/memories?path_prefix=/" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" | jq -r '.data[] | "\(.type)  \(.path)"'
  ```

  ```bash CLI
  ant beta:memory-stores:memories list \
    --memory-store-id "$store_id" \
    --path-prefix "/"
  ```

  ```python Python
  page = client.beta.memory_stores.memories.list(
      store.id,
      path_prefix="/",
  )
  for item in page.data:
      print(item.type, item.path)
  ```

  ```typescript TypeScript
  const page = await client.beta.memoryStores.memories.list(store.id, {
    path_prefix: "/"
  });
  for (const item of page.data) {
    console.log(item.type, item.path);
  }
  ```

  ```csharp C#
  var page = await client.Beta.MemoryStores.Memories.List(store.ID, new()
  {
      PathPrefix = "/",
  });
  await foreach (var item in page.Paginate())
  {
      var line = item.Match(m => $"memory  {m.Path}", p => $"memory_prefix  {p.Path}");
      Console.WriteLine(line);
  }
  ```

  ```go Go
  page, err := client.Beta.MemoryStores.Memories.List(ctx, store.ID, anthropic.BetaMemoryStoreMemoryListParams{
  	PathPrefix: anthropic.String("/"),
  })
  if err != nil {
  	panic(err)
  }
  for _, item := range page.Data {
  	fmt.Println(item.Type, item.Path)
  }
  ```

  ```java Java
  var page = client.beta().memoryStores().memories().list(
      store.id(),
      MemoryListParams.builder()
          .pathPrefix("/")
          .build()
  );
  for (var item : page.data()) {
      item.memory().ifPresent(m -> IO.println("memory  " + m.path()));
      item.memoryPrefix().ifPresent(p -> IO.println("memory_prefix  " + p.path()));
  }
  ```

  ```php PHP
  $page = $client->beta->memoryStores->memories->list(
      $store->id,
      pathPrefix: '/',
  );
  foreach ($page->data as $item) {
      echo "{$item->type}  {$item->path}\n";
  }
  ```

  ```ruby Ruby
  page = client.beta.memory_stores.memories.list(
    store.id,
    path_prefix: "/"
  )
  page.data.each do |entry|
    puts "#{entry.type}  #{entry.path}"
  end
  ```
</CodeGroup>

See the [List memories reference](/docs/en/api/beta/memory_stores/memories/list) for full parameters and response schema.

### Read a memory

Fetching an individual memory returns the full content.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" | jq -r '.content'
  ```

  ```bash CLI
  ant beta:memory-stores:memories retrieve \
    --memory-store-id "$store_id" \
    --memory-id "$mem_id"
  ```

  ```python Python
  retrieved = client.beta.memory_stores.memories.retrieve(
      mem.id,
      memory_store_id=store.id,
  )
  print(retrieved.content)
  ```

  ```typescript TypeScript
  const retrieved = await client.beta.memoryStores.memories.retrieve(mem.id, {
    memory_store_id: store.id
  });
  console.log(retrieved.content);
  ```

  ```csharp C#
  var retrieved = await client.Beta.MemoryStores.Memories.Retrieve(mem.ID, new()
  {
      MemoryStoreID = store.ID,
  });
  Console.WriteLine(retrieved.Content);
  ```

  ```go Go
  retrieved, err := client.Beta.MemoryStores.Memories.Get(ctx, mem.ID, anthropic.BetaMemoryStoreMemoryGetParams{
  	MemoryStoreID: store.ID,
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(retrieved.Content)
  ```

  ```java Java
  var retrieved = client.beta().memoryStores().memories().retrieve(
      mem.id(),
      MemoryRetrieveParams.builder().memoryStoreId(store.id()).build()
  );
  IO.println(retrieved.content());
  ```

  ```php PHP
  $retrieved = $client->beta->memoryStores->memories->retrieve($mem->id, memoryStoreID: $store->id);
  echo "{$retrieved->content}\n";
  ```

  ```ruby Ruby
  retrieved = client.beta.memory_stores.memories.retrieve(
    mem.id,
    memory_store_id: store.id
  )
  puts retrieved.content
  ```
</CodeGroup>

See the [Retrieve a memory reference](/docs/en/api/beta/memory_stores/memories/retrieve) for full parameters and response schema.

### Create a memory

`memories.create` creates a memory at a given `path`. Create does not overwrite; to change an existing memory, use [`memories.update`](#update-a-memory).

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  mem=$(curl -s "https://api.anthropic.com/v1/memory_stores/$store_id/memories" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" \
    -H "content-type: application/json" \
    -d '{"path": "/preferences/formatting.md", "content": "Always use tabs, not spaces."}')
  mem_id=$(jq -r '.id' <<< "$mem")
  mem_sha=$(jq -r '.content_sha256' <<< "$mem")
  ```

  ```bash CLI
  mem=$(ant beta:memory-stores:memories create \
    --memory-store-id "$store_id" \
    --path "/preferences/formatting.md" \
    --content "Always use tabs, not spaces." \
    --format json)
  mem_id=$(jq -r '.id' <<< "$mem")
  mem_sha=$(jq -r '.content_sha256' <<< "$mem")
  ```

  ```python Python
  mem = client.beta.memory_stores.memories.create(
      store.id,
      path="/preferences/formatting.md",
      content="Always use tabs, not spaces.",
  )
  ```

  ```typescript TypeScript
  const mem = await client.beta.memoryStores.memories.create(store.id, {
    path: "/preferences/formatting.md",
    content: "Always use tabs, not spaces."
  });
  ```

  ```csharp C#
  var mem = await client.Beta.MemoryStores.Memories.Create(store.ID, new()
  {
      Path = "/preferences/formatting.md",
      Content = "Always use tabs, not spaces.",
  });
  ```

  ```go Go
  mem, err := client.Beta.MemoryStores.Memories.New(ctx, store.ID, anthropic.BetaMemoryStoreMemoryNewParams{
  	Path:    "/preferences/formatting.md",
  	Content: anthropic.String("Always use tabs, not spaces."),
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var mem = client.beta().memoryStores().memories().create(
      store.id(),
      MemoryCreateParams.builder()
          .path("/preferences/formatting.md")
          .content("Always use tabs, not spaces.")
          .build()
  );
  ```

  ```php PHP
  $mem = $client->beta->memoryStores->memories->create(
      $store->id,
      path: '/preferences/formatting.md',
      content: 'Always use tabs, not spaces.',
  );
  ```

  ```ruby Ruby
  mem = client.beta.memory_stores.memories.create(
    store.id,
    path: "/preferences/formatting.md",
    content: "Always use tabs, not spaces."
  )
  ```
</CodeGroup>

See the [Create a memory reference](/docs/en/api/beta/memory_stores/memories/create) for full parameters and response schema.

### Update a memory

`memories.update` modifies an existing memory by ID. You can change `content`, `path` (a rename), or both. The example renames a memory to an archive path:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s -X POST "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" \
    -H "content-type: application/json" \
    -d '{"path": "/archive/2026_q1_formatting.md"}' > /dev/null
  ```

  ```bash CLI
  ant beta:memory-stores:memories update \
    --memory-store-id "$store_id" \
    --memory-id "$mem_id" \
    --path "/archive/2026_q1_formatting.md" \
    > /dev/null
  ```

  ```python Python
  client.beta.memory_stores.memories.update(
      mem.id,
      memory_store_id=store.id,
      path="/archive/2026_q1_formatting.md",
  )
  ```

  ```typescript TypeScript
  await client.beta.memoryStores.memories.update(mem.id, {
    memory_store_id: store.id,
    path: "/archive/2026_q1_formatting.md"
  });
  ```

  ```csharp C#
  await client.Beta.MemoryStores.Memories.Update(mem.ID, new()
  {
      MemoryStoreID = store.ID,
      Path = "/archive/2026_q1_formatting.md",
  });
  ```

  ```go Go
  _, err = client.Beta.MemoryStores.Memories.Update(ctx, mem.ID, anthropic.BetaMemoryStoreMemoryUpdateParams{
  	MemoryStoreID: store.ID,
  	Path:          anthropic.String("/archive/2026_q1_formatting.md"),
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().memoryStores().memories().update(
      mem.id(),
      MemoryUpdateParams.builder()
          .memoryStoreId(store.id())
          .path("/archive/2026_q1_formatting.md")
          .build()
  );
  ```

  ```php PHP
  $client->beta->memoryStores->memories->update(
      $mem->id,
      memoryStoreID: $store->id,
      path: '/archive/2026_q1_formatting.md',
  );
  ```

  ```ruby Ruby
  client.beta.memory_stores.memories.update(
    mem.id,
    memory_store_id: store.id,
    path: "/archive/2026_q1_formatting.md"
  )
  ```
</CodeGroup>

See the [Update a memory reference](/docs/en/api/beta/memory_stores/memories/update) for full parameters and response schema.

#### Safe content edits (optimistic concurrency)

To avoid clobbering a concurrent write, pass a `content_sha256` precondition. The update only applies if the stored content hash still matches the one you read; on mismatch, re-read the memory and retry against the fresh state.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s -X POST "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" \
    -H "content-type: application/json" \
    --data @- > /dev/null <<EOF
  {
    "content": "CORRECTED: Always use 2-space indentation.",
    "precondition": {"type": "content_sha256", "content_sha256": "$mem_sha"}
  }
  EOF
  ```

  ```bash CLI
  ant beta:memory-stores:memories update \
    --memory-store-id "$store_id" \
    --memory-id "$mem_id" \
    --content "CORRECTED: Always use 2-space indentation." \
    --precondition "{type: content_sha256, content_sha256: $mem_sha}" \
    > /dev/null
  ```

  ```python Python
  client.beta.memory_stores.memories.update(
      memory_id=mem.id,
      memory_store_id=store.id,
      content="CORRECTED: Always use 2-space indentation.",
      precondition={"type": "content_sha256", "content_sha256": mem.content_sha256},
  )
  ```

  ```typescript TypeScript
  await client.beta.memoryStores.memories.update(mem.id, {
    memory_store_id: store.id,
    content: "CORRECTED: Always use 2-space indentation.",
    precondition: { type: "content_sha256", content_sha256: mem.content_sha256 }
  });
  ```

  ```csharp C#
  await client.Beta.MemoryStores.Memories.Update(mem.ID, new()
  {
      MemoryStoreID = store.ID,
      Content = "CORRECTED: Always use 2-space indentation.",
      Precondition = new BetaManagedAgentsPrecondition
      {
          Type = "content_sha256",
          ContentSha256 = mem.ContentSha256,
      },
  });
  ```

  ```go Go
  _, err = client.Beta.MemoryStores.Memories.Update(ctx, mem.ID, anthropic.BetaMemoryStoreMemoryUpdateParams{
  	MemoryStoreID: store.ID,
  	Content:       anthropic.String("CORRECTED: Always use 2-space indentation."),
  	Precondition: anthropic.BetaManagedAgentsPreconditionParam{
  		Type:          anthropic.BetaManagedAgentsPreconditionTypeContentSha256,
  		ContentSha256: anthropic.String(mem.ContentSha256),
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().memoryStores().memories().update(
      mem.id(),
      MemoryUpdateParams.builder()
          .memoryStoreId(store.id())
          .content("CORRECTED: Always use 2-space indentation.")
          .precondition(
              BetaManagedAgentsPrecondition.builder()
                  .type(BetaManagedAgentsPrecondition.Type.CONTENT_SHA256)
                  .contentSha256(mem.contentSha256())
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $client->beta->memoryStores->memories->update(
      $mem->id,
      memoryStoreID: $store->id,
      content: 'CORRECTED: Always use 2-space indentation.',
      precondition: ['type' => 'content_sha256', 'content_sha256' => $mem->contentSha256],
  );
  ```

  ```ruby Ruby
  client.beta.memory_stores.memories.update(
    mem.id,
    memory_store_id: store.id,
    content: "CORRECTED: Always use 2-space indentation.",
    precondition: {type: "content_sha256", content_sha256: mem.content_sha256}
  )
  ```
</CodeGroup>

### Delete a memory

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s -X DELETE "https://api.anthropic.com/v1/memory_stores/$store_id/memories/$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" > /dev/null
  ```

  ```bash CLI
  ant beta:memory-stores:memories delete \
    --memory-store-id "$store_id" \
    --memory-id "$mem_id" \
    > /dev/null
  ```

  ```python Python
  client.beta.memory_stores.memories.delete(
      mem.id,
      memory_store_id=store.id,
  )
  ```

  ```typescript TypeScript
  await client.beta.memoryStores.memories.delete(mem.id, {
    memory_store_id: store.id
  });
  ```

  ```csharp C#
  await client.Beta.MemoryStores.Memories.Delete(mem.ID, new()
  {
      MemoryStoreID = store.ID,
  });
  ```

  ```go Go
  _, err = client.Beta.MemoryStores.Memories.Delete(ctx, mem.ID, anthropic.BetaMemoryStoreMemoryDeleteParams{
  	MemoryStoreID: store.ID,
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().memoryStores().memories().delete(
      mem.id(),
      MemoryDeleteParams.builder().memoryStoreId(store.id()).build()
  );
  ```

  ```php PHP
  $client->beta->memoryStores->memories->delete($mem->id, memoryStoreID: $store->id);
  ```

  ```ruby Ruby
  client.beta.memory_stores.memories.delete(
    mem.id,
    memory_store_id: store.id
  )
  ```
</CodeGroup>

See the [Delete a memory reference](/docs/en/api/beta/memory_stores/memories/delete) for full parameters and response schema.

## Audit memory changes

Every mutation to a memory creates an immutable **memory version** (`memver_...`). Use the version endpoints to audit who changed what and when, to inspect or restore a prior snapshot, and to scrub sensitive content out of history with redact.

Versions belong to the store (not the individual memory) and survive even after the memory itself is deleted, so the audit trail stays complete. Versions are retained for 30 days; however, the recent versions are always kept regardless of age, so memories that change infrequently might retain history beyond 30 days. The live `memories.retrieve` call always returns the latest version; the version endpoints give you the retained history.

There is no dedicated restore endpoint; to roll back, retrieve the version you want and write its `content` back with `memories.update` (or `memories.create` if the parent memory has been deleted, because versions outlive their parent).

Past memory versions might be deleted after 30 days. To preserve memory history for longer, export versions through the API.

### List versions

List version history for a store, newest first. The example filters to a single memory's history:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  versions=$(curl -s "https://api.anthropic.com/v1/memory_stores/$store_id/memory_versions?memory_id=$mem_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22")
  jq -r '.data[] | "\(.id): \(.operation)"' <<< "$versions"
  version_id=$(jq -r '.data[1].id' <<< "$versions")
  ```

  ```bash CLI
  versions=$(ant beta:memory-stores:memory-versions list \
    --memory-store-id "$store_id" \
    --memory-id "$mem_id" \
    --format json)
  jq -r '.data[] | "\(.id): \(.operation)"' <<< "$versions"
  version_id=$(jq -r '.data[1].id' <<< "$versions")
  ```

  ```python Python
  versions = client.beta.memory_stores.memory_versions.list(
      store.id,
      memory_id=mem.id,
  )
  for v in versions:
      print(f"{v.id}: {v.operation}")

  version_id = versions.data[1].id
  ```

  ```typescript TypeScript
  const versions = await client.beta.memoryStores.memoryVersions.list(store.id, {
    memory_id: mem.id
  });
  for await (const v of versions) {
    console.log(`${v.id}: ${v.operation}`);
  }

  const versionId = versions.data[1].id;
  ```

  ```csharp C#
  var versions = await client.Beta.MemoryStores.MemoryVersions.List(store.ID, new()
  {
      MemoryID = mem.ID,
  });
  var versionIds = new List<string>();
  await foreach (var v in versions.Paginate())
  {
      Console.WriteLine($"{v.ID}: {v.Operation.Raw()}");
      versionIds.Add(v.ID);
  }

  var versionId = versionIds[1];
  ```

  ```go Go
  versions := client.Beta.MemoryStores.MemoryVersions.ListAutoPaging(ctx, store.ID, anthropic.BetaMemoryStoreMemoryVersionListParams{
  	MemoryID: anthropic.String(mem.ID),
  })
  for versions.Next() {
  	v := versions.Current()
  	fmt.Printf("%s: %s\n", v.ID, v.Operation)
  }
  if err := versions.Err(); err != nil {
  	panic(err)
  }

  vpage, err := client.Beta.MemoryStores.MemoryVersions.List(ctx, store.ID, anthropic.BetaMemoryStoreMemoryVersionListParams{
  	MemoryID: anthropic.String(mem.ID),
  })
  if err != nil {
  	panic(err)
  }
  versionID := vpage.Data[1].ID
  ```

  ```java Java
  var versions = client.beta().memoryStores().memoryVersions().list(
      store.id(),
      MemoryVersionListParams.builder().memoryId(mem.id()).build()
  );
  for (var v : versions.autoPager()) {
      IO.println(v.id() + ": " + v.operation());
  }

  var versionId = versions.data().get(1).id();
  ```

  ```php PHP
  $versions = $client->beta->memoryStores->memoryVersions->list(
      $store->id,
      memoryID: $mem->id,
  );
  foreach ($versions->pagingEachItem() as $v) {
      echo "{$v->id}: {$v->operation}\n";
  }

  $versionId = $versions->data[1]->id;
  ```

  ```ruby Ruby
  versions = client.beta.memory_stores.memory_versions.list(
    store.id,
    memory_id: mem.id
  )
  versions.auto_paging_each do |v|
    puts "#{v.id}: #{v.operation}"
  end

  version_id = versions.data[1].id
  ```
</CodeGroup>

See the [List memory versions reference](/docs/en/api/beta/memory_stores/memory_versions/list) for full parameters and response schema.

### Retrieve a version

Fetching an individual version returns the same fields as the list response plus the full `content` body.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s "https://api.anthropic.com/v1/memory_stores/$store_id/memory_versions/$version_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22"
  ```

  ```bash CLI
  ant beta:memory-stores:memory-versions retrieve \
    --memory-store-id "$store_id" \
    --memory-version-id "$version_id"
  ```

  ```python Python
  version = client.beta.memory_stores.memory_versions.retrieve(
      version_id,
      memory_store_id=store.id,
  )
  print(version.content)
  ```

  ```typescript TypeScript
  const version = await client.beta.memoryStores.memoryVersions.retrieve(versionId, {
    memory_store_id: store.id
  });
  console.log(version.content);
  ```

  ```csharp C#
  var version = await client.Beta.MemoryStores.MemoryVersions.Retrieve(versionId, new()
  {
      MemoryStoreID = store.ID,
  });
  Console.WriteLine(version.Content);
  ```

  ```go Go
  version, err := client.Beta.MemoryStores.MemoryVersions.Get(ctx, versionID, anthropic.BetaMemoryStoreMemoryVersionGetParams{
  	MemoryStoreID: store.ID,
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(version.Content)
  ```

  ```java Java
  var version = client.beta().memoryStores().memoryVersions().retrieve(
      versionId,
      MemoryVersionRetrieveParams.builder().memoryStoreId(store.id()).build()
  );
  IO.println(version.content());
  ```

  ```php PHP
  $version = $client->beta->memoryStores->memoryVersions->retrieve(
      $versionId,
      memoryStoreID: $store->id,
  );
  echo "{$version->content}\n";
  ```

  ```ruby Ruby
  version = client.beta.memory_stores.memory_versions.retrieve(
    version_id,
    memory_store_id: store.id
  )
  puts version.content
  ```
</CodeGroup>

See the [Retrieve a memory version reference](/docs/en/api/beta/memory_stores/memory_versions/retrieve) for full parameters and response schema.

### Redact a version

Redact scrubs content out of a historical version while preserving the audit trail (who did what, when). Use it for compliance workflows such as removing leaked secrets, PII, or user deletion requests.

A version that is the current head of a live memory cannot be redacted. Write a new version first (or delete the memory), then redact the old one.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s -X POST "https://api.anthropic.com/v1/memory_stores/$store_id/memory_versions/$version_id/redact" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" \
    -H "content-type: application/json" \
    -d '{}'
  ```

  ```bash CLI
  ant beta:memory-stores:memory-versions redact \
    --memory-store-id "$store_id" \
    --memory-version-id "$version_id"
  ```

  ```python Python
  client.beta.memory_stores.memory_versions.redact(
      version_id,
      memory_store_id=store.id,
  )
  ```

  ```typescript TypeScript
  await client.beta.memoryStores.memoryVersions.redact(versionId, {
    memory_store_id: store.id
  });
  ```

  ```csharp C#
  await client.Beta.MemoryStores.MemoryVersions.Redact(versionId, new()
  {
      MemoryStoreID = store.ID,
  });
  ```

  ```go Go
  _, err = client.Beta.MemoryStores.MemoryVersions.Redact(ctx, versionID, anthropic.BetaMemoryStoreMemoryVersionRedactParams{
  	MemoryStoreID: store.ID,
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().memoryStores().memoryVersions().redact(
      versionId,
      MemoryVersionRedactParams.builder().memoryStoreId(store.id()).build()
  );
  ```

  ```php PHP
  $client->beta->memoryStores->memoryVersions->redact(
      $versionId,
      memoryStoreID: $store->id,
  );
  ```

  ```ruby Ruby
  client.beta.memory_stores.memory_versions.redact(
    version_id,
    memory_store_id: store.id
  )
  ```
</CodeGroup>

See the [Redact a memory version reference](/docs/en/api/beta/memory_stores/memory_versions/redact) for full parameters and response schema.

## Manage memory stores

In addition to [`create`](/docs/en/api/beta/memory_stores/create), memory stores support [`retrieve`](/docs/en/api/beta/memory_stores/retrieve), [`update`](/docs/en/api/beta/memory_stores/update), [`list`](/docs/en/api/beta/memory_stores/list), [`archive`](/docs/en/api/beta/memory_stores/archive), and [`delete`](/docs/en/api/beta/memory_stores/delete).

### List stores

List stores in the workspace. Archived stores are excluded by default; pass `include_archived: true` to include them.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s "https://api.anthropic.com/v1/memory_stores?include_archived=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" | jq '.data[] | {id, name, archived_at}'
  ```

  ```bash CLI
  ant beta:memory-stores list --include-archived
  ```

  ```python Python
  for s in client.beta.memory_stores.list(include_archived=True):
      print(s.id, s.name, s.archived_at)
  ```

  ```typescript TypeScript
  for await (const s of client.beta.memoryStores.list({ include_archived: true })) {
    console.log(s.id, s.name, s.archived_at);
  }
  ```

  ```csharp C#
  var stores = await client.Beta.MemoryStores.List(new() { IncludeArchived = true });
  await foreach (var s in stores.Paginate())
  {
      Console.WriteLine($"{s.ID} {s.Name} {s.ArchivedAt}");
  }
  ```

  ```go Go
  stores := client.Beta.MemoryStores.ListAutoPaging(ctx, anthropic.BetaMemoryStoreListParams{
  	IncludeArchived: anthropic.Bool(true),
  })
  for stores.Next() {
  	s := stores.Current()
  	fmt.Println(s.ID, s.Name, s.ArchivedAt)
  }
  if err := stores.Err(); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  for (var s : client.beta().memoryStores().list(
      MemoryStoreListParams.builder().includeArchived(true).build()
  ).autoPager()) {
      IO.println(s.id() + " " + s.name() + " " + s.archivedAt());
  }
  ```

  ```php PHP
  foreach ($client->beta->memoryStores->list(includeArchived: true)->pagingEachItem() as $s) {
      echo "{$s->id} {$s->name} {$s->archivedAt}\n";
  }
  ```

  ```ruby Ruby
  client.beta.memory_stores.list(include_archived: true).auto_paging_each do |s|
    puts "#{s.id} #{s.name} #{s.archived_at}"
  end
  ```
</CodeGroup>

See the [List memory stores reference](/docs/en/api/beta/memory_stores/list) for full parameters and response schema.

### Archive a store

Archiving makes a store read-only and prevents it from being attached to new sessions. Archiving is one-way; there is no unarchive.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl -s -X POST "https://api.anthropic.com/v1/memory_stores/$store_id/archive" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: agent-memory-2026-07-22" > /dev/null
  ```

  ```bash CLI
  ant beta:memory-stores archive --memory-store-id "$store_id"
  ```

  ```python Python
  client.beta.memory_stores.archive(store.id)
  ```

  ```typescript TypeScript
  await client.beta.memoryStores.archive(store.id);
  ```

  ```csharp C#
  await client.Beta.MemoryStores.Archive(store.ID);
  ```

  ```go Go
  _, err = client.Beta.MemoryStores.Archive(ctx, store.ID, anthropic.BetaMemoryStoreArchiveParams{})
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().memoryStores().archive(store.id());
  ```

  ```php PHP
  $client->beta->memoryStores->archive($store->id);
  ```

  ```ruby Ruby
  client.beta.memory_stores.archive(store.id)
  ```
</CodeGroup>

See the [Archive a memory store reference](/docs/en/api/beta/memory_stores/archive) for full parameters and response schema.

To permanently remove a store along with all of its memories and versions, use [`memory_stores.delete`](/docs/en/api/beta/memory_stores/delete).

## Best practices for memory management

When a store reaches its 2,000-memory limit, writes to new memories fail: both direct `memories.create` calls and the agent's file writes to unmapped paths. Existing memories remain readable and editable. The following practices help you stay well under the limit and recover gracefully if you reach it.

* **Use focused stores.** Rather than one large general-purpose store, use smaller purpose-built stores — one per user, one for shared domain knowledge, and one for project-specific context. Each store has its own 2,000-memory limit, so keeping stores scoped reduces the chance any single one fills up.

* **Condense or prune before the store fills up.** Delete stale or redundant memories with `memories.delete`. You can also run a [dreaming session](/docs/en/managed-agents/dreams), which consolidates fragmented content into a separate new output store rather than modifying the original. Switch your sessions over to that output store, then archive or delete the original.

* **Attach a new store when it makes sense.** If a store has grown beyond its useful scope, attach a fresh one for new content and attach the original with `read_only` access. The agent can read from both while only writing to the new one.

* **Limit write access where appropriate.** Sessions that only read shared reference material don't need `read_write`. Keeping write access scoped to sessions that actually add new memories makes it easier to track where growth is coming from.
