# Session event stream

Send events, stream responses, and interrupt or redirect your session mid-execution.

---

Communication with Claude Managed Agents is event-based. You send user events to the agent, and receive agent and session events back to track status.

<Note>
  Managed Agents API requests require the `managed-agents-2026-04-01` beta header, except memory store endpoints, which use `agent-memory-2026-07-22` instead. The SDK sets the correct beta header automatically. See [Beta headers](/docs/en/api/beta-headers#endpoint-specific-headers).
</Note>

## Event types

Events flow in two directions.

* **User events** and **system events** are what you send to the agent: `user.*` events kick off a session and steer it as it progresses; `system.message` updates the agent's system prompt between turns.
* **Session events**, **span events**, and **agent events** are sent to you for observability into your session state and agent progress. Stream connections that opt in also receive [event deltas](#event-deltas).

Session, span, agent, user, and system event type strings follow a `{domain}.{action}` naming convention. The stream-only delta preview events (`event_start`, `event_delta`) are the exception. See [Event types](/docs/en/managed-agents/reference#event-types) in the reference for the full catalog.

Every persisted event includes a `processed_at` timestamp indicating when the event was recorded server-side. If `processed_at` is null, it means the event has been queued by the harness and is handled after preceding events finish processing.

## Integrating events

<Tabs>
  <Tab title="Sending events">
    Send a `user.message` event to start or continue the agent's work:

    <CodeGroup>
      ```bash curl
      curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        -d @- <<'EOF'
      {
        "events": [
          {
            "type": "user.message",
            "content": [
              {"type": "text", "text": "Analyze the performance of the sort function in utils.py"}
            ]
          }
        ]
      }
      EOF
      ```

      ```bash CLI
      ant beta:sessions:events send --session-id "$SESSION_ID" <<'YAML'
      events:
        - type: user.message
          content:
            - type: text
              text: Analyze the performance of the sort function in utils.py
      YAML
      ```

      ```python Python
      client.beta.sessions.events.send(
          session.id,
          events=[
              {
                  "type": "user.message",
                  "content": [
                      {
                          "type": "text",
                          "text": "Analyze the performance of the sort function in utils.py",
                      },
                  ],
              },
          ],
      )
      ```

      ```typescript TypeScript
      await client.beta.sessions.events.send(session.id, {
        events: [
          {
            type: "user.message",
            content: [
              {
                type: "text",
                text: "Analyze the performance of the sort function in utils.py",
              },
            ],
          },
        ],
      });
      ```

      ```csharp C#
      await client.Beta.Sessions.Events.Send(session.ID, new()
      {
          Events =
          [
              new BetaManagedAgentsUserMessageEventParams
              {
                  Type = BetaManagedAgentsUserMessageEventParamsType.UserMessage,
                  Content =
                  [
                      new BetaManagedAgentsTextBlock
                      {
                          Type = BetaManagedAgentsTextBlockType.Text,
                          Text = "Analyze the performance of the sort function in utils.py",
                      },
                  ],
              },
          ],
      });
      ```

      ```go Go
      if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
      	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
      		OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
      			Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
      			Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
      				OfText: &anthropic.BetaManagedAgentsTextBlockParam{
      					Type: anthropic.BetaManagedAgentsTextBlockTypeText,
      					Text: "Analyze the performance of the sort function in utils.py",
      				},
      			}},
      		},
      	}},
      }); err != nil {
      	panic(err)
      }
      ```

      ```java Java
      client.beta().sessions().events().send(
          session.id(),
          EventSendParams.builder()
              .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
                  .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
                  .addTextContent("Analyze the performance of the sort function in utils.py")
                  .build())
              .build());
      ```

      ```php PHP
      $client->beta->sessions->events->send(
          $session->id,
          events: [
              [
                  'type' => 'user.message',
                  'content' => [
                      [
                          'type' => 'text',
                          'text' => 'Analyze the performance of the sort function in utils.py',
                      ],
                  ],
              ],
          ],
      );
      ```

      ```ruby Ruby
      client.beta.sessions.events.send_(
        session.id,
        events: [
          {
            type: "user.message",
            content: [
              {
                type: "text",
                text: "Analyze the performance of the sort function in utils.py"
              }
            ]
          }
        ]
      )
      ```
    </CodeGroup>

    Send a `user.interrupt` event to stop the agent mid-execution, then follow up with a `user.message` event to redirect it:

    <CodeGroup>
      ```bash curl
      # Agent is currently analyzing a file...
      # Interrupt with a new direction:
      curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        -d @- <<'EOF'
      {
        "events": [
          {"type": "user.interrupt"},
          {
            "type": "user.message",
            "content": [
              {"type": "text", "text": "Instead, focus on fixing the bug in line 42."}
            ]
          }
        ]
      }
      EOF
      ```

      ```bash CLI
      # Agent is currently analyzing a file...
      # Interrupt with a new direction:
      ant beta:sessions:events send --session-id "$SESSION_ID" <<'YAML'
      events:
        - type: user.interrupt
        - type: user.message
          content:
            - type: text
              text: Instead, focus on fixing the bug in line 42.
      YAML
      ```

      ```python Python
      # Agent is currently analyzing a file...
      # Interrupt with a new direction:
      client.beta.sessions.events.send(
          session.id,
          events=[
              {"type": "user.interrupt"},
              {
                  "type": "user.message",
                  "content": [
                      {
                          "type": "text",
                          "text": "Instead, focus on fixing the bug in line 42.",
                      },
                  ],
              },
          ],
      )
      ```

      ```typescript TypeScript
      // Agent is currently analyzing a file...
      // Interrupt with a new direction:
      await client.beta.sessions.events.send(session.id, {
        events: [
          { type: "user.interrupt" },
          {
            type: "user.message",
            content: [
              {
                type: "text",
                text: "Instead, focus on fixing the bug in line 42.",
              },
            ],
          },
        ],
      });
      ```

      ```csharp C#
      // Agent is currently analyzing a file...
      // Interrupt with a new direction:
      await client.Beta.Sessions.Events.Send(session.ID, new()
      {
          Events =
          [
              new BetaManagedAgentsUserInterruptEventParams
              {
                  Type = BetaManagedAgentsUserInterruptEventParamsType.UserInterrupt,
              },
              new BetaManagedAgentsUserMessageEventParams
              {
                  Type = BetaManagedAgentsUserMessageEventParamsType.UserMessage,
                  Content =
                  [
                      new BetaManagedAgentsTextBlock
                      {
                          Type = BetaManagedAgentsTextBlockType.Text,
                          Text = "Instead, focus on fixing the bug in line 42.",
                      },
                  ],
              },
          ],
      });
      ```

      ```go Go
      // Agent is currently analyzing a file...
      // Interrupt with a new direction:
      if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
      	Events: []anthropic.BetaManagedAgentsEventParamsUnion{
      		{
      			OfUserInterrupt: &anthropic.BetaManagedAgentsUserInterruptEventParams{
      				Type: anthropic.BetaManagedAgentsUserInterruptEventParamsTypeUserInterrupt,
      			},
      		},
      		{
      			OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
      				Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
      				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
      					OfText: &anthropic.BetaManagedAgentsTextBlockParam{
      						Type: anthropic.BetaManagedAgentsTextBlockTypeText,
      						Text: "Instead, focus on fixing the bug in line 42.",
      					},
      				}},
      			},
      		},
      	},
      }); err != nil {
      	panic(err)
      }
      ```

      ```java Java
      // Agent is currently analyzing a file...
      // Interrupt with a new direction:
      client.beta().sessions().events().send(
          session.id(),
          EventSendParams.builder()
              .addEvent(BetaManagedAgentsUserInterruptEventParams.builder()
                  .type(BetaManagedAgentsUserInterruptEventParams.Type.USER_INTERRUPT)
                  .build())
              .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
                  .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
                  .addTextContent("Instead, focus on fixing the bug in line 42.")
                  .build())
              .build());
      ```

      ```php PHP
      // Agent is currently analyzing a file...
      // Interrupt with a new direction:
      $client->beta->sessions->events->send(
          $session->id,
          events: [
              ['type' => 'user.interrupt'],
              [
                  'type' => 'user.message',
                  'content' => [
                      [
                          'type' => 'text',
                          'text' => 'Instead, focus on fixing the bug in line 42.',
                      ],
                  ],
              ],
          ],
      );
      ```

      ```ruby Ruby
      # Agent is currently analyzing a file...
      # Interrupt with a new direction:
      client.beta.sessions.events.send_(
        session.id,
        events: [
          {type: "user.interrupt"},
          {
            type: "user.message",
            content: [
              {type: "text", text: "Instead, focus on fixing the bug in line 42."}
            ]
          }
        ]
      )
      ```
    </CodeGroup>

    The agent acknowledges the interruption and switches to the new task.
  </Tab>

  <Tab title="Streaming events">
    Stream events from the session to receive real-time updates as the agent works. Only events emitted after the stream is opened are delivered, so open the stream before sending events to avoid a race condition.

    <CodeGroup>
      ```bash curl
      # Open the stream first, then send the user message
      exec {stream}< <(
        curl --fail-with-body -sS -N \
          "https://api.anthropic.com/v1/sessions/$SESSION_ID/events/stream?beta=true" \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2023-06-01" \
          -H "anthropic-beta: managed-agents-2026-04-01" \
          -H "content-type: application/json" \
          -H "accept: text/event-stream"
      )

      curl --fail-with-body -sS \
        "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        -d @- >/dev/null <<'EOF'
      {
        "events": [
          {
            "type": "user.message",
            "content": [{"type": "text", "text": "Summarize the repo README"}]
          }
        ]
      }
      EOF

      while IFS= read -r -u "$stream" event_line; do
        [[ $event_line == data:* ]] || continue
        event_json=${event_line#data: }
        case $(jq -r '.type' <<<"$event_json") in
          agent.message)
            jq -j '.content[] | select(.type == "text") | .text' <<<"$event_json"
            ;;
          session.status_idle)
            break
            ;;
          session.error)
            printf '\n[Error: %s]\n' "$(jq -r '.error.message // "unknown"' <<<"$event_json")"
            break
            ;;
        esac
      done
      exec {stream}<&-
      ```

      ```bash CLI
      # This workflow does not translate well to a one-off shell command.
      # Use one of the SDK examples in this code group instead.
      ```

      ```python Python
      # Open the stream first, then send the user message
      with client.beta.sessions.events.stream(session.id) as stream:
          client.beta.sessions.events.send(
              session.id,
              events=[
                  {
                      "type": "user.message",
                      "content": [{"type": "text", "text": "Summarize the repo README"}],
                  },
              ],
          )

          for event in stream:
              match event.type:
                  case "agent.message":
                      for block in event.content:
                          if block.type == "text":
                              print(block.text, end="")
                  case "session.status_idle":
                      break
                  case "session.error":
                      error_message = event.error.message if event.error else "unknown"
                      print(f"\n[Error: {error_message}]")
                      break
      ```

      ```typescript TypeScript
      // Open the stream first, then send the user message
      const stream = await client.beta.sessions.events.stream(session.id);
      await client.beta.sessions.events.send(session.id, {
        events: [
          {
            type: "user.message",
            content: [{ type: "text", text: "Summarize the repo README" }]
          }
        ]
      });

      for await (const event of stream) {
        if (event.type === "agent.message") {
          for (const block of event.content) {
            if (block.type === "text") {
              process.stdout.write(block.text);
            }
          }
        } else if (event.type === "session.status_idle") {
          break;
        } else if (event.type === "session.error") {
          console.log(`\n[Error: ${event.error?.message ?? "unknown"}]`);
          break;
        }
      }
      ```

      ```csharp C#
      // Open the stream first, then send the user message
      using var stream = await client.Beta.Sessions.Events.WithRawResponse.StreamStreaming(session.ID);
      await client.Beta.Sessions.Events.Send(session.ID, new()
      {
          Events =
          [
              new BetaManagedAgentsUserMessageEventParams
              {
                  Type = BetaManagedAgentsUserMessageEventParamsType.UserMessage,
                  Content =
                  [
                      new BetaManagedAgentsTextBlock
                      {
                          Type = BetaManagedAgentsTextBlockType.Text,
                          Text = "Summarize the repo README",
                      },
                  ],
              },
          ],
      });

      await foreach (var streamEvent in stream.Enumerate())
      {
          if (streamEvent.Value is BetaManagedAgentsAgentMessageEvent message)
          {
              foreach (var block in message.Content)
              {
                  Console.Write(block.Text);
              }
          }
          else if (streamEvent.Value is BetaManagedAgentsSessionStatusIdleEvent)
          {
              break;
          }
          else if (streamEvent.Value is BetaManagedAgentsSessionErrorEvent error)
          {
              Console.WriteLine($"\n[Error: {error.Error?.Message ?? "unknown"}]");
              break;
          }
      }
      ```

      ```go Go
      	// Open the stream first, then send the user message
      	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
      	defer stream.Close()

      	if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
      		Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
      			OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
      				Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
      				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
      					OfText: &anthropic.BetaManagedAgentsTextBlockParam{
      						Type: anthropic.BetaManagedAgentsTextBlockTypeText,
      						Text: "Summarize the repo README",
      					},
      				}},
      			},
      		}},
      	}); err != nil {
      		panic(err)
      	}

      events:
      	for stream.Next() {
      		switch event := stream.Current().AsAny().(type) {
      		case anthropic.BetaManagedAgentsAgentMessageEvent:
      			// concrete-typed list: BetaManagedAgentsTextBlock
      			for _, block := range event.Content {
      				fmt.Print(block.Text)
      			}
      		case anthropic.BetaManagedAgentsSessionStatusIdleEvent:
      			break events
      		case anthropic.BetaManagedAgentsSessionErrorEvent:
      			fmt.Printf("\n[Error: %s]\n", cmp.Or(event.Error.Message, "unknown"))
      			break events
      		}
      	}
      	if err := stream.Err(); err != nil {
      		panic(err)
      	}
      ```

      ```java Java
      // Open the stream first, then send the user message
      try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
          client.beta().sessions().events().send(
              session.id(),
              EventSendParams.builder()
                  .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
                      .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
                      .addTextContent("Summarize the repo README")
                      .build())
                  .build()
          );

          Iterable<BetaManagedAgentsStreamSessionEvents> events = stream.stream()::iterator;
          for (var event : events) {
              if (event.isAgentMessage()) {
                  event.asAgentMessage().content().forEach(block -> IO.print(block.text()));
              } else if (event.isSessionStatusIdle()) {
                  break;
              } else if (event.isSessionError()) {
                  // The `message` field spans all error variants; read it from the raw JSON.
                  var errorMessage =
                      event.asSessionError().error()._json().orElse(null) instanceof JsonObject json
                          ? json.values().get("message").asStringOrThrow()
                          : "unknown";
                  IO.println("\n[Error: " + errorMessage + "]");
                  break;
              }
          }
      }
      ```

      ```php PHP
      // Open the stream first, then send the user message
      $stream = $client->beta->sessions->events->streamStream($session->id);
      $client->beta->sessions->events->send(
          $session->id,
          events: [
              [
                  'type' => 'user.message',
                  'content' => [['type' => 'text', 'text' => 'Summarize the repo README']],
              ],
          ],
      );

      foreach ($stream as $event) {
          match ($event->type) {
              'agent.message' => array_walk(
                  $event->content,
                  static fn ($block) => $block->type === 'text' ? print($block->text) : null,
              ),
              'session.error' => printf("\n[Error: %s]", $event->error?->message ?? 'unknown'),
              default => null,
          };
          if ($event->type === 'session.status_idle' || $event->type === 'session.error') {
              break;
          }
      }
      $stream->close();
      ```

      ```ruby Ruby
      # Open the stream first, then send the user message
      stream = client.beta.sessions.events.stream_events(session.id)

      client.beta.sessions.events.send_(
        session.id,
        events: [{
          type: "user.message",
          content: [{type: "text", text: "Summarize the repo README"}]
        }]
      )

      stream.each do |event|
        case event.type
        in :"agent.message"
          event.content.each { print it.text }
        in :"session.status_idle"
          break
        in :"session.error"
          puts "\n[Error: #{event.error&.message || "unknown"}]"
          break
        else
          # ignore other event types
        end
      end
      ```
    </CodeGroup>

    To reconnect to an existing session without missing events:

    1. Open a new stream.
    2. List the full event history to seed a set of seen event IDs.
    3. Tail the live stream, skipping any events already returned by the history list.

    <CodeGroup>
      ```bash curl
      exec {stream}< <(
        curl --fail-with-body -sS -N \
          "https://api.anthropic.com/v1/sessions/$SESSION_ID/events/stream?beta=true" \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2023-06-01" \
          -H "anthropic-beta: managed-agents-2026-04-01" \
          -H "content-type: application/json" \
          -H "accept: text/event-stream"
      )

      # Stream is open and buffering. List history before tailing live.
      declare -A seen_event_ids
      while IFS= read -r event_id; do
        seen_event_ids[$event_id]=1
      done < <(
        curl --fail-with-body -sS \
          "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
          -H "x-api-key: $ANTHROPIC_API_KEY" \
          -H "anthropic-version: 2023-06-01" \
          -H "anthropic-beta: managed-agents-2026-04-01" \
          -H "content-type: application/json" | jq -r '.data[].id'
      )

      # Tail live events, skipping anything already seen
      while IFS= read -r -u "$stream" event_line; do
        [[ $event_line == data:* ]] || continue
        event_json=${event_line#data: }
        event_id=$(jq -r '.id' <<<"$event_json")
        [[ -n ${seen_event_ids[$event_id]+seen} ]] && continue
        seen_event_ids[$event_id]=1
        case $(jq -r '.type' <<<"$event_json") in
          agent.message)
            jq -j '.content[] | select(.type == "text") | .text' <<<"$event_json"
            ;;
          session.status_idle)
            break
            ;;
        esac
      done
      exec {stream}<&-
      ```

      ```bash CLI
      # This workflow does not translate well to a one-off shell command.
      # Use one of the SDK examples in this code group instead.
      ```

      ```python Python
      with client.beta.sessions.events.stream(session.id) as stream:
          # Stream is open and buffering. List history before tailing live.
          history = client.beta.sessions.events.list(session.id)
          seen_event_ids = {past_event.id for past_event in history}

          # Tail live events, skipping anything already seen
          for event in stream:
              if event.type == "event_start" or event.type == "event_delta":
                  # Delta previews aren't enabled on this connection.
                  continue
              if event.id in seen_event_ids:
                  continue
              seen_event_ids.add(event.id)
              match event.type:
                  case "agent.message":
                      for block in event.content:
                          if block.type == "text":
                              print(block.text, end="")
                  case "session.status_idle":
                      break
      ```

      ```typescript TypeScript
      const seenEventIds = new Set<string>();
      const stream = await client.beta.sessions.events.stream(session.id);

      // Stream is open and buffering. List history before tailing live.
      for await (const event of client.beta.sessions.events.list(session.id)) {
        seenEventIds.add(event.id);
      }

      // Tail live events, skipping anything already seen
      for await (const event of stream) {
        // Preview events (event_start/event_delta) carry no top-level id
        if (event.type === "event_start" || event.type === "event_delta") continue;
        if (seenEventIds.has(event.id)) continue;
        seenEventIds.add(event.id);
        if (event.type === "agent.message") {
          for (const block of event.content) {
            if (block.type === "text") {
              process.stdout.write(block.text);
            }
          }
        } else if (event.type === "session.status_idle") {
          break;
        }
      }
      ```

      ```csharp C#
      using var stream = await client.Beta.Sessions.Events.WithRawResponse.StreamStreaming(session.ID);

      // Stream is open and buffering. List history before tailing live.
      HashSet<string> seenEventIds = [];
      var history = await client.Beta.Sessions.Events.List(session.ID);
      await foreach (var pastEvent in history.Paginate())
      {
          seenEventIds.Add(pastEvent.ID);
      }

      // Tail live events, skipping anything already seen
      await foreach (var streamEvent in stream.Enumerate())
      {
          if (!seenEventIds.Add(streamEvent.ID))
          {
              continue;
          }
          if (streamEvent.Value is BetaManagedAgentsAgentMessageEvent message)
          {
              foreach (var block in message.Content)
              {
                  Console.Write(block.Text);
              }
          }
          else if (streamEvent.Value is BetaManagedAgentsSessionStatusIdleEvent)
          {
              break;
          }
      }
      ```

      ```go Go
      	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
      	defer stream.Close()

      	// Stream is open and buffering. List history before tailing live.
      	seenEventIDs := map[string]struct{}{}
      	history := client.Beta.Sessions.Events.ListAutoPaging(ctx, session.ID, anthropic.BetaSessionEventListParams{})
      	for history.Next() {
      		seenEventIDs[history.Current().ID] = struct{}{}
      	}
      	if err := history.Err(); err != nil {
      		panic(err)
      	}

      	// Tail live events, skipping anything already seen
      tail:
      	for stream.Next() {
      		event := stream.Current()
      		if _, seen := seenEventIDs[event.ID]; seen {
      			continue
      		}
      		seenEventIDs[event.ID] = struct{}{}
      		switch event := event.AsAny().(type) {
      		case anthropic.BetaManagedAgentsAgentMessageEvent:
      			// concrete-typed list: BetaManagedAgentsTextBlock
      			for _, block := range event.Content {
      				fmt.Print(block.Text)
      			}
      		case anthropic.BetaManagedAgentsSessionStatusIdleEvent:
      			break tail
      		}
      	}
      	if err := stream.Err(); err != nil {
      		panic(err)
      	}
      ```

      ```java Java
      try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
          // Stream is open and buffering. List history before tailing live.
          // Every event variant carries `id`; read it from the raw JSON to dedup across variants.
          var seenEventIds = new HashSet<String>();
          for (var pastEvent : client.beta().sessions().events().list(session.id()).autoPager()) {
              if (pastEvent._json().orElseThrow() instanceof JsonObject json) {
                  seenEventIds.add(json.values().get("id").asStringOrThrow());
              }
          }

          // Tail live events; Set.add returns false for already-seen IDs, skipping the replay.
          stream.stream()
              .filter(event -> event._json().orElseThrow() instanceof JsonObject json
                  && seenEventIds.add(json.values().get("id").asStringOrThrow()))
              .takeWhile(event -> !event.isSessionStatusIdle())
              .filter(BetaManagedAgentsStreamSessionEvents::isAgentMessage)
              .forEach(event -> event.asAgentMessage().content().forEach(block -> IO.print(block.text())));
      }
      ```

      ```php PHP
      $stream = $client->beta->sessions->events->streamStream($session->id);

      // Stream is open and buffering. List history before tailing live.
      $seenEventIds = [];
      foreach ($client->beta->sessions->events->list($session->id)->pagingEachItem() as $event) {
          $seenEventIds[$event->id] = true;
      }

      // Tail live events, skipping anything already seen
      foreach ($stream as $event) {
          if (isset($seenEventIds[$event->id])) {
              continue;
          }
          $seenEventIds[$event->id] = true;
          match ($event->type) {
              'agent.message' => array_walk(
                  $event->content,
                  static fn ($block) => $block->type === 'text' ? print($block->text) : null,
              ),
              default => null,
          };
          if ($event->type === 'session.status_idle') {
              break;
          }
      }
      $stream->close();
      ```

      ```ruby Ruby
      stream = client.beta.sessions.events.stream_events(session.id)

      # Stream is open and buffering. List history before tailing live.
      seen_event_ids = Set.new
      client.beta.sessions.events.list(session.id).auto_paging_each { seen_event_ids << it.id }

      # Tail live events, skipping anything already seen — Set#add? returns nil for duplicates
      stream.each do |event|
        next unless seen_event_ids.add?(event.id)
        case event.type
        in :"agent.message"
          event.content.each { print it.text }
        in :"session.status_idle"
          break
        else
          # ignore other event types
        end
      end
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Listing past events">
    Retrieve the full event history for a session:

    <CodeGroup>
      ```bash curl
      curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        -H "content-type: application/json" \
        | jq -r '.data[] | "[\(.type)] \(.processed_at)"'
      ```

      ```bash CLI
      ant beta:sessions:events list --session-id "$SESSION_ID" \
        --format jsonl --transform '{type,processed_at}'
      ```

      ```python Python
      events = client.beta.sessions.events.list(session.id)
      for event in events.data:
          print(f"[{event.type}] {event.processed_at}")
      ```

      ```typescript TypeScript
      const events = await client.beta.sessions.events.list(session.id);
      for (const event of events.data) {
        console.log(`[${event.type}] ${event.processed_at}`);
      }
      ```

      ```csharp C#
      var events = await client.Beta.Sessions.Events.List(session.ID);
      foreach (var sessionEvent in events.Items)
      {
          Console.WriteLine($"[{sessionEvent.Json.GetProperty("type").GetString()}] {sessionEvent.ProcessedAt}");
      }
      ```

      ```go Go
      events, err := client.Beta.Sessions.Events.List(ctx, session.ID, anthropic.BetaSessionEventListParams{})
      if err != nil {
      	panic(err)
      }
      for _, event := range events.Data {
      	fmt.Printf("[%s] %s\n", event.Type, event.ProcessedAt)
      }
      ```

      ```java Java
      var events = client.beta().sessions().events().list(session.id());
      for (var event : events.data()) {
          var eventJson = event._json().orElseThrow().convert(JsonNode.class);
          var processedAt = eventJson.path("processed_at");
          IO.println("[" + eventJson.get("type").asText() + "] "
              + (processedAt.isTextual() ? processedAt.asText() : "null"));
      }
      ```

      ```php PHP
      $events = $client->beta->sessions->events->list($session->id);
      foreach ($events->data as $event) {
          $processedAt = ($event->processedAt ?? null)?->format(DATE_RFC3339) ?? 'null';
          echo "[{$event->type}] {$processedAt}\n";
      }
      ```

      ```ruby Ruby
      events = client.beta.sessions.events.list(session.id)
      events.data.each { puts "[#{it.type}] #{it.processed_at}" }
      ```
    </CodeGroup>

    Pass a `types` filter to return only specific event types:

    <CodeGroup>
      ```bash curl
      curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true&types[]=agent.tool_use&types[]=agent.tool_result" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "anthropic-beta: managed-agents-2026-04-01" \
        | jq -r '.data[] | "[\(.type)] \(.processed_at)"'
      ```

      ```bash CLI
      ant beta:sessions:events list --session-id "$SESSION_ID" \
        --type agent.tool_use --type agent.tool_result \
        --format jsonl --transform '{type,processed_at}'
      ```

      ```python Python
      events = client.beta.sessions.events.list(
          session.id,
          types=["agent.tool_use", "agent.tool_result"],
      )
      for event in events.data:
          print(f"[{event.type}] {event.processed_at}")
      ```

      ```typescript TypeScript
      const events = await client.beta.sessions.events.list(session.id, {
        types: ["agent.tool_use", "agent.tool_result"],
      });
      for (const event of events.data) {
        console.log(`[${event.type}] ${event.processed_at}`);
      }
      ```

      ```csharp C#
      var events = await client.Beta.Sessions.Events.List(session.ID, new()
      {
          Types = ["agent.tool_use", "agent.tool_result"],
      });
      foreach (var sessionEvent in events.Items)
      {
          Console.WriteLine($"[{sessionEvent.Json.GetProperty("type").GetString()}] {sessionEvent.ProcessedAt}");
      }
      ```

      ```go Go
      events, err := client.Beta.Sessions.Events.List(ctx, session.ID, anthropic.BetaSessionEventListParams{
      	Types: []string{"agent.tool_use", "agent.tool_result"},
      })
      if err != nil {
      	panic(err)
      }
      for _, event := range events.Data {
      	fmt.Printf("[%s] %s\n", event.Type, event.ProcessedAt)
      }
      ```

      ```java Java
      var events = client.beta().sessions().events().list(
          session.id(),
          EventListParams.builder()
              .addType("agent.tool_use")
              .addType("agent.tool_result")
              .build());
      for (var event : events.data()) {
          event.agentToolUse().ifPresent(toolUse ->
              IO.println("[" + toolUse.type() + "] " + toolUse.processedAt()));
          event.agentToolResult().ifPresent(toolResult ->
              IO.println("[" + toolResult.type() + "] " + toolResult.processedAt()));
      }
      ```

      ```php PHP
      $events = $client->beta->sessions->events->list(
          $session->id,
          types: ['agent.tool_use', 'agent.tool_result'],
      );
      foreach ($events->data as $event) {
          $processedAt = ($event->processedAt ?? null)?->format(DATE_RFC3339) ?? 'null';
          echo "[{$event->type}] {$processedAt}\n";
      }
      ```

      ```ruby Ruby
      events = client.beta.sessions.events.list(
        session.id,
        types: ["agent.tool_use", "agent.tool_result"]
      )
      events.data.each { puts "[#{it.type}] #{it.processed_at}" }
      ```
    </CodeGroup>
  </Tab>
</Tabs>

## Event deltas

By default, the agent's response text reaches the stream as buffered `agent.message` events, each emitted only after the model request that produced it finishes. Event deltas let you render that text incrementally, as a live preview, while the model is still generating it. A preview is not the response: previews are a best-effort display aid, and the buffered `agent.message` is always the authoritative record. A client that ignores previews still receives a complete, correct stream.

### Opt in to previews

Previews are opt-in per stream connection. Add the `event_deltas[]` query parameter to `GET /v1/sessions/{session_id}/events/stream`, repeating it once for each event type you want previewed. The accepted values are `agent.message` and `agent.thinking`; any other value returns a 400 error. Only the session-level event stream supports the parameter. [Session thread](/docs/en/managed-agents/multi-agent) event streams reject it.

When a previewed event begins, the stream emits an `event_start` carrying the upcoming event's type and `id`:

```json
{
  "type": "event_start",
  "event": {
    "type": "agent.message",
    "id": "sevt_01abc..."
  }
}
```

For `agent.message`, the start is followed by `event_delta` events carrying incremental text. Each delta names the event it extends in `event_id` and the content block it extends in `delta.index`:

```json
{
  "type": "event_delta",
  "event_id": "sevt_01abc...",
  "delta": {
    "type": "content_delta",
    "index": 0,
    "content": {
      "type": "text",
      "text": "Here is the summary"
    }
  }
}
```

When an `agent.thinking` event is previewed, only the `event_start` is emitted. No `event_delta` events follow, and the content arrives in the buffered `agent.thinking` event as usual.

Unlike persisted events, `event_start` and `event_delta` have no `id` or `processed_at` of their own. The only identifier they carry is the `id` of the event they preview.

<Note>
  Event deltas use a different wire format from [Streaming messages](/docs/en/build-with-claude/streaming), and the difference is intentional. A previewed `agent.message` gets a single `event_start` followed only by `event_delta` events. There are no per-content-block start or stop events and no stop event for the previewed event itself. The delta type is `content_delta`, not `content_block_delta`. Accumulator code written for the Messages API does not carry over unchanged.
</Note>

### Accumulate and reconcile

The Python, TypeScript, and Go SDKs include an accumulator helper that keys the preview by the event's `id` and handles the `index` bookkeeping for you. The manual pattern works in every language: in the other SDKs, apply it to the generated event types.

In the manual pattern, treat the preview as a scratch buffer and the buffered event as the record. Key the buffer by `(event_id, index)`. Reconcile per model request: a turn opens with a single `session.status_running` event, then on a turn that completes normally each model request produces, in order, `span.model_request_start`, `event_start`, the `event_delta` events, the buffered `agent.message`, and finally [`span.model_request_end`](/docs/en/managed-agents/reference#event-types) (in the Span events tab). Process each event as it arrives:

1. On `event_start`, note the announced `id`. The identifiers always line up: `event_start.event.id`, every `event_delta.event_id`, and the buffered `agent.message`'s `id` are the same value.
2. On each `event_delta`, append `delta.content.text` to the entry at `(event_id, delta.index)` and render the running text. The first delta for an `index` creates that entry.
3. When the buffered `agent.message` arrives, match it by `id`, discard the accumulated preview, and render the message's content instead.
4. On `span.model_request_end`, close any preview that has not been reconciled by its buffered event. No more deltas are coming for it. If the turn errors or is interrupted, the buffered event may never arrive; `span.model_request_end` still does.

<CodeGroup>
  ```bash curl
  # Opt in to agent.message previews via event_deltas, then accumulate manually.
  exec {stream}< <(
    curl --fail-with-body -sS -N \
      "https://api.anthropic.com/v1/sessions/$SESSION_ID/events/stream?beta=true&event_deltas%5B%5D=agent.message" \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: managed-agents-2026-04-01" \
      -H "accept: text/event-stream"
  )

  curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- >/dev/null <<'EOF'
  {
    "events": [
      {
        "type": "user.message",
        "content": [{"type": "text", "text": "In one short sentence, describe what an event delta is."}]
      }
    ]
  }
  EOF

  # Accumulate deltas keyed by (message id, content index); the final
  # agent.message carries the full text, so it replaces every preview for that id.
  declare -A preview
  while IFS= read -r -u "$stream" event_line; do
    [[ $event_line == data:* ]] || continue
    event_json=${event_line#data: }
    case $(jq -r '.type' <<<"$event_json") in
      event_start)
        preview_id=$(jq -r '.event.id' <<<"$event_json")
        printf '[event_start id=%s]\n' "$preview_id"
        ;;
      event_delta)
        preview_key=$(jq -r '.event_id + ":" + (.delta.index | tostring)' <<<"$event_json")
        preview[$preview_key]+=$(jq -r '.delta.content.text' <<<"$event_json")
        printf '[event_delta] %s\n' "${preview[$preview_key]}"
        ;;
      agent.message)
        msg_id=$(jq -r '.id' <<<"$event_json")
        for preview_key in "${!preview[@]}"; do
          [[ $preview_key == "$msg_id":* ]] && unset "preview[$preview_key]"
        done
        printf '[agent.message id=%s] ' "$msg_id"
        jq -j '.content[] | select(.type == "text") | .text' <<<"$event_json"
        printf '\n'
        ;;
      span.model_request_end)
        for preview_key in "${!preview[@]}"; do
          printf '[closing unreconciled preview for %s]\n' "${preview_key%%:*}"
        done
        preview=()
        ;;
      session.status_idle)
        break
        ;;
    esac
  done
  exec {stream}<&-
  ```

  ```bash CLI
  # This workflow does not translate well to a one-off shell command.
  # Use one of the SDK examples in this code group instead.
  ```

  ```python Python
  # Preview snapshots, keyed by event id. accumulate_managed_agents_event folds each
  # event_start / event_delta into an agent.message snapshot; the buffered
  # agent.message replaces it.
  previews: dict[str, BetaManagedAgentsAgentMessageEvent] = {}

  # Opt in to agent.message previews on this connection
  with client.beta.sessions.events.stream(
      session.id, event_deltas=["agent.message"]
  ) as stream:
      client.beta.sessions.events.send(
          session.id,
          events=[
              {
                  "type": "user.message",
                  "content": [{"type": "text", "text": "Describe the repo in one sentence."}],
              },
          ],
      )

      for event in stream:
          match event.type:
              case "event_start":
                  snapshot = accumulate_managed_agents_event(None, event)
                  if snapshot is not None:
                      previews[event.event.id] = snapshot
                  print(f"event_start             {event.event.type} {event.event.id}")
              case "event_delta":
                  preview = accumulate_managed_agents_event(previews.get(event.event_id), event)
                  if preview is not None:
                      previews[event.event_id] = preview
                      text = "".join(block.text for block in preview.content)
                      print(f"event_delta             preview: {text!r}")
              case "agent.message":
                  # The buffered event is the record: it replaces and closes the preview
                  preview = accumulate_managed_agents_event(previews.pop(event.id, None), event)
                  text = "".join(block.text for block in preview.content)
                  print(f"agent.message           {event.id} {text!r}")
              case "span.model_request_end":
                  # No more deltas are coming. Close any preview whose
                  # buffered event never arrived.
                  for event_id in previews:
                      print(f"span.model_request_end  closing preview for {event_id}")
                  previews.clear()
              case "session.status_idle":
                  break
  ```

  ```typescript TypeScript
  // Preview snapshots, keyed by event id. `accumulateManagedAgentsEvent`
  // folds event_start / event_delta previews into an agent.message snapshot.
  const previews = new Map<string, BetaManagedAgentsAgentMessageEvent>();

  // Opt in to agent.message previews for this connection only
  const stream = await client.beta.sessions.events.stream(session.id, {
    event_deltas: ["agent.message"],
  });
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.message",
        content: [{ type: "text", text: "Summarize the repo README" }]
      }
    ]
  });

  for await (const event of stream) {
    if (event.type === "event_start") {
      // 1. Note the announced id and open the snapshot. Deltas and the
      //    buffered event carry the same id.
      const preview = accumulateManagedAgentsEvent(undefined, event);
      if (preview) previews.set(event.event.id, preview);
      console.log(`event_start             ${event.event.type} ${event.event.id}`);
    } else if (event.type === "event_delta") {
      // 2. Fold the fragment into the snapshot and render it
      const preview = accumulateManagedAgentsEvent(previews.get(event.event_id), event);
      if (preview) {
        previews.set(event.event_id, preview);
        const text = preview.content.map((block) => block.text).join("");
        console.log(`event_delta             preview: ${JSON.stringify(text)}`);
      }
    } else if (event.type === "agent.message") {
      // 3. The buffered event is the record: it replaces and closes the preview
      const message = accumulateManagedAgentsEvent(previews.get(event.id), event);
      previews.delete(event.id);
      const text = message.content.map((block) => block.text).join("");
      console.log(`agent.message           ${event.id} ${JSON.stringify(text)}`);
    } else if (event.type === "span.model_request_end") {
      // 4. No more deltas are coming. Close any preview that was never reconciled.
      for (const eventId of previews.keys()) {
        console.log(`span.model_request_end  closing preview for ${eventId}`);
      }
      previews.clear();
    } else if (event.type === "session.status_idle") {
      break;
    }
  }
  stream.controller.abort();
  ```

  ```csharp C#
  // Opt in to event deltas: agent.message events are previewed as they are produced.
  using var stream = await client.Beta.Sessions.Events.WithRawResponse.StreamStreaming(
      session.ID,
      new() { EventDeltas = [BetaManagedAgentsDeltaType.AgentMessage] }
  );
  await client.Beta.Sessions.Events.Send(session.ID, new()
  {
      Events =
      [
          new BetaManagedAgentsUserMessageEventParams
          {
              Type = BetaManagedAgentsUserMessageEventParamsType.UserMessage,
              Content =
              [
                  new BetaManagedAgentsTextBlock
                  {
                      Type = BetaManagedAgentsTextBlockType.Text,
                      Text = "Write a haiku about event streams.",
                  },
              ],
          },
      ],
  });

  // Accumulate preview fragments per (event id, content index). The buffered
  // agent.message that follows carries the complete content, so it replaces the
  // accumulated preview rather than appending to it.
  Dictionary<string, SortedDictionary<long, string>> previews = [];

  await foreach (var streamEvent in stream.Enumerate())
  {
      if (streamEvent.TryPickStartEvent(out var start))
      {
          // A preview opened for the event with this id
          Console.WriteLine($"event_start             {start.Event.Type} {start.Event.ID}");
      }
      else if (streamEvent.TryPickDeltaEvent(out var delta))
      {
          // Insert at a new index, append at an existing one
          if (!previews.TryGetValue(delta.EventID, out var fragments))
          {
              previews[delta.EventID] = fragments = [];
          }
          var index = delta.Delta.Index ?? 0;
          fragments[index] = fragments.GetValueOrDefault(index, "") + delta.Delta.Content.Text;
          Console.WriteLine($"event_delta             preview: {fragments[index]}");
      }
      else if (streamEvent.TryPickAgentMessageEvent(out var message))
      {
          // Deltas are best-effort: discard the preview and use the buffered event
          previews.Remove(message.ID);
          Console.WriteLine($"agent.message           {message.ID} {string.Concat(message.Content.Select(block => block.Text))}");
      }
      else if (streamEvent.TryPickSpanModelRequestEndEvent(out _))
      {
          // No more deltas are coming; close any preview that was never reconciled.
          foreach (var eventId in previews.Keys)
          {
              Console.WriteLine($"span.model_request_end  closing preview for {eventId}");
          }
          previews.Clear();
      }
      else if (streamEvent.TryPickSessionStatusIdleEvent(out _))
      {
          break;
      }
  }
  ```

  ```go Go
  	// Opt in to incremental previews of agent.message events
  	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{
  		EventDeltas: []anthropic.BetaManagedAgentsDeltaType{
  			anthropic.BetaManagedAgentsDeltaTypeAgentMessage,
  		},
  	})

  	if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  		Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  			OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
  				Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
  				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
  					OfText: &anthropic.BetaManagedAgentsTextBlockParam{
  						Type: anthropic.BetaManagedAgentsTextBlockTypeText,
  						Text: "Write a haiku about the ocean.",
  					},
  				}},
  			},
  		}},
  	}); err != nil {
  		panic(err)
  	}

  	// The accumulator folds event_start / event_delta fragments into
  	// per-event-id agent.message snapshots. The zero value is ready to use.
  	var previews anthropic.BetaManagedAgentsEventAccumulator

  deltas:
  	for stream.Next() {
  		event := stream.Current()
  		previews.Accumulate(event)

  		switch event := event.AsAny().(type) {
  		case anthropic.BetaManagedAgentsStartEvent:
  			fmt.Printf("event_start             %s %s\n", event.Event.Type, event.Event.ID)
  		case anthropic.BetaManagedAgentsDeltaEvent:
  			fmt.Printf("event_delta             preview: %q\n", previews.AgentMessageText(event.EventID))
  		case anthropic.BetaManagedAgentsAgentMessageEvent:
  			// The buffered event carries the complete content: the accumulator
  			// replaces the preview with it
  			fmt.Printf("agent.message           %s %q\n", event.ID, previews.AgentMessageText(event.ID))
  		case anthropic.BetaManagedAgentsSpanModelRequestEndEvent:
  			// No more deltas are coming for this request. The accumulator
  			// drops its snapshots here, closing any preview that was never
  			// reconciled by a buffered agent.message.
  			fmt.Println("span.model_request_end  no more deltas for this request")
  		case anthropic.BetaManagedAgentsSessionStatusIdleEvent:
  			break deltas
  		}
  	}
  	if err := stream.Err(); err != nil {
  		panic(err)
  	}
  	stream.Close()
  ```

  ```java Java
  // Preview text, keyed by event ID then content index. The buffered agent.message replaces it.
  Map<String, Map<Long, StringBuilder>> previews = new HashMap<>();

  // Opt in to agent.message previews on this connection
  try (var stream = client.beta().sessions().events().streamStreaming(
          session.id(),
          EventStreamParams.builder()
              .addEventDelta(BetaManagedAgentsDeltaType.AGENT_MESSAGE)
              .build()
  )) {
      client.beta().sessions().events().send(
          session.id(),
          EventSendParams.builder()
              .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
                  .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
                  .addTextContent("Describe the repo in one sentence.")
                  .build())
              .build()
      );

      Iterable<BetaManagedAgentsStreamSessionEvents> events = stream.stream()::iterator;
      for (var event : events) {
          if (event.isEventStart() && event.asEventStart().event().isAgentMessage()) {
              var preview = event.asEventStart().event().asAgentMessage();
              IO.println("event_start             " + preview.type().asString() + " " + preview.id());
          } else if (event.isEventDelta()) {
              var eventDelta = event.asEventDelta();
              var fragment = eventDelta.delta();
              var buffer = previews
                  .computeIfAbsent(eventDelta.eventId(), _ -> new HashMap<>())
                  .computeIfAbsent(fragment.index().orElse(0L), _ -> new StringBuilder());
              buffer.append(fragment.content().text());
              IO.println("event_delta             preview: " + buffer);
          } else if (event.isAgentMessage()) {
              // The buffered event is the record: drop its preview, render its content
              var message = event.asAgentMessage();
              previews.remove(message.id());
              var text = message.content().stream()
                  .map(block -> block.text())
                  .collect(Collectors.joining());
              IO.println("agent.message           " + message.id() + " " + text);
          } else if (event.isSpanModelRequestEnd()) {
              // No more deltas are coming. Close any preview whose buffered event never arrived.
              previews.keySet().forEach(eventId ->
                  IO.println("span.model_request_end  closing preview for " + eventId));
              previews.clear();
          } else if (event.isSessionStatusIdle()) {
              break;
          }
      }
  }
  ```

  ```php PHP
  // Opt in to event deltas: agent.message previews stream as incremental fragments.
  $stream = $client->beta->sessions->events->streamStream(
      $session->id,
      eventDeltas: [BetaManagedAgentsDeltaType::AGENT_MESSAGE],
  );

  $client->beta->sessions->events->send(
      $session->id,
      events: [
          [
              'type' => 'user.message',
              'content' => [['type' => 'text', 'text' => 'Give a one-sentence project tagline.']],
          ],
      ],
  );

  // Accumulate preview fragments by (event id, index). The buffered agent.message
  // with the same id is authoritative and replaces whatever the deltas built up.
  $buffers = [];

  foreach ($stream as $event) {
      if ($event->type === 'event_start') {
          printf("event_start             %s %s\n", $event->event->type, $event->event->id);
      } elseif ($event->type === 'event_delta') {
          // index is optional on the wire; a single-element preview omits it.
          $index = $event->delta->index ?? 0;
          $fragment = $event->delta->content->text;
          $buffers[$event->eventID][$index] ??= '';
          $buffers[$event->eventID][$index] .= $fragment;
          printf("event_delta             preview: %s\n", json_encode($buffers[$event->eventID][$index]));
      } elseif ($event->type === 'agent.message') {
          // Replace: drop the accumulated preview and render the complete event.
          unset($buffers[$event->id]);
          $text = '';
          foreach ($event->content as $block) {
              if ($block->type === 'text') {
                  $text .= $block->text;
              }
          }
          printf("agent.message           %s %s\n", $event->id, json_encode($text));
      } elseif ($event->type === 'span.model_request_end') {
          // No more deltas are coming. Close any preview that was never reconciled.
          foreach (array_keys($buffers) as $eventID) {
              printf("span.model_request_end  closing preview for %s\n", $eventID);
          }
          $buffers = [];
      } elseif ($event->type === 'session.status_idle') {
          break;
      }
  }
  $stream->close();
  ```

  ```ruby Ruby
  # Opt in to event deltas: agent.message previews stream as incremental fragments.
  stream = client.beta.sessions.events.stream_events(
    session.id,
    event_deltas: [Anthropic::Beta::BetaManagedAgentsDeltaType::AGENT_MESSAGE]
  )

  client.beta.sessions.events.send_(
    session.id,
    events: [{
      type: "user.message",
      content: [{type: "text", text: "Give a one-sentence project tagline."}]
    }]
  )

  # Accumulate preview fragments by (event_id, index) into explicitly mutable
  # (`+""`) buffers so `<<` can append in place. The buffered agent.message with
  # the same id is authoritative and replaces whatever the deltas built up.
  buffers = Hash.new do |by_event, event_id|
    by_event[event_id] = Hash.new { |fragments, index| fragments[index] = +"" }
  end

  stream.each do |event|
    case event.type
    in :event_start
      puts "event_start             #{event.event.type} #{event.event.id}"
    in :event_delta
      delta = event.delta
      fragment = delta.content.text
      buffers[event.event_id][delta.index || 0] << fragment
      puts "event_delta             preview: #{buffers[event.event_id][delta.index || 0].inspect}"
    in :"agent.message"
      # Replace: drop the accumulated preview and render the complete event.
      buffers.delete(event.id)
      puts "agent.message           #{event.id} #{event.content.map(&:text).join.inspect}"
    in :"span.model_request_end"
      # No more deltas are coming. Close any preview that was never reconciled.
      buffers.each_key { |event_id| puts "span.model_request_end  closing preview for #{event_id}" }
      buffers.clear
    in :"session.status_idle"
      break
    else
      # ignore other event types
    end
  end
  ```
</CodeGroup>

### Limitations

Previews are tuned for responsiveness. Build against these constraints:

* **Best effort:** Under load, the server may shed deltas for an event. When it does, you receive a contiguous prefix of the text and then no further deltas for that event. The buffered `agent.message` still arrives complete. Never treat an accumulated preview as final.
* **No replay on reconnect:** Deltas are delivered only to the connection that opted in, while it is open. If the stream drops, follow the [reconnect procedure](#integrating-events) in the Streaming events tab: reopen the stream and list the event history. The history includes any buffered events emitted while you were disconnected, including the `agent.message` your preview was waiting for. There is no way to re-request missed deltas.
* **Primary thread, text only:** Previews cover assistant text on the session's primary thread. Tool use, tool results, MCP results, and activity on other [session threads](/docs/en/managed-agents/multi-agent) are never previewed.
* **Start-only `agent.thinking`:** An `agent.thinking` preview emits only the `event_start` as a signal that a thinking block has started; no `event_delta` events follow it.
* **Never persisted:** `event_start` and `event_delta` exist only on the live stream. They do not appear in the session's event history (`GET /v1/sessions/{session_id}/events`).

## Additional scenarios

### Handling custom tool calls

When the agent invokes a [custom tool](/docs/en/managed-agents/tools#custom-tools):

1. The session emits an `agent.custom_tool_use` event containing the tool name and input.
2. The session pauses with a `session.status_idle` event containing `stop_reason: requires_action`. The blocking event IDs are in the `stop_reason.event_ids` array.
3. Execute the tool in your system and send a `user.custom_tool_result` event for each, passing the event ID in the `custom_tool_use_id` parameter along with the result content.
4. Once all blocking events are resolved, the session transitions back to `running`.

<CodeGroup>
  ```bash curl
  exec {stream_fd}< <(curl --fail-with-body -sS -N \
    "https://api.anthropic.com/v1/sessions/$SESSION_ID/events/stream?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -H "accept: text/event-stream")

  while IFS= read -r -u "$stream_fd" line; do
    [[ $line == data:* ]] || continue
    event_json="${line#data: }"
    stop_reason=$(jq -r 'select(.type == "session.status_idle") | .stop_reason.type // empty' <<<"$event_json")
    case "$stop_reason" in
      requires_action)
        while IFS= read -r event_id; do
          # Execute the tool and send the result back
          result=$(call_tool "$event_id")
          jq -n --arg id "$event_id" --arg result "$result" \
            '{events: [{type: "user.custom_tool_result", custom_tool_use_id: $id, content: [{type: "text", text: $result}]}]}' |
            curl --fail-with-body -sS \
              "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
              -H "x-api-key: $ANTHROPIC_API_KEY" \
              -H "anthropic-version: 2023-06-01" \
              -H "anthropic-beta: managed-agents-2026-04-01" \
              -H "content-type: application/json" \
              -d @-
        done < <(jq -r '.stop_reason.event_ids[]' <<<"$event_json")
        ;;
      end_turn)
        break
        ;;
    esac
  done
  exec {stream_fd}<&-
  ```

  ```bash CLI
  # This workflow does not translate well to a one-off shell command.
  # Use one of the SDK examples in this code group instead.
  ```

  ```python Python
  with client.beta.sessions.events.stream(session.id) as stream:
      for event in stream:
          if event.type == "session.status_idle" and (stop_reason := event.stop_reason):
              match stop_reason.type:
                  case "requires_action":
                      for event_id in stop_reason.event_ids:
                          # Look up the custom tool use event and execute it
                          tool_event = events_by_id[event_id]
                          result = call_tool(tool_event.name, tool_event.input)

                          # Send the result back
                          client.beta.sessions.events.send(
                              session.id,
                              events=[
                                  {
                                      "type": "user.custom_tool_result",
                                      "custom_tool_use_id": event_id,
                                      "content": [{"type": "text", "text": result}],
                                  },
                              ],
                          )
                  case "end_turn":
                      break
  ```

  ```typescript TypeScript
  const stream = await client.beta.sessions.events.stream(session.id);

  for await (const event of stream) {
    if (event.type !== "session.status_idle") continue;
    if (event.stop_reason.type === "end_turn") break;
    if (event.stop_reason.type !== "requires_action") continue;

    for (const eventId of event.stop_reason.event_ids) {
      // Look up the custom tool use event and execute it
      const toolEvent = eventsById.get(eventId);
      if (!toolEvent) continue;
      const result = await callTool(toolEvent.name, toolEvent.input);

      // Send the result back
      await client.beta.sessions.events.send(session.id, {
        events: [
          {
            type: "user.custom_tool_result",
            custom_tool_use_id: eventId,
            content: [{ type: "text", text: result }],
          },
        ],
      });
    }
  }
  ```

  ```csharp C#
  await foreach (var streamEvent in client.Beta.Sessions.Events.StreamStreaming(session.ID))
  {
      if (streamEvent.Value is not BetaManagedAgentsSessionStatusIdleEvent idle) continue;

      if (idle.StopReason?.Value is BetaManagedAgentsSessionRequiresAction requiresAction)
      {
          foreach (var eventId in requiresAction.EventIds)
          {
              // Look up the custom tool use event and execute it
              var toolEvent = eventsById[eventId];
              var result = await CallTool(toolEvent.Name, toolEvent.Input);

              // Send the result back
              await client.Beta.Sessions.Events.Send(session.ID, new()
              {
                  Events =
                  [
                      new BetaManagedAgentsUserCustomToolResultEventParams
                      {
                          Type = BetaManagedAgentsUserCustomToolResultEventParamsType.UserCustomToolResult,
                          CustomToolUseID = eventId,
                          Content =
                          [
                              new BetaManagedAgentsTextBlock
                              {
                                  Type = BetaManagedAgentsTextBlockType.Text,
                                  Text = result,
                              },
                          ],
                      },
                  ],
              });
          }
      }
      else if (idle.StopReason?.Value is BetaManagedAgentsSessionEndTurn)
      {
          break;
      }
  }
  ```

  ```go Go
  	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
  	defer stream.Close()

  loop:
  	for stream.Next() {
  		event, ok := stream.Current().AsAny().(anthropic.BetaManagedAgentsSessionStatusIdleEvent)
  		if !ok {
  			continue
  		}
  		switch stopReason := event.StopReason.AsAny().(type) {
  		case anthropic.BetaManagedAgentsSessionRequiresAction:
  			for _, eventID := range stopReason.EventIDs {
  				// Look up the custom tool use event and execute it
  				toolEvent := eventsByID[eventID]
  				result := callTool(toolEvent.Name, toolEvent.Input)
  				// Send the result back
  				if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  					Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  						OfUserCustomToolResult: &anthropic.BetaManagedAgentsUserCustomToolResultEventParams{
  							Type:            anthropic.BetaManagedAgentsUserCustomToolResultEventParamsTypeUserCustomToolResult,
  							CustomToolUseID: eventID,
  							Content: []anthropic.BetaManagedAgentsUserCustomToolResultEventParamsContentUnion{{
  								OfText: &anthropic.BetaManagedAgentsTextBlockParam{
  									Type: anthropic.BetaManagedAgentsTextBlockTypeText,
  									Text: result,
  								},
  							}},
  						},
  					}},
  				}); err != nil {
  					panic(err)
  				}
  			}
  		case anthropic.BetaManagedAgentsSessionEndTurn:
  			break loop
  		}
  	}
  	if err := stream.Err(); err != nil {
  		panic(err)
  	}
  ```

  ```java Java
  try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
      stream.stream()
          .filter(BetaManagedAgentsStreamSessionEvents::isSessionStatusIdle)
          .map(idleEvent -> idleEvent.asSessionStatusIdle().stopReason())
          .takeWhile(stopReason -> !stopReason.isEndTurn())
          .filter(stopReason -> stopReason.isRequiresAction())
          .flatMap(stopReason -> stopReason.asRequiresAction().eventIds().stream())
          .forEach(eventId -> {
              // Look up the custom tool use event and execute it
              var toolEvent = eventsById.get(eventId);
              var result = callTool(toolEvent.name(), toolEvent.input());

              // Send the result back
              client.beta().sessions().events().send(
                  session.id(),
                  EventSendParams.builder()
                      .addEvent(BetaManagedAgentsUserCustomToolResultEventParams.builder()
                          .type(BetaManagedAgentsUserCustomToolResultEventParams.Type.USER_CUSTOM_TOOL_RESULT)
                          .customToolUseId(eventId)
                          .addTextContent(result)
                          .build())
                      .build());
          });
  }
  ```

  ```php PHP
  $stream = $client->beta->sessions->events->streamStream($session->id);

  foreach ($stream as $event) {
      if ($event->type === 'session.status_idle' && $event->stopReason) {
          if ($event->stopReason->type === 'requires_action') {
              foreach ($event->stopReason->eventIDs as $eventId) {
                  // Look up the custom tool use event and execute it
                  $toolEvent = $eventsById[$eventId];
                  $result = callTool($toolEvent->name, $toolEvent->input);

                  // Send the result back
                  $client->beta->sessions->events->send(
                      $session->id,
                      events: [
                          [
                              'type' => 'user.custom_tool_result',
                              'custom_tool_use_id' => $eventId,
                              'content' => [['type' => 'text', 'text' => $result]],
                          ],
                      ],
                  );
              }
          } elseif ($event->stopReason->type === 'end_turn') {
              break;
          }
      }
  }
  ```

  ```ruby Ruby
  client.beta.sessions.events.stream_events(session.id).each do |event|
    case event
    in {type: :"session.status_idle", stop_reason: {type: :requires_action, event_ids:}}
      event_ids.each do |event_id|
        # Look up the custom tool use event and execute it
        tool_event = events_by_id[event_id]
        result = call_tool.call(tool_event.name, tool_event.input)
        # Send the result back
        client.beta.sessions.events.send_(
          session.id,
          events: [
            {
              type: "user.custom_tool_result",
              custom_tool_use_id: event_id,
              content: [{type: "text", text: result}]
            }
          ]
        )
      end
    in {type: :"session.status_idle", stop_reason: {type: :end_turn}}
      break
    else
    end
  end
  ```
</CodeGroup>

### Tool confirmation

When a [permission policy](/docs/en/managed-agents/permission-policies) requires confirmation before a tool executes:

1. The session emits an `agent.tool_use` or `agent.mcp_tool_use` event.
2. The session pauses with a `session.status_idle` event containing `stop_reason: requires_action`. The blocking event IDs are in the `stop_reason.event_ids` array.
3. Send a `user.tool_confirmation` event for each, passing the event ID in the `tool_use_id` parameter. Set `result` to `"allow"` or `"deny"`. Use `deny_message` to explain a denial.
4. Once all blocking events are resolved, the session transitions back to `running`.

<CodeGroup>
  ```bash curl
  exec {stream_fd}< <(curl --fail-with-body -sS -N \
    "https://api.anthropic.com/v1/sessions/$SESSION_ID/events/stream?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -H "accept: text/event-stream")

  while IFS= read -r -u "$stream_fd" line; do
    [[ $line == data:* ]] || continue
    event_json="${line#data: }"
    stop_reason=$(jq -r 'select(.type == "session.status_idle") | .stop_reason.type // empty' <<<"$event_json")
    case "$stop_reason" in
      requires_action)
        while IFS= read -r event_id; do
          # Approve the pending tool call
          jq -n --arg id "$event_id" \
            '{events: [{type: "user.tool_confirmation", tool_use_id: $id, result: "allow"}]}' |
            curl --fail-with-body -sS \
              "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
              -H "x-api-key: $ANTHROPIC_API_KEY" \
              -H "anthropic-version: 2023-06-01" \
              -H "anthropic-beta: managed-agents-2026-04-01" \
              -H "content-type: application/json" \
              -d @-
        done < <(jq -r '.stop_reason.event_ids[]' <<<"$event_json")
        ;;
      end_turn)
        break
        ;;
    esac
  done
  exec {stream_fd}<&-
  ```

  ```bash CLI
  # This workflow does not translate well to a one-off shell command.
  # Use one of the SDK examples in this code group instead.
  ```

  ```python Python
  with client.beta.sessions.events.stream(session.id) as stream:
      for event in stream:
          if event.type == "session.status_idle" and (stop_reason := event.stop_reason):
              match stop_reason.type:
                  case "requires_action":
                      for event_id in stop_reason.event_ids:
                          # Approve the pending tool call
                          client.beta.sessions.events.send(
                              session.id,
                              events=[
                                  {
                                      "type": "user.tool_confirmation",
                                      "tool_use_id": event_id,
                                      "result": "allow",
                                  },
                              ],
                          )
                  case "end_turn":
                      break
  ```

  ```typescript TypeScript
  const stream = await client.beta.sessions.events.stream(session.id);

  for await (const event of stream) {
    if (event.type !== "session.status_idle") continue;
    if (event.stop_reason.type === "end_turn") break;
    if (event.stop_reason.type !== "requires_action") continue;

    for (const eventId of event.stop_reason.event_ids) {
      // Approve the pending tool call
      await client.beta.sessions.events.send(session.id, {
        events: [
          {
            type: "user.tool_confirmation",
            tool_use_id: eventId,
            result: "allow",
          },
        ],
      });
    }
  }
  ```

  ```csharp C#
  await foreach (var streamEvent in client.Beta.Sessions.Events.StreamStreaming(session.ID))
  {
      if (streamEvent.Value is not BetaManagedAgentsSessionStatusIdleEvent idle) continue;

      if (idle.StopReason?.Value is BetaManagedAgentsSessionRequiresAction requiresAction)
      {
          foreach (var eventId in requiresAction.EventIds)
          {
              // Approve the pending tool call
              await client.Beta.Sessions.Events.Send(session.ID, new()
              {
                  Events =
                  [
                      new BetaManagedAgentsUserToolConfirmationEventParams
                      {
                          Type = BetaManagedAgentsUserToolConfirmationEventParamsType.UserToolConfirmation,
                          ToolUseID = eventId,
                          Result = BetaManagedAgentsUserToolConfirmationEventParamsResult.Allow,
                      },
                  ],
              });
          }
      }
      else if (idle.StopReason?.Value is BetaManagedAgentsSessionEndTurn)
      {
          break;
      }
  }
  ```

  ```go Go
  	stream := client.Beta.Sessions.Events.StreamEvents(ctx, session.ID, anthropic.BetaSessionEventStreamParams{})
  	defer stream.Close()

  loop:
  	for stream.Next() {
  		event, ok := stream.Current().AsAny().(anthropic.BetaManagedAgentsSessionStatusIdleEvent)
  		if !ok {
  			continue
  		}
  		switch stopReason := event.StopReason.AsAny().(type) {
  		case anthropic.BetaManagedAgentsSessionRequiresAction:
  			for _, eventID := range stopReason.EventIDs {
  				// Approve the pending tool call
  				if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  					Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  						OfUserToolConfirmation: &anthropic.BetaManagedAgentsUserToolConfirmationEventParams{
  							Type:      anthropic.BetaManagedAgentsUserToolConfirmationEventParamsTypeUserToolConfirmation,
  							ToolUseID: eventID,
  							Result:    anthropic.BetaManagedAgentsUserToolConfirmationEventParamsResultAllow,
  						},
  					}},
  				}); err != nil {
  					panic(err)
  				}
  			}
  		case anthropic.BetaManagedAgentsSessionEndTurn:
  			break loop
  		}
  	}
  	if err := stream.Err(); err != nil {
  		panic(err)
  	}
  ```

  ```java Java
  try (var stream = client.beta().sessions().events().streamStreaming(session.id())) {
      stream.stream()
          .filter(BetaManagedAgentsStreamSessionEvents::isSessionStatusIdle)
          .map(idleEvent -> idleEvent.asSessionStatusIdle().stopReason())
          .takeWhile(stopReason -> !stopReason.isEndTurn())
          .filter(stopReason -> stopReason.isRequiresAction())
          .flatMap(stopReason -> stopReason.asRequiresAction().eventIds().stream())
          // Approve each pending tool call
          .forEach(toolUseId -> client.beta().sessions().events().send(
              session.id(),
              EventSendParams.builder()
                  .addEvent(BetaManagedAgentsUserToolConfirmationEventParams.builder()
                      .type(BetaManagedAgentsUserToolConfirmationEventParams.Type.USER_TOOL_CONFIRMATION)
                      .toolUseId(toolUseId)
                      .result(BetaManagedAgentsUserToolConfirmationEventParams.Result.ALLOW)
                      .build())
                  .build()));
  }
  ```

  ```php PHP
  $stream = $client->beta->sessions->events->streamStream($session->id);

  foreach ($stream as $event) {
      if ($event->type === 'session.status_idle' && $event->stopReason) {
          if ($event->stopReason->type === 'requires_action') {
              foreach ($event->stopReason->eventIDs as $eventId) {
                  // Approve the pending tool call
                  $client->beta->sessions->events->send(
                      $session->id,
                      events: [
                          [
                              'type' => 'user.tool_confirmation',
                              'tool_use_id' => $eventId,
                              'result' => 'allow',
                          ],
                      ],
                  );
              }
          } elseif ($event->stopReason->type === 'end_turn') {
              break;
          }
      }
  }
  ```

  ```ruby Ruby
  client.beta.sessions.events.stream_events(session.id).each do |event|
    case event
    in {type: :"session.status_idle", stop_reason: {type: :requires_action, event_ids:}}
      event_ids.each do |event_id|
        # Approve the pending tool call
        client.beta.sessions.events.send_(
          session.id,
          events: [
            {type: "user.tool_confirmation", tool_use_id: event_id, result: "allow"}
          ]
        )
      end
    in {type: :"session.status_idle", stop_reason: {type: :end_turn}}
      break
    else
    end
  end
  ```
</CodeGroup>

### Resuming an idle session

Sessions persist between interactions. Conversation history is preserved unless the session is explicitly deleted. When a session goes idle, its sandbox is checkpointed, preserving the full sandbox state, including the filesystem, installed packages, and any files the agent created. This allows you to resume cleanly from inactivity.

<Note>
  While session history is persisted until deleted, checkpoints are only preserved for 30 days after the session's last activity. If your workflow requires the full sandbox state (files, installed tools, and so on) to persist beyond 30 days, send periodic `user.message` events to reset the inactivity timer before the checkpoint expires.
</Note>

To resume a session, send a `user.message` event to it as usual:

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  # In production, pass the stored ID of the session you want to resume.
  curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "events": [
      {
        "type": "user.message",
        "content": [
          {"type": "text", "text": "Now run the tests against the changes you made earlier."}
        ]
      }
    ]
  }
  EOF
  ```

  ```bash CLI
  # In production, pass the stored ID of the session you want to resume.
  ant beta:sessions:events send --session-id "$SESSION_ID" <<'YAML'
  events:
    - type: user.message
      content:
        - type: text
          text: Now run the tests against the changes you made earlier.
  YAML
  ```

  ```python Python
  # Resume a previously created session by sending it a new user.message event.
  # In production, pass the stored ID of the session you want to resume.
  client.beta.sessions.events.send(
      session.id,
      events=[
          {
              "type": "user.message",
              "content": [
                  {
                      "type": "text",
                      "text": "Now run the tests against the changes you made earlier.",
                  },
              ],
          },
      ],
  )
  ```

  ```typescript TypeScript
  // Resume a previously created session by sending it a new user event.
  // In production, pass the stored ID of the session you want to resume.
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "user.message",
        content: [
          {
            type: "text",
            text: "Now run the tests against the changes you made earlier.",
          },
        ],
      },
    ],
  });
  ```

  ```csharp C#
  // Resume a previously created session by ID. In production, pass the
  // session ID you stored when the session was created.
  await client.Beta.Sessions.Events.Send(session.ID, new()
  {
      Events =
      [
          new BetaManagedAgentsUserMessageEventParams
          {
              Type = BetaManagedAgentsUserMessageEventParamsType.UserMessage,
              Content =
              [
                  new BetaManagedAgentsTextBlock
                  {
                      Type = BetaManagedAgentsTextBlockType.Text,
                      Text = "Now run the tests against the changes you made earlier.",
                  },
              ],
          },
      ],
  });
  ```

  ```go Go
  // Resume a previously created session by sending it a new user.message
  // event. In production, pass the stored ID of the session to resume.
  if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  		OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
  			Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
  			Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
  				OfText: &anthropic.BetaManagedAgentsTextBlockParam{
  					Type: anthropic.BetaManagedAgentsTextBlockTypeText,
  					Text: "Now run the tests against the changes you made earlier.",
  				},
  			}},
  		},
  	}},
  }); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  // Resume a previously created session by ID. In production, pass the
  // session ID you stored when the session was created.
  client.beta().sessions().events().send(
      session.id(),
      EventSendParams.builder()
          .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
              .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
              .addTextContent("Now run the tests against the changes you made earlier.")
              .build())
          .build());
  ```

  ```php PHP
  // Resume a previously created session by sending it a new user.message event.
  // In production, pass the session ID you stored when the session was created.
  $client->beta->sessions->events->send(
      $session->id,
      events: [
          [
              'type' => 'user.message',
              'content' => [
                  [
                      'type' => 'text',
                      'text' => 'Now run the tests against the changes you made earlier.',
                  ],
              ],
          ],
      ],
  );
  ```

  ```ruby Ruby
  # Resuming a session is just sending the next event to it. In production,
  # pass the session ID you stored when the session was created.
  client.beta.sessions.events.send_(
    session.id,
    events: [
      {
        type: "user.message",
        content: [
          {type: "text", text: "Now run the tests against the changes you made earlier."}
        ]
      }
    ]
  )
  ```
</CodeGroup>

### Sending system messages

<Note>
  `system.message` is currently only supported by Claude Opus 4.8. If any model configured on the agent does not support mid-conversation system injection, the event is rejected with a `model_does_not_support_mid_conversation_system` validation error.
</Note>

Send a `system.message` event to update the agent's system prompt between turns. Unlike the `system` field on the agent definition (which is fixed at session creation), `system.message` lets you change the system prompt as the session progresses. Use it when the agent needs updated system-level guidance mid-session: a different persona, revised constraints, or context fetched at runtime that should shape the model's behavior going forward.

<CodeGroup defaultLanguage="CLI">
  ```bash curl
  curl --fail-with-body -sS "https://api.anthropic.com/v1/sessions/$SESSION_ID/events?beta=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "events": [
      {
        "type": "system.message",
        "content": [
          {"type": "text", "text": "The user's current timezone is America/New_York."}
        ]
      }
    ]
  }
  EOF
  ```

  ```bash CLI
  ant beta:sessions:events send --session-id "$SESSION_ID" <<'YAML'
  events:
    - type: system.message
      content:
        - type: text
          text: "The user's current timezone is America/New_York."
  YAML
  ```

  ```python Python
  client.beta.sessions.events.send(
      session.id,
      events=[
          {
              "type": "system.message",
              "content": [
                  {
                      "type": "text",
                      "text": "The user's current timezone is America/New_York.",
                  },
              ],
          },
      ],
  )
  ```

  ```typescript TypeScript
  await client.beta.sessions.events.send(session.id, {
    events: [
      {
        type: "system.message",
        content: [
          {
            type: "text",
            text: "The user's current timezone is America/New_York.",
          },
        ],
      },
    ],
  });
  ```

  ```csharp C#
  await client.Beta.Sessions.Events.Send(session.ID, new()
  {
      Events =
      [
          new BetaManagedAgentsSystemMessageEventParams
          {
              Type = BetaManagedAgentsSystemMessageEventParamsType.SystemMessage,
              Content =
              [
                  new BetaManagedAgentsSystemContentBlock
                  {
                      Type = BetaManagedAgentsSystemContentBlockType.Text,
                      Text = "The user's current timezone is America/New_York.",
                  },
              ],
          },
      ],
  });
  ```

  ```go Go
  if _, err := client.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
  	Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  		OfSystemMessage: &anthropic.BetaManagedAgentsSystemMessageEventParams{
  			Type: anthropic.BetaManagedAgentsSystemMessageEventParamsTypeSystemMessage,
  			Content: []anthropic.BetaManagedAgentsSystemContentBlockParam{{
  				Type: anthropic.BetaManagedAgentsSystemContentBlockTypeText,
  				Text: "The user's current timezone is America/New_York.",
  			}},
  		},
  	}},
  }); err != nil {
  	panic(err)
  }
  ```

  ```java Java
  client.beta().sessions().events().send(
      session.id(),
      EventSendParams.builder()
          .addEvent(BetaManagedAgentsSystemMessageEventParams.builder()
              .type(BetaManagedAgentsSystemMessageEventParams.Type.SYSTEM_MESSAGE)
              .addTextContent("The user's current timezone is America/New_York.")
              .build())
          .build());
  ```

  ```php PHP
  $client->beta->sessions->events->send(
      $session->id,
      events: [
          [
              'type' => 'system.message',
              'content' => [
                  [
                      'type' => 'text',
                      'text' => "The user's current timezone is America/New_York.",
                  ],
              ],
          ],
      ],
  );
  ```

  ```ruby Ruby
  client.beta.sessions.events.send_(
    session.id,
    events: [
      {
        type: "system.message",
        content: [
          {type: "text", text: "The user's current timezone is America/New_York."}
        ]
      }
    ]
  )
  ```
</CodeGroup>

`system.message` cannot be sent while the session is idle with `stop_reason: requires_action`. `content` accepts 1–1000 text items.

### Tracking usage

The session object includes a `usage` field with cumulative token statistics. Fetch the session after it goes idle to read the latest totals, and use them to track costs, enforce budgets, or monitor consumption.

```json
{
  "id": "sesn_01...",
  "status": "idle",
  "usage": {
    "input_tokens": 5000,
    "output_tokens": 3200,
    "cache_creation_input_tokens": 2000,
    "cache_read_input_tokens": 20000
  }
}
```

`input_tokens` reports uncached input tokens and `output_tokens` reports total output tokens across all model calls in the session. The `cache_creation_input_tokens` and `cache_read_input_tokens` fields reflect prompt caching activity. Cache entries use a 5-minute TTL, so back-to-back turns within that window benefit from cache reads, which reduce per-token cost.

## Console observability

The Console provides a visual timeline view of your agent sessions. Navigate to the Claude Managed Agents section in the Console to see:

* **Session list:** All sessions with their status, creation time, and model
* **Tracing view:** A chronological view of events (content, timestamps, token usage) within a session. Tracing views are only accessible to Developers and Admins.
* **Tool execution:** Details of each tool call and its result

## Debugging tips

* **Check session events:** Session errors are conveyed through the `session.error` event
* **Review tool results:** Tool execution failures often explain unexpected agent behavior
* **Track token usage:** Monitor token consumption to optimize prompts and reduce costs
* **Use system prompts:** Add logging instructions to the system prompt to make the agent explain its reasoning
