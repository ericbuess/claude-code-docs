---
title: Adding files
url: https://platform.claude.com/docs/en/managed-agents/files
description: Upload files and mount them in your sandbox for reading and processing.
---

You can provide files to your agent by uploading them through the Files API and mounting them in the session's sandbox.

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](https://platform.claude.com/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Uploading files

First, upload a file using the [Files API](https://platform.claude.com/docs/en/build-with-claude/files):

<CodeGroup>
  ```bash cURL
  file=$(curl --fail-with-body -sS "${auth[@]}" \
    "${base_url}/files" \
    -F file=@data.csv)
  file_id=$(jq -er '.id' <<<"${file}")
  printf 'File ID: %s\n' "${file_id}"
  ```

  ```bash CLI
  FILE_ID=$(ant files upload \
    --file data.csv \
    --transform id --raw-output)
  ```

  ```python Python
  file = client.files.upload(file=Path("data.csv"))
  print(f"File ID: {file.id}")
  ```

  ```typescript TypeScript
  const file = await client.files.upload({
    file: await toFile(readFile("data.csv"), "data.csv", { type: "text/csv" }),
  });
  console.log(`File ID: ${file.id}`);
  ```

  ```csharp C#
  await using var stream = File.OpenRead(csvPath);
  var file = await client.Files.Upload(new() { File = stream });
  Console.WriteLine($"File ID: {file.ID}");
  ```

  ```go Go
  csvFile, err := os.Open("data.csv")
  if err != nil {
  	panic(err)
  }
  defer csvFile.Close()

  file, err := client.Files.Upload(ctx, anthropic.FileUploadParams{
  	File: csvFile,
  })
  if err != nil {
  	panic(err)
  }
  fmt.Printf("File ID: %s\n", file.ID)
  ```

  ```java Java
  var file = client.files().upload(
      FileUploadParams.builder().file(dataCsv).build()
  );
  IO.println("File ID: " + file.id());
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  $file = $client->beta->files->upload(
      FileParam::fromResource(fopen($csvPath, 'r'), filename: 'data.csv', contentType: 'text/csv'),
  );
  echo "File ID: {$file->id}\n";
  ```

  ```ruby Ruby
  file = client.files.upload(file: Pathname(csv_path))
  puts "File ID: #{file.id}"
  ```
</CodeGroup>

## Mounting files in a session

Mount uploaded files into the sandbox by adding them to the `resources` array when creating a session:

<Tip>
  The `mount_path` is optional, but make sure the uploaded file has a descriptive name so the agent can identify it.
</Tip>

<CodeGroup>
  ```bash cURL
  session=$(
    jq -n \
      --arg agent_id "${agent_id}" \
      --arg environment_id "${environment_id}" \
      --arg file_id "${file_id}" \
      '{
        agent: $agent_id,
        environment_id: $environment_id,
        resources: [
          {
            type: "file",
            file_id: $file_id,
            mount_path: "/data.csv"
          }
        ]
      }' | curl --fail-with-body -sS "${auth[@]}" "${base_url}/sessions" --json @-
  )
  session_id=$(jq -er '.id' <<<"${session}")
  ```

  ```bash CLI
  SESSION_ID=$(ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID" \
    --transform id --raw-output <<EOF
  resources:
    - type: file
      file_id: $FILE_ID
      mount_path: /data.csv
  EOF
  )
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      resources=[
          {
              "type": "file",
              "file_id": file.id,
              "mount_path": "/data.csv",
          },
      ],
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    resources: [
      {
        type: "file",
        file_id: file.id,
        mount_path: "/data.csv",
      },
    ],
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      Resources =
      [
          new BetaManagedAgentsFileResourceParams
          {
              Type = "file",
              FileID = file.ID,
              MountPath = "/data.csv",
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
  		OfFile: &anthropic.BetaManagedAgentsFileResourceParams{
  			Type:      anthropic.BetaManagedAgentsFileResourceParamsTypeFile,
  			FileID:    file.ID,
  			MountPath: anthropic.String("/data.csv"),
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
              BetaManagedAgentsFileResourceParams.builder()
                  .type(BetaManagedAgentsFileResourceParams.Type.FILE)
                  .fileId(file.id())
                  .mountPath("/data.csv")
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
          BetaManagedAgentsFileResourceParams::with(
              type: 'file',
              fileID: $file->id,
              mountPath: '/data.csv',
          ),
      ],
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    resources: [
      {
        type: "file",
        file_id: file.id,
        mount_path: "/data.csv"
      }
    ]
  )
  ```
</CodeGroup>

With the preceding `mount_path`, the agent reads the file at `/mnt/session/uploads/data.csv` (see [File paths](https://platform.claude.com/docs/en/managed-agents/files#file-paths)).

A new `file_id` is created that references the instance of the file in the session. These copies do not count against your [storage limits](https://platform.claude.com/docs/en/build-with-claude/files).

## Multiple files

Mount multiple files by adding entries to the `resources` array:

<CodeGroup>
  ```json cURL
  "resources": [
    { "type": "file", "file_id": "file_abc123", "mount_path": "/data.csv" },
    { "type": "file", "file_id": "file_def456", "mount_path": "/config.json" },
    { "type": "file", "file_id": "file_ghi789", "mount_path": "/src/main.py" }
  ]
  ```

  ```yaml CLI
  resources:
    - type: file
      file_id: file_abc123
      mount_path: /data.csv
    - type: file
      file_id: file_def456
      mount_path: /config.json
    - type: file
      file_id: file_ghi789
      mount_path: /src/main.py
  ```

  ```python Python
  resources = [
      {"type": "file", "file_id": "file_abc123", "mount_path": "/data.csv"},
      {"type": "file", "file_id": "file_def456", "mount_path": "/config.json"},
      {"type": "file", "file_id": "file_ghi789", "mount_path": "/src/main.py"},
  ]
  ```

  ```typescript TypeScript
  resources: [
    { type: "file", file_id: "file_abc123", mount_path: "/data.csv" },
    { type: "file", file_id: "file_def456", mount_path: "/config.json" },
    { type: "file", file_id: "file_ghi789", mount_path: "/src/main.py" }
  ]
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Sessions;

  var resources = new[]
  {
      new BetaManagedAgentsFileResourceParams { Type = BetaManagedAgentsFileResourceParamsType.File, FileID = "file_abc123", MountPath = "/data.csv" },
      new BetaManagedAgentsFileResourceParams { Type = BetaManagedAgentsFileResourceParamsType.File, FileID = "file_def456", MountPath = "/config.json" },
      new BetaManagedAgentsFileResourceParams { Type = BetaManagedAgentsFileResourceParamsType.File, FileID = "file_ghi789", MountPath = "/src/main.py" },
  };
  ```

  ```go Go
  resources := []anthropic.BetaSessionNewParamsResourceUnion{
  	{OfFile: &anthropic.BetaManagedAgentsFileResourceParams{Type: "file", FileID: "file_abc123", MountPath: anthropic.String("/data.csv")}},
  	{OfFile: &anthropic.BetaManagedAgentsFileResourceParams{Type: "file", FileID: "file_def456", MountPath: anthropic.String("/config.json")}},
  	{OfFile: &anthropic.BetaManagedAgentsFileResourceParams{Type: "file", FileID: "file_ghi789", MountPath: anthropic.String("/src/main.py")}},
  }
  ```

  ```java Java
  import com.anthropic.models.beta.sessions.*;
  import java.util.List;

  var resources = List.of(
      BetaManagedAgentsFileResourceParams.builder()
          .type(BetaManagedAgentsFileResourceParams.Type.FILE).fileId("file_abc123").mountPath("/data.csv").build(),
      BetaManagedAgentsFileResourceParams.builder()
          .type(BetaManagedAgentsFileResourceParams.Type.FILE).fileId("file_def456").mountPath("/config.json").build(),
      BetaManagedAgentsFileResourceParams.builder()
          .type(BetaManagedAgentsFileResourceParams.Type.FILE).fileId("file_ghi789").mountPath("/src/main.py").build()
  );
  ```

  ```php PHP
  $resources = [
      ['type' => 'file', 'file_id' => 'file_abc123', 'mount_path' => '/data.csv'],
      ['type' => 'file', 'file_id' => 'file_def456', 'mount_path' => '/config.json'],
      ['type' => 'file', 'file_id' => 'file_ghi789', 'mount_path' => '/src/main.py'],
  ];
  ```

  ```ruby Ruby
  resources = [
    {type: "file", file_id: "file_abc123", mount_path: "/data.csv"},
    {type: "file", file_id: "file_def456", mount_path: "/config.json"},
    {type: "file", file_id: "file_ghi789", mount_path: "/src/main.py"}
  ]
  ```
</CodeGroup>

A maximum of 500 files is supported per session.

## Managing files on a running session

You can add or remove files from a session after creation using the session resources API. Each resource has an `id` returned when it is added (or listed), which you use for deletes.

<CodeGroup>
  ```bash cURL
  resource=$(
    jq -n --arg file_id "${file_id}" '{type: "file", file_id: $file_id}' \
      | curl --fail-with-body -sS "${auth[@]}" \
          "${base_url}/sessions/${session_id}/resources" --json @-
  )
  resource_id=$(jq -er '.id' <<<"${resource}")
  printf '%s\n' "${resource_id}"  # "sesrsc_01ABC..."
  ```

  ```bash CLI
  RESOURCE_ID=$(ant beta:sessions:resources add \
    --session-id "$SESSION_ID" \
    --type file \
    --file-id "$FILE_ID" \
    --transform id --raw-output)
  ```

  ```python Python
  resource = client.beta.sessions.resources.add(
      session.id,
      type="file",
      file_id=file.id,
  )
  print(resource.id)  # "sesrsc_01ABC..."
  ```

  ```typescript TypeScript
  const resource = await client.beta.sessions.resources.add(session.id, {
    type: "file",
    file_id: file.id,
  });
  if (resource.type !== "file") {
    throw new Error(`Unexpected resource type: ${resource.type}`);
  }
  console.log(resource.id); // "sesrsc_01ABC..."
  ```

  ```csharp C#
  var resource = await client.Beta.Sessions.Resources.Add(session.ID, new()
  {
      Type = "file",
      FileID = file.ID,
  });
  Console.WriteLine(resource.ID);  // "sesrsc_01ABC..."
  ```

  ```go Go
  resource, err := client.Beta.Sessions.Resources.Add(ctx, session.ID, anthropic.BetaSessionResourceAddParams{
  	BetaManagedAgentsFileResourceParams: anthropic.BetaManagedAgentsFileResourceParams{
  		Type:   anthropic.BetaManagedAgentsFileResourceParamsTypeFile,
  		FileID: file.ID,
  	},
  })
  if err != nil {
  	panic(err)
  }
  fmt.Println(resource.ID) // "sesrsc_01ABC..."
  ```

  ```java Java
  var resource = client.beta().sessions().resources().add(
      session.id(),
      ResourceAddParams.builder()
          .betaManagedAgentsFileResourceParams(
              BetaManagedAgentsFileResourceParams.builder()
                  .type(BetaManagedAgentsFileResourceParams.Type.FILE)
                  .fileId(file.id())
                  .build()
          )
          .build()
  );
  IO.println(resource.id()); // "sesrsc_01ABC..."
  ```

  ```php PHP
  $resource = $client->beta->sessions->resources->add(
      $session->id,
      type: 'file',
      fileID: $file->id,
  );
  echo "{$resource->id}\n";  // "sesrsc_01ABC..."
  ```

  ```ruby Ruby
  resource = client.beta.sessions.resources.add(
    session.id,
    type: "file",
    file_id: file.id
  )
  puts resource.id # "sesrsc_01ABC..."
  ```
</CodeGroup>

List all resources on a session with `resources.list`. To remove a file, call `resources.delete` with the resource ID:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS "${auth[@]}" \
    "${base_url}/sessions/${session_id}/resources" \
    | jq -r '.data[] | "\(.id) \(.type)"'

  curl --fail-with-body -sS "${auth[@]}" -X DELETE \
    "${base_url}/sessions/${session_id}/resources/${resource_id}" >/dev/null
  ```

  ```bash CLI
  ant beta:sessions:resources list --session-id "$SESSION_ID"

  ant beta:sessions:resources delete \
    --session-id "$SESSION_ID" \
    --resource-id "$RESOURCE_ID"
  ```

  ```python Python
  listed = client.beta.sessions.resources.list(session.id)
  for entry in listed.data:
      print(entry.id, entry.type)

  client.beta.sessions.resources.delete(resource.id, session_id=session.id)
  ```

  ```typescript TypeScript
  const listed = await client.beta.sessions.resources.list(session.id);
  for (const entry of listed.data) {
    if (entry.type !== "memory_store") {
      console.log(entry.id, entry.type);
    }
  }

  await client.beta.sessions.resources.delete(resource.id, {
    session_id: session.id,
  });
  ```

  ```csharp C#
  var listed = await client.Beta.Sessions.Resources.List(session.ID);
  await foreach (var entry in listed.Paginate())
  {
      var type = entry.Match<string>(repo => repo.Type, fileRes => fileRes.Type, memoryStore => memoryStore.Type);
      Console.WriteLine($"{entry.ID} {type}");
  }

  await client.Beta.Sessions.Resources.Delete(resource.ID, new() { SessionID = session.ID });
  ```

  ```go Go
  listed, err := client.Beta.Sessions.Resources.List(ctx, session.ID, anthropic.BetaSessionResourceListParams{})
  if err != nil {
  	panic(err)
  }
  for _, entry := range listed.Data {
  	fmt.Println(entry.ID, entry.Type)
  }

  if _, err := client.Beta.Sessions.Resources.Delete(ctx, resource.ID, anthropic.BetaSessionResourceDeleteParams{
  	SessionID: session.ID,
  }); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var listed = client.beta().sessions().resources().list(session.id());
  for (var entry : listed.data()) {
      if (entry.isFile()) {
          var fileResource = entry.asFile();
          IO.println(fileResource.id() + " " + fileResource.type());
      } else if (entry.isGitHubRepository()) {
          var repoResource = entry.asGitHubRepository();
          IO.println(repoResource.id() + " " + repoResource.type());
      }
  }

  client.beta().sessions().resources().delete(
      resource.id(),
      ResourceDeleteParams.builder().sessionId(session.id()).build()
  );
  ```

  ```php PHP
  $listed = $client->beta->sessions->resources->list($session->id);
  foreach ($listed->data as $entry) {
      echo "{$entry->id} {$entry->type}\n";
  }

  $client->beta->sessions->resources->delete($resource->id, sessionID: $session->id);
  ```

  ```ruby Ruby
  listed = client.beta.sessions.resources.list(session.id)
  listed.data.each { puts "#{it.id} #{it.type}" }

  client.beta.sessions.resources.delete(resource.id, session_id: session.id)
  ```
</CodeGroup>

## Listing and downloading session files

Use the [Files API](https://platform.claude.com/docs/en/build-with-claude/files) to list files scoped to a session and download them. Filtering by `scope_id` requires the `managed-agents-2026-04-01` beta header, so the list examples use the `beta` files namespace and pass that header explicitly.

<CodeGroup>
  ```bash cURL
  # List files associated with a session
  curl -fsSL "https://api.anthropic.com/v1/files?scope_id=sesn_abc123" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01"

  # Download a file
  curl -fsSL "https://api.anthropic.com/v1/files/$FILE_ID/content" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -o output.txt
  ```

  ```bash CLI
  # List files associated with a session
  ant beta:files list --scope-id sesn_abc123 \
    --beta managed-agents-2026-04-01

  # Download a file
  ant files download --file-id "$FILE_ID" --output output.txt
  ```

  ```python Python
  # List files associated with a session
  files = client.beta.files.list(
      scope_id="sesn_abc123",
      betas=["managed-agents-2026-04-01"],
  )
  for file in files:
      print(file.id, file.filename)

  # Download a file
  content = client.files.download(files.data[0].id)
  content.write_to_file("output.txt")
  ```

  ```typescript TypeScript
  import { writeFile } from "node:fs/promises";

  // List files associated with a session
  const files = await client.beta.files.list({
    scope_id: "sesn_abc123",
    betas: ["managed-agents-2026-04-01"]
  });
  for (const file of files.data) {
    console.log(file.id, file.filename);
  }

  // Download a file
  const content = await client.files.download(files.data[0].id);
  await writeFile("output.txt", new Uint8Array(await content.arrayBuffer()));
  ```

  ```csharp C#
  // List files associated with a session
  var files = await client.Beta.Files.List(new()
  {
      ScopeID = "sesn_abc123",
      Betas = ["managed-agents-2026-04-01"],
  });

  // Download a file
  using var content = await client.Files.Download(files.Items[0].ID);
  await using var output = File.Create("output.txt");
  await (await content.ReadAsStream()).CopyToAsync(output);
  ```

  ```go Go
  // List files associated with a session
  files, err := client.Beta.Files.List(ctx, anthropic.BetaFileListParams{
  	ScopeID: anthropic.String("sesn_abc123"),
  	Betas:   []anthropic.AnthropicBeta{"managed-agents-2026-04-01"},
  })
  if err != nil {
  	panic(err)
  }

  // Download a file
  resp, err := client.Files.Download(ctx, files.Data[0].ID)
  if err != nil {
  	panic(err)
  }
  defer resp.Body.Close()
  out, err := os.Create("output.txt")
  if err != nil {
  	panic(err)
  }
  defer out.Close()
  if _, err := io.Copy(out, resp.Body); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  // List files associated with a session
  var files = client.beta().files().list(FileListParams.builder()
      .scopeId("sesn_abc123")
      .addBeta(AnthropicBeta.of("managed-agents-2026-04-01"))
      .build());

  // Download a file
  try (HttpResponse response = client.files().download(files.data().get(0).id())) {
      try (InputStream body = response.body()) {
          Files.copy(body, Path.of("output.txt"), StandardCopyOption.REPLACE_EXISTING);
      }
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  // List files associated with a session
  $files = $client->beta->files->list(
      scopeID: 'sesn_abc123',
      betas: ['managed-agents-2026-04-01'],
  );

  // Download a file
  $content = $client->beta->files->download($files->data[0]->id);
  file_put_contents('output.txt', $content);
  ```

  ```ruby Ruby
  # List files associated with a session
  files = client.beta.files.list(
    scope_id: "sesn_abc123",
    betas: ["managed-agents-2026-04-01"]
  )

  # Download a file
  content = client.files.download(files.data[0].id)
  File.binwrite("output.txt", content.read)
  ```
</CodeGroup>

## Supported file types

The agent can work with any file type, including:

* Source code (`.py`, `.js`, `.ts`, `.go`, `.rs`, and others)
* Data files (`.csv`, `.json`, `.xml`, `.yaml`)
* Documents (`.txt`, `.md`)
* Archives (`.zip`, `.tar.gz`) - the agent can extract these using bash
* Binary files - the agent can process these with appropriate tools

## File paths

<Note>
  Files mounted in the sandbox are read-only copies. The agent can read them but cannot modify the original uploaded file. To work with modified versions, the agent writes to new paths within the sandbox.
</Note>

* The path you specify is rooted under the session's uploads directory: a `mount_path` of `/data.csv` places the file at `/mnt/session/uploads/data.csv` in the sandbox
* If you omit `mount_path`, the file is placed at `/mnt/session/uploads/<file_id>`
* Parent directories are created automatically
* Paths should be absolute (starting with `/`)
