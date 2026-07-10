# Skills

Attach reusable, filesystem-based expertise to your agent for domain-specific workflows.

---

Skills are reusable, filesystem-based resources that give your agent domain-specific expertise: workflows, context, and best practices that turn a general-purpose agent into a specialist. Unlike prompts (conversation-level instructions for one-off tasks), skills load on demand, only impacting the context window when needed.

You can attach two types of skill. Both work the same way: your agent invokes them automatically when they are relevant to the task.

* **Pre-built Anthropic skills:** Common document tasks such as PowerPoint, Excel, Word, and PDF handling (`pptx`, `xlsx`, `docx`, `pdf`).
* **Custom skills:** Skills you author and upload to your workspace.

To learn how to author custom skills, see [Agent Skills](/docs/en/agents-and-tools/agent-skills/overview) and [Skill authoring best practices](/docs/en/agents-and-tools/agent-skills/best-practices). To upload a custom skill to your workspace, see [Create a custom skill](#create-a-custom-skill).

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Create a custom skill

A custom skill is a directory containing a `SKILL.md` file plus any supporting files, uploaded to your workspace as a zip archive or as individual files. Creating the skill returns the `skill_*` ID you reference when attaching it to an agent. Anthropic pre-built skills are already available in every workspace and don't require this step. To use only pre-built skills, skip to [Attach skills to an agent](#attach-skills-to-an-agent).

When you call the Skills API directly with cURL or the CLI, pass the `anthropic-beta: skills-2025-10-02` header explicitly. The SDKs send it automatically.

These examples omit the optional `display_title` field, so the skill's title is derived from `SKILL.md`. An explicitly passed `display_title` must be unique among the custom skills in your workspace.

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/skills" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: skills-2025-10-02" \
    -F "files[]=@example_skill.zip"
  ```

  ```bash CLI
  ant beta:skills create \
    --file example_skill.zip \
    --beta skills-2025-10-02
  ```

  ```python Python
  import anthropic
  from anthropic.lib import files_from_dir

  client = anthropic.Anthropic()

  skill = client.beta.skills.create(
      files=files_from_dir("example_skill"),
  )

  print(f"Created skill: {skill.id}")
  print(f"Latest version: {skill.latest_version}")
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { toFile } from "@anthropic-ai/sdk";
  import fs from "node:fs";

  const client = new Anthropic();

  const skill = await client.beta.skills.create({
    files: [await toFile(fs.createReadStream("example_skill.zip"), "example_skill.zip")]
  });

  console.log(`Created skill: ${skill.id}`);
  console.log(`Latest version: ${skill.latest_version}`);
  ```

  ```csharp C#
  using System.IO;
  using Anthropic;
  using Anthropic.Models.Beta.Skills;

  AnthropicClient client = new();

  var parameters = new SkillCreateParams
  {
      Files = [
          new FileStream("example_skill.zip", FileMode.Open, FileAccess.Read)
      ],
  };

  var skill = await client.Beta.Skills.Create(parameters);

  Console.WriteLine($"Created skill: {skill.ID}");
  Console.WriteLine($"Latest version: {skill.LatestVersion}");
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"io"
  	"log"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func main() {
  	client := anthropic.NewClient()

  	zipFile, err := os.Open("example_skill.zip")
  	if err != nil {
  		log.Fatal(err)
  	}
  	defer zipFile.Close()

  	skill, err := client.Beta.Skills.New(context.TODO(), anthropic.BetaSkillNewParams{
  		Files: []io.Reader{zipFile},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	fmt.Printf("Created skill: %s\n", skill.ID)
  	fmt.Printf("Latest version: %s\n", skill.LatestVersion)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.MultipartField;
  import com.anthropic.models.beta.skills.SkillCreateParams;
  import com.anthropic.models.beta.skills.SkillCreateResponse;
  import java.io.IOException;
  import java.io.InputStream;
  import java.nio.file.Files;
  import java.nio.file.Path;
  import java.util.List;

  public class SkillCreate {
      public static void main(String[] args) throws IOException {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          SkillCreateParams params = SkillCreateParams.builder()
              .files(MultipartField.<List<InputStream>>builder()
                  .value(List.of(Files.newInputStream(Path.of("example_skill.zip"))))
                  .filename("example_skill.zip")
                  .contentType("application/zip")
                  .build())
              .build();

          SkillCreateResponse skill = client.beta().skills().create(params);

          System.out.println("Created skill: " + skill.id());
          System.out.println("Latest version: " + skill.latestVersion().orElseThrow());
      }
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Client;
  use Anthropic\Core\FileParam;

  $client = new Client();

  $skill = $client->beta->skills->create(
      files: [
          FileParam::fromResource(fopen('example_skill.zip', 'r'))
      ],
  );

  echo "Created skill: {$skill->id}\n";
  echo "Latest version: {$skill->latestVersion}\n";
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  skill = client.beta.skills.create(
    files: [
      File.open("example_skill.zip", "rb")
    ]
  )

  puts "Created skill: #{skill.id}"
  puts "Latest version: #{skill.latest_version}"
  ```
</CodeGroup>

To list, retrieve, delete, and version custom skills, see [Managing custom skills](/docs/en/build-with-claude/skills-guide#managing-custom-skills). For the full request and response schemas, see the [Create Skill API reference](/docs/en/api/beta/skills/create). Skill bundles upload directly to the Skills API rather than through the [Files API](/docs/en/build-with-claude/files).

## Attach skills to an agent

Attach skills when creating an agent. Each [session](/docs/en/managed-agents/sessions) supports up to 20 skills total, counted across every agent in the session (see [Multi-agent sessions](/docs/en/managed-agents/multi-agent)).

Each entry in the `skills` array uses the following fields:

| Field      | Description                                                                                                                                                                                               |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`     | Either `anthropic` for pre-built skills or `custom` for workspace-authored skills.                                                                                                                        |
| `skill_id` | The skill identifier. For Anthropic skills, use the short name (for example, `xlsx`). For custom skills, use the `skill_*` ID returned at creation (see [Create a custom skill](#create-a-custom-skill)). |
| `version`  | Custom skills only. Pin to a specific version or use `latest`. Optional. Defaults to `latest` when omitted.                                                                                               |

<CodeGroup defaultLanguage="CLI">
  ```bash cURL
  agent=$(curl -sS https://api.anthropic.com/v1/agents \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    --json @- <<'EOF'
  {
    "name": "Financial Analyst",
    "model": "claude-opus-4-8",
    "system": "You are a financial analysis agent.",
    "skills": [
      {"type": "anthropic", "skill_id": "xlsx"},
      {"type": "custom", "skill_id": "skill_abc123", "version": "latest"}
    ]
  }
  EOF
  )
  ```

  ```bash CLI
  ant beta:agents create <<'YAML'
  name: Financial Analyst
  model: claude-opus-4-8
  system: You are a financial analysis agent.
  skills:
    - type: anthropic
      skill_id: xlsx
    - type: custom
      skill_id: skill_abc123
      version: latest
  YAML
  ```

  ```python Python
  agent = client.beta.agents.create(
      name="Financial Analyst",
      model="claude-opus-4-8",
      system="You are a financial analysis agent.",
      skills=[
          {
              "type": "anthropic",
              "skill_id": "xlsx",
          },
          {
              "type": "custom",
              "skill_id": "skill_abc123",
              "version": "latest",
          },
      ],
  )
  ```

  ```typescript TypeScript
  const agent = await client.beta.agents.create({
    name: "Financial Analyst",
    model: "claude-opus-4-8",
    system: "You are a financial analysis agent.",
    skills: [
      {
        type: "anthropic",
        skill_id: "xlsx"
      },
      {
        type: "custom",
        skill_id: "skill_abc123",
        version: "latest"
      }
    ]
  });
  ```

  ```csharp C#
  var agent = await client.Beta.Agents.Create(new()
  {
      Name = "Financial Analyst",
      Model = BetaManagedAgentsModel.ClaudeOpus4_8,
      System = "You are a financial analysis agent.",
      Skills =
      [
          new BetaManagedAgentsAnthropicSkillParams { Type = BetaManagedAgentsAnthropicSkillParamsType.Anthropic, SkillID = "xlsx" },
          new BetaManagedAgentsCustomSkillParams { Type = BetaManagedAgentsCustomSkillParamsType.Custom, SkillID = "skill_abc123", Version = "latest" },
      ],
  });
  ```

  ```go Go
  agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
  	Name: "Financial Analyst",
  	Model: anthropic.BetaManagedAgentsModelConfigParams{
  		ID: "claude-opus-4-8",
  	},
  	System: anthropic.String("You are a financial analysis agent."),
  	Skills: []anthropic.BetaManagedAgentsSkillParamsUnion{
  		{OfAnthropic: &anthropic.BetaManagedAgentsAnthropicSkillParams{
  			SkillID: "xlsx",
  			Type:    anthropic.BetaManagedAgentsAnthropicSkillParamsTypeAnthropic,
  		}},
  		{OfCustom: &anthropic.BetaManagedAgentsCustomSkillParams{
  			SkillID: "skill_abc123",
  			Type:    anthropic.BetaManagedAgentsCustomSkillParamsTypeCustom,
  			Version: anthropic.String("latest"),
  		}},
  	},
  })
  if err != nil {
  	panic(err)
  }
  _ = agent
  ```

  ```java Java
  var agent = client.beta().agents().create(
      AgentCreateParams.builder()
          .name("Financial Analyst")
          .model(BetaManagedAgentsModel.CLAUDE_OPUS_4_8)
          .system("You are a financial analysis agent.")
          .addSkill(
              BetaManagedAgentsAnthropicSkillParams.builder()
                  .type(BetaManagedAgentsAnthropicSkillParams.Type.ANTHROPIC)
                  .skillId("xlsx")
                  .build()
          )
          .addSkill(
              BetaManagedAgentsCustomSkillParams.builder()
                  .type(BetaManagedAgentsCustomSkillParams.Type.CUSTOM)
                  .skillId("skill_abc123")
                  .version("latest")
                  .build()
          )
          .build()
  );
  ```

  ```php PHP
  $agent = $client->beta->agents->create(
      name: 'Financial Analyst',
      model: 'claude-opus-4-8',
      system: 'You are a financial analysis agent.',
      skills: [
          ['type' => 'anthropic', 'skill_id' => 'xlsx'],
          ['type' => 'custom', 'skill_id' => 'skill_abc123', 'version' => 'latest'],
      ],
  );
  ```

  ```ruby Ruby
  agent = client.beta.agents.create(
    name: "Financial Analyst",
    model: "claude-opus-4-8",
    system_: "You are a financial analysis agent.",
    skills: [
      {type: "anthropic", skill_id: "xlsx"},
      {type: "custom", skill_id: "skill_abc123", version: "latest"}
    ]
  )
  ```
</CodeGroup>

## Next steps

<CardGroup cols={2}>
  <Card title="Cloud environment setup" icon="settings" href="/docs/en/managed-agents/environments">
    Customize cloud sandboxes for your sessions.
  </Card>

  <Card title="Using Agent Skills with the API" icon="code" href="/docs/en/build-with-claude/skills-guide">
    Learn how to use Agent Skills to extend Claude's capabilities through the API.
  </Card>

  <Card title="Files API" icon="file" href="/docs/en/build-with-claude/files">
    Upload files once and reference them across API requests.
  </Card>

  <Card title="Get started with Agent Skills in the API" icon="graduation-cap" href="/docs/en/agents-and-tools/agent-skills/quickstart">
    Learn how to use Agent Skills to create documents with the Claude API in under 10 minutes.
  </Card>
</CardGroup>
