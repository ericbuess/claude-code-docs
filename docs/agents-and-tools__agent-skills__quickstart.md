---
title: Get started with Agent Skills in the API
url: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart
description: Learn how to use Agent Skills to create documents with the Claude API in under 10 minutes.
---

This tutorial shows you how to use Agent Skills to create a PowerPoint presentation. You'll learn how to enable Skills, make a request, and access the generated file.

## Prerequisites

* A [Claude API key](https://platform.claude.com/settings/keys) or a logged-in [ant CLI](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/authentication)
* A [client SDK](https://platform.claude.com/docs/en/cli-sdks-libraries/overview) for your language, or `curl` and `jq`
* Basic familiarity with making API requests

## Agent Skills overview

Pre-built Agent Skills extend Claude's capabilities with specialized expertise for tasks such as creating documents, analyzing data, and processing files. Anthropic provides the following pre-built Agent Skills in the API:

* **PowerPoint (pptx):** Create and edit presentations
* **Excel (xlsx):** Create and analyze spreadsheets
* **Word (docx):** Create and edit documents
* **PDF (pdf):** Generate PDF documents

<Note>
  To create custom Skills, see the [Agent Skills Cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction) for examples of building your own Skills with domain-specific expertise.
</Note>

## Step 1: List available Skills

First, check what Skills are available. Use the Skills API to list all Anthropic-managed Skills. Each language tab is an excerpt from one continuous script, with any imports and client setup at the top:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  # List Anthropic-managed Skills
  curl --fail-with-body -sS "https://api.anthropic.com/v1/skills?source=anthropic" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  # List Anthropic-managed Skills
  ant skills list --source anthropic
  ```

  ```python Python
  # List Anthropic-managed Skills
  skills = client.skills.list(source="anthropic")

  for skill in skills.data:
      print(f"{skill.id}: {skill.display_name}")
  ```

  ```typescript TypeScript
  // List Anthropic-managed Skills
  const skills = await client.skills.list({ source: "anthropic" });

  for (const skill of skills.data) {
    console.log(`${skill.id}: ${skill.display_name}`);
  }
  ```

  ```csharp C#
  // List Anthropic-managed Skills
  var skills = await client.Skills.List(new SkillListParams { Source = "anthropic" });

  foreach (var skill in skills.Items)
  {
      Console.WriteLine($"{skill.ID}: {skill.DisplayName}");
  }
  ```

  ```go Go
  // List Anthropic-managed Skills
  skills, err := client.Skills.List(ctx, anthropic.SkillListParams{
  	Source: anthropic.String("anthropic"),
  })
  if err != nil {
  	panic(err)
  }

  for _, skill := range skills.Data {
  	fmt.Printf("%s: %s\n", skill.ID, skill.DisplayName)
  }
  ```

  ```java Java
  // List Anthropic-managed Skills
  SkillListPage skills = client.skills().list(
      SkillListParams.builder().source("anthropic").build()
  );

  for (Skill skill : skills.data()) {
      IO.println(skill.id() + ": " + skill.displayName());
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Skills API under the beta namespace; field names can differ from other SDKs.
  // List Anthropic-managed Skills
  $skills = $client->beta->skills->list(source: 'anthropic');

  foreach ($skills->data as $skill) {
      echo "{$skill->id}: {$skill->displayTitle}\n";
  }
  ```

  ```ruby Ruby
  # List Anthropic-managed Skills
  skills = client.skills.list(source: "anthropic")

  skills.data.each do |skill|
    puts "#{skill.id}: #{skill.display_name}"
  end
  ```
</CodeGroup>

You see the following Skills: `pptx`, `xlsx`, `docx`, and `pdf`.

This API returns each Skill's metadata: its name and description. Claude loads this metadata at startup to determine which Skills are available. This is the first level of **progressive disclosure**, where Claude discovers Skills without loading their full instructions yet.

## Step 2: Create a presentation

Use the PowerPoint Skill to create a presentation about renewable energy. Specify Skills using the `container` parameter in the Messages API:

<CodeGroup>
  ```bash cURL
  # Create a message with the PowerPoint Skill
  response=$(
    curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
      -H "content-type: application/json" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -d @- <<'EOF'
  {
    "model": "claude-opus-5",
    "max_tokens": 16000,
    "container": {
      "skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]
    },
    "messages": [
      {"role": "user", "content": "Create a presentation about renewable energy with 5 slides"}
    ],
    "tools": [{"type": "code_execution_20260521", "name": "code_execution"}]
  }
  EOF
  )
  ```

  ```bash CLI
  # Create a message with the PowerPoint Skill
  response=$(ant messages create --format json <<'YAML'
  model: claude-opus-5
  max_tokens: 16000
  container:
    skills:
      - type: anthropic
        skill_id: pptx
        version: latest
  messages:
    - role: user
      content: Create a presentation about renewable energy with 5 slides
  tools:
    - type: code_execution_20260521
      name: code_execution
  YAML
  )
  ```

  ```python Python
  # Create a message with the PowerPoint Skill
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=16000,
      container={
          "skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]
      },
      messages=[
          {
              "role": "user",
              "content": "Create a presentation about renewable energy with 5 slides",
          }
      ],
      tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
  )

  print(f"stop_reason={response.stop_reason}, blocks={len(response.content)}")
  ```

  ```typescript TypeScript
  // Create a message with the PowerPoint Skill
  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 16000,
    container: {
      skills: [{ type: "anthropic", skill_id: "pptx", version: "latest" }],
    },
    messages: [
      {
        role: "user",
        content: "Create a presentation about renewable energy with 5 slides",
      },
    ],
    tools: [{ type: "code_execution_20260521", name: "code_execution" }],
  });

  console.log(
    `stop_reason=${response.stop_reason}, blocks=${response.content.length}`,
  );
  ```

  ```csharp C#
  // Create a message with the PowerPoint Skill
  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 16000,
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
      Messages =
      [
          new MessageParam
          {
              Role = Role.User,
              Content = "Create a presentation about renewable energy with 5 slides",
          },
      ],
      Tools = [new CodeExecutionTool20260521()],
  });

  Console.WriteLine($"stop_reason={response.StopReason?.Raw()}, blocks={response.Content.Count}");
  ```

  ```go Go
  // Create a message with the PowerPoint Skill
  response, err := client.Messages.New(ctx, anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 16000,
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
  		anthropic.NewUserMessage(
  			anthropic.NewTextBlock("Create a presentation about renewable energy with 5 slides"),
  		),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{OfCodeExecutionTool20260521: &anthropic.CodeExecutionTool20260521Param{}},
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("stop_reason=%s, blocks=%d\n", response.StopReason, len(response.Content))
  ```

  ```java Java
  // Create a message with the PowerPoint Skill
  Message response = client.messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(16000)
          .container(
              ContainerParams.builder()
                  .addSkill(
                      SkillParams.builder()
                          .type(SkillParams.Type.ANTHROPIC)
                          .skillId("pptx")
                          .version("latest")
                          .build()
                  )
                  .build()
          )
          .addUserMessage("Create a presentation about renewable energy with 5 slides")
          .addTool(CodeExecutionTool20260521.builder().build())
          .build()
  );

  IO.println(
      "stop_reason=" + response.stopReason().orElse(null)
          + ", blocks=" + response.content().size()
  );
  ```

  ```php PHP
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  // Create a message with the PowerPoint Skill
  $response = $client->beta->messages->create(
      model: 'claude-opus-5',
      maxTokens: 16000,
      betas: ['skills-2025-10-02'],
      container: [
          'skills' => [['type' => 'anthropic', 'skill_id' => 'pptx', 'version' => 'latest']],
      ],
      messages: [
          [
              'role' => 'user',
              'content' => 'Create a presentation about renewable energy with 5 slides',
          ],
      ],
      tools: [['type' => 'code_execution_20260521', 'name' => 'code_execution']],
  );

  printf("stop_reason=%s, blocks=%d\n", $response->stopReason, count($response->content));
  ```

  ```ruby Ruby
  # Create a message with the PowerPoint Skill
  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 16_000,
    container: {
      skills: [{type: "anthropic", skill_id: "pptx", version: "latest"}]
    },
    messages: [
      {
        role: "user",
        content: "Create a presentation about renewable energy with 5 slides"
      }
    ],
    tools: [{type: "code_execution_20260521", name: "code_execution"}]
  )

  puts "stop_reason=#{response.stop_reason}, blocks=#{response.content.length}"
  ```
</CodeGroup>

The request includes the following parts:

* **`model`:** A [model that supports the code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#model-compatibility)
* **`container.skills`:** Specifies which Skills Claude can use
* **`type: "anthropic"`:** Indicates this is an Anthropic-managed Skill
* **`skill_id: "pptx"`:** The PowerPoint Skill identifier
* **`version: "latest"`:** The Skill version set to the most recently published
* **`tools`:** Enables code execution (required for Skills)

<Note>
  The examples use the `code_execution_20260521` tool version, and the Step 3 code parses the result types that current tool versions return. Skills also work with older [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) versions such as `code_execution_20250825`: any current code execution tool version satisfies the Skills requirement. If you use a different version, use the tool `type` listed on the code execution tool page.
</Note>

When you make this request, Claude automatically matches your task to the relevant Skill. Because you asked for a presentation, Claude determines the PowerPoint Skill is relevant and loads its full instructions: the second level of progressive disclosure. Then Claude runs the Skill's code to create your presentation.

## Step 3: Download the created file

The presentation was created in the code execution container and saved as a file. The Step 2 `response` includes a file reference with a file ID. Extract the file ID and download the file with the Files API. The example saves it to your system temp directory:

<CodeGroup>
  ```bash cURL
  # Extract the file ID. The code execution tool runs the Skill's code through
  # its Bash sub-tool, and generated files appear as bash_code_execution_output
  # items inside the bash_code_execution_tool_result block.
  file_id=$(jq -r '
    last(
      .content[]
      | select(.type == "bash_code_execution_tool_result")
      | .content
      | select(.type == "bash_code_execution_result")
      | .content[].file_id
    ) // empty
  ' <<<"$response")

  if [[ -n "$file_id" ]]; then
    # Download the file and save it
    output_path="${TMPDIR:-/tmp}/renewable_energy.pptx"
    curl --fail-with-body -sS "https://api.anthropic.com/v1/files/$file_id/content" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -o "$output_path"
    echo "Presentation saved to $output_path"
  fi
  ```

  ```bash CLI
  # Extract the file ID. The code execution tool runs the Skill's code through
  # its Bash sub-tool, and generated files appear as bash_code_execution_output
  # items inside the bash_code_execution_tool_result block.
  file_id=$(jq -r '
    last(
      .content[]
      | select(.type == "bash_code_execution_tool_result")
      | .content
      | select(.type == "bash_code_execution_result")
      | .content[].file_id
    ) // empty
  ' <<<"$response")

  if [[ -n "$file_id" ]]; then
    # Download the file and save it
    output_path="${TMPDIR:-/tmp}/renewable_energy.pptx"
    ant files download --file-id "$file_id" --output "$output_path"
    echo "Presentation saved to $output_path"
  fi
  ```

  ```python Python
  # Extract the file ID. The code execution tool runs the Skill's code through
  # its Bash sub-tool, and generated files appear as bash_code_execution_output
  # items inside the bash_code_execution_tool_result block.
  file_id = None
  for block in response.content:
      if block.type == "bash_code_execution_tool_result":
          if block.content.type == "bash_code_execution_result":
              for output in block.content.content:
                  file_id = output.file_id

  if file_id:
      # Download the file and save it
      output_path = Path(tempfile.gettempdir()) / "renewable_energy.pptx"
      file_content = client.files.download(file_id=file_id)
      file_content.write_to_file(output_path)
      print(f"Presentation saved to {output_path}")
  ```

  ```typescript TypeScript
  // Extract the file ID. The code execution tool runs the Skill's code through
  // its Bash sub-tool, and generated files appear as bash_code_execution_output
  // items inside the bash_code_execution_tool_result block.
  let fileId: string | undefined;
  for (const block of response.content) {
    if (
      block.type === "bash_code_execution_tool_result" &&
      block.content.type === "bash_code_execution_result"
    ) {
      for (const output of block.content.content) {
        fileId = output.file_id;
      }
    }
  }

  if (fileId) {
    // Download the file and save it
    const outputPath = path.join(os.tmpdir(), "renewable_energy.pptx");
    const fileContent = await client.files.download(fileId);
    await fs.writeFile(outputPath, Buffer.from(await fileContent.arrayBuffer()));
    console.log(`Presentation saved to ${outputPath}`);
  }
  ```

  ```csharp C#
  // Extract the file ID. The code execution tool runs the Skill's code through
  // its Bash sub-tool, and generated files appear as bash_code_execution_output
  // items inside the bash_code_execution_tool_result block.
  string? fileId = null;
  foreach (var block in response.Content)
  {
      if (block.TryPickBashCodeExecutionToolResult(out var bashResult)
          && bashResult.Content.TryPickBashCodeExecutionResultBlock(out var bashResultBlock))
      {
          foreach (var output in bashResultBlock.Content)
          {
              fileId = output.FileID;
          }
      }
  }

  if (fileId is not null)
  {
      // Download the file and save it
      var outputPath = Path.Combine(Path.GetTempPath(), "renewable_energy.pptx");
      using var download = await client.Files.Download(fileId);
      await using var source = await download.ReadAsStream();
      await using var destination = File.Create(outputPath);
      await source.CopyToAsync(destination);
      Console.WriteLine($"Presentation saved to {outputPath}");
  }
  ```

  ```go Go
  // Extract the file ID. The code execution tool runs the Skill's code through
  // its Bash sub-tool, and generated files appear as bash_code_execution_output
  // items inside the bash_code_execution_tool_result block.
  var fileID string
  for _, block := range response.Content {
  	switch result := block.AsAny().(type) {
  	case anthropic.BashCodeExecutionToolResultBlock:
  		if result.Content.Type == "bash_code_execution_result" {
  			for _, output := range result.Content.Content {
  				fileID = output.FileID
  			}
  		}
  	}
  }

  if fileID != "" {
  	// Download the file and save it
  	outputPath := filepath.Join(os.TempDir(), "renewable_energy.pptx")
  	fileContent, err := client.Files.Download(ctx, fileID)
  	if err != nil {
  		panic(err)
  	}
  	defer fileContent.Body.Close()
  	outFile, err := os.Create(outputPath)
  	if err != nil {
  		panic(err)
  	}
  	defer outFile.Close()
  	if _, err := io.Copy(outFile, fileContent.Body); err != nil {
  		panic(err)
  	}
  	fmt.Printf("Presentation saved to %s\n", outputPath)
  }
  ```

  ```java Java
  // Extract the file ID. The code execution tool runs the Skill's code through
  // its Bash sub-tool, and generated files appear as bash_code_execution_output
  // items inside the bash_code_execution_tool_result block.
  String fileId = null;
  for (ContentBlock block : response.content()) {
      if (block.isBashCodeExecutionToolResult()) {
          var content = block.asBashCodeExecutionToolResult().content();
          if (content.isBashCodeExecutionResultBlock()) {
              for (var output : content.asBashCodeExecutionResultBlock().content()) {
                  fileId = output.fileId();
              }
          }
      }
  }

  if (fileId != null) {
      // Download the file and save it
      Path outputPath = Files.createTempFile("renewable_energy", ".pptx");
      try (HttpResponse fileContent = client.files().download(fileId)) {
          Files.copy(fileContent.body(), outputPath, StandardCopyOption.REPLACE_EXISTING);
      }
      IO.println("Presentation saved to " + outputPath);
  }
  ```

  ```php PHP
  // The PHP SDK exposes the Files API under the beta namespace; field names can differ from other SDKs.
  // Extract the file ID. The code execution tool runs the Skill's code through
  // its Bash sub-tool, and generated files appear as bash_code_execution_output
  // items inside the bash_code_execution_tool_result block.
  $fileId = null;
  foreach ($response->content as $block) {
      if ($block->type !== 'bash_code_execution_tool_result') {
          continue;
      }
      $resultBlock = $block->content;
      if ($resultBlock->type !== 'bash_code_execution_result') {
          continue;
      }
      foreach ($resultBlock->content as $output) {
          $fileId = $output->fileID;
      }
  }

  if ($fileId !== null) {
      // Download the file and save it
      $outputPath = sys_get_temp_dir() . '/renewable_energy.pptx';
      $fileContent = $client->beta->files->download($fileId);
      file_put_contents($outputPath, $fileContent);
      echo "Presentation saved to {$outputPath}\n";
  }
  ```

  ```ruby Ruby
  # Extract the file ID. The code execution tool runs the Skill's code through
  # its Bash sub-tool, and generated files appear as bash_code_execution_output
  # items inside the bash_code_execution_tool_result block.
  file_id = nil
  response.content.each do |block|
    next unless block.type == :bash_code_execution_tool_result

    if block.content[:type].to_s == "bash_code_execution_result"
      Array(block.content[:content]).each { |output| file_id = output[:file_id] }
    end
  end

  if file_id
    # Download the file and save it
    output_path = File.join(Dir.tmpdir, "renewable_energy.pptx")
    file_content = client.files.download(file_id)
    File.binwrite(output_path, file_content.read)
    puts "Presentation saved to #{output_path}"
  end
  ```
</CodeGroup>

<Note>
  For complete details on working with generated files, see [Retrieve generated files](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool#retrieve-generated-files) in the code execution tool documentation.
</Note>

## Try more examples

Try these variations:

### Create a spreadsheet

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 16000,
      "container": {
        "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
      },
      "messages": [
        {"role": "user", "content": "Create a quarterly sales tracking spreadsheet with sample data"}
      ],
      "tools": [{"type": "code_execution_20260521", "name": "code_execution"}]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 16000
  container:
    skills:
      - type: anthropic
        skill_id: xlsx
        version: latest
  messages:
    - role: user
      content: Create a quarterly sales tracking spreadsheet with sample data
  tools:
    - type: code_execution_20260521
      name: code_execution
  YAML
  ```

  ```python Python
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=16000,
      container={
          "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
      },
      messages=[
          {
              "role": "user",
              "content": "Create a quarterly sales tracking spreadsheet with sample data",
          }
      ],
      tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 16000,
    container: {
      skills: [{ type: "anthropic", skill_id: "xlsx", version: "latest" }]
    },
    messages: [
      {
        role: "user",
        content: "Create a quarterly sales tracking spreadsheet with sample data"
      }
    ],
    tools: [{ type: "code_execution_20260521", name: "code_execution" }]
  });
  ```

  ```csharp C#
  var response = await client.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5,
          MaxTokens = 16000,
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
          Messages =
          [
              new MessageParam
              {
                  Role = Role.User,
                  Content = "Create a quarterly sales tracking spreadsheet with sample data",
              },
          ],
          Tools = [new CodeExecutionTool20260521()],
      }
  );
  ```

  ```go Go
  response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 16000,
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
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Create a quarterly sales tracking spreadsheet with sample data")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{
  			OfCodeExecutionTool20260521: &anthropic.CodeExecutionTool20260521Param{},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  Message response = client.messages().create(
      MessageCreateParams.builder()
          .model(CLAUDE_OPUS_5)
          .maxTokens(16000)
          .container(
              ContainerParams.builder()
                  .addSkill(
                      SkillParams.builder()
                          .type(ANTHROPIC)
                          .skillId("xlsx")
                          .version("latest")
                          .build()
                  )
                  .build()
          )
          .addUserMessage("Create a quarterly sales tracking spreadsheet with sample data")
          .addTool(CodeExecutionTool20260521.builder().build())
          .build()
  );

  ```

  ```php PHP
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  $response = $client->beta->messages->create(
      model: 'claude-opus-5',
      maxTokens: 16000,
      betas: ['skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'xlsx', 'version' => 'latest'],
          ],
      ],
      messages: [
          [
              'role' => 'user',
              'content' => 'Create a quarterly sales tracking spreadsheet with sample data',
          ],
      ],
      tools: [new BetaCodeExecutionTool20260521()],
  );
  ```

  ```ruby Ruby
  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 16_000,
    container: {
      skills: [{type: "anthropic", skill_id: "xlsx", version: "latest"}]
    },
    messages: [
      {
        role: "user",
        content: "Create a quarterly sales tracking spreadsheet with sample data"
      }
    ],
    tools: [{type: "code_execution_20260521", name: "code_execution"}]
  )
  ```
</CodeGroup>

### Create a Word document

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 16000,
      "container": {
        "skills": [{"type": "anthropic", "skill_id": "docx", "version": "latest"}]
      },
      "messages": [
        {"role": "user", "content": "Write a 2-page report on the benefits of renewable energy"}
      ],
      "tools": [{"type": "code_execution_20260521", "name": "code_execution"}]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 16000
  container:
    skills:
      - type: anthropic
        skill_id: docx
        version: latest
  messages:
    - role: user
      content: Write a 2-page report on the benefits of renewable energy
  tools:
    - type: code_execution_20260521
      name: code_execution
  YAML
  ```

  ```python Python
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=16000,
      container={
          "skills": [{"type": "anthropic", "skill_id": "docx", "version": "latest"}]
      },
      messages=[
          {
              "role": "user",
              "content": "Write a 2-page report on the benefits of renewable energy",
          }
      ],
      tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 16000,
    container: {
      skills: [{ type: "anthropic", skill_id: "docx", version: "latest" }]
    },
    messages: [
      {
        role: "user",
        content: "Write a 2-page report on the benefits of renewable energy"
      }
    ],
    tools: [{ type: "code_execution_20260521", name: "code_execution" }]
  });
  ```

  ```csharp C#
  var response = await client.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5,
          MaxTokens = 16000,
          Container = new ContainerParams
          {
              Skills =
              [
                  new SkillParams
                  {
                      Type = SkillParamsType.Anthropic,
                      SkillID = "docx",
                      Version = "latest",
                  },
              ],
          },
          Messages =
          [
              new MessageParam
              {
                  Role = Role.User,
                  Content = "Write a 2-page report on the benefits of renewable energy",
              },
          ],
          Tools = [new CodeExecutionTool20260521()],
      }
  );
  ```

  ```go Go
  response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 16000,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeAnthropic,
  					SkillID: "docx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Write a 2-page report on the benefits of renewable energy")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{
  			OfCodeExecutionTool20260521: &anthropic.CodeExecutionTool20260521Param{},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  Message response = client.messages().create(
      MessageCreateParams.builder()
          .model(CLAUDE_OPUS_5)
          .maxTokens(16000)
          .container(
              ContainerParams.builder()
                  .addSkill(
                      SkillParams.builder()
                          .type(ANTHROPIC)
                          .skillId("docx")
                          .version("latest")
                          .build()
                  )
                  .build()
          )
          .addUserMessage("Write a 2-page report on the benefits of renewable energy")
          .addTool(CodeExecutionTool20260521.builder().build())
          .build()
  );

  ```

  ```php PHP
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  $response = $client->beta->messages->create(
      model: 'claude-opus-5',
      maxTokens: 16000,
      betas: ['skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'docx', 'version' => 'latest'],
          ],
      ],
      messages: [
          [
              'role' => 'user',
              'content' => 'Write a 2-page report on the benefits of renewable energy',
          ],
      ],
      tools: [new BetaCodeExecutionTool20260521()],
  );
  ```

  ```ruby Ruby
  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 16_000,
    container: {
      skills: [{type: "anthropic", skill_id: "docx", version: "latest"}]
    },
    messages: [
      {
        role: "user",
        content: "Write a 2-page report on the benefits of renewable energy"
      }
    ],
    tools: [{type: "code_execution_20260521", name: "code_execution"}]
  )
  ```
</CodeGroup>

### Generate a PDF

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 16000,
      "container": {
        "skills": [{"type": "anthropic", "skill_id": "pdf", "version": "latest"}]
      },
      "messages": [
        {"role": "user", "content": "Generate a PDF invoice template"}
      ],
      "tools": [{"type": "code_execution_20260521", "name": "code_execution"}]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 16000
  container:
    skills:
      - type: anthropic
        skill_id: pdf
        version: latest
  messages:
    - role: user
      content: Generate a PDF invoice template
  tools:
    - type: code_execution_20260521
      name: code_execution
  YAML
  ```

  ```python Python
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=16000,
      container={
          "skills": [{"type": "anthropic", "skill_id": "pdf", "version": "latest"}]
      },
      messages=[
          {
              "role": "user",
              "content": "Generate a PDF invoice template",
          }
      ],
      tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
  )
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 16000,
    container: {
      skills: [{ type: "anthropic", skill_id: "pdf", version: "latest" }]
    },
    messages: [
      {
        role: "user",
        content: "Generate a PDF invoice template"
      }
    ],
    tools: [{ type: "code_execution_20260521", name: "code_execution" }]
  });
  ```

  ```csharp C#
  var response = await client.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5,
          MaxTokens = 16000,
          Container = new ContainerParams
          {
              Skills =
              [
                  new SkillParams
                  {
                      Type = SkillParamsType.Anthropic,
                      SkillID = "pdf",
                      Version = "latest",
                  },
              ],
          },
          Messages =
          [
              new MessageParam
              {
                  Role = Role.User,
                  Content = "Generate a PDF invoice template",
              },
          ],
          Tools = [new CodeExecutionTool20260521()],
      }
  );
  ```

  ```go Go
  response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 16000,
  	Container: anthropic.MessageCreateParamsContainerUnion{
  		OfContainers: &anthropic.ContainerParams{
  			Skills: []anthropic.SkillParams{
  				{
  					Type:    anthropic.SkillParamsTypeAnthropic,
  					SkillID: "pdf",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Generate a PDF invoice template")),
  	},
  	Tools: []anthropic.ToolUnionParam{
  		{
  			OfCodeExecutionTool20260521: &anthropic.CodeExecutionTool20260521Param{},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  Message response = client.messages().create(
      MessageCreateParams.builder()
          .model(CLAUDE_OPUS_5)
          .maxTokens(16000)
          .container(
              ContainerParams.builder()
                  .addSkill(
                      SkillParams.builder()
                          .type(ANTHROPIC)
                          .skillId("pdf")
                          .version("latest")
                          .build()
                  )
                  .build()
          )
          .addUserMessage("Generate a PDF invoice template")
          .addTool(CodeExecutionTool20260521.builder().build())
          .build()
  );

  ```

  ```php PHP
  // The PHP SDK supports container skills only through $client->beta->messages with the skills beta.
  $response = $client->beta->messages->create(
      model: 'claude-opus-5',
      maxTokens: 16000,
      betas: ['skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skill_id' => 'pdf', 'version' => 'latest'],
          ],
      ],
      messages: [
          [
              'role' => 'user',
              'content' => 'Generate a PDF invoice template',
          ],
      ],
      tools: [new BetaCodeExecutionTool20260521()],
  );
  ```

  ```ruby Ruby
  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 16_000,
    container: {
      skills: [{type: "anthropic", skill_id: "pdf", version: "latest"}]
    },
    messages: [
      {
        role: "user",
        content: "Generate a PDF invoice template"
      }
    ],
    tools: [{type: "code_execution_20260521", name: "code_execution"}]
  )
  ```
</CodeGroup>

## Next steps

<CardGroup cols={2}>
  <Card title="Skill authoring best practices" icon="edit" href="https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices">
    Learn how to write effective Skills that Claude can discover and use successfully.
  </Card>

  <Card title="Using Agent Skills with the API" icon="book" href="https://platform.claude.com/docs/en/build-with-claude/skills-guide">
    Learn how to use Agent Skills to extend Claude's capabilities through the API.
  </Card>

  <Card title="Create custom Skills" icon="code" href="https://platform.claude.com/docs/en/api/skills/create">
    Upload your own Skills for specialized tasks.
  </Card>

  <Card title="Use Skills in Claude Code" icon="terminal" href="https://code.claude.com/docs/en/skills">
    Learn about Skills in Claude Code.
  </Card>

  <Card title="Agent Skills Cookbook" icon="book" href="https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction">
    Explore example Skills and implementation patterns.
  </Card>
</CardGroup>
