# Define outcomes

Tell the agent what 'done' looks like, and let it iterate until it gets there.

---

An outcome tells the session what the end result should look like and how to measure its quality. The agent works toward that target, self-evaluating and iterating until the outcome is met.

When you define an outcome, the harness automatically provisions a *grader* to evaluate the artifact against a rubric. The grader uses a separate context window to avoid being influenced by the main agent's implementation choices.

The grader returns an explanation summarizing which criteria passed or failed, or confirming that the artifact satisfies the rubric. That feedback is handed back to the agent for the next iteration.

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Create a rubric

A rubric is a markdown document describing per-criterion scoring. The rubric is required.

<Accordion title="Tips for writing effective rubrics">
  Structure the rubric as explicit, gradeable criteria, such as "The CSV contains a price column with numeric values" rather than "The data looks good." The grader scores each criterion independently, so vague criteria produce noisy evaluations.

  If you don't have a rubric on hand, try giving Claude an example of a known-good artifact and asking it to analyze what makes that content good, then turn that analysis into a rubric. This middle-ground approach often produces better results than writing criteria from scratch.
</Accordion>

Example rubric:

```markdown
# DCF Model Rubric

## Revenue Projections
- Uses historical revenue data from the last 5 fiscal years
- Projects revenue for at least 5 years forward
- Growth rate assumptions are explicitly stated and reasonable

## Cost Structure
- COGS and operating expenses are modeled separately
- Margins are consistent with historical trends or deviations are justified

## Discount Rate
- WACC is calculated with stated assumptions for cost of equity and cost of debt
- Beta, risk-free rate, and equity risk premium are sourced or justified

## Terminal Value
- Uses either perpetuity growth or exit multiple method (stated which)
- Terminal growth rate does not exceed long-term GDP growth

## Output Quality
- All figures are in a single .xlsx file with clearly labeled sheets
- Key assumptions are on a separate "Assumptions" sheet
- Sensitivity analysis on WACC and terminal growth rate is included
```

Pass the rubric as inline text on `user.define_outcome` (see [Create a session with an outcome](#create-a-session-with-an-outcome)), or upload it through the Files API for reuse across sessions.

<Note>
  Uploading through the Files API requires the `files-api-2025-04-14` beta header, which the SDKs send automatically. The curl example passes its headers explicitly.
</Note>

<CodeGroup>
  ```bash curl
  rubric=$(curl -fsSL https://api.anthropic.com/v1/files \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01,files-api-2025-04-14" \
    -F file=@/tmp/rubric.md)
  rubric_id=$(jq -r '.id' <<<"$rubric")
  printf 'Uploaded rubric: %s\n' "$rubric_id"
  ```

  ```bash CLI
  RUBRIC_ID=$(ant beta:files upload \
    --file /tmp/rubric.md \
    --transform id --raw-output)
  ```

  ```python Python
  import time
  from pathlib import Path

  from anthropic import Anthropic

  client = Anthropic()

  RUBRIC = """# DCF Model Rubric

  ## Revenue Projections
  - Uses historical revenue data from the last 5 fiscal years
  - Projects revenue for at least 5 years forward

  ## Output Quality
  - All figures are in a single .xlsx file with clearly labeled sheets
  """
  Path("/tmp/rubric.md").write_text(RUBRIC)

  rubric = client.beta.files.upload(file=Path("/tmp/rubric.md"))
  print(f"Uploaded rubric: {rubric.id}")
  ```

  ```typescript TypeScript
  import { writeFile, readFile } from "node:fs/promises";

  import Anthropic from "@anthropic-ai/sdk";
  import { toFile } from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const RUBRIC = `# DCF Model Rubric

  ## Revenue Projections
  - Uses historical revenue data from the last 5 fiscal years
  - Projects revenue for at least 5 years forward

  ## Output Quality
  - All figures are in a single .xlsx file with clearly labeled sheets
  `;
  await writeFile("/tmp/rubric.md", RUBRIC);

  const rubric = await client.beta.files.upload({
    file: await toFile(readFile("/tmp/rubric.md"), "/tmp/rubric.md"),
  });
  console.log(`Uploaded rubric: ${rubric.id}`);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta.Agents;
  using Anthropic.Models.Beta.Environments;
  using Anthropic.Models.Beta.Files;
  using Anthropic.Models.Beta.Sessions;
  using Anthropic.Models.Beta.Sessions.Events;

  var client = new AnthropicClient();

  const string Rubric = """
      # DCF Model Rubric

      ## Revenue Projections
      - Uses historical revenue data from the last 5 fiscal years
      - Projects revenue for at least 5 years forward

      ## Output Quality
      - All figures are in a single .xlsx file with clearly labeled sheets
      """;
  await File.WriteAllTextAsync("/tmp/rubric.md", Rubric);

  var rubric = await client.Beta.Files.Upload(new()
  {
      File = File.OpenRead("/tmp/rubric.md"),
  });
  Console.WriteLine($"Uploaded rubric: {rubric.ID}");
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"io"
  	"os"
  	"time"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  const rubric = `# DCF Model Rubric

  ## Revenue Projections
  - Uses historical revenue data from the last 5 fiscal years
  - Projects revenue for at least 5 years forward

  ## Output Quality
  - All figures are in a single .xlsx file with clearly labeled sheets
  `

  func main() {
  	ctx := context.Background()
  	client := anthropic.NewClient()

  	if err := os.WriteFile("/tmp/rubric.md", []byte(rubric), 0o644); err != nil {
  		panic(err)
  	}

  	f, err := os.Open("/tmp/rubric.md")
  	if err != nil {
  		panic(err)
  	}

  	uploaded, err := client.Beta.Files.Upload(ctx, anthropic.BetaFileUploadParams{
  		File: anthropic.File(f, "rubric.md", "text/markdown"),
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Printf("Uploaded rubric: %s\n", uploaded.ID)
  ```

  ```java Java
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.http.HttpResponse;
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.agents.AgentCreateParams;
  import com.anthropic.models.beta.agents.BetaManagedAgentsAgentToolset20260401Params;
  import com.anthropic.models.beta.agents.BetaManagedAgentsModel;
  import com.anthropic.models.beta.environments.BetaCloudConfigParams;
  import com.anthropic.models.beta.environments.EnvironmentCreateParams;
  import com.anthropic.models.beta.files.FileListParams;
  import com.anthropic.models.beta.files.FileUploadParams;
  import com.anthropic.models.beta.sessions.SessionCreateParams;
  import com.anthropic.models.beta.sessions.events.BetaManagedAgentsTextRubricParams;
  import com.anthropic.models.beta.sessions.events.BetaManagedAgentsUserDefineOutcomeEventParams;
  import com.anthropic.models.beta.sessions.events.BetaManagedAgentsUserInterruptEventParams;
  import com.anthropic.models.beta.sessions.events.EventSendParams;

  import java.io.InputStream;
  import java.nio.file.Files;
  import java.nio.file.Path;
  import java.nio.file.StandardCopyOption;

  void main() throws Exception {
      var client = AnthropicOkHttpClient.fromEnv();

      var RUBRIC = """
          # DCF Model Rubric

          ## Revenue Projections
          - Uses historical revenue data from the last 5 fiscal years
          - Projects revenue for at least 5 years forward

          ## Output Quality
          - All figures are in a single .xlsx file with clearly labeled sheets
          """;
      Files.writeString(Path.of("/tmp/rubric.md"), RUBRIC);

      var rubric = client.beta().files().upload(
          FileUploadParams.builder()
              .file(Path.of("/tmp/rubric.md"))
              .build());
      IO.println("Uploaded rubric: " + rubric.id());
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Core\FileParam;

  $client = new Client();

  $rubricText = <<<'MD'
  # DCF Model Rubric

  ## Revenue Projections
  - Uses historical revenue data from the last 5 fiscal years
  - Projects revenue for at least 5 years forward

  ## Output Quality
  - All figures are in a single .xlsx file with clearly labeled sheets
  MD;
  file_put_contents('/tmp/rubric.md', $rubricText);

  $rubric = $client->beta->files->upload(
      file: FileParam::fromResource(fopen('/tmp/rubric.md', 'r'), contentType: 'text/markdown'),
  );
  echo "Uploaded rubric: {$rubric->id}\n";
  ```

  ```ruby Ruby
  require "anthropic"
  require "pathname"

  client = Anthropic::Client.new

  RUBRIC = <<~MD
    # DCF Model Rubric

    ## Revenue Projections
    - Uses historical revenue data from the last 5 fiscal years
    - Projects revenue for at least 5 years forward

    ## Output Quality
    - All figures are in a single .xlsx file with clearly labeled sheets
  MD
  File.write("/tmp/rubric.md", RUBRIC)

  rubric = client.beta.files.upload(file: Pathname.new("/tmp/rubric.md"))
  puts "Uploaded rubric: #{rubric.id}"
  ```
</CodeGroup>

## Create a session with an outcome

The following examples create a [session](/docs/en/managed-agents/sessions) for an existing [agent](/docs/en/managed-agents/agent-setup) and [environment](/docs/en/managed-agents/environments) (both created separately), then send a `user.define_outcome` event. The agent begins work immediately. No additional user message event is required.

<CodeGroup>
  ```bash curl
  # Create a session
  session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    --json @- <<EOF
  {
    "agent": "$agent_id",
    "environment_id": "$environment_id",
    "title": "Financial analysis on Costco"
  }
  EOF
  )
  session_id=$(jq -r '.id' <<<"$session")

  # Define the outcome — agent starts working on receipt
  curl -fsSL "https://api.anthropic.com/v1/sessions/$session_id/events" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    --json @- >/dev/null <<EOF
  {
    "events": [
      {
        "type": "user.define_outcome",
        "description": "Build a DCF model for Costco in .xlsx",
        "rubric": {"type": "text", "content": "# DCF Model Rubric\n..."},
        "max_iterations": 5
      }
    ]
  }
  EOF
  # or: "rubric": {"type": "file", "file_id": "$rubric_id"}
  # "max_iterations" is optional; default 3, max 20
  ```

  ```bash CLI
  # Create a session
  SESSION_ID=$(ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ENVIRONMENT_ID" \
    --title "Financial analysis on Costco" \
    --transform id --raw-output)

  # Define the outcome — agent starts working on receipt
  ant beta:sessions:events send \
    --session-id "$SESSION_ID" <<YAML
  events:
    - type: user.define_outcome
      description: Build a DCF model for Costco in .xlsx
      rubric: {type: file, file_id: $RUBRIC_ID}
      # or: rubric: {type: text, content: "..."}
      max_iterations: 5  # optional; default 3, max 20
  YAML
  ```

  ```python Python
  # Create a session
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      title="Financial analysis on Costco",
  )

  # Define the outcome — agent starts working on receipt
  client.beta.sessions.events.send(
      session_id=session.id,
      events=[
          {
              "type": "user.define_outcome",
              "description": "Build a DCF model for Costco in .xlsx",
              "rubric": {"type": "text", "content": RUBRIC},
              # or: "rubric": {"type": "file", "file_id": rubric.id},
              "max_iterations": 5,  # optional; default 3, max 20
          }
      ],
  )
  ```

  ```typescript TypeScript
  // Create a session
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    title: "Financial analysis on Costco",
  });

  // Define the outcome — agent starts working on receipt
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.define_outcome",
        description: "Build a DCF model for Costco in .xlsx",
        rubric: { type: "text", content: RUBRIC },
        // or: rubric: { type: "file", file_id: rubric.id },
        max_iterations: 5, // optional; default 3, max 20
      },
    ],
  });
  ```

  ```csharp C#
  // Create a session
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      Title = "Financial analysis on Costco",
  });

  // Define the outcome — agent starts working on receipt
  await client.Beta.Sessions.Events.Send(session.ID, new()
  {
      Events =
      [
          new BetaManagedAgentsUserDefineOutcomeEventParams
          {
              Type = BetaManagedAgentsUserDefineOutcomeEventParamsType.UserDefineOutcome,
              Description = "Build a DCF model for Costco in .xlsx",
              Rubric = new BetaManagedAgentsTextRubricParams
              {
                  Type = BetaManagedAgentsTextRubricParamsType.Text,
                  Content = Rubric,
              },
              // or: Rubric = new BetaManagedAgentsFileRubricParams
              //     { Type = BetaManagedAgentsFileRubricParamsType.File, FileID = rubric.ID },
              MaxIterations = 5, // optional; default 3, max 20
          },
      ],
  });
  ```

  ```go Go
  // Create a session
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent: anthropic.BetaSessionNewParamsAgentUnion{
  		OfString: anthropic.String(agent.ID),
  	},
  	EnvironmentID: environment.ID,
  	Title:         anthropic.String("Financial analysis on Costco"),
  })
  if err != nil {
  	panic(err)
  }

  // Define the outcome — agent starts working on receipt
  _, err = client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  		OfUserDefineOutcome: &anthropic.BetaManagedAgentsUserDefineOutcomeEventParams{
  			Type:        anthropic.BetaManagedAgentsUserDefineOutcomeEventParamsTypeUserDefineOutcome,
  			Description: "Build a DCF model for Costco in .xlsx",
  			Rubric: anthropic.BetaManagedAgentsUserDefineOutcomeEventParamsRubricUnion{
  				OfText: &anthropic.BetaManagedAgentsTextRubricParams{
  					Type:    anthropic.BetaManagedAgentsTextRubricParamsTypeText,
  					Content: rubric,
  				},
  			},
  			// or: OfFile: &anthropic.BetaManagedAgentsFileRubricParams{
  			//     Type: anthropic.BetaManagedAgentsFileRubricParamsTypeFile, FileID: uploaded.ID},
  			MaxIterations: anthropic.Int(5), // optional; default 3, max 20
  		},
  	}},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  // Create a session
  var session = client.beta().sessions().create(
      SessionCreateParams.builder()
          .agent(agent.id())
          .environmentId(environment.id())
          .title("Financial analysis on Costco")
          .build());

  // Define the outcome — agent starts working on receipt
  client.beta().sessions().events().send(
      session.id(),
      EventSendParams.builder()
          .addEvent(BetaManagedAgentsUserDefineOutcomeEventParams.builder()
              .type(BetaManagedAgentsUserDefineOutcomeEventParams.Type.USER_DEFINE_OUTCOME)
              .description("Build a DCF model for Costco in .xlsx")
              .rubric(BetaManagedAgentsTextRubricParams.builder()
                  .type(BetaManagedAgentsTextRubricParams.Type.TEXT)
                  .content(RUBRIC)
                  .build())
              // or: .rubric(BetaManagedAgentsFileRubricParams.builder()
              //     .type(BetaManagedAgentsFileRubricParams.Type.FILE).fileId(rubric.id()).build())
              .maxIterations(5) // optional; default 3, max 20
              .build())
          .build());
  ```

  ```php PHP
  // Create a session
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      title: 'Financial analysis on Costco',
  );

  // Define the outcome — agent starts working on receipt
  $client->beta->sessions->events->send(
      $session->id,
      events: [
          [
              'type' => 'user.define_outcome',
              'description' => 'Build a DCF model for Costco in .xlsx',
              'rubric' => ['type' => 'text', 'content' => $rubricText],
              // or: 'rubric' => ['type' => 'file', 'file_id' => $rubric->id],
              'max_iterations' => 5, // optional; default 3, max 20
          ],
      ],
  );
  ```

  ```ruby Ruby
  # Create a session
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    title: "Financial analysis on Costco"
  )

  # Define the outcome — agent starts working on receipt
  client.beta.sessions.events.send_(
    session.id,
    events: [
      {
        type: "user.define_outcome",
        description: "Build a DCF model for Costco in .xlsx",
        rubric: {type: "text", content: RUBRIC},
        # or: rubric: {type: "file", file_id: rubric.id},
        max_iterations: 5 # optional; default 3, max 20
      }
    ]
  )
  ```
</CodeGroup>

## Outcome events

Progress on an outcome-oriented session is surfaced on the events [stream](/docs/en/managed-agents/events-and-streaming).

* `agent.*` events (such as messages and tool use) show progress toward the outcome.
* `span.outcome_evaluation_*` events are only emitted for outcome-oriented sessions and show the number of iteration loops and the grader's feedback process.
* You can also send `user.message` [events](/docs/en/managed-agents/reference#event-types) to an outcome-oriented session to direct the agent's work as it progresses, but it isn't required: the agent works toward the outcome on its own, iterating until it succeeds or runs out of iterations.
* A `user.interrupt` event pauses work on the current outcome and marks the `span.outcome_evaluation_end.result` as `interrupted`, allowing you to kick off a new outcome.
* After the final outcome evaluation, the session can be continued as a conversational session, or a new outcome can be started. The session retains history of the prior outcome.

### Define outcome user event

<Note>
  Only one outcome is supported at a time, but you may chain outcomes in sequence. To do this, send a new `user.define_outcome` event after the terminal `span.outcome_evaluation_end` event of the previous outcome.
</Note>

This is the event you send to initiate an outcome. It is echoed back on receipt, including a `processed_at` timestamp and `outcome_id`.

```json
{
  "type": "user.define_outcome",
  "description": "Build a DCF model for Costco in .xlsx",
  "rubric": { "type": "file", "file_id": "file_01..." },
  "max_iterations": 5
}
```

### Outcome evaluation start

Emitted once the grader starts an evaluation over one iteration loop. The `iteration` field is a 0-indexed revision counter: `0` is the first evaluation, `1` is the re-evaluation after the first revision, and so on.

```json
{
  "type": "span.outcome_evaluation_start",
  "id": "sevt_01def...",
  "outcome_id": "outc_01a...",
  "iteration": 0,
  "processed_at": "2026-03-25T14:01:45Z"
}
```

### Outcome evaluation ongoing

Heartbeat emitted while the grader runs. The grader's internal reasoning is opaque: you see that it's working, not what it's thinking.

```json
{
  "type": "span.outcome_evaluation_ongoing",
  "id": "sevt_01ghi...",
  "outcome_id": "outc_01a...",
  "iteration": 0,
  "processed_at": "2026-03-25T14:02:10Z"
}
```

### Outcome evaluation end

Emitted after the grader finishes evaluating one iteration. The `result` field indicates what happens next.

| Result                   | Next                                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `satisfied`              | Session transitions to `idle`.                                                                                                                               |
| `needs_revision`         | Agent starts a new iteration cycle.                                                                                                                          |
| `max_iterations_reached` | One final acknowledgment turn follows before the session transitions to `idle`. No further evaluation runs.                                                  |
| `failed`                 | Session transitions to `idle`. Returned when the rubric does not apply to the deliverables, for example if the description and rubric contradict each other. |
| `interrupted`            | Only emitted if `outcome_evaluation_start` already fired before the interrupt.                                                                               |

```json
{
  "type": "span.outcome_evaluation_end",
  "id": "sevt_01jkl...",
  "outcome_evaluation_start_id": "sevt_01def...",
  "outcome_id": "outc_01a...",
  "result": "satisfied",
  "explanation": "All 12 criteria met: revenue projections use 5 years of historical data, WACC assumptions are stated, sensitivity table is included...",
  "iteration": 0,
  "usage": {
    "input_tokens": 2400,
    "output_tokens": 350,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 1800
  },
  "processed_at": "2026-03-25T14:03:00Z"
}
```

## Check outcome status

You can either listen on the [event stream](/docs/en/managed-agents/events-and-streaming) for `span.outcome_evaluation_end`, or poll `GET /v1/sessions/:id` and read `outcome_evaluations[].result`. Until an evaluation completes, `result` reports `pending`, `running`, or `evaluating`:

<CodeGroup>
  ```bash curl
  session=$(curl -fsSL "https://api.anthropic.com/v1/sessions/$session_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01")

  jq -r '.outcome_evaluations[] | "\(.outcome_id): \(.result)"' <<<"$session"
  # outc_01a...: satisfied
  ```

  ```bash CLI
  ant beta:sessions retrieve --session-id "$SESSION_ID" \
    --transform 'outcome_evaluations' --format yaml
  ```

  ```python Python
  session = client.beta.sessions.retrieve(session.id)

  for outcome in session.outcome_evaluations:
      print(f"{outcome.outcome_id}: {outcome.result}")
      # outc_01a...: satisfied
  ```

  ```typescript TypeScript
  const retrieved = await client.beta.sessions.retrieve(session.id);

  for (const outcome of retrieved.outcome_evaluations) {
    console.log(`${outcome.outcome_id}: ${outcome.result}`);
    // outc_01a...: satisfied
  }
  ```

  ```csharp C#
  session = await client.Beta.Sessions.Retrieve(session.ID);

  foreach (var outcome in session.OutcomeEvaluations)
  {
      Console.WriteLine($"{outcome.OutcomeID}: {outcome.Result}");
      // outc_01a...: satisfied
  }
  ```

  ```go Go
  session, err = client.Beta.Sessions.Get(ctx, session.ID, anthropic.BetaSessionGetParams{})
  if err != nil {
  	panic(err)
  }

  for _, outcome := range session.OutcomeEvaluations {
  	fmt.Printf("%s: %s\n", outcome.OutcomeID, outcome.Result)
  	// outc_01a...: satisfied
  }
  ```

  ```java Java
  var retrieved = client.beta().sessions().retrieve(session.id());

  for (var outcome : retrieved.outcomeEvaluations()) {
      IO.println(outcome.outcomeId() + ": " + outcome.result());
      // outc_01a...: satisfied
  }
  ```

  ```php PHP
  $session = $client->beta->sessions->retrieve($session->id);

  foreach ($session->outcomeEvaluations as $outcome) {
      echo "{$outcome->outcomeID}: {$outcome->result}\n";
      // outc_01a...: satisfied
  }
  ```

  ```ruby Ruby
  session = client.beta.sessions.retrieve(session.id)

  session.outcome_evaluations.each do
    puts "#{it.outcome_id}: #{it.result}"
    # outc_01a...: satisfied
  end
  ```
</CodeGroup>

## Retrieve deliverables

The agent writes output files to `/mnt/session/outputs/` inside the sandbox. Once the session is idle, fetch them through the [Files API](/docs/en/build-with-claude/files) scoped to the session.

<Note>
  Filtering by `scope_id` requires the `managed-agents-2026-04-01` beta header on the files request. The SDK files methods send only the files beta automatically, so the examples pass it explicitly.
</Note>

<CodeGroup>
  ```bash curl
  # List files produced by this session
  # scope_id filtering requires the managed-agents beta alongside the files beta
  files=$(curl -fsSL "https://api.anthropic.com/v1/files?scope_id=$session_id" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01,files-api-2025-04-14")
  jq -r '.data[] | "\(.id) \(.filename)"' <<<"$files"

  # Download a file
  file_id=$(jq -r '.data[0].id // empty' <<<"$files")
  if [[ -n $file_id ]]; then
    curl -fsSL "https://api.anthropic.com/v1/files/$file_id/content" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01,files-api-2025-04-14" \
      -o /tmp/output.txt
  fi
  ```

  ```bash CLI
  # List files produced by this session
  # scope_id filtering requires the managed-agents beta on the files request
  ant beta:files list --scope-id "$SESSION_ID" \
    --beta managed-agents-2026-04-01

  # Download a file
  FILE_ID=$(ant beta:files list --scope-id "$SESSION_ID" \
    --beta managed-agents-2026-04-01 \
    --transform 'data[0].id' --raw-output)
  if [[ -n $FILE_ID ]]; then
    ant beta:files download --file-id "$FILE_ID" --output /tmp/output.txt
  fi
  ```

  ```python Python
  # List files produced by this session
  # scope_id filtering requires the managed-agents beta on the files request
  files = client.beta.files.list(scope_id=session.id, betas=["managed-agents-2026-04-01"])
  for file in files:
      print(file.id, file.filename)

  # Download a file
  if files.data:
      content = client.beta.files.download(files.data[0].id)
      content.write_to_file("/tmp/output.txt")
  ```

  ```typescript TypeScript
  // List files produced by this session
  // scope_id filtering requires the managed-agents beta on the files request
  const files = await client.beta.files.list({
    scope_id: session.id,
    betas: ["managed-agents-2026-04-01"],
  });
  for (const file of files.data) {
    console.log(file.id, file.filename);
  }

  // Download a file
  if (files.data.length > 0) {
    const content = await client.beta.files.download(files.data[0].id);
    await writeFile("/tmp/output.txt", new Uint8Array(await content.arrayBuffer()));
  }
  ```

  ```csharp C#
  // List files produced by this session
  // (scope_id filtering requires the managed-agents beta on the files request)
  var files = await client.Beta.Files.List(new()
  {
      ScopeID = session.ID,
      Betas = ["managed-agents-2026-04-01"],
  });
  foreach (var file in files.Items)
  {
      Console.WriteLine($"{file.ID} {file.Filename}");
  }

  // Download a file
  if (files.Items.Count > 0)
  {
      using var download = await client.Beta.Files.Download(files.Items[0].ID);
      await using var output = File.Create("/tmp/output.txt");
      await (await download.ReadAsStream()).CopyToAsync(output);
  }
  ```

  ```go Go
  // List files produced by this session
  // (scope_id filtering requires the managed-agents beta on the files request)
  files, err := client.Beta.Files.List(ctx, anthropic.BetaFileListParams{
  	ScopeID: anthropic.String(session.ID),
  	Betas:   []anthropic.AnthropicBeta{anthropic.AnthropicBetaManagedAgents2026_04_01},
  })
  if err != nil {
  	panic(err)
  }
  for _, file := range files.Data {
  	fmt.Println(file.ID, file.Filename)
  }

  // Download a file
  if len(files.Data) > 0 {
  	resp, err := client.Beta.Files.Download(ctx, files.Data[0].ID, anthropic.BetaFileDownloadParams{})
  	if err != nil {
  		panic(err)
  	}
  	defer resp.Body.Close()
  	out, err := os.Create("/tmp/output.txt")
  	if err != nil {
  		panic(err)
  	}
  	defer out.Close()
  	if _, err := io.Copy(out, resp.Body); err != nil {
  		panic(err)
  	}
  }
  ```

  ```java Java
  // List files produced by this session
  // (scope_id filtering requires the managed-agents beta on the files request)
  var files = client.beta().files().list(
      FileListParams.builder()
          .scopeId(session.id())
          .addBeta(AnthropicBeta.MANAGED_AGENTS_2026_04_01)
          .build());
  for (var file : files.data()) {
      IO.println(file.id() + " " + file.filename());
  }

  // Download a file
  if (!files.data().isEmpty()) {
      try (HttpResponse response = client.beta().files().download(files.data().getFirst().id())) {
          try (InputStream body = response.body()) {
              Files.copy(body, Path.of("/tmp/output.txt"), StandardCopyOption.REPLACE_EXISTING);
          }
      }
  }
  ```

  ```php PHP
  // List files produced by this session
  // scope_id filtering requires the managed-agents beta on the files request
  $files = $client->beta->files->list(scopeID: $session->id, betas: ['managed-agents-2026-04-01']);
  foreach ($files->data as $file) {
      echo "{$file->id} {$file->filename}\n";
  }

  // Download a file
  if (count($files->data) > 0) {
      $content = $client->beta->files->download($files->data[0]->id);
      file_put_contents('/tmp/output.txt', $content);
  }
  ```

  ```ruby Ruby
  # List files produced by this session
  # scope_id filtering requires the managed-agents beta on the files request
  files = client.beta.files.list(scope_id: session.id, betas: ["managed-agents-2026-04-01"])
  files.data.each { |file| puts "#{file.id} #{file.filename}" }

  # Download a file
  if (first = files.data.first)
    content = client.beta.files.download(first.id)
    File.binwrite("/tmp/output.txt", content.read)
  end
  ```
</CodeGroup>

## Next steps

<CardGroup cols={3}>
  <Card title="Authenticate with vaults" icon="fingerprint" href="/docs/en/managed-agents/vaults">
    Register per-user credentials when creating sessions.
  </Card>

  <Card title="Session event stream" icon="lightning" href="/docs/en/managed-agents/events-and-streaming">
    Send events, stream responses, and interrupt or redirect your session mid-execution.
  </Card>

  <Card title="Adding files" icon="file" href="/docs/en/managed-agents/files">
    Upload files and mount them in your sandbox for reading and processing.
  </Card>
</CardGroup>
