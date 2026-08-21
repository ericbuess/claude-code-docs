---
title: Using Agent Skills with the API
url: https://platform.claude.com/docs/en/build-with-claude/skills-guide
description: Learn how to use Agent Skills to extend Claude's capabilities through the API.
---

Agent Skills extend Claude's capabilities through organized folders of instructions, scripts, and resources. This guide shows you how to use both pre-built and custom Skills with the Claude API.

<Note>
  For complete API reference including request/response schemas and all parameters, see:

  * [Skill Management API Reference](https://platform.claude.com/docs/en/api/skills/list) - CRUD operations for Skills
  * [Skill Versions API Reference](https://platform.claude.com/docs/en/api/skills/versions/list) - Version management
</Note>

<Note>
  For how zero data retention (ZDR) applies to this feature, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).
</Note>

## Quick links

<CardGroup cols={2}>
  <Card title="Get started with Agent Skills in the API" icon="rocket" href="https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart">
    Learn how to use Agent Skills to create documents with the Claude API in under 10 minutes.
  </Card>

  <Card title="Skill authoring best practices" icon="hammer" href="https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices">
    Learn how to write effective Skills that Claude can discover and use successfully.
  </Card>
</CardGroup>

## Overview

<Note>
  For a detailed look at the architecture and real-world applications of Agent Skills, read the engineering blog post: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
</Note>

Skills integrate with the Messages API through the [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool). Whether using pre-built Skills managed by Anthropic or custom Skills you've uploaded, the integration shape is identical: both require code execution and use the same `container` structure.

### Using Skills

Skills integrate identically in the Messages API regardless of source. You specify Skills in the `container` parameter with a `skill_id`, `type`, and optional `version`, and they run in the code execution environment.

You can use Skills from two sources:

| Aspect             | Anthropic Skills                           | Custom Skills                                                                                     |
| ------------------ | ------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| **Type value**     | `anthropic`                                | `custom`                                                                                          |
| **Skill IDs**      | Short names: `pptx`, `xlsx`, `docx`, `pdf` | Generated: `skill_01AbCdEfGhIjKlMnOpQrStUv`                                                       |
| **Version format** | Date-based: `20251013` or `latest`         | Version ID: `skver_01AbCdEfGhIjKlMnOpQrStUv` or `latest`                                          |
| **Management**     | Pre-built and maintained by Anthropic      | Upload and manage through the [Skills API](https://platform.claude.com/docs/en/api/skills/create) |
| **Availability**   | Available to all users                     | Private to your workspace                                                                         |

Both skill sources are returned by the [List Skills endpoint](https://platform.claude.com/docs/en/api/skills/list) (use the `source` parameter to filter). The integration shape and execution environment are identical. The only difference is where the Skills come from and how they're managed.

### Prerequisites

To use Skills, you need:

1. **Claude API key** from the [Claude Console](https://platform.claude.com/settings/keys)
2. **[Code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)** enabled in your requests

Skills require the code execution tool, so use a model from its [model compatibility list](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#model-compatibility).

***

## Using Skills in Messages

### Container parameter

Skills are specified using the `container` parameter in the Messages API. You can include up to 20 Skills for each request.

The structure is identical for both Anthropic and custom Skills. Specify the required `type` and `skill_id`, and optionally include `version` to pin to a specific version:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {
            "type": "anthropic",
            "skill_id": "pptx",
            "version": "latest"
          }
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Create a presentation about renewable energy"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: anthropic
        skill_id: pptx
        version: latest
  messages:
    - role: user
      content: Create a presentation about renewable energy
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      container={
          "skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]
      },
      messages=[
          {"role": "user", "content": "Create a presentation about renewable energy"}
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [
        {
          type: "anthropic",
          skill_id: "pptx",
          version: "latest"
        }
      ]
    },
    messages: [
      {
        role: "user",
        content: "Create a presentation about renewable energy"
      }
    ],
    tools: [
      {
        type: "code_execution_20250825",
        name: "code_execution"
      }
    ]
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Container = new ContainerParams
      {
          Skills =
          [
              new SkillParams
              {
                  Type = SkillParamsType.Anthropic,
                  SkillID = "pptx",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Create a presentation about renewable energy" }],
      Tools = [new CodeExecutionTool20250825()],
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeAnthropic,
  					SkillID: "pptx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Create a presentation about renewable energy")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.ContainerParams;
  import com.anthropic.models.messages.SkillParams;
  import com.anthropic.models.messages.CodeExecutionTool20250825;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .container(ContainerParams.builder()
              .addSkill(SkillParams.builder()
                  .type(SkillParams.Type.ANTHROPIC)
                  .skillId("pptx")
                  .version("latest")
                  .build())
              .build())
          .addUserMessage("Create a presentation about renewable energy")
          .addTool(CodeExecutionTool20250825.builder().build())
          .build();

      Message response = client.messages().create(params);
      System.out.println(response);
  }
  ```

  ```php PHP
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Create a presentation about renewable energy']
      ],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [
              [
                  'type' => 'anthropic',
                  'skill_id' => 'pptx',
                  'version' => 'latest'
              ]
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [
        {
          type: "anthropic",
          skill_id: "pptx",
          version: "latest"
        }
      ]
    },
    messages: [
      { role: "user", content: "Create a presentation about renewable energy" }
    ],
    tools: [
      { type: "code_execution_20250825", name: "code_execution" }
    ]
  )
  puts message
  ```
</CodeGroup>

### Downloading generated files

When Skills create documents (Excel, PowerPoint, PDF, Word), they return `file_id` attributes in the response. You must use the Files API to download these files.

**How it works:**

1. Skills create files during code execution.
2. The response includes a `file_id` for each created file, inside code-execution tool result blocks (see [Response format](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#response-format)).
3. Use the Files API to download the actual file content.
4. Save locally or process as needed.

To provide input files for Skills to work on, [upload them with the Files API](https://platform.claude.com/docs/en/build-with-claude/files#uploading-a-file) and reference them in your request with a [container upload block](https://platform.claude.com/docs/en/build-with-claude/files#container-upload-blocks).

**Example: creating and downloading an Excel file**

<CodeGroup>
  ```bash cURL
  # Step 1: Use a Skill to create a file
  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Create an Excel file with a simple budget spreadsheet"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }')

  # Step 2: Extract file_id from response (using jq)
  FILE_ID=$(echo "$RESPONSE" | jq -r '.content[] | select(.type=="bash_code_execution_tool_result") | .content | select(.type=="bash_code_execution_result") | .content[] | select(.file_id) | .file_id')

  # Step 3: Get filename from metadata
  FILENAME=$(curl "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" | jq -r '.filename')

  # Step 4: Download the file using Files API
  curl "https://api.anthropic.com/v1/files/$FILE_ID/content" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    --output "$FILENAME"

  echo "Downloaded: $FILENAME"
  ```

  ```bash CLI
  # Step 1: Use the xlsx Skill to create a file
  # Step 2: Extract file_id from the response with --transform (GJSON path)
  FILE_ID=$(ant messages create \
    --transform 'content.#.content.content.#.file_id|@flatten|0' \
    --raw-output <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: anthropic
        skill_id: xlsx
        version: latest
  messages:
    - role: user
      content: Create an Excel file with a simple budget spreadsheet
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  )

  # Step 3: Get the filename from file metadata
  FILENAME=$(ant files retrieve-metadata \
    --file-id "$FILE_ID" \
    --transform filename \
    --raw-output)

  # Step 4: Download the file using Files API
  ant files download \
    --file-id "$FILE_ID" \
    --output "$FILENAME" > /dev/null

  printf 'Downloaded: %s\n' "$FILENAME"
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Step 1: Use a Skill to create a file
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      container={
          "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
      },
      messages=[
          {
              "role": "user",
              "content": "Create an Excel file with a simple budget spreadsheet",
          }
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )


  # Step 2: Extract file IDs from the response
  def extract_file_ids(response):
      file_ids = []
      for item in response.content:
          if item.type == "bash_code_execution_tool_result":
              content_item = item.content
              if content_item.type == "bash_code_execution_result":
                  # each content item is a bash_code_execution_output block carrying a file_id
                  for file in content_item.content:
                      file_ids.append(file.file_id)
      return file_ids


  # Step 3: Download the file using Files API
  for file_id in extract_file_ids(response):
      file_metadata = client.files.retrieve_metadata(file_id=file_id)
      file_content = client.files.download(file_id=file_id)

      # Step 4: Save to disk
      file_content.write_to_file(file_metadata.filename)
      print(f"Downloaded: {file_metadata.filename}")
  ```

  ```typescript TypeScript
  import { writeFile } from "node:fs/promises";

  const client = new Anthropic();

  // Step 1: Use a Skill to create a file
  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [
      {
        role: "user",
        content: "Create an Excel file with a simple budget spreadsheet"
      }
    ],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Step 2: Extract file IDs from the response
  const fileIds: string[] = [];
  for (const block of response.content) {
    if (
      block.type === "bash_code_execution_tool_result" &&
      block.content.type === "bash_code_execution_result"
    ) {
      for (const outputBlock of block.content.content) {
        fileIds.push(outputBlock.file_id);
      }
    }
  }

  // Step 3: Download each file and save to disk
  for (const fileId of fileIds) {
    const fileMetadata = await client.files.retrieveMetadata(fileId);
    const fileResponse = await client.files.download(fileId);

    await writeFile(fileMetadata.filename, Buffer.from(await fileResponse.arrayBuffer()));
    console.log(`Downloaded: ${fileMetadata.filename}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Step 1: Use a Skill to create a file
  var parameters = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Container = new ContainerParams
      {
          Skills =
          [
              new SkillParams
              {
                  Type = SkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Create an Excel file with a simple budget spreadsheet" }],
      Tools = [new CodeExecutionTool20250825()],
  };

  var response = await client.Messages.Create(parameters);

  // Step 2: Extract file IDs from the response
  List<string> fileIds = [];
  foreach (var block in response.Content)
  {
      if (block.TryPickBashCodeExecutionToolResult(out var toolResult)
          && toolResult.Content.TryPickBashCodeExecutionResultBlock(out var result))
      {
          foreach (var output in result.Content)
          {
              fileIds.Add(output.FileID);
          }
      }
  }

  // Step 3: Download each file and save to disk
  foreach (var fileId in fileIds)
  {
      var fileMetadata = await client.Files.RetrieveMetadata(fileId);
      using var download = await client.Files.Download(fileId);
      using var downloadStream = await download.ReadAsStream();
      using var outputFile = File.Create(fileMetadata.Filename);
      await downloadStream.CopyToAsync(outputFile);
      Console.WriteLine($"Downloaded: {fileMetadata.Filename}");
  }
  ```

  ```go Go
  func main() {
  	client := anthropic.NewClient()

  	// Step 1: Use a Skill to create a file
  	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     "claude-opus-5",
  		MaxTokens: 4096,
  		Container: anthropic.MessageCreateParamsContainerUnion{
  			OfContainers: &anthropic.ContainerParams{
  				Skills: []anthropic.SkillParams{
  					{
  						Type:    anthropic.SkillParamsTypeAnthropic,
  						SkillID: "xlsx",
  						Version: anthropic.String("latest"),
  					},
  				},
  			},
  		},
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Create an Excel file with a simple budget spreadsheet")),
  		},
  		Tools: []anthropic.ToolUnionParam{
  			{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// Step 2: Extract file IDs from the response
  	fileIDs := extractFileIDs(response)

  	// Step 3: Download the file using Files API
  	for _, fileID := range fileIDs {
  		fileMetadata, err := client.Files.GetMetadata(context.TODO(), fileID)
  		if err != nil {
  			log.Fatal(err)
  		}

  		fileContent, err := client.Files.Download(context.TODO(), fileID)
  		if err != nil {
  			log.Fatal(err)
  		}

  		// Step 4: Save to disk
  		out, err := os.Create(fileMetadata.Filename)
  		if err != nil {
  			log.Fatal(err)
  		}
  		if _, err := io.Copy(out, fileContent.Body); err != nil {
  			log.Fatal(err)
  		}
  		out.Close()
  		fileContent.Body.Close()
  		fmt.Printf("Downloaded: %s\n", fileMetadata.Filename)
  	}
  }

  func extractFileIDs(response *anthropic.Message) []string {
  	var fileIDs []string
  	for _, item := range response.Content {
  		switch v := item.AsAny().(type) {
  		case anthropic.BashCodeExecutionToolResultBlock:
  			if v.Content.Type == "bash_code_execution_result" {
  				for _, output := range v.Content.Content {
  					fileIDs = append(fileIDs, output.FileID)
  				}
  			}
  		}
  	}
  	return fileIDs
  }
  ```

  ```java Java
  import com.anthropic.models.messages.ContainerParams;
  import com.anthropic.models.messages.SkillParams;
  import com.anthropic.models.messages.CodeExecutionTool20250825;
  import com.anthropic.models.messages.ContentBlock;
  import com.anthropic.models.files.FileMetadata;
  import com.anthropic.core.http.HttpResponse;
  // ...
  void main() throws Exception {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Step 1: Use a Skill to create a file
      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .container(ContainerParams.builder()
              .addSkill(SkillParams.builder()
                  .type(SkillParams.Type.ANTHROPIC)
                  .skillId("xlsx")
                  .version("latest")
                  .build())
              .build())
          .addUserMessage("Create an Excel file with a simple budget spreadsheet")
          .addTool(CodeExecutionTool20250825.builder().build())
          .build();

      Message response = client.messages().create(params);

      // Step 2: Extract file IDs from the response
      List<String> fileIds = new ArrayList<>();
      for (ContentBlock block : response.content()) {
          if (block.isBashCodeExecutionToolResult()) {
              var content = block.asBashCodeExecutionToolResult().content();
              if (content.isBashCodeExecutionResultBlock()) {
                  for (var outputBlock : content.asBashCodeExecutionResultBlock().content()) {
                      fileIds.add(outputBlock.fileId());
                  }
              }
          }
      }

      // Step 3: Download the file using Files API
      for (String fileId : fileIds) {
          FileMetadata fileMetadata = client.files().retrieveMetadata(fileId);
          HttpResponse fileContent = client.files().download(fileId);

          // Step 4: Save to disk
          try (InputStream is = fileContent.body();
               FileOutputStream fos = new FileOutputStream(fileMetadata.filename())) {
              is.transferTo(fos);
          }
          System.out.println("Downloaded: " + fileMetadata.filename());
      }
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  $client = new Client();

  // Step 1: Use a Skill to create a file
  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Create an Excel file with a simple budget spreadsheet']
      ],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest']
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );

  // Step 2: Extract file IDs from the response
  function extractFileIds($response) {
      $fileIds = [];
      foreach ($response->content as $item) {
          if ($item->type === 'bash_code_execution_tool_result') {
              $contentItem = $item->content;
              if ($contentItem->type === 'bash_code_execution_result') {
                  foreach ($contentItem->content as $file) {
                      $fileIds[] = $file->fileID;
                  }
              }
          }
      }
      return $fileIds;
  }

  // Step 3: Download the file using Files API
  foreach (extractFileIds($response) as $fileId) {
      $fileMetadata = $client->beta->files->retrieveMetadata($fileId);
      $fileContent  = $client->beta->files->download($fileId);

      // Step 4: Save to disk
      file_put_contents($fileMetadata->filename, $fileContent);
      echo "Downloaded: {$fileMetadata->filename}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Step 1: Use a Skill to create a file
  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [
      {
        role: "user",
        content: "Create an Excel file with a simple budget spreadsheet"
      }
    ],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )

  # Step 2: Extract file IDs from the response
  def extract_file_ids(response)
    file_ids = []
    response.content.each do |item|
      if item.type == :bash_code_execution_tool_result
        content_item = item.content
        if content_item.type == :bash_code_execution_result
          content_item.content.each do |file|
            file_ids << file.file_id
          end
        end
      end
    end
    file_ids
  end

  # Step 3: Download the file using Files API
  extract_file_ids(response).each do |file_id|
    file_metadata = client.files.retrieve_metadata(file_id)

    file_content = client.files.download(file_id)

    # Step 4: Save to disk
    File.binwrite(file_metadata.filename, file_content.read)
    puts "Downloaded: #{file_metadata.filename}"
  end
  ```
</CodeGroup>

**Additional Files API operations:**

<CodeGroup>
  ```bash cURL
  # Get file metadata
  curl "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"

  # List all files
  curl "https://api.anthropic.com/v1/files" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"

  # Delete a file
  curl -X DELETE "https://api.anthropic.com/v1/files/$FILE_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  # Get file metadata
  ant files retrieve-metadata \
    --file-id "$FILE_ID" \
    --transform '{filename,size_bytes}' \
    --format yaml

  # List all files
  ant files list \
    --transform '{filename,created_at}' \
    --format yaml

  # Delete a file
  ant files delete --file-id "$FILE_ID" >/dev/null
  ```

  ```python Python
  client = anthropic.Anthropic()
  file_id = "file_011CNha8iCJcU1wXNR6q4V8w"
  # Get file metadata
  file_info = client.files.retrieve_metadata(file_id=file_id)
  print(f"Filename: {file_info.filename}, Size: {file_info.size_bytes} bytes")

  # List all files
  for file in client.files.list():
      print(f"{file.filename} - {file.created_at}")

  # Delete a file
  client.files.delete(file_id=file_id)
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const fileId = "file_011CNha8iCJcU1wXNR6q4V8w";

  // Get file metadata
  const fileInfo = await client.files.retrieveMetadata(fileId);
  console.log(`Filename: ${fileInfo.filename}, Size: ${fileInfo.size_bytes} bytes`);

  // List all files
  for await (const file of client.files.list()) {
    console.log(`${file.filename} - ${file.created_at}`);
  }

  // Delete a file
  await client.files.delete(fileId);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var fileId = "file_011CNha8iCJcU1wXNR6q4V8w";

  // Get file metadata
  var fileInfo = await client.Files.RetrieveMetadata(fileId);
  Console.WriteLine($"Filename: {fileInfo.Filename}, Size: {fileInfo.SizeBytes} bytes");

  // List files
  await foreach (var file in (await client.Files.List()).Paginate())
  {
      Console.WriteLine($"{file.Filename} - {file.CreatedAt}");
  }

  // Delete the file
  await client.Files.Delete(fileId);
  ```

  ```go Go
  client := anthropic.NewClient()
  fileID := "file_011CNha8iCJcU1wXNR6q4V8w"

  // Get file metadata
  fileInfo, err := client.Files.GetMetadata(context.TODO(), fileID)
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Printf("Filename: %s, Size: %d bytes\n", fileInfo.Filename, fileInfo.SizeBytes)

  // List all files
  files := client.Files.ListAutoPaging(context.TODO(), anthropic.FileListParams{})
  for files.Next() {
  	file := files.Current()
  	fmt.Printf("%s - %s\n", file.Filename, file.CreatedAt)
  }
  if files.Err() != nil {
  	log.Fatal(files.Err())
  }

  // Delete a file
  _, err = client.Files.Delete(context.TODO(), fileID)
  if err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.files.FileMetadata;
  import com.anthropic.models.files.FileListPage;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();
      String fileId = "file_011CNha8iCJcU1wXNR6q4V8w";

      // Get file metadata
      FileMetadata fileInfo = client.files().retrieveMetadata(fileId);
      System.out.println("Filename: " + fileInfo.filename() + ", Size: " + fileInfo.sizeBytes() + " bytes");

      // List files (first page)
      FileListPage files = client.files().list();
      for (var file : files.data()) {
          System.out.println(file.filename() + " - " + file.createdAt());
      }

      // Delete a file
      client.files().delete(fileId);
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  $client = new Client();
  $fileId = 'file_011CNha8iCJcU1wXNR6q4V8w';

  // Get file metadata
  $fileInfo = $client->beta->files->retrieveMetadata($fileId);
  echo "Filename: {$fileInfo->filename}, Size: {$fileInfo->sizeBytes} bytes\n";

  // List files (first page)
  $files = $client->beta->files->list();
  foreach ($files->data as $file) {
      echo "{$file->filename} - {$file->createdAt->format(DATE_ATOM)}\n";
  }

  // Delete a file
  $client->beta->files->delete($fileId);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new
  file_id = "file_011CNha8iCJcU1wXNR6q4V8w"

  # Get file metadata
  file_info = client.files.retrieve_metadata(file_id)
  puts "Filename: #{file_info.filename}, Size: #{file_info.size_bytes} bytes"

  # List all files
  client.files.list.auto_paging_each do |file|
    puts "#{file.filename} - #{file.created_at}"
  end

  # Delete a file
  client.files.delete(file_id)
  ```
</CodeGroup>

<Note>
  For complete details, see [Files API](https://platform.claude.com/docs/en/build-with-claude/files).
</Note>

### Multi-turn conversations

The response's `container` object carries the container's `id` and `expires_at` timestamp (see [Container reuse](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#container-reuse) for lifetime details). Reuse the same container across multiple messages by specifying the container ID:

<CodeGroup>
  ```bash cURL
  # Multi-turn container reuse doesn't translate well to a one-off shell
  # command; one of the SDK options would be a better fit. Capture
  # container.id from the first response, then pass it in the next request as
  # "container": {"id": "...", "skills": [...]} with the conversation history.
  ```

  ```bash CLI
  # First request creates container
  CONTAINER_ID=$(ant messages create \
    --transform container.id \
    --raw-output <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - {type: anthropic, skill_id: xlsx, version: latest}
  messages:
    - role: user
      content: Create a sample sales dataset and analyze it
  tools:
    - {type: code_execution_20250825, name: code_execution}
  YAML
  )

  # Continue conversation with same container
  ant messages create <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    id: $CONTAINER_ID  # Reuse container
    skills:
      - {type: anthropic, skill_id: xlsx, version: latest}
  messages:
    - role: user
      content: Create a sample sales dataset and analyze it
    - role: assistant
      content: []  # the assistant's text from the first response
    - role: user
      content: What was the total revenue?
  tools:
    - {type: code_execution_20250825, name: code_execution}
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # First request creates container
  response1 = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      container={
          "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
      },
      messages=[
          {"role": "user", "content": "Create a sample sales dataset and analyze it"}
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  # Continue conversation with same container
  messages = [
      {"role": "user", "content": "Create a sample sales dataset and analyze it"},
      {
          # Carry the assistant's text forward; container.id carries the execution state
          "role": "assistant",
          "content": "\n".join(
              block.text for block in response1.content if block.type == "text"
          ),
      },
      {"role": "user", "content": "What was the total revenue?"},
  ]

  response2 = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      container={
          "id": response1.container.id,  # Reuse container
          "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}],
      },
      messages=messages,
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // First request creates container
  const response1 = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [{ role: "user", content: "Create a sample sales dataset and analyze it" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Continue conversation with same container
  const messages: Anthropic.MessageParam[] = [
    { role: "user", content: "Create a sample sales dataset and analyze it" },
    {
      role: "assistant",
      // Carry the assistant's text forward; container.id carries the execution state
      content: response1.content
        .filter((block) => block.type === "text")
        .map((block) => block.text)
        .join("\n")
    },
    { role: "user", content: "What was the total revenue?" }
  ];

  const response2 = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      id: response1.container!.id, // Reuse container
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages,
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  // First request with a Skill
  var parameters1 = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Container = new ContainerParams
      {
          Skills =
          [
              new SkillParams
              {
                  Type = SkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Create a sample sales dataset and analyze it" }],
      Tools = [new CodeExecutionTool20250825()],
  };

  var response1 = await client.Messages.Create(parameters1);

  // Continue the conversation in the same container
  // Carry the assistant's text forward; container.id carries the execution state
  var assistantText = string.Join(
      "\n",
      response1.Content.Select(block => block.TryPickText(out var text) ? text.Text : null).Where(text => text is not null)
  );

  var parameters2 = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Container = new ContainerParams
      {
          ID = response1.Container!.ID,
          Skills =
          [
              new SkillParams
              {
                  Type = SkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
          ],
      },
      Messages =
      [
          new() { Role = Role.User, Content = "Create a sample sales dataset and analyze it" },
          new() { Role = Role.Assistant, Content = assistantText },
          new() { Role = Role.User, Content = "What was the total revenue?" },
      ],
      Tools = [new CodeExecutionTool20250825()],
  };

  var response2 = await client.Messages.Create(parameters2);
  Console.WriteLine(response2);
  ```

  ```go Go
  client := anthropic.NewClient()

  response1, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeAnthropic,
  					SkillID: "xlsx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Create a sample sales dataset and analyze it")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Carry the assistant's text forward; container.id carries the execution state
  var textParts []string
  for _, block := range response1.Content {
  	if block.Type == "text" {
  		textParts = append(textParts, block.Text)
  	}
  }
  assistantText := strings.Join(textParts, "\n")

  response2, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			ID: anthropic.String(response1.Container.ID), // Reuse container
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeAnthropic,
  					SkillID: "xlsx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Create a sample sales dataset and analyze it")),
  		{
  			Role:    anthropic.MessageParamRoleAssistant,
  			Content: []anthropic.ContentBlockParamUnion{anthropic.NewTextBlock(assistantText)},
  		},
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What was the total revenue?")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(response2)
  ```

  ```java Java
  import com.anthropic.models.messages.ContainerParams;
  import com.anthropic.models.messages.SkillParams;
  import com.anthropic.models.messages.CodeExecutionTool20250825;
  import com.anthropic.models.messages.ContentBlock;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params1 = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .container(ContainerParams.builder()
              .addSkill(SkillParams.builder()
                  .type(SkillParams.Type.ANTHROPIC)
                  .skillId("xlsx")
                  .version("latest")
                  .build())
              .build())
          .addUserMessage("Create a sample sales dataset and analyze it")
          .addTool(CodeExecutionTool20250825.builder().build())
          .build();

      Message response1 = client.messages().create(params1);

      MessageCreateParams params2 = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .container(ContainerParams.builder()
              .id(response1.container().get().id())
              .addSkill(SkillParams.builder()
                  .type(SkillParams.Type.ANTHROPIC)
                  .skillId("xlsx")
                  .version("latest")
                  .build())
              .build())
          .addUserMessage("Create a sample sales dataset and analyze it")
          // Carry the assistant's text forward; container.id carries the execution state
          .addAssistantMessage(response1.content().stream()
              .filter(ContentBlock::isText)
              .map(block -> block.asText().text())
              .collect(Collectors.joining("\n")))
          .addUserMessage("What was the total revenue?")
          .addTool(CodeExecutionTool20250825.builder().build())
          .build();

      Message response2 = client.messages().create(params2);
      System.out.println(response2);
  }
  ```

  ```php PHP
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  $client = new Client();

  $response1 = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Create a sample sales dataset and analyze it']
      ],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest']
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );

  $messages = [
      ['role' => 'user', 'content' => 'Create a sample sales dataset and analyze it'],
      // Carry the assistant's text forward; container.id carries the execution state
      ['role' => 'assistant', 'content' => implode("\n", array_map(
          fn ($block) => $block->text,
          array_filter($response1->content, fn ($block) => $block->type === 'text'),
      ))],
      ['role' => 'user', 'content' => 'What was the total revenue?']
  ];

  $response2 = $client->beta->messages->create(
      maxTokens: 4096,
      messages: $messages,
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'id' => $response1->container->id,
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest']
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );

  echo $response2;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response1 = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [
      { role: "user", content: "Create a sample sales dataset and analyze it" }
    ],
    tools: [
      { type: "code_execution_20250825", name: "code_execution" }
    ]
  )

  messages = [
    { role: "user", content: "Create a sample sales dataset and analyze it" },
    {
      # Carry the assistant's text forward; container.id carries the execution state
      role: "assistant",
      content: response1.content.filter_map { |block| block.text if block.type == :text }.join("\n")
    },
    { role: "user", content: "What was the total revenue?" }
  ]

  response2 = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      id: response1.container.id,
      skills: [
        { type: "anthropic", skill_id: "xlsx", version: "latest" }
      ]
    },
    messages: messages,
    tools: [
      { type: "code_execution_20250825", name: "code_execution" }
    ]
  )

  puts response2
  ```
</CodeGroup>

### Long-running operations

Skills may perform operations that require multiple turns. Handle `pause_turn` stop reasons:

<CodeGroup>
  ```bash cURL
  # Initial request
  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "latest"
          }
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Generate and process a large sample dataset"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }')

  # If stop_reason is "pause_turn", continue in the same container, appending
  # the prior response's content array to messages as the assistant turn.
  # Repeat this continuation request until stop_reason is no longer "pause_turn".
  STOP_REASON=$(echo "$RESPONSE" | jq -r '.stop_reason')
  CONTAINER_ID=$(echo "$RESPONSE" | jq -r '.container.id')

  RESPONSE=$(curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-opus-5\",
      \"max_tokens\": 4096,
      \"container\": {
        \"id\": \"$CONTAINER_ID\",
        \"skills\": [{
          \"type\": \"custom\",
          \"skill_id\": \"skill_01AbCdEfGhIjKlMnOpQrStUv\",
          \"version\": \"latest\"
        }]
      },
      \"messages\": [],
      \"tools\": [{
        \"type\": \"code_execution_20250825\",
        \"name\": \"code_execution\"
      }]
    }")
  ```

  ```bash CLI
  RESP=$(mktemp)

  # Initial request: capture the full JSON response to a temp file
  ant messages create > "$RESP" <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: latest
  messages:
    - role: user
      content: Generate and process a large sample dataset
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML

  # If stop_reason is "pause_turn", continue in the same container,
  # appending the prior response's content array to messages as the
  # assistant turn. Repeat until stop_reason is no longer "pause_turn".
  CONTAINER_ID=$(jq -r '.container.id' "$RESP")

  ant messages create > "$RESP" <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    id: $CONTAINER_ID
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: latest
  messages: [] # replace with conversation history + prior assistant content
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  messages = [{"role": "user", "content": "Generate and process a large sample dataset"}]
  max_retries = 10

  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      container={
          "skills": [
              {
                  "type": "custom",
                  "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  "version": "latest",
              }
          ]
      },
      messages=messages,
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  # Handle pause_turn for long operations
  for _ in range(max_retries):
      if response.stop_reason != "pause_turn":
          break

      messages.append({"role": "assistant", "content": response.content})
      response = client.messages.create(
          model="claude-opus-5",
          max_tokens=4096,
          container={
              "id": response.container.id,
              "skills": [
                  {
                      "type": "custom",
                      "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                      "version": "latest",
                  }
              ],
          },
          messages=messages,
          tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
      )
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const messages: Anthropic.MessageParam[] = [
    { role: "user", content: "Generate and process a large sample dataset" }
  ];
  const maxRetries = 10;

  let response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [{ type: "custom", skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv", version: "latest" }]
    },
    messages,
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Handle pause_turn for long operations
  for (let i = 0; i < maxRetries; i++) {
    if (response.stop_reason !== "pause_turn") {
      break;
    }

    messages.push({
      role: "assistant",
      content: response.content as Anthropic.ContentBlockParam[]
    });
    response = await client.messages.create({
      model: "claude-opus-5",
      max_tokens: 4096,
      container: {
        id: response.container!.id,
        skills: [
          { type: "custom", skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv", version: "latest" }
        ]
      },
      messages,
      tools: [{ type: "code_execution_20250825", name: "code_execution" }]
    });
  }
  ```

  ```csharp C#
  using System.Text.Json;
  // ...
  AnthropicClient client = new();

  List<MessageParam> messages =
  [
      new() { Role = Role.User, Content = "Generate and process a large sample dataset" },
  ];

  var maxRetries = 10;
  string? containerId = null;
  Message? response = null;

  for (var i = 0; i < maxRetries; i++)
  {
      var parameters = new MessageCreateParams
      {
          Model = "claude-opus-5",
          MaxTokens = 4096,
          Container = containerId is null
              ? new ContainerParams
              {
                  Skills =
                  [
                      new SkillParams
                      {
                          Type = SkillParamsType.Custom,
                          SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                          Version = "latest",
                      },
                  ],
              }
              : new ContainerParams
              {
                  ID = containerId,
                  Skills =
                  [
                      new SkillParams
                      {
                          Type = SkillParamsType.Custom,
                          SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                          Version = "latest",
                      },
                  ],
              },
          Messages = messages,
          Tools = [new CodeExecutionTool20250825()],
      };

      response = await client.Messages.Create(parameters);
      containerId = response.Container!.ID;

      if (response.StopReason != StopReason.PauseTurn)
      {
          break;
      }

      // Append the paused turn's content and continue
      var assistantContent = JsonSerializer.SerializeToElement(
          response.Content.Select(block => block.Json).ToArray()
      );
      messages.Add(new() { Role = Role.Assistant, Content = new MessageParamContent(assistantContent) });
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  messages := []anthropic.MessageParam{
  	anthropic.NewUserMessage(anthropic.NewTextBlock("Generate and process a large sample dataset")),
  }
  maxRetries := 10

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeCustom,
  					SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: messages,
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for i := 0; i < maxRetries; i++ {
  	if response.StopReason != anthropic.StopReasonPauseTurn {
  		break
  	}

  	messages = append(messages, response.ToParam())

  	response, err = client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     "claude-opus-5",
  		MaxTokens: 4096,
  		Container: anthropic.MessageCreateParamsContainerUnion{
  			OfContainers: &anthropic.ContainerParams{
  				ID: anthropic.String(response.Container.ID), // Reuse container
  				Skills: []anthropic.SkillParams{
  					{
  						Type:    anthropic.SkillParamsTypeCustom,
  						SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  						Version: anthropic.String("latest"),
  					},
  				},
  			},
  		},
  		Messages: messages,
  		Tools: []anthropic.ToolUnionParam{
  			{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}
  }

  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.ContainerParams;
  import com.anthropic.models.messages.SkillParams;
  import com.anthropic.models.messages.CodeExecutionTool20250825;
  import com.anthropic.models.messages.StopReason;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      List<MessageParam> messages = new ArrayList<>();
      messages.add(
          MessageParam.builder()
              .role(MessageParam.Role.USER)
              .content("Generate and process a large sample dataset")
              .build()
      );
      int maxRetries = 10;

      Message response = client.messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5)
              .maxTokens(4096L)
              .container(ContainerParams.builder()
                  .addSkill(SkillParams.builder()
                      .type(SkillParams.Type.CUSTOM)
                      .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                      .version("latest")
                      .build())
                  .build())
              .messages(messages)
              .addTool(CodeExecutionTool20250825.builder().build())
              .build());

      for (int i = 0; i < maxRetries; i++) {
          if (!response.stopReason().isPresent()
                  || !response.stopReason().get().equals(StopReason.PAUSE_TURN)) {
              break;
          }

          messages.add(response.toParam());

          response = client.messages().create(
              MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5)
                  .maxTokens(4096L)
                  .container(ContainerParams.builder()
                      .id(response.container().get().id())
                      .addSkill(SkillParams.builder()
                          .type(SkillParams.Type.CUSTOM)
                          .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                          .version("latest")
                          .build())
                      .build())
                  .messages(messages)
                  .addTool(CodeExecutionTool20250825.builder().build())
                  .build());
      }
  }
  ```

  ```php PHP
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  $client = new Client();

  $messages = [
      ['role' => 'user', 'content' => 'Generate and process a large sample dataset']
  ];
  $maxRetries = 10;

  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: $messages,
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [
              [
                  'type' => 'custom',
                  'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
                  'version' => 'latest'
              ]
          ]
      ],
      tools: [['type' => 'code_execution_20250825', 'name' => 'code_execution']]
  );

  for ($i = 0; $i < $maxRetries; $i++) {
      if ($response->stopReason !== 'pause_turn') {
          break;
      }

      $messages[] = ['role' => 'assistant', 'content' => $response->content];

      $response = $client->beta->messages->create(
          maxTokens: 4096,
          messages: $messages,
          model: 'claude-opus-5',
          betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
          container: [
              'id' => $response->container->id,
              'skills' => [
                  [
                      'type' => 'custom',
                      'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
                      'version' => 'latest'
                  ]
              ]
          ],
          tools: [['type' => 'code_execution_20250825', 'name' => 'code_execution']]
      );
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  messages = [
    { role: "user", content: "Generate and process a large sample dataset" }
  ]
  max_retries = 10

  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [
        {
          type: "custom",
          skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
          version: "latest"
        }
      ]
    },
    messages: messages,
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )

  max_retries.times do
    break if response.stop_reason != :pause_turn

    messages << { role: "assistant", content: response.content }

    response = client.messages.create(
      model: "claude-opus-5",
      max_tokens: 4096,
      container: {
        id: response.container.id,
        skills: [
          {
            type: "custom",
            skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
            version: "latest"
          }
        ]
      },
      messages: messages,
      tools: [{ type: "code_execution_20250825", name: "code_execution" }]
    )
  end
  ```
</CodeGroup>

<Note>
  The response may include a `pause_turn` stop reason, which indicates that the API paused a long-running Skill operation. You can provide the response back as-is in a subsequent request to let Claude continue its turn, or modify the content if you want to interrupt the conversation and provide additional guidance.
</Note>

### Using multiple Skills

Combine multiple Skills in a single request to handle complex workflows:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {
            "type": "anthropic",
            "skill_id": "xlsx",
            "version": "latest"
          },
          {
            "type": "anthropic",
            "skill_id": "pptx",
            "version": "latest"
          },
          {
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "latest"
          }
        ]
      },
      "messages": [{
        "role": "user",
        "content": "Analyze sales data and create a presentation"
      }],
      "tools": [{
        "type": "code_execution_20250825",
        "name": "code_execution"
      }]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: anthropic
        skill_id: xlsx
        version: latest
      - type: anthropic
        skill_id: pptx
        version: latest
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: latest
  messages:
    - role: user
      content: Analyze sales data and create a presentation
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
              {"type": "anthropic", "skill_id": "pptx", "version": "latest"},
              {
                  "type": "custom",
                  "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  "version": "latest",
              },
          ]
      },
      messages=[
          {"role": "user", "content": "Analyze sales data and create a presentation"}
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [
        {
          type: "anthropic",
          skill_id: "xlsx",
          version: "latest"
        },
        {
          type: "anthropic",
          skill_id: "pptx",
          version: "latest"
        },
        {
          type: "custom",
          skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
          version: "latest"
        }
      ]
    },
    messages: [
      {
        role: "user",
        content: "Analyze sales data and create a presentation"
      }
    ],
    tools: [
      {
        type: "code_execution_20250825",
        name: "code_execution"
      }
    ]
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Container = new ContainerParams
      {
          Skills =
          [
              new SkillParams
              {
                  Type = SkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
              new SkillParams
              {
                  Type = SkillParamsType.Anthropic,
                  SkillID = "pptx",
                  Version = "latest",
              },
              new SkillParams
              {
                  Type = SkillParamsType.Custom,
                  SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Analyze sales data and create a presentation" }],
      Tools = [new CodeExecutionTool20250825()],
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeAnthropic,
  					SkillID: "xlsx",
  					Version: anthropic.String("latest"),
  				},
  				{
  					Type:    anthropic.SkillParamsTypeAnthropic,
  					SkillID: "pptx",
  					Version: anthropic.String("latest"),
  				},
  				{
  					Type:    anthropic.SkillParamsTypeCustom,
  					SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze sales data and create a presentation")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.ContainerParams;
  import com.anthropic.models.messages.SkillParams;
  import com.anthropic.models.messages.CodeExecutionTool20250825;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .container(ContainerParams.builder()
              .skills(List.of(
                  SkillParams.builder()
                      .type(SkillParams.Type.ANTHROPIC)
                      .skillId("xlsx")
                      .version("latest")
                      .build(),
                  SkillParams.builder()
                      .type(SkillParams.Type.ANTHROPIC)
                      .skillId("pptx")
                      .version("latest")
                      .build(),
                  SkillParams.builder()
                      .type(SkillParams.Type.CUSTOM)
                      .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                      .version("latest")
                      .build()
              ))
              .build())
          .addUserMessage("Analyze sales data and create a presentation")
          .addTool(CodeExecutionTool20250825.builder().build())
          .build();

      Message response = client.messages().create(params);
      System.out.println(response);
  }
  ```

  ```php PHP
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Analyze sales data and create a presentation']
      ],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [
              [
                  'type' => 'anthropic',
                  'skill_id' => 'xlsx',
                  'version' => 'latest'
              ],
              [
                  'type' => 'anthropic',
                  'skill_id' => 'pptx',
                  'version' => 'latest'
              ],
              [
                  'type' => 'custom',
                  'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
                  'version' => 'latest'
              ]
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );

  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [
        {
          type: "anthropic",
          skill_id: "xlsx",
          version: "latest"
        },
        {
          type: "anthropic",
          skill_id: "pptx",
          version: "latest"
        },
        {
          type: "custom",
          skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
          version: "latest"
        }
      ]
    },
    messages: [
      { role: "user", content: "Analyze sales data and create a presentation" }
    ],
    tools: [
      { type: "code_execution_20250825", name: "code_execution" }
    ]
  )
  puts message
  ```
</CodeGroup>

***

## Managing custom Skills

<Warning id="workspace-scoped-access">
  **Custom Skills are accessible to your entire workspace, not scoped to an end user, conversation, or session.** Any API key in the same workspace can read, invoke, and delete every custom Skill uploaded there, and all of your keys share your organization's Default Workspace unless you have assigned them to separate [workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces#api-keys-and-resource-scoping).

  If you are building a multi-tenant platform on the Skills API, create a separate [workspace](https://platform.claude.com/docs/en/manage-claude/workspaces) for each tenant. The workspace is the isolation boundary for custom Skills, so a workspace per tenant gives each tenant's Skills hard isolation from every other tenant. Each organization can have up to 100 workspaces by default (see [How workspaces work](https://platform.claude.com/docs/en/manage-claude/workspaces#how-workspaces-work)); if you need more for tenant isolation, contact your account team.
</Warning>

### Creating a Skill

A Skill bundle is a directory containing a `SKILL.md` file at the top level with `name` and `description` YAML frontmatter, plus any supporting scripts or resources. See [Get started with Agent Skills in the API](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart) to author one, and the **Requirements** list following the examples for the full constraints.

Upload your custom Skill to make it available in your workspace. You can upload a zip archive or individual file objects. The Python SDK also provides a `files_from_dir` helper that accepts a directory path.

Files are identified by the filename you attach (the `;filename=` suffix in the cURL example and the filename arguments in the SDK examples). For the walkthrough's skill, create a zip with `zip -r financial_skill.zip financial_skill/` and substitute it for the `example_skill.zip` placeholder in the zip-upload options.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -F "files[]=@financial_skill/SKILL.md;filename=financial_skill/SKILL.md" \
    -F "files[]=@financial_skill/analyze.py;filename=financial_skill/analyze.py"
  ```

  <MultiFileExample language="cli" label="CLI">
    ```bash CLI
    zip -r financial_skill.zip financial_skill/
    ant skills create --file financial_skill.zip
    ```

    <File filename="financial_skill/SKILL.md">
      ```markdown
      ---
      name: financial-skill
      description: Docs example skill.
      ---
      ```
    </File>

    <File filename="financial_skill/analyze.py">
      ```python
      print("financial analysis helper")
      ```
    </File>
  </MultiFileExample>

  ```python Python
  from anthropic.lib import files_from_dir

  client = anthropic.Anthropic()

  # Option 1: Using a zip file
  skill = client.skills.create(
      files=[open("example_skill.zip", "rb")],
  )

  # Option 2: Using file tuples (filename, file_content, mime_type)
  skill = client.skills.create(
      files=[
          (
              "financial_skill/SKILL.md",
              open("financial_skill/SKILL.md", "rb"),
              "text/markdown",
          ),
          (
              "financial_skill/analyze.py",
              open("financial_skill/analyze.py", "rb"),
              "text/x-python",
          ),
      ],
  )

  # Option 3: Using the files_from_dir helper (Python only)
  skill = client.skills.create(
      files=files_from_dir("financial_skill"),
  )

  print(f"Created skill: {skill.id}")
  print(f"Latest version: {skill.latest_version_id}")
  ```

  ```typescript TypeScript
  import { toFile } from "@anthropic-ai/sdk";
  import fs from "node:fs";
  // ...

  const client = new Anthropic();

  // Option 1: Using a zip file
  const skillFromZip = await client.skills.create({
    files: [await toFile(fs.createReadStream("example_skill.zip"), "example_skill.zip")]
  });

  // Option 2: Using individual file objects
  const skill = await client.skills.create({
    files: [
      await toFile(fs.createReadStream("financial_skill/SKILL.md"), "financial_skill/SKILL.md", {
        type: "text/markdown"
      }),
      await toFile(
        fs.createReadStream("financial_skill/analyze.py"),
        "financial_skill/analyze.py",
        { type: "text/x-python" }
      )
    ]
  });

  console.log(`Created skill: ${skill.id}`);
  console.log(`Latest version: ${skill.latest_version_id}`);
  ```

  ```csharp C#
  using Anthropic.Core;
  // ...

  AnthropicClient client = new();

  // Option 1: Using a zip file
  var parameters = new SkillCreateParams
  {
      Files = [File.OpenRead("example_skill.zip")],
  };

  var skill = await client.Skills.Create(parameters);

  // Option 2: Using individual files (path-qualified filenames preserve the Skill's directory layout)
  var parameters2 = new SkillCreateParams
  {
      Files =
      [
          new BinaryContent
          {
              Stream = File.OpenRead("financial_skill/SKILL.md"),
              FileName = "financial_skill/SKILL.md",
          },
          new BinaryContent
          {
              Stream = File.OpenRead("financial_skill/analyze.py"),
              FileName = "financial_skill/analyze.py",
          },
      ],
  };

  var skill2 = await client.Skills.Create(parameters2);

  Console.WriteLine($"Created skill: {skill.ID}");
  Console.WriteLine($"Latest version: {skill.LatestVersionID}");
  Console.WriteLine($"Created skill 2: {skill2.ID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  // Option 1: Using a zip file
  zipFile, err := os.Open("example_skill.zip")
  if err != nil {
  	log.Fatal(err)
  }
  defer zipFile.Close()

  skill, err := client.Skills.New(context.TODO(), anthropic.SkillNewParams{
  	Files: []io.Reader{zipFile},
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Option 2: Using individual files
  skillMd, err := os.Open("financial_skill/SKILL.md")
  if err != nil {
  	log.Fatal(err)
  }
  defer skillMd.Close()

  analyzePy, err := os.Open("financial_skill/analyze.py")
  if err != nil {
  	log.Fatal(err)
  }
  defer analyzePy.Close()

  skill2, err := client.Skills.New(context.TODO(), anthropic.SkillNewParams{
  	Files: []io.Reader{
  		anthropic.File(skillMd, "financial_skill/SKILL.md", "text/markdown"),
  		anthropic.File(analyzePy, "financial_skill/analyze.py", "text/x-python"),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("Created skill: %s\n", skill.ID)
  fmt.Printf("Latest version: %s\n", skill.LatestVersionID)
  fmt.Printf("Created skill 2: %s\n", skill2.ID)
  ```

  ```java Java
  import com.anthropic.core.MultipartField;
  import com.anthropic.models.skills.SkillCreateParams;
  import com.anthropic.models.skills.Skill;
  // ...
  void main() throws Exception {
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Option 1: Using a zip file
      SkillCreateParams params = SkillCreateParams.builder()
          .addFile(MultipartField.<InputStream>builder()
              .value(Files.newInputStream(Path.of("example_skill.zip")))
              .filename("example_skill.zip")
              .contentType("application/zip")
              .build())
          .build();

      Skill skill = client.skills().create(params);

      // Option 2: Using individual files (path-qualified filenames preserve the Skill's directory layout)
      SkillCreateParams params2 = SkillCreateParams.builder()
          .addFile(MultipartField.<InputStream>builder()
              .value(Files.newInputStream(Path.of("financial_skill/SKILL.md")))
              .filename("financial_skill/SKILL.md")
              .contentType("text/markdown")
              .build())
          .addFile(MultipartField.<InputStream>builder()
              .value(Files.newInputStream(Path.of("financial_skill/analyze.py")))
              .filename("financial_skill/analyze.py")
              .contentType("text/x-python")
              .build())
          .build();

      Skill skill2 = client.skills().create(params2);

      System.out.println("Created skill: " + skill.id());
      System.out.println("Latest version: " + skill.latestVersionId());
      System.out.println("Created skill 2: " + skill2.id());
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Skills API under the beta namespace; field names can differ from other SDKs.
  use Anthropic\Core\FileParam;
  // ...

  $client = new Client();

  // Option 1: Using a zip file
  $skill = $client->beta->skills->create(
      files: [
          FileParam::fromResource(fopen('example_skill.zip', 'r'))
      ],
  );

  // Option 2: Using individual files
  $skill = $client->beta->skills->create(
      files: [
          FileParam::fromResource(fopen('financial_skill/SKILL.md', 'r'), 'financial_skill/SKILL.md', 'text/markdown'),
          FileParam::fromResource(fopen('financial_skill/analyze.py', 'r'), 'financial_skill/analyze.py', 'text/x-python')
      ],
  );

  echo "Created skill: {$skill->id}\n";
  echo "Latest version: {$skill->latestVersion}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Option 1: Using a zip file
  skill = client.skills.create(
    files: [
      File.open("example_skill.zip", "rb")
    ]
  )

  # Option 2: Using individual files
  skill = client.skills.create(
    files: [
      Anthropic::FilePart.new(
        Pathname("financial_skill/SKILL.md"),
        filename: "financial_skill/SKILL.md",
        content_type: "text/markdown"
      ),
      Anthropic::FilePart.new(
        Pathname("financial_skill/analyze.py"),
        filename: "financial_skill/analyze.py",
        content_type: "text/x-python"
      )
    ]
  )

  puts "Created skill: #{skill.id}"
  puts "Latest version: #{skill.latest_version_id}"
  ```
</CodeGroup>

**Requirements:**

* Must include a `SKILL.md` file at the upload root (or at the top of a single enclosing folder)

* `display_name` is optional: when omitted, it derives from the `SKILL.md` `name`; an explicit value may be up to 255 characters and does not need to be unique within the workspace

* Total upload size must be under 30 MB (uncompressed)

* YAML frontmatter requirements:

  * `name`: Maximum 64 characters, lowercase letters/numbers/hyphens only, no XML tags, no reserved words ("anthropic", "claude")
  * `description`: Maximum 1024 characters, non-empty, no XML tags

For complete request/response schemas, see the [Create Skill API reference](https://platform.claude.com/docs/en/api/skills/create).

### Listing Skills

Retrieve all Skills available to your workspace, including both Anthropic pre-built Skills and your custom Skills. Use the `source` parameter to filter by skill type:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  # List all Skills
  curl "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"

  # List only custom Skills
  curl "https://api.anthropic.com/v1/skills?source=custom" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  # List all Skills
  ant skills list

  # List only custom Skills
  ant skills list --source custom
  ```

  ```python Python
  client = anthropic.Anthropic()

  # List all Skills
  for skill in client.skills.list():
      print(f"{skill.id}: {skill.display_name} (source: {skill.source.type})")

  # List only custom Skills
  custom_skills = client.skills.list(source="custom")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // List all Skills
  for await (const skill of client.skills.list()) {
    console.log(`${skill.id}: ${skill.display_name} (source: ${skill.source.type})`);
  }

  // List only custom Skills
  const customSkills = await client.skills.list({
    source: "custom"
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  // List all Skills
  await foreach (var skill in (await client.Skills.List()).Paginate())
  {
      Console.WriteLine($"{skill.ID}: {skill.DisplayName} (source: {skill.Source.Type})");
  }

  // List only custom Skills
  var customSkills = await client.Skills.List(new SkillListParams { Source = "custom" });
  ```

  ```go Go
  client := anthropic.NewClient()

  // List all Skills
  skills := client.Skills.ListAutoPaging(context.TODO(), anthropic.SkillListParams{})

  for skills.Next() {
  	skill := skills.Current()
  	fmt.Printf("%s: %s (source: %s)\n", skill.ID, skill.DisplayName, skill.Source.Type)
  }
  if skills.Err() != nil {
  	log.Fatal(skills.Err())
  }

  // List only custom Skills
  customSkills := client.Skills.ListAutoPaging(context.TODO(), anthropic.SkillListParams{
  	Source: anthropic.String("custom"),
  })

  for customSkills.Next() {
  	skill := customSkills.Current()
  	fmt.Printf("%s: %s (source: %s)\n", skill.ID, skill.DisplayName, skill.Source.Type)
  }
  if customSkills.Err() != nil {
  	log.Fatal(customSkills.Err())
  }
  ```

  ```java Java
  import com.anthropic.models.skills.SkillListParams;
  import com.anthropic.models.skills.SkillListPage;
  import com.anthropic.models.skills.Skill;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // List Skills (first page)
      SkillListPage skills = client.skills().list();

      for (Skill skill : skills.data()) {
          System.out.println(skill.id() + ": " + skill.displayName() + " (source: " + skill.source().type() + ")");
      }

      // List only custom Skills
      SkillListParams customParams = SkillListParams.builder()
          .source("custom")
          .build();

      SkillListPage customSkills = client.skills().list(customParams);
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Skills API under the beta namespace; field names can differ from other SDKs.
  $client = new Client();

  // List Skills (first page)
  $skills = $client->beta->skills->list();

  foreach ($skills->data as $skill) {
      echo "{$skill->id}: {$skill->displayTitle} (source: {$skill->source})\n";
  }

  // List only custom Skills
  $customSkills = $client->beta->skills->list(
      source: 'custom',
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # List all Skills
  client.skills.list.auto_paging_each do |skill|
    puts "#{skill.id}: #{skill.display_name} (source: #{skill.source.type})"
  end

  # List only custom Skills
  custom_skills = client.skills.list(
    source: "custom"
  )
  ```
</CodeGroup>

See the [List Skills API reference](https://platform.claude.com/docs/en/api/skills/list) for pagination and filtering options.

### Retrieving a Skill

Get details about a specific Skill:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant skills retrieve \
    --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv
  ```

  ```python Python
  client = anthropic.Anthropic()

  skill = client.skills.retrieve(skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv")

  print(f"Skill: {skill.display_name}")
  print(f"Latest version: {skill.latest_version_id}")
  print(f"Created: {skill.created_at}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const skill = await client.skills.retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv");

  console.log(`Skill: ${skill.display_name}`);
  console.log(`Latest version: ${skill.latest_version_id}`);
  console.log(`Created: ${skill.created_at}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var skill = await client.Skills.Retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv");

  Console.WriteLine($"Skill: {skill.DisplayName}");
  Console.WriteLine($"Latest version: {skill.LatestVersionID}");
  Console.WriteLine($"Created: {skill.CreatedAt}");
  ```

  ```go Go
  client := anthropic.NewClient()

  skill, err := client.Skills.Get(
  	context.TODO(),
  	"skill_01AbCdEfGhIjKlMnOpQrStUv",
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("Skill: %s\n", skill.DisplayName)
  fmt.Printf("Latest version: %s\n", skill.LatestVersionID)
  fmt.Printf("Created: %s\n", skill.CreatedAt)
  ```

  ```java Java
  import com.anthropic.models.skills.Skill;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Skill skill = client.skills().retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv");

      System.out.println("Skill: " + skill.displayName());
      System.out.println("Latest version: " + skill.latestVersionId());
      System.out.println("Created: " + skill.createdAt());
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Skills API under the beta namespace; field names can differ from other SDKs.
  $client = new Client();

  $skill = $client->beta->skills->retrieve(
      skillID: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
  );

  echo "Skill: " . $skill->displayTitle . "\n";
  echo "Latest version: " . $skill->latestVersion . "\n";
  echo "Created: " . $skill->createdAt . "\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  skill = client.skills.retrieve("skill_01AbCdEfGhIjKlMnOpQrStUv")

  puts "Skill: #{skill.display_name}"
  puts "Latest version: #{skill.latest_version_id}"
  puts "Created: #{skill.created_at}"
  ```
</CodeGroup>

### Deleting a Skill

Deleting a Skill also removes all of its versions.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant skills delete \
    --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv >/dev/null
  ```

  ```python Python
  client = anthropic.Anthropic()

  client.skills.delete(skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  await client.skills.delete("skill_01AbCdEfGhIjKlMnOpQrStUv");
  ```

  ```csharp C#
  AnthropicClient client = new();

  await client.Skills.Delete("skill_01AbCdEfGhIjKlMnOpQrStUv");
  ```

  ```go Go
  client := anthropic.NewClient()

  _, err := client.Skills.Delete(
  	context.TODO(),
  	"skill_01AbCdEfGhIjKlMnOpQrStUv",
  )
  if err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      client.skills().delete("skill_01AbCdEfGhIjKlMnOpQrStUv");
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Skills API under the beta namespace; field names can differ from other SDKs.
  $client = new Client();

  // In the beta namespace, a Skill's versions must be deleted before the Skill itself.
  $skillId = 'skill_01AbCdEfGhIjKlMnOpQrStUv';
  foreach ($client->beta->skills->versions->list($skillId)->pagingEachItem() as $version) {
      $client->beta->skills->versions->delete($version->version, skillID: $skillId);
  }
  $client->beta->skills->delete($skillId);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  client.skills.delete("skill_01AbCdEfGhIjKlMnOpQrStUv")
  ```
</CodeGroup>

### Versioning

Skills support versioning to manage updates safely:

**Anthropic Skills:**

* Versions use date format: `20251013`
* New versions released as updates are made
* Specify exact versions for stability

**Custom Skills:**

* Auto-generated version IDs: `skver_01AbCdEfGhIjKlMnOpQrStUv`
* Use `"latest"` to always get the most recent version
* Create new versions when updating Skill files

A new version is a complete snapshot, not a delta: upload the Skill's full file set each time. Files you omit are not carried over, and the `name` in the new version's `SKILL.md` must match the Skill's existing name. The following examples re-upload the complete `financial_skill/` bundle from [Creating a Skill](https://platform.claude.com/docs/en/build-with-claude/skills-guide#creating-a-skill).

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  # Create a new version
  NEW_VERSION=$(curl -X POST "https://api.anthropic.com/v1/skills/skill_01AbCdEfGhIjKlMnOpQrStUv/versions" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -F "files[]=@financial_skill/SKILL.md;filename=financial_skill/SKILL.md" \
    -F "files[]=@financial_skill/analyze.py;filename=financial_skill/analyze.py")

  VERSION_ID=$(echo "$NEW_VERSION" | jq -r '.id')

  # Use specific version
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-opus-5\",
      \"max_tokens\": 4096,
      \"container\": {
        \"skills\": [{
          \"type\": \"custom\",
          \"skill_id\": \"skill_01AbCdEfGhIjKlMnOpQrStUv\",
          \"version\": \"$VERSION_ID\"
        }]
      },
      \"messages\": [{\"role\": \"user\", \"content\": \"Use updated Skill\"}],
      \"tools\": [{\"type\": \"code_execution_20250825\", \"name\": \"code_execution\"}]
    }"

  # Use latest version
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [{
          "type": "custom",
          "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
          "version": "latest"
        }]
      },
      "messages": [{"role": "user", "content": "Use latest Skill version"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'
  ```

  ```bash CLI
  # Create a new version
  VERSION_ID=$(ant skills:versions create \
    --skill-id skill_01AbCdEfGhIjKlMnOpQrStUv \
    --file financial_skill.zip \
    --transform id \
    --raw-output)

  # Use specific version
  ant messages create <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: "$VERSION_ID"
  messages:
    - role: user
      content: Use updated Skill
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML

  # Use latest version
  ant messages create <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: latest
  messages:
    - role: user
      content: Use latest Skill version
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  from anthropic.lib import files_from_dir

  client = anthropic.Anthropic()

  # Create a new version

  new_version = client.skills.versions.create(
      skill_id="skill_01AbCdEfGhIjKlMnOpQrStUv",
      files=files_from_dir("financial_skill"),
  )

  # Use specific version
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      container={
          "skills": [
              {
                  "type": "custom",
                  "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  "version": new_version.id,
              }
          ]
      },
      messages=[{"role": "user", "content": "Use updated Skill"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  # Use latest version
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      container={
          "skills": [
              {
                  "type": "custom",
                  "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  "version": "latest",
              }
          ]
      },
      messages=[{"role": "user", "content": "Use latest Skill version"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  import fs from "node:fs";

  const client = new Anthropic();

  // Create a new version from a zip of the complete financial_skill/ bundle
  const newVersion = await client.skills.versions.create("skill_01AbCdEfGhIjKlMnOpQrStUv", {
    files: [fs.createReadStream("financial_skill.zip")]
  });

  // Use specific version
  const specificVersionResponse = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [
        {
          type: "custom",
          skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
          version: newVersion.id
        }
      ]
    },
    messages: [{ role: "user", content: "Use updated Skill" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Use latest version
  const latestVersionResponse = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [
        {
          type: "custom",
          skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
          version: "latest"
        }
      ]
    },
    messages: [{ role: "user", content: "Use latest Skill version" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });
  ```

  ```csharp C#
  using Anthropic.Core;
  using Anthropic.Models.Skills.Versions;
  // ...
  AnthropicClient client = new();

  // Create a new version
  var versionParams = new VersionCreateParams
  {
      Files =
      [
          new BinaryContent
          {
              Stream = File.OpenRead("financial_skill/SKILL.md"),
              FileName = "financial_skill/SKILL.md",
          },
          new BinaryContent
          {
              Stream = File.OpenRead("financial_skill/analyze.py"),
              FileName = "financial_skill/analyze.py",
          },
      ],
  };

  var newVersion = await client.Skills.Versions.Create("skill_01AbCdEfGhIjKlMnOpQrStUv", versionParams);

  // Use specific version
  var specificVersionParams = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Container = new ContainerParams
      {
          Skills =
          [
              new SkillParams
              {
                  Type = SkillParamsType.Custom,
                  SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  Version = newVersion.ID,
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Use updated Skill" }],
      Tools = [new CodeExecutionTool20250825()],
  };

  var response = await client.Messages.Create(specificVersionParams);
  Console.WriteLine(response);

  // Use latest version
  var latestVersionParams = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Container = new ContainerParams
      {
          Skills =
          [
              new SkillParams
              {
                  Type = SkillParamsType.Custom,
                  SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Use latest Skill version" }],
      Tools = [new CodeExecutionTool20250825()],
  };

  var latestResponse = await client.Messages.Create(latestVersionParams);
  Console.WriteLine(latestResponse);
  ```

  ```go Go
  client := anthropic.NewClient()

  // Create a new version
  skillMd, err := os.Open("financial_skill/SKILL.md")
  if err != nil {
  	log.Fatal(err)
  }
  defer skillMd.Close()
  analyzePy, err := os.Open("financial_skill/analyze.py")
  if err != nil {
  	log.Fatal(err)
  }
  defer analyzePy.Close()

  newVersion, err := client.Skills.Versions.New(
  	context.TODO(),
  	"skill_01AbCdEfGhIjKlMnOpQrStUv",
  	anthropic.SkillVersionNewParams{
  		Files: []io.Reader{
  			anthropic.File(skillMd, "financial_skill/SKILL.md", "text/markdown"),
  			anthropic.File(analyzePy, "financial_skill/analyze.py", "text/x-python"),
  		},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  // Use specific version
  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeCustom,
  					SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  					Version: anthropic.String(newVersion.ID),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Use updated Skill")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)

  // Use latest version
  latestResponse, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeCustom,
  					SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Use latest Skill version")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(latestResponse)
  ```

  ```java Java
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.Model;
  import com.anthropic.core.MultipartField;
  import com.anthropic.models.messages.ContainerParams;
  import com.anthropic.models.messages.SkillParams;
  import com.anthropic.models.messages.CodeExecutionTool20250825;
  import com.anthropic.models.skills.versions.VersionCreateParams;
  import com.anthropic.models.skills.versions.SkillVersion;
  import java.io.InputStream;
  import java.nio.file.Files;
  import java.nio.file.Path;

  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Create a new version from a zip of the complete financial_skill/ bundle
  VersionCreateParams versionParams = VersionCreateParams.builder()
      .addFile(MultipartField.<InputStream>builder()
          .value(Files.newInputStream(Path.of("financial_skill.zip")))
          .filename("financial_skill.zip")
          .contentType("application/zip")
          .build())
      .build();

  SkillVersion newVersion = client.skills().versions()
      .create("skill_01AbCdEfGhIjKlMnOpQrStUv", versionParams);

  // Use specific version
  MessageCreateParams specificVersionParams = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(4096L)
      .container(ContainerParams.builder()
          .addSkill(SkillParams.builder()
              .type(SkillParams.Type.CUSTOM)
              .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
              .version(newVersion.id())
              .build())
          .build())
      .addUserMessage("Use updated Skill")
      .addTool(CodeExecutionTool20250825.builder().build())
      .build();

  Message response = client.messages().create(specificVersionParams);
  System.out.println(response);

  // Use latest version
  MessageCreateParams latestVersionParams = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(4096L)
      .container(ContainerParams.builder()
          .addSkill(SkillParams.builder()
              .type(SkillParams.Type.CUSTOM)
              .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
              .version("latest")
              .build())
          .build())
      .addUserMessage("Use latest Skill version")
      .addTool(CodeExecutionTool20250825.builder().build())
      .build();

  Message latestResponse = client.messages().create(latestVersionParams);
  System.out.println(latestResponse);
  ```

  ```php PHP
  // The PHP SDK exposes the Skills API under the beta namespace; field names can differ from other SDKs.
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  use Anthropic\Core\FileParam;

  // ...
  $client = new Client();

  // Create a new version
  $newVersion = $client->beta->skills->versions->create(
      skillID: 'skill_01AbCdEfGhIjKlMnOpQrStUv',
      files: [
          FileParam::fromResource(fopen('financial_skill/SKILL.md', 'r'), 'financial_skill/SKILL.md', 'text/markdown'),
          FileParam::fromResource(fopen('financial_skill/analyze.py', 'r'), 'financial_skill/analyze.py', 'text/x-python'),
      ],
  );

  // Use specific version
  $response = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [['role' => 'user', 'content' => 'Use updated Skill']],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [[
              'type' => 'custom',
              'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
              'version' => $newVersion->version
          ]]
      ],
      tools: [['type' => 'code_execution_20250825', 'name' => 'code_execution']]
  );
  echo $response;

  // Use latest version
  $latestResponse = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [['role' => 'user', 'content' => 'Use latest Skill version']],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [[
              'type' => 'custom',
              'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
              'version' => 'latest'
          ]]
      ],
      tools: [['type' => 'code_execution_20250825', 'name' => 'code_execution']]
  );
  echo $latestResponse;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Create a new version
  new_version = client.skills.versions.create(
    "skill_01AbCdEfGhIjKlMnOpQrStUv",
    files: [
      Anthropic::FilePart.new(
        Pathname("financial_skill/SKILL.md"),
        filename: "financial_skill/SKILL.md",
        content_type: "text/markdown"
      ),
      Anthropic::FilePart.new(
        Pathname("financial_skill/analyze.py"),
        filename: "financial_skill/analyze.py",
        content_type: "text/x-python"
      )
    ]
  )

  # Use specific version
  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [{
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: new_version.id
      }]
    },
    messages: [{ role: "user", content: "Use updated Skill" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )
  puts response

  # Use latest version
  latest_response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [{
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: "latest"
      }]
    },
    messages: [{ role: "user", content: "Use latest Skill version" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )
  puts latest_response
  ```
</CodeGroup>

See the [Create Skill Version API reference](https://platform.claude.com/docs/en/api/skills/versions/create) for complete details.

***

## How Skills are loaded

When you specify Skills in a container:

1. **Metadata discovery:** Claude sees metadata for each Skill (name, description) in the system prompt.
2. **File loading:** Skill files are copied into the container at `/skills/{skill-name}/`. The directory is the Skill's name (`pptx` for an Anthropic Skill, the `SKILL.md` `name` for a custom Skill), not its `skill_01...` ID.
3. **Automatic use:** Claude automatically loads and uses Skills when relevant to your request.
4. **Composition:** Multiple Skills compose together for complex workflows.

Claude loads full Skill instructions only when needed.

***

## Use cases

Skills fit both organizational and personal work. Organizations use them to apply brand formatting to documents, structure notes and reports around company templates, and run company-specific analytical procedures. Individuals use them for custom document templates, specialized data pipelines, and code generation or deployment conventions.

### Example: financial modeling

Combine Excel and custom DCF analysis Skills:

<CodeGroup>
  ```bash cURL
  # Create custom DCF analysis Skill
  DCF_SKILL=$(curl -X POST "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -F "files[]=@dcf_skill/SKILL.md;filename=dcf_skill/SKILL.md")

  DCF_SKILL_ID=$(echo "$DCF_SKILL" | jq -r '.id')

  # Use with Excel to create financial model
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-opus-5\",
      \"max_tokens\": 4096,
      \"container\": {
        \"skills\": [
          {
            \"type\": \"anthropic\",
            \"skill_id\": \"xlsx\",
            \"version\": \"latest\"
          },
          {
            \"type\": \"custom\",
            \"skill_id\": \"$DCF_SKILL_ID\",
            \"version\": \"latest\"
          }
        ]
      },
      \"messages\": [{
        \"role\": \"user\",
        \"content\": \"Build a DCF valuation model for a SaaS company\"
      }],
      \"tools\": [{
        \"type\": \"code_execution_20250825\",
        \"name\": \"code_execution\"
      }]
    }"
  ```

  ```bash CLI
  # Create custom DCF analysis Skill
  DCF_SKILL_ID=$(ant skills create \
    --file dcf_skill.zip \
    --transform id \
    --raw-output)

  # Use with Excel to create financial model
  ant messages create <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: anthropic
        skill_id: xlsx
        version: latest
      - type: custom
        skill_id: $DCF_SKILL_ID
        version: latest
  messages:
    - role: user
      content: Build a DCF valuation model for a SaaS company
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  from anthropic.lib import files_from_dir

  client = anthropic.Anthropic()

  # Create custom DCF analysis Skill

  dcf_skill = client.skills.create(
      files=files_from_dir("/path/to/dcf_skill"),
  )

  # Use with Excel to create financial model
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
              {"type": "custom", "skill_id": dcf_skill.id, "version": "latest"},
          ]
      },
      messages=[
          {
              "role": "user",
              "content": "Build a DCF valuation model for a SaaS company",
          }
      ],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )
  print(response)
  ```

  ```typescript TypeScript
  import Anthropic, { toFile } from "@anthropic-ai/sdk";
  import fs from "node:fs";

  const client = new Anthropic();

  // Create custom DCF analysis Skill
  const dcfSkill = await client.skills.create({
    files: [await toFile(fs.createReadStream("dcf_skill.zip"), "dcf_skill.zip")]
  });

  // Use with Excel to create financial model
  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [
        { type: "anthropic", skill_id: "xlsx", version: "latest" },
        { type: "custom", skill_id: dcfSkill.id, version: "latest" }
      ]
    },
    messages: [
      {
        role: "user",
        content: "Build a DCF valuation model for a SaaS company"
      }
    ],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });
  console.log(response);
  ```

  ```csharp C#
  using Anthropic.Core;
  // ...
  AnthropicClient client = new();

  // Create custom DCF analysis Skill
  var dcfSkill = await client.Skills.Create(new SkillCreateParams
  {
      Files =
      [
          new BinaryContent
          {
              Stream = File.OpenRead("dcf_skill/SKILL.md"),
              FileName = "dcf_skill/SKILL.md",
          },
      ],
  });

  // Use with Excel to create financial model
  var parameters = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Container = new ContainerParams
      {
          Skills =
          [
              new SkillParams
              {
                  Type = SkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
              new SkillParams
              {
                  Type = SkillParamsType.Custom,
                  SkillID = dcfSkill.ID,
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Build a DCF valuation model for a SaaS company" }],
      Tools = [new CodeExecutionTool20250825()],
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  // Custom DCF analysis Skill (ID obtained from Skills API create response)
  dcfSkillID := "skill_01AbCdEfGhIjKlMnOpQrStUv"

  // Use with Excel to create financial model
  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeAnthropic,
  					SkillID: "xlsx",
  					Version: anthropic.String("latest"),
  				},
  				{
  					Type:    anthropic.SkillParamsTypeCustom,
  					SkillID: dcfSkillID,
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Build a DCF valuation model for a SaaS company")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.ContainerParams;
  import com.anthropic.models.messages.SkillParams;
  import com.anthropic.models.messages.CodeExecutionTool20250825;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Custom DCF analysis Skill (ID obtained from Skills API create response)
      String dcfSkillId = "skill_01AbCdEfGhIjKlMnOpQrStUv";

      // Use with Excel Skill to create financial model
      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .container(ContainerParams.builder()
              .skills(List.of(
                  SkillParams.builder()
                      .type(SkillParams.Type.ANTHROPIC)
                      .skillId("xlsx")
                      .version("latest")
                      .build(),
                  SkillParams.builder()
                      .type(SkillParams.Type.CUSTOM)
                      .skillId(dcfSkillId)
                      .version("latest")
                      .build()
              ))
              .build())
          .addUserMessage("Build a DCF valuation model for a SaaS company")
          .addTool(CodeExecutionTool20250825.builder().build())
          .build();

      Message response = client.messages().create(params);
      System.out.println(response);
  }
  ```

  ```php PHP
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  $client = new Client();

  // Custom DCF analysis Skill (ID obtained from Skills API create response)
  $dcfSkillId = "skill_01AbCdEfGhIjKlMnOpQrStUv";

  // Use with Excel to create financial model
  $message = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Build a DCF valuation model for a SaaS company']
      ],
      model: 'claude-opus-5',
      betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest'],
              ['type' => 'custom', 'skill_id' => $dcfSkillId, 'version' => 'latest']
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );
  echo $message;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Create custom DCF analysis Skill
  dcf_skill = client.skills.create(
    files: [
      Anthropic::FilePart.new(
        Pathname("dcf_skill/SKILL.md"),
        filename: "dcf_skill/SKILL.md",
        content_type: "text/markdown"
      )
    ]
  )

  # Use with Excel to create financial model
  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [
        { type: "anthropic", skill_id: "xlsx", version: "latest" },
        { type: "custom", skill_id: dcf_skill.id, version: "latest" }
      ]
    },
    messages: [
      { role: "user", content: "Build a DCF valuation model for a SaaS company" }
    ],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )
  puts response
  ```
</CodeGroup>

***

## Limits and constraints

### Request limits

* **Maximum Skills per request:** 20

* **Maximum Skill upload size:** 30 MB (all files combined, uncompressed)

* **YAML frontmatter requirements:**

  * `name`: Maximum 64 characters, lowercase letters/numbers/hyphens only, no XML tags, no reserved words ("anthropic", "claude")
  * `description`: Maximum 1024 characters, non-empty, no XML tags

### Environment constraints

Skills run in the code execution container with these limitations:

* **No network access:** Cannot make external API calls
* **No runtime package installation:** Only pre-installed packages available
* **Isolated environment:** A fresh container is created unless you specify an existing container ID

See [Code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) for available packages.

***

## Best practices

### When to use multiple Skills

Combine Skills when tasks involve multiple document types or domains:

**Good use cases:**

* Data analysis (Excel) + presentation creation (PowerPoint)
* Report generation (Word) + export to PDF
* Custom domain logic + document generation

**Avoid:**

* Including unused Skills (impacts performance)

### Version management strategy

The SDK tabs in this section show the `container` value to include in a Messages request. The cURL and CLI tabs show the full request.

**For production:** pin a specific version, so Skill updates never change your deployed behavior. If you omit `version` or set it to `"latest"`, requests use the newest version of the Skill, so a version uploaded by anyone in the [workspace](https://platform.claude.com/docs/en/build-with-claude/skills-guide#workspace-scoped-access) immediately changes what your production agents run. The version ID comes from the create-version response in [Versioning](https://platform.claude.com/docs/en/build-with-claude/skills-guide#versioning) or from the [List Skill Versions API](https://platform.claude.com/docs/en/api/skills/versions/list). The ID is always a string, so quote it in JSON or YAML even when it looks numeric.

<CodeGroup>
  ```bash cURL
  # Pin to specific versions for stability
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [{
          "type": "custom",
          "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
          "version": "skver_01AbCdEfGhIjKlMnOpQrStUv"
        }]
      },
      "messages": [{"role": "user", "content": "Analyze the sales data"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'
  ```

  ```bash CLI
  # Pin to specific versions for stability
  ant messages create <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: "skver_01AbCdEfGhIjKlMnOpQrStUv"
  messages:
    - role: user
      content: Analyze the sales data
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  # Pin to specific versions for stability
  container = {
      "skills": [
          {
              "type": "custom",
              "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
              "version": "skver_01AbCdEfGhIjKlMnOpQrStUv",
          }
      ]
  }
  ```

  ```typescript TypeScript
  // Pin to specific versions for stability
  const container: Anthropic.ContainerParams = {
    skills: [
      {
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: "skver_01AbCdEfGhIjKlMnOpQrStUv"
      }
    ]
  };
  ```

  ```csharp C#
  using Anthropic.Models.Messages;

  // Pin to specific versions for stability
  var container = new ContainerParams
  {
      Skills =
      [
          new SkillParams
          {
              Type = SkillParamsType.Custom,
              SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
              Version = "skver_01AbCdEfGhIjKlMnOpQrStUv",
          },
      ],
  };
  ```

  ```go Go
  // Pin to specific versions for stability
  container := anthropic.MessageCreateParamsContainerUnion{
  	OfContainers: &anthropic.ContainerParams{
  		Skills: []anthropic.SkillParams{
  			{
  				Type:    anthropic.SkillParamsTypeCustom,
  				SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  				Version: anthropic.String("skver_01AbCdEfGhIjKlMnOpQrStUv"),
  			},
  		},
  	},
  }
  ```

  ```java Java
  import com.anthropic.models.messages.ContainerParams;
  import com.anthropic.models.messages.SkillParams;

  void main() {
      // Pin to specific versions for stability
      ContainerParams container = ContainerParams.builder()
          .addSkill(SkillParams.builder()
              .type(SkillParams.Type.CUSTOM)
              .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
              .version("skver_01AbCdEfGhIjKlMnOpQrStUv")
              .build())
          .build();
  }
  ```

  ```php PHP
  // Pin to specific versions for stability
  $container = [
      'skills' => [[
          'type' => 'custom',
          'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
          'version' => '1759178010641129'
      ]]
  ];
  ```

  ```ruby Ruby
  # Pin to specific versions for stability
  container = {
    skills: [{
      type: "custom",
      skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
      version: "skver_01AbCdEfGhIjKlMnOpQrStUv"
    }]
  }
  ```
</CodeGroup>

**For development:** use `latest` to pick up the newest version automatically as you iterate.

<CodeGroup>
  ```bash cURL
  # Use latest for active development
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [{
          "type": "custom",
          "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
          "version": "latest"
        }]
      },
      "messages": [{"role": "user", "content": "Analyze the sales data"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'
  ```

  ```bash CLI
  # Use latest for active development
  ant messages create <<YAML
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: latest
  messages:
    - role: user
      content: Analyze the sales data
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  # Use latest for active development
  container = {
      "skills": [
          {
              "type": "custom",
              "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
              "version": "latest",
          }
      ]
  }
  ```

  ```typescript TypeScript
  // Use latest for active development
  const container: Anthropic.ContainerParams = {
    skills: [
      {
        type: "custom",
        skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
        version: "latest"
      }
    ]
  };
  ```

  ```csharp C#
  using Anthropic.Models.Messages;

  // Use latest for active development
  var container = new ContainerParams
  {
      Skills =
      [
          new SkillParams
          {
              Type = SkillParamsType.Custom,
              SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
              Version = "latest",
          },
      ],
  };
  ```

  ```go Go
  // Use latest for active development
  container := anthropic.MessageCreateParamsContainerUnion{
  	OfContainers: &anthropic.ContainerParams{
  		Skills: []anthropic.SkillParams{
  			{
  				Type:    anthropic.SkillParamsTypeCustom,
  				SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  				Version: anthropic.String("latest"),
  			},
  		},
  	},
  }
  ```

  ```java Java
  import com.anthropic.models.messages.ContainerParams;
  import com.anthropic.models.messages.SkillParams;

  void main() {
      // Use latest for active development
      ContainerParams container = ContainerParams.builder()
          .addSkill(SkillParams.builder()
              .type(SkillParams.Type.CUSTOM)
              .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
              .version("latest")
              .build())
          .build();
  }
  ```

  ```php PHP
  // Use latest for active development
  $container = [
      'skills' => [[
          'type' => 'custom',
          'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
          'version' => 'latest'
      ]]
  ];
  ```

  ```ruby Ruby
  # Use latest for active development
  container = {
    skills: [{
      type: "custom",
      skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
      version: "latest"
    }]
  }
  ```
</CodeGroup>

### Prompt caching considerations

If you use [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), changing the Skills list in your container breaks the cache. Skills render into the system prompt in a fixed order, so the same list produces the same cacheable prefix:

<CodeGroup>
  ```bash cURL
  # Skills render into the system prompt in a fixed, cache-friendly order
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
      },
      "messages": [{"role": "user", "content": "Analyze sales data"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'

  # Changing the Skills list ([xlsx] vs [xlsx, pptx]) changes the prefix: a cache miss, while an identical list is a cache hit
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "container": {
        "skills": [
          {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
          {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
        ]
      },
      "messages": [{"role": "user", "content": "Create a presentation"}],
      "tools": [{"type": "code_execution_20250825", "name": "code_execution"}]
    }'
  ```

  ```bash CLI
  # Skills render into the system prompt in a fixed, cache-friendly order
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: anthropic
        skill_id: xlsx
        version: latest
  messages:
    - role: user
      content: Analyze sales data
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML

  # Changing the Skills list ([xlsx] vs [xlsx, pptx]) changes the prefix: a cache miss, while an identical list is a cache hit
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: anthropic
        skill_id: xlsx
        version: latest
      - type: anthropic
        skill_id: pptx
        version: latest
  messages:
    - role: user
      content: Create a presentation
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Skills render into the system prompt in a fixed, cache-friendly order
  response1 = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      container={
          "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
      },
      messages=[{"role": "user", "content": "Analyze sales data"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )

  # Changing the Skills list ([xlsx] vs [xlsx, pptx]) changes the prefix: a cache miss, while an identical list is a cache hit
  response2 = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      container={
          "skills": [
              {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
              {
                  "type": "anthropic",
                  "skill_id": "pptx",
                  "version": "latest",
              },  # prefix change: cache miss
          ]
      },
      messages=[{"role": "user", "content": "Create a presentation"}],
      tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Skills render into the system prompt in a fixed, cache-friendly order
  const response1 = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [{ role: "user", content: "Analyze sales data" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });

  // Changing the Skills list ([xlsx] vs [xlsx, pptx]) changes the prefix: a cache miss, while an identical list is a cache hit
  const response2 = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [
        { type: "anthropic", skill_id: "xlsx", version: "latest" },
        { type: "anthropic", skill_id: "pptx", version: "latest" } // prefix change: cache miss
      ]
    },
    messages: [{ role: "user", content: "Create a presentation" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Skills render into the system prompt in a fixed, cache-friendly order
  var parameters1 = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Container = new ContainerParams
      {
          Skills =
          [
              new SkillParams
              {
                  Type = SkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Analyze sales data" }],
      Tools = [new CodeExecutionTool20250825()],
  };

  var response1 = await client.Messages.Create(parameters1);
  Console.WriteLine(response1);

  // Different Skill set ([xlsx] vs [xlsx, pptx]) = a different prefix: a cache miss (an identical set is a cache hit)
  var parameters2 = new MessageCreateParams
  {
      Model = "claude-opus-5",
      MaxTokens = 4096,
      Container = new ContainerParams
      {
          Skills =
          [
              new SkillParams
              {
                  Type = SkillParamsType.Anthropic,
                  SkillID = "xlsx",
                  Version = "latest",
              },
              new SkillParams
              {
                  Type = SkillParamsType.Anthropic,
                  SkillID = "pptx",
                  Version = "latest",
              },
          ],
      },
      Messages = [new() { Role = Role.User, Content = "Create a presentation" }],
      Tools = [new CodeExecutionTool20250825()],
  };

  var response2 = await client.Messages.Create(parameters2);
  Console.WriteLine(response2);
  ```

  ```go Go
  client := anthropic.NewClient()

  // Skills render into the system prompt in a fixed, cache-friendly order
  response1, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeAnthropic,
  					SkillID: "xlsx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze sales data")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response1)

  // Changing the Skills list ([xlsx] vs [xlsx, pptx]) changes the prefix: a cache miss, while an identical list is a cache hit
  response2, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeAnthropic,
  					SkillID: "xlsx",
  					Version: anthropic.String("latest"),
  				},
  				{
  					Type:    anthropic.SkillParamsTypeAnthropic,
  					SkillID: "pptx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Create a presentation")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response2)
  ```

  ```java Java
  import com.anthropic.models.messages.ContainerParams;
  import com.anthropic.models.messages.SkillParams;
  import com.anthropic.models.messages.CodeExecutionTool20250825;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      // Skills render into the system prompt in a fixed, cache-friendly order
      MessageCreateParams params1 = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .container(ContainerParams.builder()
              .skills(List.of(
                  SkillParams.builder()
                      .type(SkillParams.Type.ANTHROPIC)
                      .skillId("xlsx")
                      .version("latest")
                      .build()
              ))
              .build())
          .addUserMessage("Analyze sales data")
          .addTool(CodeExecutionTool20250825.builder().build())
          .build();

      Message response1 = client.messages().create(params1);
      System.out.println(response1);

      // Changing the Skills list ([xlsx] vs [xlsx, pptx]) changes the prefix: a cache miss, while an identical list is a cache hit
      MessageCreateParams params2 = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .container(ContainerParams.builder()
              .skills(List.of(
                  SkillParams.builder()
                      .type(SkillParams.Type.ANTHROPIC)
                      .skillId("xlsx")
                      .version("latest")
                      .build(),
                  SkillParams.builder()
                      .type(SkillParams.Type.ANTHROPIC)
                      .skillId("pptx")
                      .version("latest")
                      .build()
              ))
              .build())
          .addUserMessage("Create a presentation")
          .addTool(CodeExecutionTool20250825.builder().build())
          .build();

      Message response2 = client.messages().create(params2);
      System.out.println(response2);
  }
  ```

  ```php PHP
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  $client = new Client();

  // Skills render into the system prompt in a fixed, cache-friendly order
  $response1 = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Analyze sales data']
      ],
      model: 'claude-opus-5',
      betas: [
          'code-execution-2025-08-25',
          'skills-2025-10-02',
      ],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest']
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );
  echo $response1;

  // Changing the Skills list ([xlsx] vs [xlsx, pptx]) changes the prefix: a cache miss, while an identical list is a cache hit
  $response2 = $client->beta->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Create a presentation']
      ],
      model: 'claude-opus-5',
      betas: [
          'code-execution-2025-08-25',
          'skills-2025-10-02',
      ],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest'],
              ['type' => 'anthropic', 'skill_id' => 'pptx', 'version' => 'latest']
          ]
      ],
      tools: [
          ['type' => 'code_execution_20250825', 'name' => 'code_execution']
      ]
  );
  echo $response2;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Skills render into the system prompt in a fixed, cache-friendly order
  response1 = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [{ role: "user", content: "Analyze sales data" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )
  puts response1

  # Changing the Skills list ([xlsx] vs [xlsx, pptx]) changes the prefix: a cache miss, while an identical list is a cache hit
  response2 = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    container: {
      skills: [
        { type: "anthropic", skill_id: "xlsx", version: "latest" },
        { type: "anthropic", skill_id: "pptx", version: "latest" } # prefix change: cache miss
      ]
    },
    messages: [{ role: "user", content: "Create a presentation" }],
    tools: [{ type: "code_execution_20250825", name: "code_execution" }]
  )
  puts response2
  ```
</CodeGroup>

For best caching performance, keep your Skills list, including its order, consistent across requests. Pinning custom Skill versions also helps: with `"latest"`, publishing a new version can invalidate the cached prefix if it changes the Skill's description.

### Error handling

Handle Skill-related errors gracefully:

<CodeGroup>
  ```bash cURL
  # This error-handling flow doesn't translate well to a one-off shell
  # command; one of the SDK options would be a better fit. A failing request
  # returns HTTP 400 with an error JSON whose .error.message names the
  # Skill problem.
  ```

  ```bash CLI
  if ! RESULT=$(ant messages create \
    --transform-error error.message \
    --format-error yaml 2>&1 <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  container:
    skills:
      - type: custom
        skill_id: skill_01AbCdEfGhIjKlMnOpQrStUv
        version: latest
  messages:
    - role: user
      content: Process data
  tools:
    - type: code_execution_20250825
      name: code_execution
  YAML
  ); then
    case "$RESULT" in
      *skill*)
        printf 'Skill error: %s\n' "$RESULT"
        # Handle skill-specific errors
        ;;
      *)
        printf '%s\n' "$RESULT" >&2
        exit 1
        ;;
    esac
  fi
  ```

  ```python Python
  client = anthropic.Anthropic()

  try:
      response = client.messages.create(
          model="claude-opus-5",
          max_tokens=4096,
          container={
              "skills": [
                  {
                      "type": "custom",
                      "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                      "version": "latest",
                  }
              ]
          },
          messages=[{"role": "user", "content": "Process data"}],
          tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
      )
  except anthropic.BadRequestError as e:
      if "skill" in str(e):
          print(f"Skill error: {e}")
          # Handle skill-specific errors
      else:
          raise
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  try {
    const response = await client.messages.create({
      model: "claude-opus-5",
      max_tokens: 4096,
      container: {
        skills: [
          { type: "custom", skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv", version: "latest" }
        ]
      },
      messages: [{ role: "user", content: "Process data" }],
      tools: [{ type: "code_execution_20250825", name: "code_execution" }]
    });
    console.log(response);
  } catch (error) {
    if (error instanceof Anthropic.BadRequestError && error.message.includes("skill")) {
      console.error(`Skill error: ${error.message}`);
      // Handle skill-specific errors
    } else {
      throw error;
    }
  }
  ```

  ```csharp C#
  using Anthropic.Exceptions;
  // ...
  AnthropicClient client = new();

  try
  {
      var parameters = new MessageCreateParams
      {
          Model = "claude-opus-5",
          MaxTokens = 4096,
          Container = new ContainerParams
          {
              Skills =
              [
                  new SkillParams
                  {
                      Type = SkillParamsType.Custom,
                      SkillID = "skill_01AbCdEfGhIjKlMnOpQrStUv",
                      Version = "latest",
                  },
              ],
          },
          Messages = [new() { Role = Role.User, Content = "Process data" }],
          Tools = [new CodeExecutionTool20250825()],
      };

      var response = await client.Messages.Create(parameters);
      Console.WriteLine(response);
  }
  catch (AnthropicBadRequestException e) when (e.Message.Contains("skill"))
  {
      Console.WriteLine($"Skill error: {e.Message}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-opus-5",
  	MaxTokens: 4096,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeCustom,
  					SkillID: "skill_01AbCdEfGhIjKlMnOpQrStUv",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Process data")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20250825: &anthropic.CodeExecutionTool20250825Param{}},
  	},
  })

  if err != nil {
  	var apierr *anthropic.Error
  	if errors.As(err, &apierr) && apierr.Type() == anthropic.ErrorTypeInvalidRequestError &&
  		strings.Contains(apierr.Error(), "skill") {
  		fmt.Printf("Skill error: %v\n", apierr)
  	} else {
  		log.Fatal(err)
  	}
  	return
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.errors.BadRequestException;
  import com.anthropic.models.messages.ContainerParams;
  import com.anthropic.models.messages.SkillParams;
  import com.anthropic.models.messages.CodeExecutionTool20250825;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      try {
          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5)
              .maxTokens(4096L)
              .container(ContainerParams.builder()
                  .addSkill(SkillParams.builder()
                      .type(SkillParams.Type.CUSTOM)
                      .skillId("skill_01AbCdEfGhIjKlMnOpQrStUv")
                      .version("latest")
                      .build())
                  .build())
              .addUserMessage("Process data")
              .addTool(CodeExecutionTool20250825.builder().build())
              .build();

          Message response = client.messages().create(params);
          System.out.println(response);
      } catch (BadRequestException e) {
          if (e.getMessage().contains("skill")) {
              System.err.println("Skill error: " + e.getMessage());
          } else {
              throw e;
          }
      }
  }
  ```

  ```php PHP
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  use Anthropic\Core\Exceptions\BadRequestException;

  $client = new Client();

  try {
      $message = $client->beta->messages->create(
          maxTokens: 4096,
          messages: [
              ['role' => 'user', 'content' => 'Process data']
          ],
          model: 'claude-opus-5',
          betas: ['code-execution-2025-08-25', 'skills-2025-10-02'],
          container: [
              'skills' => [
                  [
                      'type' => 'custom',
                      'skill_id' => 'skill_01AbCdEfGhIjKlMnOpQrStUv',
                      'version' => 'latest'
                  ]
              ]
          ],
          tools: [
              ['type' => 'code_execution_20250825', 'name' => 'code_execution']
          ]
      );
      echo $message;
  } catch (BadRequestException $e) {
      if (str_contains($e->getMessage(), 'skill')) {
          echo "Skill error: " . $e->getMessage();
      } else {
          throw $e;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  begin
    response = client.messages.create(
      model: "claude-opus-5",
      max_tokens: 4096,
      container: {
        skills: [
          {
            type: "custom",
            skill_id: "skill_01AbCdEfGhIjKlMnOpQrStUv",
            version: "latest"
          }
        ]
      },
      messages: [{ role: "user", content: "Process data" }],
      tools: [{ type: "code_execution_20250825", name: "code_execution" }]
    )
  rescue Anthropic::Errors::BadRequestError => e
    if e.message.include?("skill")
      puts "Skill error: #{e.message}"
    else
      raise
    end
  end
  ```
</CodeGroup>

***

## Data retention

Agent Skills are not covered by ZDR arrangements. Skill definitions and execution data are retained according to Anthropic's standard data retention policy.

For ZDR eligibility across all features, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).

## Audit logging

If your organization has the [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api) enabled, its [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed) records the creation and deletion of Skills and Skill versions made with a Claude API key or from the Claude Console. Operations that occur while the Compliance API is off are not recorded and cannot be recovered later, so [set up the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access) before you rely on this audit trail.

## Next steps

<CardGroup cols={3}>
  <Card title="API reference" icon="book" href="https://platform.claude.com/docs/en/api/skills/create">
    Complete API reference with all endpoints
  </Card>

  <Card title="Skill authoring best practices" icon="edit" href="https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices">
    Learn how to write effective Skills that Claude can discover and use successfully.
  </Card>

  <Card title="Code execution tool" icon="terminal" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool">
    Run Python and bash code in a sandboxed container to analyze data, generate files, and iterate on solutions.
  </Card>
</CardGroup>
