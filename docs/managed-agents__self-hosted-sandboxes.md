---
title: Self-hosted sandboxes
url: https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes
description: Run Claude Managed Agents sessions in self-hosted sandboxes, keeping tool execution, files, and network egress in your own infrastructure.
---

By default, Managed Agents executes tools and code inside [Anthropic-managed cloud sandboxes](https://platform.claude.com/docs/en/managed-agents/cloud-sandboxes-reference). Self-hosted sandboxes keep the orchestration on Anthropic's side but move tool execution into infrastructure you control, so the agent's code, filesystem, and network egress never leave your environment.

Tool execution stays on your host: the filesystem the agent reads and writes, the processes it spawns, and the network it can reach are all under your control. Tool inputs and outputs still flow to Anthropic's control plane (where Claude runs) so the model can see results and determine what to do next. The agent's [skills](https://platform.claude.com/docs/en/managed-agents/skills) and the contents of any [memory stores](https://platform.claude.com/docs/en/managed-agents/memory) attached to the session are stored by Anthropic and copied into your sandbox for the session; changes the agent makes to memory files sync back to the store. See the [security model](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security) for the full data-flow boundary.

<Note>
  Self-hosted sandboxes support all Claude models available in Managed Agents, including Claude Opus 4.8 and Claude Opus 5. The model is configured on the [agent](https://platform.claude.com/docs/en/managed-agents/agent-setup), not the environment.
</Note>

## How it differs from cloud environments

|                               | Cloud environment                      | Self-hosted sandbox                                       |
| ----------------------------- | -------------------------------------- | --------------------------------------------------------- |
| Where tools run               | Anthropic-managed sandboxes            | Your infrastructure                                       |
| Network reach                 | Anthropic's egress controls            | Your network policy                                       |
| File and GitHub repo mounting | Managed by Anthropic                   | Managed by you                                            |
| Memory stores                 | Mounted by Anthropic at `/mnt/memory/` | Downloaded to `/mnt/memory/` and synced by the SDK worker |
| Lifecycle                     | Managed by Anthropic                   | Managed by you                                            |

Self-hosting is a good fit when the agent needs to operate on data that cannot leave your network boundary, reach internal services that are not publicly routable, or run under your organization's own compliance and audit controls.

For Zero Data Retention and HIPAA BAA eligibility, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#feature-eligibility).

## When to combine with MCP tunnels

Self-hosting controls *where the agent's code executes*. [MCP tunnels](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview) control *how Anthropic reaches MCP servers in your network*. They are independent: a session running in Anthropic's cloud sandboxes can still reach private MCP servers through a tunnel, and a self-hosted session can use either tunneled or public MCP servers. Use both when you want execution and tool access to stay inside your boundary. To give the agent tools from an MCP server inside your network without running a tunnel, you can also [wrap the server as custom tools](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#wrap-an-mcp-server-as-custom-tools) served by your worker.

## Environment worker

<Tip>
  This guide describes how to build a worker with any generic sandboxing platform. Additional, platform-specific guides are available for [AWS Lambda MicroVMs](https://docs.aws.amazon.com/lambda/latest/dg/microvms-integrations-claude-managed-agents.html), [Blaxel](https://docs.blaxel.ai/Tutorials/Claude-Managed-Agents), [Cloudflare](https://developers.cloudflare.com/sandbox/claude-managed-agents/), [Daytona](https://www.daytona.io/docs/en/guides/claude/claude-managed-agents), [E2B](https://e2b.dev/docs/agents/claude-managed-agents), [Fly.io](https://docs.sprites.dev/integrations/claude-managed-agents/), [GKE Agent Sandbox](https://github.com/GoogleCloudPlatform/kubernetes-engine-samples/tree/main/ai-ml/anthropic-agent-sandbox), [Modal](https://github.com/modal-labs/claude-managed-agents-modal-sandbox), [Namespace](https://namespace.so/docs/integrations/claude), [Superserve](https://docs.superserve.ai/integrations/managed-agents/claude-managed-agents), and [Vercel](https://vercel.com/kb/guide/run-claude-managed-agent-tools-with-vercel-sandbox).
</Tip>

An environment worker is a process you run on your own infrastructure. It receives tool execution requests from Anthropic and runs them locally. The `self_hosted` environment acts as a work queue: when a [session](https://platform.claude.com/docs/en/managed-agents/sessions) is assigned to it, Anthropic enqueues the session as a work item. Your worker claims work items from that queue, spawns an execution context for each one, downloads the agent's [skills](https://platform.claude.com/docs/en/managed-agents/skills) (reusable, filesystem-based resources that give the agent domain-specific expertise), runs the tool calls, and posts the results back.

Work items are claimed by polling the environment's queue: either by an **always-on worker** that polls continuously, or a **webhook-triggered handler** that wakes on `session.status_run_started` and starts polling.

The CLI and SDK both ship pre-built workers. The `ant` CLI supports the always-on pattern only; the SDK supports both always-on and webhook-triggered. Both are configurable: see [Self-hosted worker](https://platform.claude.com/docs/en/managed-agents/reference#self-hosted-worker) in the reference for CLI flags, and [SDK helpers](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#sdk-helpers) on this page for the SDK options. For more control, call the [Environments Work endpoints](https://platform.claude.com/docs/en/api/beta/environments/work) directly and implement your own worker.

### Sandbox filesystem

* **`/workspace`:** the system default working directory for tool execution and skill download. The CLI's `--workdir` flag defaults to the current directory; pass `--workdir /workspace` to match the system default. Skills are downloaded to `<workdir>/skills/<name>/`. If you use a different working directory, update your agent's system prompt so Claude can locate the skill files.
* **Outputs:** on self-hosted environments the session's system prompt omits the `/mnt/session/outputs` instruction used on Anthropic-managed sandboxes, so final deliverables land wherever the agent writes them in your sandbox filesystem, typically under the working directory.
* **`/mnt/memory/`:** memory stores attached to the session are materialized here by the SDK worker, one directory per store at the store's `mount_path` (for example, `/mnt/memory/user-preferences/`). The worker creates these directories when it claims the session and removes them when the session ends; see [Use memory stores](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#use-memory-stores).

## Before you begin

You need:

* **An existing agent.** If you don't have one, complete the [Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart) first and note its agent ID.
* **A Linux host** with `/bin/bash` at that exact path. The worker's bash tool invokes it directly, without consulting `PATH`. The TypeScript SDK additionally requires `unzip` and `tar` on the `PATH` and Node.js 22 or later; the Python and Go SDKs use their standard libraries for archive extraction and have no additional binary requirements.
* **The `ant` CLI or an Anthropic SDK** (Python, TypeScript, or Go) on the worker host.
* **Credentials:** an environment key (generated in the Console in the steps that follow) authenticates the worker to its queue; your Claude API key creates sessions and reads queue stats from outside the worker host. Key generation is Console-only. Claimed work items also carry a per-session `secret` that the worker uses to mount [memory stores](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#use-memory-stores); you don't generate it, but in the sandbox-per-session pattern you forward it into the sandbox yourself (see [Run one sandbox per session](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session)).
* **For memory stores, a prepared host.** If sessions on this environment will attach memory stores, prepare `/mnt/memory` on the worker host before you start the worker; see [Prepare the host](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#prepare-the-host).

<Note>
  On [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws), the worker authenticates with AWS IAM (SigV4) or an [API key generated in the AWS Console](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws#api-key-authentication), not an environment key. Attach the [`AnthropicSelfHostedEnvironmentAccess`](https://platform.claude.com/docs/en/api/claude-platform-on-aws-iam-actions#managed-policies) managed policy to the IAM principal your worker runs as. Environment keys generated in the Claude Console don't work with the Claude Platform on AWS endpoint.

  Memory stores cannot be attached to sessions on self-hosted environments on Claude Platform on AWS.
</Note>

<Steps>
  <Step title="Create a self-hosted environment">
    In the [Console](https://platform.claude.com/workspaces/default/environments): **Workspace > Environments > New > Self-hosted**

    Or through the API:

    <CodeGroup>
      ```bash cURL
      curl -sS --fail-with-body https://api.anthropic.com/v1/environments \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        -d '{
          "name": "self-hosted",
          "config": {"type": "self_hosted"}
        }'
      ```

      <MultiFileExample language="cli" label="CLI">
        ```bash CLI
        ant beta:environments create < environment.yaml
        ```

        <File filename="environment.yaml">
          ```yaml
          name: self-hosted
          config:
            type: self_hosted
          ```
        </File>
      </MultiFileExample>

      ```python Python
      client = anthropic.Anthropic()

      environment = client.beta.environments.create(
          name="self-hosted", config={"type": "self_hosted"}
      )
      print(environment.id)
      ```

      ```typescript TypeScript
      const client = new Anthropic();

      const environment = await client.beta.environments.create({
        name: "self-hosted",
        config: { type: "self_hosted" }
      });
      console.log(environment.id);
      ```

      ```csharp C#
      using Anthropic.Models.Beta.Environments;

      var client = new AnthropicClient();

      var environment = await client.Beta.Environments.Create(
          new EnvironmentCreateParams
          {
              Name = "self-hosted",
              Config = new BetaSelfHostedConfigParams(),
          }
      );
      Console.WriteLine(environment.ID);
      ```

      ```go Go
      client := anthropic.NewClient()

      environment, err := client.Beta.Environments.New(context.Background(), anthropic.BetaEnvironmentNewParams{
      	Name: "self-hosted",
      	Config: anthropic.BetaEnvironmentNewParamsConfigUnion{
      		OfSelfHosted: &anthropic.BetaSelfHostedConfigParams{},
      	},
      })
      if err != nil {
      	panic(err)
      }
      fmt.Println(environment.ID)
      ```

      ```java Java
      import com.anthropic.models.beta.environments.BetaSelfHostedConfigParams;
      import com.anthropic.models.beta.environments.EnvironmentCreateParams;

      void main() {
          var client = AnthropicOkHttpClient.fromEnv();

          var environment = client.beta().environments().create(
              EnvironmentCreateParams.builder()
                  .name("self-hosted")
                  .config(BetaSelfHostedConfigParams.builder().build())
                  .build()
          );
          IO.println(environment.id());
      }
      ```

      ```php PHP
      $client = new Anthropic\Client();

      $environment = $client->beta->environments->create(
          name: 'self-hosted',
          config: ['type' => 'self_hosted'],
      );
      echo $environment->id, PHP_EOL;
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      environment = client.beta.environments.create(
        name: "self-hosted",
        config: {type: :self_hosted}
      )
      puts environment.id
      ```
    </CodeGroup>
  </Step>

  <Step title="Generate an environment key">
    In the Console, open the environment and click **Generate environment key**. Key generation is Console-only, regardless of whether you created the environment through the Console or the API. Then export the environment ID and key on the worker host:

    ```bash
    export ANTHROPIC_ENVIRONMENT_KEY="sk-ant-oat01-..."
    export ANTHROPIC_ENVIRONMENT_ID="env_..."
    ```
  </Step>
</Steps>

<Note>
  Skills can include executables that the agent may run directly. The CLI and SDK workers preserve the executable permissions recorded in the skill bundle when they extract it. If you implement skills download manually, you are responsible for setting executable permissions.
</Note>

## Run a worker

Choose **always-on** for the simplest setup: a long-running process polls the queue continuously and needs only outbound HTTPS. Choose **webhook-triggered** to avoid running an idle poller; it requires a webhook endpoint that Anthropic can reach (see [Webhooks](https://platform.claude.com/docs/en/managed-agents/webhooks) for endpoint setup and signature verification).

<Tabs>
  <Tab title="Always-on (ant CLI)">
    <Steps>
      <Step title="Install the ant CLI">
        Run this on the worker host.

        <Tabs>
          <Tab title="curl (Linux/WSL)">
            For Linux environments, download the release binary directly.

            ```bash
            VERSION=1.26.1
            OS=$(uname -s | tr '[:upper:]' '[:lower:]')
            case $(uname -m) in
              x86_64) ARCH=amd64 ;;
              aarch64) ARCH=arm64 ;;
            esac
            curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${VERSION}/ant_${VERSION}_${OS}_${ARCH}.tar.gz" \
              | sudo tar -xz -C /usr/local/bin ant
            ```

            You can find all releases on the [GitHub releases page](https://github.com/anthropics/anthropic-cli/releases).
          </Tab>

          <Tab title="Homebrew (macOS)">
            ```bash
            brew install anthropics/tap/ant
            ```
          </Tab>
        </Tabs>
      </Step>

      <Step title="Run the worker">
        **In-process**

        `ant beta:worker poll` claims work items assigned to the environment, downloads skills, executes tool calls in the working directory, and posts results back. It reads `ANTHROPIC_ENVIRONMENT_KEY` and `ANTHROPIC_ENVIRONMENT_ID` from the environment.

        ```bash
        ant beta:worker poll \
          --workdir "/workspace"
        ```

        The worker exits cleanly on SIGTERM or SIGINT: it cancels any in-flight tool call, posts its error result, and releases the work item before stopping.

        **Sandbox per session**

        If you need stronger isolation (a fresh filesystem, resource limits, or per-session network controls), run each session in its own sandbox. Build an image with `ant` installed and `ant beta:worker run` as the entrypoint. The base image must provide `/bin/bash`; `curl` is only used at build time. When a sandbox starts, it reads session details from environment variables, handles that session, and exits:

        ```text
        FROM your-base-image
        ARG ANT_VERSION=1.26.1
        ARG TARGETARCH
        RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo arm64 || echo amd64) && \
            curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${ANT_VERSION}/ant_${ANT_VERSION}_linux_${ARCH}.tar.gz" \
              | tar -xz -C /usr/local/bin ant
        WORKDIR /workspace
        VOLUME /workspace
        ENTRYPOINT ["ant", "beta:worker", "run"]
        ```

        Then write a spawn script that forwards session details into a fresh sandbox. The poller injects `ANTHROPIC_SESSION_ID`, `ANTHROPIC_WORK_ID`, `ANTHROPIC_ENVIRONMENT_ID`, and `ANTHROPIC_ENVIRONMENT_KEY` into the script's environment, and writes the claimed work item to the script's standard input as JSON, including the work item's per-session `secret` when Anthropic issued one. `ANTHROPIC_BASE_URL` is optional and is passed through only if it was set on the poller host; it overrides the default API endpoint. In the example, `/host/outputs` is a host directory you choose; it is bind-mounted to the sandbox's working directory (`/workspace`) so you can retrieve session deliverables after the sandbox exits. On self-hosted environments the agent writes deliverables under the working directory rather than `/mnt/session/outputs` (see [Sandbox filesystem](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#sandbox-filesystem)), so mounting the working directory is what captures them; the mount also picks up the downloaded `skills/` tree and any intermediate files the agent creates.

        ```bash
        #!/bin/bash
        # spawn.sh: called once per claimed work item
        mkdir -p "/host/outputs/$ANTHROPIC_SESSION_ID"
        exec docker run --rm \
          -e ANTHROPIC_SESSION_ID -e ANTHROPIC_ENVIRONMENT_KEY \
          -e ANTHROPIC_WORK_ID -e ANTHROPIC_ENVIRONMENT_ID -e ANTHROPIC_BASE_URL \
          -v "/host/outputs/$ANTHROPIC_SESSION_ID":/workspace \
          your-image
        ```

        The `ant beta:worker run` entrypoint does not mount [memory stores](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#use-memory-stores). If sessions on this environment attach memory stores, keep the poller, but build the per-session image around the SDK worker and extend the spawn script to forward the work item's `secret` into the sandbox, as shown in [Run one sandbox per session](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session).

        Start the poller pointing at the script:

        ```bash
        ant beta:worker poll \
          --on-work ./spawn.sh
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Always-on (SDK)">
    <Steps>
      <Step title="Run the worker">
        `EnvironmentWorker` claims work items assigned to the environment, downloads skills, executes tool calls in the working directory, and posts results back. Authenticate with the environment key you generated in [Before you begin](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#before-you-begin).

        <CodeGroup exclude="shell">
          ```python Python
          import asyncio
          import contextlib
          import os
          import signal
          from anthropic import AsyncAnthropic
          from anthropic.lib.environments import EnvironmentWorker


          async def main() -> None:
              environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
              environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
              async with AsyncAnthropic(auth_token=environment_key) as client:
                  worker = EnvironmentWorker(
                      client,
                      environment_id=environment_id,
                      environment_key=environment_key,
                      workdir="/workspace",
                  )
                  task = asyncio.create_task(worker.run())
                  # Cancelling the task, rather than killing the process, lets the worker stop its
                  # in-flight work item and upload changed memory files before it exits.
                  loop = asyncio.get_running_loop()
                  for signum in (signal.SIGINT, signal.SIGTERM):
                      loop.add_signal_handler(signum, task.cancel)
                  with contextlib.suppress(asyncio.CancelledError):
                      await task


          asyncio.run(main())
          ```

          ```typescript TypeScript
          import Anthropic from "@anthropic-ai/sdk";
          import { EnvironmentWorker } from "@anthropic-ai/sdk/helpers/beta/environments";

          const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
          const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
          const client = new Anthropic({ authToken: environmentKey });
          const controller = new AbortController();
          // Aborting on either signal lets the worker upload changed memory files and remove its
          // store directories before the process exits.
          process.once("SIGINT", () => controller.abort());
          process.once("SIGTERM", () => controller.abort());

          await new EnvironmentWorker({
            client,
            environmentId,
            environmentKey,
            workdir: "/workspace",
            signal: controller.signal
          }).run();
          ```

          ```csharp C#
          // EnvironmentWorker is not currently available in the C# SDK. See the Always-on (ant CLI) tab.
          ```

          ```go Go
          package main

          import (
          	"context"
          	"log"
          	"os"
          	"os/signal"
          	"syscall"

          	"github.com/anthropics/anthropic-sdk-go"
          	"github.com/anthropics/anthropic-sdk-go/lib/environments"
          	"github.com/anthropics/anthropic-sdk-go/option"
          )

          func main() {
          	environmentKey := os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")
          	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")

          	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
          	defer stop()

          	client := anthropic.NewClient(option.WithAuthToken(environmentKey))

          	worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
          		EnvironmentID:  environmentID,
          		EnvironmentKey: environmentKey,
          		Workdir:        "/workspace",
          	})
          	if err := worker.Run(ctx); err != nil {
          		log.Fatalf("worker: %v", err)
          	}
          }

          ```

          ```java Java
          // EnvironmentWorker is not currently available in the Java SDK. See the Always-on (ant CLI) tab.
          ```

          ```php PHP
          // EnvironmentWorker is not currently available in the PHP SDK. See the Always-on (ant CLI) tab.
          ```

          ```ruby Ruby
          # EnvironmentWorker is not currently available in the Ruby SDK. See the Always-on (ant CLI) tab.
          ```
        </CodeGroup>
      </Step>
    </Steps>
  </Tab>

  <Tab title="Webhook-triggered (SDK)">
    <Steps>
      <Step title="Subscribe to session webhooks">
        In the [Console](https://platform.claude.com/settings/workspaces/default/webhooks), define a webhook endpoint that listens for `session.status_run_started` events. See [Webhooks](https://platform.claude.com/docs/en/managed-agents/webhooks) for details.
      </Step>

      <Step title="Export the webhook signing key">
        In addition to the environment ID and key from [Before you begin](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#before-you-begin), export the webhook signing key on your handler host so the handler can verify incoming payloads. Signature verification in the Python handler needs the webhooks extra: `pip install "anthropic[webhooks]"`.

        ```bash
        export ANTHROPIC_WEBHOOK_SIGNING_KEY="whsec_..."
        ```
      </Step>

      <Step title="Implement the webhook handler">
        `EnvironmentWorker` claims the work item, downloads skills, executes tool calls in the working directory, posts results back, and exits. Invoke it when `session.status_run_started` fires.

        When you hand a claimed work item to `handle_item()` yourself, as this handler does, pass the work item's `secret` along as `work_secret` (`workSecret` in TypeScript, `WorkSecret` in Go) so the session can mount any [memory stores](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#use-memory-stores) attached to it. A handler like this one runs every claimed item in one process on one host, so two sessions that attach the same memory store cannot run through it at the same time (see [Prepare the host](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#prepare-the-host)); if your sessions share stores, launch [one sandbox per session](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session) instead.

        <CodeGroup exclude="shell">
          ```python Python
          import asyncio
          import os
          import signal
          import anthropic
          import standardwebhooks  # installed by the anthropic[webhooks] extra

          environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
          environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
          client = anthropic.AsyncAnthropic(
              auth_token=environment_key,
          )
          # Cancelled on SIGINT or SIGTERM (wired in handle) so an in-flight work item can upload
          # changed memory files and remove its store directories before the process exits.
          inflight: set[asyncio.Task[None]] = set()


          def cancel_inflight() -> None:
              for task in inflight:
                  task.cancel()


          async def handle(raw: bytes, headers: dict[str, str]) -> tuple[dict[str, str], int]:
              try:
                  event = client.beta.webhooks.unwrap(raw.decode(), headers=headers)
              except standardwebhooks.WebhookVerificationError:
                  return {"error": "signature verification failed"}, 401
              if event.data.type != "session.status_run_started":
                  return {"status": "ignored"}, 200
              loop = asyncio.get_running_loop()
              for signum in (signal.SIGINT, signal.SIGTERM):
                  loop.add_signal_handler(signum, cancel_inflight)
              task = asyncio.create_task(run_queued_work())
              inflight.add(task)
              task.add_done_callback(inflight.discard)
              try:
                  await task
              except asyncio.CancelledError:
                  return {"status": "shutting down"}, 503
              return {"status": "ok"}, 200


          async def run_queued_work() -> None:
              async for work in client.beta.environments.work.poller(
                  environment_id=environment_id,
                  environment_key=environment_key,
                  block_ms=None,
                  reclaim_older_than_ms=2000,
                  drain=True,
                  auto_stop=False,
              ):
                  await client.beta.environments.work.worker(workdir="/workspace").handle_item(
                      work_id=work.id,
                      environment_id=environment_id,
                      session_id=work.data.id,
                      environment_key=environment_key,
                      # The per-session secret is what lets the worker mount the session's memory stores.
                      work_secret=work.secret,
                  )
          ```

          ```typescript TypeScript
          import Anthropic from "@anthropic-ai/sdk";

          const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
          const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
          const client = new Anthropic({
            authToken: environmentKey
          });
          // Aborted on SIGINT or SIGTERM so an in-flight work item can upload changed memory
          // files and remove its store directories before the process exits.
          const shutdown = new AbortController();
          process.once("SIGINT", () => shutdown.abort());
          process.once("SIGTERM", () => shutdown.abort());

          export async function handle(req: Request): Promise<Response> {
            const body = await req.text();
            let event;
            try {
              event = client.beta.webhooks.unwrap(body, { headers: Object.fromEntries(req.headers) });
            } catch {
              return new Response("signature verification failed", { status: 401 });
            }
            if (event.data.type !== "session.status_run_started") {
              return Response.json({ status: "ignored" });
            }

            for await (const work of client.beta.environments.work.poller({
              environmentId,
              environmentKey,
              blockMs: null,
              reclaimOlderThanMs: 2000,
              drain: true,
              autoStop: false,
              signal: shutdown.signal
            })) {
              await client.beta.environments.work.worker({ workdir: "/workspace" }).handleItem({
                workId: work.id,
                environmentId,
                sessionId: work.data.id,
                environmentKey,
                // The per-session secret is what lets the worker mount the session's memory stores.
                workSecret: work.secret ?? undefined,
                signal: shutdown.signal
              });
            }
            return Response.json({ status: "ok" });
          }
          ```

          ```csharp C#
          // EnvironmentWorker is not currently available in the C# SDK.
          // To handle work items directly, see the Environments Work endpoints.
          ```

          ```go Go
          package main

          import (
          	"context"
          	"encoding/json"
          	"errors"
          	"io"
          	"log/slog"
          	"net/http"
          	"os"
          	"os/signal"
          	"syscall"

          	"github.com/anthropics/anthropic-sdk-go"
          	"github.com/anthropics/anthropic-sdk-go/lib/environments"
          	"github.com/anthropics/anthropic-sdk-go/option"
          	"github.com/anthropics/anthropic-sdk-go/packages/param"
          )

          var (
          	environmentKey = os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")
          	environmentID  = os.Getenv("ANTHROPIC_ENVIRONMENT_ID")
          	client         = anthropic.NewClient(
          		option.WithAuthToken(environmentKey),
          		option.WithWebhookKey(os.Getenv("ANTHROPIC_WEBHOOK_SIGNING_KEY")),
          	)
          	worker = environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
          		Workdir: "/workspace",
          	})
          	// Cancelled on SIGINT or SIGTERM (set in main) so an in-flight work item can
          	// upload changed memory files and remove its store directories before exit.
          	shutdown context.Context
          )

          func handle(w http.ResponseWriter, r *http.Request) {
          	body, err := io.ReadAll(r.Body)
          	if err != nil {
          		http.Error(w, "bad request", http.StatusBadRequest)
          		return
          	}
          	event, err := client.Beta.Webhooks.Unwrap(body, r.Header)
          	if err != nil {
          		http.Error(w, "signature verification failed", http.StatusUnauthorized)
          		return
          	}
          	if event.Data.Type != "session.status_run_started" {
          		json.NewEncoder(w).Encode(map[string]string{"status": "ignored"})
          		return
          	}

          	// The Go SDK does not provide a RunOne convenience: drain pending items
          	// with WorkPoller and run each one with HandleItem.
          	// Detach from r.Context(): the session can outlive the webhook delivery timeout.
          	// The process-wide shutdown context still ends the item cleanly on SIGTERM.
          	ctx := shutdown
          	poller := environments.NewWorkPoller(ctx, client, environments.WorkPollerOptions{
          		EnvironmentID:      environmentID,
          		EnvironmentKey:     environmentKey,
          		BlockMs:            param.Null[int64](),
          		ReclaimOlderThanMs: param.NewOpt[int64](2000),
          		Drain:              true,
          		AutoStop:           param.NewOpt(false),
          	})
          	defer poller.Close()
          	for poller.Next() {
          		item := poller.Current()
          		if err := worker.HandleItem(ctx, environments.HandleItemOptions{
          			WorkID:         item.ID,
          			EnvironmentID:  item.EnvironmentID,
          			SessionID:      item.Data.ID,
          			EnvironmentKey: environmentKey,
          			// The per-session secret is what lets the worker mount the session's memory stores.
          			WorkSecret: item.Secret,
          		}); err != nil {
          			slog.Error("handle work item", "work_id", item.ID, "err", err)
          			http.Error(w, "internal error", http.StatusInternalServerError)
          			return
          		}
          	}
          	if err := poller.Err(); err != nil {
          		slog.Error("poll work queue", "err", err)
          		http.Error(w, "internal error", http.StatusInternalServerError)
          		return
          	}
          	json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
          }

          func main() {
          	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
          	defer stop()
          	shutdown = ctx

          	server := &http.Server{Addr: ":8080"}
          	http.HandleFunc("POST /webhook", handle)
          	go func() {
          		if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
          			slog.Error("http server", "err", err)
          			os.Exit(1)
          		}
          	}()
          	// On a signal, stop accepting deliveries and return only after in-flight
          	// handlers, and therefore their work items' memory teardown, have finished.
          	<-ctx.Done()
          	if err := server.Shutdown(context.Background()); err != nil {
          		slog.Error("http shutdown", "err", err)
          	}
          }

          ```

          ```java Java
          // EnvironmentWorker is not currently available in the Java SDK.
          // To handle work items directly, see the Environments Work endpoints.
          ```

          ```php PHP
          // EnvironmentWorker is not currently available in the PHP SDK.
          // To handle work items directly, see the Environments Work endpoints.
          ```

          ```ruby Ruby
          # EnvironmentWorker is not currently available in the Ruby SDK.
          # To handle work items directly, see the Environments Work endpoints.
          ```
        </CodeGroup>
      </Step>
    </Steps>
  </Tab>
</Tabs>

### SDK helpers

The SDK provides three helpers at different levels of control. `EnvironmentWorker` covers most use cases; drop to the lower-level helpers when you need to launch your own per-session process or run tools against an already-claimed session.

* **`EnvironmentWorker`:** the out-of-the-box worker. Handles polling, setup, and execution end to end.

  * `.run()`: runs indefinitely, picking up sessions as they arrive.
  * `.handle_item()`: handles a single claimed work item and exits. Pass the work, session, and environment identifiers explicitly, or let it read the `ANTHROPIC_*` variables that `ant beta:worker poll --on-work` sets for the process it spawns. To let the session mount its [memory stores](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#use-memory-stores), also pass the work item's `secret` as `work_secret` (`workSecret` in TypeScript, `WorkSecret` in Go) or set `ANTHROPIC_WORK_SECRET`; `ant beta:worker poll --on-work` does not set that variable, so read the secret from the work item JSON it writes to your script's standard input, as shown in [Run one sandbox per session](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session).
  * `memory_sync_interval` (`memorySyncIntervalMs` in TypeScript, `MemorySyncInterval` in Go) and `memory_sync_deletions` (`memorySyncDeletions`, `MemorySyncDeletions`): how often attached memory stores reconcile with the server while the session runs, and whether files the agent deletes locally are also deleted from the store. See [Configure sync](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#configure-sync) for units, defaults, and how to disable memory support.

* **`work.poller()`:** polls the work queue on your behalf and gives you each claimed session. Use this when you want to decide what happens for each session, for example launching a sandbox rather than running tools in-process.

  * `drain`: whether to stop polling once the queue is empty rather than waiting for new work.
  * `block_ms`: how long to wait for work to arrive before returning, in milliseconds. Must be between 1 and 999 (per-poll wait; the helper re-polls automatically). Pass `null` (`None` in Python, `param.Null[int64]()` in Go) for a non-blocking check; omitting the parameter uses the default 999 ms long-poll.
  * `reclaim_older_than_ms`: re-claim work items that were claimed but never acknowledged within this many milliseconds.
  * `auto_stop` (`autoStop` in TypeScript, `AutoStop` in Go): whether to post a stop signal for each work item once your loop body finishes with it. Turn it off when the process you launch for the session, rather than the loop body, runs the work item to completion.

* **`client.beta.sessions.events.tool_runner()`:** runs tool calls for a single session, given the session ID and a tool list. Use when you've already claimed the work and only need the execution layer.

Use the work poller directly when you want to launch your own per-session process, for example spinning up a sandbox for each claimed session:

<CodeGroup>
  ```bash cURL
  # The work poller is an SDK helper (Python, TypeScript, Go), not a raw
  # endpoint. From the shell, use `ant beta:worker poll --on-work` instead;
  # see the Always-on (ant CLI) tab.
  ```

  ```bash CLI
  # The work poller is an SDK helper (Python, TypeScript, Go), not a raw
  # endpoint. From the shell, use `ant beta:worker poll --on-work` instead;
  # see the Always-on (ant CLI) tab.
  ```

  ```python Python
  import asyncio
  import os

  from anthropic import AsyncAnthropic
  from anthropic.types.beta.environments import BetaSelfHostedWork

  SANDBOX_ENV = (
      "ANTHROPIC_ENVIRONMENT_ID",
      "ANTHROPIC_ENVIRONMENT_KEY",
      "ANTHROPIC_WORK_ID",
      "ANTHROPIC_SESSION_ID",
      "ANTHROPIC_WORK_SECRET",
      "ANTHROPIC_BASE_URL",  # forwarded only when set on this host
  )


  async def launch_container(work: BetaSelfHostedWork) -> None:
      print(f"claimed session {work.data.id}")
      # Replace `docker run` with your own sandbox launcher. Forward the environment
      # key (never your API key) and the work item's per-session secret: the worker
      # inside needs the secret to mount the session's memory stores.
      env = os.environ | {
          "ANTHROPIC_WORK_ID": work.id,
          "ANTHROPIC_SESSION_ID": work.data.id,
          "ANTHROPIC_WORK_SECRET": work.secret or "",
      }
      forward = [arg for name in SANDBOX_ENV for arg in ("-e", name)]
      launcher = await asyncio.create_subprocess_exec(
          "docker", "run", "--rm", "--detach", *forward, "your-sdk-worker-image", env=env
      )
      await launcher.wait()


  async def main() -> None:
      environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
      environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
      async with AsyncAnthropic(auth_token=environment_key) as client:
          async for work in client.beta.environments.work.poller(
              environment_id=environment_id,
              environment_key=environment_key,
              auto_stop=False,  # the launched sandbox owns the stop call
          ):
              await launch_container(work)


  asyncio.run(main())
  ```

  ```typescript TypeScript
  import { spawn } from "node:child_process";
  import { once } from "node:events";
  import Anthropic from "@anthropic-ai/sdk";
  import { WorkPoller } from "@anthropic-ai/sdk/helpers/beta/environments";
  import type { BetaSelfHostedWork } from "@anthropic-ai/sdk/resources/beta/environments";

  const SANDBOX_ENV = [
    "ANTHROPIC_ENVIRONMENT_ID",
    "ANTHROPIC_ENVIRONMENT_KEY",
    "ANTHROPIC_WORK_ID",
    "ANTHROPIC_SESSION_ID",
    "ANTHROPIC_WORK_SECRET",
    "ANTHROPIC_BASE_URL" // forwarded only when set on this host
  ];

  const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
  const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
  const client = new Anthropic({ authToken: environmentKey });

  async function launchContainer(work: BetaSelfHostedWork): Promise<void> {
    console.log(`claimed session ${work.data.id}`);
    // Replace `docker run` with your own sandbox launcher. Forward the environment
    // key (never your API key) and the work item's per-session secret: the worker
    // inside needs the secret to mount the session's memory stores.
    const env = {
      ...process.env,
      ANTHROPIC_WORK_ID: work.id,
      ANTHROPIC_SESSION_ID: work.data.id,
      ANTHROPIC_WORK_SECRET: work.secret ?? ""
    };
    const forward = SANDBOX_ENV.flatMap((name) => ["-e", name]);
    const launcher = spawn(
      "docker",
      ["run", "--rm", "--detach", ...forward, "your-sdk-worker-image"],
      { env, stdio: "inherit" }
    );
    await once(launcher, "close");
  }

  const poller = new WorkPoller({
    client,
    environmentId,
    environmentKey,
    autoStop: false // the launched sandbox owns the stop call
  });

  for await (const work of poller) {
    await launchContainer(work);
  }
  ```

  ```csharp C#
  // A work-polling helper is not currently available in the C# SDK.
  // To claim work directly, see the Environments Work endpoints.
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"log"
  	"os"
  	"os/exec"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/lib/environments"
  	"github.com/anthropics/anthropic-sdk-go/option"
  	"github.com/anthropics/anthropic-sdk-go/packages/param"
  )

  var sandboxEnv = []string{
  	"ANTHROPIC_ENVIRONMENT_ID",
  	"ANTHROPIC_ENVIRONMENT_KEY",
  	"ANTHROPIC_WORK_ID",
  	"ANTHROPIC_SESSION_ID",
  	"ANTHROPIC_WORK_SECRET",
  	"ANTHROPIC_BASE_URL", // forwarded only when set on this host
  }

  func launchContainer(ctx context.Context, work *anthropic.BetaSelfHostedWork) error {
  	fmt.Printf("claimed session %s\n", work.Data.ID)
  	// Replace `docker run` with your own sandbox launcher. Forward the environment
  	// key (never your API key) and the work item's per-session secret: the worker
  	// inside needs the secret to mount the session's memory stores.
  	args := []string{"run", "--rm", "--detach"}
  	for _, name := range sandboxEnv {
  		args = append(args, "-e", name)
  	}
  	launcher := exec.CommandContext(ctx, "docker", append(args, "your-sdk-worker-image")...)
  	launcher.Env = append(os.Environ(),
  		"ANTHROPIC_WORK_ID="+work.ID,
  		"ANTHROPIC_SESSION_ID="+work.Data.ID,
  		"ANTHROPIC_WORK_SECRET="+work.Secret,
  	)
  	launcher.Stdout, launcher.Stderr = os.Stdout, os.Stderr
  	return launcher.Run()
  }

  func main() {
  	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")
  	environmentKey := os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")

  	client := anthropic.NewClient(option.WithAuthToken(environmentKey))

  	ctx := context.Background()

  	poller := environments.NewWorkPoller(ctx, client, environments.WorkPollerOptions{
  		EnvironmentID:  environmentID,
  		EnvironmentKey: environmentKey,
  		AutoStop:       param.NewOpt(false), // the launched sandbox owns the stop call
  	})
  	defer poller.Close()

  	for work, err := range poller.All() {
  		if err != nil {
  			log.Fatal(err)
  		}
  		if err := launchContainer(ctx, work); err != nil {
  			log.Fatal(err)
  		}
  	}
  }
  ```

  ```java Java
  // A work-polling helper is not currently available in the Java SDK.
  // To claim work directly, see the Environments Work endpoints.
  ```

  ```php PHP
  // A work-polling helper is not currently available in the PHP SDK.
  // To claim work directly, see the Environments Work endpoints.
  ```

  ```ruby Ruby
  # A work-polling helper is not currently available in the Ruby SDK.
  # To claim work directly, see the Environments Work endpoints.
  ```
</CodeGroup>

Whatever launches the sandbox must forward the claimed work item's `secret` into it (for example as `ANTHROPIC_WORK_SECRET`) alongside the session, work, and environment identifiers, so the worker inside can mount the session's [memory stores](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#use-memory-stores); see [Run one sandbox per session](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session).

**`AgentToolContext`** is the execution context for tool calls. It defines the working directory and path policy, and can download the session's skills. The file tools (`read`, `write`, `edit`, `glob`, `grep`) are confined to the working directory plus any directories listed in `allowed_roots` (`allowedRoots` in TypeScript, `AllowedRoots` in Go), and `write` and `edit` additionally refuse paths under `read_only_roots` (`readOnlyRoots`, `ReadOnlyRoots`). `EnvironmentWorker` adds the session's memory store directories to these lists itself. The confinement is a guardrail for the file tools only, not a sandbox; it does not constrain `bash`. **`beta_agent_toolset_20260401(env)`** takes an `AgentToolContext` and returns the standard tool implementations (`bash`, `read`, `write`, `edit`, `glob`, `grep`).

**With `EnvironmentWorker`:** both are managed automatically. Pass a `tools` factory to customize the tool list:

<CodeGroup exclude="shell">
  ```python Python
  EnvironmentWorker(client, ..., tools=lambda env: [beta_bash_tool(env), my_custom_tool])
  ```

  ```typescript TypeScript
  new EnvironmentWorker({
    client,
    environmentId,
    environmentKey,
    tools: (ctx) => [betaBashTool(ctx), myCustomTool]
  });
  ```

  ```csharp C#
  // EnvironmentWorker is not currently available in the C# SDK.
  // To answer custom tool calls directly, see the session event stream.
  ```

  ```go Go
  worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
  	EnvironmentID:  environmentID,
  	EnvironmentKey: environmentKey,
  	ToolsFunc: func(env *agenttoolset.AgentToolContext) []anthropic.BetaTool {
  		return []anthropic.BetaTool{agenttoolset.BetaBashTool(env), myCustomTool}
  	},
  })
  ```

  ```java Java
  // EnvironmentWorker is not currently available in the Java SDK.
  // To answer custom tool calls directly, see the session event stream.
  ```

  ```php PHP
  // EnvironmentWorker is not currently available in the PHP SDK.
  // To answer custom tool calls directly, see the session event stream.
  ```

  ```ruby Ruby
  # EnvironmentWorker is not currently available in the Ruby SDK.
  # To answer custom tool calls directly, see the session event stream.
  ```
</CodeGroup>

**With `work.poller()` and `tool_runner()`:** pass a tool list as `tools` to `client.beta.sessions.events.tool_runner()`. To build that list, set up `AgentToolContext` yourself and call `beta_agent_toolset_20260401(env)`:

<CodeGroup exclude="shell">
  ```python Python
  from anthropic.lib.tools.agent_toolset import (
      AgentToolContext,
      beta_agent_toolset_20260401,
  )

  async with AgentToolContext(
      workdir="/workspace", client=client, session_id=work.data.id
  ) as env:
      # skills downloaded to /workspace/skills/<name>/
      tools = beta_agent_toolset_20260401(env)
  ```

  ```typescript TypeScript
  import {
    setupSkills,
    betaAgentToolset20260401
  } from "@anthropic-ai/sdk/tools/agent-toolset/node";

  const ctx = { workdir: "/workspace", client, sessionId: work.data.id };
  await setupSkills(ctx);
  const tools = betaAgentToolset20260401(ctx);
  ```

  ```csharp C#
  // AgentToolContext is not currently available in the C# SDK.
  ```

  ```go Go
  env := &agenttoolset.AgentToolContext{Workdir: "/workspace"}
  if err := env.SetupSkills(ctx, client, work.Data.ID); err != nil {
  	panic(err)
  }
  // skills downloaded to /workspace/skills/<name>/
  tools := agenttoolset.BetaAgentToolset20260401(env)
  ```

  ```java Java
  // AgentToolContext is not currently available in the Java SDK.
  ```

  ```php PHP
  // AgentToolContext is not currently available in the PHP SDK.
  ```

  ```ruby Ruby
  # AgentToolContext is not currently available in the Ruby SDK.
  ```
</CodeGroup>

### Verify the worker is connected

From a separate shell, with `ANTHROPIC_API_KEY` set to your Claude API key (not the environment key), confirm `workers_polling` is at least 1:

```bash
ant beta:environments:work stats --environment-id "$ANTHROPIC_ENVIRONMENT_ID"
```

If `workers_polling` stays at 0, the worker isn't reaching the queue: confirm `ANTHROPIC_ENVIRONMENT_KEY` and `ANTHROPIC_ENVIRONMENT_ID` are set on the worker host. See [Read queue depth](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#read-queue-depth) for the full stats response and other language examples.

## Start a session

Once your worker is running, create a session that targets the environment. Set `AGENT_ID` to the agent ID you noted in [Before you begin](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#before-you-begin). The session enters the environment's work queue and waits there until a worker claims it; if no worker is connected, the session stays queued rather than failing.

Anthropic doesn't mount files or GitHub repositories into self-hosted sandboxes. To make session-specific files available, pass file references (such as an S3 path or commit SHA) in the session `metadata` field. The claimed work item doesn't carry the session's metadata, but it does carry the session ID: your spawn script or `--on-work` handler retrieves the session (`GET /v1/sessions/{session_id}`) to read the `metadata` field, then stages the files into the working directory before tool execution begins.

<CodeGroup>
  ```bash cURL
  curl -sS --fail-with-body https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$AGENT_ID",
    "environment_id": "$ANTHROPIC_ENVIRONMENT_ID",
    "metadata": {"input_file": "s3://my-bucket/data.csv"}
  }
  EOF
  ```

  ```bash CLI
  ant beta:sessions create \
    --agent "$AGENT_ID" \
    --environment-id "$ANTHROPIC_ENVIRONMENT_ID" \
    --metadata '{"input_file": "s3://my-bucket/data.csv"}'
  ```

  ```python Python
  session = client.beta.sessions.create(
      agent=agent.id,
      environment_id=environment.id,
      metadata={"input_file": "s3://my-bucket/data.csv"},
  )
  ```

  ```typescript TypeScript
  const session = await client.beta.sessions.create({
    agent: agent.id,
    environment_id: environment.id,
    metadata: { input_file: "s3://my-bucket/data.csv" }
  });
  ```

  ```csharp C#
  var session = await client.Beta.Sessions.Create(new()
  {
      Agent = agent.ID,
      EnvironmentID = environment.ID,
      Metadata = new Dictionary<string, string> { ["input_file"] = "s3://my-bucket/data.csv" },
  });
  ```

  ```go Go
  session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
  	Agent:         anthropic.BetaSessionNewParamsAgentUnion{OfString: anthropic.String(agent.ID)},
  	EnvironmentID: environment.ID,
  	Metadata: map[string]string{
  		"input_file": "s3://my-bucket/data.csv",
  	},
  })
  if err != nil {
  	panic(err)
  }
  ```

  ```java Java
  var session = client.beta().sessions().create(SessionCreateParams.builder()
      .agent(agent.id())
      .environmentId(environment.id())
      .metadata(SessionCreateParams.Metadata.builder()
          .putAdditionalProperty("input_file", JsonValue.from("s3://my-bucket/data.csv"))
          .build())
      .build());
  ```

  ```php PHP
  $session = $client->beta->sessions->create(
      agent: $agent->id,
      environmentID: $environment->id,
      metadata: ['input_file' => 's3://my-bucket/data.csv'],
  );
  ```

  ```ruby Ruby
  session = client.beta.sessions.create(
    agent: agent.id,
    environment_id: environment.id,
    metadata: {input_file: "s3://my-bucket/data.csv"}
  )
  ```
</CodeGroup>

<Note>
  Self-hosted sandboxes support `memory_store` resources only; see [Use memory stores](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#use-memory-stores). A session on a self-hosted environment that includes a `file` or `github_repository` resource is rejected with a 400 error:

  ```text wrap
  Environment env_... is a self-hosted environment. `resources` are not supported with self-hosted environments.
  ```

  [Deployments](https://platform.claude.com/docs/en/managed-agents/scheduled-deployments) that target a self-hosted environment follow the same rule.
</Note>

See [Self-hosted worker](https://platform.claude.com/docs/en/managed-agents/reference#self-hosted-worker) in the reference for the full list of CLI flags, and [SDK helpers](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#sdk-helpers) for the SDK helper options.

## Use memory stores

Sessions on a self-hosted environment attach [memory stores](https://platform.claude.com/docs/en/managed-agents/memory) exactly as sessions on cloud environments do: list them in `resources` when you create the session, as shown in [Attach a memory store to a session](https://platform.claude.com/docs/en/managed-agents/memory#attach-a-memory-store-to-a-session). A session accepts up to 8 memory stores. On a self-hosted environment the SDK worker, rather than Anthropic's infrastructure, materializes each store for the agent, so memory stores there require `EnvironmentWorker` (or its `handle_item()` method) from the Python, TypeScript, or Go SDK.

The `ant` CLI worker (`ant beta:worker poll` and `ant beta:worker run`) does not mount memory stores. To combine the CLI poller with memory stores, run the SDK worker inside a per-session sandbox as described in [Run one sandbox per session](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session).

Memory stores cannot be attached to sessions on self-hosted environments on [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws).

### How the worker handles memory

When the worker claims a work item whose session has memory stores attached, it:

1. Downloads each attached store to its `mount_path` on the worker host, authenticating with the work item's per-session `secret`. The `mount_path` is the same directory under `/mnt/memory/` that cloud sessions use (for example, `/mnt/memory/user-preferences/` for a store named "User Preferences"), and the session's system prompt describes it to the agent.
2. Adds those directories to the file tools' allowed roots, and the directories of stores attached with `access: "read_only"` to their read-only roots, so the agent works on memories with the same `read`, `write`, `edit`, `glob`, and `grep` tools it uses in the working directory.
3. Reconciles local and remote changes after tool calls, at most once per sync interval (15 seconds by default): memories that changed in the store are written to disk, and files the agent changed are uploaded to the store.
4. Runs a final sync when the session ends, flushes any uploads still pending for up to 30 seconds, and then removes the directories it created. A worker that is cancelled while a session runs skips the final sync but still uploads changed files and removes the directories before it exits.

The memory store on Anthropic's side remains the source of truth. [Memory versions](https://platform.claude.com/docs/en/managed-agents/memory#audit-memory-changes), redaction, and viewing or editing memories in the Console work as they do for cloud sessions, and the agent's memory reads and writes appear in the [event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming) as ordinary tool events. Because each worker syncs on an interval, a change written in one session becomes visible to another running session only after both have synced, typically well under a minute at the default interval; sessions on cloud sandboxes see each other's changes almost immediately.

Each store directory contains a marker file named `.anthropic-memory-store` that ties the directory to its store. Leave it in place: the worker does not sync a directory whose marker is missing or altered.

### Prepare the host

Memory stores on self-hosted sandboxes need a POSIX filesystem on the worker host (the Linux host from [Before you begin](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#before-you-begin)); Windows hosts are not supported, because the worker requires `O_NOFOLLOW` when it opens memory files. A case-sensitive filesystem is recommended, so that memory paths that differ only in case do not collide.

Before you start the worker, create the parent directory and make it writable by the user the worker runs as:

```bash
sudo mkdir -p /mnt/memory && sudo chown "$USER" /mnt/memory
```

Do not create the per-store directories yourself. The worker creates each store's `mount_path` directory (for example, `/mnt/memory/user-preferences`) when a session starts, refuses to start the session's work if something already exists at that path, and removes the directory when the session ends. Two operating rules follow:

* **Run one session per filesystem when sessions attach the same store.** Two sessions cannot mount the same store on one host at the same time, because both need the same path. Giving each session its own sandbox, as described in [Run one sandbox per session](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session), satisfies this rule.
* **Stop workers gracefully.** When you stop a worker while a session runs, `EnvironmentWorker` uploads the session's changed memory files and removes its store directories only if it is cancelled rather than killed: a killed process runs no teardown, and the worker does not install signal handlers itself. Wire SIGTERM and SIGINT to cancellation in the process that runs it: abort the `signal` you pass to the worker in TypeScript, cancel the context in Go, and in Python cancel the task that runs `run()` or `handle_item()` from a signal handler. Then stop workers with SIGTERM and give them at least 30 seconds to exit before any hard kill, because the final upload can take that long. If a worker is killed before its teardown runs, remove the leftover store directory under `/mnt/memory/` before the next session that attaches that store; any edits in it that had not synced are lost.

### Run one sandbox per session

The sandbox-per-session pattern in [Run a worker](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#run-a-worker) gives each session a fresh filesystem, which is what [Prepare the host](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#prepare-the-host) calls for when sessions attach the same store. Keep `ant beta:worker poll --on-work` (or the SDK's work poller) as the poller on the host.

The `ant beta:worker run` entrypoint shown there does not mount memory stores, so build the per-session image around the SDK worker instead: its entrypoint constructs `EnvironmentWorker` and calls `handle_item()` (`handleItem` in TypeScript, `HandleItem` in Go), which reads the session, work, and environment identifiers from the `ANTHROPIC_*` variables and the work item's per-session `secret` from `ANTHROPIC_WORK_SECRET`. You can also pass the secret explicitly as `work_secret` (`workSecret` in TypeScript, `WorkSecret` in Go).

<CodeGroup exclude="shell">
  ```python Python
  import asyncio
  import contextlib
  import os
  import signal
  from anthropic import AsyncAnthropic
  from anthropic.lib.environments import EnvironmentWorker


  async def main() -> None:
      async with AsyncAnthropic(auth_token=os.environ["ANTHROPIC_ENVIRONMENT_KEY"]) as client:
          worker = EnvironmentWorker(client, workdir="/workspace")
          # With no arguments, handle_item() reads the ANTHROPIC_* variables the spawn
          # script forwarded, including ANTHROPIC_WORK_SECRET.
          task = asyncio.create_task(worker.handle_item())
          # Cancelling the task when the container is stopped lets the worker upload
          # changed memory files and remove the store directories before it exits.
          loop = asyncio.get_running_loop()
          for signum in (signal.SIGINT, signal.SIGTERM):
              loop.add_signal_handler(signum, task.cancel)
          with contextlib.suppress(asyncio.CancelledError):
              await task


  asyncio.run(main())
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { EnvironmentWorker } from "@anthropic-ai/sdk/helpers/beta/environments";

  const client = new Anthropic({ authToken: process.env.ANTHROPIC_ENVIRONMENT_KEY });
  const controller = new AbortController();
  // Aborting when the container is stopped lets the worker upload changed memory
  // files and remove the store directories before it exits.
  process.once("SIGTERM", () => controller.abort());
  process.once("SIGINT", () => controller.abort());

  // With no arguments, handleItem() reads the ANTHROPIC_* variables the spawn
  // script forwarded, including ANTHROPIC_WORK_SECRET.
  await new EnvironmentWorker({
    client,
    workdir: "/workspace",
    signal: controller.signal
  }).handleItem();
  ```

  ```csharp C#
  // EnvironmentWorker is not currently available in the C# SDK.
  ```

  ```go Go
  package main

  import (
  	"context"
  	"log"
  	"os"
  	"os/signal"
  	"syscall"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/lib/environments"
  	"github.com/anthropics/anthropic-sdk-go/option"
  )

  func main() {
  	// Cancelling the context when the container is stopped lets the worker upload
  	// changed memory files and remove the store directories before it exits.
  	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
  	defer stop()

  	client := anthropic.NewClient(option.WithAuthToken(os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")))
  	worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
  		Workdir: "/workspace",
  	})
  	// With zero-value options, HandleItem reads the ANTHROPIC_* variables the spawn
  	// script forwarded, including ANTHROPIC_WORK_SECRET.
  	if err := worker.HandleItem(ctx, environments.HandleItemOptions{}); err != nil {
  		log.Fatalf("worker: %v", err)
  	}
  }

  ```

  ```java Java
  // EnvironmentWorker is not currently available in the Java SDK.
  ```

  ```php PHP
  // EnvironmentWorker is not currently available in the PHP SDK.
  ```

  ```ruby Ruby
  # EnvironmentWorker is not currently available in the Ruby SDK.
  ```
</CodeGroup>

`ant beta:worker poll --on-work` does not set `ANTHROPIC_WORK_SECRET` for the script it spawns, so the spawn script reads the secret from the work item JSON on its standard input and passes it into the sandbox:

```bash
#!/bin/bash
# spawn.sh: called once per claimed work item
# The claimed work item arrives as JSON on stdin. Its secret is the
# per-session credential that the memory store endpoints require.
ANTHROPIC_WORK_SECRET="$(jq -r '.secret // empty')"
export ANTHROPIC_WORK_SECRET
mkdir -p "/host/outputs/$ANTHROPIC_SESSION_ID"
exec docker run --rm \
  -e ANTHROPIC_SESSION_ID -e ANTHROPIC_ENVIRONMENT_KEY \
  -e ANTHROPIC_WORK_ID -e ANTHROPIC_ENVIRONMENT_ID -e ANTHROPIC_BASE_URL \
  -e ANTHROPIC_WORK_SECRET \
  -v "/host/outputs/$ANTHROPIC_SESSION_ID":/workspace \
  your-sdk-worker-image
```

If you claim work with the SDK's work poller instead, pass each claimed item's `secret` into the sandbox you launch in the same way. Pass it only into the sandbox that serves that session, and never log it.

The sandbox image also needs a writable `/mnt/memory` (see [Prepare the host](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#prepare-the-host)). Because each sandbox serves one session and is discarded afterward, no leftover directories need cleanup, and the memory directories do not need to be bind-mounted to the host: the worker uploads their contents to the store before the sandbox exits. If you stop a container before its session ends, send a signal that the entrypoint turns into cancellation (see [Prepare the host](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#prepare-the-host)) rather than killing it, so that upload still runs. Give the container time to finish the upload as well: Docker follows the stop signal with SIGKILL after 10 seconds by default, so raise that limit to at least the 30 seconds that Prepare the host calls for, with `--stop-timeout` on `docker run` or your orchestrator's termination grace period.

### Configure sync

Two `EnvironmentWorker` options control memory behavior:

* **`memory_sync_interval`** (Python, in seconds; `memorySyncIntervalMs` in TypeScript, in milliseconds; `MemorySyncInterval` in Go, a duration): how often attached stores reconcile with the server while the session runs. Defaults to 15 seconds; the minimum is 5 seconds. A shorter interval narrows the window in which another session sees stale memories, at the cost of more memory store requests. `None` in Python, `null` in TypeScript, or a negative duration in Go disables memory support entirely: the worker neither downloads nor syncs stores, and a session with memory stores attached runs without them even though its system prompt still describes them, so disable memory support only on workers whose sessions attach no memory stores. While memory support is enabled, a work item that arrives without a per-session `secret` for a session with attached stores fails rather than running without memory (see [Troubleshoot memory mounts](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#troubleshoot-memory-mounts)).
* **`memory_sync_deletions`** (`memorySyncDeletions` in TypeScript, `MemorySyncDeletions` in Go): whether a file the agent deletes locally is also deleted from the store. The value is one of `"enabled"` (the default), `"log_only"`, or `"disabled"` in Python and TypeScript, and one of the constants `environments.MemorySyncDeletionsEnabled` (the zero value), `environments.MemorySyncDeletionsLogOnly`, or `environments.MemorySyncDeletionsDisabled` in Go. When enabled, the worker deletes the memory from the store once a later sync confirms the file is still gone; in log-only mode it runs the same checks but only logs what it would have deleted, which lets you watch what your workers would delete before you trust the enabled mode; when disabled, it never deletes from the store. Uploads and downloads are unaffected by this setting.

Set these options where you construct the worker, whether through the `EnvironmentWorker` constructor or, in Python and TypeScript, the `client.beta.environments.work.worker()` factory that the webhook handler uses.

For example, to sync every 10 seconds and only log the deletes the worker would have made:

<CodeGroup exclude="shell">
  ```python Python
  worker = EnvironmentWorker(
      client,
      environment_id=environment_id,
      environment_key=environment_key,
      workdir="/workspace",
      memory_sync_interval=10,  # seconds
      memory_sync_deletions="log_only",
  )
  ```

  ```typescript TypeScript
  const worker = new EnvironmentWorker({
    client,
    environmentId,
    environmentKey,
    workdir: "/workspace",
    memorySyncIntervalMs: 10_000,
    memorySyncDeletions: "log_only"
  });
  ```

  ```csharp C#
  // EnvironmentWorker is not currently available in the C# SDK.
  ```

  ```go Go
  worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
  	EnvironmentID:       environmentID,
  	EnvironmentKey:      environmentKey,
  	Workdir:             "/workspace",
  	MemorySyncInterval:  10 * time.Second,
  	MemorySyncDeletions: environments.MemorySyncDeletionsLogOnly,
  })
  ```

  ```java Java
  // EnvironmentWorker is not currently available in the Java SDK.
  ```

  ```php PHP
  // EnvironmentWorker is not currently available in the PHP SDK.
  ```

  ```ruby Ruby
  # EnvironmentWorker is not currently available in the Ruby SDK.
  ```
</CodeGroup>

### Read-only stores and conflicts

For a store attached with `access: "read_only"`, the `write` and `edit` tools refuse to change files inside its directory, and the worker never uploads anything from it. Changes made through `bash` are not blocked locally: they are never synced to the store, and the next remote change to that memory overwrites them. If you need the local copy itself to stay unchanged during the session, disable the `bash` tool for that agent; do not mount the store path read-only, because the worker itself must create the directory and write the downloaded memories into it.

Conflicts resolve in favor of the store. When the agent changes a memory file that also changed in the store since the session last synced it, the worker keeps the store's version at the next sync, overwrites the local file with it, and logs a warning; the `write` and `edit` tools themselves succeed and no error reaches the agent. If the agent's change still applies, it can re-read the file after the sync and make the change again.

### Troubleshoot memory mounts

The worker logs mount and background sync failures rather than reporting them to the session; only read-only refusals reach the agent, as tool errors (see [Read-only stores and conflicts](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#read-only-stores-and-conflicts)). If a memory store cannot be mounted when the worker claims a session, the worker fails the work item: the session emits no error event and stays idle.

| Symptom                                                                                                                                 | Cause                                                                                                                                                                                                          | Fix                                                                                                                                                                                                                                                                                                                              |
| --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The worker log contains `the work item carried no sessions token` (in Go, the `ErrSessionMemoryNoToken` error) and the work item fails. | The work item's per-session `secret` did not reach the worker: memory stores on self-hosted sandboxes are not enabled for your organization, or your spawn script did not forward the secret into the sandbox. | In the sandbox-per-session pattern, forward `ANTHROPIC_WORK_SECRET` into the sandbox as shown in [Run one sandbox per session](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#run-one-sandbox-per-session). If the worker polls and runs sessions in one process and still logs this, contact support. |
| The worker log contains `something already exists at the memory store's path`.                                                          | A directory left over from a previous session, usually one whose worker was killed before its teardown ran.                                                                                                    | Remove the leftover directory that the log line names. Edits in it that had not synced are lost.                                                                                                                                                                                                                                 |
| The worker log contains `cannot create the memory store's folder` and `the worker host must make this mount path writable`.             | The user the worker runs as cannot create directories under `/mnt/memory`.                                                                                                                                     | Create `/mnt/memory` and `chown` it to that user; see [Prepare the host](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#prepare-the-host).                                                                                                                                                             |
| The session sits `idle` with a `requires_action` stop reason and no error event shortly after a worker claimed it.                      | The worker failed the work item because it could not mount a memory store, for one of the preceding reasons.                                                                                                   | Fix the cause on the host, then send a [`user.interrupt`](https://platform.claude.com/docs/en/managed-agents/events-and-streaming#integrating-events) event: the session's work is queued again and the next worker that claims it retries the mount.                                                                            |

## Serve custom tools from your sandbox

[Custom tools](https://platform.claude.com/docs/en/managed-agents/tools#custom-tools) are tools your own code executes: the agent emits an `agent.custom_tool_use` event and waits for a matching `user.custom_tool_result`. The worker can be that code, and because it runs inside your sandbox, the tool reaches the internal services, credentials, and network egress you configured for the sandbox, and nothing more. The environment key authorizes posting custom tool results, so your Claude API key stays off the worker host.

<Note>
  Serving custom tools requires the SDK worker: the `ant` CLI worker has no way to register a custom tool implementation. In the sandbox-per-session pattern, run `EnvironmentWorker` inside the sandbox with `handle_item()` (`handleItem` in TypeScript, `HandleItem` in Go) in place of `ant beta:worker run`.
</Note>

<Steps>
  <Step title="Declare the tool on the agent">
    Add a `custom` entry to the agent's `tools` whose `name` matches the tool your worker registers. See [Custom tools](https://platform.claude.com/docs/en/managed-agents/tools#custom-tools) for the full declaration shape.

    ```json
    {
      "type": "custom",
      "name": "get_order_status",
      "description": "Look up an order in the internal fulfillment system by order ID.",
      "input_schema": {
        "type": "object",
        "properties": {
          "order_id": { "type": "string", "description": "The order ID" }
        },
        "required": ["order_id"]
      }
    }
    ```
  </Step>

  <Step title="Register the implementation with the worker">
    Pass the tool through the worker's `tools` factory (see [SDK helpers](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes#sdk-helpers)), alongside the built-in toolset:

    <CodeGroup exclude="shell">
      ```python Python
      import asyncio
      import os
      from anthropic import AsyncAnthropic, beta_async_tool
      from anthropic.lib.environments import EnvironmentWorker
      from anthropic.lib.tools.agent_toolset import beta_agent_toolset_20260401


      @beta_async_tool
      async def get_order_status(order_id: str) -> str:
          """Look up an order in the internal fulfillment system by order ID."""
          # Runs on the worker host: call anything the sandbox can reach.
          return f"Order {order_id}: shipped"


      async def main() -> None:
          environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
          environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
          async with AsyncAnthropic(auth_token=environment_key) as client:
              await EnvironmentWorker(
                  client,
                  environment_id=environment_id,
                  environment_key=environment_key,
                  workdir="/workspace",
                  tools=lambda env: [*beta_agent_toolset_20260401(env), get_order_status],
              ).run()


      asyncio.run(main())
      ```

      ```typescript TypeScript
      import Anthropic from "@anthropic-ai/sdk";
      import { EnvironmentWorker } from "@anthropic-ai/sdk/helpers/beta/environments";
      import { betaTool } from "@anthropic-ai/sdk/helpers/beta/json-schema";
      import { betaAgentToolset20260401 } from "@anthropic-ai/sdk/tools/agent-toolset/node";

      const getOrderStatus = betaTool({
        name: "get_order_status",
        description: "Look up an order in the internal fulfillment system by order ID.",
        inputSchema: {
          type: "object",
          properties: { order_id: { type: "string", description: "The order ID" } },
          required: ["order_id"]
        },
        // Runs on the worker host: call anything the sandbox can reach.
        run: async ({ order_id }) => `Order ${order_id}: shipped`
      });

      const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
      const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
      const client = new Anthropic({ authToken: environmentKey });
      const controller = new AbortController();
      process.once("SIGTERM", () => controller.abort());

      await new EnvironmentWorker({
        client,
        environmentId,
        environmentKey,
        workdir: "/workspace",
        signal: controller.signal,
        tools: (ctx) => [...betaAgentToolset20260401(ctx), getOrderStatus]
      }).run();
      ```

      ```csharp C#
      // EnvironmentWorker is not currently available in the C# SDK.
      // To answer custom tool calls directly, see the session event stream.
      ```

      ```go Go
      package main

      import (
      	"context"
      	"log"
      	"os"
      	"os/signal"
      	"syscall"

      	"github.com/anthropics/anthropic-sdk-go"
      	"github.com/anthropics/anthropic-sdk-go/lib/environments"
      	"github.com/anthropics/anthropic-sdk-go/option"
      	"github.com/anthropics/anthropic-sdk-go/toolrunner"
      	"github.com/anthropics/anthropic-sdk-go/tools/agenttoolset"
      )

      type orderStatusInput struct {
      	OrderID string `json:"order_id"`
      }

      func main() {
      	environmentKey := os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")
      	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")

      	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
      	defer stop()

      	getOrderStatus := toolrunner.NewBetaTool(
      		"get_order_status",
      		"Look up an order in the internal fulfillment system by order ID.",
      		anthropic.BetaToolInputSchemaParam{
      			Properties: map[string]any{
      				"order_id": map[string]any{"type": "string", "description": "The order ID"},
      			},
      			Required: []string{"order_id"},
      		},
      		// Runs on the worker host: call anything the sandbox can reach.
      		func(ctx context.Context, input orderStatusInput) (anthropic.BetaToolResultBlockParamContentUnion, error) {
      			return anthropic.BetaToolResultBlockParamContentUnion{
      				OfText: &anthropic.BetaTextBlockParam{Text: "Order " + input.OrderID + ": shipped"},
      			}, nil
      		},
      	)

      	client := anthropic.NewClient(option.WithAuthToken(environmentKey))

      	worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
      		EnvironmentID:  environmentID,
      		EnvironmentKey: environmentKey,
      		Workdir:        "/workspace",
      		ToolsFunc: func(env *agenttoolset.AgentToolContext) []anthropic.BetaTool {
      			return append(agenttoolset.BetaAgentToolset20260401(env), getOrderStatus)
      		},
      	})
      	if err := worker.Run(ctx); err != nil {
      		log.Fatalf("worker: %v", err)
      	}
      }

      ```

      ```java Java
      // EnvironmentWorker is not currently available in the Java SDK.
      // To answer custom tool calls directly, see the session event stream.
      ```

      ```php PHP
      // EnvironmentWorker is not currently available in the PHP SDK.
      // To answer custom tool calls directly, see the session event stream.
      ```

      ```ruby Ruby
      # EnvironmentWorker is not currently available in the Ruby SDK.
      # To answer custom tool calls directly, see the session event stream.
      ```
    </CodeGroup>
  </Step>
</Steps>

The worker answers only the tools registered with it. A custom tool that is declared on the agent but registered with no worker or client leaves the session paused with a `requires_action` stop reason until something posts its result; see [Handling custom tool calls](https://platform.claude.com/docs/en/managed-agents/events-and-streaming#handling-custom-tool-calls) for the event flow.

### Wrap an MCP server as custom tools

The [MCP connector](https://platform.claude.com/docs/en/managed-agents/mcp-connector) connects to MCP servers from Anthropic's side, so a server must expose an HTTP endpoint that Anthropic can reach, directly or through an [MCP tunnel](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview). To use a server that only your network can reach, make the worker the MCP client instead and declare the server's tools as custom tools. The MCP server needs no inbound connectivity from outside your network; Anthropic receives the tool definitions you declare on the agent, each call's input, and the result your worker posts back. At runtime the model calls a wrapped tool like any other custom tool:

1. The agent emits an `agent.custom_tool_use` event.
2. The worker, inside your sandbox, forwards the call over its open MCP session to the server on your network.
3. The worker posts the server's response as the `user.custom_tool_result`.

The SDKs' [Client-side MCP helpers](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector#client-side-mcp-helpers) convert the server's tools into the runnable tools the worker accepts; install an MCP SDK alongside the Anthropic SDK (`pip install "anthropic[mcp]" "mcp>=1.24"`, `npm install @modelcontextprotocol/sdk`, `go get github.com/modelcontextprotocol/go-sdk`). The examples connect without authentication; to send credentials, configure the HTTP client or request options you hand to the MCP transport (`http_client` in Python, `requestInit` in TypeScript, `HTTPClient` in Go).

<Steps>
  <Step title="Declare the server's tools on the agent">
    List the MCP server's tools and declare each one as a `custom` tool; the MCP `name`, `description`, and `inputSchema` map one to one onto the custom tool's fields. If the server paginates its tool list, declare every page; the worker must list the same pages.

    <CodeGroup exclude="shell">
      ```python Python
      import asyncio
      from typing import Any, cast
      from anthropic import AsyncAnthropic
      from anthropic.types.beta import BetaManagedAgentsCustomToolParams
      from mcp import ClientSession, types
      # Requires mcp >= 1.24, which renamed streamablehttp_client to streamable_http_client.
      from mcp.client.streamable_http import streamable_http_client

      MCP_SERVER_URL = "http://mcp.internal.example.com:8000/mcp"


      def to_custom_tool(tool: types.Tool) -> BetaManagedAgentsCustomToolParams:
          # The MCP fields map one to one onto a custom tool declaration. The cast
          # hands the schema dictionary to the SDK's typed parameter unchanged.
          return {
              "type": "custom",
              "name": tool.name,
              "description": tool.description or tool.name,
              "input_schema": cast(Any, tool.inputSchema),
          }


      async def main() -> None:
          # Run this wherever you create agents, not on the worker host: it
          # authenticates with your Claude API key (ANTHROPIC_API_KEY).
          async with (
              streamable_http_client(MCP_SERVER_URL) as (read, write, _),
              ClientSession(read, write) as mcp_session,
              AsyncAnthropic() as client,
          ):
              await mcp_session.initialize()
              listed = await mcp_session.list_tools()
              agent = await client.beta.agents.create(
                  name="Internal tools agent",
                  model="claude-opus-5",
                  tools=[
                      {"type": "agent_toolset_20260401"},
                      *[to_custom_tool(tool) for tool in listed.tools],
                  ],
              )
              print(agent.id)


      asyncio.run(main())
      ```

      ```typescript TypeScript
      import Anthropic from "@anthropic-ai/sdk";
      import { Client } from "@modelcontextprotocol/sdk/client/index.js";
      import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

      const MCP_SERVER_URL = "http://mcp.internal.example.com:8000/mcp";

      // Run this wherever you create agents, not on the worker host: it
      // authenticates with your Claude API key (ANTHROPIC_API_KEY).
      const client = new Anthropic();

      const mcpClient = new Client({ name: "declare-agent-tools", version: "1.0.0" });
      await mcpClient.connect(new StreamableHTTPClientTransport(new URL(MCP_SERVER_URL)));
      const { tools } = await mcpClient.listTools();

      const agent = await client.beta.agents.create({
        name: "Internal tools agent",
        model: "claude-opus-5",
        tools: [
          { type: "agent_toolset_20260401" },
          // The MCP fields map one to one onto a custom tool declaration.
          ...tools.map((tool) => ({
            type: "custom" as const,
            name: tool.name,
            description: tool.description || tool.name,
            input_schema: tool.inputSchema
          }))
        ]
      });
      console.log(agent.id);

      await mcpClient.close();
      ```

      ```csharp C#
      // See the Python, TypeScript, and Go tabs. Declaring custom tools from
      // C# works the same way once you list the server's tools with an MCP client.
      ```

      ```go Go
      package main

      import (
      	"context"
      	"encoding/json"
      	"fmt"
      	"log"

      	"github.com/anthropics/anthropic-sdk-go"
      	mcpsdk "github.com/modelcontextprotocol/go-sdk/mcp"
      )

      const mcpServerURL = "http://mcp.internal.example.com:8000/mcp"

      // toCustomTool maps one MCP tool definition onto a custom tool declaration.
      // The fields map one to one: the typed parameter carries `properties` and
      // `required`, and every other JSON Schema keyword the server emits travels in
      // ExtraFields so the declared schema matches the server's schema.
      func toCustomTool(tool *mcpsdk.Tool) (anthropic.BetaAgentNewParamsToolUnion, error) {
      	raw, err := json.Marshal(tool.InputSchema)
      	if err != nil {
      		return anthropic.BetaAgentNewParamsToolUnion{}, err
      	}
      	var schema map[string]any
      	if err := json.Unmarshal(raw, &schema); err != nil {
      		return anthropic.BetaAgentNewParamsToolUnion{}, err
      	}

      	inputSchema := anthropic.BetaManagedAgentsCustomToolInputSchemaParam{ExtraFields: map[string]any{}}
      	for keyword, value := range schema {
      		switch keyword {
      		case "type":
      			// The parameter type always marshals "type": "object".
      		case "properties":
      			properties, _ := value.(map[string]any)
      			inputSchema.Properties = properties
      		case "required":
      			entries, _ := value.([]any)
      			for _, entry := range entries {
      				if name, isString := entry.(string); isString {
      					inputSchema.Required = append(inputSchema.Required, name)
      				}
      			}
      		default:
      			inputSchema.ExtraFields[keyword] = value
      		}
      	}

      	description := tool.Description
      	if description == "" {
      		description = tool.Name
      	}
      	return anthropic.BetaAgentNewParamsToolUnion{
      		OfCustom: &anthropic.BetaManagedAgentsCustomToolParams{
      			Type:        anthropic.BetaManagedAgentsCustomToolParamsTypeCustom,
      			Name:        tool.Name,
      			Description: description,
      			InputSchema: inputSchema,
      		},
      	}, nil
      }

      func main() {
      	ctx := context.Background()

      	// Run this wherever you create agents, not on the worker host: it
      	// authenticates with your Claude API key (ANTHROPIC_API_KEY).
      	client := anthropic.NewClient()

      	mcpClient := mcpsdk.NewClient(&mcpsdk.Implementation{Name: "declare-agent-tools", Version: "1.0.0"}, nil)
      	session, err := mcpClient.Connect(ctx, &mcpsdk.StreamableClientTransport{Endpoint: mcpServerURL}, nil)
      	if err != nil {
      		log.Fatalf("connect to MCP server: %v", err)
      	}
      	defer session.Close()

      	listed, err := session.ListTools(ctx, nil)
      	if err != nil {
      		log.Fatalf("list MCP tools: %v", err)
      	}

      	tools := []anthropic.BetaAgentNewParamsToolUnion{
      		{OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{
      			Type: anthropic.BetaManagedAgentsAgentToolset20260401ParamsTypeAgentToolset20260401,
      		}},
      	}
      	for _, tool := range listed.Tools {
      		custom, err := toCustomTool(tool)
      		if err != nil {
      			log.Fatalf("convert MCP tool %s: %v", tool.Name, err)
      		}
      		tools = append(tools, custom)
      	}

      	agent, err := client.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
      		Name:  "Internal tools agent",
      		Model: anthropic.BetaManagedAgentsModelConfigParams{ID: anthropic.BetaManagedAgentsModelClaudeOpus5},
      		Tools: tools,
      	})
      	if err != nil {
      		log.Fatalf("create agent: %v", err)
      	}
      	fmt.Println(agent.ID)
      }

      ```

      ```java Java
      // See the Python, TypeScript, and Go tabs. Declaring custom tools from
      // Java works the same way once you list the server's tools with an MCP client.
      ```

      ```php PHP
      // See the Python, TypeScript, and Go tabs. Declaring custom tools from
      // PHP works the same way once you list the server's tools with an MCP client.
      ```

      ```ruby Ruby
      # See the Python, TypeScript, and Go tabs. Declaring custom tools from
      # Ruby works the same way once you list the server's tools with an MCP client.
      ```
    </CodeGroup>
  </Step>

  <Step title="Serve the tools from the worker">
    Connect to the same MCP server at startup, convert its tools with the MCP helpers, and register them alongside the built-in toolset. Keep one MCP session open for the life of the worker.

    <CodeGroup exclude="shell">
      ```python Python
      import asyncio
      import os
      from datetime import timedelta
      from anthropic import AsyncAnthropic
      from anthropic.lib.environments import EnvironmentWorker
      from anthropic.lib.tools.agent_toolset import beta_agent_toolset_20260401
      from anthropic.lib.tools.mcp import async_mcp_tool
      from mcp import ClientSession
      # Requires mcp >= 1.24, which renamed streamablehttp_client to streamable_http_client.
      from mcp.client.streamable_http import streamable_http_client

      MCP_SERVER_URL = "http://mcp.internal.example.com:8000/mcp"


      async def main() -> None:
          environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
          environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
          # Connect to the MCP server once at startup and keep the session open for
          # the life of the worker. The timeout turns a hung tool call into an error
          # result instead of a stalled call.
          async with (
              streamable_http_client(MCP_SERVER_URL) as (read, write, _),
              ClientSession(read, write, read_timeout_seconds=timedelta(seconds=60)) as mcp_session,
              AsyncAnthropic(auth_token=environment_key) as client,
          ):
              await mcp_session.initialize()
              listed = await mcp_session.list_tools()
              mcp_tools = [async_mcp_tool(tool, mcp_session) for tool in listed.tools]
              await EnvironmentWorker(
                  client,
                  environment_id=environment_id,
                  environment_key=environment_key,
                  workdir="/workspace",
                  tools=lambda env: [*beta_agent_toolset_20260401(env), *mcp_tools],
              ).run()


      asyncio.run(main())
      ```

      ```typescript TypeScript
      import Anthropic from "@anthropic-ai/sdk";
      import { EnvironmentWorker } from "@anthropic-ai/sdk/helpers/beta/environments";
      import {
        mcpTools,
        type MCPCallToolResultLike,
        type MCPClientLike
      } from "@anthropic-ai/sdk/helpers/beta/mcp";
      import { betaAgentToolset20260401 } from "@anthropic-ai/sdk/tools/agent-toolset/node";
      import { Client } from "@modelcontextprotocol/sdk/client/index.js";
      import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

      const MCP_SERVER_URL = "http://mcp.internal.example.com:8000/mcp";

      const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
      const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
      const client = new Anthropic({ authToken: environmentKey });
      const controller = new AbortController();
      process.once("SIGTERM", () => controller.abort());

      // Connect to the MCP server once at startup and keep the connection open for
      // the life of the worker.
      const mcpClient = new Client({ name: "sandbox-worker", version: "1.0.0" });
      await mcpClient.connect(new StreamableHTTPClientTransport(new URL(MCP_SERVER_URL)));
      const { tools } = await mcpClient.listTools();

      // The MCP SDK's callTool return type still includes a legacy result shape that
      // mcpTools does not accept; narrow it. Drop this once MCPClientLike widens.
      const mcpClientForTools: MCPClientLike = {
        callTool: (params) => mcpClient.callTool(params) as Promise<MCPCallToolResultLike>
      };

      await new EnvironmentWorker({
        client,
        environmentId,
        environmentKey,
        workdir: "/workspace",
        signal: controller.signal,
        tools: (ctx) => [...betaAgentToolset20260401(ctx), ...mcpTools(tools, mcpClientForTools)]
      }).run();
      ```

      ```csharp C#
      // EnvironmentWorker is not currently available in the C# SDK.
      ```

      ```go Go
      package main

      import (
      	"context"
      	"log"
      	"os"
      	"os/signal"
      	"syscall"

      	"github.com/anthropics/anthropic-sdk-go"
      	"github.com/anthropics/anthropic-sdk-go/lib/environments"
      	"github.com/anthropics/anthropic-sdk-go/mcp"
      	"github.com/anthropics/anthropic-sdk-go/option"
      	"github.com/anthropics/anthropic-sdk-go/tools/agenttoolset"
      	mcpsdk "github.com/modelcontextprotocol/go-sdk/mcp"
      )

      const mcpServerURL = "http://mcp.internal.example.com:8000/mcp"

      func main() {
      	environmentKey := os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")
      	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")

      	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
      	defer stop()

      	client := anthropic.NewClient(option.WithAuthToken(environmentKey))

      	// Connect to the MCP server once at startup and keep the session open for
      	// the life of the worker.
      	mcpClient := mcpsdk.NewClient(&mcpsdk.Implementation{Name: "sandbox-worker", Version: "1.0.0"}, nil)
      	session, err := mcpClient.Connect(ctx, &mcpsdk.StreamableClientTransport{Endpoint: mcpServerURL}, nil)
      	if err != nil {
      		log.Fatalf("connect to MCP server: %v", err)
      	}
      	defer session.Close()

      	listed, err := session.ListTools(ctx, nil)
      	if err != nil {
      		log.Fatalf("list MCP tools: %v", err)
      	}
      	mcpTools, err := mcp.NewBetaTools(listed.Tools, session)
      	if err != nil {
      		log.Fatalf("convert MCP tools: %v", err)
      	}

      	worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
      		EnvironmentID:  environmentID,
      		EnvironmentKey: environmentKey,
      		Workdir:        "/workspace",
      		ToolsFunc: func(env *agenttoolset.AgentToolContext) []anthropic.BetaTool {
      			return append(agenttoolset.BetaAgentToolset20260401(env), mcpTools...)
      		},
      	})
      	if err := worker.Run(ctx); err != nil {
      		log.Fatalf("worker: %v", err)
      	}
      }

      ```

      ```java Java
      // EnvironmentWorker is not currently available in the Java SDK.
      ```

      ```php PHP
      // EnvironmentWorker is not currently available in the PHP SDK.
      ```

      ```ruby Ruby
      # EnvironmentWorker is not currently available in the Ruby SDK.
      ```
    </CodeGroup>
  </Step>
</Steps>

Keep the following in mind when you wrap an MCP server:

* **Tools are declared, not discovered at runtime.** The worker lists the MCP server's tools once at startup and cannot add tools to a running session. When the server's tools change, declare them again, on the agent or on an idle session through [Updating the agent configuration](https://platform.claude.com/docs/en/managed-agents/session-operations#updating-the-agent-configuration), and restart the worker.
* **Names and descriptions must fit the Managed Agents API.** Custom tool names are unique per agent and use letters, digits, underscores, and hyphens (1–128 characters); a non-empty description is required; and an agent's `tools` array takes at most 128 entries (each wrapped tool is one entry, and the built-in toolset is one more). The API rejects a declaration that reuses a tool name, names a custom tool after a built-in agent tool such as `bash` or `read`, or uses the reserved `mcp__` prefix. The MCP helpers keep the server's names and descriptions, so rename or trim where needed. When two servers expose the same tool name, define the wrapper yourself under a prefixed name and have it call the server's original tool name.
* **Most schemas pass through unchanged.** The API accepts the JSON Schema keywords MCP servers commonly emit, such as `additionalProperties` and `title`. It rejects reference keywords such as `$ref` anywhere in a custom tool's `input_schema`, so inline the schemas that generators such as pydantic factor into `$defs`. It also rejects top-level `oneOf`, `anyOf`, and `allOf`, and property names outside letters, digits, underscores, dots, and hyphens (1–64 characters).
* **Tool failures surface as error tool results.** When the MCP server reports a tool error, the worker posts an error tool result the model can react to. MCP content with no tool result equivalent, such as audio blocks and resource links, also surfaces as an error. Set a timeout on the MCP client for a faster and clearer failure, as the Python worker example does with `read_timeout_seconds`. Without one, a hung call becomes an error result only when the TypeScript MCP SDK's default request timeout fires (about a minute) or when the worker's own backstop does: about two and a half minutes in Python, and two minutes in Go, where the worker cancels a tool call that outlives its 120-second default and posts an error result.
* **Wrap servers you operate or trust.** A wrapped tool's name, description, and results enter the model's context like any other tool's: untrusted input that can influence what the agent does with its other tools, including `bash` on the worker host. Declare only the tools you intend the agent to use.
* **Permission policies do not apply to custom tools.** [Permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies#custom-tools) govern the built-in and MCP toolsets; the worker executes every wrapped tool call the model makes, so put any approval step in your own tool code.

## Monitoring and operations

These calls run from your monitoring or operations tooling, authenticated with your Claude API key, to observe and manage the worker fleet. The claim and keep-alive loop is handled inside the worker helpers, so you don't call those endpoints directly.

<Warning>
  These endpoints accept either your organization API key or the environment key. Call them from outside the worker host with your organization API key. Setting `ANTHROPIC_API_KEY` on the worker host exposes an organization-scoped credential to agent tool calls.
</Warning>

### Read queue depth

`work.stats` returns the queue state for an environment:

* `depth` is the number of items waiting to be claimed. Scale your worker fleet or alert on backlog based on this value.
* `pending` is the number of items claimed by a worker but not yet acknowledged. The worker helpers acknowledge each item before processing it, so this value stays near zero in normal operation; a sustained non-zero value means a worker stalled between claiming and acknowledging.
* `oldest_queued_at` is the timestamp of the oldest item still in the queue, waiting to be claimed or claimed but not yet acknowledged, or `null` when there is none.
* `workers_polling` is the number of workers that have polled in the last 30 seconds. Use this for liveness alerting.

<CodeGroup>
  ```bash cURL
  curl -sS "https://api.anthropic.com/v1/environments/$ANTHROPIC_ENVIRONMENT_ID/work/stats" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:environments:work stats --environment-id "$ANTHROPIC_ENVIRONMENT_ID"
  ```

  ```python Python
  import os

  import anthropic

  client = anthropic.Anthropic()

  stats = client.beta.environments.work.stats(os.environ["ANTHROPIC_ENVIRONMENT_ID"])
  print(f"depth={stats.depth} pending={stats.pending}")
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const stats = await client.beta.environments.work.stats(process.env.ANTHROPIC_ENVIRONMENT_ID!);

  console.log(`depth=${stats.depth} pending=${stats.pending}`);
  ```

  ```csharp C#
  using Anthropic;

  var client = new AnthropicClient();

  var environmentId = Environment.GetEnvironmentVariable("ANTHROPIC_ENVIRONMENT_ID")!;

  var stats = await client.Beta.Environments.Work.Stats(environmentId);

  Console.WriteLine($"depth={stats.Depth} pending={stats.Pending}");
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func main() {
  	client := anthropic.NewClient()
  	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")

  	stats, err := client.Beta.Environments.Work.Stats(
  		context.Background(),
  		environmentID,
  		anthropic.BetaEnvironmentWorkStatsParams{},
  	)
  	if err != nil {
  		panic(err)
  	}

  	fmt.Printf("depth=%d pending=%d\n", stats.Depth, stats.Pending)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.beta.environments.work.BetaSelfHostedWorkQueueStats;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      BetaSelfHostedWorkQueueStats stats = client.beta()
          .environments()
          .work()
          .stats(System.getenv("ANTHROPIC_ENVIRONMENT_ID"));

      IO.println("depth=" + stats.depth() + " pending=" + stats.pending());
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Client;

  $client = new Client();

  $stats = $client->beta->environments->work->stats(getenv('ANTHROPIC_ENVIRONMENT_ID'));

  printf("depth=%d pending=%d\n", $stats->depth, $stats->pending);
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  stats = client.beta.environments.work.stats(ENV.fetch("ANTHROPIC_ENVIRONMENT_ID"))

  puts "depth=#{stats.depth} pending=#{stats.pending}"
  ```
</CodeGroup>

```text wrap
{
  "type": "work_queue_stats",
  "depth": 0,
  "pending": 0,
  "oldest_queued_at": null,
  "workers_polling": 0
}
```

### Stop a session gracefully

Use `work.stop` to ask the worker handling a specific session to shut it down. By default the work item moves to `stopping`: the worker notices on its next lease heartbeat, cancels the session's in-flight tool call, and confirms the shutdown, at which point the work item becomes `stopped`. Pass `force: true` in the request body (with the CLI, pass `--force`) to mark the work item `stopped` immediately instead of waiting for the worker's confirmation.

Because these calls run from your operations tooling rather than the worker host, `ANTHROPIC_WORK_ID` isn't set automatically. Set it to the target work item's ID before running the following examples. To find a work item's ID, list the environment's work items through the [Environments Work endpoints](https://platform.claude.com/docs/en/api/beta/environments/work).

<CodeGroup>
  ```bash cURL
  curl -sS "https://api.anthropic.com/v1/environments/$ANTHROPIC_ENVIRONMENT_ID/work/$ANTHROPIC_WORK_ID/stop" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{}'
  ```

  ```bash CLI
  ant beta:environments:work stop \
    --environment-id "$ANTHROPIC_ENVIRONMENT_ID" \
    --work-id "$ANTHROPIC_WORK_ID"
  ```

  ```python Python
  import os

  import anthropic

  client = anthropic.Anthropic()

  work = client.beta.environments.work.stop(
      os.environ["ANTHROPIC_WORK_ID"],
      environment_id=os.environ["ANTHROPIC_ENVIRONMENT_ID"],
  )
  print(work.state)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic();

  const work = await client.beta.environments.work.stop(process.env.ANTHROPIC_WORK_ID!, {
    environment_id: process.env.ANTHROPIC_ENVIRONMENT_ID!
  });

  console.log(work.state);
  ```

  ```csharp C#
  using Anthropic;

  var client = new AnthropicClient();

  var work = await client.Beta.Environments.Work.Stop(
      Environment.GetEnvironmentVariable("ANTHROPIC_WORK_ID")!,
      new()
      {
          EnvironmentID = Environment.GetEnvironmentVariable("ANTHROPIC_ENVIRONMENT_ID")!
      }
  );

  Console.WriteLine(work.State);
  ```

  ```go Go
  package main

  import (
  	"context"
  	"fmt"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  func main() {
  	client := anthropic.NewClient()

  	work, err := client.Beta.Environments.Work.Stop(
  		context.Background(),
  		os.Getenv("ANTHROPIC_WORK_ID"),
  		anthropic.BetaEnvironmentWorkStopParams{
  			EnvironmentID: os.Getenv("ANTHROPIC_ENVIRONMENT_ID"),
  		},
  	)
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(work.State)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.beta.environments.work.BetaSelfHostedWork;
  import com.anthropic.models.beta.environments.work.BetaSelfHostedWorkStopRequest;
  import com.anthropic.models.beta.environments.work.WorkStopParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      BetaSelfHostedWork work = client.beta().environments().work().stop(
          WorkStopParams.builder()
              .environmentId(System.getenv("ANTHROPIC_ENVIRONMENT_ID"))
              .workId(System.getenv("ANTHROPIC_WORK_ID"))
              .betaSelfHostedWorkStopRequest(BetaSelfHostedWorkStopRequest.builder().build())
              .build()
      );

      IO.println(work.state());
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Client;

  $client = new Client();

  $work = $client->beta->environments->work->stop(
      getenv('ANTHROPIC_WORK_ID'),
      environmentID: getenv('ANTHROPIC_ENVIRONMENT_ID'),
  );

  echo $work->state . "\n";
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::Client.new

  work = client.beta.environments.work.stop(
    ENV.fetch("ANTHROPIC_WORK_ID"),
    environment_id: ENV.fetch("ANTHROPIC_ENVIRONMENT_ID")
  )

  puts work.state
  ```
</CodeGroup>

## Next steps

<CardGroup cols={2}>
  <Card title="Security model" icon="lock" href="https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security">
    Shared responsibility model for self-hosted sandbox environments.
  </Card>

  <Card title="Start a session" icon="settings" href="https://platform.claude.com/docs/en/managed-agents/sessions">
    Create a session to run your agent and begin executing tasks.
  </Card>

  <Card title="MCP tunnels" icon="bolt" href="https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview">
    Securely connect Claude to MCP servers running in your private network without opening inbound ports or exposing services to the public internet.
  </Card>
</CardGroup>
