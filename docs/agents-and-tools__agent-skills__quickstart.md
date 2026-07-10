# Get started with Agent Skills in the API

Learn how to use Agent Skills to create documents with the Claude API in under 10 minutes.

---

This tutorial shows you how to use Agent Skills to create a PowerPoint presentation. You'll learn how to enable Skills, make a simple request, and access the generated file.

## Prerequisites

* [Claude API key](/settings/keys)
* Python 3.7+ or curl installed
* Basic familiarity with making API requests

## Agent Skills overview

Pre-built Agent Skills extend Claude's capabilities with specialized expertise for tasks like creating documents, analyzing data, and processing files. Anthropic provides the following pre-built Agent Skills in the API:

* **PowerPoint (pptx):** Create and edit presentations
* **Excel (xlsx):** Create and analyze spreadsheets
* **Word (docx):** Create and edit documents
* **PDF (pdf):** Generate PDF documents

<Note>
  **Want to create custom Skills?** See the [Agent Skills Cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction) for examples of building your own Skills with domain-specific expertise.
</Note>

## Step 1: List available Skills

First, check what Skills are available. Use the Skills API to list all Anthropic-managed Skills:

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  # List Anthropic-managed Skills
  curl --fail-with-body -sS "https://api.anthropic.com/v1/skills?source=anthropic" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" |
    jq -r '.data[] | "\(.id): \(.display_title)"'
  ```

  ```bash CLI
  # List Anthropic-managed Skills
  ant beta:skills list --source anthropic
  ```

  ```python Python
  # List Anthropic-managed Skills
  skills = client.beta.skills.list(source="anthropic")

  for skill in skills.data:
      print(f"{skill.id}: {skill.display_title}")
  ```

  ```typescript TypeScript
  // List Anthropic-managed Skills
  const skills = await client.beta.skills.list({ source: "anthropic" });

  for (const skill of skills.data) {
    console.log(`${skill.id}: ${skill.display_title}`);
  }
  ```

  ```csharp C#
  // List Anthropic-managed Skills
  var skills = await client.Beta.Skills.List(new SkillListParams { Source = "anthropic" });

  foreach (var skill in skills.Items)
  {
      Console.WriteLine($"{skill.ID}: {skill.DisplayTitle}");
  }
  ```

  ```go Go
  // List Anthropic-managed Skills
  skills, err := client.Beta.Skills.List(ctx, anthropic.BetaSkillListParams{
  	Source: anthropic.String("anthropic"),
  })
  if err != nil {
  	panic(err)
  }

  for _, skill := range skills.Data {
  	fmt.Printf("%s: %s\n", skill.ID, skill.DisplayTitle)
  }
  ```

  ```java Java
  // List Anthropic-managed Skills
  SkillListPage skills = client.beta().skills().list(
      SkillListParams.builder().source("anthropic").build()
  );

  for (SkillListResponse skill : skills.data()) {
      IO.println(skill.id() + ": " + skill.displayTitle().orElse(""));
  }
  ```

  ```php PHP
  // List Anthropic-managed Skills
  $skills = $client->beta->skills->list(source: 'anthropic');

  foreach ($skills->data as $skill) {
      echo "{$skill->id}: {$skill->displayTitle}\n";
  }
  ```

  ```ruby Ruby
  # List Anthropic-managed Skills
  skills = client.beta.skills.list(source: "anthropic")

  skills.data.each do |skill|
    puts "#{skill.id}: #{skill.display_title}"
  end
  ```
</CodeGroup>

You see the following Skills: `pptx`, `xlsx`, `docx`, and `pdf`.

This API returns each Skill's metadata: its name and description. Claude loads this metadata at startup to know what Skills are available. This is the first level of **progressive disclosure**, where Claude discovers Skills without loading their full instructions yet.

## Step 2: Create a presentation

Now use the PowerPoint Skill to create a presentation about renewable energy. Specify Skills using the `container` parameter in the Messages API:

<CodeGroup>
  ```bash cURL
  # Create a message with the PowerPoint Skill
  response=$(
    curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
      -H "content-type: application/json" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: skills-2025-10-02" \
      -d @- <<'EOF'
  {
    "model": "claude-opus-4-8",
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
  jq -r '"stop_reason=\(.stop_reason), blocks=\(.content | length)"' <<<"$response"
  ```

  ```bash CLI
  # Create a message with the PowerPoint Skill
  response=$(ant beta:messages create --format json \
    --beta skills-2025-10-02 <<'YAML'
  model: claude-opus-4-8
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

  jq -r '"stop_reason=\(.stop_reason), blocks=\(.content | length)"' <<<"$response"
  ```

  ```python Python
  # Create a message with the PowerPoint Skill
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=16000,
      betas=["skills-2025-10-02"],
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
  const response = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    betas: ["skills-2025-10-02"],
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
  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 16000,
      Betas = ["skills-2025-10-02"],
      Container = new BetaContainerParams
      {
          Skills =
          [
              new BetaSkillParams
              {
                  Type = BetaSkillParamsType.Anthropic,
                  SkillID = "pptx",
                  Version = "latest",
              },
          ],
      },
      Messages =
      [
          new BetaMessageParam
          {
              Role = Role.User,
              Content = "Create a presentation about renewable energy with 5 slides",
          },
      ],
      Tools = [new BetaCodeExecutionTool20260521()],
  });

  Console.WriteLine($"stop_reason={response.StopReason?.Raw()}, blocks={response.Content.Count}");
  ```

  ```go Go
  // Create a message with the PowerPoint Skill
  response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Betas: []anthropic.AnthropicBeta{
  		anthropic.AnthropicBetaSkills2025_10_02,
  	},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "pptx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(
  			anthropic.NewBetaTextBlock("Create a presentation about renewable energy with 5 slides"),
  		),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{OfCodeExecutionTool20260521: &anthropic.BetaCodeExecutionTool20260521Param{}},
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Printf("stop_reason=%s, blocks=%d\n", response.StopReason, len(response.Content))
  ```

  ```java Java
  // Create a message with the PowerPoint Skill
  BetaMessage response = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(16000)
          .addBeta(AnthropicBeta.SKILLS_2025_10_02)
          .container(
              BetaContainerParams.builder()
                  .addSkill(
                      BetaSkillParams.builder()
                          .type(BetaSkillParams.Type.ANTHROPIC)
                          .skillId("pptx")
                          .version("latest")
                          .build()
                  )
                  .build()
          )
          .addUserMessage("Create a presentation about renewable energy with 5 slides")
          .addTool(BetaCodeExecutionTool20260521.builder().build())
          .build()
  );

  IO.println(
      "stop_reason=" + response.stopReason().orElse(null)
          + ", blocks=" + response.content().size()
  );
  ```

  ```php PHP
  // Create a message with the PowerPoint Skill
  $response = $client->beta->messages->create(
      model: 'claude-opus-4-8',
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
  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 16_000,
    betas: ["skills-2025-10-02"],
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

Let's break down what each part does:

* **`container.skills`:** Specifies which Skills Claude can use
* **`type: "anthropic"`:** Indicates this is an Anthropic-managed Skill
* **`skill_id: "pptx"`:** The PowerPoint Skill identifier
* **`version: "latest"`:** The Skill version set to the most recently published
* **`tools`:** Enables code execution (required for Skills)
* **Beta header:** `skills-2025-10-02`

<Note>
  The examples here use the `code_execution_20260521` tool version, which is generally available and requires no code execution beta header. Skills also work with older [code execution tool](/docs/en/agents-and-tools/tool-use/code-execution-tool) versions (such as `code_execution_20250825`); any code execution tool version satisfies the Skills requirement. Whichever version you use, keep its tool `type` and any beta header consistent with the code execution tool page, and always include `skills-2025-10-02`.
</Note>

When you make this request, Claude automatically matches your task to the relevant Skill. Since you asked for a presentation, Claude determines the PowerPoint Skill is relevant and loads its full instructions: the second level of progressive disclosure. Then Claude executes the Skill's code to create your presentation.

## Step 3: Download the created file

The presentation was created in the code execution container and saved as a file. The response includes a file reference with a file ID. Extract the file ID and download it using the Files API:

<CodeGroup>
  ```bash cURL
  # Extract file ID from the code-execution tool result. The Skill might run
  # its work through either the Python or bash code-execution tool, so check
  # both result types.
  file_id=$(jq -r '
    last(
      .content[]
      | select(.type == "code_execution_tool_result" or .type == "bash_code_execution_tool_result")
      | .content
      | select(.type == "code_execution_result" or .type == "bash_code_execution_result")
      | .content[].file_id
    ) // empty
  ' <<<"$response")

  if [[ -n "$file_id" ]]; then
    # Download the file and save it
    output_path="${TMPDIR:-/tmp}/renewable_energy.pptx"
    curl --fail-with-body -sS "https://api.anthropic.com/v1/files/$file_id/content" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: files-api-2025-04-14" \
      -o "$output_path"
    echo "Presentation saved to $output_path"
  fi
  ```

  ```bash CLI
  # Extract file ID from the code-execution tool result. The Skill might run
  # its work through either the Python or bash code-execution tool, so check
  # both result types.
  file_id=$(jq -r '
    last(
      .content[]
      | select(.type == "code_execution_tool_result"
            or .type == "bash_code_execution_tool_result")
      | .content
      | select(.type == "code_execution_result"
            or .type == "bash_code_execution_result")
      | .content[].file_id
    ) // empty
  ' <<<"$response")

  if [[ -n "$file_id" ]]; then
    # Download the file and save it
    output_path="${TMPDIR:-/tmp}/renewable_energy.pptx"
    ant beta:files download --file-id "$file_id" --output "$output_path"
    echo "Presentation saved to $output_path"
  fi
  ```

  ```python Python
  # Extract file ID from the code-execution tool result. The Skill might run
  # its work through either the Python or bash code-execution tool, so check
  # both result types.
  file_id = None
  for block in response.content:
      if block.type == "code_execution_tool_result":
          if block.content.type == "code_execution_result":
              for output in block.content.content:
                  file_id = output.file_id
      elif block.type == "bash_code_execution_tool_result":
          if block.content.type == "bash_code_execution_result":
              for output in block.content.content:
                  file_id = output.file_id

  if file_id:
      # Download the file and save it
      output_path = Path(tempfile.gettempdir()) / "renewable_energy.pptx"
      file_content = client.beta.files.download(file_id=file_id)
      file_content.write_to_file(output_path)
      print(f"Presentation saved to {output_path}")
  ```

  ```typescript TypeScript
  // Extract file ID from the code-execution tool result. The Skill might run
  // its work through either the Python or bash code-execution tool, so check
  // both result types.
  let fileId: string | undefined;
  for (const block of response.content) {
    if (block.type === "code_execution_tool_result") {
      if (block.content.type === "code_execution_result") {
        for (const output of block.content.content) {
          fileId = output.file_id;
        }
      }
    } else if (block.type === "bash_code_execution_tool_result") {
      if (block.content.type === "bash_code_execution_result") {
        for (const output of block.content.content) {
          fileId = output.file_id;
        }
      }
    }
  }

  if (fileId) {
    // Download the file and stream it to disk
    const outputPath = path.join(os.tmpdir(), "renewable_energy.pptx");
    const fileContent = await client.beta.files.download(fileId);
    await fs.writeFile(outputPath, fileContent.body!);
    console.log(`Presentation saved to ${outputPath}`);
  }
  ```

  ```csharp C#
  // Extract the file ID from the code-execution tool result. The Skill might
  // run its work through either the Python or bash code-execution tool, so
  // check both result types.
  string? fileId = null;
  foreach (var block in response.Content)
  {
      if (block.TryPickCodeExecutionToolResult(out var codeResult)
          && codeResult.Content.TryPickResultBlock(out var codeResultBlock))
      {
          foreach (var output in codeResultBlock.Content)
          {
              fileId = output.FileID;
          }
      }
      else if (block.TryPickBashCodeExecutionToolResult(out var bashResult)
          && bashResult.Content.TryPickBetaBashCodeExecutionResultBlock(out var bashResultBlock))
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
      using var download = await client.Beta.Files.Download(fileId);
      await using var source = await download.ReadAsStream();
      await using var destination = File.Create(outputPath);
      await source.CopyToAsync(destination);
      Console.WriteLine($"Presentation saved to {outputPath}");
  }
  ```

  ```go Go
  // Extract file ID from the code-execution tool result. The Skill might run
  // its work through either the Python or bash code-execution tool, so check
  // both result types.
  var fileID string
  for _, block := range response.Content {
  	switch result := block.AsAny().(type) {
  	case anthropic.BetaCodeExecutionToolResultBlock:
  		if result.Content.Type == "code_execution_result" {
  			for _, output := range result.Content.Content {
  				fileID = output.FileID
  			}
  		}
  	case anthropic.BetaBashCodeExecutionToolResultBlock:
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
  	fileContent, err := client.Beta.Files.Download(ctx, fileID, anthropic.BetaFileDownloadParams{})
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
  // Extract file ID from the code-execution tool result. The Skill might run
  // its work through either the Python or bash code-execution tool, so check
  // both result types.
  String fileId = null;
  for (BetaContentBlock block : response.content()) {
      if (block.isCodeExecutionToolResult()) {
          var content = block.asCodeExecutionToolResult().content();
          if (content.isResultBlock()) {
              for (var output : content.asResultBlock().content()) {
                  fileId = output.fileId();
              }
          }
      } else if (block.isBashCodeExecutionToolResult()) {
          var content = block.asBashCodeExecutionToolResult().content();
          if (content.isBetaBashCodeExecutionResultBlock()) {
              for (var output : content.asBetaBashCodeExecutionResultBlock().content()) {
                  fileId = output.fileId();
              }
          }
      }
  }

  if (fileId != null) {
      // Download the file and save it
      Path outputPath = Files.createTempFile("renewable_energy", ".pptx");
      try (HttpResponse fileContent = client.beta().files().download(fileId)) {
          Files.copy(fileContent.body(), outputPath, StandardCopyOption.REPLACE_EXISTING);
      }
      IO.println("Presentation saved to " + outputPath);
  }
  ```

  ```php PHP
  // Extract file ID from the code-execution tool result. The Skill might run
  // its work through either the Python or bash code-execution tool, so check
  // both result types.
  $fileId = null;
  foreach ($response->content as $block) {
      if ($block instanceof BetaCodeExecutionToolResultBlock) {
          if ($block->content instanceof BetaCodeExecutionResultBlock) {
              foreach ($block->content->content as $output) {
                  $fileId = $output->fileID;
              }
          }
      } elseif ($block instanceof BetaBashCodeExecutionToolResultBlock) {
          if ($block->content instanceof BetaBashCodeExecutionResultBlock) {
              foreach ($block->content->content as $output) {
                  $fileId = $output->fileID;
              }
          }
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
  # Extract file ID from the code-execution tool result. The Skill might run
  # its work through either the Python or bash code-execution tool, so check
  # both result types.
  file_id = nil
  response.content.each do |block|
    case block.type
    when :code_execution_tool_result
      if block.content[:type] == "code_execution_result"
        block.content[:content].each { |output| file_id = output[:file_id] }
      end
    when :bash_code_execution_tool_result
      if block.content[:type] == "bash_code_execution_result"
        block.content[:content].each { |output| file_id = output[:file_id] }
      end
    end
  end

  if file_id
    # Download the file and save it
    output_path = File.join(Dir.tmpdir, "renewable_energy.pptx")
    file_content = client.beta.files.download(file_id)
    File.binwrite(output_path, file_content.read)
    puts "Presentation saved to #{output_path}"
  end
  ```
</CodeGroup>

<Note>
  For complete details on working with generated files, see the [code execution tool documentation](/docs/en/agents-and-tools/tool-use/code-execution-tool#retrieve-generated-files).
</Note>

## Try more examples

Now that you've created your first document with Skills, try these variations:

### Create a spreadsheet

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 16000,
      "container": {
        "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
      },
      "messages": [
        {"role": "user", "content": "Create a quarterly sales tracking spreadsheet with sample data"}
      ],
      "tools": [{"type": "code_execution_20260521", "name": "code_execution"}]
    }' | jq -r '"stop_reason=\(.stop_reason)"'
  ```

  ```bash CLI
  ant beta:messages create --format json \
    --beta skills-2025-10-02 <<'YAML' | jq -r '"stop_reason=\(.stop_reason)"'
  model: claude-opus-4-8
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
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=16000,
      betas=["skills-2025-10-02"],
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
  const response = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    betas: ["skills-2025-10-02"],
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
  var response = await client.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Betas = ["skills-2025-10-02"],
          Container = new BetaContainerParams
          {
              Skills =
              [
                  new BetaSkillParams
                  {
                      Type = BetaSkillParamsType.Anthropic,
                      SkillID = "xlsx",
                      Version = "latest",
                  },
              ],
          },
          Messages =
          [
              new BetaMessageParam
              {
                  Role = Role.User,
                  Content = "Create a quarterly sales tracking spreadsheet with sample data",
              },
          ],
          Tools = [new BetaCodeExecutionTool20260521()],
      }
  );
  ```

  ```go Go
  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Betas: []anthropic.AnthropicBeta{
  		anthropic.AnthropicBetaSkills2025_10_02,
  	},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "xlsx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Create a quarterly sales tracking spreadsheet with sample data")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{
  			OfCodeExecutionTool20260521: &anthropic.BetaCodeExecutionTool20260521Param{},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  void main() {
      BetaMessage response = client.beta().messages().create(
          MessageCreateParams.builder()
              .model(CLAUDE_OPUS_4_8)
              .maxTokens(16000)
              .addBeta(AnthropicBeta.SKILLS_2025_10_02)
              .container(
                  BetaContainerParams.builder()
                      .addSkill(
                          BetaSkillParams.builder()
                              .type(ANTHROPIC)
                              .skillId("xlsx")
                              .version("latest")
                              .build()
                      )
                      .build()
              )
              .addUserMessage("Create a quarterly sales tracking spreadsheet with sample data")
              .addTool(BetaCodeExecutionTool20260521.builder().build())
              .build()
      );

  ```

  ```php PHP
  $response = $client->beta->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 16000,
      betas: ['skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skillID' => 'xlsx', 'version' => 'latest'],
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
  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 16_000,
    betas: ["skills-2025-10-02"],
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
    -H "anthropic-beta: skills-2025-10-02" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 16000,
      "container": {
        "skills": [{"type": "anthropic", "skill_id": "docx", "version": "latest"}]
      },
      "messages": [
        {"role": "user", "content": "Write a 2-page report on the benefits of renewable energy"}
      ],
      "tools": [{"type": "code_execution_20260521", "name": "code_execution"}]
    }' | jq -r '"stop_reason=\(.stop_reason)"'
  ```

  ```bash CLI
  ant beta:messages create --format json \
    --beta skills-2025-10-02 <<'YAML' | jq -r '"stop_reason=\(.stop_reason)"'
  model: claude-opus-4-8
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
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=16000,
      betas=["skills-2025-10-02"],
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
  const response = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    betas: ["skills-2025-10-02"],
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
  var response = await client.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Betas = ["skills-2025-10-02"],
          Container = new BetaContainerParams
          {
              Skills =
              [
                  new BetaSkillParams
                  {
                      Type = BetaSkillParamsType.Anthropic,
                      SkillID = "docx",
                      Version = "latest",
                  },
              ],
          },
          Messages =
          [
              new BetaMessageParam
              {
                  Role = Role.User,
                  Content = "Write a 2-page report on the benefits of renewable energy",
              },
          ],
          Tools = [new BetaCodeExecutionTool20260521()],
      }
  );
  ```

  ```go Go
  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Betas: []anthropic.AnthropicBeta{
  		anthropic.AnthropicBetaSkills2025_10_02,
  	},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "docx",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Write a 2-page report on the benefits of renewable energy")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{
  			OfCodeExecutionTool20260521: &anthropic.BetaCodeExecutionTool20260521Param{},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  void main() {
      BetaMessage response = client.beta().messages().create(
          MessageCreateParams.builder()
              .model(CLAUDE_OPUS_4_8)
              .maxTokens(16000)
              .addBeta(AnthropicBeta.SKILLS_2025_10_02)
              .container(
                  BetaContainerParams.builder()
                      .addSkill(
                          BetaSkillParams.builder()
                              .type(ANTHROPIC)
                              .skillId("docx")
                              .version("latest")
                              .build()
                      )
                      .build()
              )
              .addUserMessage("Write a 2-page report on the benefits of renewable energy")
              .addTool(BetaCodeExecutionTool20260521.builder().build())
              .build()
      );

  ```

  ```php PHP
  $response = $client->beta->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 16000,
      betas: ['skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skillID' => 'docx', 'version' => 'latest'],
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
  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 16_000,
    betas: ["skills-2025-10-02"],
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
    -H "anthropic-beta: skills-2025-10-02" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 16000,
      "container": {
        "skills": [{"type": "anthropic", "skill_id": "pdf", "version": "latest"}]
      },
      "messages": [
        {"role": "user", "content": "Generate a PDF invoice template"}
      ],
      "tools": [{"type": "code_execution_20260521", "name": "code_execution"}]
    }' | jq -r '"stop_reason=\(.stop_reason)"'
  ```

  ```bash CLI
  ant beta:messages create --format json \
    --beta skills-2025-10-02 <<'YAML' | jq -r '"stop_reason=\(.stop_reason)"'
  model: claude-opus-4-8
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
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=16000,
      betas=["skills-2025-10-02"],
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
  const response = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    betas: ["skills-2025-10-02"],
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
  var response = await client.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Betas = ["skills-2025-10-02"],
          Container = new BetaContainerParams
          {
              Skills =
              [
                  new BetaSkillParams
                  {
                      Type = BetaSkillParamsType.Anthropic,
                      SkillID = "pdf",
                      Version = "latest",
                  },
              ],
          },
          Messages =
          [
              new BetaMessageParam
              {
                  Role = Role.User,
                  Content = "Generate a PDF invoice template",
              },
          ],
          Tools = [new BetaCodeExecutionTool20260521()],
      }
  );
  ```

  ```go Go
  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Betas: []anthropic.AnthropicBeta{
  		anthropic.AnthropicBetaSkills2025_10_02,
  	},
  	Container: anthropic.BetaMessageNewParamsContainerUnion{
  		OfContainers: &anthropic.BetaContainerParams{
  			Skills: []anthropic.BetaSkillParams{
  				{
  					Type:    anthropic.BetaSkillParamsTypeAnthropic,
  					SkillID: "pdf",
  					Version: anthropic.String("latest"),
  				},
  			},
  		},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Generate a PDF invoice template")),
  	},
  	Tools: []anthropic.BetaToolUnionParam{
  		{
  			OfCodeExecutionTool20260521: &anthropic.BetaCodeExecutionTool20260521Param{},
  		},
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  void main() {
      BetaMessage response = client.beta().messages().create(
          MessageCreateParams.builder()
              .model(CLAUDE_OPUS_4_8)
              .maxTokens(16000)
              .addBeta(AnthropicBeta.SKILLS_2025_10_02)
              .container(
                  BetaContainerParams.builder()
                      .addSkill(
                          BetaSkillParams.builder()
                              .type(ANTHROPIC)
                              .skillId("pdf")
                              .version("latest")
                              .build()
                      )
                      .build()
              )
              .addUserMessage("Generate a PDF invoice template")
              .addTool(BetaCodeExecutionTool20260521.builder().build())
              .build()
      );

  ```

  ```php PHP
  $response = $client->beta->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 16000,
      betas: ['skills-2025-10-02'],
      container: [
          'skills' => [
              ['type' => 'anthropic', 'skillID' => 'pdf', 'version' => 'latest'],
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
  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 16_000,
    betas: ["skills-2025-10-02"],
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

Now that you've used pre-built Agent Skills, you can:

<CardGroup cols={2}>
  <Card title="API Guide" icon="book" href="/docs/en/build-with-claude/skills-guide">
    Use Skills with the Claude API
  </Card>

  <Card title="Create Custom Skills" icon="code" href="/docs/en/api/skills/create-skill">
    Upload your own Skills for specialized tasks
  </Card>

  <Card title="Authoring Guide" icon="edit" href="/docs/en/agents-and-tools/agent-skills/best-practices">
    Learn best practices for writing effective Skills
  </Card>

  <Card title="Use Skills in Claude Code" icon="terminal" href="https://code.claude.com/docs/en/skills">
    Learn about Skills in Claude Code
  </Card>

  <Card title="Agent Skills Cookbook" icon="book" href="https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction">
    Explore example Skills and implementation patterns
  </Card>
</CardGroup>
