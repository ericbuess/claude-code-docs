# Subscribe to webhooks

Get notified when major events happen without polling.

---

Sessions are long-running interactions. While most real-time interactions happen through the [SSE event stream](/docs/en/managed-agents/events-and-streaming), webhooks notify you of major state changes.

Webhook events return the event `type` and `id`, not the full object. When you receive a webhook event, you need to fetch the object directly with a `GET` call. This avoids delivering stale data on retries and keeps every delivery small.

## Supported event types

<Tabs>
  <Tab title="Session events">
    | Event                              | Trigger                                                                                                                                          |
    | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
    | `session.status_run_started`       | Agent execution kicked off. This triggers at every session status transition to `running`.                                                       |
    | `session.status_idled`             | Agent awaiting input, for example a tool permission approval or a new user message.                                                              |
    | `session.status_rescheduled`       | A transient error occurred and the session is retrying automatically.                                                                            |
    | `session.status_terminated`        | The session hit a terminal error.                                                                                                                |
    | `session.thread_created`           | New [multi-agent thread](/docs/en/managed-agents/multi-agent) opened, meaning an additional agent called by the coordinator is kicking off work. |
    | `session.thread_idled`             | An agent in a [multi-agent interaction](/docs/en/managed-agents/multi-agent) is waiting for input.                                               |
    | `session.thread_terminated`        | A [multi-agent thread](/docs/en/managed-agents/multi-agent) was archived.                                                                        |
    | `session.outcome_evaluation_ended` | [Outcome evaluation](/docs/en/managed-agents/define-outcomes) for a single iteration completed.                                                  |
    | `session.updated`                  | Session properties changed (for example, its name or configuration was updated).                                                                 |
    | `session.deleted`                  | Session permanently deleted. There is no object left to fetch, so treat the event itself as final.                                               |
  </Tab>

  <Tab title="Vault events">
    | Event                             | Trigger                                                                                                              |
    | --------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
    | `vault.created`                   | Vault created.                                                                                                       |
    | `vault.archived`                  | Vault archived. A `vault_credential.archived` event is also emitted for each underlying credential.                  |
    | `vault.deleted`                   | Vault deleted. A `vault_credential.deleted` event is also emitted for each underlying credential.                    |
    | `vault_credential.created`        | Credential created.                                                                                                  |
    | `vault_credential.archived`       | Credential archived, either directly or as a result of vault archival.                                               |
    | `vault_credential.deleted`        | Credential deleted, either directly or as a result of vault deletion.                                                |
    | `vault_credential.refresh_failed` | An `mcp_oauth` credential cannot be refreshed (invalid refresh token, or irrecoverable error from the OAuth server). |
  </Tab>

  <Tab title="Agent events">
    These events track the lifecycle of the agent resources in your workspace, and are distinct from the agent events delivered on a session's event stream.

    | Event            | Trigger                                                                                                                                                              |
    | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `agent.created`  | Agent created.                                                                                                                                                       |
    | `agent.updated`  | A [new version of the agent](/docs/en/managed-agents/agent-setup#update-an-agent) was published. Updates that do not create a new version do not trigger this event. |
    | `agent.archived` | Agent archived.                                                                                                                                                      |
    | `agent.deleted`  | Agent permanently deleted. There is no object left to fetch, so treat the event itself as final.                                                                     |
  </Tab>

  <Tab title="Deployment events">
    | Event                 | Trigger                                                                                                                                                                                                                                                                                                                                 |
    | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `deployment.created`  | [Scheduled deployment](/docs/en/managed-agents/scheduled-deployments) created.                                                                                                                                                                                                                                                          |
    | `deployment.updated`  | Deployment properties changed (for example, its schedule was updated).                                                                                                                                                                                                                                                                  |
    | `deployment.paused`   | Deployment paused, either by request or automatically when a scheduled run fails with an unrecoverable error, such as an archived subagent or an archived environment. Recoverable failures, including rate limits, don't pause the deployment. See [Failure behavior](/docs/en/managed-agents/scheduled-deployments#failure-behavior). |
    | `deployment.unpaused` | Deployment unpaused, resuming its schedule.                                                                                                                                                                                                                                                                                             |
    | `deployment.archived` | Deployment archived, either directly or as a result of agent archival or deletion.                                                                                                                                                                                                                                                      |
    | `deployment.deleted`  | Deployment permanently deleted. There is no object left to fetch, so treat the event itself as final.                                                                                                                                                                                                                                   |
  </Tab>

  <Tab title="Deployment run events">
    | Event                      | Trigger                                                                                                                                                                                                                                                                                                                                        |
    | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `deployment_run.started`   | A scheduled run started. Only scheduled runs emit `deployment_run` events; [manual runs](/docs/en/managed-agents/scheduled-deployments#trigger-a-manual-run) do not.                                                                                                                                                                           |
    | `deployment_run.succeeded` | A scheduled run created its session. The event carries the same `data.id` (the run ID) as the run's `deployment_run.started` event. To follow the session's work, subscribe to its session events (the Session events tab), or fetch the [deployment run](/docs/en/managed-agents/scheduled-deployments#deployment-runs) for its `session_id`. |
    | `deployment_run.failed`    | A scheduled run did not create a session. The event carries the same `data.id` as the run's `deployment_run.started` event. Fetch the [deployment run](/docs/en/managed-agents/scheduled-deployments#deployment-runs) for the error details.                                                                                                   |
  </Tab>
</Tabs>

## Register an endpoint

Visit **Manage > Webhooks** in [Console](https://platform.claude.com/settings/workspaces/default/webhooks).

A webhook endpoint consists of:

* **URL:** Must be HTTPS on port 443 with a publicly resolvable hostname.
* **Event types:** The list of `data.type` values this endpoint receives. An endpoint only receives events it's subscribed to, plus test events (see [Delivery behavior](#delivery-behavior)).
* **Signing secret:** A 32-byte `whsec_`-prefixed secret generated at creation. It's shown only once, so store it securely to verify webhook deliveries.

## Verify the signature

Every delivery carries an `X-Webhook-Signature` header. Use the SDK's `unwrap()` helper to verify the signature and parse the event in one step. It throws if the signature is invalid or the payload is more than five minutes old.

Set `ANTHROPIC_WEBHOOK_SIGNING_KEY` to the `whsec_`-prefixed secret shown at endpoint creation.

<CodeGroup>
  ```python Python
  from flask import Flask, request
  import anthropic

  client = anthropic.Anthropic()  # reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env
  app = Flask(__name__)


  @app.route("/webhook", methods=["POST"])
  def webhook():
      try:
          # unwrap() raises if the signature is invalid or the payload is stale
          event = client.beta.webhooks.unwrap(
              request.get_data(as_text=True),
              headers=dict(request.headers),
          )
      except Exception:
          return "invalid signature", 400

      if event.data.type == "session.status_idled":
          print("session idled:", event.data.id)
      # handle other event types

      return "", 200
  ```

  ```typescript TypeScript
  import express from "express";
  import Anthropic from "@anthropic-ai/sdk";

  const client = new Anthropic(); // reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env
  const app = express();

  // IMPORTANT: use express.raw(), not express.json(). The signature is computed over raw bytes.
  app.post("/webhook", express.raw({ type: "application/json" }), (req, res) => {
    let event;
    try {
      // unwrap() throws if the signature is invalid or the payload is stale
      event = client.beta.webhooks.unwrap(req.body.toString("utf8"), {
        headers: req.headers as Record<string, string>
      });
    } catch {
      return res.status(400).send("invalid signature");
    }

    switch (event.data.type) {
      case "session.status_idled":
        console.log("session idled:", event.data.id);
        break;
      // handle other event types
    }

    res.sendStatus(200);
  });
  ```

  ```csharp C#
  using Anthropic;

  var client = new AnthropicClient(); // reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env
  var app = WebApplication.Create(args);

  app.MapPost("/webhook", async (HttpRequest request) =>
  {
      using var reader = new StreamReader(request.Body);
      var body = await reader.ReadToEndAsync();
      var headers = request.Headers.ToDictionary(header => header.Key, header => header.Value.ToString());

      UnwrapWebhookEvent webhookEvent;
      try
      {
          // Unwrap() throws if the signature is invalid or the payload is stale
          webhookEvent = client.Beta.Webhooks.Unwrap(body, headers);
      }
      catch
      {
          return Results.BadRequest("invalid signature");
      }

      if (webhookEvent.Data.TryPickSessionStatusIdled(out var idled))
      {
          Console.WriteLine($"session idled: {idled.ID}");
      }
      // handle other event types

      return Results.Ok();
  });
  ```

  ```go Go
  package main

  import (
  	"fmt"
  	"io"
  	"net/http"

  	"github.com/anthropics/anthropic-sdk-go"
  )

  var client = anthropic.NewClient() // reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env

  func webhook(w http.ResponseWriter, r *http.Request) {
  	body, err := io.ReadAll(r.Body)
  	if err != nil {
  		http.Error(w, "could not read body", http.StatusBadRequest)
  		return
  	}

  	// Unwrap returns an error if the signature is invalid or the payload is stale
  	event, err := client.Beta.Webhooks.Unwrap(body, r.Header)
  	if err != nil {
  		http.Error(w, "invalid signature", http.StatusBadRequest)
  		return
  	}

  	switch event.Data.Type {
  	case "session.status_idled":
  		fmt.Println("session idled:", event.Data.ID)
  		// handle other event types
  	}

  	w.WriteHeader(http.StatusOK)
  }

  func main() {
  	http.HandleFunc("/webhook", webhook)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.UnwrapWebhookParams;
  import com.anthropic.core.http.Headers;
  import com.sun.net.httpserver.HttpServer;

  // reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  void main() throws Exception {
      var server = HttpServer.create(new InetSocketAddress(8000), 0);
      server.createContext("/webhook", exchange -> {
          var body = new String(exchange.getRequestBody().readAllBytes());
          var headers = Headers.builder();
          exchange.getRequestHeaders().forEach(headers::put);

          try {
              // unwrap() throws if the signature is invalid or the payload is stale
              var event = client.beta().webhooks().unwrap(
                  UnwrapWebhookParams.builder()
                      .body(body)
                      .headers(headers.build())
                      .build());

              event.data().sessionStatusIdled().ifPresent(idled ->
                  IO.println("session idled: " + idled.id()));
              // handle other event types

              exchange.sendResponseHeaders(200, -1);
          } catch (Exception _) {
              exchange.sendResponseHeaders(400, -1);
          }
          exchange.close();
      });
  }
  ```

  ```php PHP
  use Anthropic\Client;
  use Anthropic\Core\Exceptions\WebhookException;

  $client = new Client(); // reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env

  $body = file_get_contents('php://input');
  $headers = getallheaders();

  try {
      // unwrap() throws if the signature is invalid or the payload is stale
      $event = $client->beta->webhooks->unwrap($body, headers: $headers);
  } catch (WebhookException) {
      http_response_code(400);
      exit('invalid signature');
  }

  match ($event->data->type) {
      'session.status_idled' => print "session idled: {$event->data->id}\n",
      // handle other event types
      default => null,
  };

  http_response_code(200);
  ```

  ```ruby Ruby
  require "sinatra"
  require "anthropic"

  client = Anthropic::Client.new # reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env

  post "/webhook" do
    headers = request.env
      .select { |key, _| key.start_with?("HTTP_") }
      .transform_keys { it.delete_prefix("HTTP_").downcase.tr("_", "-") }

    begin
      # unwrap raises if the signature is invalid or the payload is stale
      event = client.beta.webhooks.unwrap(request.body.read, headers: headers)
    rescue StandardError
      halt 400, "invalid signature"
    end

    if event.data.type == "session.status_idled"
      puts "session idled: #{event.data.id}"
    end
    # handle other event types

    status 200
  end
  ```
</CodeGroup>

## Handle an event

Parse the body, switch on `data.type`, and fetch the resource by ID. Return any `2xx` to acknowledge. Anything else (including `3xx`) counts as a failure and triggers a retry.

Every event payload has the same structure, including the event type, identifier, and timestamp of when the object was created.

```json
{
  "type": "event",
  "id": "event_01ABC...",
  "created_at": "2026-03-18T14:05:22Z",
  "data": {
    "type": "session.status_idled",
    "id": "sesn_01XYZ...",
    "organization_id": "8a3d2f1e-...",
    "workspace_id": "c7b0e4d9-..."
  }
}
```

<CodeGroup>
  ```python Python
  if event.data.type == "session.status_idled":
      session = client.beta.sessions.retrieve(event.data.id)
      notify_user(session)
  return "", 204
  ```

  ```typescript TypeScript
  if (event.data.type === "session.status_idled") {
    const session = await client.beta.sessions.retrieve(event.data.id);
    notifyUser(session);
  }
  res.sendStatus(204);
  ```

  ```csharp C#
  if (webhookEvent.Data.TryPickSessionStatusIdled(out var idled))
  {
      var session = await client.Beta.Sessions.Retrieve(idled.ID);
      NotifyUser(session);
  }
  return Results.StatusCode(204);
  ```

  ```go Go
  if event.Data.Type == "session.status_idled" {
  	session, err := client.Beta.Sessions.Get(r.Context(), event.Data.ID, anthropic.BetaSessionGetParams{})
  	if err != nil {
  		panic(err)
  	}
  	notifyUser(session)
  }
  w.WriteHeader(http.StatusNoContent)
  ```

  ```java Java
  event.data().sessionStatusIdled().ifPresent(idled -> {
      var session = client.beta().sessions().retrieve(idled.id());
      notifyUser(session);
  });
  exchange.sendResponseHeaders(204, -1);
  ```

  ```php PHP
  if ($event->data->type === 'session.status_idled') {
      $session = $client->beta->sessions->retrieve($event->data->id);
      notifyUser($session);
  }
  http_response_code(204);
  ```

  ```ruby Ruby
  if event.data.type == "session.status_idled"
    session = client.beta.sessions.retrieve(event.data.id)
    notify_user(session)
  end
  status 204
  ```
</CodeGroup>

The top-level `event.id` is unique per event, not per delivery. If you receive the same `event.id` twice, it's a retry and you can discard it.

## Delivery behavior

* **Ordering is not guaranteed.** `session.status_idled` may arrive before `session.outcome_evaluation_ended` even if the outcome was produced first. Use the `created_at` timestamp to sort if ordering matters.
* **Retries:** Anthropic retries at least once. The retry delivers the same `event.id`.
* **Redirects are not followed.** A `3xx` is treated as a failure. If your endpoint moves, update the URL in Console.
* **Auto-disable:** An endpoint is automatically set to `disabled` with a machine-readable `disabled_reason` after roughly 20 consecutive failed deliveries, or immediately if the hostname resolves to a private IP or the endpoint returns a redirect. Re-enable manually in Console after resolving the issue.
